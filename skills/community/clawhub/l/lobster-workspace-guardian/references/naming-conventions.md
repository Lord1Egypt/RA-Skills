# Naming Conventions

## Directory Names

```
projects/YYYYNNNN_project-name/
  YYYY = year (e.g., 2026)
  NNNN = sequential number from 0001 (yearly reset)
```

### Rules

- No spaces — use `-` (hyphen) as separator
- No Chinese characters in directory or file names
- All lowercase, except uppercase allowed in conventions (YYYY, NNNN)

---

## Output File Naming

```
{short-description}_{version}.{ext}

Examples:
  enterprise-growth-transition_v1.md       ← first draft
  enterprise-growth-transition_v2.md       ← revision
  enterprise-growth-transition_final.md    ← final published version
  enterprise-growth-transition_final.html  ← final rendered HTML
  enterprise-growth-transition_preview.html ← preview (delete after publish)
```

### Version Suffix Rules

| Suffix | Meaning |
|---|---|
| `_v1` | First draft |
| `_v2` | Revision (increment per revision) |
| `_final` | Final published/released |
| `_preview` | Temporary preview, delete after publish |

---

## Script Naming

```
{verb}_{object}.{ext}

Examples:
  generate_report.py
  validate_workspace.py
  update_news.py
```

---

## Memory / Log Files

```
memory/YYYY-MM-DD.md           ← daily log
memory/YYYY-MM-DD-HHMM.md      ← milestone entry

.temp/temp_{uuid}.json         ← temporary search result
.temp/temp_{uuid}.txt          ← temporary batch output
```

---

## What NOT to Do

- ❌ `我的文件.txt` (Chinese characters)
- ❌ `final report v3 (2).docx` (spaces + parentheses)
- ❌ `新建文件夹` (default Chinese folder name)
- ❌ `output/随便起的名字.html` (no context)
