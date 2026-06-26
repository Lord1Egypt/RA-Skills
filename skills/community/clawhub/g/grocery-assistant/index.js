import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, mkdirSync, renameSync } from 'node:fs';
import { homedir } from 'node:os';
import path from 'node:path';
import https from 'node:https';

// ─── Constants ────────────────────────────────────────────────────────────────

const STATUS_NEEDED = 'needed';
const STATUS_HAVE = 'have';
const CALLBACK_PREFIX = 'gchk';
const CALLBACK_TOGGLE = 'tgl';
const CALLBACK_VIEW = 'view';
const VIEW_NEEDED = 'needed';
const VIEW_ALL = 'all';

// ─── Utilities ────────────────────────────────────────────────────────────────

function utcNow() {
    return new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
}

function statePath() {
    const env = process.env.GROCERY_STATE_FILE;
    if (env) return env.replace(/^~/, homedir());
    return path.join(homedir(), '.openclaw', 'data', 'grocery-checklist', 'state.json');
}

function openclawConfigPath() {
    return path.join(homedir(), '.openclaw', 'openclaw.json');
}

// ─── Name normalization ───────────────────────────────────────────────────────

function depluralize(word) {
    if (word.length <= 3) return word;
    if (word.endsWith('ies') && word.length > 4) return word.slice(0, -3) + 'y';
    if (word.endsWith('s') && !word.endsWith('ss')) return word.slice(0, -1);
    return word;
}

function normalizeName(value) {
    let s = value.trim().toLowerCase();
    s = s.replace(/[&+]/g, ' and ');
    s = s.replace(/[^a-z0-9]+/g, ' ');
    s = s.replace(/\s+/g, ' ').trim();
    return s.split(' ').filter(Boolean).map(depluralize).join(' ');
}

function displayName(value) {
    return value.replace(/\s+/g, ' ').trim();
}

function itemIdFor(normalized) {
    return createHash('sha1').update(normalized, 'utf8').digest('hex').slice(0, 10);
}

function splitItemTokens(values) {
    const items = [];
    for (const raw of values) {
        for (const part of raw.split(/,|\n|\band\b/)) {
            const cleaned = displayName(part);
            if (cleaned) items.push(cleaned);
        }
    }
    const seen = new Set();
    const unique = [];
    for (const item of items) {
        const key = normalizeName(item);
        if (!key || seen.has(key)) continue;
        seen.add(key);
        unique.push(item);
    }
    return unique;
}

// ─── Categories ───────────────────────────────────────────────────────────────

const CATEGORY_KEYWORDS = [
    ['Fruits & Vegetables', ['apple', 'banana', 'orange', 'lemon', 'lime', 'tomato', 'onion', 'garlic', 'ginger', 'carrot', 'potato', 'lettuce', 'cucumber', 'capsicum', 'pepper', 'chili', 'coriander', 'spring onion', 'celery', 'mushroom', 'avocado', 'mango', 'grape', 'berry', 'honeydew', 'watermelon', 'melon', 'basil', 'parsley', 'mint', 'spinach', 'broccoli', 'cauliflower', 'zucchini', 'eggplant', 'corn', 'sweet corn', 'pea', 'bean', 'herb']],
    ['Meat & Fish', ['chicken', 'beef', 'pork', 'lamb', 'fish', 'prawn', 'shrimp', 'salmon', 'tuna', 'mackerel', 'turkey', 'duck', 'sausage', 'bacon', 'mince', 'steak']],
    ['Dairy & Eggs', ['milk', 'cheese', 'egg', 'yogurt', 'yoghurt', 'butter', 'cream', 'condensed milk']],
    ['Bakery', ['bread', 'wrap', 'tortilla', 'pita', 'bun', 'roll', 'bagel']],
    ['Staples', ['rice', 'pasta', 'noodle', 'flour', 'sugar', 'salt', 'oil', 'vinegar', 'sauce', 'soy', 'stock', 'broth', 'paste', 'mayonnaise', 'ketchup', 'mustard', 'coconut']],
    ['Spices', ['seasoning', 'spice', 'cumin', 'turmeric', 'paprika', 'curry', 'laksa', 'fajita', 'chili flake', 'chilli flake']],
    ['Beverages', ['tea', 'coffee', 'juice', 'water', 'drink', 'soda', 'cola']],
    ['Snacks & Sweets', ['chocolate', 'biscuit', 'cookie', 'crisp', 'chip', 'marshmallow', 'candy', 'sweet', 'snack']],
];
const CATEGORY_ORDER = [...CATEGORY_KEYWORDS.map(([cat]) => cat), 'Other'];

