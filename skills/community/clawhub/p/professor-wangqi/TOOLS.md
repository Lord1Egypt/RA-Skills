# 工具参考 (TOOLS.md)

> 本文档包含所有 CLI 命令的详细说明。日常使用时，SKILL.md 会自动引导你使用这些命令。

---

## 快速开始

```bash
# 1. 初始化（在项目目录下）
wangqi-skill init

# 2. 配置 LLM API
wangqi-skill config --api-key sk-xxx --base-url http://localhost:1234/v1

# 3. 构建向量索引
wangqi-skill build-index

# 4. 开始问答
wangqi-skill ask "痰湿质与肥胖有什么关系？"
```

---

## 命令总览

| 命令 | 用途 | 场景 |
|------|------|------|
| `init` | 初始化用户目录 | 首次使用 |
| `config` | 配置 API | 设置 LLM |
| `ask` | 学术问答 | 查询知识 |
| `interactive` | 交互模式 | 连续问答 |
| `retrieve` | 纯检索 | 外部 LLM 调用 |
| `add-pdf` | 添加 PDF | 知识库维护 |
| `extract` | 批量提取 | 知识库维护 |
| `build-index` | 构建索引 | 知识库维护 |
| `validate` | 验证质量 | 质量检查 |
| `install-skill` | 安装到 Claude Code | 集成 |
| `uninstall` | 从 Claude Code 移除 | 清理 |
| `version` | 显示版本 | 信息查询 |

---

## 学术问答

### ask - 单次问答

```bash
wangqi-skill ask "你的问题"
```

**示例：**
```bash
wangqi-skill ask "痰湿质与肥胖有什么关系？"
wangqi-skill ask "王琦教授如何治疗气虚质失眠？"
```

### interactive - 交互模式

```bash
wangqi-skill interactive
```

进入连续问答模式，输入 `quit` 或 `exit` 退出。

### retrieve - 纯检索（供外部 LLM 调用）

```bash
wangqi-skill retrieve "查询词" --format context --n-results 5
```

**参数：**
- `--format`：输出格式（`context` / `json`）
- `--n-results`：返回结果数量（默认 5）

**输出格式：**
```
[论文] 《文献标题》 (年份)
文献内容...

---

[诊疗经验] 《文献标题》
文献内容...
```

---

## 知识库维护

### add-pdf - 智能添加 PDF

```bash
wangqi-skill add-pdf --pdf path/to/paper.pdf --type paper
```

**参数：**
- `--pdf`：PDF 文件路径（必填）
- `--type`：文档类型（`paper` / `experience`，默认 `paper`）
- `--no-index`：不添加到向量索引

**示例：**
```bash
# 添加 SCI 论文
wangqi-skill add-pdf --pdf ./paper.pdf --type paper

# 添加诊疗经验
wangqi-skill add-pdf --pdf ./experience.pdf --type experience

# 只提取，不入库
wangqi-skill add-pdf --pdf ./paper.pdf --no-index
```

### extract - 批量提取

```bash
wangqi-skill extract --input data/pdfs/ --type paper
```

**参数：**
- `--input`：PDF 目录
- `--output`：输出目录（可选）
- `--type`：文档类型

### build-index - 构建向量索引

```bash
wangqi-skill build-index
```

从知识卡构建 ChromaDB 向量索引。首次使用或添加新知识卡后需要运行。

### validate - 验证知识卡质量

```bash
wangqi-skill validate
```

检查知识卡质量，输出质量报告。

---

## 配置管理

### config - 配置 API

```bash
# 显示当前配置
wangqi-skill config

# 配置 chat 模型
wangqi-skill config --api-key sk-xxx --base-url http://localhost:1234/v1

# 配置 embedding 模型（如果与 chat 模型不同）
wangqi-skill config --embedding-model nomic-embed-text --embedding-base-url http://localhost:1234/v1

# 配置 embedding 维度
wangqi-skill config --embedding-dimensions 768
```

