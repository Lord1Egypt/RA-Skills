# OpenCode Free Models

自动配置 opencode.ai 免费 AI 模型到 OpenClaw/QClaw。

## 快速使用

```
配置 opencode 免费模型
```

OpenClaw 会自动:
1. 从 opencode.ai 获取免费模型列表
2. 添加到 ~/.openclaw/openclaw.json
3. 使用 "public" 作为 API Key

## 支持的免费模型

| 模型 | 推理 | 上下文 |
|------|------|--------|
| minimax-m2.5-free | ✅ | 131K |
| trinity-large-preview-free | ✅ | - |
| nemotron-3-super-free | ✅ | - |

## 手动运行

```bash
python3 scripts/configure-models.py
```

## 配置文件位置

- OpenClaw: ~/.openclaw/openclaw.json
- QClaw: ~/.qclaw/openclaw.json

## 仓库

- GitHub: https://github.com/pinke/opencode-free-models-skills
- ClawHub: https://clawhub.ai/skill/opencode-free-models