function categorizeItem(name) {
    const normalized = normalizeName(name);
    for (const [category, keywords] of CATEGORY_KEYWORDS) {
        for (const keyword of keywords) {
            const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            if (new RegExp(`\\b${escaped}\\b`).test(normalized)) return category;
        }
    }
    return 'Other';
}

// ─── HTML helpers ─────────────────────────────────────────────────────────────

function htmlEscape(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// ─── JSON helpers ─────────────────────────────────────────────────────────────

function sortedStringify(value) {
    function replacer(key, val) {
        if (val !== null && typeof val === 'object' && !Array.isArray(val)) {
            return Object.keys(val).sort().reduce((acc, k) => { acc[k] = val[k]; return acc; }, {});
        }
        return val;
    }
    return JSON.stringify(value, replacer, 2) + '\n';
}

function tryParseJson(raw) {
    try { return [JSON.parse(raw), false]; } catch { /* fall through */ }
    // Salvage: scan for end of first balanced JSON object
    let depth = 0, inStr = false, escape = false;
    for (let i = 0; i < raw.length; i++) {
        const c = raw[i];
        if (escape) { escape = false; continue; }
        if (c === '\\' && inStr) { escape = true; continue; }
        if (c === '"') { inStr = !inStr; continue; }
        if (inStr) continue;
        if (c === '{') depth++;
        if (c === '}') {
            depth--;
            if (depth === 0) {
                try { return [JSON.parse(raw.slice(0, i + 1)), true]; } catch { break; }
            }
        }
    }
    return [null, false];
}

// ─── State migration & repair ─────────────────────────────────────────────────

function migrateV1toV2(state) {
    const items = state.items;
    if (!items || typeof items !== 'object') { state.version = 2; return false; }
    const newItems = {};
    let changed = false;
    for (const [oldId, item] of Object.entries(items)) {
        if (!item || typeof item !== 'object') { changed = true; continue; }
        const newNormalized = normalizeName(item.name || '');
        const newId = itemIdFor(newNormalized);
        item.id = newId;
        item.normalized = newNormalized;
        if (newId !== oldId) changed = true;
        if (newId in newItems) {
            const existing = newItems[newId];
            if (item.status === STATUS_NEEDED || existing.status === STATUS_NEEDED) existing.status = STATUS_NEEDED;
            if ((item.updated_at || '') > (existing.updated_at || '')) existing.updated_at = item.updated_at;
        } else {
            newItems[newId] = item;
        }
    }
    state.items = newItems;
    state.version = 2;
    return changed;
}

function pruneCorruptedItems(state) {
    if (!state.items || typeof state.items !== 'object') { state.items = {}; return true; }
    let changed = false;
    for (const [itemId, item] of Object.entries(state.items)) {
        if (!item || typeof item !== 'object') { delete state.items[itemId]; changed = true; continue; }
        const name = String(item.name || '').trim();
        const normalized = name ? normalizeName(name) : '';
        if (/^[0-9a-f]{10}$/.test(normalized) && normalized in state.items && normalized !== itemId) {
            delete state.items[itemId]; changed = true; continue;
        }
        if (name && item.normalized !== normalized) { item.normalized = normalized; changed = true; }
    }
    return changed;
}

// ─── State I/O ────────────────────────────────────────────────────────────────

function loadState(filePath) {
    let raw;
    try { raw = readFileSync(filePath, 'utf-8'); } catch { /* not found */ }
    if (!raw) return { version: 2, updated_at: utcNow(), items: {}, views: {} };

    const [data, repaired] = tryParseJson(raw);
    if (!data || typeof data !== 'object') throw new Error('State file is invalid.');

    data.version ??= 1;
    data.updated_at ??= utcNow();
    data.items ??= {};
    data.views ??= {};

    let needsSave = repaired;
    if ((data.version || 1) < 2) needsSave = migrateV1toV2(data) || needsSave;
    needsSave = pruneCorruptedItems(data) || needsSave;
    if (needsSave) saveState(filePath, data);
    return data;
}

function saveState(filePath, state) {
    state.updated_at = utcNow();
    mkdirSync(path.dirname(filePath), { recursive: true });
    const tmp = `${filePath}.${process.pid}.tmp`;
    writeFileSync(tmp, sortedStringify(state), 'utf-8');
    renameSync(tmp, filePath);
}

// ─── Item CRUD ────────────────────────────────────────────────────────────────

function getOrCreateItem(state, rawName) {
    const name = displayName(rawName);
    const normalized = normalizeName(name);
    if (!normalized) throw new Error('Empty grocery item.');
    const id = itemIdFor(normalized);
    const existing = state.items[id];
    if (existing) {
        existing.normalized = normalized;
        existing.created_at ??= utcNow();
        return existing;
    }
    const item = { id, name, normalized, status: STATUS_NEEDED, created_at: utcNow(), updated_at: utcNow() };
    state.items[id] = item;
    return item;
}

function updateStatus(state, rawItems, status) {
    const changed = [];
    for (const rawName of splitItemTokens(rawItems)) {
        const item = getOrCreateItem(state, rawName);
        if (!item.name) item.name = displayName(rawName);
        item.status = status;
        item.updated_at = utcNow();
        changed.push(item);
    }
    return changed;
}

function removeItems(state, rawItems) {
    const removed = [];
    for (const rawName of splitItemTokens(rawItems)) {
        const id = itemIdFor(normalizeName(rawName));
        const item = state.items[id];
        if (item) { removed.push(item.name); delete state.items[id]; }
    }
    return removed;
}

function mergeItems(state, destinationName, sourceNames) {
    const destId = itemIdFor(normalizeName(destinationName));
    const destExisting = state.items[destId];
    const destination = getOrCreateItem(state, destinationName);
    const statuses = new Set();
    if (destExisting) statuses.add(destination.status || STATUS_HAVE);

    const sourceIds = [];
    for (const rawName of splitItemTokens(sourceNames)) {
        const id = itemIdFor(normalizeName(rawName));
        if (id !== destination.id) sourceIds.push(id);
    }

    const mergedNames = [];
    for (const id of sourceIds) {
        const item = state.items[id];
        if (!item) continue;
        mergedNames.push(item.name || id);
        statuses.add(item.status || STATUS_HAVE);
        delete state.items[id];
    }

    const sourceStatuses = new Set(statuses);
    if (destExisting) sourceStatuses.delete(destination.status || STATUS_HAVE);
    const effective = sourceStatuses.size > 0 ? sourceStatuses : statuses;
    destination.status = effective.has(STATUS_NEEDED) ? STATUS_NEEDED : STATUS_HAVE;
    destination.updated_at = utcNow();
    return { item: destination, merged: mergedNames };
}

function renameItem(state, sourceName, destinationName) {
    const sourceId = itemIdFor(normalizeName(sourceName));
    const source = state.items[sourceId];
    if (!source) throw new Error(`Grocery item not found: ${sourceName}`);
    const result = mergeItems(state, destinationName, [sourceName]);
    result.item.status = source.status || result.item.status || STATUS_HAVE;
    result.item.updated_at = utcNow();
    return result;
}

function sortedItems(state, status) {
    let items = Object.values(state.items);
    if (status === STATUS_NEEDED || status === STATUS_HAVE) {
        items = items.filter(item => item.status === status);
    }
    return items.sort((a, b) => {
        const aLate = a.status !== STATUS_NEEDED ? 1 : 0;
        const bLate = b.status !== STATUS_NEEDED ? 1 : 0;
        if (aLate !== bLate) return aLate - bLate;
        return (a.name || '').toLowerCase().localeCompare((b.name || '').toLowerCase());
    });
}

// ─── Views ────────────────────────────────────────────────────────────────────

function senderKey(account, target, threadId) {
    return `${account}:${target}:${threadId || '-'}`;
}

function resolveView(state, account, target, threadId) {
    const key = senderKey(account, target, threadId);
    const existing = state.views[key];
    if (existing && typeof existing === 'object') {
        existing.mode ??= VIEW_NEEDED;
        existing.account ??= account;
        existing.target ??= target;
        existing.thread_id ??= threadId ?? null;
        return existing;
    }
    const view = { account, target, thread_id: threadId ?? null, mode: VIEW_NEEDED, updated_at: utcNow() };
    state.views[key] = view;
    return view;
}

// ─── Render ───────────────────────────────────────────────────────────────────

function renderMessage(state, mode = VIEW_NEEDED, sessionIds = null) {
    const needed = sortedItems(state, STATUS_NEEDED);
    const have = sortedItems(state, STATUS_HAVE);
    const body = [];
    const buttons = [];

    if (mode === VIEW_ALL) {
        body.push('<b>Pantry</b>', '');
        const allItems = [...needed, ...have];
        if (allItems.length) {
            const byCat = {};
            for (const item of allItems) {
                const cat = categorizeItem(item.name);
                (byCat[cat] ??= []).push(item);
            }
            for (const cat of CATEGORY_ORDER) {
                const catItems = byCat[cat] || [];
                if (!catItems.length) continue;
                const inStock = catItems.filter(i => i.status === STATUS_HAVE).map(i => htmlEscape(i.name));
                const toBuy = catItems.filter(i => i.status === STATUS_NEEDED).map(i => htmlEscape(i.name));
                body.push(`<b>${htmlEscape(cat)}</b>`);
                if (inStock.length) body.push(`in stock: ${inStock.join(', ')}`);
                if (toBuy.length) body.push(`need to buy: ${toBuy.join(', ')}`);
                body.push('');
            }
        } else {
            body.push('Nothing here yet.', '');
        }
        buttons.push([{ text: 'Shopping View', callback_data: `${CALLBACK_PREFIX}:${CALLBACK_VIEW}:${VIEW_NEEDED}` }]);
    } else {
        body.push('Groceries to buy', '');
        const sessionSet = sessionIds instanceof Set ? sessionIds : null;
        const sessionHave = sessionSet ? have.filter(item => sessionSet.has(item.id)) : [];
        const allItems = [...needed, ...sessionHave];
        if (allItems.length) {
            const byCat = {};
            for (const item of allItems) {
                const cat = categorizeItem(item.name);
                (byCat[cat] ??= []).push(item);
            }
            for (const cat of CATEGORY_ORDER) {
                const catItems = byCat[cat] || [];
                if (!catItems.length) continue;
                body.push(`<b>${htmlEscape(cat)}</b>`);
                for (const item of catItems) {
                    if (item.status === STATUS_NEEDED) {
                        body.push(`☐ ${htmlEscape(item.name)}`);
                    } else {
                        body.push(`<s>☑ ${htmlEscape(item.name)}</s>`);
                    }
                }
                body.push('');
            }
        } else {
            body.push('Nothing pending.', '');
        }
        body.push('Tap to check off. Tap again to undo.');

        let row = [];
        for (const item of allItems) {
            const label = item.status === STATUS_NEEDED ? `☐ ${item.name}` : `✅ ${item.name}`;
            row.push({ text: label, callback_data: `${CALLBACK_PREFIX}:${CALLBACK_TOGGLE}:${item.id}` });
            if (row.length === 2) { buttons.push(row); row = []; }
        }
        if (row.length) buttons.push(row);
        buttons.push([{ text: 'Pantry View', callback_data: `${CALLBACK_PREFIX}:${CALLBACK_VIEW}:${VIEW_ALL}` }]);
    }

    return { message: body.join('\n').trim(), buttons };
}

// ─── Telegram API ─────────────────────────────────────────────────────────────

function httpsPost(url, data) {
    return new Promise((resolve, reject) => {
        const urlObj = new URL(url);
        const body = new URLSearchParams(
            Object.entries(data).map(([k, v]) => [k, typeof v === 'object' ? JSON.stringify(v) : String(v)])
        ).toString();
        const req = https.request({
            hostname: urlObj.hostname,
            path: urlObj.pathname,
            method: 'POST',
            family: 4,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': Buffer.byteLength(body),
            },
            timeout: 15_000,
        }, (res) => {
            const chunks = [];
            res.on('data', chunk => chunks.push(chunk));
            res.on('end', () => {
                try { resolve(JSON.parse(Buffer.concat(chunks).toString('utf-8'))); }
                catch { reject(new Error(`Invalid JSON from Telegram API`)); }
            });
        });
        req.on('error', reject);
        req.on('timeout', () => { req.destroy(); reject(new Error('Telegram request timed out')); });
        req.write(body);
        req.end();
    });
}

