# Feishu Model

Feishu Base is the default v1 backend.

## Standard tables

The Feishu bootstrap should create these tables:

- `班级配置`
- `学生主档`
- `考试批次`
- `成绩明细`
- `成长事件`
- `家校沟通`
- `座位安排`
- `值日安排`
- `班委任命`
- `产物索引`

## Field design principles

- keep `学生主档` as the source of truth for student identity
- use link fields such as `student_ref` and `exam_ref` instead of plain name text
- keep score data in long-form rows inside `成绩明细`
- keep conduct, duty, and learning observations in `成长事件`
- never default to overwriting an existing Base

## Existing Base inspection

When a user provides an existing Base:

1. inspect with `tools/migration_inspector.py`
2. classify it
3. if it is a subject-teacher base, recommend copy-and-refactor

Typical subject-teacher signals:

- `学生信息` mixes profile fields and score columns
- `学生记录` stores generic activity notes
- student references are plain text instead of relation fields

## Views

Create at least one grid view per table. Recommended named views:

- `学生总览`
- `全科成绩`
- `德育与班务`
- `家校沟通`
- `当前座位`
- `当前值日`
- `当前班委`
- `产物归档`

## Dashboard stance

Dashboard creation is optional in v1.

- It is acceptable to create empty dashboard shells
- It is not required to fully configure chart blocks in the first bootstrap pass
