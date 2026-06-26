# ADR 0002 — 移除自动切换模型（model-router）

## 决策（v6.7.19）

删除 `src/modules/model-router.ts`（自动按任务复杂度/配额/熔断在 `before_model_resolve` 切模型），**保留** context-watchdog 的上下文超限保护切换。

## 背景

model-router 长期是问题源（CHANGELOG 多次为它 hotfix：deepseek 100% 400、sidus 429 限流卡长任务、bare id 等）。产品上希望模型选择**可预期** —— 交回龙虾原生 / 用户配置，不被插件自动改。

## 范围（关键）

「自动切换模型」其实有两处：
1. **model-router**：通用任务路由 —— **移除**。
2. **context-watchdog**：ctx 95% 超限时强切大 ctx 模型防 overflow —— **保留**（这是安全网，不是通用路由；另有 70/85/95% 预警 banner + 手动切换工具 `enhance_route_to_long_ctx` / `enhance_route_revert_to_original`）。

## 实现

- 删 model-router.ts、index.ts 注册块与 import、`ModelRouterConfig`（types.ts）、manifest `contracts.tools` 的 7 个 `enhance_model_route_*`。
- 更新 context-watchdog 里引用 model-router 的用户可见消息（切回原模型时不再承诺「model-router 重新路由」，改为「恢复默认模型」）。
- **保留** `latency-tracker` / `route-history` / `model-route-config`：context-watchdog 的 `isModelBanned` 仍 import；model-router 走后 ban 列表无人填充 → 该检查变 no-op，无害，不必删（删了反而要改 context-watchdog import）。

## 后果

- 模型行为可预期；少一个 hotfix 高发模块。
- ctx 超限保护不受影响。
