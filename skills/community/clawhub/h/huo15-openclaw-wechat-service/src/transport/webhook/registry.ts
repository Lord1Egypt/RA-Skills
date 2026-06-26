/**
 * 微信服务号 webhook 目标注册表
 *
 * 每个账号在 gateway lifecycle startAccount 时注册一个目标；
 * 请求进入时按路径匹配，多个账号可共用同一路径（通过签名 token 区分）。
 */

import type { PluginRuntime } from "openclaw/plugin-sdk";

import type {
  ResolvedWechatServiceAccount,
  WechatServiceEncryptMode,
} from "../../types.js";

export type WebhookTarget = {
  account: ResolvedWechatServiceAccount;
  path: string;
  runtime: {
    log?: (msg: string) => void;
    error?: (msg: string) => void;
  };
  core?: PluginRuntime;
  encryptMode: WechatServiceEncryptMode;
  touchTransportSession?: (patch: {
    running?: boolean;
    lastInboundAt?: number;
  }) => void;
};

const targets = new Map<string, WebhookTarget[]>();

export function registerWebhookTarget(target: WebhookTarget): () => void {
  const list = targets.get(target.path) ?? [];
  list.push(target);
  targets.set(target.path, list);
  return () => unregisterWebhookTarget(target);
}

export function unregisterWebhookTarget(target: WebhookTarget): void {
  const list = targets.get(target.path) ?? [];
  const next = list.filter(
    (entry) => entry.account.accountId !== target.account.accountId,
  );
  if (next.length === 0) {
    targets.delete(target.path);
  } else {
    targets.set(target.path, next);
  }
}

export function getWebhookTargets(path: string): WebhookTarget[] {
  return targets.get(path) ?? [];
}

export function listAllWebhookTargets(): WebhookTarget[] {
  const out: WebhookTarget[] = [];
  for (const list of targets.values()) out.push(...list);
  return out;
}

export function clearWebhookTargets(): void {
  targets.clear();
}
