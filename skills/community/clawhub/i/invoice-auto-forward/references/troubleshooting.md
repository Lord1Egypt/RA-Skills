# 排障与参考（Troubleshooting）

## 获取 QQ 邮箱授权码

1. 登录 QQ 邮箱网页版（mail.qq.com 或 wx.mail.qq.com）
2. 设置 → 账号 → 找到「POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务」
3. 开启「IMAP/SMTP服务」，按提示短信验证，生成**授权码**（16 位字母）
4. 授权码 ≠ QQ 密码；它同时用于 IMAP 登录与 SMTP 登录

## 常见报错

| 现象 | 原因与处理 |
|---|---|
| `Login failed` / 535 认证失败 | 授权码错填成了 QQ 密码，或授权码已失效 → 重新生成 |
| `未找到配置文件` | 未走 setup 流程；参照 config.example.json 创建 config.json |
| PDF 解析依赖报错 | PDF 发票需要这两个库：`pip install pdfplumber pymupdf`（至少其一，推荐 pdfplumber）；**OFD/XML 用 Python 内置库即可，无需安装** |
| 解析出来字段为空 | 该发票可能是图片型/扫描件（需 OCR，本工具不支持）→ 归入待人工 |
| 无发票待人工：链接均未返回发票文件 | 链接型发票的下载链接需登录（如发票管理控制台页）或已过期（如 30 天有效期的预签名 URL 超时）→ 邮件已自动尝试抓取正文所有链接，仅接受确为 PDF/OFD/XML 的响应 |
| 发送成功但网页版「已发送」没有 | QQ 默认不保存 SMTP 发件；设置 → 账号 中开启「SMTP发信后保存到服务器」 |
| 发送被拒/限流 | 腾讯反垃圾限制，短时间大量发信会触发；个人正常频率（每天几十封内）无影响 |

## QQ 邮箱 IMAP 三个实测坑（脚本已内置规避，了解即可）

1. **UID 跨会话会重排**：同一批邮件隔一段时间 UID 全变。去重键必须用 Message-ID（脚本已实现），切勿用 UID 或邮件序号。
2. **UID SEARCH 条件要分开传参**：`uid("SEARCH", None, "SINCE", date)` 正确；整串带括号 `"(SINCE ...)"` 会被服务器静默忽略并返回全部邮件。
3. **OFD 转换的发票 PDF**：fitz（内容流顺序）会把标签和值拆到两个文本块导致字段提取失败；pdfplumber（视觉顺序）标签值同行，是首选解析库。

## 163 / 126 邮箱接入（网易系）

163.com 与 126.com 同属网易，配置完全一致（仅后缀不同）：IMAP `imap.163.com`/`imap.126.com`:993、SMTP `smtp.163.com`/`smtp.126.com`:465，均需**客户端授权码**。

**最简配置**：在 `account` 写 `"provider": "163"`（或 `"126"`），脚本自动填入 host/port，无需手动查。
```json
"account": { "provider": "163", "secrets_file": "~/.workbuddy/secrets/invoice-forward.env" }
```

**获取授权码**：登录 mail.163.com（或 mail.126.com）→ 设置 → 开启「POP3/SMTP/IMAP 服务」（默认禁用，需手动开启）→ 短信验证 → 生成**授权码**（仅显示一次，立即保存）。授权码 ≠ 登录密码。

**⚠️ 反垃圾风控（与 QQ 最大差异）**：163/126 对「相似内容 + 脚本秒级连发」判为群发/机器人，会临时限发甚至封号。务必配合发送节奏（`config.json` 的 `send` 段）：
- `send.interval >= 3`（每封间隔 ≥3 秒，模拟人类）
- `send.batch_limit <= 20`（单批不超过 20 封，超出下轮自动续跑）
- 主题模板建议加 `{invoice_no}` 提升单封区分度：`"{item} {amount} {date} {invoice_no}"`
- 新绑定账号首周放慢频率

**接入步骤**：开服务→改 config（provider）→换 secrets 授权码→`check`→`scan --days 30` 干跑确认（重点看 IMAP UID/SEARCH/文件夹名是否如预期）→小批量 `run` 试发观察风控。

