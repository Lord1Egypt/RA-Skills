/**
 * Multi-Agent Group Chat Plugin v2.0
 * 
 * 功能：子 Agent 完成任务后，自动将回复发送到来源群聊
 * 特性：
 * - 自动检测来源群，无需配置群 ID
 * - 支持 Telegram 和飞书
 * - 仅处理 sessions_send 来的内部任务
 */

interface PluginConfig {
  enabled?: boolean;
}

interface SessionMeta {
  source?: string;
  sourceChannel?: string;
  sourceChatId?: string;
  sourceAccountId?: string;
  parentSessionKey?: string;
  [key: string]: any;
}

interface AgentEndEvent {
  messages?: Array<{ role: string; content: string }>;
  finalReply?: string;
  [key: string]: any;
}

interface AgentContext {
  agentId?: string;
  sessionKey?: string;
  sessionMeta?: SessionMeta;
  source?: string;
  [key: string]: any;
}

export default function (api: any) {
  
  /**
   * 从 context 中提取来源群信息
   */
  function extractSourceInfo(ctx: AgentContext): {
    channel: string | null;
    chatId: string | null;
    accountId: string | null;
  } {
    const meta = ctx?.sessionMeta || {};
    
    // 尝试多种可能的字段名
    const channel = meta.sourceChannel 
      || meta.channel 
      || meta.inboundChannel
      || null;
    
    const chatId = meta.sourceChatId 
      || meta.chatId 
      || meta.sourceChat 
      || meta.inboundChatId
      || meta.groupId
      || null;
    
    const accountId = meta.sourceAccountId 
      || meta.accountId 
      || ctx?.agentId
      || null;

    return { channel, chatId, accountId };
  }

  /**
   * 检查是否是内部任务（来自 sessions_send）
   */
  function isInternalTask(ctx: AgentContext): boolean {
    const source = ctx?.sessionMeta?.source 
      || ctx?.source 
      || ctx?.sessionMeta?.parentSessionKey
      || "";
    
    // 检查是否来自 sessions_send 或有父 session
    return source.includes("sessions_send") 
      || source.includes("session_send")
      || source.includes("subagent")
      || (typeof ctx?.sessionMeta?.parentSessionKey === "string" 
          && ctx.sessionMeta.parentSessionKey.length > 0);
  }

  /**
   * 获取 Agent 的最终回复
   */
  function getFinalReply(event: AgentEndEvent): string | null {
    // 优先使用 finalReply
    if (event?.finalReply && event.finalReply !== "NO_REPLY") {
      return event.finalReply;
    }

    // 从 messages 中获取最后一条 assistant 消息
    const messages = event?.messages || [];
    const assistantMessages = messages.filter((m) => m.role === "assistant");
    
    if (assistantMessages.length === 0) {
      return null;
    }

    const lastMessage = assistantMessages[assistantMessages.length - 1];
    const content = lastMessage?.content;

    if (!content || content === "NO_REPLY" || content.trim() === "") {
      return null;
    }

    return content;
  }

  // 主逻辑：监听 agent_end 事件
  api.on("agent_end", async (event: AgentEndEvent, ctx: AgentContext) => {
    try {
      // 1. 检查是否是内部任务
      if (!isInternalTask(ctx)) {
        api.logger?.debug?.("[multi-agent-chat] 非内部任务，跳过");
        return;
      }

      // 2. 获取来源群信息
      const { channel, chatId, accountId } = extractSourceInfo(ctx);
      
      if (!chatId) {
        api.logger?.debug?.("[multi-agent-chat] 无法获取来源群 ID，跳过");
        return;
      }

      // 3. 获取回复内容
      const reply = getFinalReply(event);
      
      if (!reply) {
        api.logger?.debug?.("[multi-agent-chat] 无有效回复，跳过");
        return;
      }

      // 4. 确定使用的 channel 和 accountId
      const finalChannel = channel || "telegram";
      const finalAccountId = accountId || ctx?.agentId || "default";

      // 5. 发送到群里
      api.logger?.info?.(
        `[multi-agent-chat] ${finalAccountId} → ${finalChannel}:${chatId}: ${reply.slice(0, 50)}...`
      );

      // 尝试使用 gateway.rpc
      if (api.gateway?.rpc) {
        await api.gateway.rpc("message.send", {
          channel: finalChannel,
          accountId: finalAccountId,
          target: chatId,
          message: reply
        });
      } 
      // 备选：使用 runtime.message
      else if (api.runtime?.message?.send) {
        await api.runtime.message.send({
          channel: finalChannel,
          accountId: finalAccountId,
          target: chatId,
          message: reply
        });
      }
      // 备选：使用 api.message
      else if (api.message?.send) {
        await api.message.send({
          channel: finalChannel,
          accountId: finalAccountId,
          target: chatId,
          message: reply
        });
      }
      else {
        api.logger?.warn?.("[multi-agent-chat] 找不到消息发送 API");
      }

    } catch (err: any) {
      api.logger?.error?.(
        `[multi-agent-chat] 发送失败: ${err?.message || err}`
      );
    }
  });

  api.logger?.info?.("[multi-agent-chat] 插件已加载 v2.0（自动检测来源群）");
}
