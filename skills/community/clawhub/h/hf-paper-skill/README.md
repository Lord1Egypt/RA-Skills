# hf-paper-skill

HuggingFace Papers 热门论文获取与中文翻译

## 功能

- 获取 HuggingFace Papers 热门论文（日/周/月）
- **双翻译后端**：DeepLX 或 OpenAI 兼容 LLM（OpenAI、硅基流动、DeepSeek 等）
- 中英文摘要对照展示
- 趋势分析 + 推荐阅读排序
- **自动降级**：主后端失败时无缝切换到备用后端，都失败则保留英文原文

## 配置

### 依赖

```bash
pip3 install python-dotenv
```

### 翻译后端

翻译功能支持两种后端，通过 `.env` 文件配置（复制 `.env.example` 为 `.env` 并根据需要填写）：

**DeepLX（默认）：**
```env
TRANSLATE_BACKEND="deeplx"
DEEPLX_URL="https://api.deeplx.org/你的token/translate"
```

**OpenAI 兼容 LLM（OpenAI、硅基流动、DeepSeek 等）：**
```env
TRANSLATE_BACKEND="openai"
OPENAI_BASE_URL="https://api.openai.com/v1"
OPENAI_API_KEY="sk-your-key-here"
OPENAI_MODEL="gpt-4o-mini"
```

> 支持任意 OpenAI 兼容 API，只需修改 `OPENAI_BASE_URL` 和 `OPENAI_MODEL` 即可切换不同的 LLM 服务商。
> 主后端失败时自动降级到另一后端，都失败则保留英文原文。

## 使用方法

```bash
# 获取论文列表（今日热门）
python3 scripts/get_papers.py

# 生成分析报告（本周热门，自动翻译为中文）
mkdir -p reports
python3 scripts/generate_report.py --period weekly --output reports/HuggingFace_本周热门论文_$(date +%Y-%m-%d).md

# 指定数量和范围
python3 scripts/generate_report.py --period weekly --limit 10

# 纯英文输出
python3 scripts/generate_report.py --period weekly --no-translate
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--period` | daily / weekly / monthly | weekly |
| `--limit` | 论文数量 | 10 |
| `--output` | 输出文件路径 | stdout |
| `--no-translate` | 不翻译为中文 | false |

## 翻译

### DeepLX

专用翻译 API，速度快、成本低，适合大批量摘要翻译。通过 `DEEPLX_URL` 配置端点。

### OpenAI 兼容 LLM

通过 LLM 进行翻译，利用大模型的语义理解能力，翻译质量更高。支持任何兼容 OpenAI 格式的 API：

| 服务商 | BASE_URL | 推荐模型 |
|--------|----------|----------|
| OpenAI | `https://api.openai.com/v1` | `gpt-4o-mini` |
| 硅基流动 | `https://api.siliconflow.cn/v1` | `Qwen/Qwen2.5-7B-Instruct` |
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-chat` |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-turbo` |

## Agent 集成

将本 skill 接入不同的 AI Agent 框架，让 Agent 在用户问"最近有什么热门论文"时自动调起。

### Hermes Agent

```bash
# 方式一：克隆到 Hermes skills 目录
git clone https://github.com/isongxw/hf-paper-skill.git ~/.hermes/skills/research/hf-papers

# 方式二：如果已克隆到其他地方，创建软链接
ln -s /path/to/hf-paper-skill ~/.hermes/skills/research/hf-papers
```

完成后在 `.env` 中配置翻译 token，Hermes 下次启动时自动识别此 skill。

### Claude Code (Claude CLI)

将本 skill 目录添加到 Claude Code 的工作区中，或直接在项目中使用：

```bash
# 克隆到项目内
cd your-project
git clone https://github.com/isongxw/hf-paper-skill.git skills/hf-papers

# 在 CLAUDE.md 中添加配置说明
cat >> CLAUDE.md << 'EOF'

## hf-papers skill

路径：`skills/hf-papers/`
使用：`python3 skills/hf-papers/scripts/generate_report.py --period weekly --limit 10`
配置：复制 `skills/hf-papers/.env.example` 为 `skills/hf-papers/.env` 并填入 token
EOF
```

### OpenClaw

```bash
# 克隆到 OpenClaw workspace 的 skills 目录
git clone https://github.com/isongxw/hf-paper-skill.git /path/to/openclaw/workspace/skills/hf-papers
```

### 通用（任意框架）

本 skill 不依赖任何特定框架，纯 Python 脚本运行，通过 `.env` 文件配置。任何能执行 shell 命令的 Agent 都可以使用：

```bash
git clone https://github.com/isongxw/hf-paper-skill.git
cd hf-paper-skill
cp .env.example .env
# 编辑 .env 填入翻译 token
pip3 install python-dotenv
python3 scripts/generate_report.py --period weekly
```
