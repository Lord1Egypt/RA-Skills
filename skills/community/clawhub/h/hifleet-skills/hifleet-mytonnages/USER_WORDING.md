# 对用户说话时的用词规范（硬性）

助手在**回复用户**时须用业务口语，**禁止**暴露内部实现术语。分册文件名（如 `WORKFLOW_2_MAIL.md`）仅助手 `read_file` 使用，**不要**在对话里让用户去读。

**语言**：默认用**英文**与用户交流（见 **`LOCALIZATION.md`**）；若智能体前端 locale 为中文等，将**提示/错误/说明**译为对应语言；**船名、港口、货物名、API 返回值**等业务数据**不翻译**。

---

## 禁止对用户说的话 → 改用

| 禁止 | 改用（示例） |
|------|----------------|
| Workflow、工作流 | **查询步骤**、**按下面方式查** |
| Schema、PARSE_SCHEMA、parse_schema | **邮件解析字段**、**从邮件里提取的字段** |
| SQLite、charter_facts | **本地船货盘库**、**已保存的船货记录** |
| enrich、富化、enrich_row | **补充船舶信息**、**补齐 IMO 和标签** |
| 路由 A/C | **查您邮箱** / **查预抵船** |
| 班轮船期 | 使用 **`hifleet-schedule`** 技能 |
| 公开船盘/公开货盘 | 使用 **`hifleet-opentonnages`** 技能（先列船货信息；联系方式按需用 **记录 id** 获取） |
| memory_search、向量库 | **邮件检索**、**在您的邮件里搜索** |
| API 路径、POST、Query | **在 HiFleet 上查询**（必要时只说「需要您的 API Key」） |
| offset/limit、filterLabels | **分页**、**筛选条件**（或直接用船龄、船型等中文） |
| typeCode、product_*、unlock | **班轮/公开船货/预抵**均说 **获取联系方式**（用记录 id）；禁止对用户说「解锁」；typeCode 表见 **`references/charter_contact_unlock.md`** |
| preview_url、mail_preview | **查看原邮件**（系统内预览，见 **`MAIL_PREVIEW.md`**） |
| webmail_url、webmail_locate | **在您的邮箱网页里打开**（浏览器须已登录该邮箱） |
| reply_url、mail_reply | **回复这封邮件**（优先网页邮箱回复，或配置 SMTP 后系统内发送） |
| stat、payload_json | **统计汇总**、**详细记录** |

---

## 路由 C（预抵）对用户的说法

- ✅ 「正在查询**预抵**天津港的船舶…」「共找到 **N** 艘预抵船」  
- ✅ 列表后：「如需某条船的联系方式，请告诉我 **记录 id**；若要本页全部，请说 **全部**。」  
- ✅ 获取后：「已获取联系方式」— **不要**说「已解锁」  
- ❌ 「调用 destination/search 接口」「filterLabels.vesselAge」「portid」「portcode」

---

## 路由 A 邮件解析

- ✅ 「已从邮件中提取船盘/货盘并**保存到本地**」  
- ❌ 「按 PARSE_SCHEMA 落库」「执行 2.4.1」