function resolveTelegramToken(account) {
    const config = JSON.parse(readFileSync(openclawConfigPath(), 'utf-8'));
    const token = config?.channels?.telegram?.accounts?.[account]?.botToken;
    if (!token) throw new Error(`Missing Telegram bot token for account ${account}.`);
    return token;
}

async function telegramApi(method, payload, account) {
    const token = resolveTelegramToken(account);
    const result = await httpsPost(`https://api.telegram.org/bot${token}/${method}`, payload);
    if (!result.ok) throw new Error(result.description || 'Telegram API call failed.');
    return result;
}

async function telegramSendMessage(target, account, text, buttons, threadId) {
    const payload = { chat_id: target, text, parse_mode: 'HTML', reply_markup: { inline_keyboard: buttons } };
    if (threadId) payload.message_thread_id = threadId;
    return telegramApi('sendMessage', payload, account);
}

async function telegramEditMessage(view, account, text, buttons) {
    if (!view.message_id || !view.chat_id) throw new Error('No Telegram checklist message to edit.');
    const payload = {
        chat_id: view.chat_id,
        message_id: view.message_id,
        text,
        parse_mode: 'HTML',
        reply_markup: { inline_keyboard: buttons },
    };
    try {
        return await telegramApi('editMessageText', payload, account);
    } catch (err) {
        if (String(err).toLowerCase().includes('message is not modified')) return { ok: true, not_modified: true };
        throw err;
    }
}

