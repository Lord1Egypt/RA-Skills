---
name: project-onboarding
version: "2.0.0"
homepage: https://github.com/z-Zihan/awesome-skills
description: >
  帮助有经验的开发者快速接手陌生项目，支持前端 Web、后端服务、
  客户端（Electron/Tauri）、小程序、移动端等多种项目类型。自动识别项目类型，分阶段输出
  项目概览、开发流程、工程规范、类型专项指南等，达到"可以开始安全开发"的状态。
  触发词：接手项目, 项目上手, 快速上手, 新人接手, 项目入门, onboarding,
  如何开发, 怎么启动项目, 项目怎么跑, 开发流程, onboarding guide,
  how to onboard, project handover, developer quick start.
  NOT for: generating long architecture reports, code analysis without dev context,
  beginner programming tutorials, onboarding for interns.
---

# project-onboarding — 项目接手指南

## 语言规则

**检测用户使用的语言，全程使用同一语言输出。** 中文用户 → 读下方中文部分，全中文输出；English users → read the English section below, output in English only. 技术术语（React、Electron、IPC 等）保留原文即可。

---

# 中文版

帮助有经验的开发者快速理解并接手一个陌生项目，尽快具备实际开发能力。

## 支持的项目类型

按优先级排序：

| 类型 | 识别信号 | 专项模块 |
|---|---|---|
| **前端 Web** | React/Vue/Svelte/Angular, webpack/vite/nextjs | 组件体系、路由、状态管理、CSS 方案、API 集成、浏览器兼容 |
| **后端服务** | Express/Nest/Django/Spring/Gin, ORM/migration | 数据库 Schema、ORM、中间件链、API 设计、认证鉴权、缓存与队列 |
| **客户端** | Electron/Tauri/Capacitor, 主进程/渲染进程 | 主进程架构、渲染进程、IPC 通信、原生能力、签名与分发、自动更新 |
| **小程序** | 微信/支付宝/抖音小程序, app.json/pages.json | 平台适配、分包策略、审核流程、原生能力调用、用户体系 |
| **移动端** | React Native/Flutter/SwiftUI/Kotlin, podfile/gradle | 原生模块 Bridge、热更新、应用签名、应用商店发布、权限管理 |

**多类型混合项目**（如 Electron + Vue、Tauri + React）：同时加载对应专项模块，按优先级排序。

> **扩展指南**：新增项目类型时，需要同步更新三个位置：
> 1. 上方「支持的项目类型」表格
> 2. 「项目类型自动识别」信号列表
> 3. 对应的专项模块章节（新增或复用）
> 建议保持模块命名和排序的一致性。

## 这个 Skill 不是

- 面向编程新手
- 面向实习生教学
- 面向基础知识解释
- 面向纯代码分析

## 核心目标

让专业开发者在最短时间内完成：

- 项目理解
- 工程结构理解
- 开发流程理解
- 团队规范理解
- 环境体系理解
- 项目类型特有的核心能力理解
- 发布流程理解
- 调试与开发能力建立

最终达到：

**"开发者已经可以开始安全地开发功能并参与协作。"**

## 语言策略

- 默认输出中文，同时提供英文版本
- 中文优先

## 核心原则

### 1. 以"快速进入开发状态"为最高优先级

优先帮助开发者理解：

- 项目如何运行
- 功能如何开发
- 项目类型特有的核心机制
- 目录如何组织
- 环境如何切换
- 如何调试
- 如何发版
- 如何避免踩坑

**而不是：**

- 生成超长架构分析报告
- 输出无意义目录树
- 罗列所有源码文件

### 2. 避免一次性信息轰炸

- 分阶段输出
- 优先级排序
- 保持简洁
- 支持多轮渐进式探索

### 3. 模拟"资深工程师带新人"

你的角色不是代码分析器，而是团队里的资深工程师在带一个有经验的新同事。

重点关注：

- 实际开发流程
- 隐式规范
- 高风险区域
- 常见坑
- 推荐参考模块

### 4. 证据优先，不假装理解

- 所有结论基于仓库真实证据
- 仓库中没有的规范或机制，不要编造
- 区分：已确认事实 / 合理推断 / 证据不足

### 5. 按项目类型裁剪内容

- 只分析与当前项目类型相关的模块
- 不要给后端项目讲组件体系，不要给前端项目讲 ORM
- 混合项目按优先级排序专项模块

## 执行工具指引

本 Skill 的每个分析步骤都应配合具体工具执行，而非凭空"编"输出：

### 项目类型识别 — 执行动作

1. `read {project}/package.json` → 提取 dependencies 和 devDependencies，匹配前端/客户端/Node 后端信号
2. `exec find {project} -maxdepth 2 -name "*.config.*" -o -name "go.mod" -o -name "Cargo.toml" -o -name "pom.xml" -o -name "app.json"` → 识别后端/小程序/移动端信号
3. `exec ls {project}/src-tauri/ {project}/electron/ 2>/dev/null` → 客户端信号
4. `exec ls {project}/android/ {project}/ios/ 2>/dev/null` → 移动端信号
5. 多信号命中时 → 按混合项目处理，所有匹配的专项模块均加载

