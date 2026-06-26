---
name: feishu-setup
version: 1.0.0
description: >
  飞书（Feishu/Lark）全套能力接入配置向导。引导用户完成 lark-cli 安装、应用授权、
  用户身份登录、权限续期设置，打通文档、多维表格、日历、消息、邮件、PPT、妙记、OKR、
  知识库、审批等全部飞书能力。
  Use when: 用户说"帮我接入飞书"、"配置飞书"、"打通飞书"、"飞书授权"、
  "lark-cli 配置"、"飞书 CLI 安装"、"飞书 token 过期"、"飞书重新授权"。
---

# feishu-setup — 飞书全套能力接入向导

## 概述

本 Skill 引导完成飞书 lark-cli 的完整配置，打通以下能力：

| 模块 | 覆盖功能 |
|------|---------|
| 文档 | 创建、读取、编辑、评论、导入导出 |
| 多维表格 | 数据表、字段、记录、视图、仪表盘 |
| 电子表格 | 读写、公式、格式 |
| 幻灯片 PPT | 创建、编辑 |
| 日历 | 日程、忙闲查询 |
| 消息 | 发消息、群聊管理 |
| 邮件 | 收发、草稿、文件夹 |
| 任务 | 创建、清单、子任务 |
| 知识库 | 空间、节点管理 |
| 妙记 | 搜索、下载 |
| OKR | 目标、进展记录 |
| 审批 | 实例、任务管理 |

---

## Step 0：检查当前状态

**每次执行前先运行，判断从哪一步开始：**

```bash
lark-cli auth status 2>&1
```

解读输出：
- `user.status = "ready"` → 已配置完成，跳到「验证」
- `user.status = "missing"` 且 `tokenStatus = "expired"` → 执行 Step 2（重新登录）
- 命令不存在（command not found）→ 执行 Step 1（安装）
- `user.status = "missing"` 且从未配置过 → 执行 Step 1 → Step 2

---

## Step 1：安装 lark-cli

```bash
# 检查是否已安装
which lark-cli && lark-cli --version

# 未安装则执行（需要 npm 环境）
npm install -g @larksuite/cli --registry https://registry.npmmirror.com
```

安装完成后验证：
```bash
lark-cli --version
# 期望输出：lark-cli/x.x.x
```

> 如果 npm 不可用，引导用户先安装 Node.js：https://nodejs.org

---

## Step 2：用户身份授权（核心步骤）

### 2.1 发起授权（non-blocking 方式）

```bash
lark-cli auth login --domain all --no-wait --json 2>&1
```

**重要**：必须用 `--no-wait --json` 非阻塞方式，拿到 `device_code` 和 `verification_url`。

输出示例：
```json
{
  "device_code": "xxx...xxx",
  "verification_url": "https://accounts.feishu.cn/oauth/v1/device/verify?..."
}
```

### 2.2 生成二维码并展示给用户

```bash
# 在工作目录生成二维码（必须用相对路径）
cd ~/.openclaw/workspace && lark-cli auth qrcode --output ./lark-auth-qr.png "<verification_url>" 2>&1
```

**关键规则**：
- 必须生成二维码图片并展示给用户（用 MEDIA: 或图片附件）
- 同时展示原始链接（用户可手动打开）
- 告知用户：用飞书 App 扫码或浏览器打开链接，用飞书账号登录授权
- 二维码有效期 **10 分钟**，过期需重新执行 2.1

### 2.3 等待用户确认完成授权

告知用户授权完成后回复「完成」或「好了」，然后执行：

```bash
lark-cli auth login --device-code <device_code> 2>&1
```

### 2.4 验证授权结果

```bash
lark-cli auth status 2>&1 | head -20
```

期望：`user.status = "ready"`，`tokenStatus = "valid"`

> **注意**：如果提示 `profile:user_profile:read` scope 未授予，属于企业管控限制，不影响正常使用，忽略即可。

---

## Step 3：设置自动续期 Cron

Refresh token 有效期 **7 天**，需要定期刷新避免失效。

使用 OpenClaw cron 工具创建每周自动续期任务：

```
每周一 09:00 自动执行 lark-cli auth refresh
```

Cron job 配置参数：
- `schedule.kind`: "cron"
- `schedule.expr`: "0 9 * * 1"
- `schedule.tz`: "Asia/Shanghai"
- `payload.kind`: "agentTurn"
- `payload.message`: 见下方模板
- `sessionTarget`: "isolated"
- `delivery.mode`: "announce"

**payload.message 模板**：
```
请执行以下命令刷新飞书 lark-cli 用户授权 token：

lark-cli auth refresh --json

执行完成后，检查输出中 user.status 是否为 ready，并将结果简要汇报。
如果失败，通知用户需要重新手动授权（执行 lark-cli auth login --domain all --no-wait --json 重新走授权流程）。
```

---

## Step 4：功能验证

授权完成后，用以下命令快速验证各模块是否正常：

```bash
# 验证日历（最快）
lark-cli calendar +agenda 2>&1 | head -10

# 验证文档列表
lark-cli drive +list 2>&1 | head -10

# 验证邮件
lark-cli mail +messages --page-size 3 2>&1 | head -10
```

全部返回数据（非报错）即为成功 ✅

---

## 常见问题处理

### 问题1：token 过期（expired）

```bash
# 尝试自动刷新
lark-cli auth refresh --json 2>&1
```

- 成功 → 完成
- 失败（refresh token 也过期）→ 重走 Step 2

### 问题2：权限不足（permission denied）

错误响应中会包含：
- `permission_violations`：缺少的 scope
- `console_url`：飞书开发者后台链接

解决方案：
- **User 身份**：重新执行 `lark-cli auth login --domain all` 重新授权
- **Bot 身份**：将 `console_url` 发给用户，让管理员在开发者后台开通对应 scope

### 问题3：代理环境警告

```
[WARN] proxy detected: HTTPS_PROXY=...
```

这是正常提示，不影响使用，忽略即可。

### 问题4：版本过期

```bash
lark-cli update 2>&1
```

升级完成后重新验证授权状态。

### 问题5：二维码生成路径报错

必须使用相对路径：
```bash
# 错误 ❌
lark-cli auth qrcode --output /tmp/qr.png "..."

# 正确 ✅
cd ~/.openclaw/workspace && lark-cli auth qrcode --output ./lark-auth-qr.png "..."
```

---

## 执行流程总结

```
检查状态（Step 0）
    ↓
已安装？ → No → 安装 lark-cli（Step 1）
    ↓ Yes
已授权？ → No → 发起授权 → 生成二维码 → 等用户扫码 → 完成授权（Step 2）
    ↓ Yes
设置自动续期 Cron（Step 3）
    ↓
功能验证（Step 4）
    ↓
完成 ✅ 告知用户已打通的飞书能力清单
```

---

## 完成后告知用户

配置完成后，向用户确认以下能力已就绪，可直接使用：

- 📄 **文档**：创建/读取/编辑/评论云文档
- 📊 **多维表格**：全套数据操作
- 📅 **日历**：查看/创建日程
- 💬 **消息**：发送/搜索消息
- 📧 **邮件**：收发邮件
- 📝 **PPT**：创建和编辑幻灯片
- 🎙️ **妙记**：搜索和下载会议纪要
- ✅ **任务**：创建和管理任务
- 📚 **知识库**：管理 Wiki 节点
- 🎯 **OKR**：查看和更新目标进展
- ✍️ **审批**：处理审批实例
