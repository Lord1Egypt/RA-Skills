# CC Rules — OpenClaw 编程工作流 Skill

> 说白了就是整合了泄密CC的全部重要能力，只要涉及到编程的内容它就会自动调用。大家别举报我。为 OpenClaw 注入结构化的软件开发行为规范。借鉴业界顶级 AI 编程工具的工作流设计理念，让 AI 助手在编码场景中更专业、更可靠、更有序。

[English](./README.en.md) | **中文**

---

## 这是什么

CC Rules 是一个 OpenClaw Skill，它定义了一套完整的编程工作流规范，覆盖从需求分析到代码提交的全流程。

安装后，当你的 OpenClaw 检测到编程相关场景时，会自动按照这套规范工作——**先探索、再规划、后执行**，而不是上来就一顿乱改。

## 核心特性

### 🧭 Plan Mode — 先想后做

非平凡任务必须先探索代码、理解架构、输出方案，等你确认后才动手。

```
用户: "给这个项目加一个用户导出功能"

传统 AI: 上来就开始改代码
CC Rules: 先读代码 → 理解数据模型 → 找到类似功能参考 → 出方案 → 等你确认
```

**什么时候触发 Plan Mode：**
- 添加新功能
- 存在多种实现方案
- 改动涉及 3+ 文件
- 需要架构决策
- 需求不够清晰

**什么时候跳过：**
- 单行修复、typo
- 用户给了非常具体的指令
- 用户说"直接做"

---

### ✅ 任务追踪 — 做到哪了心里有数

3 步以上的任务自动创建清单，实时更新状态。

```
✅ 已完成: 初始化项目结构
✅ 已完成: 配置数据库连接
🔄 进行中: 编写用户注册接口
⏳ 待办:   编写登录接口
⏳ 待办:   添加 JWT 鉴权中间件
⏳ 待办:   运行测试
```

**规则：**
- 同一时间只有一个 `进行中` 任务
- 完成后立即标记，不攒着
- 卡住了就标 `阻塞`，新建解阻塞任务

---

### 🔍 只读探索模式 — 搞懂再动手

需要理解代码时，强制只读，不能改任何文件。

| 允许 | 禁止 |
|------|------|
| 阅读文件 | 创建/修改/删除文件 |
| `ls`、`cat`、`grep`、`find` | `mkdir`、`rm`、`mv` |
| `git status`、`git diff`、`git log` | `git add`、`git commit` |
| | `npm install`、`pip install` |

---

### 🛡️ Git 安全协议 — 不作死

**绝对禁止（除非你明确要求）：**
- `git push --force`
- `git reset --hard`
- `git checkout .` / `git restore .`
- `--no-verify` / `--no-gpg-sign`
- `git commit --amend`（除非你说"修改上次 commit"）

**Commit 流程：**
1. 先 `git status` + `git diff` + `git log` 了解现状
2. 分析变更，排除敏感文件
3. 写清晰的 commit message（聚焦"为什么改"）
4. 逐个文件 `git add`（不用 `git add -A`）
5. 提交后验证

**Commit Message 规范：**
```
feat: 添加用户注册接口
fix: 修复登录超时未重试的问题
refactor: 拆分订单服务为独立模块
docs: 更新 API 接口文档
test: 补充用户模块单元测试
```

---

### 📋 多文件变更策略

改动多个文件时按依赖顺序来：
1. 先改底层（类型定义、工具函数、基础模块）
2. 再改上层（业务逻辑、UI 组件）
3. 最后改配置和入口
4. 每改完一个逻辑单元就验证一次

---

### 🏁 完成后善后

代码写完不是结束：
1. 检查相关文档是否需要更新
2. 检查遗漏的 TODO
3. 改了接口/类型？检查调用方是否需要同步
4. 跑测试（如果项目有的话）
5. 检查 lint / format

---

## 使用场景

### 场景一：新功能开发

