import type { HearApiClient } from '@h-ear/core';
import { formatClassesList } from '../formatter.js';

export async function soundsCommand(
    client: HearApiClient,
    search?: string,
    options?: {
        limit?: number;
        offset?: number;
        taxonomy?: 'audioset-yamnet-521' | 'audioset-panns-527' | 'species';
    },
): Promise<string> {
    const result = await client.listClasses({
        category: search,
        limit: options?.limit ?? 20,
        offset: options?.offset ?? 0,
        taxonomy: options?.taxonomy,
    });
    return formatClassesList(result, search);
}
