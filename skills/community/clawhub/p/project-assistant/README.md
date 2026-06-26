# Project Assistant 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 为 OpenClaw 设计的项目分析工具集，群聊单聊都能用！

---

## ✨ 亮点速览

### 💰 Token 消耗直接砍掉 80%-95%！

传统方式一次性加载整个项目文档，动辄 5-10 万 Token 😱

我们采用**分层文档架构**：

| 对比项 | Token 消耗 | 省了多少 |
|--------|-----------|---------|
| 传统一次性文档 | 50,000-100,000 | - |
| 我们 L0 概览 | ~11,500 | **77-88%** |
| 后续问答缓存命中 | ~0 | **接近 100%** |

### 🎯 50+ 项目类型一键识别

| 分类 | 支持类型 |
|------|---------|
| 嵌入式 MCU | STM32, ESP32, Arduino, Pico, Keil, IAR |
| 嵌入式 RTOS | FreeRTOS, Zephyr, RT-Thread |
| 嵌入式 Linux | Yocto, Buildroot, OpenWrt, QNX |
| Android | 应用, NDK, AOSP |
| iOS | Swift, SwiftUI |
| Web 前端 | React, Vue, Angular, Svelte, Next.js |
| Web 后端 | Django, FastAPI, Flask, Spring |
| 桌面应用 | Qt, Electron, Flutter |
| 系统编程 | C/C++, Rust, Go |

### 🔥 新功能：跨会话个性化配置

**群聊、单聊、不同会话，一个配置全搞定！**

```
# 设置工作目录
/set-workdir /home/user/projects/my-project

# 设置构建命令
/set-config build_command "make all"

# 设置偏好
/set-config preferences.language zh

# 设置自定义配置
/set-config custom.board_type bk7258
```

**支持任意配置项，你想存什么就存什么！**

| 配置项 | 说明 |
|--------|------|
| `workdir` | 工作目录 |
| `build_command` | 构建命令 |
| `run_command` | 运行命令 |
| `test_command` | 测试命令 |
| `preferences.*` | 偏好设置 |
| `custom.*` | 任意自定义配置 |

再也不用每次都重复输入了 🎉

---

## 🛠️ 核心功能

| 功能 | 说明 |
|------|------|
| 🤖 智能问答 | 自动识别问题类型，精准回答 |
| 📝 问答沉淀 | 自动生成文档，Git变更检测，过期提醒 |
| 📋 飞书集成 | 与飞书 Skill 协作，生成文档更新建议 ✨ |
| 🔗 调用链分析 | 支持 7 种语言，函数调用一追到底 |
| 📡 IPC 分析 | Binder/DBus/gRPC/SOME/IP/Socket |
| ⚡ 影响分析 | 改代码前就知道会影响谁 |
| 🏗️ 大型项目 | 自动识别子系统、进程、IPC 协议 |
| 💾 智能缓存 | 相似问题秒回，Token 省到底 |

---

## 📦 快速开始

### 安装

```bash
# ClawHub 安装（推荐）
claw install project-assistant

# 手动安装
git clone https://github.com/Northcipher/project-assistant.git ~/.claude/skills/project-assistant
```

### 基本使用

```
/set-workdir /path/to/project    # 设置工作目录（跨会话有效）
/init                            # 初始化项目
/init /path/to/project           # 初始化指定项目
/search-qa WiFi                  # 搜索历史问答 ✨
/check-qa                        # 检查问答文档是否过期 ✨
```

### 示例对话

**初始化项目：**

```
用户: /init

助手: [1/4] 探测项目类型... ✓ react (置信度: 95%)
      [2/4] 分析项目结构... ✓ src/, components/, hooks/
      [3/4] 解析配置文件... ✓ package.json, tsconfig.json
      [4/4] 生成项目文档... ✓ .claude/project.md
```

**智能问答（自动生成文档）：**

