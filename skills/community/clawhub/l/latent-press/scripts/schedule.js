#!/usr/bin/env node
// Print the exact command that schedules the nightly Latent Press run on your runtime.
// It prints, it never executes: creating a cron is the operator's call, and a wrong cron
// is worse than none. Run the output yourself if your runtime lets you, or hand it over.
//
// Usage: node schedule.js <runtime> [--at HH:MM] [--tz Area/City] [--deliver target] [--prompt "..."]
//   runtimes: hermes | openclaw | claude-code | codex | cron

const path = require('path');

const RUNTIMES = ['hermes', 'openclaw', 'claude-code', 'codex', 'cron'];
const DEFAULT_TIME = '02:30';
const NIGHTLY_PROMPT = 'Run the latent-press skill: resume, write the next chapter, end with the link.';
const SKILL_DIR = process.env.CLAUDE_SKILL_DIR || path.join(__dirname, '..');

const USAGE = `Usage: node schedule.js <runtime> [options]

Runtimes:
  hermes        hermes cron create (delivers to a chat; cron expression is UTC)
  openclaw      openclaw automations create (delivers to a channel; --tz sets the zone)
  claude-code   crontab line running \`claude -p\`, or a /schedule routine
  codex         crontab line running \`codex exec\`
  cron          crontab line for any other agent CLI

Options:
  --at HH:MM            Local time to run each night (default ${DEFAULT_TIME})
  --tz Area/City        IANA timezone the time is in (default: this machine's)
  --deliver <target>    Where the final message goes: telegram:<chat_id>, discord:<channel>, ...
  --prompt "..."        Override the nightly prompt
  --agent "<command>"   cron runtime only: the command that starts your agent with a prompt

Nothing is executed. Copy the printed command, check it, run it where the agent lives.`;

function parseArgs(args) {
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--') && i + 1 < args.length) opts[args[i].slice(2)] = args[++i];
  }
  return opts;
}

function parseTime(raw) {
  const match = /^(\d{1,2}):(\d{2})$/.exec(raw || '');
  const hour = match ? Number(match[1]) : NaN;
  const minute = match ? Number(match[2]) : NaN;
  if (!match || hour > 23 || minute > 59) {
    console.error(`Invalid --at "${raw}". Use HH:MM, e.g. 02:30.`);
    process.exit(1);
  }
  return { hour, minute };
}

function localTimezone() {
  return Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
}

// Convert a wall-clock time in tz to UTC for today's offset. Good enough for a nightly job;
// the printed note tells the operator to re-check after a DST change.
function toUtc({ hour, minute }, tz) {
  const now = new Date();
  const probe = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), hour, minute));
  const parts = new Intl.DateTimeFormat('en-US', { timeZone: tz, hour: 'numeric', minute: 'numeric', hour12: false }).formatToParts(probe);
  const localHour = Number(parts.find((p) => p.type === 'hour').value) % 24;
  const localMinute = Number(parts.find((p) => p.type === 'minute').value);
  const offsetMinutes = (localHour * 60 + localMinute) - (hour * 60 + minute);
  const utcMinutes = (((hour * 60 + minute) - offsetMinutes) % 1440 + 1440) % 1440;
  return { hour: Math.floor(utcMinutes / 60), minute: utcMinutes % 60 };
}

function cronExpr({ hour, minute }) {
  return `${minute} ${hour} * * *`;
}

function sh(value) {
  return `"${String(value).replace(/(["\\$`])/g, '\\$1')}"`;
}

function section(title, lines) {
  console.log(`\n${title}`);
  console.log('-'.repeat(title.length));
  for (const line of lines) console.log(line);
}

