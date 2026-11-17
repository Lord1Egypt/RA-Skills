---
name: invoice-auto-forward
description: 自动扫描邮箱（支持 QQ/163/126 等主流邮箱，provider 一键切换）里的发票邮件，解析发票（PDF/OFD/XML 三种格式）后按标准化模板转发给指定收件人（如财务/行政），支持抬头白名单过滤、定时无人值守运行、发送节奏控制（防反垃圾风控）。对「链接型发票」（邮件只有下载链接、无 PDF 附件，如腾讯云电子发票）也能自动扫描正文链接并下载发票文件（PDF/OFD/XML）后转发。This skill should be used when 用户想把邮箱收到的发票自动转发给他人、设置发票自动归档/报销流程、配置发票转发规则（授权码/收件人/主题模板），或触发词包括：发票转发、发票自动转发、QQ邮箱发票、163邮箱发票、126邮箱发票、链接型发票、OFD发票、XML发票、转发发票给财务、invoice forward。
slug: invoice-auto-forward
displayName: Invoice Auto Forward — 邮箱发票自动转发
version: 1.0.10
python_optional: ["pdfplumber", "pymupdf", "fitz"]
metadata: {"openclaw": {"envVars": [{"name": "INVOICE_FORWARD_CONFIG", "required": false, "description": "自定义 config.json 路径（可选）"}, {"name": "MAIL_USER", "required": false, "description": "登录邮箱，仅用于 CI/临时代跑，优先于 secrets 文件（可选）"}, {"name": "MAIL_AUTH_CODE", "required": false, "description": "IMAP/SMTP 授权码，仅用于 CI/临时代跑，优先于 secrets 文件（可选）"}]}}
---

# Invoice Auto Forward — 邮箱发票自动转发

## 概述

本 skill 引导用户完成一次性配置（邮箱授权码、转发规则、收件人、主题/正文模板），之后即可自动扫描邮箱中的发票邮件，解析 PDF 发票并按统一格式转发给指定人。支持定时无人值守运行与对话手动触发。

- 主脚本：`scripts/invoice_forward.py`（子命令：`setup` / `check` / `scan` / `run` / `parse`）
- 配置模板与全字段说明：`references/config.example.json`
- 排障与授权码获取指引：`references/troubleshooting.md`

## 依赖

- **Python 3.8+**，网络可达邮箱 IMAP/SMTP 服务器
- **首次使用自动安装**（`check --install-deps`，装到当前 Python 环境）：`pdfplumber`（PDF 解析首选）、`pymupdf`（PDF 兜底，二者至少其一）。**OFD / XML 用 Python 内置 `zipfile` + `xml.etree` 解析，无需任何额外依赖。**
- 手动安装等价命令：`pip install pdfplumber pymupdf`
- 可选环境变量：`INVOICE_FORWARD_CONFIG`（自定义 config.json 路径，默认 `~/.workbuddy/invoice-forward/config.json`）

## Setup 引导流程（首次使用，按序执行）

1. **检查依赖**：直接运行 `python3 scripts/invoice_forward.py check --install-deps`——缺少 `pdfplumber`/`pymupdf` 时会自动 pip 安装到当前 Python 环境（执行前向用户说明将安装这两个库）；若用户环境禁止自动安装，改为给出 `pip install pdfplumber pymupdf` 命令让其自行执行。
2. **收集凭证**：向用户询问邮箱地址与 SMTP/IMAP 授权码。QQ 获取路径：网页版 → 设置 → 账号 → POP3/IMAP/SMTP 服务 → 生成授权码；163/126 获取路径：网页版 → 设置 → 开启 POP3/SMTP/IMAP 服务（默认禁用）→ 短信验证 → 生成授权码（详见 references/troubleshooting.md）。这些值与转发规则可**一次性交给 `setup` 子命令**完成（推荐，见下方「一键配置」），它会验证连通性后写入 secrets（chmod 600）+ config.json，无需手工改文件。**授权码只进 secrets 文件，绝不写入 config.json、SKILL.md 或任何 skill 包内文件。**
3. **收集转发规则**（逐项询问，给默认值，允许用户直接回车采用）：
   - 抬头白名单：默认空 = 全部转发；填写后仅转发购买方抬头匹配的发票
   - 扫描天数：默认 7
   - 主题关键词：默认 `["发票"]`
   - 收件人（必填，支持多个）
   - 主题模板：默认 `{item} {amount} {date}`
   - 正文模板：默认含发票号码/日期/抬头/销售方/物品/金额六要素
