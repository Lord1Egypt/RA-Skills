/**
 * 图片下载辅助:把 http(s) URL 或本地文件路径统一加载为 Buffer,
 * 供 WeCom Agent API / Bot WS sendMedia 使用。
 *
 * - http/https：复用 openclaw 的 fetchRemoteMedia（带 SSRF 防护 / redirect / maxBytes /
 *   readIdleTimeout），并显式带上桌面 UA（部分 CDN 如 Tencent COS / 阿里 OSS 在某些
 *   bucket 配置下会拒绝裸 Node fetch）。
 * - 其它路径按本地文件处理(fs.readFile),尝试根据扩展名推断 MIME。
 */

import { fetchRemoteMedia } from "openclaw/plugin-sdk/media-runtime";

const MIME_BY_EXT: Record<string, string> = {
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    png: "image/png",
    gif: "image/gif",
    webp: "image/webp",
    bmp: "image/bmp",
};

const DEFAULT_FETCH_USER_AGENT =
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36";

const DEFAULT_IMAGE_FETCH_MAX_BYTES = 20 * 1024 * 1024; // 20MB safety cap for inline images

export interface ImagePayload {
    buffer: Buffer;
    filename: string;
    contentType: string;
}

/**
 * 下载图片 URL 或读取本地文件,返回上传所需的 buffer + 文件名 + MIME。
 *
 * @param url - 远端 URL（http/https）或本地文件路径
 * @param options.maxBytes - 远端下载大小上限，默认 20MB
 * @throws 下载/读取失败或超时
 */
export async function loadImageAsPayload(
    url: string,
    options?: { maxBytes?: number },
): Promise<ImagePayload> {
    const src = String(url ?? "").trim();
    if (!src) {
        throw new Error("Image source URL is empty");
    }

    if (/^https?:\/\//i.test(src)) {
        const result = await fetchRemoteMedia({
            url: src,
            maxBytes: options?.maxBytes ?? DEFAULT_IMAGE_FETCH_MAX_BYTES,
            filePathHint: src,
            requestInit: {
                headers: { "user-agent": DEFAULT_FETCH_USER_AGENT },
            },
        });
        const filename =
            result.fileName?.trim() ||
            (() => {
                try {
                    const last = new URL(src).pathname.split("/").pop() || "";
                    return last || "image";
                } catch {
                    return "image";
                }
            })();
        const contentType =
            result.contentType?.trim() ||
            inferMimeFromFilename(filename) ||
            "application/octet-stream";
        return { buffer: result.buffer, filename, contentType };
    }

    const fs = await import("node:fs/promises");
    const path = await import("node:path");
    const buffer = await fs.readFile(src);
    const filename = path.basename(src) || "image";
    const contentType = inferMimeFromFilename(filename) || "application/octet-stream";
    return { buffer, filename, contentType };
}

function inferMimeFromFilename(name: string): string | undefined {
    const ext = name.includes(".") ? name.split(".").pop()!.toLowerCase() : "";
    if (!ext) return undefined;
    return MIME_BY_EXT[ext];
}
