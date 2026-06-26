# Input formats

## 1. Standard mode

Use when you already have a full request object.

Required top-level fields:
- `documentType`: `docx` | `xlsx` | `pptx`
- `contentSpec`: object

Optional common fields:
- `templateId`
- `title`
- `purpose`
- `output.filename`
- `output.directory`

Example:

```json
{
  "documentType": "docx",
  "templateId": "meeting_minutes_v1",
  "title": "Office 评审会纪要",
  "purpose": "内部存档",
  "contentSpec": {
    "sections": [
      {
        "heading": "一、讨论要点",
        "bullets": ["确认 Python 路线", "继续 Skill 化封装"]
      }
    ]
  }
}
```

## 2. Business mode

Use when the request matches a built-in template family.

Kinds:
- `word-report`
- `meeting-minutes`
- `excel-tracker`
- `project-plan`
- `ppt-brief`
- `project-status-brief`

In business mode, the input file can be either:
- a full object containing `contentSpec`, or
- a direct `contentSpec` object

Example content file for `meeting-minutes`:

```json
{
  "contentSpec": {
    "sections": [
      {
        "heading": "一、会议基本信息",
        "paragraphs": ["时间：2026-03-15", "地点：线上"]
      },
      {
        "heading": "二、结论",
        "bullets": ["继续扩展模板", "准备上层接入"]
      }
    ]
  }
}
```

## 3. ContentSpec shapes

### Word

```json
{
  "sections": [
    {
      "heading": "章节标题",
      "paragraphs": ["段落1"],
      "bullets": ["要点1"],
      "table": [["列1", "列2"], ["值1", "值2"]],
      "images": [{"path": "/absolute/path/demo.png", "widthInches": 5.5}]
    }
  ]
}
```

### Excel

```json
{
  "sheets": [
    {
      "name": "计划",
      "columns": ["任务", "负责人", "状态"],
      "rows": [["Skill 化封装", "小程", "进行中"]]
    }
  ]
}
```

### PPT

```json
{
  "slides": [
    {
      "title": "项目背景",
      "layout": "content",
      "bullets": ["要点1", "要点2"]
    },
    {
      "title": "里程碑",
      "layout": "table",
      "table": [["阶段", "状态"], ["开发", "完成"]]
    },
    {
      "title": "产品截图",
      "layout": "image",
      "image": {"path": "/absolute/path/demo.png"},
      "bullets": ["图片说明"]
    }
  ]
}
```