4. **生成配置**：按 `references/config.example.json` 的结构写入 `~/.workbuddy/invoice-forward/config.json`（用 `setup` 子命令则自动生成）。
5. **验证**：依次执行
   - `python3 scripts/invoice_forward.py check` — 体检全过才继续
   - `python3 scripts/invoice_forward.py scan` — 干跑预览，向用户展示将转发的邮件清单（主题渲染结果），请用户确认
6. **定时任务（可选，引导创建）**：询问用户是否创建定时任务及频率（如每 3 天）。WorkBuddy 环境用 automation 工具创建，任务内容就是执行 `run` 子命令并复述输出；非 WorkBuddy 环境给出 crontab 行。**创建前务必先读「定时任务（无人值守）」章节**——脚本必须落在持久目录，否则可能长期静默失败，该章节提供了可直接复用的 automation prompt 模板与 crontab 行。提醒：创建后核对下次运行时间是否符合预期。
7. **完成汇报**：告知用户配置位置、手动执行方式、如何修改规则。

## 一键配置（setup 子命令，推荐）

把上面步骤 2–5 合并成一条命令：自动合并已有配置、应用你给的参数、交互补缺失项、验证 IMAP/SMTP 连通性，**确认授权码真能用后才写入 secrets（chmod 600）与 config.json**。凭证绝不会写进 config.json。

```bash
python3 scripts/invoice_forward.py setup \
  --user yourname@163.com \         # 登录邮箱；省略 provider 时由域名推导主机
  --provider 163 \                  # qq/163/126/yeah 或域名；可省略，由 --user 域名自动推导
  --auth-code xxxxxxxx \            # IMAP/SMTP 授权码；不传则交互隐藏输入（getpass，不回显）
  --to finance@example.com \        # 转发收件人，多个用空格分隔
  --days 7 \                        # 扫描天数窗口
  --buyer-whitelist "公司A" "公司B" \  # 抬头白名单，空=全部
  --interval 3 --batch-limit 20 \   # 163/126 防反垃圾节奏（QQ 可设 0）
  --fetch-links \                   # 启用链接型发票抓取（默认开）；--no-fetch-links 关闭
  --link-domains myqcloud.com tencent.com \  # 仅下载这些域名后缀的链接（空=全部，靠 PDF 闸门兜底）
  --config ~/.workbuddy/invoice-forward/config.json   # 可放任意路径；默认即此
```

要点：
- **准确性保证**：默认会真实登录 IMAP + SMTP 验证；验证不通过**绝不写 secrets**（config.json 仍会保存，方便重跑）。加 `--no-verify` 可跳过（仅当你确定授权码正确、或离线调试时）。
- **幂等合并**：目标 config.json 已存在时在其基础上合并，不会清空你已有的其他设置。
- **交互兜底**：缺 `--user`/`--auth-code` 等且在终端（tty）下运行时会逐项交互询问；非交互（agent 批处理）则缺项直接报错，提示补参数。
- **域名推导**：不传 `--provider` 时，按 `--user` 域名（如 `163.com`/`126.com`）自动选主机，少记一个参数。
- 写盘后打印配置路径与权限，并提示下一步跑 `check`。

## 日常使用

- **对话手动执行**：用户说"跑一次发票转发"等——先执行 `python3 scripts/invoice_forward.py scan` 向用户展示将发送清单，**用户确认后**再执行 `python3 scripts/invoice_forward.py run` 并复述输出（已发送/跳过/无发票待人工 各几封，含义见下方「输出解读」）。仅当用户明确说"直接发、不用确认"时才跳过 scan 直接 run。
- **指定扫描窗口**：`scan --days 30` / `run --days 30`（默认取 config.json 的 scan.days）。
- **预览不发送**：`python3 scripts/invoice_forward.py scan`（不写状态、不发送，随时可跑）。
- **修改规则**：直接编辑 `~/.workbuddy/invoice-forward/config.json` 后重跑 `check` 验证。
- **调试单张发票**：`python3 scripts/invoice_forward.py parse /path/to/发票.pdf`（或 `.ofd` / `.xml`，自动识别格式）。
- **每日报告**：`run` 会在配置目录生成 `~/.workbuddy/invoice-forward/报告_YYYYMMDD.md`（同一天重跑覆盖），可直接读它复述结果，无需重新解析邮件。

