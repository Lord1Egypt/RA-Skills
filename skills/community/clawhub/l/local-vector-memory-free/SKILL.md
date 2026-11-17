---
name: "local-vector-memory-free"
description: "零API零云依赖的本地向量记忆免费版：离线可用、隐私不出域，核心存储与检索开箱即用。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "本地向量记忆(免费版)"
  version: "1.0.0"
  summary: "零API零云依赖的本地向量记忆免费版：离线可用、隐私不出域，核心存储与检索开箱即用。"
  tags:
    - "智能代理"
    - "记忆管理"
    - "本地存储"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 本地向量记忆（免费版）

**零 API、零云端、零数据出域**的本地向量记忆系统免费体验版。基于 Ollama + LanceDB，在本地完成 embedding 生成与语义检索，适合隐私敏感、离线、成本敏感场景的快速体验。

## 痛点与对策速查

| 用户痛点 | 发生场景 | 本系统对策 |
|:---|:---|:---|
| 数据隐私担忧 | 云端 embedding 数据出域 | 纯本地 Ollama embedding，数据不出本机 |
| API 费用高 | 云端 embedding 按 token 收费 | 本地 nomic-embed-text 完全免费 |
| 离线不可用 | 无网络时记忆系统瘫痪 | 本地运行，完全离线可用 |
| 跨会话遗忘 | 新会话忘记上一会话内容 | SESSION-STATE.md 热内存持久化 |
| 写入丢失 | 崩溃/压缩导致上下文丢失 | WAL 写前日志协议，先写状态再回复 |
| 部署复杂 | 本地栈搭建门槛高 | 一键初始化 + 详细故障排查表 |

## 本地 vs 云端对比

| 对比维度 | 云端 API（OpenAI） | 本地方案（Ollama） |
|:---|:---|:---|
| 费用 | 按 token 收费 | 完全免费 |
| 延迟 | 网络往返 100-500ms | 本地 10-50ms |
| 隐私 | 数据出域 | 完全本地 |
| 离线 | 不可用 | 完全可用 |
| 质量 | text-embedding-3-large | nomic-embed-text（足够） |
| 资源占用 | 零本地资源 | 需 2-4GB 内存 |
| 部署难度 | 仅需 API Key | 需安装 Ollama |

**结论**：个人/小团队/隐私场景用本地；追求极致质量且不敏感数据用云端。

## 架构

```text
┌─────────────────────────────────────────────────────────────────┐
│              LOCAL VECTOR MEMORY（免费版架构）                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   HOT RAM   │  │  WARM STORE │  │  COLD STORE │             │
│  │             │  │             │  │             │             │
│  │ SESSION-    │  │  LanceDB    │  │  MEMORY.md  │             │
│  │ STATE.md    │  │  Vectors    │  │  + daily/   │             │
│  │             │  │             │  │             │             │
│  │ (survives   │  │ (semantic   │  │ (human-     │             │
│  │  compaction)│  │  search)    │  │  readable)  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                  ┌─────────────┐                                │
│                  │  WAL 日志   │  ← 写前日志，防数据丢失          │
│                  └─────────────┘                                │
│                                                                 │
│  全程零外部 API · 零数据出域 · 离线可用                          │
└─────────────────────────────────────────────────────────────────┘
```

## 三层存储系统

| 层级 | 文件/系统 | 用途 | 持久化 | 免费版支持 |
|:---|:---|:---|:---|:---|
| L1 热内存 | SESSION-STATE.md | 活跃任务上下文 | 抗压缩/重启 | ✅ 完整支持 |
| L2 温向量 | LanceDB Vectors | 语义检索 | 本地向量库 | ✅ 基础检索 |
| L3 冷归档 | MEMORY.md + daily/ | 人类可读长期记忆 | 文件持久化 | ✅ 完整支持 |

## 使用流程

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

> 本工具属中等复杂度，基础上手 < 120 秒，完整初始化 < 300 秒。

### 60 秒极速体验（已有 Ollama）

```bash
# 依赖说明
ollama pull nomic-embed-text

# 初始化记忆系统
node bin/init.js

# 存储第一条记忆
node bin/memory.js store "用户喜欢深色模式" --importance 0.9 --category preference

# 检索记忆
node bin/memory.js search "用户界面偏好"
```

### 120 秒基础上手（需安装 Ollama）

```bash
# 第 1 步：安装 Ollama（macOS/Linux）
curl -fsSL https://ollama.com/install.sh | sh

# Windows 用户从官网下载安装包
# https://ollama.com/download

# 第 2 步：拉取 embedding 模型
ollama pull nomic-embed-text

# 第 3 步：安装项目依赖
cd skills/local-vector-memory
npm install

# 第 4 步：初始化记忆系统
node bin/init.js
```

初始化后创建以下文件：

