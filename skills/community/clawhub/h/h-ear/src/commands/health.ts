import type { HearApiClient } from '@h-ear/core';
import { formatHealth } from '../formatter.js';

export async function healthCommand(client: HearApiClient): Promise<string> {
    const result = await client.health();
    return formatHealth(result);
}