**⚠️ 关于 "Unsafe Login"**：163/126 要求客户端先发 IMAP `ID` 命令自报身份，否则 `SELECT`/`EXAMINE` 选文件夹会被拒（`NO [Unsafe Login. Please contact kefu@188.com]`），表现为 `scan` 报 `SEARCH illegal in state AUTH` 或 `check` 假绿。v1.0.4 起脚本登录后已**自动发 `ID`** 绕过，无需用户操作；若用旧版本须升级。

## 链接型发票抓取（如腾讯云电子发票）

很多服务商（腾讯云、部分电商/ SaaS）的发票邮件**不含发票附件**，只有一个下载链接。本工具 v1.0.6 起自动处理这类邮件，v1.0.7 起链接下载支持 **PDF / OFD / XML** 三种格式：

- **机制**：邮件无发票附件时，扫描正文全部链接（HTML 的 `href`/`src` + 纯文本 URL，HTML 实体如 `&amp;` 会反转义）→ 逐一下载 → **仅当最终响应确为发票文件才采用**（按 Content-Type / Content-Disposition 后缀 / 魔数判定：PDF=`%PDF`、OFD=ZIP 且根含 `OFD.xml`、XML=`<?xml` 开头）→ 照常解析转发。
- **实测案例（腾讯云）**：邮件内含一个腾讯云 COS **预签名 URL**（`*.myqcloud.com/...?sign=...&response-content-type=application/pdf&response-content-disposition=attachment; filename=...pdf`）。该链接**无需登录**即可 GET 下载，签名有效期通常 **30 天**（邮件正文会写明）。下载后文件名从 Content-Disposition 提取，含发票号与日期。✅ 已验证可端到端自动转发（PDF 实测；OFD/XML 走同一链接通道，仅按响应格式判定）。
- **抓不到的情况（归入"无发票待人工"并注明原因）**：
  - 链接指向**需登录的页面**（如发票管理控制台 `console.cloud.tencent.com/...`）而非直链发票文件 → 下载到的是 HTML 登录页，非发票格式，自动跳过。
  - 预签名 URL **已过期**（超 30 天）→ 返回错误页，非发票格式。
  - 这类情况需用户手动从网页下载后转发，或重新触发一封带有效链接的邮件。
- **安全闸门**（重要）：链接抓取只下载 http(s)，且**仅接受最终响应确为发票格式的内容**——绝不执行下载到的任何内容，只保存发票字节。字面量私有/环回/链路本地 IP 会被拒绝（SSRF 基础防护）。域名用 DNS 解析拦截不可靠（公有 CDN 会被误杀），故不做解析拦截，由发票格式闸门兜底。
- **配置**（`config.json` 的 `scan` 段）：`fetch_links`（默认 true）、`link_domains`（非空时仅下载这些域名后缀的链接，如 `["myqcloud.com","tencent.com"]`，进一步缩小下载范围；空=全部）、`link_timeout`、`link_max_bytes`（默认 25MB）、`link_user_agent`。setup 对应参数：`--fetch-links`/`--no-fetch-links`、`--link-domains`、`--link-timeout`。

## 扩展到其他邮箱（Gmail / Outlook / 企业邮箱等）

脚本不绑定任何邮箱，连接参数全读 `config.json`：

1. `account` 写 `provider`（若已支持）或直接改 `imap_host` / `smtp_host` / `port`
2. 用对应邮箱的授权码/客户端专用密码更新 secrets 文件
3. 重跑 `check` 验证

注意：不同邮箱 IMAP 行为差异（UID 稳定性、SEARCH 语法、文件夹名）未经实测，先 `scan` 预览确认再 `run`。

## 安全与隐私

- 授权码只存本机 secrets 文件（chmod 600），skill 包、config.json 均不含凭证；也支持 `MAIL_USER`/`MAIL_AUTH_CODE` 环境变量临时传入（优先级更高，授权码免落盘，适合隔离验证 / CI）
- 发票 PDF 全程在内存中处理，不落盘
- 转发记录（processed.json、报告文件）存于本机 `~/.workbuddy/invoice-forward/`
