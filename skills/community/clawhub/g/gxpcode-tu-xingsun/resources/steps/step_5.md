# Step 5 — 通知

```bash
python "${SKILL_DIR}/scripts/step5_notify.py" gxpcode_data [output_dir]
```
- `output_dir` 可选（第二参数），报告输出到此目录；不传则用当前工作目录

## 目的

汇总 S4 分析结果，生成 GxpCode-制药法规跟踪报告（Markdown + PDF），更新 history.json。

## 输入

- `gxpcode_data/s4/`：S4 分析结果（含 summary / tags / applicability / reason / needs_manual_review）
- `resources/templates/report.md`：报告框架模板
- `resources/templates/report_group.md`：分组标题模板
- `resources/templates/report_item.md`：法规条目卡片模板（10 字段）

## 输出

- `{output_dir}/s5_report_{date}.md`：Markdown 报告
- `{output_dir}/s5_report_{date}.pdf`：PDF 报告（微软雅黑，A4）
- `{SKILL_DIR}/gxpcode_data/history.json`：更新历史记录（按 source 分组，title+url 去重）

## 报告结构

| 字段 | 来源 |
|------|------|
| 发布机构 | 从 source 推导（CDE/NMPA/PIC/S） |
| 发布日期 | S4 `date` |
| 文号 | 正则提取 `2026年第XX号` |
| 相关主题 | S4 `tags` |
| 适用企业 | config.yaml `enterprise_type` |
| 摘要 | S4 `summary` |
| 链接 | S4 `url`（可点击超链接） |
| 附件本地路径 | S4 `attachment`（完整绝对路径） |
| 来源 | S4 `source` |

按 applicability 分组展示：🔴 直接适用 / 🟡 潜在相关 / 🟢 仅供参考 / ⚠️ 待人工复核。
