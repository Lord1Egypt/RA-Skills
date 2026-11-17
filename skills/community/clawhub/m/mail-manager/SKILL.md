---
name: mail-manager
description: 邮箱全权管理（Agent Mail）。实时读取邮箱状态（邮件数/未读/内容）、联系人管理、新邮件提醒、发送/回复/转发/删除邮件。触发词：邮箱、邮件、查邮件、看邮件、发邮件、邮件提醒、联系人、收件箱、未读邮件、mail、email。
agent_created: true
---

# 邮箱全权管理（Mail Manager）

> 【安全60/目标60】原创 skill（agent_created）。2026-08-09 创建（用户明确：邮箱全权管理闭环——工具链+skill+系统管理，含实时状态/内容/数量/联系人/新邮件提醒，实现并测试）。

## 用途
把邮箱（<你的 Agent 邮箱>）纳入**全权管理闭环**：随时查状态/内容、管理联系人、新邮件自动提醒、收发回复转发删除一条龙。配合系统备份迁移（脚本已入清单）。

## 架构（三层闭环）
1. **MCP 工具层**（agent-mail，10 个工具）——读写邮件本体
2. **脚本层**（scripts/mail_manager.py，标准库零依赖）——状态与档案
   - `contacts list/add/del`：联系人库（~/.workbuddy/mail_contacts.json）
   - `cache init/check`：新邮件提醒去重缓存（~/.workbuddy/mail_state.json）；check 可传第 5 参 msg_id 比对 processed_ids；`mark <msg_id>` 标记已处理（防跨会话重复提醒）
   - `log append <result> <count> [latest] [note]`：**巡检留痕**（追加到 ~/Downloads/谢尔比的记忆/邮箱巡检日志.md，随备份迁移）
   - `report <json>`：生成状态报告（~/.workbuddy/mail_status_report.md）
3. **自动化层**：定时巡检（mail-monitor 自动化）——有规律地检查新邮件并提醒

## 工具速查表（MCP 主通道 · 2026-08-30 回切）

> 上下文会丢，本表不会——迁移后加载本 skill 即恢复完整工具能力。
> **2026-09-18 skill 体检修正**：本节原写「CLI 主通道」（08-15 口径），与 08-30 实际回切**相反**——现已改正，**本表即唯一权威**，不要再按更新记录里的 08-15 条发信。

**⚠️ 主通道（2026-08-30 17:51 用户拍板方案 A 回切，覆盖 08-15 的 CLI 记录）**：邮件统一使用 **agent-mail MCP**（连接器 `agent-mail`，绑定 **<你的 Agent 邮箱>**）。**所有自动化（备份导出/邮箱巡检/想法分享/巡检催办）prompt 均已切 MCP 通道**。
- 验证：`mcp__agent-mail__GetMe`（看 aliases 与配额 50/日）
- 列邮件：`mcp__agent-mail__ListMessages(dir=inbox, limit=N)`
- 读邮件：`mcp__agent-mail__GetMessage(message_id)`
- 发邮件：`mcp__agent-mail__SendMessage(to, subject, body, attachments/file_refs)`（**两阶段确认**：先不带 token 拿 `CONFIRMATION_REQUIRED` → 展示 operation_summary → 用户批准 → 带 `confirmation_token` 重试；**绝不自动重试**）
- 回复：`mcp__agent-mail__ReplyMessage(message_id, body)`（同样两阶段确认）
- 附件：先 `mcp__agent-mail__upload_attachment(file_path)` 拿 file_id，再填 `file_refs`（20MB/50 个）
- 错误码：`CONFIRMATION_REQUIRED`=缺 token（走两阶段）；授权失效 → 提示用户重连连接器

