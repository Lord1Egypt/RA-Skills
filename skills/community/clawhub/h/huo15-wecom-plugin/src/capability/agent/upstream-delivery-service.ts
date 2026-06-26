import type { ResolvedAgentAccount } from "../../types/index.js";
import { resolveScopedWecomTarget } from "../../target.js";
import { deliverUpstreamAgentApiMedia, deliverUpstreamAgentApiText } from "../../transport/agent-api/upstream-delivery.js";
import { canUseAgentApiDelivery } from "./fallback-policy.js";
import { getWecomRuntime } from "../../runtime.js";

/**
 * 上下游企业消息发送服务
 * 
 * 使用下游企业的 access_token 和 agentId 发送消息
 */
export class WecomUpstreamAgentDeliveryService {
  constructor(
    private readonly upstreamAgent: ResolvedAgentAccount,
    private readonly primaryAgent: ResolvedAgentAccount,
  ) { }

  assertAvailable(): void {
    if (!canUseAgentApiDelivery(this.upstreamAgent)) {
      throw new Error(
        `WeCom upstream outbound requires channels.wecom.accounts.<accountId>.agent.agentId for upstream corp=${this.upstreamAgent.corpId}.`,
      );
    }
  }

  resolveTargetOrThrow(to: string | undefined) {
    const scoped = resolveScopedWecomTarget(to, this.upstreamAgent.accountId);
    if (!scoped) {
      console.error(`[wecom-upstream-delivery] missing target account=${this.upstreamAgent.accountId}`);
      throw new Error("WeCom upstream outbound requires a target (userid, partyid, tagid or chatid).");
    }
    if (scoped.accountId && scoped.accountId !== this.upstreamAgent.accountId) {
      console.error(
        `[wecom-upstream-delivery] account mismatch current=${this.upstreamAgent.accountId} targetAccount=${scoped.accountId} raw=${String(to ?? "")}`,
      );
      throw new Error(
        `WeCom upstream outbound account mismatch: target belongs to account=${scoped.accountId}, current account=${this.upstreamAgent.accountId}.`,
      );
    }
    const target = scoped.target;
    // v2.8.12: 与 delivery-service.ts 对齐，不再硬性拒绝群聊 chatid。上游 Agent 若有
    // 群聊权限即可正常发送，无权限时由 WeCom API 返回错误，上层 catch 降级处理。
    if (target.chatid) {
      console.warn(
        `[wecom-upstream-delivery] group chat delivery via Agent API (may fail with 86008) account=${this.upstreamAgent.accountId} chatId=${target.chatid}`,
      );
    }
    return target;
  }

  async sendText(params: { to: string | undefined; text: string }): Promise<void> {
    this.assertAvailable();
    const target = this.resolveTargetOrThrow(params.to);
    console.log(
      `[wecom-upstream-delivery] sendText account=${this.upstreamAgent.accountId} corpId=${this.upstreamAgent.corpId} to=${String(params.to ?? "")} len=${params.text.length}`,
    );

    const runtime = getWecomRuntime();
    const chunks = runtime.channel.text.chunkText(params.text, 2048);

    for (const chunk of chunks) {
      if (!chunk.trim()) continue;
      await deliverUpstreamAgentApiText({
        upstreamAgent: this.upstreamAgent,
        primaryAgent: this.primaryAgent,
        target,
        text: chunk,
      });
    }
  }

  async sendMedia(params: {
    to: string | undefined;
    text?: string;
    buffer: Buffer;
    filename: string;
    contentType: string;
  }): Promise<void> {
    this.assertAvailable();
    const target = this.resolveTargetOrThrow(params.to);
    console.log(
      `[wecom-upstream-delivery] sendMedia account=${this.upstreamAgent.accountId} corpId=${this.upstreamAgent.corpId} to=${String(params.to ?? "")} filename=${params.filename} contentType=${params.contentType}`,
    );
    await deliverUpstreamAgentApiMedia({
      upstreamAgent: this.upstreamAgent,
      primaryAgent: this.primaryAgent,
      target,
      buffer: params.buffer,
      filename: params.filename,
      contentType: params.contentType,
      text: params.text,
    });
  }
}
