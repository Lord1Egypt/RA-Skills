/**
 * v6.6.8: 全模块 hook 防御性包裹工具
 *
 * 触发原因：用户实测 v6.6.5/6.6.6/6.6.7 升级后**反复**撞 "Something went wrong while processing
 * your request"。v6.6.6 只把 ctx-watchdog 的 6 个 hook 包了 safeHook，但 enhance 总共有
 * **28 个 hook 跨 17 个模块**，剩 22 个完全裸奔——任何一个抛 unhandled exception 都会让
 * OpenClaw 整个请求 fail-fast。
 *
 * 修法：proxy 整个 OpenClawPluginApi，拦截 api.on()，让所有 hook handler 自动包 try/catch。
 * 这样不用手工逐个包 22 个 hook（容易漏 + 容易 typo），一次性给所有 enhance 模块同时上保险。
 *
 * 关键不变：
 *   - hook 抛 → log error + return undefined（不影响主流程）
 *   - hook 返 undefined / void → 透传原样（不要把 undefined 变 truthy）
 *   - hook 返 result → 透传原样
 *   - api.on 的 priority opts 透传
 *   - 其他 api.* 方法透传不动
 */
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

/**
 * 用 Proxy 包裹 api，让 api.on 注册的所有 hook handler 都自动加 try/catch。
 * 已被 ctx-watchdog 内部 safeHook() 二次包过的 handler 不影响（双层 try-catch 仍只 catch 一次）。
 *
 * 注意：proxy 缓存在外部，**对同一个 api 只 wrap 一次**（避免 hot-reload 时双层 proxy）。
 */
export function wrapApiForSafeHooks(api: OpenClawPluginApi): OpenClawPluginApi {
  // 标记位检测重复 wrap
  const marker = "__enhance_safehook_wrapped__";
  if ((api as any)[marker]) return api;

  const originalOn = api.on.bind(api);

  const safeOn = ((hookName: any, handler: any, opts?: any) => {
    const wrappedHandler = (event: any, ctx: any) => {
      try {
        return handler(event, ctx);
      } catch (err) {
        try {
          api.logger.error(
            `[enhance safeHook] ${String(hookName)} hook 异常已捕获（不影响主流程）: ${
              (err as Error)?.message ?? err
            }`,
          );
          // 调试场景：stack trace 第一行（可定位到哪个模块）
          const stack = (err as Error)?.stack;
          if (stack) {
            const firstFrame = stack.split("\n").slice(1, 3).join(" | ");
            api.logger.error(`[enhance safeHook] stack: ${firstFrame}`);
          }
        } catch {
          /* logger 也抛？吞掉避免无限循环 */
        }
        return undefined;
      }
    };
    return originalOn(hookName, wrappedHandler, opts);
  }) as typeof api.on;

  return new Proxy(api, {
    get(target, prop, receiver) {
      if (prop === "on") return safeOn;
      if (prop === marker) return true;
      return Reflect.get(target, prop, receiver);
    },
  });
}
