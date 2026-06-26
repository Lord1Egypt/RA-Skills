---
name: oh-my-skill
description: Automatically generate and save a reusable skill after AI agent successfully completes a complex task involving 5 or more tool calls. Use this skill whenever a multi-step workflow has just been completed successfully — such as document creation pipelines, data transformation flows, research-and-write tasks, multi-file editing workflows, or any agentic sequence that involved planning, tool use, and structured output. Trigger this skill proactively at the end of complex task completions even if the user hasn't asked for it, offering to save the workflow as a reusable skill. Also trigger when users say things like "save this as a skill", "make this repeatable", "turn this into a skill" or "oh-my-skill".
metadata:
  openclaw:
    requires:
      bins:
        - python
---

# oh-my-skill: Auto-Skill Generator

Automatically captures and packages successful complex workflows as reusable skills.  
*Warning*: Make sure your session doesn't contain any highly private data. If it's already been sent to Claude, then that's it.  
you could modify the Desensitize process to match your scence/case.

## When to Trigger

Trigger **proactively** after completing any task that involved:
- 5 or more distinct tool calls
- A clear sequence of steps (plan → execute → verify)
- A structured or repeatable output (file, report, transformation, research summary)
- Tool combinations that aren't obvious and took iteration

After such a task completes successfully, say something like:
> "That was a fairly involved workflow — want me to save it as a reusable skill so you can repeat it easily next time?"

If the user says yes, or explicitly asks to generate a skill, proceed with the steps below.

---

## Workflow: Capturing a Skill from a Completed Task

### Step 1: Analyze the Session

Review the current conversation and extract:

1. **What was accomplished** — the goal and final output
2. **The tool call sequence** — ordered list of tools used and why
3. **Key decisions made** — branch points, error recovery, formats chosen
4. **Inputs required** — what the user had to provide (files, preferences, constraints)
5. **Output format** — what was produced and where it was saved

Look for patterns: What made this hard? What would be needed to repeat it?

### Step 1b: Desensitize the Session

Before extracting any content, run the session text through the masking script to strip sensitive data:

```bash
python3 ~/.openclaw/workspace/skills/oh-my-skill/scripts/desensitize.py session.txt clean_session.txt
```

Or pipe text directly:
```bash
echo "my text" | python3 ~/.openclaw/workspace/skills/oh-my-skill/scripts/desensitize.py
```

The script applies two layers of masking:

**Literal replacements** (named individuals → generic labels):
- `Bill Gates` → `A man`
- Add more entries in the `LITERAL_REPLACEMENTS` list in `desensitize.py`

**Pattern-based masking** (regex, auto-detected)

Use the **cleaned text** as the source for all subsequent steps.

### Step 2: Draft the Skill

Write a `SKILL.md` with:

```
---
name: <kebab-case-name>
description: <What it does, when to trigger. Be specific and "pushy" — list all the user phrases and contexts that should trigger this skill.>
---

# <Skill Title>

<One-paragraph summary of what this skill does and why it's valuable.>

## Inputs

List what the user must provide:
- File paths / uploads
- Preferences or configuration
- Any required context

## Workflow

Step-by-step instructions Claude should follow, referencing tool calls and decision points extracted from the session.

### Step 1: ...
### Step 2: ...
...

## Output

What gets produced, in what format, saved where.

## Notes / Edge Cases

Anything learned from the original run: gotchas, fallbacks, format quirks.
```

**Naming conventions:**
- Use `kebab-case` for the name
- Keep it specific: `pdf-to-summary-docx` not `document-helper`
- Reflect the *domain + action*: `research-and-cite`, `excel-data-cleaner`, `slide-deck-from-outline`
- **Always append a 4-digit UUID suffix** to the name: e.g. `pdf-to-summary-docx-4f2a`, `excel-data-cleaner-9c31`
- Generate the suffix randomly: `python3 -c "import uuid; print(str(uuid.uuid4())[:4])"`

### Step 3: Save the Skill

Save to `~/.openclaw/workspace/skills/<skill-name>/SKILL.md`.

If the task also used supporting scripts or reference files, save those under:
```
~/.openclaw/workspace/skills/<skill-name>/scripts/
~/.openclaw/workspace/skills/<skill-name>/references/
~/.openclaw/workspace/skills/<skill-name>/assets/
```

### Step 4: Confirm with the User

Show the user:
- The skill name and description
- A brief summary of the workflow it captures

Ask: "Does this look right? Want me to adjust the name, description, or any steps?"

---

## Quality Checklist

Before saving, verify:
- [ ] Description is specific enough to trigger reliably (not vague like "helps with files")
- [ ] Workflow steps are ordered and actionable
- [ ] Inputs section lists everything the user must supply
- [ ] Edge cases from the original run are documented
- [ ] Skill name is unique and descriptive

---

## Example Output

After a session where Claude built a Word report from a PDF + web research:

```markdown
---
name: pdf-research-to-docx-report
description: Build a polished Word document report by combining content from an uploaded PDF with live web research. Use this whenever a user uploads a PDF and wants a written report, briefing, or summary that also pulls in current data from the web. Trigger on phrases like "make a report from this PDF", "write me a briefing", "research and write a doc".
---

# PDF + Research → DOCX Report

Combines PDF extraction, web search, and Word document generation into a single pipeline.

## Inputs
- Uploaded PDF file
- Report topic / framing question
- Desired length and tone (optional)

## Workflow

### Step 1: Read the skill files
Load `docx/SKILL.md` for Word generation instructions.

### Step 2: Extract PDF content
Use `bash_tool` to extract text from the PDF via `pdftotext` or Python `pdfplumber`.

### Step 3: Web research
Run 3–5 `web_search` calls to supplement the PDF with current data.

### Step 4: Outline and draft
Combine findings into a structured outline, then write the full report draft.

### Step 5: Generate DOCX
Follow `docx/SKILL.md` instructions to produce a styled Word document.

### Step 6: Present
Copy to `/mnt/user-data/outputs/` and call `present_files`.

## Output
A `.docx` report file, downloadable by the user.
```

---

## Notes

- This skill is self-referential: it was itself generated using the oh-my-skill pattern.
- Keep captured skills focused — one workflow per skill is better than one mega-skill.
- If the session was messy (lots of retries, dead ends), simplify the skill to the *successful path only*.
- If the user ran the same workflow before and already has a skill for it, offer to *update* the existing skill instead of creating a duplicate.