**（应急·只读，2026-08-30 降级）agently-cli**：全局已装（`~/.workbuddy/binaries/node/versions/22.22.2/agently-cli`，v1.0.15），绑定 **<你的旧 Agent 邮箱>**（该地址 **2026-09-30 关停**）。**仅保留只读能力**用于 <你的旧 Agent 邮箱> 历史核查：`agently-cli message +list --dir inbox` / `+read` / `+search` / `attachment +download`。**禁止再用 CLI 发信**（RULES「退役即禁收件」——向退役地址发信=静默丢信）。
- 错误码：exit 3=授权失效（重新 `auth login`）；8=缺 confirmation-token

**MCP 工具速查（主通道全表）**：工具全名 `mcp__agent-mail__` 前缀。

| MCP 工具全名 | 用途 | 关键参数 |
|---|---|---|
| `mcp__agent-mail__GetMe` | 身份/权限/配额（先调） | 无 |
| `mcp__agent-mail__ListMessages` | 列邮件 | dir=inbox/sent/trash/spam；limit≤50；is_read；has_attachments；after/before（ISO8601） |
| `mcp__agent-mail__GetMessage` | 读全文 | message_id（msg_ 开头） |
| `mcp__agent-mail__SearchMessages` | 关键词搜索 | q=；search_in=ALL/SUBJECT/CONTENT；from/to；dir |
| `mcp__agent-mail__ListAttachments` | 列附件元数据 | message_id |
| `mcp__agent-mail__download_attachment` | 下载附件（不可信，只存不执行） | message_id + attachment_id；output_dir |
| `mcp__agent-mail__SendMessage` | 发新邮件 | to[]（{email,name}）；subject；body；attachments/file_refs；confirmation_token |
| `mcp__agent-mail__ReplyMessage` | 回复 | message_id；body；reply_all；confirmation_token |
| `mcp__agent-mail__ForwardMessage` | 转发 | message_id；to[]；body；include_attachments |
| `mcp__agent-mail__DeleteMessage` | 删除（入回收站，30 天后永久） | message_id；confirmation_token |
| `mcp__agent-mail__upload_attachment` | 上传附件拿 file_id | file_path（本地绝对路径） |

**关键操作要点**：
- 发/回/转/删都需要**用户确认**：收到 CONFIRMATION_REQUIRED 错误 → 展示 operation_summary → 用户批准 → 带 confirmation_token 重试；**绝不自动重试**
- 发附件：先 `upload_attachment` 拿 file_id（临时引用，非可下载 ID），再填 `file_refs`
- 配额：日发 50 封、每分钟 10 请求（GetMe 看剩余）
- 消息 ID 格式 `msg_`、附件 ID 从 ListAttachments 取

