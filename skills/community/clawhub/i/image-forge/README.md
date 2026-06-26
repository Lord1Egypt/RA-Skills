# image-forge

> AI 画图统一路由技能 for OpenClaw — 三维路由体系 × 双后端调度

## 功能概览

- **5 条意图路径**：风格反推 / 参考图编辑 / 风格库 / 用途路由 / 直接生成
- **37 种风格**：10 Signature（独立 YAML） + 15 Rendering（inline modifier） + 12 Logo 展示背景
- **12 类用途**：海报/头像/电商/YouTube/社媒/App/漫画/游戏/信息图/logo 展示等
- **双后端调度**：GPT Image 2（写实/产品/文字）/ Gemini Imagen 3（动漫/艺术/多参考图）
- **Prompt 库**：15 个场景 JSON，含 YouMind/EvoLink 实战案例精炼

## 安装

```bash
# 通过 clawhub 安装（推荐）
clawhub install image-forge

# 或手动克隆
git clone https://github.com/your-username/image-forge
# 将 image-forge/ 目录放入 OpenClaw workspace/skills/ 下
```

## 环境配置

复制 `.env.example` 并填入你的 key：

```bash
cp .env.example .env
```

| 变量 | 说明 | 必填 |
|------|------|------|
| `CRS_API_KEY` | Claude Relay Service API Key（用于 GPT Image 2） | GPT Image 2 后端必填 |
| `CRS_BASE_URL` | CRS 服务地址，默认 `http://127.0.0.1:8765` | 可选 |
| `GEMINI_API_KEY` | Google Gemini API Key（用于 Nano Banana 2） | Gemini 后端必填 |
| `NANO_BANANA_API_KEY` | Nano Banana API Key（备用） | 可选 |

> **注**：CRS（Claude Relay Service）是一个 self-hosted OpenAI 兼容代理，通过 ChatGPT Plus 账号访问 GPT Image 2。如果你没有 CRS，可以配置任何兼容 `/openai/v1/images/generations` 的服务，或直接使用 OpenAI 官方 API。

## 后端支持

| 后端 | 调用方式 | 擅长场景 |
|------|---------|---------|
| GPT Image 2 | CRS / 任意 OpenAI 兼容端点 | 写实摄影、产品图、文字渲染、4K、海报 |
| Gemini Imagen 3 | `scripts/generate_image.py` | 动漫、插画、中国风、水彩、多参考图 |

要切换为官方 OpenAI API，修改 `backends.yaml`：

```yaml
- id: gpt-image-2
  endpoint: "https://api.openai.com/v1/images/generations"
  auth_header: "Bearer $OPENAI_API_KEY"
```

## 扩展

- **加新风格** → `styles/index.yaml`
- **加新用途** → `use-cases/index.yaml` + `references/`
- **加新后端** → `backends.yaml`
- 详细说明见 `EXTEND.md`

## 许可证

- 本技能代码：MIT
- `references/` 下来源于 YouMind/EvoLink 的 JSON 内容：CC BY 4.0（见下方致谢）
- Signature 风格 YAML（原创）：MIT

## 致谢

- [YouMind-OpenLab/awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2) (CC BY 4.0) — 用途分类体系 + prompt 案例
- [EvoLinkAI/awesome-gpt-image-2-prompts](https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts) (CC BY 4.0) — 实战 prompt 案例
- [YouMind-OpenLab/awesome-nano-banana-pro-prompts](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts) — Gemini 用途 JSON 原始来源
