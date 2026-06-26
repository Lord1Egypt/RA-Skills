---
name: milb-email
description: 军工采购（军采）商机专用推报工具。汇总三大军采平台数据，生成 Excel 并通过 SMTP 发送邮件报告。与政府采购（政采）工具无关，仅处理军队采购渠道。当用户说"milb-email"、"军工商机邮件"、"推送军工商机"、"军工商机通报"时触发。注意：这不是通用邮件客户端，仅用于执行 milb 业务逻辑。
metadata: {"openclaw":{"emoji":"📧","requires":{"bins":["milb-email","milb-fetcher"]},"install":"pip install -e {baseDir}"}}
---

# Milb Email

自动抓取商机并发送邮件报告。

## 环境变量要求

该技能必须在 `.env` 中配置以下核心参数才能激活：

- `EMAIL_TO`, `EMAIL_CC`, `EMAIL_FROM`: 收发件地址
- `EMAIL_SMTP_HOST`, `EMAIL_SMTP_PORT`: SMTP 服务器信息
- `EMAIL_SMTP_USER`, `EMAIL_SMTP_PASSWORD`: 认证信息
- `EMAIL_SUBJECT_PREFIX`, `EMAIL_BODY_INTRO`: 邮件模板配置
- `EMAIL_RECIPIENT_NAME`, `EMAIL_SENDER_NAME`: 称呼和签名

## 快速使用

- `/milb-email` → 发送昨日报告（默认，解决军队采购网白天更新的问题）
- `/milb-email --help` → 显示帮助信息
- `/milb-email --today` → 发送今日报告（获取各渠道最新数据）
- `/milb-email --date 2026-03-23` → 发送指定日期报告
- `/milb-email --keywords "模型,仿真"` → 使用自定义关键词筛选
- `/milb-email --to test@example.com` → 测试发送至指定收件人

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 无参数 | 默认昨日 | 启用 |
| `--today` | 今日（获取各渠道最新数据） | - |
| `--date YYYY-MM-DD` | 指定日期 | - |
| `--keywords WORDS` | 关键词，逗号分隔 | 配置中的默认关键词 |
| `--to ADDRESS` | 测试发送至指定收件人 | .env 中的配置 |

## 数据源

- 全军武器装备采购信息网
- 军队采购网
- 国防科大采购信息网

## 触发词

发送邮件、推送报告、邮件通知、商机通报

## 配置文件

配置文件位于 `milb_email/.env`（独立配置），可配置以下参数：

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

创建配置文件可复制 `milb_email/.env.example` 为 `milb_email/.env` 后修改。

## 技术说明

- 数据来源：全军武器装备采购信息网、军队采购网、国防科大采购信息网（均为军采渠道，非政采）
- 使用 SMTP 直接发送邮件（配置 EMAIL_SMTP_* 环境变量）
- 使用文件锁防止并发执行
