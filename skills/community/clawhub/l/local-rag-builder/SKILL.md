---
name: local-rag-builder
version: 1.1.3
description: 本地 RAG 系统搭建技能，支持环境检测修复、嵌入模型多源下载、5种切分策略 + GuardStack + 后处理 + 插件注册、多知识库管理 + 自动分类规则、可调 Prompt、Web 可视化配置 + 极客模式 + 模板管理
author: wUwproject
license: MIT
sensitive_access: true
critical_write: false
trigger: ['搭建 RAG 系统', '本地知识库', '嵌入模型下载', '文本切分', '向量检索', 'RAG 环境配置', '下载模型', '入库文档', '切分文档', '知识库管理']
trigger_negative: ['纯聊天', '简单问答']
tags: ['rag', 'embedding', 'llm', 'python', 'vector-db', 'text-splitter', 'guard-stack', 'plugin']
data_dir: skills/.standardization/local-rag-builder/data/
h1_position: true
external_data_dir: true
permission_weight: CRITICAL
faq_quality: improve_qa
meta_field_sync: true
data_dir_compliance: true
create_permissions_md: true
---
# local-rag-builder（本地 RAG 搭建工具）

一站式本地 RAG 系统搭建工具。支持环境自动检测修复、嵌入模型多源下载、5 种切分策略 + GuardStack 守卫栈 + 后处理子切 + 插件注册、多知识库管理与自动分类规则、可调 Prompt、Web 可视化配置。

**两种运行模式：**
- **🔌 集成模式（默认）** — 纯检索，不调用 LLM。智能体（xxxx 等）根据检索到的 context 自行回答。无需配置 LLM，无额外推理成本。
- **🤖 独立模式** — 检索 + LLM 全链路。`rag_standalone.py` 直接调用外部 LLM（LM Studio / Ollama / vLLM）完成回答，不经过智能体。用户自行选择平台和模型。

> **工作流说明（以下 xxxx 代指任意智能体）：**
>
> **集成模式：**
> 1. 你把文档/链接给 xxxx → xxxx 调用 `rag_skill.py` 向量化入库
> 2. 你提问 → xxxx 调用 `rag_skill.py --query "..."` 检索知识库
> 3. xxxx 根据检索到的 context 组织回答
>
> **独立模式：**
> 1. 你把文档/链接给 xxxx → xxxx 调用 `rag_standalone.py --import-file <path>` 入库
> 2. 你提问 → xxxx 调用 `rag_standalone.py --query "..."` 
> 3. `rag_standalone.py` 自行检索知识库 → 调用本地 LLM → 输出回答
> 4. xxxx 仅透传结果，不参与推理

## 触发条件

**正向触发：**
- **搭建 RAG** — "帮我搭一个本地 RAG 系统"
- **环境检测** — "检查我的 Python 环境能否跑 RAG"
- **下载模型** — "下载一个嵌入模型" / "换个模型源重试"
- **切分文档** — "对这个 Markdown 文件做层级切分"
- **向量检索** — "把这份资料入库，搜索相似内容"
- **知识库管理** — "创建一个知识库" / "把这类资料存入指定库"
- **调整参数** — "更新切分参数" / "改 Prompt 模板"
- **智能体集成** — "根据这份资料回答：xxx"（智能体调用 skill 的集成模式）

**否定条件：**
- **不触发**：纯 LLM 聊天不需要检索、简单问答不需要外部资料

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

| # | 能力 | 说明 |
| --- |------| ------ |
| 1 | **环境自动检测修复** | 检测 Python 版本（需 3.8-3.11）、缺失包，自动创建虚拟环境安装 |
| 2 | **嵌入模型管理** | 多源下载（ModelScope / HuggingFace 镜像 / 官方 / 直连），自动重试，完整性校验，路径修正 |
| 3 | **5 种切分策略 + GuardStack + 后处理** | 固定窗口、递归切、层级/标题切、按句切、语义切；守卫栈（mermaid/代码块/公式/表格/HTML 保护）；后处理子切（递归/固定/语义，metadata 白名单继承） |
| 4 | **多知识库管理** | 支持多个向量知识库并行，LLM 自动分类入库或用户指定 |
| 5 | **可调 Prompt** | 模板持久化，支持自定义占位符（`{context}` `{question}`），运行时编辑 |
| 6 | **Web 可视化界面** | 内嵌 HTML 配置面板：输入源开关、GuardStack 守卫配置、5 策略动态表单 + 后处理配置、极客模式 JSON 编辑器 + 配置模板管理、知识库自动分类规则编辑器 |
| 7 | **双模式接口** | 技能模式纯检索（`rag_skill.py`），智能体自行回答；独立模式（`rag_standalone.py`）检索 + LLM 全链路 |

### 渐进式文件索引