async function telegramDeleteMessage(chatId, messageId, account) {
    if (!chatId || !messageId) return;
    try { await telegramApi('deleteMessage', { chat_id: chatId, message_id: messageId }, account); }
    catch { /* ignore stale messages */ }
}

// ─── View send / edit ─────────────────────────────────────────────────────────

async function sendTelegramView(state, target, account, mode, threadId) {
    const view = resolveView(state, account, target, threadId);
    // Capture old message ref before mutating view
    const oldChatId = view.chat_id;
    const oldMessageId = view.message_id;

    view.mode = mode;
    if (mode === VIEW_NEEDED) {
        view.session_ids = sortedItems(state, STATUS_NEEDED).map(i => i.id);
    }
    const sessionIds = new Set(view.session_ids || []);
    const payload = renderMessage(state, mode, sessionIds);

    await telegramDeleteMessage(oldChatId, oldMessageId, account);

    const result = await telegramSendMessage(target, account, payload.message, payload.buttons, threadId);
    const msgObj = result.result || {};
    Object.assign(view, {
        message_id: msgObj.message_id,
        chat_id: (msgObj.chat || {}).id || target,
        updated_at: utcNow(),
    });
    return { ok: true, view, message: payload.message, buttons: payload.buttons, result };
}

async function editExistingView(state, target, account, threadId, mode) {
    const view = resolveView(state, account, target, threadId);
    const sessionIds = new Set(view.session_ids || []);
    const payload = renderMessage(state, mode, sessionIds);
    const result = await telegramEditMessage(view, account, payload.message, payload.buttons);
    view.mode = mode;
    view.updated_at = utcNow();
    return { ok: true, view, message: payload.message, buttons: payload.buttons, result };
}

