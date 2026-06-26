---
name: govb-email
description: 政府采购商机专用推报工具。根据商机数据自动生成 Excel 并通过 SMTP 发送邮件。当用户说"govb-email"、"政府采购商机邮件"、"推送政府采购商机"、"政采商机通报"时触发。注意：这不是通用邮件客户端，仅用于执行 govb 业务逻辑。
metadata: {"openclaw":{"emoji":"📧","requires":{"bins":["govb-email","govb-fetcher"]},"install":"pip install -e {baseDir}"}}
---

# Govb Email

自动抓取政府采购商机并发送邮件报告。

## 环境变量要求

该技能必须在 `.env` 中配置以下核心参数才能激活：

- `EMAIL_TO`, `EMAIL_CC`, `EMAIL_FROM`: 收发件地址
- `EMAIL_SMTP_HOST`, `EMAIL_SMTP_PORT`: SMTP 服务器信息
- `EMAIL_SMTP_USER`, `EMAIL_SMTP_PASSWORD`: 认证信息
- `EMAIL_SUBJECT_PREFIX`, `EMAIL_BODY_INTRO`: 邮件模板配置
- `EMAIL_RECIPIENT_NAME`, `EMAIL_SENDER_NAME`: 称呼和签名

## 快速使用

- `/govb-email` → 发送昨日报告（默认）
- `/govb-email --help` → 显示帮助信息
- `/govb-email --today` → 发送今日报告
- `/govb-email --date 2026-03-23` → 发送指定日期报告
- `/govb-email --keywords "模型,仿真"` → 使用自定义关键词筛选
- `/govb-email --to test@example.com` → 测试发送至指定收件人

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 无参数 | 默认昨日 | 启用 |
| `--today` | 今日 | - |
| `--date YYYY-MM-DD` | 指定日期 | - |
| `--keywords WORDS` | 关键词，逗号分隔 | govb_fetcher 配置的默认关键词 |
| `--to ADDRESS` | 测试发送至指定收件人 | .env 中的配置 |

## 数据源

- 北京政采（zbcg-bjzc.zhongcy.com）
- 湖南政采（ccgp-hunan.gov.cn）

## 触发词

发送邮件、推送报告、邮件通知、政采商机通报

## 配置文件

配置文件位于 `~/.config/govb-email/.env`，可配置以下参数：

| 环境变量 | 用途 |
|----------|------|
| `EMAIL_TO` | 收件人，逗号分隔 |
| `EMAIL_CC` | 抄送人，逗号分隔 |
| `EMAIL_FROM` | 发件人 |
| `EMAIL_RECIPIENT_NAME` | 收件人称呼 |
| `EMAIL_SENDER_NAME` | 发件人签名 |
| `EMAIL_SUBJECT_PREFIX` | 邮件主题前缀 |
| `EMAIL_BODY_INTRO` | 邮件正文开头 |
| `EMAIL_SMTP_HOST` | SMTP 服务器 |
| `EMAIL_SMTP_PORT` | SMTP 端口 |
| `EMAIL_SMTP_USER` | SMTP 用户名 |
| `EMAIL_SMTP_PASSWORD` | SMTP 密码 |

创建配置文件可复制 `.env.example` 为 `~/.config/govb-email/.env` 后修改。

## 技术说明

- 使用 SMTP 直接发送邮件（配置 EMAIL_SMTP_* 环境变量）
- 使用文件锁防止并发执行
