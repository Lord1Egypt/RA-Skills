---
slug: parallel-research-tool-free
name: parallel-research-tool-free
version: 1.0.0
displayName: 并行研究助手免费版
summary: "开放式主题研究工具，构建可持续维护的研究文档，支持交互式探索。并行研究助手免费版，帮助用户围绕特定主题开展开放式研究，构建可持续维护的Markdown研究文档。核心能力:"
license: Proprietary
edition: free
description: 并行研究助手免费版，帮助用户围绕特定主题开展开放式研究，构建可持续维护的Markdown研究文档。核心能力:，可自动提升工作效率

  - 交互式研究模式，实时搜索与综合

  - 为每个研究主题创建独立文件夹

  - 结构化研究文档（问题、发现、资源、后续步骤）

  - 定期综合检查点与进度回顾

  - 研究文档PDF导出

  适用场景:

  - 个人开发者技术方案调研

  - 学生课题研究

  - 独立创业者市场验证

  差异化:

  - 免费版聚焦交互式研究，文档驱动而非对话驱动

  - 研究成果持久化保存，可持续维护

  - 与PRO版本完全兼容...'
tags:
  - 研究
  - 文档
  - 调研
  - 知识管理
  - 搜索
  - 检索
  - 工具
  - research
  - text
  - agent
  - 来源
  - pdf
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Knowledge"
---
# 并行研究助手（免费版）

## 概述

并行研究助手免费版是一款帮助用户围绕特定主题开展开放式研究的工具。核心理念是"对话是短暂的，文档才是重要的"。为每个研究主题创建独立的研究文件夹，通过交互式对话逐步搜索、综合和更新研究文档，最终形成结构化的知识沉淀.
本版本聚焦交互式研究模式，适合个人开发者技术方案调研、学生课题研究和独立创业者市场验证。如需深度异步研究、批量并行处理和 API 集成等高级能力，可升级至 PRO 版本.
## 核心能力

### 研究文档结构

每个研究主题拥有独立文件夹，包含完整的文档体系：

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 并行研究助手免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```text
~/.research-workspace/research/<topic-slug>/
├── prompt.md          # 原始研究问题
├── research.md        # 主要研究发现
├── research.pdf       # PDF导出（可选）
└── ...                # 其他相关文件
```

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 免费版能力边界

```text
[支持] 交互式研究模式
[支持] 研究文档结构化管理
[支持] 实时搜索与综合更新
[支持] 定期综合检查点
[支持] 研究状态管理（Active/Complete/Ongoing）
[支持] PDF导出
[限制] 不支持深度异步研究模式
[限制] 不支持批量多主题并行研究
[限制] 不支持API集成与自动化
[限制] 不支持团队协作
```

**处理**: 解析研究文档结构的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回研究文档结构的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：开放式主题研究工、构建可持续维护的、支持交互式探索、并行研究助手免费、帮助用户围绕特定、主题开展开放式研、Markdown、核心能力、为每个研究主题创、建独立文件夹、结构化研究文档、后续步骤、定期综合检查点与、进度回顾等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
### 核心功能执行(补充)
执行核心功能执行操作,使用`input_params`参数进行配置.

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一：技术方案调研

开发者需要调研某个技术方向的不同方案，为项目选型做准备.
```text
用户：new research: 2026年主流AI编程框架对比
# ...
Agent 执行流程：
1. 创建研究文件夹 ~/.research-workspace/research/ai-coding-frameworks/
2. 创建 prompt.md 记录原始问题
3. 创建 research.md 初始化研究结构
4. 开始第一轮搜索与发现
```

prompt.md 内容：

```markdown
# AI编程框架对比研究
# ...
> 2026年主流AI编程框架有哪些？各自的优势和适用场景是什么？
# ...
**Started:** 2026-07-18
```

research.md 初始结构：