| 文件名 | 分类 | 包含内容 | 审计关联 |
| -------- |------| ---------- |----------|
| `references/antipatterns.md` | 规范指南 | skill 编写中的常见反模式。包含：错误做法示例、正确做法示例、避坑指引。 | R-18 |
| `references/architecture.md` | 架构设计 | local-rag-builder 整体架构。包含：模块关系、数据流、核心设计决策。 | 无 |
| `references/changelog.md` | 版本管理 | 版本更新日志。包含：版本号、更新类型、修复项、升级说明。 | R-24 |
| `references/examples.md` | 使用示例 | 各场景完整执行示例。包含：CLI 命令、执行过程、输出结果。 | R-25 C-17 |
| `references/faq.md` | 常见问题 | 常见疑问与解答。包含：问题分类、原因分析、解决方案。 | R-19, R-25 C-19 |
| `references/guide.md` | 使用指南 | 三种执行模式操作教程。包含：audit/create/refactor 流程、参数说明、注意事项。 | 无 |
| `references/llm-setup.md` | 参考文档 | > 本文件适用于 **独立模式**（`rag_standalone.py`）。技能模式（`rag_skill.py`）不需要 LLM。 | 无 |
| `references/permissions.md` | 权限与测试 | 权限扫描说明与测试结论。包含：风险等级、高权限操作说明、测试概览、计时统计。 | R-15, R-16 |
| `references/LICENSE.md` | 许可协议 | MIT 开源许可证声明。 | R-26 |
| `references/setup-spec.md` | 规范文档 | RAG 搭建完整参数规范（32 参数 + 6 阶段流水线）。 | 无 |
| `references/commands.md` | 命令参考 | 脚本命令速查表。包含：脚本名称、作用、核心参数。 | 无 |
| `references/data-directory.md` | 数据目录 | 运行时数据目录结构说明。包含：各子目录用途。 | 无 |
| `references/custom-extensions.md` | 扩展指南 | 插件注册指南与代码示例。包含：自定义切分策略、自定义守卫。 | 无 |
## 快速开始

```bash
# 1. 进入技能目录
cd ~/.workbuddy/skills/local-rag-builder

# 2. 运行环境检测（自动修复，建议首次用国内镜像）
python scripts/rag_env_setup.py --auto-install --mirror aliyun      # 国内用户推荐
# python scripts/rag_env_setup.py --auto-install                    # 海外用户/默认
# python scripts/rag_env_setup.py --check-only                      # 仅检测不安装
# python scripts/rag_env_setup.py --cleanup-locks                   # 清理 pip 锁文件

# 3. 下载嵌入模型（交互式选择）
python scripts/embedding_model_manager.py --interactive

# 4. 启动 Web 配置界面
python scripts/rag_web_ui.py

# 5a. [技能模式] 纯检索，供智能体调用（无需 LLM）
python scripts/rag_skill.py --query "问题"
python scripts/rag_skill.py --query "问题" --json          # JSON 输出

# 5b. [独立模式] 检索 + LLM 全链路，需外部 LLM 服务
python scripts/rag_standalone.py                            # 交互式 CLI
python scripts/rag_standalone.py --query "问题"              # 单次问答
python scripts/rag_standalone.py --query "问题" --json       # JSON 输出
python scripts/rag_standalone.py --llm-help                  # 查看 LLM 接入指南
```

## 工作流程

1. **环境准备** — `rag_env_setup.py` 检测并安装依赖
   - 输入：当前 Python 环境 + 系统包管理器
   - 输出：完整的依赖环境（chromadb / sentence-transformers / langchain 等）
2. **模型下载** — `embedding_model_manager.py` 下载/校验嵌入模型
   - 输入：模型名称（如 BAAI/bge-small-zh-v1.5）
   - 输出：本地缓存的嵌入模型（支持 ModelScope / HuggingFace 镜像多源重试）
3. **文档入库** — `text_splitter.py` 切分文档 → `knowledge_base_manager.py` 向量化
   - 输入：原始文档（txt / md / py / json / yaml）
   - 输出：向量化存储到指定知识库（Chroma DB）
4. **模式选择** — 根据用途选择入口
   - **技能模式** → `rag_skill.py`（纯检索，供智能体调用，无需 LLM）
   - **独立模式** → `rag_standalone.py`（检索 + LLM 全链路，需外部 LLM）
5. **配置调整** — `rag_web_ui.py` 提供可视化面板

→ 详见 references/commands.md（命令速查表）

→ 详见 references/data-directory.md（数据目录结构说明）

→ 详见 references/custom-extensions.md（插件注册指南）

## 约束

1. **Python 版本**：建议 3.8-3.11（3.12+ 需测试 chromadb 兼容性）
2. **嵌入模型路径**：下载后自动修正真实路径（如 `bge-small-zh-v1___5`）
3. **知识库隔离**：不同资料自动/手动归入不同库
4. **重置**：删除 `data/` 下对应子目录即可重置相关数据

## 限制

- **文件类型支持**：仅支持纯文本格式（txt / md / py / json / yaml），不支持 PDF、图片 OCR 或音视频转录 — 影响：数据来源受限 ✅ 已接受
- **知识库容量**：单个知识库建议 5 万条以内，超过需考虑分段策略优化 — 影响：大规模部署需规划 🟡 有替代方案（分段入库）
- **模型范围**：仅支持 sentence-transformers/HuggingFace 格式的嵌入模型，不直接支持 OpenAI/Cohere API 格式 — 影响：API 方式无法直接对接 ✅ 已接受
- **LLM 依赖**：独立模式需要外部 LLM 服务（LM Studio / Ollama / vLLM），技能模式不需要 — 影响：独立模式有额外部署成本 ✅ 已说明
- **并发限制**：单进程运行，不支持多用户并发写入知识库 — 影响：不适合高并发生产环境 🟡 规划中
- **切分参数范围**：`chunk_size` 50–5000（默认 500），`chunk_overlap` 0–1000（默认 50）；超出范围自动钳位 — 影响：极端参数影响检索精度 ✅ 已处理

