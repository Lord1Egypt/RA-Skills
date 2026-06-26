---
Affected_Projects: [leio-sdlc]
---

# PRD: Planner_Tech_Lead_Upgrade

## 1. Context & Problem (业务背景与核心痛点)
Currently, the `leio-sdlc` Planner agent functions merely as a "secretary" that splits PRDs into PR Contracts without providing architectural or testing guidance. This leads to two critical failures downstream for the Coder:
1. **Orphaned Files & Path Hallucination:** The Coder guesses where to put new files, often cluttering the root directory.
2. **Missing TDD Discipline:** The Coder doesn't know *how* to test the code, leading to incomplete test coverage or failing CI pipelines.

However, our v1.0 PRD introduced a Waterfall anti-pattern by strictly locking the Coder to explicit paths, which breaks the Coder's autonomy to fix underlying dependencies to make tests pass. We must balance Planner guidance with Coder autonomy using the "Working Set" pattern.

## 2. Requirements & User Stories (需求定义)
- The Planner must be upgraded to a "Tech Lead & QA Architect" persona.
- The Planner must explore the project directory structure before writing contracts.
- The Planner must define a **"Target Working Set"** of files, guiding but NOT strictly locking the Coder.
- The Planner must translate high-level BDD acceptance criteria into precise, language-agnostic TDD blueprints (specifying test file paths and test case names).
- The Coder must be instructed to prioritize the Working Set but retains the freedom to modify necessary dependencies to achieve green tests (Implementation Freedom).