async function updateAllViews(state, account) {
    const staleKeys = [];
    for (const [key, view] of Object.entries(state.views)) {
        if (!view || typeof view !== 'object') continue;
        if (view.account !== account || !view.message_id) continue;
        try {
            await editExistingView(state, view.target || '', account, view.thread_id, view.mode || VIEW_NEEDED);
        } catch (err) {
            const msg = String(err).toLowerCase();
            if (msg.includes('message to edit not found') || msg.includes('message_id_invalid') || msg.includes('chat not found')) {
                staleKeys.push(key);
            }
        }
    }
    for (const key of staleKeys) delete state.views[key];
}

// ─── Callbacks ────────────────────────────────────────────────────────────────

function parseCallback(raw) {
    const match = raw.match(/(?:callback_data:\s*)?(gchk:[^\s]+)/);
    const token = match ? match[1].trim() : raw.trim();
    const parts = token.split(':');
    if (parts.length !== 3 || parts[0] !== CALLBACK_PREFIX) return null;
    return [parts[1], parts[2]];
}

async function togglePending(state, itemId, target, account, threadId) {
    const item = state.items[itemId];
    if (!item) throw new Error('Grocery item not found.');
    item.status = item.status === STATUS_NEEDED ? STATUS_HAVE : STATUS_NEEDED;
    item.updated_at = utcNow();
    await updateAllViews(state, account);
    return { ok: true, item: { id: item.id, name: item.name, status: item.status } };
}