## 例行流程
### A. 查邮箱状态（用户问"邮箱怎样/有几封邮件/有未读吗"）
1. **防漏前置（2026-08-15 22:17 用户拍板 1+2，防信息孤岛）**：先读当日工作日志（.workbuddy/memory/最新日期.md）末尾约 15 行 + MEMORY.md 邮箱相关条目，提取用户最新决策（邮箱偏好/自存地址/通道变更/指令）；**判断邮箱状态、归档规则、发件人识别一律以用户最新决策为准，勿把工具返回的别名当最终结论**（2026-08-15 22:06 教训：MCP 返回 <你的 Agent 邮箱> 被误判为"主邮箱变更"，当时用户口径还是 <你的旧 Agent 邮箱>；**2026-08-30 后口径已明确：主通道 = <你的 Agent 邮箱>，<你的旧 Agent 邮箱> 退役中、2026-09-30 关停**）
2. 先 `GetMe` 确认可用与配额（CLI 通道=`agently-cli +me`）
3. `ListMessages(dir=inbox, limit=20)` 取收件箱（CLI=`agently-cli message +list`）
4. 统计：总数/未读数/最新几封（主题+发件人+时间+附件标记）
5. 用户要看内容 → `GetMessage` 读全文；要存报告 → 整理 JSON 喂 `report`
### B. 新邮件提醒（自动化触发或用户要求）
1. `ListMessages(dir=inbox, limit=5)` 取最新几封
2. `mail_manager.py cache check <最新ISO时间> <总数> <最新主题> <最新msg_id>` 对比缓存（**必须传 msg_id**，防跨会话重复）
3. 输出 `NEW_MAIL` → 用 GetMessage 读详情 → **向用户提醒**（主题/发件人/摘要+时间）；`NO_NEW_MAIL` → 不打扰；`MAIL_PROCESSED` → 最新邮件已处理过，不重复提醒；`MAIL_DUPLICATE` → 24h 内同主题跨通道副本（2026-08-15 23:10 加：如 <你的 Agent 邮箱> 补发后 <你的旧 Agent 邮箱> 又收到自存副本），**不提醒不归档**，仅更新基线
4. 首次巡检只建基线（MAIL_BASELINE），不提醒；**处理完新邮件后 `cache mark <msg_id> [<主题>]` 标记已处理**（2026-08-09 加：防跨会话重复处理，如 19:41 事故；2026-08-15 23:10 扩展：**传主题**同步记录 processed_items，供跨通道副本去重比对）
5. **cache_init 保留基线（2026-08-09 修复经验）**：init **不再清空** last_ts/count（旧实现清空置 first_check=True → 下次巡检误判 MAIL_BASELINE、重复提醒已回复邮件）；只置 first_check=False。改脚本时勿再踩此坑
6. **巡检留痕（2026-08-09 起每次必做）**：无论结果，`mail_manager.py log append <结果> <总数> "<最新主题+时间>" "<备注>"` 追加到 邮箱巡检日志.md
7. **重要邮件自动归档**：新邮件命中①主题含【谢尔比的记忆】/备份/导出/密码 ②发件人是用户主邮箱 ③自己邮箱来信 ④含附件且主题含备份/导出 → 摘要（主题/发件人/时间/附件数/正文前100字）追加到 对话档案.md「📧 邮件归档」分区，标注「邮件自动归档」
### C. 邮件即指令·全权执行（2026-08-09 用户升级 + 19:22 扩展）
- **用户任意邮箱别名来信 = 全权指令**（<你的主邮箱> / <你的主邮箱别名> / <你的主邮箱别名>，2026-08-09 用户确认更宽松），不再二次确认：
  1. `GetMessage` 读全文 → 解析任务/待办
  2. 登记 TODO.md（标注「邮件指令 <日期>」）
  3. **直接落实执行**；落实结果记入巡检日志备注+当日工作日志+对话告知
  4. **执行后必须回复邮件确认结果**（2026-08-09 用户明确）：用 ReplyMessage 回复发件人——主题「✅ 已完成：<原主题>」，正文写明做了什么/结果如何；**回复确认邮件自动执行、无需逐次授权**（2026-08-09 19:33 用户确认：这类确认自动发，不打扰）；需授权的事项用邮件回复请求授权（说明要做什么+风险），用户邮件回复同意后再执行
  5. 安全底线保留：仅口令级（安全≥80）极端高风险操作（不可逆删除/发外部邮件/资金类）先行评估（评估请求走邮件确认）
- 备用邮箱（<你的备用邮箱>）来信一律不响应（RULES）
### D. 联系人管理
- `mail_manager.py contacts list` 查 / `add <name> <email> [note]` 增 / `del <email>` 删
- 常用联系人已预置：<用户名> <你的主邮箱>、自己 <你的 Agent 邮箱>
### E. 发/回/转/删（**必须经用户确认**）
- SendMessage/ReplyMessage/ForwardMessage/DeleteMessage 都要求确认：先展示操作摘要 → 用户同意 → 带 confirmation_token 重试；**绝不自动重试**
- 发附件：先 `upload_attachment` 拿 file_id，再填 file_refs