### Stage 1 快速总览 — 执行动作

1. `read {project}/package.json` 或 `Cargo.toml` 或 `go.mod` → 技术栈
2. `exec ls {project}/` → 目录结构概览
3. `read {project}/README.md` → 项目用途（如存在）
4. `read {project}/.env.example` → 环境变量（如存在）
5. `exec find {project} -name "*.config.*" -maxdepth 1` → 构建配置

### Stage 2 通用模块深入 — 执行动作

1. `exec find {project}/src -type d -maxdepth 2` → 目录结构
2. `read {project}/src/index.*` 或 `main.*` → 入口文件
3. `exec find {project} -name ".eslintrc*" -o -name ".prettierrc*" -o -name "tsconfig.json" -maxdepth 1` → 工程规范
4. `exec find {project} -name "Dockerfile" -o -name "docker-compose*" -o -name ".github" -type d -maxdepth 2` → 部署配置
5. `exec find {project} -name "*.test.*" -o -name "*.spec.*" | head -5` → 测试结构

### Stage 3 专项模块 — 按类型选择执行

**前端 Web：**
- `exec find {project}/src -name "router*" -o -name "routes*" | head -5` → 路由
- `exec find {project}/src -name "store*" -o -name "*reducer*" | head -5` → 状态管理
- `exec find {project}/src -name "request*" -o -name "api*" -o -name "http*" | head -5` → API 层

**后端：**
- `exec find {project} -path "*/migration*" -o -path "*/schema*" | head -5` → 数据库
- `exec find {project} -path "*/middleware*" -o -path "*/guard*" | head -5` → 中间件
- `exec find {project} -path "*/route*" -o -name "controller*" | head -5` → 路由/控制器

**客户端：**
- `read {project}/electron/main.*` 或 `{project}/src-tauri/src/main.rs` → 主进程
- `exec find {project} -name "preload*" -o -name "bridge*" | head -5` → IPC

### 大项目策略

当 `exec find {project} -type f | wc -l` 超过 200 时：
1. 先用 `find` + `ls` 建立文件索引，不全量读取
2. 只读 P0 文件（package.json、入口、README）
3. 核心链路深入（入口 → 中间件 → 服务 → 数据），其余跳过

### 输出格式定义

每个 Stage 的输出应使用以下 Markdown 结构：

```markdown
# [项目名] — Stage N: [阶段名]

## 项目类型
[类型]（识别信号：[列出检测到的信号]）

## [各分析维度]
...

## ⏸ 下一步
[提示用户可以深入的方向]
```

---

## 分析模块

### 一、通用模块（所有项目类型）

以下模块适用于任何项目类型，按分析顺序排列：

#### 1. 项目概览

- 项目用途与业务领域
- 项目类型（自动识别）
- 核心能力与主要模块
- 技术栈
- 系统架构
- 外部依赖
- 核心链路

#### 2. 开发快速启动

- 如何安装依赖
- 如何启动项目
- 本地开发命令
- 如何切换环境
- 必需环境变量
- 如何本地调试
- 如何运行测试
- 如何构建

#### 3. 项目目录导航

必须说明：

- 为什么这样组织
- 哪些目录最重要
- 哪些目录最常修改
- 哪些目录风险最高
- 哪些属于基础设施

#### 4. 工程规范

- 命名规范
- 目录规范
- 代码组织方式
- commit 规范
- lint/format 规范
- 测试规范
- 错误处理规范
- 隐式规范（README 没写但团队默认遵守的规则）

#### 5. 环境与部署体系

- 环境列表（local/dev/test/staging/production 等）
- 环境如何切换
- 配置如何管理
- CI/CD 流程
- 如何发版 / 如何提测 / 如何回滚

#### 6. 团队协作流程

- 分支策略
- PR / Code Review 流程
- QA / UAT 流程

#### 7. 高频开发路径

总结团队最常见的开发套路（按项目类型定制示例）

#### 8. 推荐参考模块

- 最规范的模块
- 最推荐模仿的实现
- 入口文件

#### 9. 危险区域识别

- 哪些区域改动风险高
- 哪些代码耦合严重
- 哪些模块容易引发线上问题

---

### 二、前端 Web 专项

当识别到前端 Web 项目时加载：

#### A. 组件体系与 UI 基础设施

- 内部组件库
- 第三方组件库
- layout 系统 / icon 系统 / theme 系统
- 通用业务组件
- 哪些组件应优先复用
- 新组件放哪里

#### B. 路由系统

- 路由如何组织
- 路由守卫与权限
- 动态路由 / 懒加载
- 新增页面的路由配置方式

#### C. 状态管理