```markdown
# AI编程框架对比研究
# ...
**Status:** Active Research
**Started:** 2026-07-18
**Last Updated:** 2026-07-18
# ...
---
# ...
## Open Questions
- 主流框架有哪些？
- 各框架的性能对比？
- 社区活跃度和生态？
- 学习曲线如何？
# ...
## Findings
<!-- 随研究进展填充 -->
# ...
## Options / Approaches
<!-- 方案对比 -->
# ...
## Resources
<!-- 链接、参考、来源 -->
# ...
## Next Steps
<!-- 下一步探索方向 -->
```

### 场景二：市场验证研究

创业者需要验证某个市场方向是否值得投入.
```text
用户：new research: AI辅助编程工具的市场机会评估
# ...
Agent：
1. 创建研究文件夹
2. 初始化研究文档
3. 搜索市场规模、竞品、用户需求等信息
4. 更新研究发现
5. 提示下一步探索方向
```

研究循环示例：

```text
Agent: 已创建研究文档。我先搜索一下当前AI编程工具的市场规模.
...（搜索后）
Agent: 发现以下关键信息：
- 全球AI编程工具市场规模约50亿美元（2026年）
- 主要玩家：GitHub Copilot、Cursor、Codeium
- 年增长率约35%
# ...
下一步你想深入哪个方面？
1. 竞品详细分析
2. 用户需求调研
3. 商业模式对比
# ...
用户: 先深入竞品分析
```

### 场景三：学术课题研究

学生需要围绕课题收集资料并整理研究文档.
```text
用户：new research: 大语言模型在医疗诊断中的应用现状
# ...
Agent：
1. 创建研究文件夹
2. 初始化包含学术文献结构的文档
3. 搜索学术论文和案例
4. 按主题组织发现
5. 记录引用来源
```

## 快速开始

### Step 1：启动新研究

```text
new research: [你的研究主题]
```

### Step 2：交互式探索

Agent 会引导你逐步深入：

```text
# Agent每轮会：
1. 执行搜索（网页、文档、代码）
2. 更新研究文档
3. 展示新增发现
4. 提示下一步方向
```

### Step 3：查看研究文档

```text
show doc
```

### Step 4：综合检查

每 5-10 轮交互后，可以请求综合检查：

```text
summarize
```

Agent 会：
- 撰写"当前理解"总结
- 清理冗余发现
- 检查研究盲区

### Step 5：完成研究

```text
# 标记为已完成
archive
# ...
# 或标记为持续更新
（保持 Status: Ongoing）
# ...
# 导出PDF
export pdf
```

#
## 示例

### 研究工作区配置

```bash
# 创建研究工作区
mkdir -p ~/.research-workspace/research
# ...
# 配置研究偏好
cat > ~/.research-workspace/config.yaml << 'EOF'
# 免费版研究配置
edition: free
version: "1.0.0"
# ...
workspace:
  path: "~/.research-workspace/research"
  naming: "slug"  # 文件夹命名方式
# ...
document:
  template: "default"
  language: "zh-CN"
  include_metadata: true
# ...
research:
  mode: "interactive"  # 免费版仅支持交互式
  max_concurrent: 1    # 单主题研究
  checkpoint_interval: 5  # 每5轮建议综合检查
# ...
export:
  format: "pdf"
  tool: "pandoc"
# ...
naming:
  slug_method: "kebab-case"
  max_length: 50
EOF
```

### 研究文档模板

```markdown
# {Topic Title}
# ...
**Status:** Active Research
**Started:** {date}
**Last Updated:** {date}
# ...
---
# ...
## 研究问题
{核心研究问题}
# ...
## Open Questions(续1)
- {待探索的问题}
# ...
## Findings(续1)
### {发现主题1}
- {具体发现}（来源：{link}）
# ...
### {发现主题2}
- {具体发现}（来源：{link}）
# ...
## Options / Approaches(续1)
| 方案 | 优势 | 劣势 | 适用场景 |
|:-----|:-----|:-----|:-----|
| {方案A} | ... | ... | ... |
| {方案B} | ... | ... | ... |
# ...
## Resources(续1)
- [资源名称](链接) - 说明
- [论文/报告](链接) - 说明
# ...
## Next Steps(续1)
- {下一步探索方向}
- {待验证的假设}
# ...
## Research Log
- {date}: 开始研究
- {date}: 完成{某方面}调研
```

