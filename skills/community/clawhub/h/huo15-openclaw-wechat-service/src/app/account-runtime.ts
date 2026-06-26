/**
 * **WechatServiceAccountRuntime** —— 单账号运行时状态机
 *
 * 模仿 `@huo15/wecom` 的 `WecomAccountRuntime` 设计（参 `wecom/src/app/account-runtime.ts`），
 * 但删掉了 wechat-service 不需要的成分（多 transport session / audit log 注册表 / media service 类）。
 *
 * **核心职责**：
 *  - 持有当前账号的运行时状态（`running` / `lastInboundAt` / `lastOutboundAt` / `lastError`）
 *  - 暴露明确的 lifecycle 方法（`markStart` / `markStop` / `markInbound` / `markOutbound` / `markError`）
 *  - 提供 `getStatusSnapshot()` 给 `channel.ts:status.buildAccountSnapshot` 复用，避免散落在多处的状态读写
 *
 * 旧的 plain-object `AccountRuntime` 类型保留作 backward-compat alias，调用方代码无需改动。
 */

import type { ChannelGatewayContext } from "openclaw/plugin-sdk";

import type { ResolvedWechatServiceAccount } from "../types.js";

export type AccountRuntimeLogger = {
  info?: (msg: string) => void;
  warn?: (msg: string) => void;
  error?: (msg: string) => void;
  debug?: (msg: string) => void;
};

export type AccountRuntimeStatusSnapshot = {
  accountId: string;
  running: boolean;
  lastStartAt: number | null;
  lastStopAt: number | null;
  lastInboundAt: number | null;
  lastOutboundAt: number | null;
  lastError: string | null;
};

export class WechatServiceAccountRuntime {
  readonly accountId: string;
  readonly log: AccountRuntimeLogger;

  // status fields (kept public so legacy callers reading runtime.lastInboundAt etc still work)
  running: boolean = false;
  lastStartAt: number | null = null;
  lastStopAt: number | null = null;
  lastInboundAt: number | null = null;
  lastOutboundAt: number | null = null;
  lastError: string | null = null;

  constructor(params: {
    accountId: string;
    log?: AccountRuntimeLogger;
  }) {
    this.accountId = params.accountId;
    this.log = params.log ?? {};
  }

  /** 从 OpenClaw gateway context 构造 runtime（gateway-monitor.ts 用） */
  static fromGatewayContext(
    ctx: ChannelGatewayContext<ResolvedWechatServiceAccount>,
  ): WechatServiceAccountRuntime {
    return new WechatServiceAccountRuntime({
      accountId: ctx.account.accountId,
      log: {
        info: (msg) => ctx.log?.info(msg),
        warn: (msg) => ctx.log?.warn(msg),
        error: (msg) => ctx.log?.error(msg),
        debug: (msg) => ctx.log?.debug?.(msg),
      },
    });
  }

  // ---- lifecycle methods ----

  markStart(at: number = Date.now()): void {
    this.running = true;
    this.lastStartAt = at;
    this.lastStopAt = null;
    this.lastError = null;
  }

  markStop(at: number = Date.now()): void {
    this.running = false;
    this.lastStopAt = at;
  }

  markInbound(at: number = Date.now()): void {
    this.lastInboundAt = at;
  }

  markOutbound(at: number = Date.now()): void {
    this.lastOutboundAt = at;
  }

  markError(error: unknown, at: number = Date.now()): void {
    this.lastError = error instanceof Error ? error.message : String(error);
    void at; // reserved for future audit log
  }

  clearError(): void {
    this.lastError = null;
  }

  // ---- status snapshot (for channel.ts buildAccountSnapshot) ----

  getStatusSnapshot(): AccountRuntimeStatusSnapshot {
    return {
      accountId: this.accountId,
      running: this.running,
      lastStartAt: this.lastStartAt,
      lastStopAt: this.lastStopAt,
      lastInboundAt: this.lastInboundAt,
      lastOutboundAt: this.lastOutboundAt,
      lastError: this.lastError,
    };
  }
}

/**
 * **Backward-compat alias** —— 旧的 plain-object `AccountRuntime` 类型。
 *
 * v0.1 ~ v1.0.x 调用方代码用 `runtime.log.info()` / `runtime.lastInboundAt` 这种
 * 字段访问，不依赖 class 方法。`WechatServiceAccountRuntime` 作为 class 实现了所有
 * 这些字段，可以向后兼容。
 *
 * 新代码请直接用 `WechatServiceAccountRuntime`。
 */
export type AccountRuntime = WechatServiceAccountRuntime;