## 输出解读（重要：别把「跳过」当成漏发）

`scan` / `run` 结尾会打印一行汇总，再按类别列出条目。五类状态含义完全不同：

| 标记 | 含义 | 需要人工介入吗 |
|---|---|---|
| ✅ 已发送 / 将发送 | 抬头命中白名单，正常转发 | 否 |
| ⚪ 跳过 | **抬头白名单不匹配**（个人消费票、他人抬头等） | 否——这是正确过滤，**不是漏发** |
| ⚪ 跳过（发票号重复） | 同一张发票被多封邮件重复投递，或已转发过 | 否 |
| ⚠️ 无发票 X — 原因 | 没拿到发票内容：缺 PDF 解析库 / 链接需登录或已过期 / 链接抓取被禁用 | **是** |
| ⚠️ 无发票 X — 解析失败 | 拿到了附件但提取不出购买方名称（版面异常、加密 PDF、非发票附件） | **是** |
| ⏸️ 延后 | 触达 `batch_limit` 单批上限 | 否——下轮自动续跑 |
| ❌ 发送失败 | SMTP 发送报错（收件人被拒、风控拦截等） | **是** |

关键区分：**「跳过」= 脚本已成功解析发票，只是判断抬头不命中而主动不转发**；
「无发票」= 脚本根本没拿到可信的发票内容。两者在代码里是两条独立分支，不会互相掩盖。

**「解析失败」绝不会落到「跳过」**：只要开启了抬头白名单却没提取到购买方名称，一律计入「无发票待人工」。
这条约束是为一次真实事故加的——邮件正文 HTML 以 `<` 开头，被魔数嗅探误判成 XML 发票，
六要素全空导致 4 张本该转发的发票全被记成「跳过」，报告上看不出任何异常。

所以排查"是不是漏了发票"时，要看 **「无发票」和「发送失败」**，而不是「跳过」。

## 定时任务（无人值守）

### ⚠️ 路径第一原则：脚本与配置必须在持久目录

真实事故：曾有人把定时任务指向临时产物目录（如 `output/`）下自制的转发脚本，
该目录被清理后任务**连续静默失败 25 天**——每次运行都报错，却因无人查看汇报而一直没暴露。

因此：

- 定时任务**只指向本 skill 自带的 `scripts/invoice_forward.py`**（位于 skill 安装目录，稳定持久），
  或你确认不会被定期清空的路径；不要指向临时产物目录
- 配置与去重库（默认 `~/.workbuddy/invoice-forward/`）同理——`processed.json` 一旦丢失，
  重跑会重复转发窗口期内的发票
- 换环境或重装后，先跑一次 `check` 确认脚本与配置都在，再启用定时任务

### WorkBuddy automation prompt 参考模板

````
每天 10:30 执行一次发票自动转发（脚本在持久路径，唯一动作就是跑它）：

  <python> <skill_dir>/scripts/invoice_forward.py run --days 7

脚本行为（无需干预）：IMAP 扫描近 7 天主题含「发票」的邮件 → 解析发票文件
（PDF/OFD/XML，无附件时自动抓正文链接）→ 仅当购买方抬头命中白名单时转发
→ 按 Message-ID + 发票号双重去重，已处理不重发。

配置与状态文件（勿改勿删）：
- 配置：~/.workbuddy/invoice-forward/config.json（收件人/抬头白名单/扫描天数都在这里）
- 去重库：~/.workbuddy/invoice-forward/processed.json
- 凭证：~/.workbuddy/secrets/invoice-forward.env（chmod 600；禁止把授权码打印到聊天或日志）
- 每日报告：~/.workbuddy/invoice-forward/报告_YYYYMMDD.md

你的汇报（简短即可）：
- 复述脚本输出：候选几封 / 已发送几封 / 跳过几封 / 无发票待人工几封
- 若有「无发票」条目或脚本报错（授权码失效、网络异常等），逐条列出并提示需人工处理；
  不要把报错静默成成功
