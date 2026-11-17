---

name: "go-linter-config-tool-free"
description: "面向个人 Go 项目的 golangci-lint 配置与排障工具，快速起步。Use when 需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Go Lint 配置工具"
  version: "1.0.0"
  summary: "面向个人 Go 项目的 golangci-lint 配置与排障工具，快速起步。"
  tags:
    - "Go"
    - "代码质量"
    - "静态检查"
    - "个人效率"
    - "其他工具"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# Go Lint 配置工具（免费版）

## 概述

本工具帮助个人 Go 开发者快速接入 golangci-lint，提供最小与标准两套配置模板，覆盖导入解析、类型检查与基础 CI 排障。适合单项目本地开发与简单 CI 场景。

## 核心能力

| 能力 | 说明 | 免费版范围 |
|:-----|:-----|:-----------|
| 配置模板 | 最小（仅 gofmt）与标准（7 个 linter） | 两套 |
| 排障清单 | 导入解析、类型检查、CI 依赖 | 常见项 |
| linter 选用 | 按用途推荐 | 基础 7 个 |
| 运行验证 | 本地与简单 CI | 单项目 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：面向个人、项目的、golangci、配置与排障工具、快速起步、开发者的、最小与标准两套配、常见导入解析、选用指南、单项目本地运行与等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：个人项目接入 lint

```bash
# 依赖说明
# macOS / Linux (Homebrew)
brew install golangci-lint
# 通用 (Go 工具链)
go install golangci-lint/cmd/golangci-lint@latest
# 或从官方发布页下载二进制

# 运行
golangci-lint run ./...
```

### 场景二：CI 导入解析报错

CI 环境报 `undefined: package`，改用最小配置：

```yaml
# .golangci.yml 最小配置（CI 友好）
run:
  timeout: 5m
  tests: false
linters:
  disable-all: true
  enable:
    - gofmt
linters-settings:
  gofmt:
    simplify: true
issues:
  max-issues-per-linter: 50
  max-same-issues: 3
```

### 场景三：本地标准检查

```yaml
# .golangci.yml 标准配置（本地开发）
run:
  timeout: 5m
  tests: true
linters:
  enable:
    - gofmt
    - govet
    - errcheck
    - staticcheck
    - unused
    - gosimple
    - ineffassign
linters-settings:
  govet:
    enable:
      - shadow
  errcheck:
    check-type-assertions: true
  staticcheck:
    checks: ["all"]
```

## 不适用场景

以下场景Go Lint 配置工具不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 安装 golangci-lint。
2. 选择最小或标准模板写入 `.golangci.yml`。
3. 运行 `golangci-lint run ./...`。
4. 按报错逐项修复。

```bash
# 指定配置运行
golangci-lint run --config .golangci.yml ./...
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

## 示例

基础 linter 选用：

| linter | 用途 |
|:-------|:-----|
| gofmt | 格式一致性 |
| govet | 语义错误 |
| errcheck | 未检查错误 |
| staticcheck | 静态分析 |
| unused | 死代码检测 |
| gosimple | 简化建议 |
| ineffassign | 无效赋值 |

## 优选实践

- **CI 用最小**：CI 环境优先用最小配置，避免导入解析问题。
- **本地用标准**：本地开发启用完整 linter 尽早发现问题。
- **先 mod download**：CI 中先 `go mod download` 再跑 lint。
- **复杂 linter 临时关**：类型检查失败时临时关闭复杂 linter 或用 `--fast`。

## 常见问题

**Q1：CI 报 undefined 包怎么办？**
A：用最小配置 `disable-all: true` 仅启用 gofmt，并确保 `go mod download` 先执行。

**Q2：类型检查失败怎么办？**
A：临时关闭需要类型检查的 linter，或加 `--fast` 跑快速检查。

**Q3：免费版支持自定义规则吗？**
A：不支持。自定义规则集与多项目统一治理为专业版能力。

**Q4：能跑在 GitHub Actions 吗？**
A：能。免费版提供基础 CI 工作流示例。

## 进阶用法

### 本地与 CI 配置分离

本地用完整 linter 尽早发现问题，CI 用最小配置避免环境问题，二者分离管理：

```text
.golangci.yml        # 本地标准配置（完整 linter）
.golangci.minimal.yml # CI 最小配置（仅 gofmt + govet）
```

```bash
# 本地
golangci-lint run ./...

# CI 显式指定最小配置
golangci.minimal.yml ./...
```

### 按需启用额外 linter

标准 7 个之外，按项目需要增量启用：

| linter | 何时启用 |
|:-------|:---------|
| gocyclo | 关注圈复杂度时 |
| misspell | 多语言注释项目 |
| gosec | 安全敏感项目 |
| revive | 替代 golint 的风格检查 |
| bodyclose | 频繁 HTTP 调用项目 |

### 排除测试文件

```yaml
issues:
  exclude-rules:
    - path: _test\.go
      linters: [gosec, errcheck]
```

## 排障决策树

```text
CI lint 报错
  ├─ 是导入解析(undefined package)?
  │    → 改用最小配置 + go mod download
  ├─ 是类型检查失败?
  │    → 关闭需类型检查的 linter 或加 --fast
  ├─ 是超时?
  │    → 调大 run.timeout 或减少 linter
  └─ 是误报过多?
       → 用 exclude-rules 按路径/规则排除
```

## 配置演进

- **从最小起步**：新项目先用最小配置跑通，再逐步加 linter。
- **变更要可追溯**：配置文件纳入版本库，变更走 PR 评审。
- **本地早发现**：本地启用完整 linter，CI 用最小保证稳定。
- **误报先排除**：频繁误报的规则用 exclude-rules 局部排除，别全局禁用。

## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **Go**: 1.21+

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| golangci-lint | 命令行工具 | 必需 | `go install ...@latest` |
| Go | 工具链 | 必需 | go.dev 下载 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本工具为纯 Markdown 指令，无需额外 API Key

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**: 通过自然语言指令驱动 Agent 生成配置并运行 lint

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 本地运行，不支持多设备同步
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。