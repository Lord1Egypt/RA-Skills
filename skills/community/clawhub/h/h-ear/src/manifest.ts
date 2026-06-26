/**
 * Single source of truth for the `h-ear` CLI command surface.
 *
 * Each entry binds:
 *   - The CLI path the user types (e.g. ["job", "events"])
 *   - A schema name from @h-ear/core (Zod shape + description, shared with mcp-server)
 *   - A handler that calls the underlying library command
 *
 * Consumed by:
 *   - cli.ts → dispatcher, top-level help, per-subcommand help, --list-tools --json
 *   - scripts/doc.shared-generate.mjs → bakes the SKILL.md commands table
 *
 * Why this exists: the CLI surface, the SKILL.md the LLM reads, and the JSON
 * the LLM gets from `h-ear --list-tools` MUST agree, or qwen2.5:14b (and any
 * tool-using model) starts inventing flags. By making a single manifest the
 * authority, drift is impossible.
 */

import type { HearApiClient } from '@h-ear/core';
import { toolDescriptions, toolShapes } from '@h-ear/core';

import { healthCommand } from './commands/health.js';
import { soundsCommand } from './commands/sounds.js';
import { usageCommand } from './commands/usage.js';
import { classifySyncCommand, classifyFileCommand } from './commands/classify.js';
import { classifyBatchCommand } from './commands/classify-batch.js';
import { jobsCommand, jobDetailCommand } from './commands/jobs.js';
import { jobEventsCommand } from './commands/job-events.js';
import { jobAudioCommand } from './commands/job-audio.js';
import { jobWaveformCommand } from './commands/job-waveform.js';
import { jobReportCommand } from './commands/job-report.js';
import {
    webhookListCommand, webhookDetailCommand, webhookCreateCommand,
    webhookPingCommand, webhookDeliveriesCommand,
    webhookUpdateCommand, webhookDeleteCommand,
} from './commands/webhooks.js';

// ─── Types ───────────────────────────────────────────────────────────────────

export interface ParsedArgs {
    /** Positional values, indexed by their declared name. */
    positionals: Record<string, string | undefined>;
    /** Flag values, raw strings (numbers parsed in the handler). */
    flags: Record<string, string | undefined>;
    /** Boolean flags that were present. */
    bools: Record<string, boolean>;
}

export interface CommandPositional {
    /** Positional name as the user types it: `<jobId>`. */
    name: string;
    /** Schema key this positional binds to (for help text). */
    schemaKey: string;
    /** Whether this positional is required. Defaults to true. */
    required?: boolean;
}

export interface CommandFlag {
    /** Flag name without leading dashes: "limit" → --limit. */
    name: string;
    /** Schema key this flag binds to. */
    schemaKey: string;
    /** Type hint for parsing — string is left as-is, number is parseFloat'd. */
    kind: 'string' | 'number' | 'boolean';
}

export interface CommandSpec {
    /** CLI path, e.g. ["jobs"] or ["job", "events"] or ["webhook", "list"]. */
    cliPath: string[];
    /** Key in toolShapes/toolDescriptions in @h-ear/core, e.g. "getJobEvents". */
    schemaName: string;
    /** One-line summary for top-level help. Pulled from schema if omitted. */
    summary: string;
    /** Positional args declared in CLI order. */
    positionals?: CommandPositional[];
    /** Flag args. */
    flags?: CommandFlag[];
    /** Concrete examples — the LLM reads these to learn the syntax. */
    examples: string[];
    /** Calls the underlying library command and returns formatted markdown. */
    handler: (client: HearApiClient, parsed: ParsedArgs) => Promise<string>;
}

// ─── Helpers for handlers ────────────────────────────────────────────────────

function num(v: string | undefined): number | undefined {
    if (v === undefined) return undefined;
    const n = parseFloat(v);
    return Number.isFinite(n) ? n : undefined;
}

function int(v: string | undefined): number | undefined {
    const n = num(v);
    return n === undefined ? undefined : Math.trunc(n);
}

function need(parsed: ParsedArgs, name: string): string {
    const v = parsed.positionals[name];
    if (v === undefined || v === '') throw new Error(`Missing required positional <${name}>`);
    return v;
}

// ─── Manifest ────────────────────────────────────────────────────────────────

