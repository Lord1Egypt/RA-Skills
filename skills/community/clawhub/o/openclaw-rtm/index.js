const fs = require('fs');
const path = require('path');
const os = require('os');

// Load .env manually to avoid third-party dependencies
const envPath = path.join(__dirname, '.env');
if (fs.existsSync(envPath)) {
    const envFile = fs.readFileSync(envPath, 'utf8');
    envFile.split(/\r?\n/).forEach(line => {
        const match = line.match(/^\s*([^#\s][^=\s]+)\s*=\s*(.*)?\s*$/);
        if (match) {
            const key = match[1];
            let val = match[2] || '';
            if (val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1);
            else if (val.startsWith("'") && val.endsWith("'")) val = val.slice(1, -1);
            if (!process.env[key]) process.env[key] = val;
        }
    });
}

const RTMClient = require('./rtm-client');

const TOKEN_FILE = path.join(os.homedir(), '.rtm-token.json');
const CREDENTIALS_FILE = path.join(os.homedir(), '.rtm-credentials.json');
const ID_CACHE_FILE = path.join(os.homedir(), '.rtm-id-cache.json');

module.exports = {
    name: 'rtm-skill',
    version: '1.0.0',
    register: function (context) {
        const logger = context.logger || console;
        logger.info('[rtm-skill] registering skill');

        let API_KEY = process.env.RTM_API_KEY || '';
        let SHARED_SECRET = process.env.RTM_SHARED_SECRET || '';

        if ((!API_KEY || !SHARED_SECRET) && fs.existsSync(CREDENTIALS_FILE)) {
            try {
                const creds = JSON.parse(fs.readFileSync(CREDENTIALS_FILE, 'utf8'));
                if (creds.API_KEY) API_KEY = creds.API_KEY;
                if (creds.SHARED_SECRET) SHARED_SECRET = creds.SHARED_SECRET;
            } catch (err) {
                logger.error('[rtm-skill] failed to parse credentials file:', err.message);
            }
        }

        if (!API_KEY || !SHARED_SECRET) {
            logger.warn('[rtm-skill] RTM_API_KEY or RTM_SHARED_SECRET are missing. Set env vars or run `rtm config <api_key> <shared_secret>`.');
        }

        const client = new RTMClient(API_KEY, SHARED_SECRET);

        // Try to load token from disk
        try {
            if (fs.existsSync(TOKEN_FILE)) {
                const data = fs.readFileSync(TOKEN_FILE, 'utf8');
                const parsed = JSON.parse(data);
                if (parsed.token) {
                    client.setToken(parsed.token);
                    logger.info('[rtm-skill] loaded auth token from disk');
                }
            }
        } catch (err) {
            logger.error('[rtm-skill] failed to load token:', err.message);
        }

        // Cache is managed via ID_CACHE_FILE now.

        context.registerCommand && context.registerCommand({
            name: 'rtm',
            description: 'Manage Remember The Milk tasks (rtm config, auth, list, add, note, due, start, postpone, priority, complete, delete)',
            async handler({ argv, reply }) {
                const subcmd = argv[0] || 'list';

                const resolveTask = async (targetId) => {
                    let idMap = {};
                    if (fs.existsSync(ID_CACHE_FILE)) {
                        try { idMap = JSON.parse(fs.readFileSync(ID_CACHE_FILE, 'utf8')); } catch(e){}
                    }
                    let task = idMap[targetId];
                    if (!task) {
                        const all = await client.getTasks('');
                        const found = all.find(t => t.task_id === targetId);
                        if (found) {
                            task = { list_id: found.list_id, taskseries_id: found.taskseries_id, task_id: found.task_id, name: found.name };
                            idMap[targetId] = task;
                            fs.writeFileSync(ID_CACHE_FILE, JSON.stringify(idMap), { mode: 0o600 });
                        }
                    }
                    if (!task) throw new Error(`Task ID ${targetId} not found. Please verify valid task_id via 'rtm list'.`);
                    return task;
                };

                try {
                    if (subcmd === 'config') {
                        const newApiKey = argv[1];
                        const newSecret = argv[2];
                        if (!newApiKey || !newSecret) {
                            throw new Error('Provide both API Key and Shared Secret: rtm config <api_key> <shared_secret>');
                        }
                        fs.writeFileSync(CREDENTIALS_FILE, JSON.stringify({ API_KEY: newApiKey, SHARED_SECRET: newSecret }, null, 2), { mode: 0o600 });
                        // Update in-memory variables to immediately allow auth if needed
                        client.apiKey = newApiKey;
                        client.sharedSecret = newSecret;
                        const msg = `✅ Credentials saved securely to ${CREDENTIALS_FILE}.`;
                        if (reply) await reply(msg);
                        return msg;
                    }

                    if (subcmd === 'auth') {
                        const frob = await client.getFrob();
                        // In a real scenario we might save frob to disk temporarily, but here we'll just ask the user to pass it
                        const url = client.getAuthUrl();
                        const msg = `Please open this URL in your browser to authorize:\n${url}\n\nOnce authorized, run: rtm token ${frob}`;
                        if (reply) await reply(msg);
                        return msg;
                    }

                    if (subcmd === 'token') {
                        const frob = argv[1];
                        if (!frob) throw new Error('You must provide the frob from the auth command: rtm token <frob>');
                        const token = await client.getToken(frob);
                        client.setToken(token);
                        fs.writeFileSync(TOKEN_FILE, JSON.stringify({ token }), { mode: 0o600 });
                        const msg = `Success! RTM is authorized. Token saved securely.`;
                        if (reply) await reply(msg);
                        return msg;
                    }

                    // Require token for the rest
                    if (!client.token) {
                        throw new Error('Not authorized. Run `rtm auth` first.');
                    }

                    if (subcmd === 'list') {
                        const listArg = argv[1] || 'incomplete';
                        let filterStr = '';
                        let limit = null;

                        if (listArg === 'incomplete') {
                            filterStr = 'status:incomplete';
                        } else if (listArg === 'completed') {
                            filterStr = 'status:completed';
                            limit = 100; // 変更: 100件
                        } else if (listArg === 'all') {
                            filterStr = '';
                        } else {
                            // Defaults to incomplete if unknown arg is passed, or we could threat it as a custom filter.
                            filterStr = 'status:incomplete';
                        }

                        let tasks = await client.getTasks(filterStr);
                        
                        if (listArg === 'completed') {
                            // 最新の完了を上位に持ってくるため、完了日時で降順ソート
                            tasks.sort((a, b) => new Date(b.completed || 0) - new Date(a.completed || 0));
                            if (limit && tasks.length > limit) {
                                tasks = tasks.slice(0, limit);
                            }
                        }

                        const listsObj = await client.getLists();

                        // map list ids to names
                        const listMap = {};
                        if (listsObj) {
                            const listsArr = Array.isArray(listsObj) ? listsObj : [listsObj];
                            for (const l of listsArr) {
                                listMap[l.id] = l.name;
                            }
                        }

                        let idMap = {};
                        if (fs.existsSync(ID_CACHE_FILE)) {
                            try { idMap = JSON.parse(fs.readFileSync(ID_CACHE_FILE, 'utf8')); } catch (e) {}
                        }

                        if (tasks.length === 0) {
                            const msg = "No tasks found!";
                            if (reply) await reply(msg);
                            return msg;
                        }

                        let output = `📝 Your Tasks (${listArg === 'completed' ? 'Recent Completed' : listArg === 'all' ? 'All' : 'Incomplete'}):\n`;
                        tasks.forEach((t) => {
                            const tId = t.task_id;
                            idMap[tId] = { list_id: t.list_id, taskseries_id: t.taskseries_id, task_id: t.task_id, name: t.name };

                            const cat = listMap[t.list_id] || 'Inbox';
                            const statusIcon = t.completed ? '✅' : '⬜️';
                            let line = `[${tId}] ${statusIcon} [${cat}] ${t.name}`;

                            const formatTime = (ts) => {
                                if (!ts) return '';
                                const d = new Date(ts);
                                return isNaN(d.getTime()) ? ts : d.toLocaleString();
                            };

                            const extras = [];
                            if (t.priority && t.priority !== 'N') extras.push(`Priority: ${t.priority}`);
                            if (t.due) extras.push(`Due: ${formatTime(t.due)}`);
                            if (t.completed) extras.push(`Completed: ${formatTime(t.completed)}`);
                            if (t.source) extras.push(`Source: ${t.source}`);
                            if (t.tags && t.tags.length > 0) extras.push(`Tags: ${t.tags.join(', ')}`);

                            const validNotes = (t.notes || []).filter(n => n && n.$t).map(n => n.$t).join('; ');
                            if (validNotes) extras.push(`Notes: ${validNotes}`);

                            if (extras.length > 0) {
                                line += ` (${extras.join(' | ')})`;
                            }
                            output += line + '\n';
                        });

                        fs.writeFileSync(ID_CACHE_FILE, JSON.stringify(idMap), { mode: 0o600 });

                        if (reply) await reply(output);
                        return output;
                    }

                    if (subcmd === 'add') {
                        const name = argv.slice(1).join(' ');
                        if (!name) throw new Error('Provide a task name: rtm add <name>');
                        const tl = await client.createTimeline();
                        await client.addTask(tl, name);
                        const msg = `✅ Added task: "${name}"`;
                        if (reply) await reply(msg);
                        return msg;
                    }

                    if (subcmd === 'note') {
                        const targetId = argv[1];
                        const noteText = argv.slice(2).join(' ');
                        if (!targetId || !noteText) throw new Error('Provide a task ID and note text: rtm note <id> <text>');
                        
                        const task = await resolveTask(targetId);
                        const tl = await client.createTimeline();

                        await client.addNote(tl, task.list_id, task.taskseries_id, task.task_id, 'Note', noteText);
                        const msg = `📝 Added note to task "${task.name}": "${noteText}"`;
                        if (reply) await reply(msg);
                        return msg;
                    }

                    if (['due', 'start', 'priority', 'postpone'].includes(subcmd)) {
                        const targetId = argv[1];
                        if (!targetId) throw new Error(`Provide a task ID: rtm ${subcmd} <id> [value]`);
                        
                        const task = await resolveTask(targetId);
                        const tl = await client.createTimeline();
                        let msg = "";

                        if (subcmd === 'due') {
                            const dueStr = argv.slice(2).join(' ') || '';
                            await client.setDueDate(tl, task.list_id, task.taskseries_id, task.task_id, dueStr);
                            msg = dueStr ? `📅 Set due date for "${task.name}" to "${dueStr}"` : `🗑️ Removed due date for "${task.name}"`;
                        } else if (subcmd === 'start') {
                            const startStr = argv.slice(2).join(' ') || '';
                            await client.setStartDate(tl, task.list_id, task.taskseries_id, task.task_id, startStr);
                            msg = startStr ? `⏳ Set start date for "${task.name}" to "${startStr}"` : `🗑️ Removed start date for "${task.name}"`;
                        } else if (subcmd === 'priority') {
                            const p = argv[2];
                            if (!['1', '2', '3', 'N'].includes(p)) throw new Error("Priority must be 1, 2, 3, or N (none).");
                            await client.setPriority(tl, task.list_id, task.taskseries_id, task.task_id, p);
                            msg = `🔥 Set priority for "${task.name}" to ${p}`;
                        } else if (subcmd === 'postpone') {
                            await client.postponeTask(tl, task.list_id, task.taskseries_id, task.task_id);
                            msg = `⏭️ Postponed task: "${task.name}"`;
                        }

                        if (reply) await reply(msg);
                        return msg;
                    }

                    if (subcmd === 'complete' || subcmd === 'delete') {
                        const targetId = argv[1];
                        if (!targetId) throw new Error(`Provide a task ID: rtm ${subcmd} <id>`);
                        
                        const task = await resolveTask(targetId);
                        const tl = await client.createTimeline();

                        if (subcmd === 'complete') {
                            await client.completeTask(tl, task.list_id, task.taskseries_id, task.task_id);
                            const msg = `✔️ Completed task: "${task.name}"`;
                            if (reply) await reply(msg);
                            return msg;
                        } else {
                            await client.deleteTask(tl, task.list_id, task.taskseries_id, task.task_id);
                            const msg = `🗑️ Deleted task: "${task.name}"`;
                            if (reply) await reply(msg);
                            return msg;
                        }
                    }

                    throw new Error(`Unknown subcommand: ${subcmd}`);

                } catch (err) {
                    const msg = `❌ RTM Error: ${err.message}`;
                    logger.error(msg);
                    if (reply) await reply(msg);
                    return msg;
                }
            }
        });
    }
};
