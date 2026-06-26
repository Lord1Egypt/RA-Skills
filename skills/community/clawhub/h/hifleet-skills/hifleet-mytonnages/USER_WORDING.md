# 对用户说话时的用词规范（硬性）

助手在**回复用户**时须用业务口语，**禁止**暴露内部实现术语。分册文件名（如 `WORKFLOW_2_MAIL.md`）仅助手 `read_file` 使用，**不要**在对话里让用户去读。

---

## 禁止对用户说的话 → 改用

| 禁止 | 改用（示例） |
|------|----------------|
| Workflow、工作流 | **查询步骤**、**按下面方式查** |
| Schema、PARSE_SCHEMA、parse_schema | **邮件解析字段**、**从邮件里提取的字段** |
| SQLite、charter_facts | **本地船货盘库**、**已保存的船货记录** |
| enrich、富化、enrich_row | **补充船舶信息**、**补齐 IMO 和标签** |
| 路由 A/B/C | **查您邮箱** / **查班轮船期** / **查预抵船** |
| memory_search、向量库 | **邮件检索**、**在您的邮件里搜索** |
| API 路径、POST、Query | **在 HiFleet 上查询**（必要时只说「需要您的 API Key」） |
| offset/limit、filterLabels | **分页**、**筛选条件**（或直接用船龄、船型等中文） |
| typeCode、product_* | **解锁完整联系人信息**（不说内部编码） |
| stat、payload_json | **统计汇总**、**详细记录** |

---

## 路由 C（预抵）对用户的说法

- ✅ 「正在查询**预抵**天津港的船舶…」「共找到 **N** 艘预抵船」  
- ❌ 「调用 destination/search 接口」「filterLabels.vesselAge」

---

## 路由 A 邮件解析

- ✅ 「已从邮件中提取船盘/货盘并**保存到本地**」  
- ❌ 「按 PARSE_SCHEMA 落库」「执行 2.4.1」