export const COMMANDS: CommandSpec[] = [
    {
        cliPath: ['health'],
        schemaName: 'healthCheck',
        summary: 'Check H-ear API health and liveness (no auth required).',
        examples: ['h-ear health'],
        handler: (client) => healthCommand(client),
    },
    {
        cliPath: ['usage'],
        schemaName: 'usage',
        summary: 'Show API usage statistics (minutes, calls, quota).',
        examples: ['h-ear usage'],
        handler: (client) => usageCommand(client),
    },
    {
        cliPath: ['sounds'],
        schemaName: 'listClasses',
        summary: 'List supported sound classes (521+ across 3 taxonomies).',
        positionals: [{ name: 'search', schemaKey: 'category', required: false }],
        flags: [
            { name: 'limit', schemaKey: 'limit', kind: 'number' },
            { name: 'offset', schemaKey: 'offset', kind: 'number' },
            { name: 'taxonomy', schemaKey: 'taxonomy', kind: 'string' },
        ],
        examples: [
            'h-ear sounds                          # default 20 from yamnet-521',
            'h-ear sounds Animal --limit 5         # 5 animal classes',
            'h-ear sounds --taxonomy species       # bird species taxonomy',
        ],
        handler: (client, p) =>
            soundsCommand(client, p.positionals.search, {
                limit: int(p.flags.limit),
                offset: int(p.flags.offset),
                taxonomy: p.flags.taxonomy as 'audioset-yamnet-521' | 'audioset-panns-527' | 'species' | undefined,
            }),
    },
    {
        cliPath: ['jobs'],
        schemaName: 'listJobs',
        summary: 'List recent classification jobs (paginated).',
        flags: [
            { name: 'limit', schemaKey: 'limit', kind: 'number' },
            { name: 'offset', schemaKey: 'offset', kind: 'number' },
            { name: 'status', schemaKey: 'status', kind: 'string' },
            { name: 'batchId', schemaKey: 'batchId', kind: 'string' },
        ],
        examples: [
            'h-ear jobs                            # last 10 jobs',
            'h-ear jobs --limit 5                  # last 5',
            'h-ear jobs --status completed         # only completed',
        ],
        handler: (client, p) =>
            jobsCommand(client, {
                limit: int(p.flags.limit),
                offset: int(p.flags.offset),
                status: p.flags.status,
            }),
    },
    {
        cliPath: ['job'],
        schemaName: 'getJob',
        summary: 'Get detail for one job: status, fileName, eventCount, timestamps.',
        positionals: [{ name: 'jobId', schemaKey: 'jobId' }],
        examples: ['h-ear job job-1777340510821-1453bf9b-...'],
        handler: (client, p) => jobDetailCommand(client, need(p, 'jobId')),
    },
    {
        cliPath: ['job', 'events'],
        schemaName: 'getJobEvents',
        summary: 'Get noise events for a completed job (timeline order, filterable).',
        positionals: [{ name: 'jobId', schemaKey: 'jobId' }],
        flags: [
            { name: 'minConfidence', schemaKey: 'minConfidence', kind: 'number' },
            { name: 'category', schemaKey: 'category', kind: 'string' },
            { name: 'tier2', schemaKey: 'tier2', kind: 'string' },
            { name: 'tier3', schemaKey: 'tier3', kind: 'string' },
            { name: 'startTime', schemaKey: 'startTime', kind: 'number' },
            { name: 'endTime', schemaKey: 'endTime', kind: 'number' },
            { name: 'sourceId', schemaKey: 'sourceId', kind: 'string' },
            { name: 'taxonomy', schemaKey: 'taxonomy', kind: 'string' },
            { name: 'offset', schemaKey: 'offset', kind: 'number' },
        ],
        examples: [
            'h-ear job events job-1777...',
            'h-ear job events job-1777... --minConfidence 0.7',
            'h-ear job events job-1777... --category Animal --tier3 Dog',
        ],
        handler: (client, p) =>
            jobEventsCommand(client, need(p, 'jobId'), {
                minConfidence: num(p.flags.minConfidence),
                category: p.flags.category,
                tier2: p.flags.tier2,
                tier3: p.flags.tier3,
                startTime: num(p.flags.startTime),
                endTime: num(p.flags.endTime),
                sourceId: p.flags.sourceId,
                taxonomy: p.flags.taxonomy,
                offset: int(p.flags.offset),
            }),
    },
    {
        cliPath: ['job', 'audio'],
        schemaName: 'getJobAudio',
        summary: 'Get a 1-hour SAS URL to stream the source audio of a job.',
        positionals: [{ name: 'jobId', schemaKey: 'jobId' }],
        examples: ['h-ear job audio job-1777...'],
        handler: (client, p) => jobAudioCommand(client, need(p, 'jobId')),
    },
    {
        cliPath: ['job', 'waveform'],
        schemaName: 'getJobWaveform',
        summary: 'Get pre-computed peaks.js waveform + audio URL.',
        positionals: [{ name: 'jobId', schemaKey: 'jobId' }],
        flags: [{ name: 'zoom', schemaKey: 'zoom', kind: 'number' }],
        examples: [
            'h-ear job waveform job-1777...',
            'h-ear job waveform job-1777... --zoom 256   # high detail',
        ],
        handler: (client, p) =>
            jobWaveformCommand(client, need(p, 'jobId'), {
                zoom: int(p.flags.zoom) as 256 | 1024 | 4096 | undefined,
            }),
    },
    {
        cliPath: ['job', 'report'],
        schemaName: 'getJobReport',
        summary: 'Get a 7-day SAS URL to download the Excel analysis report.',
        positionals: [{ name: 'jobId', schemaKey: 'jobId' }],
        examples: ['h-ear job report job-1777...'],
        handler: (client, p) => jobReportCommand(client, need(p, 'jobId')),
    },
    {
        cliPath: ['classify'],
        schemaName: 'classifyAudio',
        summary: 'Classify audio (URL or local file). Polls until complete.',
        positionals: [{ name: 'fileOrUrl', schemaKey: 'filePath' }],
        flags: [
            { name: 'threshold', schemaKey: 'threshold', kind: 'number' },
            { name: 'lat', schemaKey: 'latitude', kind: 'number' },
            { name: 'lng', schemaKey: 'longitude', kind: 'number' },
            { name: 'callbackUrl', schemaKey: 'callbackUrl', kind: 'string' },
        ],
        examples: [
            'h-ear classify https://example.com/audio.mp3',
            'h-ear classify /path/to/local.wav --threshold 0.5',
            'h-ear classify ./demo.mp3 --lat -35.25 --lng 149.05',
        ],
        handler: async (client, p) => {
            const target = p.positionals.fileOrUrl;
            if (!target) throw new Error('h-ear classify <file-or-url> is required');
            const opts = {
                threshold: num(p.flags.threshold),
                latitude: num(p.flags.lat),
                longitude: num(p.flags.lng),
                callbackUrl: p.flags.callbackUrl,
            };
            const onProgress = (msg: string) => process.stderr.write(`  ${msg}\n`);
            if (target.startsWith('http://') || target.startsWith('https://')) {
                return classifySyncCommand(client, target, opts, onProgress);
            }
            return classifyFileCommand(client, target, { ...opts, waitForResult: true }, onProgress);
        },
    },
    {
        cliPath: ['classify', 'batch'],
        schemaName: 'classifyBatch',
        summary: 'Submit a batch of audio URLs for asynchronous classification (callback delivery).',
        flags: [
            { name: 'urls', schemaKey: 'files', kind: 'string' },
            { name: 'callbackUrl', schemaKey: 'callbackUrl', kind: 'string' },
            { name: 'callbackSecret', schemaKey: 'callbackSecret', kind: 'string' },
            { name: 'threshold', schemaKey: 'threshold', kind: 'number' },
            { name: 'filterMinDurationSeconds', schemaKey: 'filterMinDurationSeconds', kind: 'number' },
        ],
        examples: [
            'h-ear classify batch --urls https://a.example/x.mp3,https://b.example/y.mp3 --callbackUrl https://my.host/hook',
            'h-ear classify batch --urls https://a.example/x.mp3 --callbackUrl https://my.host/hook --threshold 0.5',
        ],
        handler: (client, p) => {
            const raw = p.flags.urls;
            if (!raw) throw new Error('h-ear classify batch requires --urls <comma-separated-list>');
            const urls = raw.split(',').map(s => s.trim()).filter(Boolean);
            if (urls.length === 0) throw new Error('--urls must contain at least one URL');
            const callbackUrl = p.flags.callbackUrl;
            if (!callbackUrl) throw new Error('--callbackUrl is required (URL-based batch delivers results via webhook)');
            return classifyBatchCommand(client, urls, {
                callbackUrl,
                callbackSecret: p.flags.callbackSecret,
                threshold: num(p.flags.threshold),
                filterMinDurationSeconds: num(p.flags.filterMinDurationSeconds),
            });
        },
    },
    {
        cliPath: ['webhook', 'list'],
        schemaName: 'listWebhooks',
        summary: 'List enterprise webhook registrations.',
        examples: ['h-ear webhook list'],
        handler: (client) => webhookListCommand(client),
    },
    {
        cliPath: ['webhook', 'get'],
        schemaName: 'getWebhook',
        summary: 'Show one webhook (URL, events, filter config, delivery stats).',
        positionals: [{ name: 'webhookId', schemaKey: 'webhookId' }],
        examples: ['h-ear webhook get wh_abc123'],
        handler: (client, p) => webhookDetailCommand(client, need(p, 'webhookId')),
    },
    {
        cliPath: ['webhook', 'create'],
        schemaName: 'createWebhook',
        summary: 'Create an enterprise webhook (returns signing secret ONCE).',
        positionals: [{ name: 'url', schemaKey: 'url' }],
        flags: [
            { name: 'description', schemaKey: 'description', kind: 'string' },
        ],
        examples: [
            'h-ear webhook create https://my.host/hook',
            'h-ear webhook create https://my.host/hook --description "alerts"',
        ],
        handler: (client, p) =>
            webhookCreateCommand(client, need(p, 'url'), {
                description: p.flags.description,
            }),
    },
    {
        cliPath: ['webhook', 'update'],
        schemaName: 'updateWebhook',
        summary: 'Update webhook URL, status (active/paused), or filters.',
        positionals: [{ name: 'webhookId', schemaKey: 'webhookId' }],
        flags: [
            { name: 'url', schemaKey: 'url', kind: 'string' },
            { name: 'status', schemaKey: 'status', kind: 'string' },
            { name: 'description', schemaKey: 'description', kind: 'string' },
        ],
        examples: [
            'h-ear webhook update wh_abc123 --status paused',
            'h-ear webhook update wh_abc123 --url https://new.host/hook',
        ],
        handler: (client, p) =>
            webhookUpdateCommand(client, need(p, 'webhookId'), {
                url: p.flags.url,
                status: p.flags.status as 'active' | 'paused' | undefined,
                description: p.flags.description,
            }),
    },
    {
        cliPath: ['webhook', 'delete'],
        schemaName: 'deleteWebhook',
        summary: 'Permanently delete a webhook (cannot be undone).',
        positionals: [{ name: 'webhookId', schemaKey: 'webhookId' }],
        examples: ['h-ear webhook delete wh_abc123'],
        handler: (client, p) => webhookDeleteCommand(client, need(p, 'webhookId')),
    },
    {
        cliPath: ['webhook', 'ping'],
        schemaName: 'pingWebhook',
        summary: 'Send a test ping to a webhook (verify connectivity + signing).',
        positionals: [{ name: 'webhookId', schemaKey: 'webhookId' }],
        examples: ['h-ear webhook ping wh_abc123'],
        handler: (client, p) => webhookPingCommand(client, need(p, 'webhookId')),
    },
    {
        cliPath: ['webhook', 'deliveries'],
        schemaName: 'listWebhookDeliveries',
        summary: 'Audit trail: recent delivery attempts for a webhook.',
        positionals: [{ name: 'webhookId', schemaKey: 'webhookId' }],
        flags: [{ name: 'limit', schemaKey: 'limit', kind: 'number' }],
        examples: [
            'h-ear webhook deliveries wh_abc123',
            'h-ear webhook deliveries wh_abc123 --limit 50',
        ],
        handler: (client, p) =>
            webhookDeliveriesCommand(client, need(p, 'webhookId'), {
                limit: int(p.flags.limit),
            }),
    },
];

