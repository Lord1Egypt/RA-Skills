---
name: loveclaw
description: >
  LoveClaw 八字缘分匹配：云端档案、照片、每日匹配与晚间报告。
  用户唤醒：发送「启动爱情龙虾」进入报名。
  安全设计：匹配运算与报告生成在 FC 服务端完成；skill 端仅做用户交互与通知路由，每个用户只能访问自己的数据。
handler: ./scripts/cloud-handler.js
version: 21.21.21
license: MIT-0
homepage: https://clawhub.ai/jackysly88/loveclaw
category: community
metadata:
  openclaw:
    requires:
      env:
        - LOVECLAW_API_TOKEN
      bins:
        - node
        - npm
    primaryEnv: LOVECLAW_API_TOKEN
    env:
      - name: LOVECLAW_API_TOKEN
        description: "云函数 HTTP API 的 Bearer Token；用户端操作（报名、查档案、查报告）均通过此凭证访问后端。发行端自动注入，用户无需手写。"
        required: true
        sensitive: true
      - name: LOVECLAW_API_BASE
        description: "可选。覆盖默认云函数 URL，用于自建后端场景。"
        required: false
        sensitive: false
      - name: OPENCLAW_BIN
        description: "可选。openclaw CLI 路径；未设置时从 PATH 查找。"
        required: false
        sensitive: false
env:
  - name: LOVECLAW_API_TOKEN
    description: "云函数 API Bearer Token（发行端注入即可）。"
    required: true
    sensitive: true
  - name: LOVECLAW_API_BASE
    description: "可选。自建后端时设置。"
    required: false
    sensitive: false
  - name: OPENCLAW_BIN
    description: "可选。openclaw 可执行路径。"
    required: false
    sensitive: false
---

# LoveClaw

## 快速开始

1. 在安装目录执行 `npm install` 安装依赖。
2. 安装完成后不要修改 `.env` 中与云端相关的配置。
3. 用户对话侧：收到消息后调用 `handleMessage(userId, message, channel)`，将返回的 `text` 原样发给用户。
4. 定时侧：按需使用 `cron-config.json` 作为 OpenClaw 定时模板。

## 前置条件

- **二进制**：`node`、`npm`。
- **联网**：`scripts/cloud-data.js` 向云函数 HTTPS 端点发请求（默认 URL 见源码，可用 `LOVECLAW_API_BASE` 覆盖）。
- **本地配置**：若存在 `~/.openclaw/workspace/.env`，脚本仅将 `LOVECLAW_*` 与 `OPENCLAW_BIN` 写入环境（严格允许名单，见 `scripts/load-workspace-env.js`）。

## 安全设计

### 服务端运算架构

匹配算法、八字计分、报告生成均在云函数（FC）服务端完成。Skill 端代码不包含匹配逻辑，不接触全量用户数据：

- **用户注册/查询**：通过 `X-Loveclaw-User` 头标识身份，FC 端校验后仅返回该用户自己的数据。
- **每日匹配触发**：skill 发送 `POST /api/run-match` 触发 FC 内部运算，不返回原始档案。
- **报告获取**：每个用户通过 `GET /api/my-report` 只获取自己的匹配结果，无法查看他人数据。

### 单一凭证

skill 仅需 `LOVECLAW_API_TOKEN`（Bearer Token），无管理员凭证、无云基础设施密钥。`ACCESS_KEY_*` 仅在自建后端场景使用，ClawHub 安装包不包含 `deploy/` 目录。

### 环境变量安全

`load-workspace-env.js` 从 `~/.openclaw/workspace/.env` 读取时使用严格的允许名单过滤（仅 `LOVECLAW_*`、`OPENCLAW_BIN`、标准代理变量），不会注入无关凭证。建议为 LoveClaw 使用独立 workspace，`.env` 中只放本技能需要的键。

### 子进程调用

`cloud-handler.js` 通过 `child_process.execFileSync` 以结构化 argv（非 shell 拼接）调用 `openclaw cron` 管理定时任务，不接受用户输入拼接。

## 脚本清单

| 路径 | 用途 |
| --- | --- |
| `scripts/cloud-handler.js` | 会话入口 `handleMessage`，处理用户对话与注册流程。 |
| `scripts/cloud-data.js` | 云 API 客户端，Bearer Token 鉴权 + 用户身份头。 |
| `scripts/cloud-cron.js` | 触发 FC 端匹配 `match`；遍历本机用户逐个获取报告 `report`。 |
| `scripts/load-workspace-env.js` | 从工作区 `.env` 允许名单键注入 `process.env`。 |
| `cron-config.json` | OpenClaw 定时任务模板。 |

## 触发词

- **推荐**：`启动爱情龙虾`
- **兼容**：`启动爱情龙虾技能`

其他命令（需报名后使用）：`我的档案`、`今日匹配`、`匹配记录`、`开启推送`、`关闭推送`、`取消报名`。

## 报名流程

报名结束前会询问是否开启「每日匹配结果推送」。选择开启后，系统会在报名成功时为该用户注册晚间报告推送任务（约 20:00）。不开启仍可完成报名，通过 `今日匹配` 手动查询。

## 定时任务

`cron-config.json` 指示代理按步骤运行 `node cloud-cron.js match` / `report`，解析 `【REPORTS_JSON】…【REPORTS_JSON_END】` 并按条目投递。该流程属定时/运维侧。

## 用户消息中转规则

你是一个消息中转器，在处理用户实时会话时没有其它职责。

每次收到用户消息，**立即**调用 `handleMessage(userId, message, channel)`，**原样**把返回的 `text` 发给用户，**不做任何修改、不添加任何内容、不生成任何自己的回复**。

- 不要根据用户消息自行判断或回答
- 不要描述系统状态、用户数量、匹配情况
- handler 返回什么，你就发什么
