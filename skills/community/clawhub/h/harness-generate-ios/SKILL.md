---
name: harness-generate-iOS
description: "Auto-generate the full Claude Code harness for an iOS project (CLAUDE.md, docs/, README quick-cards, .claude/rules/). Default scans the entire project; pass a module path to process a single module. Triggers: harness-generate-iOS, generate harness, init harness. iOS/Swift projects only."
---

# iOS Generate Harness

Scan an iOS project and auto-generate the Claude Code harness file system. Core principle: **CLAUDE.md is a map, not an encyclopedia** — it holds only pointers and hard constraints; details live in docs/, READMEs, and .claude/rules/.

## Arguments

- **None** (default): Full project initialization — generate the complete harness
- **`<module-path>`**: Process a single module (e.g. `Packages/SomeKit`, `App/LoginModule`)

Routing: if an argument is provided and is not `--init` → single-module mode; otherwise → full-project mode.

---

## Execution Protocol (Mandatory)

**All multi-step flows MUST create a task list via TaskCreate and execute step by step.**

### Why
- Models tend to skip or forget steps when processing long instructions
- Task lists provide visible progress — users can track what's done
- Each task must be marked `completed` before moving to the next, preventing skipped steps
- If something fails, the exact failing task is identifiable

### How
1. After reading this skill, the **first action** MUST be TaskCreate for all Phase tasks
2. Before starting each task → `TaskUpdate(status: "in_progress")`
3. After completing each task → `TaskUpdate(status: "completed")`
4. Before starting the next task → `TaskList` to confirm the previous task is completed
5. If a task fails → keep it `in_progress`, fix the issue, then mark `completed`

### Task Template (Full Project)

When running Full Project Initialization, MUST create these tasks (in order):

```
Task 1: [Phase 1] Scan project structure
Task 2: [Phase 2] Generate docs/ files
Task 3: [Phase 3] Process each module (README + rules)
Task 4: [Phase 4] Generate CLAUDE.md
Task 5: [Phase 5] Cross-validation
Task 6: [Phase 6] Summary output + write Memory
```

### Task Template (Single Module)

When running Single Module Flow, MUST create these tasks:

```
Task 1: Scan module {module-name}
Task 2: Generate README quick-card
Task 3: Evaluate and generate Rule file
Task 4: Update indexes (CLAUDE.md + parent package README)
Task 5: Cross-validation
```

---

## Full Project Initialization

### Phase 1: Scan Project Structure

Read [scan-procedures.md](references/scan-procedures.md) for extraction methods. Collect:

1. **Project metadata**: workspace filename, scheme list, iOS deployment target
2. **Dependencies**: CocoaPods pod list, SPM package list
3. **Compiler flags**: `#if` macro names → identify dual/multi-target structure
4. **SwiftLint rules**: error-level rule list
5. **Module inventory**: SPM packages under `Packages/` + business modules under the main directory
6. **Architecture pattern**: infer from file naming and imports (MVVM / MVP / MVC / Coordinator etc.)

Run all scans in parallel (multiple Glob/Grep calls or Agent sub-tasks).

### Phase 2: Generate docs/

Generate each file per [templates.md](references/templates.md) templates. Prepend `<!-- AUTO-GENERATED, review and edit -->` to every file.

| File | Data source | Scan method |
|------|-------------|-------------|
| ARCHITECTURE.md | import statements → dependency graph; directory structure → layering | see scan-procedures.md "Architecture inference" |
| PITFALLS.md | swiftlint:disable comments + force unwrap/cast scan | see scan-procedures.md "Dangerous patterns" |
| STYLE.md | file naming patterns + directory structure + localization detection | see scan-procedures.md "Naming & style detection" |
| QUALITY.md | fixed template, tweaked per detected toolchain | use template directly |
| SCRIPTS.md | Scripts/ directory scan + Makefile + fastlane | see scan-procedures.md "Script discovery" |

**Existing file handling**: if a same-named file already exists in docs/, read it and merge — do not overwrite. Use `<!-- AUTO-GENERATED -->` markers to distinguish generated vs. hand-written content.

### Phase 3: Process Each Module

Run the "Single Module Flow" (below) for every module discovered in Phase 1.

**Order**:
1. SPM packages under `Packages/` first (skip packages with only Package.swift and no .swift source files)
2. Then business modules under the main directory

**Parallelism**: multiple modules can be processed concurrently via Agent sub-tasks, but within a single module README and rule generation must be sequential (rule depends on README analysis).

**Phase 3 completion criteria (ALL must be met to mark task completed)**:
- [ ] Every module with source code has a README
- [ ] Skipped modules (e.g. empty packages) have documented reasons

### Phase 4: Generate CLAUDE.md

Fill the "CLAUDE.md skeleton" template from [templates.md](references/templates.md) with Phase 1 scan data + Phase 3 module outputs.

At this point all READMEs and rule files already exist, so CLAUDE.md can be written once with complete routing.

**Fill rules**:
- Quick Reference: direct scan results from Phase 1
- Task Routing: checklist-group format; one entry per README created in Phase 3, plus rule file auto-load annotations
- Key Rules: translate SwiftLint error-level rules to human-readable constraints + hard constraints found by code scanning (e.g. force-unwrap ban)
- Build & Compile: infer commands from workspace + scheme names; if multiple schemes, state when to build which
- Verification Loop: use fixed template

**Constraint**: final CLAUDE.md < 80 lines. If over, trim Key Rules to error-level only.

### Phase 5: Cross-Validation (Mandatory)