- 若脚本或 config 文件不存在，直接汇报「文件缺失：<路径>，需人工处理」后停止，
  不要自己重写脚本或改配置
````

模板里两条硬约束都来自真实事故，别省掉：

- **禁止模型自行重写脚本或改配置**——脚本缺失时应该报给人，而不是让模型"顺手"再造一个
- **禁止把授权码打印到聊天或日志**

### 非 WorkBuddy 环境（crontab）

```bash
# 每天 10:30 跑一次，输出追加到日志
30 10 * * * /usr/bin/python3 /path/to/skills/invoice-auto-forward/scripts/invoice_forward.py run --days 7 >> /tmp/invoice-forward.log 2>&1
```

## 行为与边界

- 去重：按 Message-ID + 发票号双重去重，`run` 重复执行不会重复转发（状态存于 `~/.workbuddy/invoice-forward/processed.json`）。
- **链接型发票（无 PDF 附件）**：邮件没有发票附件时，自动扫描正文链接（HTML 的 href/src + 纯文本 URL，HTML 实体反转义）逐一尝试下载，**仅当最终响应确为发票文件才采用**——支持 PDF / OFD / XML 三种格式（按 Content-Type / Content-Disposition 后缀 / 魔数判定：PDF=`%PDF`、OFD=ZIP 且含 `OFD.xml`、XML=`<?xml` 开头），随后照常解析转发。适用于腾讯云电子发票等"邮件内只有下载链接"的场景（实测：腾讯云用 COS 预签名 URL，无需登录即可下载）。链接均失败才列入"无发票待人工"并注明原因（链接未返回发票文件=可能需登录或链接已过期 / 链接抓取已禁用）。
- **链接抓取安全闸门**：`config.json` 的 `scan` 段可设 `fetch_links`（默认开）、`link_domains`（非空时仅下载这些域名后缀的链接，如 `["myqcloud.com","tencent.com"]`，空=全部）、`link_timeout`（下载超时秒）、`link_max_bytes`（单链接上限字节，默认 25MB）、`link_user_agent`。仅 http(s) 会被下载；字面量私有/环回/链路本地 IP 会被拒绝（SSRF 基础防护）；真正兜底的是"仅接受发票格式响应"——绝不执行下载内容，只保存发票字节。
- 防循环：收件人地址发来的邮件自动排除。
- 发送节奏（防反垃圾风控）：`config.json` 的 `send` 段可设 `interval`（每封最小间隔秒）、`jitter`（额外随机秒上限）、`batch_limit`（单批上限，超出下轮续跑）。QQ 默认 0 即可；163/126 等严格风控邮箱建议 `interval>=3`、`batch_limit<=20`，主题模板建议加 `{invoice_no}` 提升区分度。
- 多邮箱：支持在 `account.provider` 写 `qq`/`163`/`126`/`yeah` 或域名后缀自动选主机；也可直接写 `imap_host`/`smtp_host` 覆盖。网易系（163/126）登录后会自动发 IMAP `ID` 自报身份以绕过 "Unsafe Login" 风控（否则选文件夹会被拒）。
- 凭证安全：secrets 文件 chmod 600；也支持环境变量 `MAIL_USER`/`MAIL_AUTH_CODE` 临时传入（优先级高于 secrets 文件，便于隔离验证 / CI，授权码免落盘）；排查问题时不得把授权码打印到聊天或日志。
- 发送侧记录：QQ 邮箱默认不把 SMTP 发出的邮件存入网页版「已发送」，验证送达以收件方为准（用户可在邮箱设置中开启保存）。

## 回归测试

改动解析逻辑后先跑这个（纯标准库，无需依赖）：

```bash
python3 tests/test_attachment.py
```

覆盖「正文 HTML 误判成发票」「PDF 优先于 XML」「RFC2047 折行编码的中文附件名」等历史事故场景。
判定标准：`scan` 输出的「将发送」数量必须等于真实命中抬头的发票数；若「跳过」数量突然升高且
「无发票」为 0，先怀疑附件识别退化，用 `parse <附件>` 单独验证单个文件。

## 常见问题

优先查阅 `references/troubleshooting.md`（含授权码获取、QQ IMAP 三个实测坑、限流说明、扩展支持 163 等其他邮箱的方法）。
