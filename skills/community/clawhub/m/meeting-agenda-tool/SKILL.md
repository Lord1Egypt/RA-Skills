---
name: meeting-agenda
description: >
  This skill should be used when the user provides meeting-related information
  (title, venue, time, agenda items, participants, etc.) and wants to generate
  a formatted meeting agenda document. It produces both a Word (.docx) and PDF
  file following a standardized Chinese government/enterprise meeting agenda
  format with correct fonts: Heiti for headings, FangSong GB2312 for body text,
  and Kaiti GB2312 for organizational unit headers.
---

# Meeting Agenda Generator

## Purpose

Generate professional Chinese meeting agenda documents in Word (.docx) and PDF formats.
Apply the standard font and layout conventions described in `references/template.md`.

## Trigger Conditions

Use this skill when the user:
- Provides meeting information (title, time, location, agenda, participants) and asks to generate an agenda
- Mentions keywords like "会议议程"、"议程安排"、"生成议程"、"帮我做个会议议程"
- Provides raw meeting details and asks for a formatted document output

## Workflow

### Step 1: Collect Meeting Information

Ask the user to provide (or extract from their message):
- **会议名称** (Meeting title)
- **环节列表** (Session list), for each session:
  - 环节名称 (Session name)
  - 时间 (Time, e.g. "2026年4月2日（星期四）09:00-10:00")
  - 地点 (Location)
  - 内容 (Content description, optional for simple sessions)
  - 主持人 (Host, optional)
  - 议程 (Agenda items list, optional)
  - 参会人员 (Participants by organization, optional)
    - 单位名称 (Organization name)
    - 成员列表: 姓名 + 职务 + 补充说明(optional)

If any critical fields are missing, ask the user before proceeding.
Use `references/template.md` for exact field names, structure, and JSON format.

### Step 2: Build the JSON Data File

Construct a JSON file following the schema in `references/template.md`.
Save it as a temporary file, e.g. `agenda_input.json`, in a working directory
(suggest using the user's workspace or a temp folder).

Example minimal JSON:
```json
{
  "title": "XXX合作座谈会议议程",
  "filename": "XXX合作座谈会议议程",
  "sections": [
    {
      "name": "产品演示",
      "time": "2026年4月2日（星期四）09:00-10:00",
      "location": "XX楼会议室",
      "content": "演示核心功能"
    }
  ]
}
```

### Step 3: Run the Generation Script

Execute `scripts/generate_agenda.py` with the JSON data file:

```bash
python <skill_base_dir>/scripts/generate_agenda.py \
  --data <path_to_agenda_input.json> \
  --output <output_directory>
```

- `<skill_base_dir>` is the absolute path to this skill directory
  (typically `~/.workbuddy/skills/meeting-agenda`)
- `<output_directory>` is where the files will be saved
  (use the user's workspace directory or a subdirectory they specify)

The script will:
1. Auto-install `python-docx` and `reportlab` if not present
2. Generate `<filename>.docx` (Word document)
3. Generate `<filename>.pdf` (PDF document)

### Step 4: Deliver Results

After generation:
1. Confirm both files exist
2. Report the file paths to the user
3. Use `deliver_attachments` tool to attach both `.docx` and `.pdf` files

## Font & Style Reference

Refer to `references/template.md` for the complete font specification:
- Meeting title: FangSong GB2312 (仿宋_GB2312), 24pt (小一), bold, centered
- Section headings (including 人员): Heiti (黑体), 16pt, bold, left-aligned; numbered with Chinese numerals (一、二、三…)
- Field labels (时间/地点/内容/议程 etc.): Heiti (黑体), 16pt, bold
- Body text (field values, agenda items): FangSong GB2312 (仿宋_GB2312), 16pt
- Organization unit headers: Kaiti GB2312 (楷体_GB2312), 16pt, bold, preceded by two full-width spaces (　　)
- Member lines: FangSong GB2312, 16pt, NO leading dash; name and title separated by two full-width spaces (　　)

**人员排列规则：**
- 每个 section 如含 `persons` 字段，人员独立作为一个带序号的一级标题（如"三、人员"），序号接续前面环节编号

## Error Handling

- If PDF generation fails (missing fonts or reportlab issues), still deliver the Word file and explain the PDF issue
- If the user's system lacks Chinese fonts, the Word file will still display correctly when opened in Word; the PDF may show fallback fonts
- If `python-docx` install fails, ask the user to run `pip install python-docx reportlab` manually
