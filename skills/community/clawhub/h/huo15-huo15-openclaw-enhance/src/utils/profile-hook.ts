/**
 * v5.8.0: profileHook 包装器
 *
 * 用法（替换 api.on 一对一调用）：
 *   import { profileHook } from "../utils/profile-hook.js";
 *   profileHook(api, "before_prompt_build", "prompt-enhancer", (event, ctx) => { ... });
 *
 * 行为零变化：内部 await handler，把返回值原样透传，异常原样 rethrow。
 * 唯一副作用：在 hook_profile 表写一条记录（duration_ms + status）。写表失败静默。
 *
 * 关闭开关：setHookProfilerEnabled(false) 后只 register handler，不写表。
 * 这样即使 DB 出问题，wrapped handler 也能正常跑。
 */
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { getDb } from "./sqlite-store.js";
import { insertHookProfile } from "./hook-profile-db.js";

const PLUGIN_ID = "@huo15/openclaw-enhance";

let _enabled = true;

export function setHookProfilerEnabled(enabled: boolean): void {
  _enabled = enabled;
}

export function isHookProfilerEnabled(): boolean {
  return _enabled;
}

type AnyHandler = (event: any, ctx: any) => any;

export function profileHook(
  api: OpenClawPluginApi,
  event: string,
  moduleName: string,
  handler: AnyHandler,
  options?: unknown,
): void {
  const wrapped: AnyHandler = async (e, ctx) => {
    if (!_enabled) return await handler(e, ctx);

    const t0 = Date.now();
    let status: "ok" | "error" = "ok";
    let errMsg: string | null = null;
    try {
      return await handler(e, ctx);
    } catch (err) {
      status = "error";
      errMsg = err instanceof Error ? err.message : String(err);
      throw err;
    } finally {
      const duration = Date.now() - t0;
      try {
        const db = getDb();
        insertHookProfile(db, {
          ts: t0,
          source: "wrap",
          hook_event: event,
          plugin_id: PLUGIN_ID,
          module: moduleName,
          duration_ms: duration,
          status,
          err_msg: errMsg,
        });
      } catch {
        // 静默 — profiler 写表失败不影响主流程
      }
    }
  };

  // 透传 options（priority 等 openclaw 4.24 hook 选项）
  if (options !== undefined) {
    (api.on as any)(event, wrapped, options);
  } else {
    (api.on as any)(event, wrapped);
  }
}