```
用户: 登录功能是怎么实现的？

助手: ## 登录实现

      通过 `AuthService` + `JwtUtil` 实现：

      1. 前端提交 → `LoginApi.login()`
      2. 后端验证 → `AuthService.authenticate()`
      3. Token生成 → `JwtUtil.createToken()`

      相关代码：
      - `src/pages/Login.tsx:45-78`
      - `src/api/auth.ts:23-56`

      📝 已生成文档: .claude/docs/qa/feature/20260311_120000_登录功能是怎么实现的.md
```

**搜索历史问答：**

```
用户: /search-qa WiFi

助手: 找到 3 条相关问答：

      1. [feature] WiFi怎么连接？| 2026-03-10
      2. [debug] WiFi连接失败怎么办？| 2026-03-11
      3. [api] WiFi API 接口说明 | 2026-03-09
```

**检查文档过期：**

```
用户: /check-qa

助手: 📋 文档检查结果：

      当前提交: 1e5c122
      过期文档: 2 条

      1. "WiFi怎么连接？" - 相关文件已修改
      2. "构建流程是什么？" - 代码有新提交

      建议重新询问这些问题以更新文档。
```

**影响分析：**

```
用户: 修改 login 函数会影响什么？

助手: ## 影响分析: login

      ### 直接调用者
      - `src/pages/Login.tsx:45` - handleLogin
      - `src/pages/Signup.tsx:78` - autoLogin

      ### 测试覆盖
      - `src/tests/auth.test.ts` - 3 个测试用例
```

---

## 🏢 飞书群聊场景

### 👨‍💻 开发工程师

```
@OpenClaw 登录功能在哪？
@OpenClaw 修改 handleLogin 会影响哪些地方？
@OpenClaw 调用链：从 main 到 UserService
```

### 🧪 测试工程师

```
@OpenClaw 登录模块有哪些测试用例？
@OpenClaw 测试覆盖率怎么样？
@OpenClaw 这个接口的边界条件是什么？
```

### 📋 产品经理

```
@OpenClaw 这个项目有多少个模块？
@OpenClaw 支付功能实现了吗？
@OpenClaw 项目的技术栈是什么？
```

### 🔧 运维工程师

```
@OpenClaw 项目的 CI/CD 配置在哪？
@OpenClaw 需要哪些环境变量？
@OpenClaw 如何构建和部署？
```

### 🎓 新人入职

```
@OpenClaw 帮我初始化这个项目
@OpenClaw 项目的架构是什么？
@OpenClaw 从哪里开始看代码？
```

### 👔 技术 Leader

```
@OpenClaw 这个模块的复杂度如何？
@OpenClaw 有哪些技术债务（TODO）？
@OpenClaw IPC 通信架构是怎样的？
```

---

## 🏗️ 架构设计

### 分层文档结构

```
.claude/
├── project.md           # L0: 项目概览 (~1-2KB)
├── index/               # 数据索引 (JSON)
│   ├── processes.json   # 进程索引
│   ├── ipc.json         # IPC 接口索引
│   └── structure.json   # 目录结构索引
├── docs/                # 详细文档（按需生成）
│   └── subsystems/      # 子系统文档
└── qa_cache.json        # Q&A 缓存
```

**按需生成**：详细文档只在需要时才生成，避免不必要的 Token 消耗。

### 缓存机制

- ✅ Git 状态检测 - 有未提交变更时更新
- ✅ 配置文件变更 - package.json 等被修改时更新
- ✅ 提交变化 - HEAD commit 改变时更新
- ✅ TTL 过期 - 默认 24 小时
- ✅ Q&A 缓存 - 相似问题自动匹配，有效期 7 天

---

## 📁 项目结构

```
project-assistant/
├── SKILL.md              # 主入口
├── config.json           # 工作目录配置（跨会话共享）✨新增
├── scripts/
│   ├── detector.py       # 项目类型探测器
│   ├── config_manager.py # 配置管理器 ✨新增
│   ├── parsers/          # 14 个配置文件解析器
│   ├── analyzers/        # 6 个代码分析器
│   └── utils/            # 工具函数
├── references/templates/ # 子 Skill 模板（11 个）
└── tests/                # 测试套件
```

---

## 📋 更新日志

### v1.5.0 (2026-03-11)

**🚀 性能优化：Token 消耗大幅降低**

