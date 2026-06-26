# Ontology Evolution

知识图谱不是一次性建好的静态模型。实体会被重新分类，schema 会增加字段，多次扫描会产生冲突。本文定义 schema 版本控制、实体重分类、冲突处理和向后兼容的机制。

## 1. Schema 版本控制

schema.yaml 顶部已有 `meta.version`。版本控制规则：

```yaml
meta:
  version: "1.1"          # 语义化版本：major.minor
  last_updated: "2026-03-17"
  changelog:
    - version: "1.1"
      date: "2026-03-17"
      changes: "新增关系语义属性(temporal/confidence/evidence)"
    - version: "1.0"
      date: "2026-03-16"
      changes: "初始版本，8 core types + 10 domain types"
```

**版本递增规则**：
- **minor**（1.0 → 1.1）：新增可选字段、新增 domain type、新增关系类型。旧数据不需迁移
- **major**（1.x → 2.0）：修改 core type 定义、删除字段、修改 ID 格式。旧数据需要迁移脚本

**graph.jsonl 中的版本标记**：

每个实体的 source 中记录写入时的 schema 版本：

```json
{
  "id": "per-00001",
  "source": {
    "type": "scan",
    "scan_id": "scan-20260316-step2",
    "schema_version": "1.0"
  }
}
```

查询时可按 schema_version 过滤，定位需要迁移的旧实体。

## 2. 实体重分类

场景：扫描时把"2020年9月蓝天信息并入星辰集团国际"记为 Note，复查后发现应该是 Event。

**操作流程**：

```jsonl
// 1. 创建新 Event 实体
{"op":"create","ts":"2026-03-17T10:00:00Z","entity":{"id":"evt-00164","type":"Event","properties":{"title":"蓝天信息以研发中心形式并入星辰集团国际","date":"2020-09"},"source":{"type":"manual","reason":"reclassify from note-00007","schema_version":"1.1"}}}

// 2. 标记旧 Note 为 deprecated
{"op":"update","ts":"2026-03-17T10:00:01Z","entity_id":"note-00007","changes":{"deprecated_by":"evt-00164","deprecated_at":"2026-03-17","deprecated_reason":"reclassified as Event"}}
```

**核心原则**：
- **append-only**：不删除旧实体，只追加 deprecated 标记
- **双向链接**：新实体的 source.reason 引用旧 ID，旧实体的 deprecated_by 引用新 ID
- **query_graph.py 默认行为**：排除带 deprecated_by 字段的实体。加 `--include-deprecated` 参数可查看全量

**批量重分类**：

Step 2 完成后发现一批 Note 应该是 Event（都有明确日期），用脚本批量处理：

```python
# 伪代码：筛选有 date 属性的 Note，逐条重分类
for note in notes_with_date_property:
    create_event(from_note=note)
    mark_deprecated(note, new_id=event.id)
```

## 3. Schema 合并冲突

两次扫描可能对同一概念给出不同定义。

**场景举例**：
- 第一次扫描从邮件中提取 `org-00002 蓝天信息`，type 记为 "IT企业"
- 第二次扫描从合同文档中提取同名实体，type 记为 "研发中心"（并入星辰集团国际后的角色）

**处理策略**：

| 冲突类型 | 策略 | 示例 |
|----------|------|------|
| 属性值矛盾 | 保留两个版本，标记 `review_flag` | 蓝天信息的 type 到底是"IT企业"还是"研发中心"？两个都对——不同时期不同角色 |
| 同名不同实体 | 分别保留，用 ID 区分 | 两个"赵六"——per-00006 是蓝天信息的，per-00XXX 是星辰总部的 |
| 不同名同一实体 | 合并为一条，保留别名 | "蓝天信息" = "蓝天信息" = "蓝天信息"，aliases 数组保存所有名称变体 |

**合并规则**：
- **属性取并集**：A 有 email 但没 phone，B 有 phone 但没 email → 合并后两个都有
- **约束取交集**：A 说 Organization.type 可选 5 种，B 说可选 3 种 → 合并后只保留 A、B 都认可的
- **冲突属性不自动覆盖**：值矛盾时两个都保留，生成 review_flag 等用户裁决

**review_flag 格式**：

```json
{
  "type": "merge_conflict",
  "entity_id": "org-00002",
  "field": "type",
  "values": ["IT企业", "研发中心"],
  "sources": ["scan-20260316-step2-email", "scan-20260317-step2-contracts"],
  "suggestion": "两个都对，建议用 labels 同时标记"
}
```

## 4. 向后兼容

新版本 schema 不能让旧数据失效。

**规则**：

| 变更类型 | 兼容性 | 处理方式 |
|----------|--------|----------|
| 新增可选字段 | 向后兼容 | 旧实体中该字段为 null，query 时视为"未知" |
| 修改字段名 | 不兼容 | 必须递增 major 版本，提供迁移脚本 |
| 新增关系属性（temporal/confidence/evidence） | 向后兼容 | 旧关系只有 type + target_id 继续有效 |
| 新增 core type | 不兼容 | 8 个 core types 是固定的，不应新增 |
| 新增 domain type | 向后兼容 | 直接追加到 schema.yaml 的 domain_types |
| 收紧属性值域（如 type_enum 减少选项） | 不兼容 | 需要检查旧数据中是否有被删除的选项 |

**实际操作**：

关系新增 temporal/confidence/evidence 字段（1.0 → 1.1）：
- 旧关系 `{"type":"works_at","target_id":"org-00002"}` 继续合法
- 读取时：temporal=null（时间未知）、confidence=medium（默认中等）、evidence=null（来源未知）
- 不需要回填旧数据，除非后续扫描发现了时间或来源信息

**迁移脚本约定**：

如果发生 major 版本变更，在 `scripts/` 下创建 `migrate_vX_to_vY.py`：
- 读取 graph.jsonl 全量
- 按新 schema 转换每条记录
- 输出新的 graph.jsonl（旧文件重命名为 graph.jsonl.v1.bak）
- 更新所有实体的 source.schema_version
