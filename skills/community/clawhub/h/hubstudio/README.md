# HubStudio OpenAPI Skill

这是一个面向 `HubStudio` 本地 API 的技能项目，目标是让你可以用统一方式完成：

- API 能力检索（有哪些接口、每个接口做什么）
- 请求参数校验（必填项、类型、约束）
- 自动化调用（浏览器环境、云手机、账号、分组等）
- 常见问题排查（HTTP 成功但业务失败、环境无法启动等）

项目核心定位：**把 `openapi.yaml` 的接口能力，转成可查询、可执行、可自动化的工程化工具链。**

---

## 项目提供的 Skill 能力

## 1) 全量接口查询能力

- 基于 `openapi.yaml` 提供 HubStudio 全量接口定义
- 当前生成命令总数：`56`（见 `commands.generated.json`）
- 覆盖业务域：
  - 浏览器环境
  - 云手机
  - 环境管理
  - 平台账号管理
  - 分组管理

你可以快速回答类似问题：

- “打开环境接口叫什么？请求体怎么写？”
- “批量开启云手机需要哪些字段？”
- “某接口返回字段 `debuggingPort` 是什么含义？”

---

## 2) 请求/响应字段解释能力

Skill 可以按接口粒度解释：

- 请求参数（query/header/body）
- 必填字段与可选字段
- 字段类型与含义
- 响应 `code/msg/data` 结构

这使得你可以在自动化流程里先做参数检查，再发请求，减少无效调用。

---

## 3) 本地 CLI 执行能力（开箱即用）

项目内置 `hubstudio.js`，可直接调用 HubStudio 本地 API：

```bash
node hubstudio.js help
node hubstudio.js list
node hubstudio.js browserStart 1502764609
node hubstudio.js browserStatus 1502764609
node hubstudio.js browserStop 1502764609
```

也支持生成命令直调：

```bash
node hubstudio.js postV1BrowserStart --body '{"containerCode":"1502764609"}'
```

---

## 4) 浏览器自动化接入能力（Playwright）

项目已提供端到端示例脚本：`playwright_hubstudio_baidu_demo.js`，可完成：

1. 启动 HubStudio 环境
2. 获取 `debuggingPort`
3. 使用 Playwright 通过 CDP 连接该浏览器
4. 打开百度并搜索 `HubStudio`
5. 点击第一条结果并提取正文
6. 生成摘要文件并关闭环境

执行命令：

```bash
node playwright_hubstudio_baidu_demo.js
```

输出结果示例文件：

- `summary_hubstudio_baidu_playwright.txt`

---

## 5) ADB 连接辅助能力（云手机）

项目提供云手机 ADB 连接专项说明：`ADB_CONNECTION_GUIDE.md`，用于：

- 开启 ADB
- 查询连接信息
- 根据 Android 版本选择连接模式
- 验证 `adb devices`

---

## 项目文件说明

- `SKILL.md`：Skill 主说明（使用指引、调用建议、FAQ）
- `openapi.yaml`：HubStudio OpenAPI 源定义
- `reference.md`：从 OpenAPI 生成的本地接口参考文档
- `commands.generated.json`：从 OpenAPI 生成的 CLI 命令映射
- `hubstudio.js`：统一命令行入口（别名 + 生成命令）
- `playwright_hubstudio_baidu_demo.js`：Playwright 端到端自动化示例
- `ADB_CONNECTION_GUIDE.md`：云手机 ADB 接入指南
- `OPENCLAW_AGENT_BROWSER_TUTORIAL.md`：面向新手的实操教程（当前已切换为 Playwright 流程）

---

## 快速开始（建议流程）

### 1. 环境准备

```bash
# 先进入项目根目录（README 所在目录）
cd ./
node --version
openclaw --version
```

### 2. 安装依赖（如需运行 Playwright 示例）

```bash
npm init -y
npm install playwright
```

### 3. 验证 HubStudio API 可用

```bash
node hubstudio.js browserStatus 1502764609
```

若返回 `code: 0` 说明 API 可正常调用。

### 4. 运行示例

```bash
node playwright_hubstudio_baidu_demo.js
```

---

## 安装 HubStudio Skill 到 OpenClaw（详细步骤）

这一节专门说明：如何把当前项目作为一个 Skill 安装到 OpenClaw 并让 OpenClaw 识别。

### 1) 先确认 OpenClaw 已初始化

```bash
openclaw onboard --install-daemon
openclaw gateway status
```

### 2) 创建 OpenClaw 的 workspace skills 目录

```bash
mkdir -p "$HOME/.openclaw/workspace/skills"
```

### 3) 安装方式二选一

#### 方式 A（推荐）：软链接，方便你持续更新

适合开发调试：你修改当前项目文件，OpenClaw 立即读取最新内容。

```bash
ln -sfn "./" "$HOME/.openclaw/workspace/skills/hubstudio"
```

#### 方式 B：复制一份稳定版本

适合“先固定版本再使用”。

```bash
rm -rf "$HOME/.openclaw/workspace/skills/hubstudio"
cp -R "./" "$HOME/.openclaw/workspace/skills/hubstudio"
```

### 4) 让 OpenClaw 刷新技能状态

```bash
openclaw gateway restart
```

### 5) 验证 Skill 是否安装成功

```bash
openclaw skills check
openclaw skills list
openclaw skills info hubstudio-openapi
```

成功时你应看到：

- `hubstudio-openapi` 状态为 `ready`
- 来源显示为 `openclaw-workspace`
- 路径类似：`~/.openclaw/workspace/skills/hubstudio/SKILL.md`

### 6) 安装后建议做一次能力验证

```bash
cd ./
node hubstudio.js list
node hubstudio.js browserStatus 1502764609
```

如果你在 OpenClaw 中调用与 HubStudio API 相关任务时，模型能够命中 `hubstudio-openapi` 这个 skill，即说明集成生效。

---

## 响应判定规范（非常重要）

HubStudio 常见返回结构：

```json
{
  "code": 0,
  "msg": "Success",
  "data": {}
}
```

判定规则：

- `HTTP 200` 不代表业务成功
- 以 `code` 为准：
  - `code = 0`：成功
  - `code != 0`：业务失败（参数、权限、资源状态等）

---

## 典型使用场景

- 批量管理浏览器环境（开关、状态、窗口排列）
- 云手机应用安装/启动/停止自动化
- ADB 开启与连接状态查询
- 将 HubStudio 接口能力接入 OpenClaw/脚本工作流
- 用 Playwright 基于 HubStudio 环境做网页自动化

---

## 常见问题

### 1) 接口返回 200 但任务没成功

请检查返回体中的 `code` 和 `msg`，不要只看 HTTP 状态码。

### 2) 启动环境失败

优先检查：

- HubStudio 客户端是否登录
- 是否开通VIP
- `containerCode` 是否存在且属于当前账号
- 本地服务地址是否是 `http://127.0.0.1:6873` 端口可能存在变动需要检查

### 3) 自动化脚本连接不上浏览器

请确认：

- `browserStart` 后返回了 `debuggingPort`
- 环境未提前关闭
- 本机端口未被拦截

---

## 参考文档

- OpenClaw Getting Started: <https://docs.openclaw.ai/start/getting-started>
- HubStudio API Docs: <https://api-docs.hubstudio.cn/>
- 项目内接口参考：`reference.md`