## 3. Architecture & Technical Strategy (架构设计与技术路线)
This is a pure Prompt Engineering and Template Refactoring task. (We rely on the system's default behavior where agents already have native search/read tools enabled; no Python orchestrator code changes are needed to inject tool capabilities.)
- **`TEMPLATES/PR_Contract.md.template`**: 
  - Add a "Target Working Set" section. Instruct the Coder to heavily focus modifications here, while explicitly permitting necessary dependency changes.
  - Upgrade the AC section to a "TDD Blueprint & Acceptance Criteria" section.
- **`playbooks/planner_playbook.md`**: 
  - Inject the "Exploration Phase" (Goal-Oriented Rule: "Before writing the contract, act as an Architect analyzing a new PRD: Ask yourself 'Where should the changes be made based on the project structure?' and 'How do we know the changes are correct?' You MUST use available safe read/search tools to understand the architecture, then provide an architectural-level solution and TDD strategy, leaving the code-level implementation to the Junior Coder").
  - Inject "Working Set Strategy", "QA Architect Persona" (TDD Translation), and "Slice-Failed-PR Protocol".
- **`config/prompts.json`**: Update the `"planner"` prompt to enforce the generation of Working Sets and TDD blueprints, rather than blindly giving complete path freedom without guidance.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1:** Generating a PR Contract
  - **Given** a detailed PRD requesting a new module
  - **When** the Planner processes the PRD
  - **Then** the generated PR_Contract.md contains a specific Target Working Set for modifications and explicit test case signatures to be implemented.
- **Scenario 2:** Coder Path Prioritization & Autonomy
  - **Given** a generated PR Contract with a Target Working Set
  - **When** the Coder executes the task
  - **Then** the Coder heavily focuses its changes on the Working Set, BUT successfully modifies external unlisted dependencies (e.g., config, shared utils) if logically required to make the tests pass, without being artificially blocked by path restrictions.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Core Quality Risk:** The updated prompts might cause the Planner to over-constrain the Coder or hallucinate paths itself if it fails to use the `read`/`exec` tools properly.
- **Test Strategy:** Altering the template structure (e.g., renaming "Acceptance Criteria" to "TDD Blueprint") will break existing agentic smoke tests and linters that rely on regex or hardcoded assertions. 
- **Delegation of Blast Radius:** As the PM, I am highlighting this architectural risk. It is the **Planner's explicit responsibility** during its Exploration Phase to use `exec find` and the native `read` tool to locate the old template headers (e.g., `scripts/lint_pr_contract.sh` or `tests/`), identify the exact files affected, and include them in the PR Contract's Target Working Set. The Coder will then implement the fixes. The final CI pipeline must be 100% green.

## 6. Framework Modifications (框架防篡改声明)
- `/root/.openclaw/workspace/projects/leio-sdlc/TEMPLATES/PR_Contract.md.template`
- `/root/.openclaw/workspace/projects/leio-sdlc/playbooks/planner_playbook.md`
- `/root/.openclaw/workspace/projects/leio-sdlc/config/prompts.json`
- **ALL AFFECTED CI/TEST SCRIPTS**: Specifically `scripts/lint_pr_contract.sh` and any other tests dynamically identified by the Planner during the Exploration Phase.

## 7. Exact Implementation Payloads (精确代码替换清单)
> **[CRITICAL INSTRUCTION TO CODER]** 
> To prevent the "telephone game" effect (hallucinations or paraphrasing), you MUST EXACTLY copy-paste the blocks below into the target files. Do not invent your own prompts.

### 7.1 For `TEMPLATES/PR_Contract.md.template`
Replace sections 2 and 3 with exactly the following:
```markdown
## 2. Target Working Set & File Placement
> **[CRITICAL INSTRUCTION TO CODER]** 
> 1. **NEW FILES:** You are STRICTLY FORBIDDEN to create new files outside of the directories listed below. No orphaned files in the root directory!
> 2. **EXISTING FILES:** You HAVE FULL FREEDOM to modify ANY existing files in the workspace necessary to make the tests pass, but you MUST prioritize the files listed here.

### 2.1 Existing Files to Modify
- [ ] `path/to/existing_file`

### 2.2 New Files to Create
- [ ] `path/to/new_file` (Purpose: ...)

## 3. Implementation Scope (实现细节)
[Detailed logic changes]

## 4. TDD Blueprint & Acceptance Criteria (QA 测试蓝图)
> **[Instruction to Coder]** Implement these test cases exactly in the test files specified in section 2. You must ensure the CI preflight script passes before considering this task done.
- [ ] Test Case 1: [Test Name/Signature] (Expected: ...)
- [ ] Test Case 2: [Test Name/Signature] (Expected: ...)
```

### 7.2 For `playbooks/planner_playbook.md`
**ACTION 1: REPLACE** the entire outdated "Contract Generation (Output Format for the `write` tool's `content`)" section with exactly this:
```markdown
## Contract Generation (Output Format)
Generate the markdown content with EXACTLY the structure defined in `TEMPLATES/PR_Contract.md.template`. You MUST include:
- `## 2. Target Working Set & File Placement`
- `## 3. Implementation Scope`
- `## 4. TDD Blueprint & Acceptance Criteria`
```

**ACTION 2: APPEND** EXACTLY this to the playbook (and remove conflicting rules like "NO HALLUCINATED PATHS" or "Do NOT specify absolute or relative file paths"):
```markdown
## 4. The Exploration Phase & Target Working Set
Before writing the contract, act as an Architect analyzing a new PRD: Ask yourself 'Where should the changes be made based on the project structure?' and 'How do we know the changes are correct?'. 
1. You are authorized and REQUIRED to use `exec` with read-only shell tools (e.g., `tree`, `ls`, `find`) to explore the workspace structure, and the native `read` tool to read file contents. NEVER use shell commands for reading or modifying file contents (like `grep`, `cat`, `sed`, `echo >`); use the native `read`/`write`/`edit` tools for that, as per the MANDATORY FILE I/O POLICY.
2. If a new file needs to be created, deduce the correct subfolder based on the existing architecture. Do NOT put files in the root directory.
3. Explicitly list the exact paths for all new and modified files in the "Target Working Set" section of the PR Contract.

## 5. The QA Architect Persona (Language-Agnostic TDD)
You must translate the PRD's macro test strategy into concrete TDD blueprints.
1. Specify the exact test file paths to create/modify based on the project's ecosystem.
2. Provide the names/signatures of the test cases (e.g., `test_auth_failure` for Python, `should fail authentication` for JS, or `.sh` e2e test scripts).
3. Specify what behaviors to assert and what dependencies to mock, without writing the actual code.
```

### 7.3 For `config/prompts.json`
**ACTION 1: MODIFY** the `"coder"` prompt:
Replace the sentences `"The PR Contract provides functional requirements, NOT exact file paths. YOU must search the workspace, read the code, and autonomously decide which files to modify to implement the feature."`
with EXACTLY this:
`"The PR Contract provides a Target Working Set. You MUST prioritize modifying the files listed in the Working Set, but you have the autonomy to modify external dependencies if strictly required to pass the tests."`

**ACTION 2: MODIFY** the `"planner"` prompt:
Remove the exact phrase: `without hardcoding specific file paths. Give implementation freedom to the Coder.`

**ACTION 3: MODIFY** the `"planner_slice"` prompt:
Remove any instructions that forbid specifying paths. Ensure the prompt allows defining a Target Working Set.

---

## Appendix: Architecture Evolution Trace (架构演进与审查追踪)
> **[CRITICAL INSTRUCTION FOR PLANNER & CODER]** 
> IGNORING THIS SECTION IS MANDATORY. This section is strictly for historical tracking of the PM-Auditor-Boss discussion loop. Do NOT read, reference, or implement any logic from this appendix into the SDLC pipeline.

- **v1.0**: Initial draft to upgrade Planner to Tech Lead & QA Architect.
- **v1.1**: Fixed governance violations, updated exact implementation payloads to ensure Playbook and Template stay perfectly synchronized. Confirmed native read tools are guaranteed by the platform architecture.