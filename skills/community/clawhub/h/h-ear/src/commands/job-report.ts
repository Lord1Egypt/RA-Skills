import type { HearApiClient } from '@h-ear/core';
import { formatJobReport } from '../formatter.js';

export async function jobReportCommand(client: HearApiClient, jobId: string): Promise<string> {
    const result = await client.getJobReport(jobId);
    return formatJobReport(result);
}