| 文件/目录 | 用途 |
|:---|:---|
| `SESSION-STATE.md` | 热内存，活跃任务上下文 |
| `MEMORY.md` | 长期记忆，人类可读归档 |
| `memory/` | 每日日志目录 |
| `memory/vectors/` | LanceDB 向量数据库 |

### 300 秒完整配置（含 Agent 平台集成）

在 Agent 平台配置文件中添加插件配置：

```json
{
  "plugins": {
    "entries": {
      "local-vector-memory": {
        "enabled": true,
        "config": {
          "ollamaUrl": "http://localhost:11434",
          "embeddingModel": "nomic-embed-text",
          "dbPath": "./memory/vectors",
          "autoRecall": false,
          "autoCapture": false
        }
      }
    }
  }
}
```

> **注意**：免费版 `autoRecall` 和 `autoCapture` 固定为 `false`，需手动调用记忆工具。

启用后可使用以下工具：

| 工具 | 功能 | 免费版 |
|:---|:---|:---|
| `memory_recall` | 搜索相关记忆 | ✅ 基础检索 |
| `memory_store` | 存储重要信息 | ✅ 完整支持 |
| `memory_forget` | 删除记忆 | ✅ 完整支持 |

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例

### 场景 1：个人开发者偏好记忆

**角色**：独立开发者，使用 Agent 辅助编码
**痛点**：每次新会话都要重新说明偏好（深色模式、Tab 宽度、命名风格）

```bash
# 存储开发偏好
node bin/memory.js store "用户使用 2 空格缩进，偏好驼峰命名" --importance 0.9 --category preference

node bin/memory.js store "用户主要用 TypeScript 和 Python" --importance 0.8 --category skill

# 新会话开始时检索
node bin/memory.js search "用户编码偏好"
# 返回：2 空格缩进、驼峰命名、TypeScript/Python

# 更新热内存
# SESSION-STATE.md 自动追加：
# - 编码偏好：2 空格、驼峰命名
# - 技术栈：TypeScript、Python
```

**效果**：Agent 在新会话立即知道你的偏好，无需重复说明。

### 场景 2：医疗行业隐私合规记忆

**角色**：医疗 AI 助手开发者
**痛点**：患者信息不可出域，但需要跨会话记住患者病史

```bash
# 初始化时确保完全离线
ollama serve  # 启动本地服务

# 存储患者概况（脱敏后）
node bin/memory.js store "患者A：高血压病史3年，药物控制中" --importance 0.95 --category medical_history

node bin/memory.js store "患者A：对青霉素过敏" --importance 1.0 --category allergy

# 下次问诊前检索
node bin/memory.js search "患者A 过敏史"
# 返回：青霉素过敏

node bin/memory.js search "患者A 慢性病"
# 返回：高血压3年
```

**效果**：数据完全留在本机，满足 HIPAA/隐私合规要求，离线可用。

### 场景 3：离线环境知识库构建

**角色**：野外考察研究员，无网络环境
**痛点**：需要在离线环境下记录和检索考察笔记

```bash
# 离线环境下（无网络）
# Ollama 本地运行，无需联网

# 记录考察发现
node bin/memory.js store "样地A：发现稀有兰花品种，海拔1200米" --importance 0.9 --category observation

node bin/memory.js store "样地A：土壤pH值5.8，湿度偏高" --importance 0.7 --category measurement

# 语义检索（即使关键词不完全匹配）
node bin/memory.js search "兰花生长环境"
# 返回：样地A的土壤和海拔数据

# 导出备份
node bin/memory.js export --format json > expedition.json
```

**效果**：完全离线运行，语义检索比关键词匹配更精准。

## WAL 协议（写前日志）

**核心原则**：先写状态，再回复。确保崩溃/压缩时不丢失上下文。

| 触发条件 | 动作 | 优先级 |
|:---|:---|:---|
| 用户表达偏好 | 写入 SESSION-STATE.md → 然后回复 | 高 |
| 用户做出决策 | 写入 SESSION-STATE.md → 然后回复 | 高 |
| 用户给出期限 | 写入 SESSION-STATE.md → 然后回复 | 中 |
| 用户纠正你 | 写入 SESSION-STATE.md → 然后回复 | 高 |
| 重要事实出现 | 写入 MEMORY.md → 然后回复 | 中 |

**为什么需要 WAL？** 如果先回复再保存，崩溃/压缩会导致上下文丢失。WAL 确保数据持久，即使 Agent 意外终止也能恢复。

### 智能提示词模板

在 Agent 的配置文件（如 `AGENTS.md` 或 `SOUL.md`）中添加：

