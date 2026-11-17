---
name: mail-messenger
description: |
  邮件与消息发送助手。覆盖 SMTP 发信（Gmail / Outlook / QQ / 163 / 企业邮箱）、IMAP 收信检索、以及常见消息通知（Webhook / 企业微信 / 飞书 / 钉钉机器人）。当用户需要"发邮件""通知我""把结果发到邮箱""读取邮件"时调用。
agent_created: true
visibility: "public"
---

# 邮件与消息发送助手

帮助用户通过代码可靠地发送邮件、检索邮件、推送消息通知。核心原则：**凭据永不写死在脚本里，一律走环境变量或参数注入**。

## 适用场景
- 把长文 / 报告 / 生成物作为附件或正文发送到指定邮箱
- 定时任务完成后推送通知（Webhook / 机器人）
- 从邮箱检索特定邮件（按主题 / 发件人 / 日期）
- 多账号、多服务商（Gmail、Outlook、QQ、163）

## 主流邮箱 SMTP 配置速查

| 服务商 | SMTP 主机 | 端口(TLS) | 端口(SSL) | 认证注意 |
|--------|-----------|-----------|-----------|----------|
| Gmail | smtp.gmail.com | 587 | 465 | 需用**应用专用密码**，非账号密码 |
| Outlook/Hotmail | smtp.office365.com | 587 | 465 | 账号密码或 OAuth |
| QQ 邮箱 | smtp.qq.com | 587 | 465 | 需**授权码**（设置→账户→POP3/SMTP）|
| 163 邮箱 | smtp.163.com | 587 | 465 | 需**授权码** |
| 企业微信邮箱 | exmail.qq.com | 587 | 465 | 授权码 |

> ⚠️ 国内邮箱（QQ/163）几乎都要求"授权码"而非登录密码，且需先在网页端开启 SMTP 服务。

## 标准工作流

### 1. 发送邮件
使用 `scripts/smtp_send.py`：
```bash
python scripts/smtp_send.py \
  --to "recipient@example.com" \
  --subject "每日报告" \
  --body "正文内容……" \
  --attach "/path/to/report.pdf" \
  --smtp-host smtp.qq.com --port 465 --user "you@qq.com" --pass "$MAIL_PASS"
```
- 凭据从环境变量 `MAIL_PASS` 注入（不要明文写在命令里）。
- 支持多附件（`--attach` 可重复）。
- HTML 正文加 `--html`。

### 2. 检索邮件（IMAP）
使用 `scripts/imap_fetch.py`：
```bash
python scripts/imap_fetch.py \
  --host imap.qq.com --user "you@qq.com" --pass "$MAIL_PASS" \
  --folder INBOX --since 2026-07-01 --subject "发票" --max 10
```

### 3. 消息通知（机器人 Webhook）
- **企业微信群机器人**：`curl -X POST "$WECOM_WEBHOOK" -H 'Content-Type: application/json' -d '{"msgtype":"text","text":{"content":"任务完成"}}'`
- **飞书**：POST 到飞书自定义机器人 webhook，body 同上结构。
- **钉钉**：webhook 后需加 `&timestamp=&sign=`（加签模式）。

## 质量门禁（发送前自查）
- [ ] 收件人是否误填（生产环境先发给自己验证）
- [ ] 凭据是否走环境变量（绝不落盘到脚本/日志）
- [ ] 大附件是否超服务商单封上限（通常 20~50MB，超限走网盘链接）
- [ ] 正文编码是否 UTF-8（中文乱码预防）

## 自进化学习系统

> 本技能内置 self-improve 闭环：每次发送 / 检索后请用 learner 记录成败与偏好，使越用越稳。

```bash
python scripts/learner.py record . --capability "SMTP发信" [--fail --error <类型> --note <说明>]
python scripts/learner.py insight .
python scripts/learner.py reflect .
```

### 迭代规则
- 同一服务商连续 2 次认证失败 → 记录为 `error=auth`，下次优先提示"检查授权码/应用专用密码"
- 发送成功率低于 0.8 → reflect 建议增加"先发测试信"预检步骤，并回写本文件
- 用户偏好某家服务商 → `prefer` 记录，下次默认选用

## 安全边界
- 绝不读取或发送用户的个人私密邮件内容到外部；涉及隐私邮件时先征求确认
- 凭据仅在内存/环境变量中使用，脚本不写日志、不缓存密码
