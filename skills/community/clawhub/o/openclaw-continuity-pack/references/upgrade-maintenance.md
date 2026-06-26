# Upgrade Maintenance

## 为什么需要这份文档
Continuity pack 目前仍然是增强层，不是 OpenClaw 原生的 thread-first 架构。
这意味着 OpenClaw 升级后，最容易断的是 patch 锚点，而不是 workflow 模板。

## 升级后最容易漂移的文件

### 高风险
- `src/gateway/thread-rollover.ts`
- `src/gateway/server-methods/chat.ts`
- `src/agents/pi-embedded-runner/session-manager-init.ts`
- `ui/src/ui/chat-event-reload.ts`
- `ui/src/ui/controllers/chat.ts`
- `ui/src/ui/views/chat.ts`

### 中风险
- `src/config/sessions/types.ts`
- `src/gateway/session-utils.ts`
- `src/gateway/session-utils.types.ts`
- `ui/src/ui/app-view-state.ts`
- `ui/src/ui/app-render.ts`

### 低风险
- `AGENTS.md`
- `SESSION_CONTINUITY.md`
- `plans/status/handoff` 模板

## 升级后的最短检查顺序
1. 先在目标源码树里跑：

```bash
python3 <PACK_ROOT>/scripts/continuity_doctor.py --source-root <OPENCLAW_SOURCE_ROOT>
```

2. doctor 通过后，再检查 patch 是否还能干净应用：

```bash
python3 <PACK_ROOT>/scripts/apply_runtime_patch.py --source-root <OPENCLAW_SOURCE_ROOT>
```

3. 真正应用 patch 后，必须重新构建：

```bash
cd <OPENCLAW_SOURCE_ROOT>
pnpm build
pnpm ui:build
```

4. 最后按 `verify.md` 做 disposable thread continuity 验收

## doctor 失败时先看什么
1. `chat.history` 响应体里 continuity 字段是否还在
2. `prepareThreadedSessionForChat(...)` 是否仍在 `chat.send` 主入口被调用
3. `session-manager-init.ts` 是否仍保留 `__openclawThreadHandoff`
4. `chat-event-reload.ts` 的 final refresh 是否还在
5. `views/chat.ts` 是否仍然隐藏 continuity/context 提示

## 一句话原则
版本升级后不要先上 live。
先跑 doctor，再检查 patch，再重建，再做 disposable thread continuity 验收。