async function handleCallback(state, callback, target, account, threadId) {
    const parsed = parseCallback(callback);
    if (!parsed) throw new Error('Unsupported callback payload.');
    const [action, value] = parsed;
    const view = resolveView(state, account, target, threadId);
    if (action === CALLBACK_TOGGLE) {
        return togglePending(state, value, target, account, threadId);
    }
    if (action === CALLBACK_VIEW) {
        const mode = value === VIEW_ALL ? VIEW_ALL : VIEW_NEEDED;
        if (mode === VIEW_NEEDED) view.session_ids = sortedItems(state, STATUS_NEEDED).map(i => i.id);
        if (view.message_id) return editExistingView(state, target, account, threadId, mode);
        return sendTelegramView(state, target, account, mode, threadId);
    }
    throw new Error('Unsupported callback action.');
}

// ─── Plugin registration ──────────────────────────────────────────────────────

export default function register(api) {
    // Intercept gchk: button callbacks instantly, before Claude sees them.
    api.registerInteractiveHandler({
        channel: 'telegram',
        namespace: 'gchk',
        handler: async ({ callback, senderId }) => {
            const target = String(callback.chatId || senderId);
            const fp = statePath();
            let state;
            try { state = loadState(fp); } catch (err) {
                console.error('[grocery-checklist] state load error:', String(err));
                return;
            }
            try {
                await handleCallback(state, callback.data, target, 'grocery', null);
                saveState(fp, state);
            } catch (err) {
                console.error('[grocery-checklist] callback error:', String(err));
            }
        },
    });

    // Expose render as a proper tool so Claude calls it reliably as a
    // function call rather than trying to compose a bash command.
    api.registerTool({
        name: 'render_grocery_view',
        label: 'Render Grocery View',
        description: 'Render the grocery shopping list or pantry view as a Telegram inline-keyboard message. Use mode "needed" for the shopping list, "all" for the full pantry.',
        parameters: {
            type: 'object',
            properties: {
                mode: {
                    type: 'string',
                    enum: ['needed', 'all'],
                    description: '"needed" = shopping list, "all" = pantry view',
                },
            },
            required: [],
        },
        async execute(_toolCallId, params, context) {
            const mode = params?.mode ?? VIEW_NEEDED;
            const account = 'grocery';
            const senderId = context?.senderId ?? context?.message?.senderId;
            const fp = statePath();
            let state;
            try { state = loadState(fp); } catch (err) {
                return { ok: false, error: String(err) };
            }
            try {
                let targets = [];
                if (senderId) {
                    targets = [String(senderId)];
                } else {
                    targets = Object.values(state.views)
                        .filter(v => v && typeof v === 'object' && v.account === account && v.target)
                        .map(v => v.target);
                    if (!targets.length) {
                        const config = JSON.parse(readFileSync(openclawConfigPath(), 'utf-8'));
                        const allow = config?.channels?.telegram?.accounts?.[account]?.allowFrom || [];
                        targets = allow.map(String);
                    }
                }
                if (!targets.length) return { ok: false, error: 'No target to send to.' };
                const results = [];
                for (const target of targets) {
                    results.push(await sendTelegramView(state, target, account, mode, null));
                }
                saveState(fp, state);
                return results.length === 1 ? results[0] : { ok: true, results };
            } catch (err) {
                return { ok: false, error: String(err) };
            }
        },
    }, { name: 'render_grocery_view' });

    api.registerTool({
        name: 'mutate_grocery_items',
        label: 'Mutate Grocery Items',
        description: 'Update grocery state directly. Use action "need" to add or mark items as needed, "have" to mark bought/in stock, "remove" to delete, "rename" to rename one item, and "merge" to merge source items into a destination.',
        parameters: {
            type: 'object',
            properties: {
                action: {
                    type: 'string',
                    enum: ['need', 'have', 'remove', 'rename', 'merge'],
                },
                items: {
                    type: 'array',
                    items: { type: 'string' },
                    description: 'Items for need/have/remove actions.',
                },
                source: {
                    type: 'string',
                    description: 'Source item name for rename.',
                },
                destination: {
                    type: 'string',
                    description: 'Destination item name for rename/merge.',
                },
                sources: {
                    type: 'array',
                    items: { type: 'string' },
                    description: 'Source item names for merge.',
                },
            },
            required: ['action'],
        },
        async execute(_toolCallId, params) {
            const action = params?.action;
            const fp = statePath();
            let state;
            try { state = loadState(fp); } catch (err) {
                return { ok: false, error: String(err) };
            }
            try {
                let result;
                if (action === 'need' || action === 'have' || action === 'remove') {
                    const items = Array.isArray(params?.items) ? params.items.filter(Boolean).map(String) : [];
                    if (!items.length) return { ok: false, error: 'items is required' };
                    if (action === 'remove') {
                        result = { ok: true, removed: removeItems(state, items) };
                    } else {
                        const status = action === 'need' ? STATUS_NEEDED : STATUS_HAVE;
                        const updated = updateStatus(state, items, status);
                        result = { ok: true, updated: updated.map(i => ({ id: i.id, name: i.name, status: i.status })) };
                    }
                } else if (action === 'rename') {
                    const source = params?.source ? String(params.source) : '';
                    const destination = params?.destination ? String(params.destination) : '';
                    if (!source || !destination) return { ok: false, error: 'source and destination are required' };
                    const renamed = renameItem(state, source, destination);
                    result = { ok: true, item: { id: renamed.item.id, name: renamed.item.name, status: renamed.item.status }, renamed: source };
                } else if (action === 'merge') {
                    const destination = params?.destination ? String(params.destination) : '';
                    const sources = Array.isArray(params?.sources) ? params.sources.filter(Boolean).map(String) : [];
                    if (!destination || !sources.length) return { ok: false, error: 'destination and sources are required' };
                    const merged = mergeItems(state, destination, sources);
                    result = { ok: true, item: { id: merged.item.id, name: merged.item.name, status: merged.item.status }, merged: merged.merged };
                } else {
                    return { ok: false, error: `unsupported action: ${String(action)}` };
                }
                saveState(fp, state);
                return result;
            } catch (err) {
                return { ok: false, error: String(err) };
            }
        },
    }, { name: 'mutate_grocery_items' });
}
