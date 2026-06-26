# Artifact Generator

Use this prompt when the user asks for a concrete output file.

## Supported outputs in v1

- `.docx`
  - 家访记录
  - 班级通知
  - 学生谈话记录
- `.xlsx`
  - 座位表
  - 值日表
  - 班委表
  - 扣分汇总表
- `.pptx`
  - 家长会 PPT

## Workflow

1. Confirm the workspace is initialized.
2. Query structured data first.
3. Identify the artifact family:
   - arrangement artifact
   - presentation / communication artifact
3. Confirm which template or source materials should be used.
4. Generate the local file.
5. Register it:

```bash
python3 tools/artifact_registry.py register ...
```

6. If the user wants cloud sync, then sync and update the registry entry.

## Parent meeting PPT guidance

For 家长会 PPT in v1:

- use a text-defined outline instead of depending on a bundled `.pptx` template
- pull both score records and daily performance / conduct records into the slide plan
- prefer sections such as:
  - 封面与会议主题
  - 教师与班级概况
  - 班委/科代表/班级文化
  - 纪律、作业、宿舍等运行现状
  - 考试与成绩分析
  - 学习方法建议
  - 给家长的建议
  - 学科教师补充建议
- if the user has prior local slides, treat them as outline references only
- do not keep the original Office file inside the skill directory

## Arrangement artifact guidance

For 排座表 or 值日表:

- gather the arrangement goal first
- confirm which attributes should drive the arrangement, such as:
  - score
  - gender
  - height
  - dorm or group
  - conduct or discipline constraints
- generate from structured student data instead of manual spreadsheet edits

## Rules

- do not generate artifacts directly from vague chat context if structured data is missing
- call out missing templates or missing data explicitly
- the registry must record local path, type, timestamp, and optional remote link