// ─── Lookups & introspection ─────────────────────────────────────────────────

/** Find the longest-prefix manifest entry matching the user's argv tokens. */
export function findCommand(argv: string[]): { spec: CommandSpec; remaining: string[] } | null {
    // Sort by depth descending so "job events" beats "job"
    const byDepth = [...COMMANDS].sort((a, b) => b.cliPath.length - a.cliPath.length);
    for (const spec of byDepth) {
        if (argv.length < spec.cliPath.length) continue;
        const matches = spec.cliPath.every((p, i) => argv[i] === p);
        if (matches) return { spec, remaining: argv.slice(spec.cliPath.length) };
    }
    return null;
}

/** Render the manifest as MCP-style JSON for `--list-tools --json`. */
export function listToolsJson(): unknown {
    return COMMANDS.map(spec => {
        const shape = toolShapes[spec.schemaName];
        const params: Record<string, unknown> = {};
        if (shape) {
            for (const [key, zod] of Object.entries(shape)) {
                // .description() lives on the zod object's _def; defensively read it.
                const def = (zod as { _def?: { description?: string; typeName?: string } })._def;
                params[key] = {
                    description: def?.description ?? '',
                    type: def?.typeName ?? 'unknown',
                };
            }
        }
        return {
            name: spec.cliPath.join(' '),
            schemaName: spec.schemaName,
            summary: spec.summary,
            description: toolDescriptions[spec.schemaName] ?? spec.summary,
            positionals: spec.positionals ?? [],
            flags: spec.flags ?? [],
            examples: spec.examples,
            params,
        };
    });
}