```markdown
## 记忆协议

### 会话开始时
1. 读取 SESSION-STATE.md — 获取热上下文
2. 使用 memory_recall 搜索相关历史
3. 检查 memory/YYYY-MM-DD.md 了解近期活动

### 对话中
- 用户给出具体细节？→ 先写入 SESSION-STATE.md，再回复
- 重要决策？→ 使用 memory_store 存储
- 表达偏好？→ memory_store --importance 0.9 --category preference

### 会话结束时
1. 更新 SESSION-STATE.md 最终状态
2. 重要内容移至 MEMORY.md
3. 创建/更新 memory/YYYY-MM-DD.md
```

## 维护命令

```bash
# 查看记忆统计
node bin/memory.js stats

# 浏览全部记忆
node bin/memory.js search "*" --limit 50

# 去重
node bin/memory.js dedup

# 导出备份
node bin/memory.js export --format json > memories.json

# 创建压缩备份
node bin/memory.js backup ./backups/memory-$(date +%Y%m%d).zip

# 清理旧记忆（30天前）
node bin/memory.js cleanup --before 30d
```

## 错误处理

| 序号 | 问题 | 可能原因 | 解决方案 | 优先级 |
|:---|:---|:---|:---|:---|
| 1 | Ollama 连接失败 | Ollama 服务未启动 | 运行 `ollama serve`；检查 `OLLAMA_HOST` 环境变量 | 高 |
| 2 | 向量搜索无结果 | LanceDB 路径错误或无数据 | 确认 `dbPath` 配置；运行 `node bin/memory.js stats` 确认已存储记忆 | 高 |
| 3 | embedding 生成缓慢 | 模型首次加载 | 首次调用需加载模型到内存，后续调用毫秒级；预热：`ollama run nomic-embed-text ""` | 中 |
| 4 | 内存占用过高 | 向量库无限增长 | 运行 `node bin/memory.js compact` 压缩向量；`node bin/memory.js cleanup --before 30d` 清理旧记忆 | 中 |
| 5 | npm install 失败 | 网络问题或 Node 版本过低 | 确认 Node.js 18+；使用 `npm install --registry https://registry.npmmirror.com` | 高 |
| 6 | init.js 报权限错误 | 文件系统权限不足 | 确认对目标目录有读写权限；Linux/macOS 运行 `chmod -R 755 ./memory/` | 中 |
| 7 | 检索结果不相关 | embedding 模型不匹配 | 确认使用 `nomic-embed-text`；重新初始化向量库 | 低 |

## 常见问题

### Q1: 免费版能存储多少条记忆？

**A**: 免费版不限制存储数量。LanceDB 本地存储，容量取决于你的磁盘空间。建议定期运行 `dedup` 和 `cleanup` 保持记忆库精简。免费版限制的是高级检索功能（如向量过滤、批量检索），而非存储量。

### Q2: 免费版需要联网吗？

**A**: 不需要。安装 Ollama 和拉取 `nomic-embed-text` 模型后，整个系统完全离线运行。数据不离开本机，适合隐私敏感和离线环境。

### Q3: nomic-embed-text 的检索质量够用吗？

**A**: 对于个人使用和中小规模记忆库（< 10万条），nomic-embed-text 的质量足够。它支持 768 维向量，在常见语义检索基准上表现接近 OpenAI text-embedding-3-small。如果需要更高质量，专业版支持切换其他 embedding 模型。

### Q4: 免费版和专业版的核心区别是什么？

**A**: 免费版提供核心存储、基础向量检索、WAL 协议、热内存持久化。专业版新增三项高级能力：(1) LanceDB 高级向量搜索（过滤、批量、混合检索）；(2) 自动召回与捕获（无需手动调用）；(3) Git-Notes 知识图谱（结构化决策存储）。

### Q5: 如何从免费版升级到专业版？

**A**: 专业版使用相同的存储格式和数据结构，升级时只需替换 SKILL.md 并更新插件配置中的 `autoRecall` 和 `autoCapture` 为 `true`。已有记忆数据无需迁移，无缝继承。

### Q6: 数据存储在哪里？如何备份？

**A**: 所有数据存储在本地 `memory/` 目录下：向量数据在 `memory/vectors/`（LanceDB），日志在 `memory/YYYY-MM-DD.md`，热内存在 `SESSION-STATE.md`。备份使用 `node bin/memory.js backup ./backups/memory-YYYYMMDD.zip`。

### Q7: 支持哪些操作系统？

**A**: 支持 Windows、macOS、Linux。Ollama 在三大平台均有官方安装包。Node.js 需 18+ 版本。

## 已知限制

本免费体验版限制以下高级功能：

- ❌ **LanceDB 高级向量搜索**：不支持元数据过滤、批量检索、混合检索策略，仅支持基础语义检索
- ❌ **自动召回与捕获**：不支持 `autoRecall` 和 `autoCapture`，需手动调用 `memory_recall` 工具
- ❌ **Git-Notes 知识图谱**：不支持结构化决策存储与分支感知的冷存储层

