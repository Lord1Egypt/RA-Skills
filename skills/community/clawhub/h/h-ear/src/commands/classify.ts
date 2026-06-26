import { readFileSync, existsSync, statSync } from 'fs';
import { basename, extname } from 'path';
import type { HearApiClient, ChunkSource, ClassifyOptions } from '@h-ear/core';
import { HearApiError, HEAR_API, getAudioDuration } from '@h-ear/core';
import { formatClassifySubmitted, formatClassifyResult } from '../formatter.js';

interface ClassifyOpts {
    threshold?: number;
    callbackUrl?: string;
    callbackSecret?: string;
    filterMinDurationSeconds?: number;
    latitude?: number;
    longitude?: number;
    fileName?: string;
}

function validateGps(opts?: { latitude?: number; longitude?: number }): void {
    if (!opts) return;
    if ((opts.latitude !== undefined) !== (opts.longitude !== undefined)) {
        throw new Error('latitude and longitude must both be provided together.');
    }
}

/** Pre-flight auth probe — fail fast before kicking off a long classify. */
async function preflightAuth(client: HearApiClient): Promise<void> {
    try {
        await client.usage();
    } catch (err) {
        if (err instanceof HearApiError && (err.status === 401 || err.code === 'INVALID_API_KEY')) {
            throw new Error(`Authentication failed: ${err.message}. Verify your API key or Bearer token.`, { cause: err });
        }
        // Non-auth errors (network, 5xx) — don't block; classify may still work.
    }
}

/** Async submit — returns immediately with job ID. callbackUrl is optional. */
export async function classifyCommand(
    client: HearApiClient,
    url: string,
    options?: ClassifyOpts,
): Promise<string> {
    validateGps(options);
    await preflightAuth(client);
    const accepted = await client.submitClassify({
        url,
        threshold: options?.threshold ?? 0.3,
        fileName: options?.fileName,
        callbackUrl: options?.callbackUrl,
        callbackSecret: options?.callbackSecret,
        filterMinDurationSeconds: options?.filterMinDurationSeconds,
        latitude: options?.latitude,
        longitude: options?.longitude,
    });
    return formatClassifySubmitted(accepted);
}

/** Sync classify — submits, polls until complete, returns formatted result. */
export async function classifySyncCommand(
    client: HearApiClient,
    url: string,
    options?: ClassifyOpts,
    onProgress?: (msg: string) => void,
): Promise<string> {
    validateGps(options);
    await preflightAuth(client);
    const result = await client.classify(
        {
            url,
            threshold: options?.threshold ?? 0.3,
            fileName: options?.fileName,
            callbackUrl: options?.callbackUrl,
            callbackSecret: options?.callbackSecret,
            filterMinDurationSeconds: options?.filterMinDurationSeconds,
            latitude: options?.latitude,
            longitude: options?.longitude,
        },
        onProgress,
    );
    return formatClassifyResult(result);
}

/**
 * Local-file classify — reads file from disk, picks small-file or chunked-upload
 * path based on size + duration, optionally polls. Mirrors mcp-server's classifyAudio.
 */
export async function classifyFileCommand(
    client: HearApiClient,
    filePath: string,
    options?: ClassifyOpts & { waitForResult?: boolean },
    onProgress?: (msg: string) => void,
): Promise<string> {
    validateGps(options);

    if (!existsSync(filePath)) throw new Error(`File not found: ${filePath}`);
    const ext = extname(filePath).toLowerCase().replace('.', '').toUpperCase();
    if (!(HEAR_API.SUPPORTED_FORMATS as readonly string[]).includes(ext)) {
        throw new Error(`Unsupported format: ${ext}. Supported: ${HEAR_API.SUPPORTED_FORMATS.join(', ')}`);
    }

    await preflightAuth(client);

    const stat = statSync(filePath);
    const fileName = basename(filePath);
    const duration = getAudioDuration(filePath);
    const sliceOptions: ClassifyOptions = {
        threshold: options?.threshold ?? 0.3,
        callbackUrl: options?.callbackUrl,
        callbackSecret: options?.callbackSecret,
        filterMinDurationSeconds: options?.filterMinDurationSeconds,
        latitude: options?.latitude,
        longitude: options?.longitude,
    };

    // Small file: direct multipart upload
    if (stat.size <= HEAR_API.MAX_FILE_SIZE_BYTES && duration <= HEAR_API.MAX_DURATION_SECONDS) {
        const buffer = readFileSync(filePath);
        const accepted = await client.submitClassifyFile(buffer, fileName, sliceOptions);
        if (options?.callbackUrl || !options?.waitForResult) {
            return formatClassifySubmitted(accepted);
        }
        const result = await client.pollJob(accepted.requestId, onProgress);
        return formatClassifyResult(result);
    }

    // Large file: byte-slice chunked upload (chunk-by-requeue pipeline)
    const totalSlices = Math.ceil(stat.size / HEAR_API.MAX_FILE_SIZE_BYTES);
    const chunks: ChunkSource[] = [];
    for (let i = 0; i < totalSlices; i++) {
        const offset = i * HEAR_API.MAX_FILE_SIZE_BYTES;
        const length = Math.min(HEAR_API.MAX_FILE_SIZE_BYTES, stat.size - offset);
        chunks.push({ filePath, offset, length, index: i });
    }
    onProgress?.(`Large file (${(stat.size / 1024 / 1024).toFixed(1)}MB) — uploading in ${totalSlices} chunks`);
    const accepted = await client.submitClassifyChunked(chunks, fileName, sliceOptions, onProgress);
    if (options?.callbackUrl || !options?.waitForResult) {
        return formatClassifySubmitted(accepted);
    }
    const result = await client.pollJob(accepted.requestId, onProgress);
    return formatClassifyResult(result);
}