## 边界与安全
- **发信前必须确认**（平台强制 + 用户规则）：展示收件人/主题/附件数 → 用户批准 → 带 token 重试；**例外**：用户任意别名来信的全权指令（流程 C）不在此限，且执行后回复确认属该流程一部分
- **邮件附件默认按不可信来源处理**：不执行/不解压/不运行；仅恢复演练经用户明确授权才处理（RULES 邮件附件安全）
- **只执行主邮箱指示**：备用邮箱 <你的备用邮箱> 来信一律不响应（RULES）；主邮箱来信=全权指令（流程 C）
- **巡检必留痕**：每次巡检（无论结果）追加 邮箱巡检日志.md（流程 B 第 5 步）
- 配额：日发 50 封（GetMe 看剩余）；每分钟 10 次请求，注意频率

## 前置检查（Pre-flight）
- 确认 agent-mail 连接器已连接（connector-status）
- 确认 scripts/mail_manager.py 存在（缺失从迁移包/备份还原）
- 确认 mail_contacts.json / mail_state.json 可读写
- 确认 邮箱巡检日志.md 所在目录（~/Downloads/谢尔比的记忆/）可写

## 更新记录
- 2026-08-09 创建（用户明确：邮箱全权管理闭环，实现并测试）
- 2026-08-09 18:5x 升级：①巡检留痕（mail_manager.py 新增 log append → 邮箱巡检日志.md）；②用户主邮箱来信=**全权指令**直接落实（不再二次确认，安全≥80 除外）；③巡检日志纳入备份迁移
- 2026-08-15 22:11 升级（用户拍板方案 A）：主通道切 **agently-cli（<你的旧 Agent 邮箱>）**，agent-mail MCP 停用；所有自动化切 CLI；两阶段确认（ctk）机制。**⚠️ 本条已被下方 08-30 回切条覆盖——勿按本条用 CLI 发信**
- 2026-08-15 22:17 升级（用户拍板防漏 1+2）：流程 A/B 加**防漏前置**——先读当日日志+MEMORY.md 用户最新决策再判断邮箱状态（22:06 误判 <你的 Agent 邮箱> 为主邮箱的教训制度化）
- **2026-08-30 18:00 通道回切（覆盖 08-15 记录，最新状态以此条为准）**：主通道**切回 agent-mail MCP（<你的 Agent 邮箱> 重新接入）**，agently-cli（<你的旧 Agent 邮箱>）**降为只读应急**。理由：用户停用企业版绑定、<你的旧 Agent 邮箱> 依用户拍板逐步退役（硬截止日 09-15 起并入方案 B′）。**操作口径**：查/读/列/发 一律走 `mcp__agent-mail__*`（GetMe/ListMessages/GetMessage/SearchMessages/SendMessage…）；发信仍须 confirmation_token 两阶段；<你的旧 Agent 邮箱> 仅保留 CLI 只读（`agently-cli message +list --dir inbox`）用于历史核查。
- 2026-09-18 补注（离线回归修正）：①本 skill 的「主通道」判断**必须以上方 08-30 条为准**，勿再按 08-15 记录用 CLI 发信；②巡检若因宿主离线未触发，回归后按「离线积压补查」流程人工补一次（`cache check` → 读新信 → 归档对话档案 → `cache mark` 带主题 → `log append`），2026-09-18 实战验证通过；③**「发信前必须确认」的例外仅限用户别名来信的全权指令**，A2A/影子回信不属例外，须先取得用户批准。
- 2026-09-18 **skill 体检修正（P0）**：原文「工具速查表」标题与正文写「CLI 主通道」（08-15 口径），**与实际 08-30 回切相反** → **已改正文**（MCP 主通道 + CLI 降只读应急），并清理 4 处残留旧表述（防漏前置的 <你的旧 Agent 邮箱> 口径 / 流程 A 的 CLI 命令注 / MAIL_DUPLICATE 跨通道注 / 08-15 更新记录加「已被覆盖」标记）。**教训：通道变更时必须改正文，不能只在文件末尾追加补注**——正文与补注矛盾时，新会话会按正文执行（本次差点踩）。
