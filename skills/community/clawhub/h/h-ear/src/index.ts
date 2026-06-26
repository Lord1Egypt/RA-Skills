/**
 * @h-ear/openclaw — OpenClaw skill for H-ear World audio classification.
 *
 * Exposes H-ear Enterprise API as conversational commands for messaging channels.
 */

import { createRequire } from 'module';
import { HearApiClient, type ServerConfig } from '@h-ear/core';
import { resolveConfig } from './config.js';

const require = createRequire(import.meta.url);
const { version: SKILL_VERSION } = require('../package.json') as { version: string };

export { SKILL_VERSION };

// Commands
export { classifyCommand, classifySyncCommand, classifyFileCommand } from './commands/classify.js';
export { classifyBatchCommand } from './commands/classify-batch.js';
export { soundsCommand } from './commands/sounds.js';
export { healthCommand } from './commands/health.js';
export { usageCommand } from './commands/usage.js';
export { jobsCommand, jobDetailCommand } from './commands/jobs.js';
export { jobEventsCommand } from './commands/job-events.js';
export { jobAudioCommand } from './commands/job-audio.js';
export { jobWaveformCommand } from './commands/job-waveform.js';
export { jobReportCommand } from './commands/job-report.js';
export { alertOnCommand, alertOffCommand } from './commands/alerts.js';
export {
    webhookListCommand, webhookDetailCommand, webhookCreateCommand,
    webhookPingCommand, webhookDeliveriesCommand,
    webhookUpdateCommand, webhookDeleteCommand,
} from './commands/webhooks.js';

// Formatter
export {
    formatClassifyResult, formatClassesList, formatHealth,
    formatUsage, formatJobsList, formatJobDetail,
    formatJobEvents, formatJobAudio, formatJobWaveform, formatJobReport,
    formatAlertRegistered, formatAlertDeregistered,
    formatWebhookList, formatWebhookDetail, formatWebhookCreated,
    formatWebhookPing, formatWebhookDeliveries,
    formatWebhookUpdated, formatWebhookDeleted,
} from './formatter.js';

// Config
export { resolveConfig } from './config.js';

/** Create a configured skill instance with API client. */
export function createSkill(config?: ServerConfig): {
    client: HearApiClient;
    config: ServerConfig;
    version: string;
} {
    const resolved = config ?? resolveConfig();
    const client = new HearApiClient(resolved);
    return { client, config: resolved, version: SKILL_VERSION };
}
