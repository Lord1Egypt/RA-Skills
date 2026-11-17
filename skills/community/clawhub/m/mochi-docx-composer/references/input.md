# Action contract

create: title, sections:[{heading,paragraphs:[string],bullets:[string],table:[[string]]?}]. <=100 sections, <=200 paragraphs or bullets per section, <=1000 table rows/10 columns; rows need equal width. inspect: file (DOCX <=16 MiB, <=32 MiB unpacked), returns paragraph text/table count/hash and rejects macro/DTD content. New DOCX has A4 pages, named Title/Heading1 styles and bordered tables; bullets are visual bullet paragraphs, not editable numbering definitions.

## Request example

```json
{
  "action": "create",
  "title": "项目简报 / Project Brief",
  "sections": [
    {
      "heading": "进展 / Progress",
      "paragraphs": [
        "这是虚构示例。This is a fictional sample."
      ],
      "bullets": [
        "Review the draft"
      ],
      "table": [
        [
          "Item",
          "Status"
        ],
        [
          "Demo",
          "Ready"
        ]
      ]
    }
  ]
}
```

## Runtime and boundaries

Python 3.10+ standard library. Paths must be relative to the active workspace; absolute paths, parent traversal, symbolic links and junctions are rejected. This is a path guard, not OS-level isolation: retain the host container/sandbox. A helper field does not grant permission to access another account or send information.

Verify the generated file in Word/LibreOffice or an available renderer before claiming visual layout is approved. Does not edit tracked changes, preserve an existing template, embed images, or export PDF. Inspection is structural, not visual verification.