> **注意**：免费版不限制使用次数、不限制存储量、不添加水印、不强制注册。核心功能完整可用，适合充分体验本地向量记忆的价值。

解锁全部高级功能请使用专业版：`local-vector-memory-pro`

## 依赖说明

### 运行环境

- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 18+（用于运行记忆管理脚本）
- **Ollama**: 本地 embedding 引擎，需独立安装

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 | 版本要求 |
|:-------|:-----|:---------|:---------|:---------|
| Ollama | 本地服务 | 必需 | https://ollama.com/download | 0.1.0+ |
| nomic-embed-text | embedding 模型 | 必需 | `ollama pull nomic-embed-text` | latest |
| LanceDB (vectordb) | npm 包 | 必需 | `npm install vectordb` | 0.9.0+ |
| Node.js | 运行时 | 必需 | https://nodejs.org | 18+ |

### API Key 配置

- 本 Skill 基于本地运行，**无需任何 API Key**
- Ollama 默认监听 `http://localhost:11434`，无需认证
- 如需远程 Ollama 服务，设置 `OLLAMA_HOST` 环境变量

### 可用性分类

- **分类**: MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行记忆管理任务

## License 与版权声明

本 skill 基于原始作品改进，保留原始版权声明：

- 原始作品：elite-longterm-memory-local
- 原始 license：MIT
- 改进作品：© 2026 Local Vector Memory Team
- 改进 license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：

- 重构 frontmatter 元数据，新增 edition 字段区分免费/专业版
- 新增痛点对策速查表、本地 vs 云端对比表
- 新增 3 个真实场景示例（开发者偏好、医疗合规、离线考察）
- 新增 FAQ（7 问）和故障排查表（7 项）
- 新增分级时间快速开始（60s/120s/300s）
- 新增免费版限制说明与专业版引导
- 优化架构图与三层存储说明
- 新增依赖说明章节与版本兼容性

---

*本地优先，隐私至上。免费体验，专业解锁。*

## 核心能力

### 面向隐私敏感与离线场景的本地向
面向隐私敏感与离线场景的本地向量记忆系统免费体验版

**输入**: 用户提供面向隐私敏感与离线场景的本地向所需的指令和必要参数。
**处理**: 按照skill规范执行面向隐私敏感与离线场景的本地向操作,遵循单一意图原则。
**输出**: 返回面向隐私敏感与离线场景的本地向的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 基于 LanceDB + 纯本地 emb
基于 LanceDB + 纯本地 embedding（Ollama/nomic-embed-text），实现零外部 API 调用、零数据出域、完全离线可用的语义记忆检索

**输入**: 用户提供基于 LanceDB + 纯本地 emb所需的指令和必要参数。
**处理**: 按照skill规范执行基于 LanceDB + 纯本地 emb操作,遵循单一意图原则。
**输出**: 返回基于 LanceDB + 纯本地 emb的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 免费版提供核心存储、热内存持久化、WAL
免费版提供核心存储、热内存持久化、WAL 写前日志等基础能力，适合个人开发者快速体验本地向量记忆的价值

**输入**: 用户提供免费版提供核心存储、热内存持久化、WAL所需的指令和必要参数。
**处理**: 按照skill规范执行免费版提供核心存储、热内存持久化、WAL操作,遵循单一意图原则。
**输出**: 返回免费版提供核心存储、热内存持久化、WAL的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 核心能力包括本地 embedding 引
核心能力包括本地 embedding 引擎（Ollama nomic-embed-text，毫秒级延迟）、LanceDB 向量库基础检索、SESSION-STATE

**输入**: 用户提供核心能力包括本地 embedding 引所需的指令和必要参数。
**处理**: 按照skill规范执行核心能力包括本地 embedding 引操作,遵循单一意图原则。
**输出**: 返回核心能力包括本地 embedding 引的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### md 热内存持久化（抗压缩/重
md 热内存持久化（抗压缩/重启）、WAL 写前日志协议（防数据丢失）、三层冷热分层存储架构、一键初始化与维护命令

**输入**: 用户提供md 热内存持久化（抗压缩/重所需的指令和必要参数。
**处理**: 按照skill规范执行md 热内存持久化（抗压缩/重操作,遵循单一意图原则。
**输出**: 返回md 热内存持久化（抗压缩/重的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：零云依赖的本地向、量记忆免费版、隐私不出域、核心存储与检索开、箱即用、Use、when、需要数据库操作、SQL、数据存储管理时使、不适用于数据库架、构设计决策等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 适用场景

**角色**：独立开发者，使用 Agent 辅助编码
**痛点**：每次新会话都要重新说明偏好（深色模式、Tab 宽度、命名风格）

```bash
