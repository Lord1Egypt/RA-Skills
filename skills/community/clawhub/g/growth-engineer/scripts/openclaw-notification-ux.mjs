import { createHash } from 'node:crypto';
const MAX_ITEM_SUMMARY_LENGTH = 260;
const MAX_MARKDOWN_FALLBACK_LENGTH = 3_800;
const MAX_RECOMMENDED_ACTION_LENGTH = 700;
const MAX_EVIDENCE_FILES = 8;
const MAX_SLACK_SECTION_LENGTH = 3_000;
const MAX_SLACK_CONTEXT_LENGTH = 3_000;
const MAX_SLACK_BLOCKS = 50;
const STATE_LABELS = {
    new: 'New',
    changed: 'Changed',
    ongoing: 'Ongoing',
    recovered: 'Recovered',
    summary: 'Summary',
};
const SEVERITY_ICONS = {
    critical: '🔴',
    warning: '🟡',
    info: '🔵',
    success: '🟢',
};
const DISCORD_COLORS = {
    critical: 0xd92d20,
    warning: 0xf79009,
    info: 0x2e90fa,
    success: 0x12b76a,
};
const normalizeWhitespace = (value) => String(value ?? '').replace(/\s+/g, ' ').trim();
const neutralizeMassMentions = (value) => value
    .replace(/@(everyone|here)\b/gi, '@\u200b$1')
    .replace(/<!(channel|everyone|here)(?:\^[^>]*)?>/gi, '@\u200b$1')
    .replace(/<!subteam\^[^>|]+(?:\|[^>]+)?>/gi, '@\u200bgroup')
    .replace(/<@&[A-Za-z0-9]+>/g, '@\u200brole');