- 使用的方案（Redux/Pinia/Zustand/Jotai 等）
- 全局状态 vs 局部状态的划分策略
- store 如何组织
- 新功能应该用全局还是局部状态

#### D. CSS 与样式方案

- CSS Modules / Tailwind / CSS-in-JS / styled-components / SCSS
- 设计系统 / token 体系
- 样式约定

#### E. API 集成

- 请求层如何封装
- token/auth 如何工作
- 错误拦截机制
- mock 策略
- 新接口应该如何接入

**高频开发路径示例（前端 Web）：**

```
新增页面: 新增 route → 新增 page → 新增 API → 接入 store → 接入权限 → 配置菜单 → 提测 → 发版
新增接口: 定义 API → request 封装 → 类型定义 → hooks/store 接入 → 页面消费 → 错误处理
新增组件: 放入 shared/components → 补充 story/test → theme 适配 → 权限处理
```

---

### 三、客户端专项

当识别到 Electron / Tauri / Capacitor 等客户端项目时加载：

#### A. 进程架构

**Electron 项目：**
- 主进程（Main Process）职责与入口
- 渲染进程（Renderer Process）架构
- 预加载脚本（Preload）与 contextBridge
- 多窗口管理
- 进程间通信（IPC）设计

**Tauri 项目：**
- 前端层（WebView）
- Rust 后端层（Tauri Commands）
- IPC 通信方式（invoke/listen）
- 插件系统
- 安全策略（allowlist/CSP）

#### B. 原生能力集成

- 文件系统操作（读写、对话框）
- 系统托盘与通知
- 剪贴板 / 屏幕截图 / 全局快捷键
- 网络状态监听
- 系统信息获取
- 原生模块（Node Addons / Rust FFI）

#### C. 签名与分发

- 开发者证书与签名配置
- macOS: codesign + notary / Windows: 签名证书
- 自动更新机制（autoUpdater）
- 更新服务器配置
- 各平台分发渠道（App Store / Microsoft Store / 自建）

#### D. 构建与打包

- 构建命令与配置
- 多平台构建（macOS arm64/x64 / Windows x64）
- 安装包格式（DMG/EXE/MSI/AppImage）
- 构建时间优化
- CI/CD 中的构建流程

#### E. 客户端特有调试

- 主进程调试
- 渲染进程调试（DevTools）
- IPC 通信调试
- 原生能力调试
- 性能分析（CPU/内存/启动速度）

**高频开发路径示例（客户端）：**

```
新增功能: 前端开发 → IPC 通信定义 → 主进程/Rust 命令实现 → 联调 → 测试 → 构建
新增原生能力: 调研 API → 实现 IPC 命令 → 前端调用封装 → 错误处理 → 多平台测试
发版流程: 构建多平台 → 签名 → 公证 → 上传更新服务器 → 灰度 → 全量
```

---

### 四、后端服务专项

当识别到 Express/Nest/Django/Spring/Gin 等后端服务项目时加载：

#### A. 数据库与存储

- 使用的数据库（MySQL/PostgreSQL/MongoDB/Redis 等）
- ORM/Query Builder（Prisma/TypeORM/Sequelize/GORM 等）
- Migration 策略
- 数据库 Schema 设计思路
- 缓存策略（Redis/Memcached）
- 文件存储（OSS/S3/本地）

#### B. 中间件与请求处理

- 中间件链与执行顺序
- 认证与鉴权（JWT/Session/OAuth）
- 请求验证与参数校验
- 日志策略
- 限流与熔断

#### C. API 设计

- RESTful / GraphQL / gRPC / tRPC
- API 版本管理
- 错误码体系
- 文档生成（Swagger/OpenAPI）
- 请求/响应格式约定

#### D. 异步与任务处理

- 消息队列（RabbitMQ/Kafka/Redis）
- 定时任务（Cron）
- 后台任务/Worker
- WebSocket / SSE 长连接

**高频开发路径示例（后端）：**

```
新增接口: 定义路由 → 参数校验 → 业务逻辑 → 数据库操作 → 返回响应 → 补充测试
新增数据表: 设计 Schema → 创建 Migration → 编写 Model → 实现业务逻辑 → API 接入
新增定时任务: 注册 Cron → 实现任务逻辑 → 日志与监控 → 测试验证
```

---

### 五、小程序专项

当识别到微信/支付宝/抖音小程序项目时加载：

#### A. 平台与框架

- 目标平台（微信/支付宝/抖音/多端）
- 使用原生还是跨端框架（Taro/uni-app）
- 平台 API 差异处理

#### B. 小程序架构

- 页面与组件结构
- 全局配置（app.json/pages.json）
- 自定义组件封装
- 分包策略
- 插件使用

#### C. 用户体系与登录

- 登录流程（wx.login 等）
- 用户信息获取与存储
- Session 管理
- 与后端用户系统的对接

#### D. 发布与审核

- 审核流程与注意事项
- 体验版 / 正式版 发布
- 版本管理与回滚
- 小程序码 / 分享配置

