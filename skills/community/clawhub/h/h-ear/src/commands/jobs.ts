import type { HearApiClient } from '@h-ear/core';
import { formatJobsList, formatJobDetail } from '../formatter.js';

export async function jobsCommand(
    client: HearApiClient,
    options?: { limit?: number; offset?: number; status?: string },
): Promise<string> {
    const result = await client.listJobs({
        limit: options?.limit ?? 10,
        offset: options?.offset ?? 0,
        status: options?.status,
    });
    return formatJobsList(result);
}

export async function jobDetailCommand(
    client: HearApiClient,
    jobId: string,
): Promise<string> {
    const result = await client.getJob(jobId);
    return formatJobDetail(result);
}
