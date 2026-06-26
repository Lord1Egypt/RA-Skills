/**
 * Knowledge base dual-write hooks.
 *
 * 在 inbound 消息处理完成、回复送出后异步调用，将对话转录：
 *  1) 写入本地 `{localPath}/wechat-service/{accountId}/{openid}/{YYYY-MM-DD}.md`
 *  2) 同步到 Odoo knowledge.article（按 title 去重，存在则追加 body）
 *
 * 两个 backend 独立 best-effort：一个失败不影响另一个；整体绝不 throw。
 */

import type {
  ResolvedWechatServiceAccount,
  WechatServiceUnifiedInboundEvent,
} from "../types.js";
import { writeLocalTranscript } from "./local-sync.js";
import { writeOdooTranscript } from "./odoo-sync.js";

export type DualWriteInboundTranscriptParams = {
  account: ResolvedWechatServiceAccount;
  event: WechatServiceUnifiedInboundEvent;
  replyText: string;
};

export async function dualWriteInboundTranscript(
  params: DualWriteInboundTranscriptParams,
): Promise<void> {
  const { account } = params;
  if (!account.knowledgeSync?.enabled) return;

  const tasks: Array<Promise<unknown>> = [];

  tasks.push(
    writeLocalTranscript(params).catch((err) => {
      console.error(
        `[wechat-service] knowledge_local_write_failed accountId=${account.accountId}: ${err instanceof Error ? err.message : String(err)}`,
      );
    }),
  );

  if (account.knowledgeSync.odoo?.url) {
    tasks.push(
      writeOdooTranscript(params).catch((err) => {
        console.error(
          `[wechat-service] knowledge_odoo_write_failed accountId=${account.accountId}: ${err instanceof Error ? err.message : String(err)}`,
        );
      }),
    );
  }

  await Promise.allSettled(tasks);
}
