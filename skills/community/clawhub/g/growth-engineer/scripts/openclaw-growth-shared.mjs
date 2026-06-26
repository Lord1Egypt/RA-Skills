import path from 'node:path';
const BUILTIN_SOURCE_NAMES = ['analytics', 'revenuecat', 'paddle', 'seo', 'sentry', 'coolify', 'feedback'];
const DEFAULT_CONFIG_PATH = 'data/openclaw-growth-engineer/config.json';
function quote(value) {
    const raw = String(value);
    if (/^[a-zA-Z0-9_./:@-]+$/.test(raw)) {
        return raw;
    }
    return `'${raw.replace(/'/g, `'\\''`)}'`;
}
const SERVICE_KIND_ALIASES = {
    analytics: [
        'analytics',
        'analyticscli',
        'telemetry',
    ],
    revenue: [
        'revenuecat',
        'paddle',
        'stripe',
        'lemonsqueezy',
        'lemon-squeezy',
        'purchases',
        'billing',
        'adapty',
        'superwall',
    ],
    seo: [
        'seo',
        'gsc',
        'google-search-console',
        'search-console',
        'dataforseo',
        'organic-search',
        'search',
    ],
    crash: ['sentry', 'glitchtip', 'crashlytics', 'bugsnag', 'datadog', 'rollbar'],
    infrastructure: ['coolify', 'vercel', 'cloudflare', 'deployment', 'deployments', 'hosting', 'infrastructure', 'infra'],
    feedback: [
        'feedback',
        'support',
        'intercom',
        'zendesk',
        'linear',
        'app-store-reviews',
        'app_store_reviews',
        'play-store-reviews',
        'play_console_reviews',
    ],
    store: [
        'asc',
        'asc-cli',
        'app-store-connect',
        'app_store_connect',
        'play-console',
        'play_console',
        'google-play',
        'google_play',
        'appfollow',
        'app-follow',
        'apptweak',
        'app-tweak',
        'aso',
    ],
    acquisition: [
        'apple-search-ads',
        'apple-ads',
        'google-ads',
        'meta-ads',
        'facebook-ads',
        'tiktok-ads',
        'postiz',
        'postiz-api',
        'social-publishing',
        'social-scheduler',
    ],
    lifecycle: ['resend', 'customerio', 'customer-io', 'mailchimp'],
};
export function getBuiltinSourceNames() {
    return [...BUILTIN_SOURCE_NAMES];
}
export function normalizeServiceType(value) {
    return String(value || '')
        .trim()
        .toLowerCase()
        .replace(/[\s/]+/g, '-')
        .replace(/[^a-z0-9._-]/g, '');
}
export function classifyServiceKind(service) {
    const normalized = normalizeServiceType(service);
    for (const [kind, aliases] of Object.entries(SERVICE_KIND_ALIASES)) {
        if (aliases.includes(normalized)) {
            return kind;
        }
    }
    return 'custom';
}
export function normalizeSourceKey(value, fallback = 'source') {
    const normalized = normalizeServiceType(value).replace(/[.-]+/g, '_');
    return normalized || fallback;
}
export function getDefaultSourcePath(key) {
    return `data/openclaw-growth-engineer/${normalizeSourceKey(key)}_summary.json`;
}
export function getDefaultSourceHint(service) {
    const kind = classifyServiceKind(service);
    if (kind === 'analytics') {
        return '- Preferred: AnalyticsCLI bounded query/export written to JSON.\n- For command mode, output summary JSON in the shared signals[] shape.';
    }
    if (kind === 'revenue') {
        return '- Revenue provider summary with monetization deltas, package/offering signals, and churn notes.\n- Command mode should output JSON in the shared signals[] shape.';
    }
    if (kind === 'seo') {
        return '- SEO/acquisition summary from Google Search Console, Bing Webmaster, DataForSEO, or CSV exports.\n- Prefer GSC, Bing Webmaster diagnostics, and cached CSVs; only use paid APIs with an explicit request cap.';
    }
    if (kind === 'crash') {
        return '- Crash/error provider summary with top regressions, affected users, and issue evidence.\n- `issues[]` or shared `signals[]` payloads are both accepted.';
    }
    if (kind === 'infrastructure') {
        return '- Hosting/deployment summary with failed deploys, unhealthy resources, and health-check gaps.\n- Command mode should output JSON in the shared signals[] shape.';
    }
    if (kind === 'feedback') {
        return '- Aggregate app reviews, support tickets, or in-app feedback into recurring themes.\n- `items[]` or shared `signals[]` payloads are both accepted.';
    }
    if (kind === 'store') {
        return '- Store/distribution summary from ASC CLI, Play Console exports, or release tooling.\n- Focus on review trends, release blockers, ratings, and ASO signals.';
    }
    if (kind === 'acquisition') {
        return '- Paid acquisition summary with spend, conversions, CAC, ROAS, campaign quality, and channel movement.\n- Keep campaign/ad/account IDs discoverable instead of hard-coded when possible.';
    }
    if (kind === 'lifecycle') {
        return '- Lifecycle messaging summary with sends, opens/clicks where relevant, bounces, complaints, journeys, campaigns, and conversion signals.\n- Prefer account/workspace-level summaries over individual campaign pins.';
    }
    return '- Any connector is supported when it can produce JSON in the shared `signals[]` shape.\n- Use `issues[]` for crash tools or `items[]` for feedback-like tools when that fits better.';
}
export function getDefaultSourceCommand(service) {
    const normalized = normalizeServiceType(service);
    if (normalized === 'analytics' || normalized === 'analyticscli') {
        return 'node scripts/export-analytics-summary.mjs';
    }
    if (normalized === 'revenuecat' || normalized === 'revenue-cat' || normalized === 'rc') {
        return 'node scripts/export-revenuecat-summary.mjs';
    }
    if (normalized === 'paddle') {
        return 'node scripts/export-paddle-summary.mjs';
    }
    if (normalized === 'seo' ||
        normalized === 'gsc' ||
        normalized === 'google-search-console' ||
        normalized === 'search-console' ||
        normalized === 'dataforseo') {
        return 'node scripts/export-seo-summary.mjs';
    }
    if (normalized === 'sentry') {
        return 'node scripts/export-sentry-summary.mjs';
    }
    if (normalized === 'coolify') {
        return 'node scripts/export-coolify-summary.mjs';
    }
    if (normalized === 'feedback') {
        return 'analyticscli feedback summary --format json';
    }
    if (normalized === 'asc' ||
        normalized === 'asc-cli' ||
        normalized === 'app-store-connect' ||
        normalized === 'app_store_connect') {
        return 'node scripts/export-asc-summary.mjs';
    }
    return null;
}
export function getAutomationConfig(config) {
    const automation = config?.automation && typeof config.automation === 'object' ? config.automation : {};
    const openclawCron = automation.openclawCron && typeof automation.openclawCron === 'object' ? automation.openclawCron : {};
    const openclawCronDelivery = openclawCron.delivery && typeof openclawCron.delivery === 'object' ? openclawCron.delivery : {};
    const openclawCronDeliveryMode = String(openclawCronDelivery.mode || 'announce').trim() || 'announce';
    const hermesCron = automation.hermesCron && typeof automation.hermesCron === 'object' ? automation.hermesCron : {};
    return {
        ...automation,
        openclawCron: {
            enabled: openclawCron.enabled !== false,
            mode: String(openclawCron.mode || 'main').trim() || 'main',
            schedule: String(openclawCron.schedule || '*/30 * * * *').trim() || '*/30 * * * *',
            timezone: String(openclawCron.timezone || process.env.TZ || 'UTC').trim() || 'UTC',
            name: String(openclawCron.name || 'OpenClaw Growth Engineer scheduler').trim() ||
                'OpenClaw Growth Engineer scheduler',
            delivery: {
                enabled: openclawCronDelivery.enabled !== false && openclawCronDeliveryMode !== 'none',
                mode: openclawCronDeliveryMode,
                channel: String(openclawCronDelivery.channel || 'last').trim() || 'last',
                to: String(openclawCronDelivery.to || '').trim(),
            },
        },
        hermesCron: {
            enabled: hermesCron.enabled !== false,
            schedule: String(hermesCron.schedule || openclawCron.schedule || '*/30 * * * *').trim() || '*/30 * * * *',
            name: String(hermesCron.name || 'Hermes Growth Engineer scheduler').trim() ||
                'Hermes Growth Engineer scheduler',
            skill: String(hermesCron.skill || 'growth-engineer').trim() || 'growth-engineer',
            deliver: String(hermesCron.deliver || 'local').trim() || 'local',
            workdir: typeof hermesCron.workdir === 'string' ? hermesCron.workdir.trim() : '',
        },
    };
}
export function deriveStatePathFromConfigPath(configPath) {
    const normalized = String(configPath || DEFAULT_CONFIG_PATH).trim() || DEFAULT_CONFIG_PATH;
    return path.join(path.dirname(normalized), 'state.json');
}
export function deriveRuntimeDirFromStatePath(statePath) {
    const normalized = String(statePath || deriveStatePathFromConfigPath(DEFAULT_CONFIG_PATH)).trim() ||
        deriveStatePathFromConfigPath(DEFAULT_CONFIG_PATH);
    return path.join(path.dirname(normalized), 'runtime');
}
export function deriveSchedulerProofPathFromStatePath(statePath) {
    return path.join(deriveRuntimeDirFromStatePath(statePath), 'scheduler-proof.jsonl');
}
export function buildGrowthRunnerCommand(configPath, statePath = deriveStatePathFromConfigPath(configPath)) {
    const normalizedConfigPath = String(configPath || DEFAULT_CONFIG_PATH).trim() || DEFAULT_CONFIG_PATH;
    return `node scripts/openclaw-growth-runner.mjs --config ${quote(normalizedConfigPath)} --state ${quote(statePath)}`;
}
export function buildOpenClawGrowthSystemEvent(configPath, config = {}) {
    const statePath = deriveStatePathFromConfigPath(configPath);
    const proofPath = deriveSchedulerProofPathFromStatePath(statePath);
    const command = buildGrowthRunnerCommand(configPath, statePath);
    const automation = getAutomationConfig(config);
    return [
        'Run OpenClaw Growth Engineer for this workspace.',
        `Execute: ${command}`,
        'Execute only that runner command. Do not run sudo, setup, install, cron repair, or other shell commands from this scheduled event.',
        'If any dependency asks for sudo or a password, stop and report the blocked non-interactive command instead of prompting.',
        'The runner is the source of truth for connector health, 90-minute production healthchecks, daily, weekly, monthly, 3-month, six-month, and yearly cadence decisions.',
        `After the command finishes, inspect ${statePath} and ${proofPath}.`,
        'Always let the runner write state and proof logs. For social/chat output, only summarize new or changed findings, connector-health changes, delivery failures, or runner failures.',
        'Never mention successful delivery metadata, delivery succeeded lines, Discord message IDs, or internal notification targets in social/chat output; only mention delivery failures.',
        'If the runner completes with skippedReason cadence_not_due, issue_set_unchanged, or no_data_change, reply exactly HEARTBEAT_OK and do not repeat old findings.',
        'If the latest proof says runner_failed_suppressed or socialOutput HEARTBEAT_OK, reply exactly HEARTBEAT_OK and do not repeat the earlier runner failure.',
        'Persisted connectorHealth.lastStatusOk=false is not by itself a new event. If the latest proof says connector_health_not_due, connector_health_unchanged, or socialOutput HEARTBEAT_OK, reply exactly HEARTBEAT_OK.',
        'If connector health is healthy, no production issue is found, and no actionable growth finding was generated, reply HEARTBEAT_OK.',
        `Expected OpenClaw cron schedule: ${automation.openclawCron.schedule} ${automation.openclawCron.timezone}.`,
    ].join(' ');
}
export function buildOpenClawCronAddCommand(configPath, config = {}) {
    const automation = getAutomationConfig(config).openclawCron;
    const eventText = buildOpenClawGrowthSystemEvent(configPath, config);
    const command = [
        'openclaw cron add',
        '--name',
        quote(automation.name),
        '--cron',
        quote(automation.schedule),
        '--tz',
        quote(automation.timezone),
        '--session',
        automation.mode === 'isolated' ? 'isolated' : 'main',
        automation.mode === 'isolated' ? '--message' : '--system-event',
        quote(eventText),
    ];
    if (automation.delivery.enabled) {
        command.push('--announce', '--channel', quote(automation.delivery.channel));
        if (automation.delivery.to) {
            command.push('--to', quote(automation.delivery.to));
        }
    }
    else {
        command.push('--no-deliver');
    }
    if (automation.mode !== 'isolated') {
        command.push('--wake now');
    }
    return command.join(' ');
}
function getOpenClawCronJobId(job) {
    if (!job || typeof job !== 'object')
        return '';
    for (const key of ['id', 'jobId', 'job_id', 'uuid']) {
        const value = job[key];
        if (typeof value === 'string' && value.trim())
            return value.trim();
    }
    return '';
}
export function buildOpenClawCronEditDeliveryCommand(job, config = {}) {
    const automation = getAutomationConfig(config).openclawCron;
    const jobId = typeof job === 'string' ? job.trim() : getOpenClawCronJobId(job);
    if (!jobId)
        return '';
    const command = ['openclaw cron edit', quote(jobId)];
    if (automation.delivery.enabled) {
        command.push('--announce', '--channel', quote(automation.delivery.channel));
        if (automation.delivery.to) {
            command.push('--to', quote(automation.delivery.to));
        }
        command.push('--best-effort-deliver');
    }
    else {
        command.push('--no-deliver');
    }
    return command.join(' ');
}
export function getOpenClawCronEditDeliveryCommandFromInspection(inspection, config = {}) {
    const jobs = Array.isArray(inspection?.jobs) ? inspection.jobs : [];
    for (const job of jobs) {
        const command = buildOpenClawCronEditDeliveryCommand(job, config);
        if (command)
            return command;
    }
    return '';
}
function normalizeCronComparable(value) {
    return String(value || '')
        .replace(/\\"/g, '"')
        .replace(/\\'/g, "'")
        .replace(/\s+/g, ' ')
        .trim();
}
function collectObjects(value, result = []) {
    if (!value || typeof value !== 'object')
        return result;
    if (Array.isArray(value)) {
        for (const item of value)
            collectObjects(item, result);
        return result;
    }
    result.push(value);
    for (const item of Object.values(value))
        collectObjects(item, result);
    return result;
}
function parseJsonMaybe(value) {
    const text = String(value || '').trim();
    if (!text)
        return null;
    try {
        return JSON.parse(text);
    }
    catch {
        const starts = [text.indexOf('{'), text.indexOf('[')].filter((index) => index >= 0);
        if (starts.length === 0)
            return null;
        try {
            return JSON.parse(text.slice(Math.min(...starts)));
        }
        catch {
            return null;
        }
    }
}
export function buildOpenClawCronVerification(configPath, config = {}) {
    const automation = getAutomationConfig(config).openclawCron;
    const statePath = deriveStatePathFromConfigPath(configPath);
    const proofPath = deriveSchedulerProofPathFromStatePath(statePath);
    return {
        name: automation.name,
        schedule: automation.schedule,
        timezone: automation.timezone,
        delivery: automation.delivery,
        statePath,
        proofPath,
        requiredFragments: [
            automation.name,
            automation.schedule,
            automation.timezone,
            'Run OpenClaw Growth Engineer for this workspace',
            'openclaw-growth-runner.mjs',
            '--config',
            configPath,
            '--state',
            statePath,
            proofPath,
            'HEARTBEAT_OK',
        ],
    };
}
function hasExpectedOpenClawCronDelivery(job, verification) {
    const expected = verification?.delivery || {};
    const delivery = job && typeof job === 'object' && job.delivery && typeof job.delivery === 'object'
        ? job.delivery
        : null;
    if (!expected.enabled) {
        if (!delivery)
            return true;
        const mode = String(delivery.mode || '').trim().toLowerCase();
        return delivery.enabled === false || mode === 'none' || mode === 'disabled';
    }
    if (delivery) {
        const mode = String(delivery.mode || '').trim().toLowerCase();
        if (delivery.enabled === false || mode === 'none' || mode === 'disabled')
            return false;
        if (mode && mode !== 'announce')
            return false;
        const expectedChannel = String(expected.channel || '').trim();
        const actualChannel = String(delivery.channel || '').trim();
        if (expectedChannel && expectedChannel !== 'last' && actualChannel !== expectedChannel)
            return false;
        const expectedTo = String(expected.to || '').trim();
        if (expectedTo && String(delivery.to || '').trim() !== expectedTo)
            return false;
        return true;
    }
    const blob = normalizeCronComparable(JSON.stringify(job || {}));
    const required = ['announce'];
    const expectedChannel = String(expected.channel || '').trim();
    if (expectedChannel && expectedChannel !== 'last')
        required.push(expectedChannel);
    if (expected.to)
        required.push(String(expected.to));
    return required.every((fragment) => blob.includes(normalizeCronComparable(fragment)));
}
export function evaluateOpenClawCronRecords(records, verification) {
    const objects = collectObjects(records);
    const directJobs = objects.filter((job) => {
        const directName = typeof job.name === 'string' ? job.name : typeof job.title === 'string' ? job.title : '';
        return directName === verification.name;
    });
    const jobs = directJobs.length > 0 ? directJobs : objects.filter((job) => {
        return normalizeCronComparable(JSON.stringify(job)).includes(normalizeCronComparable(verification.name));
    });
    if (jobs.length === 0) {
        return { exists: false, verified: false, reason: 'not_found', jobs: [] };
    }
    let deliveryMismatch = false;
    for (const job of jobs) {
        const blob = normalizeCronComparable(JSON.stringify(job));
        const missing = verification.requiredFragments.filter((fragment) => !blob.includes(normalizeCronComparable(fragment)));
        if (missing.length === 0) {
            if (hasExpectedOpenClawCronDelivery(job, verification)) {
                return { exists: true, verified: true, reason: 'verified', jobs };
            }
            deliveryMismatch = true;
        }
    }
    return { exists: true, verified: false, reason: deliveryMismatch ? 'delivery_mismatch' : 'missing_required_fragments', jobs };
}
export function evaluateOpenClawCronText(text, verification) {
    const blob = normalizeCronComparable(text);
    if (!blob.includes(normalizeCronComparable(verification.name))) {
        return { exists: false, verified: false, reason: 'not_found' };
    }
    const missing = verification.requiredFragments.filter((fragment) => !blob.includes(normalizeCronComparable(fragment)));
    return {
        exists: true,
        verified: missing.length === 0,
        reason: missing.length === 0 ? 'verified' : 'text_listing_unverified',
    };
}
export async function inspectOpenClawCronInstall({ configPath, config = {}, runCommand, readFile, home = process.env.HOME, }) {
    const verification = buildOpenClawCronVerification(configPath, config);
    for (const command of ['openclaw cron list --json', 'openclaw cron list --format json']) {
        const result = await runCommand(command, 30_000);
        if (!result?.ok)
            continue;
        const parsed = parseJsonMaybe(result.stdout);
        if (!parsed)
            continue;
        const evaluated = evaluateOpenClawCronRecords(parsed, verification);
        if (evaluated.exists) {
            return { ...evaluated, source: command, verification };
        }
    }
    if (readFile && home) {
        const jobStorePaths = [
            path.join(home, '.openclaw', 'cron', 'jobs.json'),
            path.join(home, '.config', 'openclaw', 'cron', 'jobs.json'),
        ];
        for (const filePath of jobStorePaths) {
            try {
                const parsed = parseJsonMaybe(await readFile(filePath, 'utf8'));
                if (!parsed)
                    continue;
                const evaluated = evaluateOpenClawCronRecords(parsed, verification);
                if (evaluated.exists) {
                    return { ...evaluated, source: filePath, verification };
                }
            }
            catch {
                // Ignore missing or unreadable implementation-specific stores.
            }
        }
    }
    const list = await runCommand('openclaw cron list', 30_000);
    if (list?.ok) {
        const evaluated = evaluateOpenClawCronText(list.stdout, verification);
        if (evaluated.exists) {
            return { ...evaluated, source: 'openclaw cron list', verification };
        }
    }
    return { exists: false, verified: false, reason: 'not_found', source: 'openclaw cron list', verification };
}
function normalizeOpenClawCronDeliveryForStore(delivery) {
    return {
        mode: 'announce',
        channel: String(delivery?.channel || 'last').trim() || 'last',
        to: String(delivery?.to || '').trim(),
    };
}
function repairOpenClawCronDeliveryRecords(records, verification) {
    let repaired = 0;
    const objects = collectObjects(records);
    for (const job of objects) {
        if (!job || typeof job !== 'object')
            continue;
        const directName = typeof job.name === 'string' ? job.name : typeof job.title === 'string' ? job.title : '';
        if (directName !== verification.name)
            continue;
        const blob = normalizeCronComparable(JSON.stringify(job));
        const missing = verification.requiredFragments.filter((fragment) => !blob.includes(normalizeCronComparable(fragment)));
        if (missing.length > 0 || hasExpectedOpenClawCronDelivery(job, verification))
            continue;
        job.delivery = normalizeOpenClawCronDeliveryForStore(verification.delivery);
        repaired += 1;
    }
    return repaired;
}
export async function repairOpenClawCronDeliveryStore({ configPath, config = {}, readFile, writeFile, home = process.env.HOME, }) {
    if (!readFile || !writeFile || !home) {
        return { ok: false, repaired: false, reason: 'missing_io' };
    }
    const verification = buildOpenClawCronVerification(configPath, config);
    const jobStorePaths = [
        path.join(home, '.openclaw', 'cron', 'jobs.json'),
        path.join(home, '.config', 'openclaw', 'cron', 'jobs.json'),
    ];
    for (const filePath of jobStorePaths) {
        let raw = '';
        let parsed = null;
        try {
            raw = await readFile(filePath, 'utf8');
            parsed = parseJsonMaybe(raw);
        }
        catch {
            continue;
        }
        if (!parsed)
            continue;
        const repairedCount = repairOpenClawCronDeliveryRecords(parsed, verification);
        if (repairedCount === 0)
            continue;
        await writeFile(filePath, `${JSON.stringify(parsed, null, 2)}\n`, 'utf8');
        return { ok: true, repaired: true, repairedCount, path: filePath, verification };
    }
    return { ok: true, repaired: false, reason: 'not_found', verification };
}
export function buildHermesGrowthPrompt(configPath, config = {}) {
    const statePath = deriveStatePathFromConfigPath(configPath);
    const proofPath = deriveSchedulerProofPathFromStatePath(statePath);
    const command = buildGrowthRunnerCommand(configPath, statePath);
    const automation = getAutomationConfig(config);
    return [
        'Run Growth Engineer for this workspace.',
        `Execute: ${command}`,
        'The runner is the source of truth for connector health, daily, weekly, monthly, quarterly, six-month, and yearly cadence decisions.',
        `After the command finishes, inspect ${statePath} and ${proofPath}.`,
        'For social/chat output, only summarize new or changed findings, connector-health changes, delivery failures, or runner failures.',
        'Never mention successful delivery metadata, delivery succeeded lines, Discord message IDs, or internal notification targets in social/chat output; only mention delivery failures.',
        'Persisted connectorHealth.lastStatusOk=false is not by itself a new event. If the latest proof says issue_set_unchanged, no_data_change, connector_health_not_due, connector_health_unchanged, or socialOutput HEARTBEAT_OK, reply exactly HEARTBEAT_OK.',
        'If connector health is healthy, no production issue is found, and no actionable growth finding was generated, reply HEARTBEAT_OK.',
        `Expected Hermes cron schedule: ${automation.hermesCron.schedule}.`,
    ].join(' ');
}
export function buildHermesCronCreateCommand(configPath, config = {}, options = {}) {
    const automation = getAutomationConfig(config).hermesCron;
    const workdir = path.resolve(options.workdir || automation.workdir || process.cwd());
    const prompt = buildHermesGrowthPrompt(configPath, {
        ...config,
        automation: {
            ...config?.automation,
            hermesCron: automation,
        },
    });
    return [
        'hermes cron create',
        quote(automation.schedule),
        quote(prompt),
        '--name',
        quote(automation.name),
        '--skill',
        quote(automation.skill),
        '--deliver',
        quote(automation.deliver),
        '--workdir',
        quote(workdir),
    ].join(' ');
}
export function buildHermesCronVerification(configPath, config = {}, options = {}) {
    const automation = getAutomationConfig(config).hermesCron;
    const statePath = deriveStatePathFromConfigPath(configPath);
    const proofPath = deriveSchedulerProofPathFromStatePath(statePath);
    const workdir = path.resolve(options.workdir || automation.workdir || process.cwd());
    return {
        name: automation.name,
        schedule: automation.schedule,
        workdir,
        statePath,
        proofPath,
        requiredFragments: [
            automation.name,
            automation.schedule,
            automation.skill,
            automation.deliver,
            workdir,
            'Run Growth Engineer for this workspace',
            'openclaw-growth-runner.mjs',
            '--config',
            configPath,
            '--state',
            statePath,
            proofPath,
            'HEARTBEAT_OK',
        ],
    };
}
export async function inspectHermesCronInstall({ configPath, config = {}, runCommand, readFile, home = process.env.HOME, workdir = process.cwd(), }) {
    const verification = buildHermesCronVerification(configPath, config, { workdir });
    if (readFile && home) {
        const jobStorePaths = [
            path.join(home, '.hermes', 'cron', 'jobs.json'),
            path.join(home, '.config', 'hermes', 'cron', 'jobs.json'),
        ];
        for (const filePath of jobStorePaths) {
            try {
                const parsed = parseJsonMaybe(await readFile(filePath, 'utf8'));
                if (!parsed)
                    continue;
                const evaluated = evaluateOpenClawCronRecords(parsed, verification);
                if (evaluated.exists) {
                    return { ...evaluated, source: filePath, verification };
                }
            }
            catch {
                // Ignore missing or unreadable implementation-specific stores.
            }
        }
    }
    const list = await runCommand('hermes cron list', 30_000);
    if (list?.ok) {
        const evaluated = evaluateOpenClawCronText(list.stdout, verification);
        if (evaluated.exists) {
            return { ...evaluated, source: 'hermes cron list', verification };
        }
    }
    return { exists: false, verified: false, reason: 'not_found', source: 'hermes cron list', verification };
}
export function buildExtraSourceConfig(service, options = {}) {
    const normalizedService = normalizeServiceType(service);
    const key = normalizeSourceKey(options.key || normalizedService || `extra_${Date.now()}`);
    const defaultCommand = getDefaultSourceCommand(normalizedService || key);
    const mode = options.mode || (defaultCommand ? 'command' : 'file');
    return {
        key,
        label: options.label || normalizedService || key,
        service: normalizedService || key,
        enabled: options.enabled !== false,
        mode,
        ...(mode === 'command'
            ? { command: options.command || defaultCommand || '' }
            : { path: options.path || getDefaultSourcePath(key) }),
        hint: options.hint || getDefaultSourceHint(normalizedService || key),
        secretEnv: options.secretEnv || null,
    };
}
export function getExtraSources(config) {
    const extra = Array.isArray(config?.sources?.extra) ? config.sources.extra : [];
    const seen = new Set();
    const result = [];
    for (const [index, source] of extra.entries()) {
        if (!source || typeof source !== 'object') {
            continue;
        }
        const key = normalizeSourceKey(source.key || source.name || source.service || `extra_${index + 1}`);
        if (seen.has(key)) {
            continue;
        }
        seen.add(key);
        result.push({
            ...source,
            key,
            label: String(source.label || source.name || source.service || key),
            service: normalizeServiceType(source.service || source.name || key),
            enabled: source.enabled !== false,
            mode: String(source.mode || 'file').toLowerCase() === 'command' ? 'command' : 'file',
            secretEnv: typeof source.secretEnv === 'string' && source.secretEnv.trim()
                ? source.secretEnv.trim()
                : null,
            hint: typeof source.hint === 'string' && source.hint.trim()
                ? source.hint
                : getDefaultSourceHint(source.service || key),
        });
    }
    return result;
}
export function getAllSourceEntries(config) {
    const builtins = getBuiltinSourceNames()
        .filter((name) => Boolean(config?.sources?.[name]))
        .map((name) => {
        const source = config.sources[name];
        return {
            key: name,
            label: name,
            service: normalizeServiceType(source?.service || name),
            builtIn: true,
            ...(source || {}),
        };
    });
    return [...builtins, ...getExtraSources(config).map((source) => ({ ...source, builtIn: false }))];
}
export function getActionMode(config) {
    const configured = normalizeServiceType(config?.actions?.mode || '');
    if (configured === 'pull-request' || configured === 'pull_request' || configured === 'pr') {
        return 'pull_request';
    }
    if (config?.actions?.autoCreatePullRequests === true) {
        return 'pull_request';
    }
    return 'issue';
}
export function getGitHubArtifactModes(config) {
    const modes = [];
    const hasExplicitDestinations = Array.isArray(config?.actions?.outputDestinations);
    const destinations = hasExplicitDestinations
        ? config.actions.outputDestinations.map((value) => normalizeServiceType(value))
        : [];
    const deliveryModes = Array.isArray(config?.deliveries?.github?.modes)
        ? config.deliveries.github.modes.map((value) => normalizeServiceType(value))
        : [];
    if (config?.actions?.autoCreateIssues === true ||
        destinations.includes('github_issue') ||
        deliveryModes.includes('issue')) {
        modes.push('issue');
    }
    if (config?.actions?.autoCreatePullRequests === true ||
        destinations.includes('github_pull_request') ||
        destinations.includes('github-pr') ||
        destinations.includes('draft_pr') ||
        deliveryModes.includes('pull_request') ||
        deliveryModes.includes('pull-request')) {
        modes.push('pull_request');
    }
    if (modes.length === 0 && !hasExplicitDestinations) {
        modes.push(getActionMode(config));
    }
    return [...new Set(modes)];
}
export function shouldAutoCreateGitHubArtifact(config, requestedMode = null) {
    if (config?.actions?.disableAutoCreateGitHubArtifacts === true) {
        return false;
    }
    if (!requestedMode && Array.isArray(config?.actions?.outputDestinations) && getGitHubArtifactModes(config).length === 0) {
        return false;
    }
    const mode = requestedMode || getActionMode(config);
    if (mode === 'pull_request') {
        return config?.actions?.autoCreatePullRequests === true;
    }
    if (config?.actions?.autoCreateIssues === true) {
        return true;
    }
    const tokenEnv = String(config?.secrets?.githubTokenEnv || 'GITHUB_TOKEN').trim();
    const hasToken = Boolean(process.env[tokenEnv]);
    const hasRepo = Boolean(String(config?.project?.githubRepo || '').trim());
    const autoCreateWhenWritable = config?.actions?.autoCreateWhenGitHubWriteAccess !== false;
    return autoCreateWhenWritable && hasToken && hasRepo;
}
export function getGitHubRequirementText(actionMode) {
    if (actionMode === 'pull_request') {
        return 'fine-grained PAT with Pull requests: Read/Write and Contents: Read/Write';
    }
    return 'fine-grained PAT with Issues: Read/Write and Contents: Read';
}
export function getGitHubConnectionSummary(actionMode) {
    if (actionMode === 'pull_request') {
        return 'GitHub auth, repository access, pull-request API read checks, and default-branch metadata checks passed';
    }
    return 'GitHub auth, repository access, and issues API read checks passed';
}
export function getGitHubActionNoun(actionMode) {
    return actionMode === 'pull_request' ? 'pull requests' : 'issues';
}