#### E. 性能优化

- 分包加载
- 图片懒加载
- setData 优化
- 长列表优化
- 自定义组件懒加载

**高频开发路径示例（小程序）：**

```
新增页面: pages.json 注册 → 创建页面目录 → 实现页面逻辑 → 配置路由 → 提交体验版 → 审核
新增组件: 创建组件目录 → 实现 component → 引入使用 → 样式隔离
新增接口: 封装请求方法 → 页面调用 → 错误处理 → 加载态
```

---

### 六、移动端专项

当识别到 React Native / Flutter / SwiftUI / Kotlin 等移动端项目时加载：

#### A. 应用架构

- 使用的框架（React Native/Flutter/SwiftUI/Compose）
- 架构模式（MVI/MVVM/Clean Architecture）
- 模块化方案
- 导航系统

#### B. 原生模块与 Bridge

- 原生模块列表与用途
- Bridge 通信机制
- 如何新增原生模块
- 第三方原生 SDK 集成方式

#### C. 状态管理与数据持久化

- 状态管理方案
- 本地存储（AsyncStorage/MMKV/SQLite/CoreData）
- 离线策略

#### D. 发布与应用商店

- Android: 签名配置（keystore）
- iOS: 证书与 Profile 管理
- 应用商店提交流程（App Store / Google Play）
- 热更新方案（CodePush/EAS Update）
- TestFlight / 内测分发

#### E. 移动端特有调试

- 真机调试流程
- 性能分析工具
- 崩溃日志收集
- 网络抓包

**高频开发路径示例（移动端）：**

```
新增页面: 创建页面/Screen → 注册路由 → 接入状态 → 接入导航 → 联调接口
新增原生模块: 定义 Bridge 接口 → 实现 Android/iOS 原生代码 → JS 调用封装 → 测试
发版流程: 构建 Android/iOS → 签名 → 上传商店 → 提交审核 → 发布
```

---

## 项目类型自动识别

分析项目前，先通过以下信号识别项目类型（可多选）：

**前端 Web 信号：**
- `package.json` 中有 react/vue/svelte/angular/next/nuxt
- 存在 webpack.config/vite.config/tsconfig.json
- 存在 public/index.html 或 index.html
- src 下有 pages/views/components/hooks/store 目录

**客户端信号：**
- `package.json` 中有 electron/tauri
- 存在 electron/ 目录或 src-tauri/ 目录
- Capacitor 配置文件
- main process 入口文件

**后端服务信号：**
- `package.json` 中有 express/nest/fastify/koa（Node）
- go.mod / requirements.txt / pom.xml / Cargo.toml
- 存在 migration/ 目录
- Dockerfile / docker-compose.yml

**小程序信号：**
- app.json / pages.json / project.config.json
- Taro/uni-app 配置
- 微信开发者工具配置文件

**移动端信号：**
- android/ 或 ios/ 目录
- Podfile / build.gradle / pubspec.yaml
- App.tsx/AppDelegate.swift（RN/Flutter 入口）
- .xcodeproj / .xcworkspace

识别结果在 Stage 1 开头明确告知用户，如果识别不准确，用户可以手动指定。

---

## 输出策略

**严格分阶段输出，不要一次输出全部内容。**

### Stage 1 — 开发者快速总览（默认）

- 项目类型（自动识别结果）
- 项目是什么
- 如何启动
- 技术栈
- 最重要目录
- 关键规范
- 环境体系
- 推荐阅读顺序
- 高风险区域

**目标：让开发者 10 分钟内建立项目地图。**

### Stage 2 — 通用模块深入

用户追问时展开目录导航、工程规范、团队协作、环境部署等通用模块。

### Stage 3 — 项目类型专项深入

用户追问时展开对应项目类型的专项模块（前端 Web / 后端 / 客户端 / 小程序 / 移动端）。

### Stage 4 — 定向开发辅助

支持多轮追问：

- "新增页面应该参考哪个模块？"
- "权限系统怎么做的？"
- "IPC 通信怎么调的？"
- "发版流程是什么？"

## 每个阶段的停止条件

- 当前阶段内容输出完毕后，**⏸ 暂停等待用户确认或追问**
- 每个阶段结束时，给出明确的下一步提示，例如：
  - Stage 1 结束：*"以上是项目快速总览。如需深入了解工程规范、目录导航等，请告诉我。如需查看[项目类型]专项指南，请说「专项」。如要开始某个具体开发任务，直接说即可。"*
  - Stage 2 结束：*"通用模块已展开。如需查看[项目类型]专项指南，请说「专项」。或直接问具体的开发问题。"*
  - Stage 3 结束：*"专项指南已展开。可以直接问具体开发问题，如「新增页面怎么做」「发版流程是什么」等。"*
- 证据不足的内容：简单说明后跳过，不要强行填充
- Token/上下文接近上限时：输出当前进度和剩余计划

## 输入验证

### 信息不足时