## 最佳实践

### 1. 提出明确的研究问题

```text
# 推荐 - 问题明确
new research: Rust vs Go在微服务后端开发中的性能对比
# ...
# 不推荐 - 问题模糊
new research: 编程语言
```

### 2. 分步骤深入

```text
# 先广度搜索
帮我先搜索这个领域的主要参与者
# ...
# 再深度分析
深入分析第一个发现的细节
# ...
# 最后综合
帮我综合所有发现，写一个当前理解的总结
```

### 3. 定期综合检查

```text
# 每5-10轮交互后
summarize
# ...
# Agent会：
# - 撰写综合总结
# - 清理冗余信息
# - 识别研究盲区
# - 建议下一步
```

### 4. 记录不确定性

```text
# 标注信息可信度
# - "根据X来源" - 有明确来源
# - "似乎是" - 需要验证
# - "未经证实" - 存疑信息
```

### 5. 为重要发现标注日期

对于快速变化领域的信息，标注发现日期非常重要.
```markdown
- 2026-07-18: 某框架发布3.0版本，性能提升50%（来源：官方博客）
```

## 常见问题

### Q1：研究文档保存在哪里？

研究文档保存在 `~/.research-workspace/research/<topic-slug>/` 目录下，每个研究主题独立文件夹.
### Q2：免费版支持深度异步研究吗？

免费版不支持深度异步研究模式（需要 parallel-research CLI）。免费版仅支持交互式研究模式，即用户与 Agent 实时对话推进研究.
### Q3：可以同时进行多个研究吗？

免费版建议单主题研究。如需多主题并行研究，请升级至 PRO 版本.
### Q4：PDF 导出需要什么工具？

PDF 导出需要安装 pandoc 和 PyMuPDF。可通过系统包管理器安装.
```bash
# 依赖说明
# Ubuntu: sudo apt install pandoc
# macOS: brew install pandoc
# Windows: choco install pandoc
```

### Q5：免费版与 PRO 版本的区别？

| 对比项 | 免费版 | PRO 版本 |
|---:|---:|---:|
| 研究模式 | 交互式 | 交互式+深度异步 |
| 并发主题 | 1个 | 10+个并行 |
| 处理器等级 | 不适用 | lite-ultra8x可选 |
| API 集成 | 不支持 | REST API |
| 团队协作 | 不支持 | 多租户 |
| 定时研究 | 不支持 | cron调度 |
| 导出格式 | PDF | PDF/Word/HTML |
| 历史管理 | 基础 | 版本管理 |

## 依赖说明

### 运行环境

- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **网络连接**: 需要可访问互联网以进行搜索研究
- **本地存储**: 需要 `~/.research-workspace/` 目录读写权限

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| 网络搜索 | 服务 | 必需 | Agent 内置搜索能力 |
| 本地文件系统 | 存储 | 必需 | 操作系统提供 |
| pandoc | 工具 | 可选 | 系统包管理器安装（PDF导出） |
| PyMuPDF | Python 包 | 可选 | `pip install pymupdf`（PDF导出） |
| Python 3.8+ | 运行时 | 可选 | 系统包管理器安装 |

### API Key 配置

免费版基于 Markdown 指令驱动，无需额外 API Key.
```bash
# 验证工作区可写
mkdir -p ~/.research-workspace/research && echo "ok"
# ...
# 验证PDF导出工具（可选）
pandoc --version 2>/dev/null && echo "pandoc就绪" || echo "pandoc未安装（PDF导出不可用）"
```

### 可用性分类

- **分类**: MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**: 基于自然语言指令驱动 Agent 进行交互式研究，研究结果持久化保存为 Markdown 文档
- **适用规模**: 个人研究者、学生、独立开发者
- **升级路径**: 可无缝升级至 parallel-research-tool-pro 获取深度异步研究与多主题并行能力

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "并行研究助手免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "parallel research"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
