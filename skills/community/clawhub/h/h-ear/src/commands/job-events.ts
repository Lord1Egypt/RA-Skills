import type { HearApiClient } from '@h-ear/core';
import { formatJobEvents } from '../formatter.js';

export async function jobEventsCommand(
    client: HearApiClient,
    jobId: string,
    options?: {
        taxonomy?: string;
        minConfidence?: number;
        category?: string;
        tier2?: string;
        tier3?: string;
        startTime?: number;
        endTime?: number;
        sourceId?: string;
        offset?: number;
    },
): Promise<string> {
    const result = await client.getJobEvents(jobId, {
        taxonomy: options?.taxonomy,
        minConfidence: options?.minConfidence,
        category: options?.category,
        tier2: options?.tier2,
        tier3: options?.tier3,
        startTime: options?.startTime,
        endTime: options?.endTime,
        sourceId: options?.sourceId,
        offset: options?.offset ?? 0,
    });
    return formatJobEvents(result);
}