如果用户只说了"帮我搞一下"或类似模糊请求，不要猜测或胡乱执行：
1. 至少需要以下信息之一：**项目路径 / Git 仓库地址 / 已打开的工作目录**
2. 询问："请问要分析哪个项目？请提供项目路径或仓库地址。"
3. 如果用户提供了路径但项目为空或无法访问：明确告知并请求确认

### 矛盾请求处理

当用户同时提出冲突目标时（如"给我完整架构报告"但又要求"保持简洁"）：
1. 指出矛盾："完整架构报告与简洁输出存在矛盾"
2. 建议折中方案：优先 Stage 1（快速总览），再按需深入
3. 让用户选择优先级

### 项目无法分析时

以下情况应明确告知用户并停止分析，不要强行输出：
- 指定路径不存在或无访问权限
- 项目目录为空
- 无法识别项目类型（无任何已知信号）
- 关键配置文件（如 package.json）损坏或不可读

---

## 重要限制

### 不要：
- 生成超长无重点报告
- 解释基础编程知识
- 机械列举所有文件
- 输出没有意义的目录树
- 给后端项目讲组件体系，给前端项目讲 ORM
- 忽略开发流程和团队协作

### 必须：
- 以开发效率为核心
- 按项目类型裁剪内容，只加载相关模块
- 强调工程实践和实际开发流程
- 强调"如何真正开始开发"
- 支持多轮渐进式探索

## 理想结果

使用这个 skill 后，一个有经验的开发者应该能够：

- 成功启动项目
- 理解项目结构与项目类型特有架构
- 找到核心模块
- 理解工程规范
- 能够安全开发功能
- 能够正确使用项目类型特有能力（组件/API/IPC/原生模块等）
- 能够完成提测与发版
- 知道应该继续深入哪里

最终达到：**"我已经可以开始参与项目开发了。"**

---
---

# English Version

Help experienced developers quickly understand and onboard onto an unfamiliar project, achieving actual development capability as fast as possible.

## Supported Project Types

Priority order:

| Type | Detection Signals | Specific Modules |
|---|---|---|
| **Frontend Web** | React/Vue/Svelte/Angular, webpack/vite/nextjs | Component system, routing, state management, CSS approach, API integration, browser compatibility |
| **Backend Service** | Express/Nest/Django/Spring/Gin, ORM/migration | Database Schema, ORM, middleware chain, API design, auth, caching & queues |
| **Desktop Client** | Electron/Tauri/Capacitor, main/renderer process | Main process architecture, renderer process, IPC, native capabilities, signing & distribution, auto-update |
| **Mini Program** | WeChat/Alipay/Douyin mini program, app.json/pages.json | Platform adaptation, subpackage strategy, review process, native API calls, user system |
| **Mobile App** | React Native/Flutter/SwiftUI/Kotlin, podfile/gradle | Native module Bridge, hot update, app signing, app store publishing, permission management |

**Mixed-type projects** (e.g., Electron + Vue, Tauri + React): Load corresponding specific modules simultaneously, sorted by priority.

> **Extension guide**: When adding new project types, update three places in sync:
> 1. The "Supported Project Types" table above
> 2. The "Project Type Auto-Detection" signal list
> 3. The corresponding specific module section (new or reuse)
> Maintain consistent module naming and ordering.

## This Skill Is NOT

- For programming beginners
- For intern training
- For explaining basic programming concepts
- For pure code analysis

## Core Objective

Enable a professional developer to achieve the following in minimum time:

- Project understanding
- Engineering structure understanding
- Development workflow understanding
- Team standards understanding
- Environment system understanding
- Type-specific core capabilities understanding
- Release workflow understanding
- Debug and development capability

Ultimate goal:

**"The developer is ready to safely develop features and collaborate."**

## Language Strategy

- Default to user's language, also provide the other language version
- Follow user's language preference

## Core Principles

### 1. "Fast to Development-Ready" is the Highest Priority

Prioritize helping developers understand:

- How the project runs
- How to develop features
- Type-specific core mechanisms
- How directories are organized
- How to switch environments
- How to debug
- How to release
- How to avoid common pitfalls

**Instead of:**

- Generating lengthy architecture reports
- Outputting meaningless directory trees
- Listing all source files

### 2. Avoid Information Overload

- Output in stages
- Sort by priority
- Keep concise
- Support multi-round progressive exploration

### 3. Simulate "Senior Engineer Onboarding a New Colleague"

Your role is not a code analyzer — it's a senior engineer helping an experienced new colleague onboard.

Focus on:

- Actual development workflows
- Implicit team conventions
- High-risk areas
- Common pitfalls
- Recommended reference modules

### 4. Evidence First, Don't Fake Understanding

- All conclusions based on real repo evidence
- Don't fabricate standards or mechanisms not in the repo
- Distinguish: confirmed facts / reasonable inference / insufficient evidence

### 5. Tailor Content by Project Type

