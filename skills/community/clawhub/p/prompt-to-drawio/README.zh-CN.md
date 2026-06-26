# prompt-to-drawio

[English](README.md) | [简体中文](README.zh-CN.md)

这是一个面向 CLI 的 draw.io 技能：可将自然语言提示词转换为图，并支持编辑、导出与校验，无需前端。

## 安装

### 方案 A：`npx skills` 多 Agent 安装（推荐）

如果你希望同一套命令覆盖 Codex / Claude Code / 其他支持的 Agent，可使用 [`npx skills`](https://github.com/vercel-labs/skills)。

默认安装到当前检测到的 Agent：

```bash
npx skills@latest add lzfxxx/prompt-to-drawio-skill
```

仅安装到 Codex：

```bash
npx skills@latest add lzfxxx/prompt-to-drawio-skill -a codex
```

仅安装到 Claude Code：

```bash
npx skills@latest add lzfxxx/prompt-to-drawio-skill -a claude-code
```

全局安装（跨项目共享）：

```bash
npx skills@latest add lzfxxx/prompt-to-drawio-skill -g -y
```

说明：

- `npx skills` 是社区开源安装器，不是所有 Agent 产品内置命令。
- 如果你的环境不支持，请使用下方手动安装方案。

### 方案 B：手动安装（Codex 本地）

```bash
mkdir -p "$HOME/.codex/skills"
git clone https://github.com/lzfxxx/prompt-to-drawio-skill.git "$HOME/.codex/skills/prompt-to-drawio"
```

更新到最新：

```bash
git -C "$HOME/.codex/skills/prompt-to-drawio" pull
```

## 技能能力

- 提示词生成 `.drawio`
- 提示词编辑已有 `.drawio`
- 导出 `png/svg/pdf/jpg`
- 支持文件 / URL / 图片 / PDF 上下文
- 支持 shape library 查询
- 支持视觉校验和重试

## 仓库结构

- `SKILL.md`: Codex 技能入口说明
- `scripts/prompt_to_drawio.py`: 运行时 CLI 脚本
- `references/`: 能力说明与渲染说明
- `agents/openai.yaml`: Agent 元信息

## 依赖要求

- Python `3.9+`
- draw.io CLI：`drawio`
- 可访问模型 API 的网络

快速检查：

```bash
python3 --version
drawio --help
```

## 配置

脚本使用 OpenAI-compatible 接口，建议将变量放在项目 `.env` 或 shell 环境中。

### Google Gemini（OpenAI-compatible）示例

```env
DRAWIO_LLM_API_KEY=YOUR_API_KEY
DRAWIO_LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
DRAWIO_LLM_MODEL=gemini-3-pro-preview

DRAWIO_VALIDATION_API_KEY=YOUR_API_KEY
DRAWIO_VALIDATION_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
DRAWIO_VALIDATION_MODEL=gemini-3-pro-preview
```

模型名建议：

- 推荐：`gemini-3-pro-preview`
- 避免使用旧模型名（如 `gemini-3-pro`），除非 provider 的模型列表确实存在

## 运行控制参数

- `--no-dotenv`: 禁用自动加载 `.env`
- `--dotenv-file /abs/path/.env`: 指定 `.env`
- `--no-config-summary`: 关闭启动时配置摘要打印
- `--no-model-preflight`: 跳过 `/models` 预检

`.env` 行为：

- 默认从当前工作目录向上查找最近 `.env`
- 优先级：CLI 参数 > 进程已有环境变量 > 自动加载 `.env`

## 使用示例

### 生成新图

```bash
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" generate \
  --prompt "Create a login + MFA + session flow" \
  --out-drawio "/tmp/auth-flow.drawio" \
  --out-image "/tmp/auth-flow.pdf" \
  --validate \
  --validate-soft
```

### 带上下文生成

```bash
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" generate \
  --prompt "Replicate architecture style and improve readability" \
  --file "/abs/path/requirements.pdf" \
  --file "/abs/path/reference.png" \
  --url "https://example.com/spec" \
  --shape-library aws4 \
  --out-drawio "/tmp/cloud.drawio" \
  --out-image "/tmp/cloud.svg"
```

### 编辑已有图

```bash
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" edit \
  --in-drawio "/tmp/cloud.drawio" \
  --prompt "Add WAF before ALB and split app tier into two services" \
  --out-drawio "/tmp/cloud-v2.drawio" \
  --out-image "/tmp/cloud-v2.png" \
  --validate \
  --validate-soft
```

### 仅导出

```bash
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" export \
  --in-drawio "/tmp/cloud-v2.drawio" \
  --out-image "/tmp/cloud-v2.pdf"
```

### 仅校验

```bash
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" validate \
  --in-drawio "/tmp/cloud-v2.drawio" \
  --fail-on-critical
```

### Shape library 查询

```bash
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" library --list
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" library --name aws4
```

## 输出约定

成功时会输出以下机器可读字段：

- `DRAWIO_FILE=...`
- `IMAGE_FILE=...`（如有导出）
- `BACKUP_FILE=...`（edit 时）
- `VALIDATION_JSON=`（启用校验时）

## 注意事项

- 启动时会打印有效配置摘要（dotenv 来源、最终 model/base_url、key 掩码）
- JSON 解析对 fenced/truncated 输出做了容错，仍失败时会把原响应写入临时文件
- 使用 `--validate-soft` 时，即使校验请求/解析失败，只要文件已生成仍返回 0
- 论文场景建议优先导出 `pdf/svg`

## 排障

### `HTTP 404 ... model not found`

- 先看启动摘要中的实际模型名
- 改为 provider 已发布模型
- Gemini 可优先尝试 `gemini-3-pro-preview`

### `Network error calling model endpoint`

- 检查目标域名 DNS/网络连通
- 在受限环境中，使用有网络权限的执行方式重试

### 环境看似配置了但实际不生效

- 默认会自动加载最近 `.env`，除非显式 `--no-dotenv`
- 可用 `--dotenv-file` 指定配置文件
- 以启动配置摘要为准

## 致谢与来源说明

本项目基于以下上游项目的思路与能力演进而来：

- [DayuanJiang/next-ai-draw-io](https://github.com/DayuanJiang/next-ai-draw-io)

当前仓库主要面向 CLI/Agent 技能场景（Codex、Claude Code 及其他 Agent 环境）做了封装与工程化增强，同时保持了上游项目的 prompt-to-diagram 核心方向。

## License

MIT
