Scripts for kg-note-method-obsidian.

## checklist-generator.py
生成执行清单 + 检查清单文件。
```
python scripts/checklist-generator.py <任务名> <步1> [步2...]
```
自动追加"删除本任务2个清单文件"为最后一步，检查清单 bitmask 同步。

## yaml-validator.py
YAML frontmatter 校验。支持：
- 概念/某物/skill/关系 类型检查
- frontmatter 开闭确认
- 禁止字段检查（type/[[links]/related_fragments）
- agent memory 碎片专用检查（summary必需）
- Git Bash 路径兼容
```
python scripts/yaml-validator.py <文件.md>
```

## enrichment.py
补完计划 — 将搜索结果格式化为 KG 标准段落，追加到笔记。
```
echo "内容" | python scripts/enrichment.py <笔记.md> --stdout
python scripts/enrichment.py <笔记.md> --text "补充内容"
```
根据笔记类型自动匹配格式（概念→来源, 某物→补充信息, 关系→单句）。
