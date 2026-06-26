/**
 * Format H-ear API responses as chat-friendly markdown.
 * Designed for messaging channels: Telegram, Slack, Discord, WhatsApp, Teams.
 */

import type {
    ClassifyResult, ClassesResult, HealthResult,
    UsageResult, JobsResult, JobResult, AsyncAccepted,
    JobEventsResult, JobAudioResult, JobWaveformResult, JobReportResult,
    EnterpriseWebhookListResult, EnterpriseWebhook, EnterpriseWebhookCreateResult,
    PingResult, WebhookDeliveriesResult,
} from '@h-ear/core';

export function formatClassifyResult(result: ClassifyResult): string {
    // Server returns the job as { id, ... }; ClassifyResult declares requestId.
    // Read either so the formatter is robust to the wire shape.
    const id = result.requestId ?? (result as { id?: string }).id ?? '';

    const lines: string[] = [
        `**Audio Classification Complete**`,
        `Duration: ${result.duration?.toFixed(1) ?? '?'}s | ${result.eventCount} noise events detected`,
    ];

    if (result.eventCount === 0) {
        lines.push('', 'No sound events detected above threshold.');
    } else {
        lines.push('', `Call getJobEvents("${id}") for the per-event records, or formatJobWithEvents(result, events) to render a combined view.`);
    }

    if (result.reportUrl) {
        lines.push('', `Full report: ${result.reportUrl}`);
    }

    return lines.join('\n');
}

export function formatClassesList(result: ClassesResult, search?: string): string {
    const lines: string[] = [
        `**Sound Classes** (${result.taxonomy})`,
        `${result.totalFiltered} of ${result.totalAvailable} classes`,
        '',
    ];

    if (result.classes.length > 0) {
        lines.push('| # | Class | Category |');
        lines.push('|---|-------|----------|');

        for (const cls of result.classes.slice(0, 20)) {
            lines.push(`| ${cls.index} | ${cls.name} | ${cls.category} |`);
        }

        if (result.pagination?.hasMore) {
            lines.push('', `_Showing ${result.classes.length} of ${result.totalFiltered} — use pagination for more._`);
        }
    } else {
        const hint = search ? ` matching "${search}"` : '';
        lines.push(`No classes found${hint}.`);
    }

    return lines.join('\n');
}

export function formatHealth(result: HealthResult): string {
    return [
        `**H-ear API Status**`,
        `Status: ${result.status}`,
        `Version: ${result.version}`,
        `Deployed: ${result.deployedTimestamp}`,
    ].join('\n');
}

export function formatUsage(result: UsageResult): string {
    const minutesPct = result.period.minutesLimit > 0
        ? Math.round((result.period.minutesUsed / result.period.minutesLimit) * 100)
        : 0;
    const callsPct = result.daily.limit > 0
        ? Math.round((result.daily.used / result.daily.limit) * 100)
        : 0;

    return [
        `**H-ear API Usage**`,
        `Tier: ${result.tier}`,
        `Minutes: ${result.period.minutesUsed.toLocaleString()} / ${result.period.minutesLimit.toLocaleString()} (${minutesPct}%)`,
        `Today: ${result.daily.used.toLocaleString()} / ${result.daily.limit.toLocaleString()} calls (${callsPct}%)`,
        `Remaining: ${result.daily.remaining.toLocaleString()} calls`,
        `Period: ${result.period.start} to ${result.period.end}`,
    ].join('\n');
}

export function formatJobsList(result: JobsResult): string {
    const lines: string[] = [
        `**Recent Jobs** (${result.total} total)`,
        '',
    ];

    if (result.jobs.length > 0) {
        lines.push('| Job ID | Status | File | Events | Created |');
        lines.push('|--------|--------|------|--------|---------|');

        for (const job of result.jobs) {
            // Server emits each job as { id, ... }; JobSummary declares jobId.
            const jobId = job.jobId ?? (job as { id?: string }).id ?? '-';
            const status = job.status === 'completed' ? 'done' : job.status;
            const file = job.fileName || '-';
            const events = job.eventCount ?? '-';
            const created = job.createdAt ? job.createdAt.substring(0, 16).replace('T', ' ') : '-';
            // Full job ID (LLM needs it for follow-up calls; truncated IDs cause flag-guessing).
            lines.push(`| \`${jobId}\` | ${status} | ${file} | ${events} | ${created} |`);
        }

        if (result.hasMore) {
            lines.push('', `_Showing ${result.jobs.length} of ${result.total} — use "jobs last N" for more._`);
        }
    } else {
        lines.push('No jobs found.');
    }

    return lines.join('\n');
}

