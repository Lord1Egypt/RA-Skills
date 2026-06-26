import type { HearApiClient } from '@h-ear/core';
import { formatJobAudio } from '../formatter.js';

export async function jobAudioCommand(
    client: HearApiClient,
    jobId: string,
): Promise<string> {
    const result = await client.getJobAudio(jobId);
    return formatJobAudio(result);
}