**所有配置选项：**

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--api-key` | LLM API 密钥 | - |
| `--base-url` | LLM API 地址 | - |
| `--model` | Chat 模型名称 | `qwen/qwen3.6-35b-a3b` |
| `--embedding-model` | Embedding 模型名称 | `text-embedding-nomic-embed-text-v1.5` |
| `--embedding-base-url` | Embedding API 地址 | 同 `--base-url` |
| `--embedding-api-key` | Embedding API 密钥 | 同 `--api-key` |
| `--embedding-dimensions` | Embedding 维度 | `768` |

---

## Claude Code 集成

### 即时模式（零配置 - 推荐）

最简单的安装方式：直接复制 SKILL.md 到 Claude Code skills 目录。无需 Python、ChromaDB 或 LLM 配置。

```bash
# Linux/macOS
mkdir -p ~/.claude/skills/professor-wangqi
cp SKILL.md ~/.claude/skills/professor-wangqi/
# 重启 Claude Code

# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills\professor-wangqi"
Copy-Item SKILL.md "$env:USERPROFILE\.claude\skills\professor-wangqi\"
# 重启 Claude Code
```

AI 通过 SKILL.md 内嵌的关键词索引、诊断公式和常见问题速查直接回答基础问题。

### install-skill - npm 方式安装到 Claude Code（完整模式）

```bash
wangqi-skill install-skill
```

将 skill 安装到 `~/.claude/skills/professor-wangqi/`，Claude Code 会自动识别。需要已配置 npm 包 + LLM + ChromaDB。

**安装后重启 Claude Code 生效。**

### uninstall - 从 Claude Code 移除

```bash
wangqi-skill uninstall
```

---

## 多平台分发

### 发布到 ClawHub

ClawHub 是国际公共 Skill 注册中心（[clawhub.ai](https://clawhub.ai)），发布后用户可通过 `openclaw skills install` 安装。

**前置条件**：SKILL.md frontmatter 需包含 `name`、`description`、`version`、`tags` 字段（当前版本已满足）。

```bash
# 1. 安装 CLI 并登录
npm i -g clawhub
clawhub login

# 2. 预览发布（--dry-run，不实际上传）
clawhub skill publish ./professor-wangqi \
  --slug professor-wangqi \
  --name "王琦中医体质学术助手" \
  --version 1.3.0 \
  --changelog "v1.3.0 更新说明" \
  --tags latest,tcm \
  --dry-run

# 3. 正式发布
clawhub skill publish ./professor-wangqi \
  --slug professor-wangqi \
  --name "王琦中医体质学术助手" \
  --version 1.3.0 \
  --changelog "v1.3.0 更新说明" \
  --tags latest,tcm

# 4. 后续版本更新（自动检测变更并升级 patch 版本）
clawhub skill publish ./professor-wangqi --changelog "新增 X 功能"
```

**用户安装方式**：
```bash
openclaw skills install professor-wangqi
# 或
clawhub install professor-wangqi
```

### 发布到 SkillHub（腾讯云）

SkillHub 是面向中国用户的 AI Skill 社区（[skillhub.cn](https://skillhub.cn)），需实名认证后发布。

**前置条件**：
1. SKILL.md frontmatter 需包含 `slug`、`displayName`、`summary` 字段（当前版本已满足）
2. 在 skillhub.cn 完成实名认证
3. 在个人中心获取 API key

```bash
# 1. 安装 CLI
curl -fsSL https://skillhub.cn/install/install.sh | bash -s -- --no-skills

# 2. 登录
skillhub login --key "$SKILLHUB_KEY" --host https://api.skillhub.cn

# 3. 推送文件（草稿状态）
skillhub push

# 4. 发布上线（提交审核）
skillhub publish --changelog "v1.3.0 更新：关键词索引、诊断公式、失败预防协议"

