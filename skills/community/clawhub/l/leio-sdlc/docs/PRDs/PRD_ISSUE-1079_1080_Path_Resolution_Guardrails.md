---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1079 & 1080 Path Resolution Guardrails

## 1. Context & Problem (业务背景与核心痛点)
The SDLC process suffers from a "CWD drift" issue across the OpenClaw native tools. The native file tools (`read`, `write`, `edit`) resolve paths against the global root `/root/.openclaw/workspace`, ignoring the project-specific workspace directory passed down via the orchestrator. Because PR Contracts and target working sets naturally use relative paths for readability and portability, downstream agents (Coder, Reviewer) frequently encounter "File not found" errors or mistakenly modify the wrong paths, wasting tokens and occasionally breaking the pipeline.
Additionally, there is a hidden bug in the `reviewer` prompt inside `config/prompts.json`. The `spawn_reviewer.py` script passes an absolute path for `--out-file`, but the prompt hardcodes `'{workdir}/{out_file}'`. This creates a nested absolute path (e.g., `/root/.../leio-sdlc/root/.../Review_Report.md`), causing Orchestrator to fail to find the generated `Review_Report.md` and triggering a false State 5 crash loop.

## 2. Requirements & User Stories (需求定义)
1. **Maintain Clean PRDs**: PRDs and PR Contracts must continue to use portable relative paths for readability and environment agnosticism.
2. **Explicit CWD Declaration**: The PRD template must explicitly declare its context working directory in the frontmatter.
3. **Agent Mental Model Enforcement**: The system prompts for Coder and Reviewer must be injected with a severe, explicit instruction defining the CWD drift tooling quirk and mandating the `{workdir}/` prefix for all tool calls.
4. **Fix Reviewer Report Pathing Bug**: The `reviewer` prompt must be corrected to use exactly `'{out_file}'` instead of `'{workdir}/{out_file}'`, so absolute paths are not mangled.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
We will solve this entirely via Prompt Engineering and Context Boundaries, rather than engineering a heavy wrapper around native tools. 
- **`skills/pm-skill/TEMPLATES/PRD.md.template`**: Add a new YAML frontmatter field `Context_Workdir: <Project_Root>` to document the intended root for relative paths.
- **`config/prompts.json`**: Update the `coder` and `reviewer` prompts to include the "CRITICAL TOOLING QUIRK" rule. This rule explicitly tells the agents to manually prepend `{workdir}/` to all relative file paths when using native tools. Additionally, in the `"reviewer"` prompt, fix the string `'{workdir}/{out_file}'` by removing `{workdir}/`, leaving just `'{out_file}'`.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: PRD Template Context**
  - **Given** The PM Skill generates a new PRD scaffold
  - **When** The file is written
  - **Then** The frontmatter contains the `Context_Workdir: <Project_Root>` placeholder.
- **Scenario 2: System Prompts Contain Tooling Quirk Rule**
  - **Given** The `config/prompts.json` is deployed
  - **When** Orchestrator builds the prompt for Coder or Reviewer
  - **Then** The prompt strictly commands them to prepend `{workdir}/` when using `read`, `write`, or `edit` tools.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Unit Testing**: Minimal. The changes are strictly text modifications to JSON configs and Markdown templates. 
- **E2E Validation**: The very next SDLC run using these updated prompts will inherently test this behavior. If the Coder can successfully edit a file in a sub-project using the `{workdir}/` prefix, the test passes.

## 6. Framework Modifications (框架防篡改声明)
- `config/prompts.json` (Internal to `leio-sdlc` workspace, absolute path: `/root/.openclaw/workspace/projects/leio-sdlc/config/prompts.json`)
- `skills/pm-skill/TEMPLATES/PRD.md.template` (Internal to `leio-sdlc` workspace, absolute path: `/root/.openclaw/workspace/projects/leio-sdlc/skills/pm-skill/TEMPLATES/PRD.md.template`)

---
## 7. HARDCODED CONTENT (CODER MUST COPY EXACTLY)

> **[CRITICAL INSTRUCTION TO CODER - ANTI-PITFALL GUIDE]**
> Before this fix is applied, YOU are currently vulnerable to the CWD drift bug. You MUST manually prepend the absolute workdir path (i.e., `/root/.openclaw/workspace/projects/leio-sdlc/`) to all relative file paths when using your `read`, `edit`, or `write` tools during this specific task. 
> To be absolutely clear, you will modify these specific files using these exact absolute paths:
> 1. `/root/.openclaw/workspace/projects/leio-sdlc/config/prompts.json`
> 2. `/root/.openclaw/workspace/projects/leio-sdlc/skills/pm-skill/TEMPLATES/PRD.md.template`

**1. Content for `config/prompts.json`:**
(Insert the following warning paragraph into both the `"coder"` and `"reviewer"` values in `config/prompts.json`, right after the `ATTENTION: Your root workspace is rigidly locked to {workdir}...` sentence and before the `--- PLAYBOOK ---` section.)

```json
"⚠️ CRITICAL TOOLING QUIRK ⚠️\nThe OpenClaw native file tools (`read`, `write`, `edit`) suffer from CWD drift. They execute from the global root, NOT your project root. YOU MUST NOT try to guess the absolute path. YOU MUST read the `{workdir}` variable passed in this prompt, and manually prepend it to EVERY relative file path you operate on. (e.g., `{workdir}/src/main.py`). If a tool fails with 'File not found' or 'Could not find edits', you forgot the `{workdir}/` prefix."
```

**2. Fix nested path bug in `config/prompts.json`:**
Inside the `"reviewer"` prompt, locate this exact sentence:
`You MUST use the write tool to save your final evaluation into exactly '{workdir}/{out_file}' using the provided template.`
Change it to:
`You MUST use the write tool to save your final evaluation into exactly '{out_file}' using the provided template.`

**3. Content for `skills/pm-skill/TEMPLATES/PRD.md.template`:**
(Ensure the frontmatter at the very top of the template looks exactly like this:)
```markdown
---
Affected_Projects: [List the target projects here, e.g., leio-sdlc, AMS]
Context_Workdir: <Project_Root>
---
```