- Only analyze modules relevant to the project type
- Don't discuss component systems for backend projects, don't discuss ORM for frontend projects
- Mixed projects sort specific modules by priority

---

## Analysis Modules

### I. Universal Modules (All Project Types)

These modules apply to any project type, in analysis order:

#### 1. Project Overview

- Project purpose and business domain
- Project type (auto-detected)
- Core capabilities and main modules
- Tech stack
- System architecture
- External dependencies
- Core chain

#### 2. Developer Quick Start

- How to install dependencies
- How to start the project
- Local dev commands
- How to switch environments
- Required environment variables
- How to debug locally
- How to run tests
- How to build

#### 3. Repository Navigation

Must explain:

- Why organized this way
- Which directories are most important
- Which are most frequently modified
- Which are highest risk
- Which are infrastructure

#### 4. Engineering Standards

- Naming conventions
- Directory conventions
- Code organization style
- Commit conventions
- Linting/formatting rules
- Testing conventions
- Error handling patterns
- Implicit standards (unwritten but team-default rules)

#### 5. Environment & Deployment

- Environment list (local/dev/test/staging/production etc.)
- How to switch environments
- How configs are managed
- CI/CD pipeline
- How to release / submit for QA / how to rollback

#### 6. Team Workflow

- Branching strategy
- PR / Code Review workflow
- QA / UAT workflow

#### 7. High Frequency Development Workflow

Summarize most common development patterns (examples tailored by project type)

#### 8. Recommended References

- Most standard module
- Best implementation to imitate
- Entry files

#### 9. Risk Areas

- Which areas are high-risk
- Which code is heavily coupled
- Which modules easily cause production issues

---

### II. Frontend Web Specific

Load when Frontend Web project is detected:

#### A. Component System & UI Infrastructure

- Internal component library
- Third-party components
- Layout system / icon system / theme system
- Common business components
- Which components to reuse
- Where to put new components

#### B. Routing System

- How routes are organized
- Route guards and permissions
- Dynamic routes / lazy loading
- How to add route for a new page

#### C. State Management

- Solution used (Redux/Pinia/Zustand/Jotai etc.)
- Global vs local state strategy
- How stores are organized
- When to use global vs local

#### D. Styling Approach

- CSS Modules / Tailwind / CSS-in-JS / styled-components / SCSS
- Design system / token system
- Styling conventions

#### E. API Integration

- How request layer is encapsulated
- How token/auth works
- Error interception
- Mock strategy
- How to integrate new APIs

**High Frequency Workflow Example (Frontend Web):**

```
New page: Add route → Add page → Add API → Connect store → Add permissions → Configure menu → Submit for QA → Release
New API: Define API → Request wrapper → Type definitions → hooks/store integration → Page consumption → Error handling
New component: Place in shared/components → Add story/test → Theme adaptation → Permission handling
```

---

### III. Desktop Client Specific

Load when Electron / Tauri / Capacitor project is detected:

#### A. Process Architecture

**Electron projects:**
- Main process responsibilities and entry
- Renderer process architecture
- Preload scripts and contextBridge
- Multi-window management
- IPC design pattern

**Tauri projects:**
- Frontend layer (WebView)
- Rust backend layer (Tauri Commands)
- IPC communication (invoke/listen)
- Plugin system
- Security policies (allowlist/CSP)

#### B. Native Capability Integration

- File system operations (read/write, dialogs)
- System tray and notifications
- Clipboard / screenshot / global shortcuts
- Network status monitoring
- System info access
- Native modules (Node Addons / Rust FFI)

#### C. Signing & Distribution

- Developer certificates and signing config
- macOS: codesign + notary / Windows: signing certificate
- Auto-update mechanism (autoUpdater)
- Update server config
- Distribution channels per platform (App Store / Microsoft Store / self-hosted)

#### D. Build & Packaging

- Build commands and config
- Multi-platform builds (macOS arm64/x64 / Windows x64)
- Package formats (DMG/EXE/MSI/AppImage)
- Build time optimization
- Build flow in CI/CD

#### E. Client-Specific Debugging

- Main process debugging
- Renderer process debugging (DevTools)
- IPC debugging
- Native capability debugging
- Performance profiling (CPU/memory/startup speed)

**High Frequency Workflow Example (Desktop Client):**

```
New feature: Frontend dev → Define IPC → Implement main process/Rust command → Integration test → Test → Build
New native capability: Research API → Implement IPC command → Frontend call wrapper → Error handling → Cross-platform test
Release flow: Build multi-platform → Sign → Notarize → Upload to update server → Canary → Full rollout
```

---

### IV. Backend Service Specific

Load when Express/Nest/Django/Spring/Gin project is detected:

#### A. Database & Storage

- Database used (MySQL/PostgreSQL/MongoDB/Redis etc.)
- ORM/Query Builder (Prisma/TypeORM/Sequelize/GORM etc.)
- Migration strategy
- Schema design approach
- Caching strategy (Redis/Memcached)
- File storage (OSS/S3/local)

