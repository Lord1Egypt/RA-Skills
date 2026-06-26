import crypto from "node:crypto";
import { decodeEncodingAESKey, pkcs7Unpad, WECOM_PKCS7_BLOCK_SIZE } from "./crypto.js";
import { readResponseBodyAsBuffer, wecomFetch, type WecomHttpOptions } from "./http.js";

export type DecryptedWecomMedia = {
    buffer: Buffer;
    sourceContentType?: string;
    sourceFilename?: string;
    sourceUrl?: string;
};

function normalizeMime(contentType?: string | null): string | undefined {
    const raw = String(contentType ?? "").trim();
    if (!raw) return undefined;
    return raw.split(";")[0]?.trim().toLowerCase() || undefined;
}

function extractFilenameFromContentDisposition(disposition?: string | null): string | undefined {
    const raw = String(disposition ?? "").trim();
    if (!raw) return undefined;

    const star = raw.match(/filename\*\s*=\s*([^;]+)/i);
    if (star?.[1]) {
        const v = star[1].trim().replace(/^UTF-8''/i, "").replace(/^"(.*)"$/, "$1");
        try {
            const decoded = decodeURIComponent(v);
            if (decoded.trim()) return decoded.trim();
        } catch { /* ignore */ }
        if (v.trim()) return v.trim();
    }

    const plain = raw.match(/filename\s*=\s*([^;]+)/i);
    if (plain?.[1]) {
        const v = plain[1].trim().replace(/^"(.*)"$/, "$1").trim();
        if (v) return v;
    }
    return undefined;
}

/**
 * **decryptWecomMedia (解密企业微信媒体文件)**
 * 
 * 简易封装：直接传入 URL 和 AES Key 下载并解密。
 * 企业微信媒体文件使用与消息体相同的 AES-256-CBC 加密，IV 为 AES Key 前16字节。
 * 解密后需移除 PKCS#7 填充。
 */
export async function decryptWecomMedia(url: string, encodingAESKey: string, maxBytes?: number): Promise<Buffer> {
    return decryptWecomMediaWithHttp(url, encodingAESKey, { maxBytes });
}

/**
 * **decryptWecomMediaWithHttp (解密企业微信媒体 - 高级)**
 * 
 * 支持传递 HTTP 选项（如 Proxy、Timeout）。
 * 流程：
 * 1. 下载加密内容。
 * 2. 准备 AES Key 和 IV。
 * 3. AES-CBC 解密。
 * 4. PKCS#7 去除填充。
 */
export async function decryptWecomMediaWithHttp(
    url: string,
    encodingAESKey: string,
    params?: { maxBytes?: number; http?: WecomHttpOptions },
): Promise<Buffer> {
    const decrypted = await decryptWecomMediaWithMeta(url, encodingAESKey, params);
    return decrypted.buffer;
}

/**
 * **decryptWecomMediaWithMeta (解密企业微信媒体并返回源信息)**
 * 
 * 在返回解密结果的同时，保留下载响应中的元信息（content-type / filename / final url），
 * 供上层更准确地推断文件后缀和 MIME。
 */
export async function decryptWecomMediaWithMeta(
    url: string,
    encodingAESKey: string,
    params?: { maxBytes?: number; http?: WecomHttpOptions },
): Promise<DecryptedWecomMedia> {
    // 1. Download encrypted content
    const res = await wecomFetch(url, undefined, { ...params?.http, timeoutMs: params?.http?.timeoutMs ?? 15_000 });
    if (!res.ok) {
        throw new Error(`failed to download media: ${res.status}`);
    }
    const sourceContentType = normalizeMime(res.headers.get("content-type"));
    const sourceFilename = extractFilenameFromContentDisposition(res.headers.get("content-disposition"));
    const sourceUrl = res.url || url;
    const encryptedData = await readResponseBodyAsBuffer(res, params?.maxBytes);

    // 2. Prepare Key and IV
    const aesKey = decodeEncodingAESKey(encodingAESKey);
    const iv = aesKey.subarray(0, 16);

    // 3. Decrypt
    const decipher = crypto.createDecipheriv("aes-256-cbc", aesKey, iv);
    decipher.setAutoPadding(false); // We handle padding manually
    const decryptedPadded = Buffer.concat([
        decipher.update(encryptedData),
        decipher.final(),
    ]);

    // 4. Unpad
    // Note: Unlike msg bodies, usually removing PKCS#7 padding is enough for media files.
    // The Python SDK logic: pad_len = decrypted_data[-1]; decrypted_data = decrypted_data[:-pad_len]
    // Our pkcs7Unpad function does exactly this + validation.
    return {
        buffer: pkcs7Unpad(decryptedPadded, WECOM_PKCS7_BLOCK_SIZE),
        sourceContentType,
        sourceFilename,
        sourceUrl,
    };
}
