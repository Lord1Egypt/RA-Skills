# Changelog

All notable changes to this skill are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/); versions follow [SemVer](https://semver.org/).

### v1.0.10 (2026-10-20)

修复「邮件正文 HTML 被当成发票」导致的**静默漏发**。实测场景：近 7 天 4 张发票抬头全部命中，
但 `scan` 报告「跳过 4」，且报告口径看起来像正常的抬头过滤。

#### Fixed

- **`detect_fmt_from_magic` 把 HTML 误判为 XML**（根因）：原判定为「首字符是 `<` 即视为 XML」，
  而邮件正文 HTML 同样以 `<` 开头，且 MIME 树里正文排在附件之前 → `find_invoice_attachment`
  第一个命中的就是正文 → `extract_xml` 解析 HTML 得空字段 → 抬头比对失败 → 记为 `skipped`。
  现改为：识别 `<!DOCTYPE` / `<html` / `<head` / `<body` 等 HTML 头直接排除；XML 必须能被
  `ElementTree` 解析且根标签含 `Invoice` / `EInvoice` / `发票`。
- **`find_invoice_attachment` 只看真附件分区**：新增 `_is_attachment_part()`，要求有文件名或
  `Content-Disposition: attachment`；正文分区不参与判定。另：多个候选按 **PDF > OFD > XML**
  取最优（转发只带 PDF，PDF 版面也最贴近视觉顺序）；名为 `.xml` 实为 HTML 的附件直接丢弃。
- **解析失败不再伪装成「抬头不符」**：开启抬头白名单后，若提取不到购买方名称，新增状态
  `parse_failed` 并计入「无发票待人工」，绝不写入 `skipped`。这是防止同类事故再次静默的关键闸门。
- **销售方提取补兜底**：数电票把购销双方排在同一行（`购 名称:A 售 名称:B`），原正则
  `销售方\s*名称[:：]` 失配导致 seller 恒为空。改为回退取「名称:」第 2 次命中。

#### Added

- `tests/test_attachment.py`：9 条纯标准库回归用例，覆盖「纯正文 HTML 不算发票」「正文 HTML +
  PDF 附件取 PDF」「PDF 优先于 XML」「RFC2047 折行编码的中文附件名」「名为 .xml 实为 HTML」
  以及 extract 的购买方/销售方/金额/发票号断言。运行：`python3 tests/test_attachment.py`。

#### Documentation

- 「输出解读」新增「解析失败」状态行，并写明「解析失败绝不会落到跳过」的硬约束及其事故来源。

### v1.0.9 (2026-09-05)

无功能变更，`scripts/invoice_forward.py` 行为与 v1.0.8 完全一致。全部为文档改进与勘误。

#### Fixed

- 修正 v1.0.7 条目中「本地已升至 v1.0.7，GitHub/clawhub 仍停 v1.0.3（待发布）」的过时陈述——
  实际早已同步至 v1.0.8，该句会误导读者以为开源版滞后。

#### Documentation

- **新增「输出解读」章节**（重要）：用表格区分「已发送 / 跳过 / 跳过（发票号重复）/ 无发票 / 延后 /
  发送失败」六类状态，明确 **「跳过」= 抬头白名单不命中（正确过滤，不是漏发）**，与「无发票」
  （解析或下载失败）在代码中是两条独立分支，排查漏发应看后者而非前者。
  此前该语义只存在于源码里，用户必须读代码才能判断有没有漏发。
- **新增「定时任务（无人值守）」章节**：
  - ⚠️ **路径第一原则**：脚本与配置必须落在持久目录。记录了「自制脚本放在 `output/` 被清理 →
    定时任务连续静默失败 25 天」的真实事故。
  - 给出 WorkBuddy automation prompt 参考模板，含两条来自事故的硬约束：
    禁止模型自行重写脚本或改配置、禁止把授权码打印到聊天或日志。
  - 给出非 WorkBuddy 环境的 crontab 行。
- 补充「每日报告」说明：`run` 会在配置目录生成 `~/.workbuddy/invoice-forward/报告_YYYYMMDD.md`
  （同日重跑覆盖）——这是脚本既有行为，此前文档未提及。
- 术语修正：日常使用章节「无PDF」→「无发票待人工」（脚本自 v1.0.7 起已支持 OFD/XML，输出文案同步更新）。

### v1.0.8 (2026-07-30)

- **新增：转发抄送（CC）支持，默认关闭**。`forward` 配置新增 `cc` 数组字段，填写后每封转发邮件同时抄送给这些地址；默认空数组（`"cc": []`）= 完全关闭，对既有用户零影响、零行为变化。
  - `SmtpSession.send` 在 `cc` 非空时写入 `Cc` 头，`send_message` 自动将其纳入实际收件人。
  - `setup` 与 `doctor(check)` 输出新增「抄送(CC)」一行，显示当前是否启用。
  - `config.example.json` 增加 `cc` 字段与说明注释。
- 实现遵循最小改动：防自转发循环的 `exclude`（基于 From 字段）无需调整，抄送不会引发循环。

### v1.0.7 (2026-07-23)

- **新增：发票格式支持 PDF / OFD / XML 三种**。`find_invoice_attachment` 按「文件名后缀 / Content-Type / 魔数」三重判定格式（PDF=`%PDF`、OFD=ZIP 且根含 `OFD.xml`、XML=`<?xml` 开头），附件、链接下载、转发附件 MIME 全部走统一格式分发。
  - **PDF**：沿用既有 `pdf_text` + `extract` 正则（需 pdfplumber/pymupdf 其一）。
  - **OFD**：ZIP 容器内遍历页面 `Content.xml` 抽取 `TextCode` 文本，复用 PDF 同款正则；若抽取不足（缺发票号/抬头），自动回退到 OFD 内嵌的结构化发票 XML（若存在）做精确解析。无需任何第三方库（Python 内置 `zipfile`）。
  - **XML**：结构化解析（兼容增值税电子发票 `FPML` / 全电发票等），命名空间无关、按已知字段标签（大小写不敏感，支持 `FPHM`/`KPRQ`/`GMF`+`NSRMC`/`XHF`+`NSRMC`/`XMMC`/`JSHJ` 等）在父子关系中取值；开票日期归一化为 `YYYYMMDD`。无需任何第三方库（Python 内置 `xml.etree`）。
- **链接型发票下载泛化**：`download_link_pdf` → `download_link_invoice`，接受链接最终响应为 PDF/OFD/XML 任一格式（按 Content-Type / Content-Disposition 后缀 / 魔数判定），其余安全闸门（仅 http(s)、域名白名单、SSRF 字面量私有 IP 拦截、限大小/超时、仅保存发票字节）完全保留。
- **依赖说明更新**：PDF 解析仍需 pdfplumber/pymupdf 至少其一；OFD/XML 用 Python 标准库即可，无额外安装负担。`process` 仅在遇到 PDF 且缺解析库时才跳过该邮件（并提示 `check --install-deps`），不再因缺 PDF 库整体退出，OFD/XML 流程不受影响。
- 文档同步：`SKILL.md` 描述与支持范围扩至 OFD/XML、`parse` 子命令支持三种格式；`config.example.json` 注释将链接抓取的描述从"下载 PDF"更正为"下载发票文件"。

### v1.0.6 (2026-07-23)

- **新增：链接型发票自动下载（如腾讯云电子发票）**：邮件无 PDF 附件时，自动扫描正文全部链接（HTML 的 `href`/`src` + 纯文本 URL，HTML 实体反转义去重），逐一下载，**仅当最终响应确为 PDF 才采用**（Content-Type 含 `pdf` / Content-Disposition 含 `pdf` / `%PDF` 魔数三重判定），随后照常解析转发。适用于邮件内只有下载链接、无 PDF 附件的场景。
  - 实测案例：腾讯云电子发票邮件内含 COS 预签名 URL（`*.myqcloud.com`），无需登录即可 GET 下载，签名有效期 30 天；已端到端验证可正确下载并解析转发（发票号 / 金额 / 日期 / 购买方均正确提取）。
  - 抓不到时归入"无PDF待人工"并注明原因（链接未返回 PDF=可能需登录或已过期 / 链接抓取禁用），不阻塞其他邮件。
- **新增配置（config.json 的 `scan` 段）**：`fetch_links`（默认 true）、`link_domains`（非空时仅下载这些域名后缀的链接，空=全部）、`link_timeout`（下载超时秒）、`link_max_bytes`（单链接上限字节，默认 25MB）、`link_user_agent`。setup 对应参数：`--fetch-links`/`--no-fetch-links`、`--link-domains`、`--link-timeout`。
- **安全闸门**：链接抓取仅下载 http(s)，字面量私有/环回/链路本地 IP 拒绝（SSRF 基础防护）；真正兜底的是"仅接受 PDF 响应"——绝不执行下载内容，只保存 PDF 字节。域名不做 DNS 解析拦截（公有 CDN 在代理/沙箱下会被误杀，已有教训）。
- **Bug 修复（真实验证发现）**：初版 SSRF 防护对链接域名做 DNS 解析拦截，把腾讯云公有 COS 域名（`s2-jarvis-gz-...myqcloud.com`）误判为私有 IP 而拒绝下载。改为仅拦截字面量私有/环回/链路本地/保留/多播 IP，域名放行，由 PDF 闸门兜底。

### v1.0.5 (2026-07-23)

- **新增 `setup` 子命令（一键配置）**：把「收集凭证 + 收集转发规则 + 生成 config.json + 验证 + 写盘」合并为一条命令。特性：
  - 凭证与非凭证配置一起支持（user/provider/auth-code/to/days/keywords/buyer-whitelist/templates/send 节奏等），授权码绝不写入 config.json。
  - **写入准确性保证**：默认真实登录 IMAP + SMTP 验证连通性，验证通过才写 secrets（chmod 600）；验证失败则**不写 secrets**（config.json 仍保存便于重跑），杜绝把错误授权码落盘。
  - 幂等合并已有 config（重跑不清空既有设置）；`--provider` 省略时按 `--user` 域名自动推导主机；非 tty 缺参直接报错、tty 下交互逐项询问；`--no-verify` 可跳过验证（离线调试用）。
  - secrets 以 `os.open(..., 0o600)` 原子创建并 `chmod 600`，杜绝 umask 导致权限过宽。

### v1.0.4 (2026-07-23)

- **Bug 修复（163/126 真实验证发现）**：163/126 登录后选文件夹返回 `NO [Unsafe Login]`，读写 `SELECT` 与只读 `EXAMINE` 都被拒，导致 `scan` 报 `SEARCH illegal in state AUTH` 且 `check` 假绿（未校验 select 返回码）。修复：登录后自动发 IMAP `ID` 命令自报客户端身份再只读 `SELECT`；`check` 的 IMAP 步骤现校验 select 返回码，不再误报通过。QQ 等不受影响（不支持/忽略 ID 时静默跳过）。
- **增强：凭证支持环境变量回退**：`load_cred` 现优先读取环境变量 `MAIL_USER` / `MAIL_AUTH_CODE`（两者齐全时优先于 secrets 文件），便于临时隔离验证、CI / 容器场景，授权码免落盘。

### v1.0.3 (2026-07-23)

- **多邮箱支持（provider preset）**：`account` 新增 `provider` 字段（`qq`/`163`/`126`/`yeah` 或域名后缀如 `163.com`），配置即自动填入对应 IMAP/SMTP 主机与端口，免去手动查 host。同时修了 `__version__` 长期停留在 1.0.0 的版本号不一致问题（现与包版本对齐 1.0.3）。
- **发送节奏参数（防反垃圾风控）**：新增 `send` 配置段——`interval`（每封最小间隔秒）、`jitter`（额外随机秒上限）、`batch_limit`（单批最多发送封数，超出则本轮延后、下轮自动续跑，配合 `processed.json` 去重天然支持）。163/126 等严格风控邮箱必配，避免相似内容 + 脚本连发被判群发机器人。
- **文档**：troubleshooting.md 新增「163/126 接入」专节（授权码获取路径、风控提醒、发送节奏建议、接入步骤）；config.example.json 增加 `provider` 与 `send` 示例；SKILL.md 描述与支持范围扩至 163/126。

### v1.0.2 (2026-07-23)

- **Bug 修复**：`scan` 干跑预览漏报发票号重复。原 `_nos`（同轮内按发票号去重集合）累加被关在 `if do_send`（run 真实发送）分支内，`scan` 不维护它，导致预览与实际行为不一致——同一张发票被不同邮件多次投递时，预览会显示多封、而 run 实际只发一封。改为在循环体中无论是否发送都维护 `_nos`，使 `scan` 与 `run` 去重行为一致。

### v1.0.1 (2026-07-22)

- **Bug 修复**：`extract()` 销售方（seller）字段提取为空。原正则 `销\s*名称` 匹配不到标准增值税电子发票标签「销售方名称」（中间含"售方"），改为 `销售方\s*名称`。E2E 验证发现并修复。

### v1.0.0 (2026-07-22)

- Initial open-source release
