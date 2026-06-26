---
name: kimi2.5skill
description: Troubleshoot and operate Kimi 2.5 / OpenClaw image understanding. Use when image recognition fails, OCR/images cannot be analyzed, `image` tool reports `Unknown model`, configured vision models are ignored at runtime, or you need a safe recovery workflow for OpenClaw image-capable models.
---

# kimi2.5skill

处理 OpenClaw 中 Kimi 2.5 / 识图模型的排障、恢复、验证与运维收口。

## 快速流程
1. 先做 runtime 实测，不要只看配置文件
2. 再检查：
   - `~/.openclaw/openclaw.json`
   - `~/.openclaw/agents/<agent>/agent/models.json`
3. 如果出现 `Unknown model`，优先怀疑 agent 级 `models.json` 的非法 provider 配置导致整份自定义模型注册表加载失败
4. 修复后必须重启 gateway，并跑一张真实图片回归测试

## 参考文件
- 修复流程：`references/recovery-playbook.md`
- 本次事件：`references/incident-2026-04-14.md`

## 本轮已验证结论（2026-04-14）
本轮问题的真实根因是：

> agent 级 `models.json` 中的自定义 `codex` provider 配置不合法，导致模型注册表加载异常，继而让 `image` runtime 报 `Unknown model`。

已验证修复点：
- `/Users/admin-ai/.openclaw/agents/qiang/agent/models.json`
- `/Users/admin-ai/.openclaw/agents/sally-bot/agent/models.json`

移除有问题的 `codex` provider 后，`image` 工具已成功返回图片描述，说明识图 runtime 恢复。

## 成功标准
以下同时满足才算修好：
- 不再出现 `Unknown model`
- `image` 工具返回正常图片描述 / OCR 结果
- gateway 状态正常
- 至少完成一张真实图片回归测试

## 收口口径
恢复后统一表述：
- 识图已恢复可用
- 根因是 agent 级 `models.json` 非法 provider 配置污染了 image runtime 注册表
- 后续若再遇 `Unknown model`，优先检查 `~/.openclaw/agents/<agent>/agent/models.json`
