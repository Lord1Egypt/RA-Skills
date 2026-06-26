---
name: project-assistant
description: 项目初始化与智能分析工具。当用户要求初始化新项目、分析项目结构、项目问答时使用。触发词：初始化项目、init、分析项目、项目问答。
metadata:
  openclaw:
    emoji: "🚀"
    homepage: "https://github.com/Northcipher/project-assistant"
    requires:
      bins: ["python3"]
---

# project-assistant

项目全能助手，支持 50+ 项目类型，提供智能问答、文档沉淀、飞书集成。

## 触发条件

TRIGGER when: 用户询问项目相关问题：
- "这个项目的架构是什么？"
- "XXX功能是怎么实现的？"
- "如何构建/运行这个项目？"
- "修改XXX会影响什么？"

## 角色视角

| 问题类型 | 角色 | 关注点 |
|---------|------|-------|
| 架构设计 | 架构师 | 系统架构、扩展性 |
| 功能实现 | 开发工程师 | 代码逻辑、调试 |
| 项目进度 | 项目经理 | 里程碑、风险点 |
| 测试质量 | 测试工程师 | 测试用例、覆盖率 |
| 部署运维 | DevOps | 部署流程、环境配置 |

---

## 命令索引

### 配置管理

| 命令 | 说明 | 详细指南 |
|------|------|---------|
| `/set-config <key> <value>` | 设置配置项 | `{baseDir}/references/guides/config.md` |
| `/get-config <key>` | 获取配置项 | - |
| `/show-config` | 显示所有配置 | - |
| `/delete-config <key>` | 删除配置项 | - |

### 项目初始化

| 命令 | 说明 | 详细指南 |
|------|------|---------|
| `/init [目录] [选项]` | 初始化项目 | `{baseDir}/references/guides/init.md` |

### 问答文档

| 命令 | 说明 | 详细指南 |
|------|------|---------|
| `/search-qa <关键词>` | 搜索历史问答 | `{baseDir}/references/guides/qa.md` |
| `/list-qa [分类]` | 列出问答文档 | - |
| `/check-qa` | 检查文档过期 | - |
| `/delete-qa <id>` | 删除问答文档 | - |

### 飞书集成

| 命令 | 说明 | 详细指南 |
|------|------|---------|
| `/feishu-report` | 生成更新建议 | `{baseDir}/references/guides/feishu.md` |
| `/feishu-status` | 检查同步状态 | - |
| `/feishu-suggest <file> <type>` | 生成文档建议 | - |

---

## 执行流程

### Step 1: 确定项目目录

```bash
# 读取配置的工作目录
python3 {baseDir}/scripts/config_manager.py {baseDir} get workdir
```

优先级：命令行参数 > 配置的 workdir > 当前目录

### Step 2: 检查项目文档

检查 `$PROJECT_DIR/.claude/project.md` 是否存在，不存在则调用 `/init`

### Step 3: 智能缓存检查

根据问题类型决定缓存检查策略：

| 问题类型 | 检查策略 | 原因 |
|---------|---------|------|
| LOCATION | 跳过 | 直接搜索即可 |
| CONFIG | 快速 | 只检查时间戳 |
| ARCHITECTURE | 完整 | 需要最新数据 |
| IMPACT | 强制 | 必须最新 |

```bash
python3 {baseDir}/scripts/utils/cache_manager.py check "$PROJECT_DIR" --quick
```

### Step 4: 搜索历史问答

```bash
python3 {baseDir}/scripts/qa_doc_manager.py "$PROJECT_DIR" search "$QUERY"
```

### Step 5: 分析并回答

根据问题意图选择回答策略：

| 意图 | 关键词 | 格式 |
|------|--------|------|
| LOCATION | 在哪、哪个文件 | 简洁路径 |
| EXPLAIN | 怎么实现、原理 | Markdown详情 |
| MODIFY | 如何修改 | 步骤指导 |
| IMPACT | 影响什么 | 影响树 |

### Step 6: 沉淀问答文档

```bash
python3 {baseDir}/scripts/qa_doc_manager.py "$PROJECT_DIR" create "$QUESTION" "$ANSWER" "$FILES" "$TAGS"
```

---

## 工具命令

```bash
# 配置管理
python3 {baseDir}/scripts/config_manager.py {baseDir} <get|set|delete|show> [args]

# 项目探测
python3 {baseDir}/scripts/detector.py "$PROJECT_DIR"

# 问答文档
python3 {baseDir}/scripts/qa_doc_manager.py "$PROJECT_DIR" <search|list|check|create|delete> [args]

# 飞书集成
python3 {baseDir}/scripts/feishu_doc_manager.py "$PROJECT_DIR" <report|status|suggest> [args]

# 缓存管理
python3 {baseDir}/scripts/utils/cache_manager.py <check|update|clear> "$PROJECT_DIR"

# 调用链分析
python3 {baseDir}/scripts/utils/call_chain_analyzer.py "$PROJECT_DIR" "$FUNCTION" --impact
```

---

## 子模块索引

按需加载详细指南：

| 模块 | 路径 | 内容 |
|------|------|------|
| 配置管理 | `{baseDir}/references/guides/config.md` | 配置项详细说明 |
| 项目初始化 | `{baseDir}/references/guides/init.md` | 初始化流程详解 |
| 问答文档 | `{baseDir}/references/guides/qa.md` | 问答功能详解 |
| 飞书集成 | `{baseDir}/references/guides/feishu.md` | 飞书协作详解 |
| 示例对话 | `{baseDir}/references/guides/examples.md` | 完整示例 |

---

## 项目类型支持

| 分类 | 类型 |
|------|------|
| 嵌入式MCU | STM32, ESP32, Arduino, Pico, Keil, IAR |
| 嵌入式RTOS | FreeRTOS, Zephyr, RT-Thread |
| 嵌入式Linux | Yocto, Buildroot, OpenWrt, QNX |
| Android | 应用, NDK, AOSP |
| iOS | Swift, SwiftUI |
| Web前端 | React, Vue, Angular, Svelte, Next.js |
| Web后端 | Django, FastAPI, Flask, Spring |
| 桌面应用 | Qt, Electron, Flutter |
| 系统编程 | C/C++, Rust, Go |

---

## 目录结构

```
project-assistant/
├── SKILL.md                    # 主入口（本文件）
├── scripts/                    # Python 工具脚本
│   ├── config_manager.py       # 配置管理器
│   ├── qa_doc_manager.py       # 问答文档管理器
│   ├── feishu_doc_manager.py   # 飞书文档管理器
│   ├── detector.py             # 项目类型探测器
│   ├── parsers/                # 配置文件解析器
│   ├── analyzers/              # 代码分析器
│   └── utils/                  # 工具函数
├── references/
│   ├── templates/              # 子 Skill 模板
│   └── guides/                 # 详细指南（按需加载）
├── tests/                      # 测试套件
└── README.md
```

## 依赖

- Python 3.6+
- Git（可选）
- PyYAML（可选）

## 许可证

MIT License