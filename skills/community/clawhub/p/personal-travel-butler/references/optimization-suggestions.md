# Personal Travel Butler Skill 优化建议

> 以下建议供其他 AI 调整 skill 时使用。每条建议标注了优先级和影响范围。

---

## 一、高优先级：修复现有问题

### 1.1 城市字段歧义问题
**现状**：文昌码头老爸茶的 city 字段最初写了 `"海口文昌"`，已修正为 `"文昌"`。
**问题**：skill 没有强制校验城市格式，容易混入 `"XX市XX区"` 或 `"海口文昌"` 这类模糊写法。
**建议**：
- 在 `create_entry.py` 或 `validate_db.py` 中加入城市标准化逻辑（如使用 `province + city` 两级字段）
- 或至少在 ingestion workflow 中增加城市校验步骤

### 1.2 证据字段格式不一致
**现状**：Markdown 文件中的 `evidence` 是结构化数组（含 `source`、`date`、`note` 字段），但 `_records.jsonl` 中的 evidence 被扁平化为字符串列表。
**问题**：Notion 同步时丢失了证据的结构化信息（日期、来源链接等）。
**建议**：
- 在 `notion_common.py` 中让 evidence 保持 JSON 对象数组格式，而非字符串
- Notion 的 `Evidence` 字段可以考虑用 `rich_text` 存储 JSON 序列化后的字符串，或拆分为子属性

### 1.3 标签字段在 Notion 中可能超出限制
**现状**：Notion 的 `Tags` 是 `multi_select` 类型，但 `notion_common.py` 中没有对标签数量做限制。
**问题**：Notion API 对 multi_select 的选项数量有限制（每个页面最多 100 个标签）。
**建议**：
- 在 `notion_properties_for_record()` 中增加标签数量上限（如 20 个）
- 超出部分截断或在 summary 中体现

---

## 二、中优先级：增强功能

### 2.1 自动从 Markdown 同步到 _records.jsonl
**现状**：需要手动运行 `build_records_from_places.py` 脚本来把 Markdown 文件转为 compact record。
**问题**：每次新增 Markdown 文件后，必须手动触发转换，容易忘记。
**建议**：
- 在 `notion_sync.py` 的 push 逻辑中增加一步：自动扫描 `places/` 目录下没有对应 compact record 的新文件，自动生成并追加到 `_records.jsonl`
- 或者在 `validate_db.py` 中增加一个 `--auto-sync` 标志，自动检测并补齐

### 2.2 增量同步检测
**现状**：`plan_push()` 比较的是 `local_hash`，但 hash 计算使用的是 compact record 的内容，不包含 Markdown detail file 的变化。
**问题**：如果只更新了 Markdown 文件但没有更新 `_records.jsonl` 中的 summary/notes，Notion 不会感知到变化。
**建议**：
- 当 `record_weight` 为 `standard` 或 `detailed` 时，hash 计算应同时考虑 compact record 和 detail file 的内容
- 或者在 push 前自动从 detail file 重新提取 summary/notes 写入 compact record

### 2.3 冲突检测增强
**现状**：`_conflicts.md` 只在双向修改时触发，但当前逻辑依赖 `ledger` 中的 `local_hash` 和 `notion_hash` 对比。
**问题**：如果 Notion 端有人工编辑（直接在 Notion 里改），而本地 `_records.jsonl` 没更新，ledger 无法检测到差异。
**建议**：
- 在 pull 时增加一个 `--strict` 模式：每次 pull 前先重新计算 Notion 页面的内容 hash，与 ledger 中的 `notion_hash` 对比
- 或者在 Notion 页面中增加一个隐藏字段存储内容 hash，便于检测人工编辑

### 2.4 地理位置坐标补全
**现状**：所有记录的 `coordinates` 都是 `null`。
**问题**：无法在地图上展示，也无法做距离排序。
**建议**：
- 在 enrichment 步骤中增加地理编码（geocoding）：通过地址调用地图 API 获取经纬度
- 或者在 `create_entry.py` 中增加 `--coords` 参数

---

## 三、低优先级：体验优化

### 3.1 索引文件自动生成
**现状**：`_index.md` 由 `save_records()` 自动生成，但 `places/` 目录下的 Markdown 文件有独立的索引（如 `indexes/cities.md`）。
**问题**：两套索引可能不一致。
**建议**：
- 统一索引来源：以 `_records.jsonl` 为准，不再维护独立的 `indexes/` 目录
- 或者在 `notion_sync.py` 的 sync 完成后自动更新 `indexes/cities.md`

### 3.2 批量操作支持
**现状**：`notion_sync.py` 一次只能 push/pull 所有记录，不支持按城市或标签筛选。
**建议**：
- 增加 `--filter-city`、`--filter-tag` 参数，支持选择性同步

### 3.3 同步日志
**现状**：同步过程没有持久化日志。
**建议**：
- 在 `notion-sync/` 下增加 `_sync_log.jsonl`，记录每次同步的时间、方向、影响记录数、错误信息

---

## 四、Notion Schema 扩展建议

当前 Notion 数据库缺少以下有用字段：

| 建议新增 | 类型 | 用途 |
|---------|------|------|
| `Address` | rich_text | 详细地址 |
| `Province` | rich_text | 省份 |
| `Phone` | rich_text | 联系电话 |
| `Website` | url | 官方网站 |
| `Visited` | checkbox | 是否已去过 |
| `Rating` | number | 个人评分 |
| `Last Visited` | date | 最后访问日期 |
| `Photos` | files & media | 现场照片 |

这些字段可以在 `PROPERTY_CREATE_SCHEMA` 和 `notion_properties_for_record()` 中一并添加。
