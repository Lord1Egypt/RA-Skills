# Kinema's Concept Re-Search Onboarding

> 本文档指导 AI Agent 完成首次环境配置。按顺序执行，遇到问题时参考 Troubleshooting。

## Prerequisites | 前置条件

- **searxng-search-cli** skill 已安装并配置完成（本 skill 依赖 SearXNG 搜索引擎）
- 网络（搜索时需访问外部搜索引擎）

## Step 1: 检查依赖 Skill

### 检测

确认 searxng-search-cli 已安装并可用：

```bash
searxng-search status
```

**期望输出**: `✓ 服务运行中: http://127.0.0.1:8888`

如果 searxng-search-cli 未安装：
1. 先安装 searxng-search-cli skill
2. 按照其 `references/ONBOARDING.md` 完成 SearXNG 环境配置
3. 确认搜索功能正常后再继续

### 验证

```bash
searxng-search search "test" --limit 1
```

**期望输出**: 至少一条搜索结果

## Step 2: 确认工作目录

### 检测

```bash
ls -d ~/projects/ 2>/dev/null && echo "OK" || echo "NEED_CREATE"
```

### 安装

```bash
mkdir -p ~/projects
```

### 验证

```bash
ls -d ~/projects/
```

## Step 3: 验证搜索工具

### 验证

使用多种搜索方式验证 SearXNG 可用：

```bash
# 基础搜索
searxng-search search "artificial intelligence" --limit 3

# 指定引擎搜索
searxng-search search "AI framework" --engine google --limit 3

# 中文搜索
searxng-search search "人工智能" --lang zh --limit 3
```

**期望输出**: 每次搜索均返回有效结果列表

## Step 4: 功能测试

### 验证

执行一次完整的概念搜索流程验证：

```bash
# 模拟搜索：使用多组关键词搜索同一概念
searxng-search search "concept research tool" --limit 5
searxng-search search "concept status research" --lang zh --limit 5
```

确认搜索结果可正常获取并展示。

## Onboarding 完成

以上步骤全部通过后，onboarding 完成。后续可按 SKILL.md 中的工作流使用本 skill 进行概念调研。

## Troubleshooting | 故障排除

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `searxng-search: command not found` | searxng-search-cli 未安装 | 先安装 searxng-search-cli skill 并完成其 onboarding |
| `connection refused` | SearXNG 服务未启动 | 执行 `searxng-search start` 启动服务 |
| 搜索返回空结果 | 所有引擎被封/超时 | 尝试换关键词或指定引擎 `--engine brave` |
| `projects/` 目录不存在 | 工作目录未创建 | 执行 `mkdir -p ~/projects` |
| 网络超时 | 网络不稳定 | 检查网络连接，推荐在稳定网络环境下使用 |
