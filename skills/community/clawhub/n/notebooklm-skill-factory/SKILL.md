---
name: notebooklm-skill-factory
description: >-
  Orchestrate NotebookLM research into SKILL.md generation and Claude Code validation in a single automated pipeline.
  Use when user asks to create a new Claude Code skill from source materials (PDFs, articles, YouTube, URLs),
  batch-produce skills, or convert domain knowledge into reusable skills.
  Trigger phrases -- create a skill for X, make me a skill that does X, turn this into a skill, generate a skill from these sources, build a skill factory pipeline.
  NOT for manual skill editing (use skill-creator) or NotebookLM-only tasks (use notebooklm directly).
---

# NotebookLM Skill Factory

Orchestrate the full pipeline: NotebookLM source ingestion → structured SKILL.md extraction → write to skills directory → validate → test → iterate.

## Prerequisites Check

Before the pipeline, verify NotebookLM is authenticated:

```bash
notebooklm status || notebooklm login
```

If `notebooklm login` opens a browser, tell user to complete Google OAuth and press ENTER in their terminal.

## Pipeline

### Phase 1: Setup & Source Ingestion

1. **Create a dedicated notebook** for this skill:
   ```bash
   notebooklm create "Skill: {skill-name}" --json
   ```
   Parse the notebook `id` from JSON output.

2. **Collect sources from user.** Ask:
   > "What sources should this skill be based on? Give me URLs, local file paths, YouTube links — anything high-quality and specific to this domain."

   If the user doesn't have sources ready, suggest:
   - Official documentation URLs
   - Well-known books/articles on the topic (user can provide PDFs)
   - YouTube tutorials/channels specializing in the area

3. **Add sources** (use `-n <notebook_id>` for all subsequent commands):
   ```bash
   notebooklm source add "https://..." -n <id> --json
   notebooklm source add ./local-file.pdf -n <id> --json
   ```
   Capture each `source_id`.

4. **Wait for indexing** — spawn a background agent to avoid blocking:
   ```bash
   notebooklm source wait <source_id> -n <id> --timeout 600
   ```
   For multiple sources, wait them all. If any source fails indexing (exit code 1), log a warning but continue with remaining sources.

### Phase 2: Extract SKILL.md

1. **Load the extraction prompt template:**
   Read [references/skill-extraction-prompt.md](references/skill-extraction-prompt.md). Replace `{USER_INTENT}` with the user's original request.

2. **Query NotebookLM** against all indexed sources:
   ```bash
   notebooklm ask "{extraction_prompt}" -n <id> --json
   ```

3. **Parse the output** into a clean SKILL.md:
   ```bash
   echo '<json_output>' | python3 scripts/parse-skill-output.py > /tmp/skill-output.md
   ```
   Or save the JSON to a temp file first, then pipe.

4. **Validate basic structure:**
   - Starts with `---` YAML frontmatter
   - Has `name:` and `description:` fields
   - Body is non-empty after frontmatter
   If validation fails, re-prompt NotebookLM with more specific instructions.

### Phase 3: Install & Validate

1. **Create the skill directory:**
   ```bash
   mkdir -p ~/.claude/skills/{skill-name}
   ```

2. **Write the SKILL.md:**
   Move the parsed output to `~/.claude/skills/{skill-name}/SKILL.md`

3. **Run skill-creator validation** (via Skill tool):
   Invoke `skill-creator` with: "Validate the skill at ~/.claude/skills/{skill-name}/ and fix any issues found. Run package_skill.py to check for errors."

4. **Run skill-vetter security check** (via Skill tool):
   Invoke `skill-vetter` with: "Review the skill at ~/.claude/skills/{skill-name}/ for security issues."

### Phase 4: Test & Iterate

1. **Test the skill** by invoking it with a realistic prompt matching its intended use case.

2. **Collect failures:**
   - Did the skill trigger correctly?
   - Did it produce correct output?
   - Any hallucinations or gaps?

3. **If issues found, iterate:**
   - Feed the failure description back to NotebookLM:
     ```bash
     notebooklm ask "The SKILL.md generated earlier has this issue: {failure}. Based on the sources, rewrite it to fix this. Output complete corrected SKILL.md in a markdown code block." -n <id> --json
     ```
   - Parse again and overwrite SKILL.md
   - Re-test

4. **Repeat** until the skill passes a real usage test.

## Error Recovery

| Situation | Action |
|-----------|--------|
| NotebookLM auth expired | Run `notebooklm login`, retry |
| Source indexing failed | Skip that source, warn user, continue |
| Extraction prompt returned empty | Check if sources are indexed (status=ready), re-query with `--new` flag |
| Generated SKILL.md fails validation | Send failure description back to NB for rewrite (Phase 4 iteration) |
| NB rate limited | Wait 5-10 min, retry once |

## Source Quality Guidelines

Remind users:
- One notebook per skill, one theme per notebook
- 3-10 high-quality sources work better than 20+ mixed ones
- Official docs > blog posts > YouTube transcripts
- If the skill covers multiple unrelated domains, create separate notebooks for each
- After generation, user should be the final human reviewer — check tone, logic, completeness

## Completing the Pipeline

When the skill passes testing, report:
- Skill name and path (`~/.claude/skills/{name}/`)
- Number of sources used
- Number of iteration rounds
- Final test result summary
