import type { HearApiClient } from '@h-ear/core';
import { formatAlertRegistered, formatAlertDeregistered } from '../formatter.js';

export async function alertOnCommand(
    client: HearApiClient,
    soundClass: string,
    options?: { callbackUrl?: string },
): Promise<string> {
    if (!options?.callbackUrl) throw new Error('callbackUrl is required for alert registration');
    await client.registerWebhook({
        url: options.callbackUrl,
        events: ['job.completed'],
        soundClass,
    });
    return formatAlertRegistered(soundClass);
}

export async function alertOffCommand(
    client: HearApiClient,
    webhookId: string,
    soundClass: string,
): Promise<string> {
    await client.deregisterWebhook(webhookId);
    return formatAlertDeregistered(soundClass);
}
