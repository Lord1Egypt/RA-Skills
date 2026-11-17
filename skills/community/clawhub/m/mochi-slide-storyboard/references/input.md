# Action contract

create: title, language(zh-CN/en, default zh-CN), slides:[{title,bullets:[string],notes?}]. 1..50 slides, <=8 bullets/slide, <=700 characters/bullet. Output slides.html and outline.md plus report. All text escaped; no JavaScript or external fonts/images. Browser print uses landscape pages and hides notes/navigation. Not a PPTX writer; long content still requires print-preview review.

## Request example

```json
{
  "action": "create",
  "title": "项目介绍",
  "language": "zh-CN",
  "slides": [
    {
      "title": "目标",
      "bullets": [
        "减少重复工作",
        "保留可核对的结果"
      ],
      "notes": "先介绍使用场景。"
    },
    {
      "title": "下一步",
      "bullets": [
        "确认方案",
        "完成试用"
      ]
    }
  ]
}
```

## Runtime and boundaries

Python 3.10+ standard library. Paths must be relative to the active workspace; absolute paths, parent traversal, symbolic links and junctions are rejected. This is a path guard, not OS-level isolation: retain the host container/sandbox. A helper field does not grant permission to access another account or send information.

Use when the user accepts an HTML presentation. If they explicitly need PPTX, use an available PPTX tool or explain the missing capability. Check browser and print layout; HTML generation alone is not visual approval.