export function formatJobDetail(result: JobResult): string {
    // Server emits job as { id, ... }; JobResult declares jobId.
    const jobId = result.jobId ?? (result as { id?: string }).id ?? '';

    const lines: string[] = [
        `**Job** \`${jobId}\``,
        `Status: ${result.status}`,
    ];

    if (result.fileName) lines.push(`File: ${result.fileName}`);
    if (result.duration) lines.push(`Duration: ${result.duration.toFixed(1)}s`);
    if (result.eventCount !== undefined) lines.push(`Events: ${result.eventCount}`);
    lines.push(`Created: ${result.createdAt}`);
    if (result.completedAt) lines.push(`Completed: ${result.completedAt}`);

    if (result.eventCount && result.eventCount > 0) {
        lines.push('', `Call getJobEvents("${jobId}") for the per-event records, or formatJobWithEvents(job, events) to render a combined view.`);
    }

    if (result.reportUrl) {
        lines.push('', `Full report: ${result.reportUrl}`);
    }

    return lines.join('\n');
}

/**
 * Render a job's metadata + per-event records in one block. Convenient when the
 * caller has just chained getJob(jobId) and getJobEvents(jobId).
 */
export function formatJobWithEvents(job: JobResult, events: JobEventsResult): string {
    return [formatJobDetail(job), '', formatJobEvents(events)].join('\n');
}

export function formatClassifySubmitted(accepted: AsyncAccepted): string {
    return [
        `**Analyzing Audio**`,
        `Job ID: ${accepted.requestId}`,
        `Status: ${accepted.status}`,
        `Results will be delivered when ready.`,
        '',
        `Check status: \`job ${accepted.requestId}\``,
    ].join('\n');
}

export function formatJobEvents(result: JobEventsResult): string {
    const lines: string[] = [
        `**Job Events** (${result.total} total)`,
        `Job: \`${result.jobId}\``,
        '',
    ];

    if (result.events.length > 0) {
        lines.push('| Sound | Confidence | Category | Time |');
        lines.push('|-------|-----------|----------|------|');

        for (const event of result.events.slice(0, 20)) {
            const name = event.tier2 || event.tier1;
            const pct = `${Math.round(event.confidence * 100)}%`;
            const cat = event.tier1;
            const time = `${event.startTime.toFixed(1)}s`;
            lines.push(`| ${name} | ${pct} | ${cat} | ${time} |`);
        }

        if (result.hasMore) {
            lines.push('', `_Showing ${result.events.length} of ${result.total} — use pagination for more._`);
        }
    } else {
        lines.push('No events found.');
    }

    return lines.join('\n');
}

export function formatJobAudio(result: JobAudioResult): string {
    const lines: string[] = [
        `**Job Audio**`,
        `Job: \`${result.jobId}\``,
        `URL: ${result.audioUrl}`,
        `Expires: ${result.expiresAt}`,
    ];
    if (result.duration) lines.push(`Duration: ${result.duration.toFixed(1)}s`);
    if (result.mimeType) lines.push(`Type: ${result.mimeType}`);
    return lines.join('\n');
}

export function formatJobWaveform(result: JobWaveformResult): string {
    const lines: string[] = [
        `**Job Waveform**`,
        `Job: \`${result.jobId}\``,
        `Waveform: ${result.waveformUrl}`,
        `Zoom: ${result.zoom} (${result.samplesPerPixel} samples/px)`,
        `Expires: ${result.expiresAt}`,
    ];
    if (result.audioUrl) lines.push(`Audio: ${result.audioUrl}`);
    if (result.duration) lines.push(`Duration: ${result.duration.toFixed(1)}s`);
    return lines.join('\n');
}

export function formatAlertRegistered(soundClass: string): string {
    return `Alert registered. You'll be notified whenever **${soundClass}** is detected.`;
}

export function formatAlertDeregistered(soundClass: string): string {
    return `Alert for **${soundClass}** has been removed.`;
}