After all files are generated and before the summary output, run these cross-validation checks. **Any failure must be fixed before marking this task completed.**

#### Check 1: README → CLAUDE.md reference completeness
```
For each newly created/updated Packages/*/README.md:
  - Does CLAUDE.md task routing have a corresponding checklist entry?
  - Missing → immediately add to the appropriate task routing group
```

#### Check 2: Rule → CLAUDE.md annotation completeness
```
For each newly created .claude/rules/*.md:
  - Does CLAUDE.md annotate "auto-loads .claude/rules/xxx.md"?
  - Missing → add annotation after the corresponding task routing entry
```

#### Check 3: CLAUDE.md path validity
```
For all [text](path) links in CLAUDE.md:
  - Does the path target actually exist?
  - Missing → remove the reference or annotate <!-- TODO: create this file -->
```

#### Check 4: Rule paths coverage accuracy
```
For each .claude/rules/*.md paths field:
  - Does the glob pattern match the expected files?
  - No matches → fix the pattern
```

### Phase 6: Summary Output

List all generated/updated files in a table:

```
| File | Status | Lines |
|------|--------|-------|
| CLAUDE.md | created | 72 |
| docs/ARCHITECTURE.md | created | 45 |
| Packages/XXX/README.md | updated | 28 |
| .claude/rules/xxx.md | created | 12 |
```

Prompt the user to review all files marked `<!-- AUTO-GENERATED -->`.

---

## Single Module Flow

### Step 1: Scan Module

Use the "Swift code scanning" methods from [scan-procedures.md](references/scan-procedures.md). Collect:

```
├── public/open type list (name + one-line responsibility)
├── singletons (shared instances)
├── delegate/protocol definitions
├── async methods
├── import dependency list
└── existing README.md and .claude/rules/ content
```

### Step 2: Generate README Quick-Card

Use the "README quick-card" template from [templates.md](references/templates.md).

**Must include**:
- Module name + one-line description (infer purpose from class/method names)
- API index table (public/open types only, one-line responsibility each)
- Constraints (hard constraints that cause crashes or bugs)
- Anti-patterns (real mistakes or highly common errors)

**Optional**:
- Usage examples: only when the API is non-obvious (builder pattern, chaining, etc.)
- Dependency notes: only when dependencies are non-obvious

**Never write**: full method signatures, parameter type details, changelog, installation instructions.

**Constraint**: 20–40 lines. If over, merge similar types in the API index and drop optional sections.

**Existing README handling**: if the module already has a README.md, read it and preserve hand-written content; only add missing sections.

### Step 3: Decide Whether a Rule Is Needed

Check each condition — generate a rule if **any** is met:

| Condition | Detection method | Example rule content |
|-----------|-----------------|----------------------|
| Call-order constraint | Has `configure`/`setup` + `start`/`begin` method pairs | "Call configure before start" |
| Thread constraint | Has `@MainActor` or UI class with async methods | "UI updates must be on main thread" |
| Easy-to-misuse API | Method names contain `unsafe`/`force`, or parameters include Bool toggles | "Do not call unsafeXxx directly" |
| Design token constraint | Module is a UI component library | "Colors/fonts must use semantic tokens" |
| Compiler flag divergence | Files contain `#if TARGET_A`/`#if TARGET_B` | "Build both schemes when modifying" |

**None met → do not generate a rule file.**

Generated rules use the "Rule file" template from [templates.md](references/templates.md): < 15 lines, imperative sentences.

### Step 4: Update Indexes

- If the module belongs to an umbrella package (e.g. UIComponents sub-component) → update that package's README index table
- **MUST** add a CLAUDE.md task routing entry for every newly created README
- **MUST** annotate the auto-load relationship in CLAUDE.md for every newly created rule file

---

## Output Constraints

| File type | Line limit | Over-limit strategy |
|-----------|-----------|---------------------|
| CLAUDE.md | 80 lines | Trim Key Rules to error-level only |
| README quick-card | 40 lines | Merge similar types, drop optional sections |
| Rule file | 15 lines | Merge similar rules |
| docs/ files | No hard limit | Keep concise, avoid duplication |

## Path Validation

- All reference paths in generated files must point to real, existing files
- After generation, verify every `[link](path)` target exists
- Missing targets → remove the reference or annotate `<!-- TODO: create this file -->`

---

## Post-Generation: Write Memory

After all files are generated, write or update a single memory entry to guide Claude's daily behavior when maintaining the harness. This memory teaches Claude how to **use** the harness structure, which CLAUDE.md itself cannot express.

**Memory file**: `feedback_harness_maintenance.md`

```markdown
---
name: Harness maintenance rules
description: How to maintain the harness structure when adding rules, modules, or fixing bugs — keep CLAUDE.md as an index, put details in docs/
type: feedback
---

新增规则/规范时，按 CLAUDE.md 任务路由找对应 docs/ 文件写入，不要直接改 CLAUDE.md。
新增模块时补 README 速查卡，有硬约束时补 .claude/rules/。

**Why:** CLAUDE.md 是索引入口，具体内容分散在 docs/、README、rules 中。直接往 CLAUDE.md 塞内容会破坏分层。

**How to apply:**
1. 用户让记录规则 → 查任务路由确定归属文件
2. 新建模块 → 补 README（20-40 行）+ 按需补 rule（< 15 行）
3. 改完代码 → 执行 Verification Loop
```

If a memory with similar content already exists (e.g. `feedback_docs_harness.md`), update it in-place rather than creating a duplicate. Update MEMORY.md index accordingly.