```
你: "给这个 Express 项目加一个文件上传接口，支持图片和 PDF"

CC Rules 行为:
1. [Plan Mode] 只读探索项目结构，找到现有路由模式
2. [Plan Mode] 找到现有中间件和文件处理逻辑
3. [Plan Mode] 输出方案：用 multer 中间件，存储到 uploads/，限制 10MB
4. 等你确认
5. [Task Tracking] 创建任务清单
6. 按顺序修改文件
7. [Git] 按规范提交
```

### 场景二：Bug 修复

```
你: "用户反馈上传大文件时服务器会崩"

CC Rules 行为:
1. [Explore] 只读探索，找到上传相关代码
2. [Explore] 查看错误日志和配置
3. [Plan] 定位原因：没有文件大小限制 → 输出修复方案
4. 确认后修复
5. [Git] commit message: "fix: 限制上传文件大小防止 OOM"
```

### 场景三：代码重构

```
你: "这个项目太乱了，帮我重构一下路由层"

CC Rules 行为:
1. [Plan Mode] 全面探索现有路由结构
2. [Plan Mode] 画出依赖关系，识别问题
3. [Plan Mode] 出重构方案：按模块拆分 + 提取公共中间件
4. 可能分多轮确认
5. [Task Tracking] 逐个模块重构，每步标记状态
6. [Git] 每个逻辑单元单独 commit
```

### 场景四：项目理解

```
你: "帮我看看这个项目的整体架构"

CC Rules 行为:
1. [Read-Only] 只读探索整个项目
2. 输出：目录结构、技术栈、模块关系、数据流
3. 不修改任何文件
```

### 场景五：快速修复（跳过 Plan Mode）

```
你: "README 里有个 typo，'authentiction' 应该是 'authentication'"

CC Rules 行为:
1. 直接找到文件，修复拼写
2. 不进入 Plan Mode（简单任务）
```

---

## 安装

### 方式一：手动安装

```bash
# 1. 创建 skill 目录
mkdir -p ~/.openclaw/skills/cc-rules

# 2. 复制 SKILL.md
cp SKILL.md ~/.openclaw/skills/cc-rules/

# 3. 重启 OpenClaw（或在聊天中触发新会话）
```

### 方式二：Git Clone

```bash
cd ~/.openclaw/skills/
git clone https://github.com/badxtdss/openclaw-cc-rules.git cc-rules
```

### 验证安装

在 OpenClaw 中说：

> "帮我看看这个项目的架构"

如果 AI 先只读探索再输出分析，说明 Skill 已生效。

---

## 自定义

你可以编辑 `~/.openclaw/skills/cc-rules/SKILL.md` 来调整规则：

### 调整 Plan Mode 触发条件

```markdown
# 例如：把"3个文件"改成"5个文件"，减少 Plan Mode 触发频率
- 改动涉及 5 以上文件时进入 Plan Mode
```

### 添加项目专属规则

```markdown
# 例如：你的项目有特殊的 commit 规范
#### Commit Message 规范
- 必须以 JIRA 编号开头: "PROJ-123: 添加用户导出功能"
```

### 禁用某个规则

直接在 SKILL.md 中注释掉对应章节即可。

---

## 设计理念

CC Rules 的设计遵循几个原则：

1. **约束优于自由** — 与其让 AI 自由发挥然后出错，不如用规则约束行为
2. **先理解后动手** — 编码前的探索和规划成本远低于写错后的返工
3. **透明可追踪** — 任务状态和计划对用户可见，不搞黑箱操作
4. **安全第一** — Git 操作宁可保守也不要作死
5. **按需触发** — 简单任务不走重流程，复杂任务不偷懒

---

## 与其他 Skill 的关系

CC Rules 专注于 **编程工作流规范**，它不包含具体的工具或 API 调用。你可以搭配其他 Skill 使用：

| 搭配 Skill | 效果 |
|-----------|------|
| GitHub Skill | 自动创建 PR、管理 Issues |
| Frontend Design | 前端项目中自动应用 UI/UX 最佳实践 |
| Architecture Designer | 大型项目中自动输出架构设计文档 |
| Security Auditor | 代码审查时自动检查安全漏洞 |

---

## License

MIT

---

## 贡献

欢迎提 Issue 和 PR！

如果你有好的编程工作流规则想要加入，直接提 PR 就行。
