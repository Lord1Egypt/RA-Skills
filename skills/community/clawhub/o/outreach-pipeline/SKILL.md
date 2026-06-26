---
name: outreach-pipeline
description: 邮件外联自动化（批量邮件外联、序列发送、模板合并、节流与送达合规）。当用户要：1) 导入收件人列表（CSV/表格）并批量发送个性化外联邮件；2) 运行简单的邮件序列与跟进；3) 通过 SMTP 或常见 ESP（SendGrid/Mailgun）发送；4) 使用 Gmail/Outlook（OAuth/App Password）发送；5) 需要反垃圾合规、节流与退订处理时，使用本 Skill。
---

# 邮件外联自动化 Skill

本 Skill 提供一套可复用的邮件外联流程与脚本：
- 输入联系人（CSV）
- 使用可读模板（支持 {{变量}} 合并）
- 选择发送提供方（SMTP / SendGrid / Mailgun；Gmail/Outlook 支持见参考）
- 节流（每分钟/每小时限速）、重试与结果日志
- 合规与送达最佳实践（退订语/域名与身份配置）

适用触发语示例（供模型触发参考）
- “邮件外联自动化/发外联邮件/批量发邮件”
- “把这份 CSV 的联系人发一封模板邮件”
- “用 SMTP/SendGrid/Mailgun/Gmail 发外联，注意限流和退订”
- “生成第一封冷启动外联模板并发送”

快速开始
1) 准备数据与模板
- CSV 格式参考：see references/csv-format.md（至少包含 email 列，建议 name/company 等）
- 邮件模板：支持 {{name}}、{{company}} 等占位符（示例见 assets/templates/first-touch.txt）

2) 选择发送方式
- SMTP：配置主机、端口、用户名/密码（或 App Password），支持 STARTTLS
- ESP（SendGrid/Mailgun）：准备 API Key（见 references/templates.md 中的示例与说明）
- Gmail/Outlook：推荐使用 OAuth 或 App Password（见 references/tips.md）

3) 运行脚本（使用 uv 调用 Python）
- 示例（SMTP）：
  uv run python skills/outreach-pipeline/scripts/send.py \
    --csv path/to/contacts.csv \
    --template skills/outreach-pipeline/assets/templates/first-touch.txt \
    --subject "你好 {{name}}，关于{{company}}的合作想法" \
    --from-name "你的姓名" \
    --from-email "you@your-domain.com" \
    --provider smtp \
    --smtp-host smtp.your-domain.com \
    --smtp-port 587 \
    --smtp-user you@your-domain.com \
    --smtp-pass "<PASSWORD>" \
    --rate-limit 15 \
    --out-log out/send_results.csv

- 示例（SendGrid）：
  设置环境变量 SENDGRID_API_KEY 后：
  uv run python skills/outreach-pipeline/scripts/send.py \
    --csv path/to/contacts.csv \
    --template skills/outreach-pipeline/assets/templates/first-touch.txt \
    --subject "Hi {{name}}" \
    --from-name "你的姓名" \
    --from-email "you@your-domain.com" \
    --provider sendgrid \
    --rate-limit 25

4) 查看结果
- 发送过程与每个收件人的状态写入 --out-log 指定的 CSV（默认 send_results.csv）

输入约定
- CSV 标题至少包含：email；可选列将作为模板变量（如 name/company/title 等）
- 模板文件为纯文本或轻度 Markdown，变量格式 {{var}}
- 主题也支持 {{变量}} 合并

核心动作（给调用者的流程指引）
- 校验输入：CSV 列、模板变量、主题变量是否匹配（缺失变量将置为空字符串）
- 发送策略：
  - 节流：--rate-limit（每分钟最多 N 封），避免触发提供方或 ISP 限制
  - 批次控制：--max-per-run 限制本次运行数量；先小批测试（如 10 封）再放大
  - 重试：轻度网络错误可在脚本层面第2次尝试；硬错误记录日志并跳过
- 退订与合规：
  - 模板底部附上退订说明（见 references/risks.md）
  - 优先使用独立域名、正确的 From/Reply-To、SPF/DKIM/DMARC 合规（见 references/tips.md）

提供方说明（摘要）
- SMTP：通用，适合小批量与自有域；需配置 SPF/DKIM 提升送达
- SendGrid/Mailgun：适合批量与稳定送达；使用 API Key；注意速率与信誉
- Gmail/Outlook：建议 App Password 或 OAuth；免费额度有限，节流严格

目录结构
- scripts/send.py — 主脚本（CSV 导入、模板合并、SMTP/ESP 发送、节流、日志）
- references/
  - csv-format.md — CSV 列格式说明与示例
  - tips.md — 送达与账号配置（SPF/DKIM/DMARC、OAuth/App Password）
  - risks.md — 合规、反垃圾与退订建议
  - templates.md — 模板与变量示例、常见序列骨架
- assets/templates/first-touch.txt — 冷启动外联模板示例

注意与限制
- 本 Skill 不提供“邮箱列表抓取/购买”；仅面向有来源与同意基础的 B2B 合法外联
- 法规合规：遵守当地法律（例如 CAN-SPAM/GDPR/各平台政策）；不可群发骚扰邮件
- 初次运行请用自己的邮箱进行自测（3–5 封）确认显示与追踪无误

示例交互
- 用户：“把这份 contacts.csv 的联系人用 SMTP 发一封冷启动外联，速率 10/分钟，主题和正文按模板。”
- 代理：校验 CSV→渲染 3 封样例→提示确认→开始发送→输出日志路径与统计

扩展
- 如需序列化跟进（Day 1/3/7），可用 cron 或外部调度每次调用脚本并传入不同模板与过滤条件。
