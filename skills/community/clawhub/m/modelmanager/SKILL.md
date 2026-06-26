---
name: model-manager
description: |
  OpenClaw 模型管理工具。用于查看、设置和管理 OpenClaw 使用的大语言模型。
  当用户提到以下场景时使用：切换模型、查看可用模型、设置备用模型、管理模型降级。
  重要：此 skill 必须在获得用户明确指示后才能使用。
---

# model-manager

OpenClaw 模型管理工具，用于查看、设置和管理当前使用的大语言模型（LLM）。

## ⚠️ 使用限制

- 查询操作（list, status, fallback list）无需授权，可自由使用
- 修改操作（set, fallback add/remove）必须获得用户的明确指示才能使用
- 未经许可，不得自动切换模型或修改模型配置

## 前置依赖

- OpenClaw 已正常运行
- 已配置模型提供者（如 qclaw、ollama 等）

## 使用方式

所有命令通过以下格式执行：

```bash
python3 ~/.qclaw/workspace/skills/model-manager/scripts/model_manager.py <command> [args]
```

### 命令列表

| 命令 | 说明 | 示例 |
|------|------|------|
| `list` | 列出所有可用模型 | `./model_manager.py list` |
| `set <model_id>` | 设置默认模型 | `./model_manager.py set ollama/nemotron-3-super:cloud` |
| `fallback add <model_id>` | 添加备用模型 | `./model_manager.py fallback add ollama/ministral-3:14b` |
| `fallback remove <model_id>` | 移除备用模型 | `./model_manager.py fallback remove ollama/ministral-3:14b` |
| `fallback list` | 列出所有备用模型 | `./model_manager.py fallback list` |
| `status` | 查看当前模型状态 | `./model_manager.py status` |

### 示例用法

```bash
# 查看可用模型
python3 ~/.qclaw/workspace/skills/model-manager/scripts/model_manager.py list

# 切换到 Ollama 云端模型
python3 ~/.qclaw/workspace/skills/model-manager/scripts/model_manager.py set ollama/nemotron-3-super:cloud

# 添加本地模型作为备用
python3 ~/.qclaw/workspace/skills/model-manager/scripts/model_manager.py fallback add ollama/ministral-3:14b

# 查看当前状态
python3 ~/.qclaw/workspace/skills/model-manager/scripts/model_manager.py status
```

## 工作原理

此 skill 通过调用 OpenClaw 的内置 `models` CLI 命令来实现模型管理：

- 查询模型列表：`openclaw models list`
- 设置默认模型：`openclaw models set <model-id>`
- 管理备用模型：`openclaw models fallbacks add/remove/list <model-id>`
- 查看状态：`openclaw models status`

所有更改会保存到：
- `~/.qclaw/agents/main/agent/models.json`（当前会话）
- `~/.qclaw/openclaw.json`（全局配置）

## 注意事项

1. **查询自由，修改需授权**：list、status、fallback list 可直接使用；set、fallback add/remove 需要用户明确授权
2. **模型可用性取决于配置**：只有在 `openclaw.json` 中正确配置了对应的模型提供者后，才能成功切换
3. **切换时机**：模型变更将在下次新会话或模型调用失败时生效
4. **安全考虑**：防止未经授权的模型更改可能导致的成本增加或服务中断

## 示例场景

用户说： “列出当前可用模型”  
→ 无需授权，skill 可直接执行 list

用户说： “查看当前模型状态”  
→ 无需授权，skill 可直接执行 status

用户说： “把模型切换到 ollama/nemotron-3-super:cloud”  
→ 需要明确授权后，skill 才能执行 set 操作

用户说： “添加 ollama/ministral-3:14b 作为备用模型”  
→ 需要明确授权后，skill 才能执行 fallback add 操作