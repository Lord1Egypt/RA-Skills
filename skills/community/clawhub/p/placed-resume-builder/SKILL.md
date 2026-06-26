---
name: placed-resume-builder
description: This skill should be used when the user wants to "build a resume", "create a resume", "update my resume", "export resume as PDF", "change resume template", "list my resumes", "download resume", "switch template", or wants to manage resumes using the Placed career platform at placed.exidian.tech.
version: 1.0.0
metadata:
  { "openclaw": { "emoji": "📄", "homepage": "https://placed.exidian.tech" } }
tags: "resume,resume-builder,cv,resume-creator,pdf-resume,resume-template,career,job-search,placed,exidian,ai-resume,resume-generator"
---

# Placed Resume Builder

Build and manage professional resumes via the Placed API. No MCP server required — all calls are made directly with curl.

## API Key

Load the key from `~/.config/placed/credentials`, falling back to the environment:

```bash
if [ -z "$PLACED_API_KEY" ] && [ -f "$HOME/.config/placed/credentials" ]; then
  source "$HOME/.config/placed/credentials"
fi
```

If `PLACED_API_KEY` is still not set, ask the user:

> "Please provide your Placed API key (get it at https://placed.exidian.tech/settings/api)"

Then save it for future sessions:

```bash
mkdir -p "$HOME/.config/placed"
echo "export PLACED_API_KEY=<key_provided_by_user>" > "$HOME/.config/placed/credentials"
export PLACED_API_KEY=<key_provided_by_user>
```

## How to Call the API

```bash
placed_call() {
  local tool=$1
  local args=${2:-'{}'}
  curl -s -X POST https://placed.exidian.tech/api/mcp \
    -H "Authorization: Bearer $PLACED_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$tool\",\"arguments\":$args}}" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result']['content'][0]['text'])"
}
```

## Available Tools

| Tool                     | Description                                |
| ------------------------ | ------------------------------------------ |
| `list_resumes`           | List all resumes                           |
| `create_resume`          | Create a new resume                        |
| `get_resume`             | Get resume by ID (or most recent if no ID) |
| `update_resume`          | Update any resume section                  |
| `get_resume_schema`      | See all available fields and formats       |
| `list_resume_templates`  | Browse available templates                 |
| `get_template_preview`   | Preview a specific template                |
| `change_resume_template` | Switch resume template                     |
| `get_resume_pdf_url`     | Get PDF download URL (expires 15 min)      |
| `get_resume_docx_url`    | Get Word document download URL             |
| `export_resume_json`     | Export resume as JSON                      |
| `export_resume_markdown` | Export resume as Markdown                  |

## Usage Examples

**List all resumes:**

```bash
placed_call "list_resumes"
```

**Create a resume:**

```bash
placed_call "create_resume" '{"title":"Senior Engineer Resume","target_role":"Staff Engineer"}'
```

**Update resume sections:**

```bash
placed_call "update_resume" '{
  "resume_id": "res_abc123",
  "summary": "Principal SRE with 10+ years...",
  "skills": [{"name":"Infrastructure","keywords":["Kubernetes","Terraform","AWS"]}]
}'
```

**Get PDF download URL:**

```bash
placed_call "get_resume_pdf_url" '{"resume_id":"res_abc123"}'
```

**Change template:**

```bash
# First list templates
placed_call "list_resume_templates"
# Then apply one
placed_call "change_resume_template" '{"resume_id":"res_abc123","template_id":"onyx"}'
```

**Export as Markdown:**

```bash
placed_call "export_resume_markdown" '{"resume_id":"res_abc123"}'
```

## Resume Sections

All sections are optional and can be updated independently via `update_resume`:

- `basics` — name, email, phone, headline, location
- `summary` — professional overview
- `experience` — work history with company, position, date, bullets
- `education` — degrees, institutions, dates
- `skills` — skill groups with keywords
- `languages` — language proficiencies
- `certifications` — professional certs with issuer and date
- `awards` — honors and recognition
- `projects` — personal/professional projects
- `publications` — articles, papers, books
- `references` — professional references
- `volunteer` — volunteer experience
- `interests` — hobbies and interests
- `profiles` — LinkedIn, GitHub, portfolio links

## Tips

- Call `get_resume_schema` to see exact field formats before updating
- Quantify achievements with metrics (numbers, percentages, dollars)
- Use action verbs at the start of bullet points
- Mirror job description language for better ATS matching
- Use `placed-resume-optimizer` skill to check ATS compatibility after building