const runtimes = {
  hermes({ time, tz, deliver, prompt }) {
    const utc = toUtc(time, tz);
    const target = deliver || 'telegram:<YOUR_CHAT_ID>';
    section('Hermes', [
      `hermes cron create ${sh(cronExpr(utc))} ${sh(prompt)} \\`,
      `  --skill latent-press --deliver ${sh(target)} --name "Latent Press nightly"`,
      '',
      `Hermes cron expressions are UTC. ${pad(time)} ${tz} is ${pad(utc)} UTC today; re-check after a DST change.`,
      deliver ? '' : 'Replace <YOUR_CHAT_ID> with the chat that should receive the nightly link (the id Hermes shows in `hermes cron list` for your other jobs, or your Telegram user id).',
      'The skill must be installed first: `hermes skills install latent-press`, and LATENTPRESS_API_KEY set in the profile .env.',
      'Verify: `hermes cron list`. Trigger once now: `hermes cron run <job-id>`.',
    ].filter(Boolean));
  },

  openclaw({ time, tz, deliver, prompt }) {
    const [channel, to] = (deliver || 'telegram:<YOUR_CHAT_ID>').split(':');
    section('OpenClaw', [
      `openclaw automations create ${sh(cronExpr(time))} ${sh(prompt)} \\`,
      `  --tz ${sh(tz)} --name "Latent Press nightly" \\`,
      `  --announce --channel ${sh(channel)} --to ${sh(to || '<YOUR_CHAT_ID>')}`,
      '',
      `Runs at ${pad(time)} ${tz} (the --tz flag does the conversion).`,
      deliver ? '' : 'Replace <YOUR_CHAT_ID> with the chat that should receive the nightly link.',
      'The skill must be installed first: `openclaw skills add latent-press`, with the key in skills.entries.latent-press.apiKey.',
      'Verify: `openclaw automations list`. Trigger once now: `openclaw automations run <job-id>`.',
    ].filter(Boolean));
  },

  'claude-code'({ time, tz, prompt }) {
    section('Claude Code', [
      'A crontab line on the machine where Claude Code and this skill are installed:',
      '',
      `CRON_TZ=${tz}`,
      `${cronExpr(time)} cd ${sh(path.dirname(SKILL_DIR))} && set -a && . ${sh(path.join(SKILL_DIR, '.env'))} && set +a && claude -p ${sh(prompt)} >> ~/latent-press-nightly.log 2>&1`,
      '',
      `Sources the .env that \`register.js\` wrote beside this skill (chmod 600) instead of putting the key in the crontab line itself.`,
      'Add it with `crontab -e`; the log holds each night\'s final message with the chapter link.',
      'Prefer a cloud routine that runs without your laptop? In Claude Code type `/schedule` and describe it in one line:',
      `  every day at ${pad(time)} ${tz}: ${prompt}`,
      'The routine\'s result is the final message, so the link lands there.',
    ]);
  },

  codex({ time, tz, prompt }) {
    section('Codex', [
      'A crontab line on the machine where Codex and this skill are installed:',
      '',
      `CRON_TZ=${tz}`,
      `${cronExpr(time)} cd ${sh(path.dirname(SKILL_DIR))} && set -a && . ${sh(path.join(SKILL_DIR, '.env'))} && set +a && codex exec ${sh(prompt)} >> ~/latent-press-nightly.log 2>&1`,
      '',
      `Sources the .env that \`register.js\` wrote beside this skill (chmod 600) instead of putting the key in the crontab line itself.`,
      '`codex exec` is the non-interactive, scriptable entry point. Codex app Automations can run the same prompt on a schedule from the app instead.',
    ]);
  },

  cron({ time, tz, prompt, agent }) {
    const start = agent || '<your-agent-command> ' + sh(prompt);
    section('Bare cron', [
      `CRON_TZ=${tz}`,
      `${cronExpr(time)} cd ${sh(path.dirname(SKILL_DIR))} && set -a && . ${sh(path.join(SKILL_DIR, '.env'))} && set +a && ${start} >> ~/latent-press-nightly.log 2>&1`,
      '',
      `Sources the .env that \`register.js\` wrote beside this skill (chmod 600) instead of putting the key in the crontab line itself.`,
      agent ? '' : 'Replace <your-agent-command> with whatever starts your agent with a prompt (pass --agent "..." to fill it in).',
      'Your agent must be able to read this skill folder and must end its run by printing the chapter link; the log is where the human finds it.',
    ].filter(Boolean));
  },
};

function pad({ hour, minute }) {
  return `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`;
}

function main() {
  const [, , runtime, ...rest] = process.argv;
  if (!runtime || runtime === '--help' || runtime === '-h') {
    console.log(USAGE);
    return;
  }
  if (!RUNTIMES.includes(runtime)) {
    console.error(`Unknown runtime "${runtime}". One of: ${RUNTIMES.join(', ')}`);
    process.exit(1);
  }
  const opts = parseArgs(rest);
  const time = parseTime(opts.at || DEFAULT_TIME);
  const tz = opts.tz || localTimezone();
  const prompt = opts.prompt || NIGHTLY_PROMPT;

  console.log(`Nightly Latent Press run at ${pad(time)} ${tz}. Prompt:\n  ${prompt}`);
  runtimes[runtime]({ time, tz, deliver: opts.deliver, prompt, agent: opts.agent });
  console.log('\nNothing was executed. Run the command above where the agent lives, then confirm the job is listed.');
}

main();
