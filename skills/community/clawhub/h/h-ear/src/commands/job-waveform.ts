import type { HearApiClient } from '@h-ear/core';
import { formatJobWaveform } from '../formatter.js';

export async function jobWaveformCommand(
    client: HearApiClient,
    jobId: string,
    options?: { zoom?: 256 | 1024 | 4096 },
): Promise<string> {
    const result = await client.getJobWaveform(jobId, { zoom: options?.zoom });
    return formatJobWaveform(result);
}