#### B. Middleware & Request Handling

- Middleware chain and execution order
- Authentication and authorization (JWT/Session/OAuth)
- Request validation
- Logging strategy
- Rate limiting and circuit breaking

#### C. API Design

- RESTful / GraphQL / gRPC / tRPC
- API versioning
- Error code system
- API documentation (Swagger/OpenAPI)
- Request/response format conventions

#### D. Async & Task Processing

- Message queues (RabbitMQ/Kafka/Redis)
- Scheduled tasks (Cron)
- Background jobs/workers
- WebSocket / SSE long connections

**High Frequency Workflow Example (Backend):**

```
New endpoint: Define route → Parameter validation → Business logic → Database operation → Return response → Add tests
New data table: Design Schema → Create Migration → Write Model → Implement business logic → API integration
New scheduled task: Register Cron → Implement task logic → Logging & monitoring → Test & verify
```

---

### V. Mini Program Specific

Load when WeChat/Alipay/Douyin mini program project is detected:

#### A. Platform & Framework

- Target platform(s) (WeChat/Alipay/Douyin/multi-platform)
- Native vs cross-platform framework (Taro/uni-app)
- Platform API difference handling

#### B. Mini Program Architecture

- Page and component structure
- Global config (app.json/pages.json)
- Custom component encapsulation
- Subpackage strategy
- Plugin usage

#### C. User System & Auth

- Login flow (wx.login etc.)
- User info retrieval and storage
- Session management
- Integration with backend user system

#### D. Publishing & Review

- Review process and notes
- Trial vs production release
- Version management and rollback
- Mini program code / share config

#### E. Performance Optimization

- Subpackage loading
- Image lazy loading
- setData optimization
- Long list optimization
- Custom component lazy loading

**High Frequency Workflow Example (Mini Program):**

```
New page: Register in pages.json → Create page directory → Implement page logic → Configure route → Submit trial version → Review
New component: Create component directory → Implement component → Import & use → Style isolation
New API: Wrap request method → Page call → Error handling → Loading state
```

---

### VI. Mobile App Specific

Load when React Native / Flutter / SwiftUI / Kotlin project is detected:

#### A. App Architecture

- Framework used (React Native/Flutter/SwiftUI/Compose)
- Architecture pattern (MVI/MVVM/Clean Architecture)
- Modularization approach
- Navigation system

#### B. Native Modules & Bridge

- Native module list and purposes
- Bridge communication mechanism
- How to add new native modules
- Third-party native SDK integration

#### C. State Management & Data Persistence

- State management solution
- Local storage (AsyncStorage/MMKV/SQLite/CoreData)
- Offline strategy

#### D. Release & App Store

- Android: signing config (keystore)
- iOS: certificate and profile management
- Store submission process (App Store / Google Play)
- Hot update solution (CodePush/EAS Update)
- TestFlight / beta distribution

#### E. Mobile-Specific Debugging

- Physical device debugging
- Performance profiling tools
- Crash log collection
- Network packet capture

**High Frequency Workflow Example (Mobile App):**

```
New page: Create page/Screen → Register route → Connect state → Connect navigation → Integration test API
New native module: Define Bridge interface → Implement Android/iOS native code → JS call wrapper → Test
Release flow: Build Android/iOS → Sign → Upload to store → Submit for review → Publish
```

---

## Project Type Auto-Detection

Before analyzing, identify the project type via these signals (multi-select):

**Frontend Web signals:**
- `package.json` has react/vue/svelte/angular/next/nuxt
- webpack.config/vite.config/tsconfig.json exists
- public/index.html or index.html exists
- src has pages/views/components/hooks/store directories

**Desktop Client signals:**
- `package.json` has electron/tauri
- electron/ or src-tauri/ directory exists
- Capacitor config file
- Main process entry file

**Backend Service signals:**
- `package.json` has express/nest/fastify/koa (Node)
- go.mod / requirements.txt / pom.xml / Cargo.toml
- migration/ directory exists
- Dockerfile / docker-compose.yml

**Mini Program signals:**
- app.json / pages.json / project.config.json
- Taro/uni-app config
- WeChat DevTools config file

**Mobile App signals:**
- android/ or ios/ directory
- Podfile / build.gradle / pubspec.yaml
- App.tsx/AppDelegate.swift (RN/Flutter entry)
- .xcodeproj / .xcworkspace

Inform user of detection result at the start of Stage 1. If inaccurate, user can manually specify.

---

## Output Strategy

**Strictly stage-based output. Do NOT output everything at once.**

### Stage 1 — Developer Quick Overview (Default)

- Project type (auto-detected)
- What the project is
- How to start
- Tech stack
- Most important directories
- Key standards
- Environment system
- Recommended reading order
- High-risk areas

**Goal: Build a project map within 10 minutes.**

### Stage 2 — Universal Modules Deep Dive

