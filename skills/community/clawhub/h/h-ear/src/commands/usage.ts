import type { HearApiClient } from '@h-ear/core';
import { formatUsage } from '../formatter.js';

export async function usageCommand(client: HearApiClient): Promise<string> {
    const result = await client.usage();
    return formatUsage(result);
}