# 或一步到位
skillhub publish ./professor-wangqi --host https://api.skillhub.cn --changelog "首次发布"
```

**用户安装方式**：
```bash
skillhub search 王琦
skillhub install professor-wangqi
```

### 发布到 OpenClawMP（水产市场）

OpenClawMP 是更广泛的 AI Agent 资产市场（[openclawmp.cc](https://openclawmp.cc)），支持 skill / plugin / trigger 等多种类型。

**前置条件**：
1. 在 `professor-wangqi/` 目录下创建 `.metadata.json` 文件
2. 获取 API key 或通过 OAuth 认证

**.metadata.json 模板**：
```json
{
    "assetType": "skill",
    "name": "wangqi-tcm-constitution",
    "displayName": "王琦中医体质学术助手",
    "semver": "1.3.0",
    "category": "学术研究",
    "tags": ["中医", "体质学说", "王琦", "九种体质", "辨体论治"],
    "description": "基于王琦教授学术论文与诊疗经验，提供九种体质辨识、辨体论治思路学习、知识库维护和数据分析功能。",
    "longDescription": "支持九种体质完整诊断公式、辨体论治决策树、常见问题速查、失败预防三级协议。内嵌关键词索引，支持即时模式（零配置）和完整模式（RAG检索）两种用法。"
}
```

**发布命令**：
```bash
# 1. 安装 CLI
npm i -g openclawmp

# 2. 认证（API key 方式）
openclawmp oauth <your-token>

# 3. 预览
openclawmp publish ./professor-wangqi --dry-run

# 4. 正式发布
openclawmp publish ./professor-wangqi --yes

# 首次发布后会自动生成 .assetid 文件，后续更新时自动读取
```

**用户安装方式**：
```bash
openclawmp search "王琦"
openclawmp install skill/@owner/wangqi-tcm-constitution
```

### 各平台对比

| 特性 | npm | ClawHub | SkillHub | OpenClawMP |
|------|-----|---------|----------|------------|
| **目标用户** | 开发者 | 国际用户 | 中国用户 | 国际用户 |
| **安装方式** | `npm install` | `clawhub install` | `skillhub install` | `openclawmp install` |
| **发布方式** | `npm publish` | `clawhub skill publish` | `skillhub publish` | `openclawmp publish` |
| **审核机制** | 无 | 自动检测 | 三线并行安全审核 | 不明确 |
| **认证要求** | npm 账号 | GitHub OAuth | 实名认证 + API key | API key / OAuth |
| **额外文件** | `package.json` | 无（SKILL.md 即可） | 无（SKILL.md 即可） | `.metadata.json` |
| **付费支持** | 不支持 | 不支持 | 不支持 | 不支持 |

---

## 数据位置

所有用户数据存储在当前目录的 `.wangqi-skill/` 下：

```
./.wangqi-skill/
├── .env           # 配置文件
├── data/          # 用户数据
│   └── cards/     # 用户知识卡
└── chroma_db/     # 向量索引
```

---

## 环境变量

配置保存在 `.wangqi-skill/.env`：

```env
# Chat 模型配置
API_KEY=sk-your-api-key
BASE_URL=http://localhost:1234/v1
MODEL_NAME=qwen/qwen3.6-35b-a3b

# Embedding 模型配置
EMBEDDING_MODEL=text-embedding-nomic-embed-text-v1.5
EMBEDDING_BASE_URL=http://localhost:1234/v1
EMBEDDING_API_KEY=sk-your-api-key
EMBEDDING_DIMENSIONS=768
```

---

## 支持的 LLM 服务

- **LM Studio**（本地，推荐）
- OpenAI
- Azure OpenAI
- 其他 OpenAI 兼容 API

---

## 常见问题

### Q: 构建索引时报 "Embedding service failed"

检查：
1. Embedding 服务是否运行？
2. `EMBEDDING_BASE_URL` 是否正确？
3. 模型名称是否正确？

### Q: 问答返回空结果

检查：
1. 是否运行了 `build-index`？
2. `.wangqi-skill/chroma_db/` 目录是否存在？

### Q: 如何更新知识库？

```bash
# 1. 添加新 PDF
wangqi-skill add-pdf --pdf new.pdf --type paper

# 2. 重建索引（会自动增量更新）
wangqi-skill build-index
```