const sanitizeCopy = (value) => neutralizeMassMentions(normalizeWhitespace(value))
    .replace(/\bBearer\s+[A-Za-z0-9._~+/=-]+/gi, 'Bearer [redacted]')
    .replace(/\b(token|secret|password|authorization|api[-_ ]?key)\s*[:=]\s*["']?[^\s"',;}]+/gi, '$1=[redacted]')
    .replace(/\/(?:home|Users|private|tmp|var|opt)\/[^\s)"'`]+/g, '[host path]')
    .replace(/\b[A-Za-z]:\\(?:Users|Temp|ProgramData)\\[^\s)"'`]+/gi, '[host path]');
const truncate = (value, maxLength) => {
    const text = sanitizeCopy(value);
    if (text.length <= maxLength)
        return text;
    return `${text.slice(0, Math.max(0, maxLength - 1)).trim()}…`;
};
const truncateRendered = (value, maxLength) => {
    if (value.length <= maxLength)
        return value;
    return `${value.slice(0, Math.max(0, maxLength - 1)).trim()}…`;
};
const escapeMarkdownLabel = (value) => sanitizeCopy(value).replace(/[[\]_*`]/g, '');
const safeHttpUrl = (value) => {
    const raw = normalizeWhitespace(value);
    if (!raw)
        return undefined;
    try {
        const parsed = new URL(raw);
        return ['http:', 'https:'].includes(parsed.protocol)
            ? parsed.toString()
            : undefined;
    }
    catch {
        return undefined;
    }
};
const formatMinutes = (milliseconds) => {
    const minutes = Math.max(1, Math.round(milliseconds / 60_000));
    return `${minutes} ${minutes === 1 ? 'minute' : 'minutes'}`;
};
const safeCount = (value) => {
    const count = Number(value);
    if (!Number.isFinite(count) || count < 0)
        return undefined;
    return Math.min(999_999, Math.floor(count));
};
const safeEvidenceFileName = (value) => {
    let raw = normalizeWhitespace(value);
    if (!raw)
        return undefined;
    try {
        if (/^(?:file|https?):\/\//i.test(raw)) {
            raw = decodeURIComponent(new URL(raw).pathname);
        }
    }
    catch {
        // Fall back to basename extraction from the untrusted input.
    }
    const withoutQuery = raw.split(/[?#]/, 1)[0] || '';
    const fileName = withoutQuery.split(/[\\/]/).filter(Boolean).at(-1);
    if (!fileName || fileName === '.' || fileName === '..')
        return undefined;
    return truncate(fileName, 160) || undefined;
};
const safeEvidence = (evidence) => {
    if (!evidence)
        return undefined;
    const files = Array.from(new Set((Array.isArray(evidence.files) ? evidence.files : [])
        .map((file) => safeEvidenceFileName(file))
        .filter((file) => Boolean(file)))).slice(0, MAX_EVIDENCE_FILES);
    const explicitCount = safeCount(evidence.count);
    const chartCount = safeCount(evidence.chartCount);
    const count = explicitCount ?? (files.length > 0 ? files.length : undefined);
    if (count === undefined && chartCount === undefined && files.length === 0) {
        return undefined;
    }
    return { count, chartCount, files };
};
export const summarizeSocialNotificationEvidence = (evidence) => {
    const safe = safeEvidence(evidence);
    if (!safe)
        return undefined;
    const parts = [];
    if (safe.count !== undefined && safe.count !== safe.chartCount) {
        parts.push(`${safe.count} ${safe.count === 1 ? 'evidence item' : 'evidence items'}`);
    }
    if (safe.chartCount !== undefined) {
        parts.push(`${safe.chartCount} ${safe.chartCount === 1 ? 'chart' : 'charts'}`);
    }
    if (safe.files.length > 0) {
        const visibleFiles = safe.files.slice(0, 4);
        const hiddenFileCount = safe.files.length - visibleFiles.length;
        parts.push(`Files: ${visibleFiles.join(', ')}` +
            (hiddenFileCount > 0 ? ` (+${hiddenFileCount} more)` : ''));
    }
    return parts.join(' · ') || undefined;
};
export const humanizeRecommendedAction = (value) => {
    const raw = normalizeWhitespace(value);
    if (!raw)
        return '';
    const looksLikeJson = ((/^\{[\s\S]*\}$/.test(raw) || /^\[[\s\S]*\]$/.test(raw)) &&
        /[:",]/.test(raw)) ||
        /\{[\s\S]*["'][^"']+["']\s*:/.test(raw);
    if (looksLikeJson) {
        return 'Review the structured error details in the run output.';
    }
    const commandWithoutFormatting = raw
        .replace(/^```(?:shell|bash|sh|zsh|console)?\s*/i, '')
        .replace(/```$/i, '')
        .replace(/^`|`$/g, '')
        .replace(/^\$\s*/, '')
        .trim();
    const looksLikeWizardCommand = /\b(?:growth-engineer|analyticscli)\b[\s\S]*\bwizard\b/i.test(commandWithoutFormatting);
    const startsLikeCommand = /^(?:(?:[A-Za-z_][A-Za-z0-9_]*)=[^\s]+\s+)*(?:npx|npm|pnpm|yarn|bun|node|deno|python(?:3)?|pip(?:3)?|ruby|go|cargo|java|bash|sh|zsh|powershell|cmd|curl|wget|sudo|rm|mv|cp|chmod|chown|git|gh|docker|podman|kubectl|helm|asc|analyticscli)\b/i.test(commandWithoutFormatting);
    const containsEmbeddedCommand = /(?:\b(?:run|execute|command|terminal|shell|fix)\s*:?\s*(?:this\s+)?|[`$]\s*)(?:npx|npm|pnpm|yarn|bun|node|deno|python(?:3)?|pip(?:3)?|ruby|go|cargo|java|bash|sh|zsh|powershell|cmd|curl|wget|sudo|rm|mv|cp|chmod|chown|git|gh|docker|podman|kubectl|helm|asc|analyticscli)\b/i.test(commandWithoutFormatting);
    const containsShellControl = /(?:^|\s)(?:&&|\|\||[|;])(?:\s|$)|(?:^|\s)>\s*\S/.test(commandWithoutFormatting);
    const looksLikeHostPath = /^(?:\/(?:home|Users|private|tmp|var|opt)(?:\/|$)|~\/|[A-Za-z]:[\\/])/.test(commandWithoutFormatting) ||
        /^\[host path\](?:\/|$)/i.test(sanitizeCopy(commandWithoutFormatting));
    if (looksLikeWizardCommand) {
        return 'Open the guided connector setup from a trusted host terminal.';
    }
    if (startsLikeCommand || containsEmbeddedCommand || containsShellControl) {
        return 'Review the suggested command in the trusted run details before executing it.';
    }
    if (looksLikeHostPath) {
        return 'Review the generated run details on the trusted host.';
    }
    return truncate(raw, MAX_RECOMMENDED_ACTION_LENGTH);
};
export const humanizeNotificationIdentifier = (value) => {
    const raw = normalizeWhitespace(value);
    if (!raw)
        return 'Unknown source';
    const known = {
        analyticscli: 'AnalyticsCLI',
        appstoreconnect: 'App Store Connect',
        asc: 'App Store Connect',
        asc_cli: 'App Store Connect export',
        coolify: 'Coolify',
        feedback: 'User feedback',
        github: 'GitHub',
        glitchtip: 'GlitchTip',
        revenuecat: 'RevenueCat',
        sentry: 'Sentry',
    };
    const lookup = raw.toLowerCase().replace(/[\s-]+/g, '_');
    if (known[lookup])
        return known[lookup];
    return raw
        .replace(/[_:-]+/g, ' ')
        .replace(/\b\w/g, (character) => character.toUpperCase());
};
export const humanizeConnectorDiagnostic = (value) => {
    const raw = normalizeWhitespace(value);
    if (!raw)
        return 'Needs attention.';
    const coverage = raw.match(/(?:exist for|coverage[^0-9]*)(\d+)\s*\/\s*(\d+)/i);
    if (coverage) {
        const covered = Number(coverage[1]);
        const total = Number(coverage[2]);
        const missing = Math.max(0, total - covered);
        return `${covered} of ${total} apps are covered${missing > 0 ? `; ${missing} still need setup` : ''}.`;
    }
    const timeout = raw.match(/Timed out after\s+(\d+)ms/i);
    if (timeout) {
        return `Collection timed out after ${formatMinutes(Number(timeout[1]))}.`;
    }
    if (/source collection failed during scheduled run/i.test(raw)) {
        return 'Scheduled collection failed; this run continued without this source.';
    }
    if (/command failed/i.test(raw)) {
        return 'The configured collection command failed.';
    }
    if (/token.*(?:missing|required)|(?:missing|required).*token/i.test(raw)) {
        return 'Authentication is missing or no longer valid.';
    }
    if (/source .*disabled|still disabled/i.test(raw)) {
        return 'The source is disabled.';
    }
    return truncate(raw
        .replace(/\bcommand\s+[^;]+;?/gi, '')
        .replace(/\/(?:home|Users|var|opt)\/\S+/g, '[host path]')
        .replace(/\{["'][\s\S]*$/g, '')
        .replace(/\s*[-–—]\s*$/g, ''), MAX_ITEM_SUMMARY_LENGTH) || 'Needs attention.';
};
const formatTimestamp = (value, timeZone = 'UTC') => {
    const parsed = Date.parse(value);
    if (!Number.isFinite(parsed))
        return normalizeWhitespace(value);
    try {
        return new Intl.DateTimeFormat('en-GB', {
            timeZone,
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            timeZoneName: 'short',
            hourCycle: 'h23',
        }).format(new Date(parsed));
    }
    catch {
        return new Date(parsed).toISOString().replace('T', ' ').replace('.000Z', ' UTC');
    }
};
const notificationHeader = (notification) => `${SEVERITY_ICONS[notification.severity]} **${truncate(notification.title, 180)}**`;
const socialNotificationPhase = (notification) => ['new', 'changed', 'ongoing'].includes(String(notification.state || ''))
    ? 'active'
    : notification.state || 'summary';
const socialNotificationScopeHash = (notification) => {
    const scope = normalizeWhitespace(notification.scope);
    return scope
        ? createHash('sha256').update(scope).digest('hex').slice(0, 12)
        : undefined;
};
export const socialNotificationEventId = (notification) => {
    const scopeHash = socialNotificationScopeHash(notification);
    return [
        notification.kind || 'notification',
        socialNotificationPhase(notification),
        scopeHash,
        notification.fingerprint || 'no-fingerprint',
    ]
        .filter(Boolean)
        .join(':');
};
export const renderSocialNotificationMarkdown = (notification) => {
    const lines = [
        notificationHeader(notification),
        `${STATE_LABELS[notification.state]}${notification.summary ? ` · ${truncate(notification.summary, 500)}` : ''}`,
    ];
    if (notification.impact) {
        lines.push('', `**Impact:** ${truncate(notification.impact, 500)}`);
    }
    const evidence = summarizeSocialNotificationEvidence(notification.evidence);
    if (evidence) {
        lines.push('', `**Evidence:** ${truncate(evidence, 500)}`);
    }
    for (const item of notification.items.slice(0, 8)) {
        const label = escapeMarkdownLabel(item.label);
        const status = item.status ? ` · ${escapeMarkdownLabel(item.status)}` : '';
        const itemUrl = safeHttpUrl(item.url);
        const link = itemUrl ? ` · [Open](${itemUrl})` : '';
        lines.push('', `**${label}${status}**${link}`, truncate(item.summary, MAX_ITEM_SUMMARY_LENGTH));
        if (item.occurredAt) {
            lines.push(`Last seen: ${formatTimestamp(item.occurredAt, notification.timeZone)}`);
        }
        const action = humanizeRecommendedAction(item.action);
        if (action)
            lines.push(`Next: ${truncate(action, MAX_ITEM_SUMMARY_LENGTH)}`);
    }
    if (notification.items.length > 8) {
        lines.push('', `+${notification.items.length - 8} more items in the run details.`);
    }
    if (notification.nextStep) {
        lines.push('', `**Next:** ${truncate(humanizeRecommendedAction(notification.nextStep), 500)}`);
    }
    if (notification.nextRetryAt) {
        lines.push(`**Automatic retry:** ${formatTimestamp(notification.nextRetryAt)}`);
    }
    if (notification.automation) {
        lines.push(`**Automation:** ${truncate(notification.automation, 500)}`);
    }
    return `${truncateRendered(lines.join('\n'), MAX_MARKDOWN_FALLBACK_LENGTH).trimEnd()}\n`;
};
const discordField = (name, value, inline = false) => ({
    name: truncate(name, 256) || 'Detail',
    value: truncate(value, 1024) || '-',
    inline,
});
export const buildDiscordSocialPayload = (notification) => {
    const fields = notification.items.slice(0, 8).map((item) => {
        const status = item.status ? `**${item.status}**\n` : '';
        const itemUrl = safeHttpUrl(item.url);
        const link = itemUrl ? `\n[Open details](${itemUrl})` : '';
        const recommendedAction = humanizeRecommendedAction(item.action);
        const action = recommendedAction
            ? `\n**Next:** ${recommendedAction}`
            : '';
        const occurredAt = item.occurredAt
            ? `\n**Last seen:** ${formatTimestamp(item.occurredAt, notification.timeZone)}`
            : '';
        return discordField(item.label, `${status}${item.summary}${occurredAt}${action}${link}`);
    });
    if (notification.impact) {
        fields.unshift(discordField('Impact', notification.impact));
    }
    const evidence = summarizeSocialNotificationEvidence(notification.evidence);
    if (evidence) {
        fields.unshift(discordField('Evidence', evidence));
    }
    if (notification.nextStep || notification.nextRetryAt) {
        const parts = [
            notification.nextStep
                ? humanizeRecommendedAction(notification.nextStep)
                : null,
            notification.nextRetryAt
                ? `Automatic retry: ${formatTimestamp(notification.nextRetryAt)}`
                : null,
        ].filter(Boolean);
        fields.push(discordField('Next', parts.join('\n')));
    }
    if (notification.automation) {
        fields.push(discordField('Automation', notification.automation));
    }
    return {
        content: '',
        embeds: [
            {
                title: truncate(`${SEVERITY_ICONS[notification.severity]} ${notification.title}`, 256),
                description: `**${STATE_LABELS[notification.state]}**` +
                    `${notification.summary ? ` · ${truncate(notification.summary, 500)}` : ''}`,
                color: DISCORD_COLORS[notification.severity],
                fields: fields.slice(0, 20),
                footer: {
                    text: [
                        notification.kind.toUpperCase(),
                        notification.fingerprint?.slice(0, 12),
                    ].filter(Boolean).join(' • '),
                },
                timestamp: notification.generatedAt,
            },
        ],
        fallbackText: renderSocialNotificationMarkdown(notification),
    };
};
const slackEscape = (value) => sanitizeCopy(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
const boundedSlackText = (value, maxLength) => truncateRendered(slackEscape(value), maxLength);
export const buildSlackSocialPayload = (notification) => {
    const blocks = [
        {
            type: 'header',
            text: {
                type: 'plain_text',
                text: truncate(`${SEVERITY_ICONS[notification.severity]} ${notification.title}`, 150),
            },
        },
        {
            type: 'section',
            text: {
                type: 'mrkdwn',
                text: truncateRendered(`*${STATE_LABELS[notification.state]}*` +
                    `${notification.summary
                        ? ` · ${boundedSlackText(notification.summary, 1_300)}`
                        : ''}` +
                    `${notification.impact
                        ? `\n*Impact:* ${boundedSlackText(notification.impact, 1_300)}`
                        : ''}`, MAX_SLACK_SECTION_LENGTH),
            },
        },
    ];
    for (const item of notification.items.slice(0, 8)) {
        const itemUrl = safeHttpUrl(item.url);
        const url = itemUrl ? ` · <${itemUrl}|Open>` : '';
        const status = item.status
            ? ` · ${boundedSlackText(item.status, 160)}`
            : '';
        const recommendedAction = humanizeRecommendedAction(item.action);
        const action = recommendedAction
            ? `\n*Next:* ${boundedSlackText(recommendedAction, MAX_RECOMMENDED_ACTION_LENGTH)}`
            : '';
        const occurredAt = item.occurredAt
            ? `\n*Last seen:* ${boundedSlackText(formatTimestamp(item.occurredAt, notification.timeZone), 160)}`
            : '';
        blocks.push({
            type: 'section',
            text: {
                type: 'mrkdwn',
                text: truncateRendered(`*${boundedSlackText(item.label, 256)}${status}*${url}\n` +
                    `${boundedSlackText(item.summary, MAX_ITEM_SUMMARY_LENGTH)}${occurredAt}${action}`, MAX_SLACK_SECTION_LENGTH),
            },
        });
    }
    const evidence = summarizeSocialNotificationEvidence(notification.evidence);
    const context = [
        evidence ? `Evidence: ${evidence}` : null,
        notification.nextStep
            ? `Next: ${humanizeRecommendedAction(notification.nextStep)}`
            : null,
        notification.nextRetryAt
            ? `Automatic retry: ${formatTimestamp(notification.nextRetryAt)}`
            : null,
        notification.automation ? `Automation: ${notification.automation}` : null,
    ].filter(Boolean);
    if (context.length > 0) {
        blocks.push({
            type: 'context',
            elements: [
                {
                    type: 'mrkdwn',
                    text: boundedSlackText(context.join(' · '), MAX_SLACK_CONTEXT_LENGTH),
                },
            ],
        });
    }
    return {
        text: renderSocialNotificationMarkdown(notification),
        blocks: blocks.slice(0, MAX_SLACK_BLOCKS),
    };
};
export const socialNotificationSummary = (notification) => ({
    schema: notification.schema,
    version: notification.version,
    kind: notification.kind,
    state: notification.state,
    severity: notification.severity,
    title: truncate(notification.title, 256),
    summary: notification.summary
        ? truncate(notification.summary, 1_000)
        : undefined,
    impact: notification.impact
        ? truncate(notification.impact, 1_000)
        : undefined,
    items: notification.items.map((item) => ({
        id: item.id ? truncate(item.id, 160) : undefined,
        label: truncate(item.label, 256),
        status: item.status ? truncate(item.status, 160) : undefined,
        summary: truncate(item.summary, 1_000),
        action: item.action
            ? truncate(humanizeRecommendedAction(item.action), 1_000)
            : undefined,
        url: safeHttpUrl(item.url),
        occurredAt: item.occurredAt,
    })),
    nextStep: notification.nextStep
        ? truncate(humanizeRecommendedAction(notification.nextStep), 1_000)
        : undefined,
    nextRetryAt: notification.nextRetryAt,
    automation: notification.automation
        ? truncate(notification.automation, 1_000)
        : undefined,
    evidence: safeEvidence(notification.evidence),
    generatedAt: notification.generatedAt,
    fingerprint: notification.fingerprint
        ? truncate(notification.fingerprint, 256)
        : undefined,
    scopeHash: socialNotificationScopeHash(notification),
    timeZone: notification.timeZone,
});
