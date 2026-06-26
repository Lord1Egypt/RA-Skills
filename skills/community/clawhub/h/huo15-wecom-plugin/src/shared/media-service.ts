import type { OpenClawConfig, PluginRuntime } from "openclaw/plugin-sdk";
import { resolveWecomMediaMaxBytes } from "../config/index.js";
import { decryptWecomMediaWithMeta } from "../media.js";
import type { UnifiedInboundEvent } from "../types/index.js";
import type { NormalizedMediaAttachment } from "./media-types.js";

export class WecomMediaService {
  constructor(
    private readonly core: PluginRuntime,
    private readonly cfg: OpenClawConfig,
  ) {}

  private resolveInboundMaxBytes(accountId: string): number {
    return resolveWecomMediaMaxBytes(this.cfg, accountId);
  }

  async downloadRemoteMedia(params: {
    url: string;
    maxBytes: number;
  }): Promise<NormalizedMediaAttachment> {
    const loaded = await this.core.channel.media.fetchRemoteMedia({
      url: params.url,
      maxBytes: params.maxBytes,
    });
    return {
      buffer: loaded.buffer,
      contentType: loaded.contentType,
      filename: loaded.fileName,
    };
  }

  /**
   * Download and decrypt WeCom AES-encrypted media.
   * Bot-ws: each message carries a unique per-URL aeskey in the message body.
   * Bot-webhook: uses the account-level EncodingAESKey.
   * Both use AES-256-CBC with PKCS#7 padding (32-byte block), IV = key[:16].
   */
  async downloadEncryptedMedia(params: {
    url: string;
    aesKey: string;
    maxBytes: number;
  }): Promise<NormalizedMediaAttachment> {
    const decrypted = await decryptWecomMediaWithMeta(params.url, params.aesKey, {
      maxBytes: params.maxBytes,
    });
    return {
      buffer: decrypted.buffer,
      contentType: decrypted.sourceContentType,
      filename: decrypted.sourceFilename,
    };
  }

  async saveInboundAttachment(
    event: UnifiedInboundEvent,
    attachment: NormalizedMediaAttachment,
  ): Promise<string> {
    const maxBytes = this.resolveInboundMaxBytes(event.accountId);
    const saved = await this.core.channel.media.saveMediaBuffer(
      attachment.buffer,
      attachment.contentType,
      "inbound",
      maxBytes,
      attachment.filename,
    );
    return saved.path;
  }

  async normalizeFirstAttachment(
    event: UnifiedInboundEvent,
  ): Promise<NormalizedMediaAttachment | undefined> {
    const first = event.attachments?.[0];
    if (!first?.remoteUrl) {
      return undefined;
    }
    return this.normalizeOneAttachment(event.accountId, first);
  }

  /**
   * v2.8.8 ⭐ 多图支持：把所有 attachments（不仅是首张）解密下载下来。
   *
   * 单条消息只能填一个 ctx.MediaPath，所以 session-manager 仍然把首张挂在 MediaPath 上；
   * 但这里把后续的也保存到 inbound dir，并把 path 记到 event.raw 上方便上层 staging。
   * 单个失败不阻塞整体，会降级为 undefined 并记录 warn。
   */
  async normalizeAllAttachments(
    event: UnifiedInboundEvent,
  ): Promise<NormalizedMediaAttachment[]> {
    const list = event.attachments ?? [];
    if (list.length === 0) return [];
    const results: NormalizedMediaAttachment[] = [];
    for (let i = 0; i < list.length; i += 1) {
      const attachment = list[i];
      if (!attachment?.remoteUrl) continue;
      try {
        const normalized = await this.normalizeOneAttachment(event.accountId, attachment);
        if (normalized) results.push(normalized);
      } catch (err) {
        console.warn(
          `[wecom-media] attachment#${i} normalize failed url=${attachment.remoteUrl} ${err instanceof Error ? err.message : String(err)}`,
        );
      }
    }
    return results;
  }

  private async normalizeOneAttachment(
    accountId: string,
    attachment: NonNullable<UnifiedInboundEvent["attachments"]>[number],
  ): Promise<NormalizedMediaAttachment | undefined> {
    if (!attachment?.remoteUrl) return undefined;
    // Keep fetch/decrypt/save on the same account-aware limit instead of falling back
    // to the core media store default (5MB).
    const maxBytes = this.resolveInboundMaxBytes(accountId);
    if (attachment.aesKey) {
      return this.downloadEncryptedMedia({
        url: attachment.remoteUrl,
        aesKey: attachment.aesKey,
        maxBytes,
      });
    }
    return this.downloadRemoteMedia({ url: attachment.remoteUrl, maxBytes });
  }
}