- **SKILL.md 精简**：1884 行 → 208 行（**节省 89%**）
- **分层架构**：主入口 + 按需加载子模块
- **倒排索引**：问答搜索 O(1) 复杂度
- **命令合并**：统一使用 `/set-config`

**新增子模块：**
- `references/guides/config.md` - 配置管理详解
- `references/guides/init.md` - 项目初始化详解
- `references/guides/qa.md` - 问答功能详解
- `references/guides/feishu.md` - 飞书集成详解
- `references/guides/examples.md` - 示例对话

**优化效果：**
| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| SKILL.md 行数 | 1884 | 208 | 89% |
| 每次触发 Token | ~15000 | ~2000 | 87% |
| 问答搜索复杂度 | O(n) | O(1) | 显著 |

### v1.4.0 (2026-03-11)

**✨ 新功能：飞书文档集成**

- 新增 `feishu_doc_manager.py` - 飞书文档管理器
- 与飞书 Skill 协作，生成文档更新建议
- **不直接修改文档**，只生成建议报告
- 分析项目变更，生成飞书友好的更新建议
- 按优先级分类更新建议（高/中/低）

**新增命令：**
- `/feishu-report` - 生成飞书文档更新建议报告
- `/feishu-status` - 检查文档同步状态
- `/feishu-suggest <file> <type>` - 生成单个文件的文档建议

**新增配置项：**
- `feishu.doc_token` - 飞书文档 token
- `feishu.folder_token` - 飞书文件夹 token
- `feishu.wiki_token` - 飞书知识库 token
- `feishu.doc_url` - 飞书文档 URL

**解决的问题：**
- ❌ 之前：项目变更后不知道哪些文档需要更新
- ✅ 现在：自动生成更新建议，与飞书 Skill 协作

### v1.3.0 (2026-03-11)

**✨ 新功能：问答文档沉淀系统**

- 新增 `qa_doc_manager.py` - 问答文档管理器
- 回答完成后自动生成 Markdown 文档
- 按 8 种分类自动归档（架构、构建、功能、调试等）
- 记录 Git commit hash，支持过期检测
- 记录相关文件哈希，代码变更时提醒

**新增命令：**
- `/search-qa <关键词>` - 搜索历史问答
- `/list-qa [分类]` - 列出问答文档
- `/check-qa` - 检查文档是否过期
- `/delete-qa <id>` - 删除问答文档

**解决的问题：**
- ❌ 之前：问过的问题下次还要重新问
- ✅ 现在：自动沉淀成文档，新人可以直接查

### v1.2.0 (2026-03-11)

**✨ 新功能：通用个性化配置系统**

- 重构 `config_manager.py` 支持任意配置项
- 新增 `/set-config <key> <value>` 命令 - 设置任意配置
- 新增 `/get-config <key>` 命令 - 获取配置项
- 新增 `/show-config` 命令 - 显示所有配置
- 新增 `/delete-config <key>` 命令 - 删除配置项
- 支持嵌套键，如 `preferences.language`、`custom.board_type`

**预定义配置项：**
- `workdir` - 工作目录
- `build_command` - 构建命令
- `run_command` - 运行命令
- `test_command` - 测试命令
- `preferences.*` - 偏好设置
- `custom.*` - 自定义配置（任意键值对）

### v1.1.0 (2026-03-11)

**✨ 新功能：跨会话工作目录配置**

- 新增 `/set-workdir` 命令 - 设置工作目录
- 新增 `/show-workdir` 命令 - 显示当前配置
- 新增 `/clear-workdir` 命令 - 清除配置
- 新增 `config_manager.py` - 配置管理器
- 配置存储在 `config.json`，群聊单聊共享
- 更新 README 为小红书风格

**解决的问题：**
- ❌ 之前：每个会话都要重新指定项目路径
- ✅ 现在：设置一次，群聊单聊都能用

---

## 📦 依赖

- Python 3.6+
- Git（可选）
- PyYAML（可选，CI/CD 解析）

---

## 📜 许可证

[MIT License](LICENSE)

---

**#OpenClaw #项目分析 #AI助手 #代码分析 #开发工具**