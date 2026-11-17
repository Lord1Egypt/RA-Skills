# 家长版成长档案协议

本文件定义单个孩子/单个家庭的成长档案数据边界、确认门槛和 CLI 使用方式。档案默认关闭，不保存作文全文、原图、完整 OCR、学校、班级、住址或无关个人信息。

## 数据原则

1. 默认不启用档案。
2. 每次写入前必须向家长展示完整拟保存摘要，并取得明确确认。
3. 只保存能帮助下一次指导的摘要。
4. 不默认收集孩子真实姓名，可用家长自定义昵称。
5. 平台无法持久化或脚本无法执行时，不得虚称已保存；可导出便携 JSON 或仅保留本次结果。
6. 删除整个档案必须二次确认。

## 家长设置

`ParentSettings`：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `profile_enabled` | boolean | 是否启用成长档案。 |
| `privacy_notice_confirmed` | boolean | 家长是否已理解保存范围、确认机制和删除方式。 |
| `nickname` | string 或 null | 家长自定义孩子昵称，可为空。 |
| `grade_level` | integer | 当前年级，1-6。 |
| `default_mode` | string | `full`、`quick_check`、`structure` 或 `encouraging`。 |
| `child_facing_output` | boolean | 是否默认同时输出孩子直接可看版本。 |
| `advanced_review_offer` | string | 进阶版提示状态：`unoffered`、`declined`、`interested` 或 `enabled`。默认 `unoffered`；用户拒绝后写为 `declined`。 |

`advanced_review_offer` 只记录用户对进阶版提示的偏好，不表示 API 已启用，也不保存 API Key 或账号信息。

只有 `profile_enabled=true` 且 `privacy_notice_confirmed=true` 时，才能执行档案写入、导出、导入、修正或删除。

## 档案摘要

`GrowthProfile`：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `schema_version` | string | 固定为 `parent-growth-profile/1`。 |
| `created_date` | string | 创建日期，`YYYY-MM-DD`。 |
| `updated_date` | string | 最近更新日期。 |
| `records` | ReviewRecord[] | 最近最多 20 次批改摘要。 |
| `recurring_issues` | string[] | 仍然反复出现的问题。 |
| `documented_progress` | string[] | 已经体现的进步。 |
| `current_goals` | string[] | 当前 1-2 个重点目标。 |

`ReviewRecord`：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `review_id` | string | 唯一编号，格式如 `2026-08-22-001`。 |
| `date` | string | 批改日期。 |
| `grade_level` | integer | 年级。 |
| `title` | string | 作文题目。 |
| `composition_type` | string | 作文类型。 |
| `strengths` | string[] | 本次具体优点。 |
| `recurring_issues` | string[] | 本次仍出现或新发现的问题。 |
| `next_goals` | string[] | 下一阶段 1-2 个目标。 |
| `dimension_summaries` | object | 只包含 `content`、`structure`、`language`、`conventions` 四个简短描述。 |
| `teacher_requirements` | string 或 null | 家长提供的老师要求摘要，可为空。 |

不保存字段：

- 作文全文。
- 原图。
- 完整 OCR。
- 学校。
- 班级。
- 家庭住址。
- 家长身份信息。
- 孩子真实姓名。
- 与写作指导无关的信息。

## CLI

脚本位置：

```bash
python3 scripts/manage_profiles.py --store-dir STORE_DIR <子命令>
```

`STORE_DIR` 是唯一本地数据边界。JSON 输入必须位于该目录内。

| 子命令 | 用途 | 确认要求 |
| --- | --- | --- |
| `settings-get` | 读取设置，包括进阶版提示状态。 | 无。 |
| `settings-set --settings SETTINGS_JSON` | 写入完整设置。 | 设置中的隐私确认字段必须为 true 才能开启档案。 |
| `get` | 读取档案。 | 档案必须已启用。 |
| `append --review REVIEW_JSON --confirmed` | 追加批改摘要。 | 必须带 `--confirmed`。 |
| `update-review --review-id ID --review REVIEW_JSON --confirmed` | 替换某次摘要。 | 必须带 `--confirmed`，且 `review_id` 一致。 |
| `delete-review --review-id ID` | 删除单次记录。 | 需要精确 ID；执行前由 Skill 向家长确认。 |
| `delete-profile --confirm-delete` | 删除整档。 | 必须带 `--confirm-delete`。 |
| `export --output OUTPUT_JSON` | 导出便携档案。 | 档案必须已启用。 |
| `import --input PORTABLE_JSON --confirmed` | 导入档案。 | 必须带 `--confirmed`；同名或已有档案时拒绝覆盖。 |

## 导出格式

```json
{
  "schema_version": "parent-growth-profile/1",
  "parent_settings": {},
  "growth_profile": {}
}
```

导入时执行严格字段白名单和类型校验。未知字段、多余字段或不合法类型直接拒绝，不自动补值。
