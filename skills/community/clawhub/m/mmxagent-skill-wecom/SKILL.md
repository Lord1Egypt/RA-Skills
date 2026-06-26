---
name: mmxagent-skill-wecom
description: 连接企业微信。调用 generate 接口获取授权链接，用户把链接发到企业微信聊天里点开完成授权。用户提到连接企业微信、接入企微、绑定企微机器人、创建企微机器人、扫码绑定企微时使用。
---

# WeCom Connect Skill

## 适用场景

当用户要求连接企业微信、绑定企微机器人、创建新的企微机器人、给 OpenClaw 接入企业微信、或明确提到"扫码绑定企微"时，直接使用本流程。

## 核心原则

- **不生成 PNG，不走 CDN**。generate 拿到 `auth_url` 后直接给用户，用户把链接发到企业微信聊天里点开完成授权。
- **不要自动开轮询**。给完链接等用户说"配好了"再轮询。
- **不要手动卸载/禁用插件**。

## 执行流程（写死，照抄执行）

### 第 1 步：调用 generate 接口

```bash
curl -s "https://work.weixin.qq.com/ai/qc/generate?source=wecom-cli&plat=3"
```

从返回值提取 `scode` 和 `auth_url`。`scode` 留着后面轮询用，`auth_url` 直接给用户。

### 第 2 步：把 auth_url 给用户，等用户回复

```markdown
## 企业微信二维码

复制下面的链接，发到你的企业微信任意聊天里，然后点击打开：

<auth_url>

**操作步骤：**
1. 打开手机上的 **企业微信 App**（不是微信）
2. 随便找一个聊天对话框，把上面的链接通过发消息的方式发过去
3. 点击消息里的链接，在企业微信内打开
4. 在页面中完成授权确认
5. **配置完成后告诉我**

有效期：3 分钟
```

然后**停下来，等用户说"配好了"**。

## 用户确认后：轮询 + 写配置

用户说"配好了 / 扫完了 / done / ok"后：

```bash
curl -s "https://work.weixin.qq.com/ai/qc/query_result?scode=<scode>"
```

轮询间隔 3 秒，超时 3 分钟。成功条件：`data.status === 'success'` 且 `data.bot_info.botid` 和 `data.bot_info.secret` 存在。

拿到后写入 `~/.openclaw/openclaw.json`：

```text
channels.wecom.botId = <botId>
channels.wecom.secret = <secret>
channels.wecom.enabled = true
```

然后 `openclaw gateway restart`。

超时则重新走第 1~2 步。

## 成功回复模板

```markdown
## 企业微信连接结果

- 状态：已绑定成功
- 机器人凭证：已获取（botId: `<botId>`）
- OpenClaw 配置：已写入
- Gateway：已重启
```

## 绝对禁止

- **禁止生成 PNG / 走 CDN / Batch Upload**：直接给 auth_url 链接。
- **禁止自动开轮询**：等用户说"配好了"。
- **禁止手动卸载/禁用插件**。

## 一句话总结

generate → 给用户链接 → 用户发到企业微信聊天里点开授权 → 等用户说"配好了" → 轮询 → 写配置。