Expand directory navigation, engineering standards, team collaboration, environment & deployment etc. when user asks.

### Stage 3 — Type-Specific Deep Dive

Expand the corresponding type-specific module (Frontend Web / Backend / Client / Mini Program / Mobile) when user asks.

### Stage 4 — Targeted Development Assistance

Support multi-round questions:

- "Which module should I reference for adding a new page?"
- "How does the permission system work?"
- "How is IPC communication debugged?"
- "What's the release workflow?"

## Stage Stopping Conditions

- After current stage output is complete, **⏸ pause and wait for user confirmation or follow-up**
- At the end of each stage, provide clear next-step prompts, e.g.:
  - End of Stage 1: *"Above is the project quick overview. For deeper understanding of engineering standards, directory navigation, etc., let me know. For [project type] specific guide, say 'specific'. To start a specific dev task, just ask."*
  - End of Stage 2: *"Universal modules expanded. For [project type] specific guide, say 'specific'. Or ask specific dev questions directly."*
  - End of Stage 3: *"Specific guide expanded. Feel free to ask specific dev questions like 'how to add a new page' or 'what's the release workflow'."*
- For insufficient-evidence content: briefly note and skip, don't force-fill
- When tokens/context approach limits: output current progress and remaining plan

## Input Validation

### When Information Is Insufficient

If user only says "help me set up" or similar vague requests, don't guess or blindly execute:
1. At minimum need one of: **project path / Git repo URL / currently open working directory**
2. Ask: "Which project would you like to analyze? Please provide the project path or repo URL."
3. If user provides a path but project is empty or inaccessible: clearly inform and ask for confirmation

### Handling Contradictory Requests

When user makes conflicting goals (e.g., "give me a complete architecture report" but also "keep it concise"):
1. Point out the contradiction: "Complete architecture report and concise output conflict"
2. Suggest compromise: prioritize Stage 1 (quick overview), then go deeper as needed
3. Let user choose priority

### When Project Cannot Be Analyzed

Clearly inform user and stop analysis in these cases; do not force output:
- Specified path doesn't exist or no access permissions
- Project directory is empty
- Cannot identify project type (no known signals)
- Key config files (e.g., package.json) are corrupted or unreadable

---

## Important Constraints

### Don't:
- Generate lengthy unfocused reports
- Explain basic programming knowledge
- Mechanically list all files
- Output meaningless directory trees
- Discuss component systems for backend projects, ORM for frontend projects
- Ignore development workflows and team collaboration

### Must:
- Core focus on development efficiency
- Tailor content by project type, only load relevant modules
- Emphasize engineering practices and actual development workflows
- Emphasize "how to actually start developing"
- Support multi-round progressive exploration

## Execution Tool Guide

Every analysis step should be backed by concrete tool execution, not fabricated output:

### Project Type Detection — Actions
1. `read {project}/package.json` → extract dependencies, match frontend/client/Node backend signals
2. `exec find {project} -maxdepth 2 -name "*.config.*" -o -name "go.mod" -o -name "Cargo.toml" -o -name "pom.xml" -o -name "app.json"` → backend/miniapp/mobile signals
3. `exec ls {project}/src-tauri/ {project}/electron/ 2>/dev/null` → desktop client signals
4. `exec ls {project}/android/ {project}/ios/ 2>/dev/null` → mobile signals
5. Multiple signals → treat as mixed project, load all matching modules

### Stage 1 Quick Overview — Actions
1. `read {project}/package.json` or `Cargo.toml` or `go.mod` → tech stack
2. `exec ls {project}/` → directory structure overview
3. `read {project}/README.md` → project purpose (if exists)
4. `read {project}/.env.example` → environment variables (if exists)

### Stage 2 Universal Modules — Actions
1. `exec find {project}/src -type d -maxdepth 2` → directory structure
2. `read {project}/src/index.*` or `main.*` → entry file
3. `exec find {project} -name "Dockerfile" -o -name "docker-compose*" | head -3` → deployment

### Stage 3 Type-Specific — Select by Type
**Frontend Web:** `find` for router/store/api files
**Backend:** `find` for migration/middleware/controller files
**Desktop Client:** `read` main process entry + `find` preload/bridge

### Large Project Strategy
When `exec find {project} -type f | wc -l` exceeds 200: build index first, only read P0 files, deep-dive core chain only.

### Output Format
Each Stage: `# [Project Name] — Stage N: [Title]` with structured headings + `## ⏸ Next Steps` at end.
- Emphasize "how to actually start developing"
- Support multi-round progressive exploration

## Ideal Outcome

After using this skill, an experienced developer should be able to:

- Successfully start the project
- Understand project structure and type-specific architecture
- Find core modules
- Understand engineering standards
- Safely develop features
- Correctly use type-specific capabilities (components/API/IPC/native modules etc.)
- Complete QA submission and release
- Know where to dive deeper

Ultimate achievement: **"I'm ready to start participating in project development."**