export function formatWebhookList(result: EnterpriseWebhookListResult): string {
    const lines: string[] = [
        `**Webhooks** (${result.webhooks.length}/${result.maxWebhooks})`,
        '',
    ];

    if (result.webhooks.length > 0) {
        lines.push('| ID | URL | Events | Status | Failures |');
        lines.push('|----|-----|--------|--------|----------|');

        for (const w of result.webhooks) {
            const url = w.url.length > 40 ? w.url.substring(0, 37) + '...' : w.url;
            const events = w.events.join(', ');
            // Full webhook ID — needed for `h-ear webhook get/update/delete <id>`.
            lines.push(`| \`${w.id}\` | ${url} | ${events} | ${w.status} | ${w.failureCount} |`);
        }
    } else {
        lines.push('No webhooks registered.');
    }

    if (result.canCreate) {
        lines.push('', `_${result.maxWebhooks - result.webhooks.length} webhook slot(s) available._`);
    }

    return lines.join('\n');
}

export function formatWebhookDetail(webhook: EnterpriseWebhook): string {
    const lines: string[] = [
        `**Webhook** \`${webhook.id}\``,
        `URL: ${webhook.url}`,
        `Events: ${webhook.events.join(', ')}`,
        `Status: ${webhook.status}`,
        `Failures: ${webhook.failureCount}`,
    ];

    if (webhook.taxonomyFilter) lines.push(`Taxonomy filter: ${webhook.taxonomyFilter.join(', ')}`);
    if (webhook.notificationTierDepth) {
        lines.push(`Tier depth: ${webhook.notificationTierDepth}`);
        if (webhook.notificationTierValues) lines.push(`Tier values: ${webhook.notificationTierValues.join(', ')}`);
    }
    if (webhook.description) lines.push(`Description: ${webhook.description}`);
    if (webhook.lastDeliveryAt) lines.push(`Last delivery: ${webhook.lastDeliveryAt} (${webhook.lastDeliveryStatus})`);
    if (webhook.disabledReason) lines.push(`Disabled reason: ${webhook.disabledReason}`);
    lines.push(`Created: ${webhook.createdAt}`);

    return lines.join('\n');
}

export function formatWebhookCreated(result: EnterpriseWebhookCreateResult): string {
    return [
        `**Webhook Created**`,
        `ID: ${result.webhook.id}`,
        `URL: ${result.webhook.url}`,
        `Events: ${result.webhook.events.join(', ')}`,
        '',
        `**Secret: \`${result.secret}\`**`,
        `_This secret is shown ONCE. Save it now for webhook signature verification._`,
    ].join('\n');
}

export function formatWebhookPing(result: PingResult): string {
    const status = result.success ? 'Success' : 'Failed';
    return [
        `**Webhook Ping ${status}**`,
        `Delivery ID: ${result.deliveryId}`,
        `Response: ${result.responseStatus ?? 'N/A'}`,
        `Duration: ${result.durationMs}ms`,
    ].join('\n');
}

export function formatJobReport(result: JobReportResult): string {
    return [
        `**Job Report**`,
        `Job: \`${result.jobId}\``,
        `Report: ${result.reportUrl}`,
        `Expires: ${result.expiresIn}`,
    ].join('\n');
}

export function formatWebhookUpdated(webhook: EnterpriseWebhook): string {
    return [
        `**Webhook Updated**`,
        formatWebhookDetail(webhook),
    ].join('\n');
}

export function formatWebhookDeleted(webhookId: string): string {
    return `Webhook \`${webhookId}\` deleted.`;
}

export function formatWebhookDeliveries(result: WebhookDeliveriesResult): string {
    const lines: string[] = [
        `**Webhook Deliveries** (${result.deliveries.length})`,
        '',
    ];

    if (result.deliveries.length > 0) {
        lines.push('| Event | Status | Success | Attempt | Time |');
        lines.push('|-------|--------|---------|---------|------|');

        for (const d of result.deliveries) {
            const status = d.responseStatus ?? '-';
            const success = d.success ? 'yes' : 'no';
            const time = d.createdAt.substring(0, 16).replace('T', ' ');
            lines.push(`| ${d.event} | ${status} | ${success} | ${d.attempt} | ${time} |`);
        }
    } else {
        lines.push('No delivery records found.');
    }

    return lines.join('\n');
}
