import type { HearApiClient } from '@h-ear/core';

export async function classifyBatchCommand(
    client: HearApiClient,
    urls: string[],
    options?: {
        threshold?: number;
        callbackUrl?: string;
        callbackSecret?: string;
        filterMinDurationSeconds?: number;
    },
): Promise<string> {
    // Note: BatchRequest does not currently accept GPS — apply per-file via classifyFileCommand
    // if you need to tag local recordings with location.
    const files = urls.map((url, i) => ({ url, id: `file-${i + 1}` }));
    const result = await client.classifyBatch({
        files,
        callbackUrl: options?.callbackUrl ?? '',
        callbackSecret: options?.callbackSecret,
        threshold: options?.threshold ?? 0.3,
        filterMinDurationSeconds: options?.filterMinDurationSeconds,
    });

    return [
        `**Batch Submitted**`,
        `Batch ID: ${result.batchId}`,
        `Files: ${result.fileCount}`,
        `Estimated: ~${result.estimatedCompletionMinutes} min`,
        `Status: ${result.status}`,
    ].join('\n');
}
