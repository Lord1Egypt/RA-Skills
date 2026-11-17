# README FOR AI

## 1. Skill Identity

| Field | Value |
|---|---|
| Skill Name | k12-teacher |
| Version | 1.0.0 |
| License | GNU GPL v3 |
| Language | English (compilation and runtime) |
| Target Users | Students in grades 1-12 (primary and secondary education) |
| Scope | All subjects across the K-12 curriculum |
| Compilation Language | English |

## 2. Purpose Statement

This skill transforms an AI agent into a licensed K-12 educator capable of delivering instruction across every subject in the primary and secondary school curriculum. The pedagogical framework is calibrated against five progressive professional tiers -- from entry-level qualification through expert mastery -- ensuring that instructional output scales in depth, rigor, and autonomy as the target learner level advances.

The skill does not merely retrieve facts. It implements structured teaching methodology: diagnosis of learner state, selection of instructional strategy, delivery of content, formative assessment, and iterative remediation.

## 3. Governing Constraints

The following constraints are non-negotiable and apply to every file produced during skill compilation:

| ID | Constraint | Enforcement |
|---|---|---|
| C-01 | No emoji in any compiled file | Static scan at build time |
| C-02 | All source and documentation files in English | Linter check | Exception: Parenthetical references to proper nouns (e.g., 教育部) and curriculum terminology (e.g., 教学大纲) are permitted as glossary aids but should be minimized |
| C-03 | SKILL.md contains index and quick-reference only | Size cap: 200 lines |
| C-04 | All code templates reside in references/method-patterns.md | No inline code blocks in SKILL.md |
| C-05 | prompts/ files are copy-paste deliverables for end users | No agent-autoinvoke markers |
| C-06 | Harness engineering compliance | Every module has defined input, output, boundary, and failure mode |
| C-07 | Modular isolation | No cross-file circular dependencies |
| C-08 | Single Responsibility per file | One domain concern per file |
| C-09 | Minimal surface area | Each file under 300 lines unless justified |
| C-10 | Automation-ready | All templates parameterized, no hardcoded values |

## 4. Complete File Tree

```
k12-teacher/
|
|-- .gitignore
|-- .editorconfig
|-- LICENSE
|-- CONTRIBUTING.md
|-- CODE_OF_CONDUCT.md
|-- CHANGELOG.md
|-- SECURITY.md
|-- README.md
|-- README_FOR_AI.md
|
|-- SKILL.md
|
|-- references/
|   |-- method-patterns.md
|   |-- knowledge-base.md
|   |-- syllabus-registry.md
|   |-- grade-crosswalk.md
|
|-- prompts/
|   |-- 01-implement-method.md
|   |-- 02-robustness-checks.md
|
|-- tests/
|   |-- test-cases.md
|
|-- scripts/
|   |-- validate-structure.sh
|   |-- knowledge-base-update.sh
|
|-- downloads/
|   |-- syllabus/              [Optional: for locally downloaded syllabus documents]
|-- .github/          [Optional: for CI/CD workflows, issue/PR templates]
|   |-- workflows/
|   |-- ISSUE_TEMPLATE/
|   |-- PULL_REQUEST_TEMPLATE/
```

**Note on .github/:** The above directory is optional but recommended for projects emphasizing GitHub standardization. It can host CI/CD workflow definitions (e.g., automated validation on push), issue templates, and pull request templates. Its absence does not constitute a build failure.

## 5. File-by-File Specification

### 5.1 Root Files

#### .gitignore

Purpose: Exclude build artifacts, OS metadata, and editor temp files from version control.

Required entries:
- OS files: .DS_Store, Thumbs.db, desktop.ini
- Editor files: *.swp, *.swo, *~, .vscode/, .idea/
- Build artifacts: build/, dist/, *.pyc, __pycache__/
- Environment: .env, .env.local, node_modules/

#### .editorconfig

Purpose: Define coding style rules (indentation, line endings, character set) to ensure consistency across different editors and IDEs.

Required settings:
- root = true
- charset = utf-8
- end_of_line = lf
- insert_final_newline = true
- trim_trailing_whitespace = true
- indent_size = 4 (for markdown files)
- [*.{md,sh}] apply to markdown and shell files

#### LICENSE

Type: GNU General Public License Version 3 (GPLv3).

Full canonical text of the GPLv3 must be included. No abbreviation, no custom license.

#### CONTRIBUTING.md

Purpose: Define the contribution workflow for human and AI contributors.

Required sections:
- Code of Conduct (referenced from CODE_OF_CONDUCT.md)
- Branch Naming Convention (prefix/type: feat/, fix/, docs/, refactor/, test/)
- Commit Message Format (Conventional Commits specification)
- Pull Request Template
- Review Checklist
- Testing Requirements

#### CODE_OF_CONDUCT.md

Purpose: Establish community standards for participant behavior. Adopt the Contributor Covenant code of conduct.

#### SECURITY.md

Purpose: Define the security policy for reporting vulnerabilities. Include a security.txt contact method and disclosure timeline.

#### CHANGELOG.md

Purpose: Chronological record of all releases.

Format: Keep a Changelog (https://keepachangelog.com) specification.

Required sections per release:
- Added
- Changed
- Deprecated
- Removed
- Fixed
- Security

Initial entry: v1.0.0 with release date and full feature list.

#### README.md

Purpose: Human-facing project overview.

Required sections:
- Project Title and One-Line Description
- Features
- Quick Start
- File Structure Overview
- License Reference
- Links to README_FOR_AI.md and CONTRIBUTING.md

#### README_FOR_AI.md

Purpose: This document. The master build instruction set for AI-driven skill compilation.

### 5.2 SKILL.md

Purpose: The agent-facing index and quick-reference document. This is the entry point the AI reads at runtime.

Constraint: Maximum 200 lines. No code templates. No emoji. English only.

Required structure:

| Section | Content |
|---|---|
| Identity | Name, version, scope, license (tabular format) |
| Capability Matrix | Five-tier capability ladder (Qualification -> Level 3 -> Level 2 -> Level 1 -> Senior -> Principal); Each tier: one-line descriptor of teaching autonomy |
| Subject Registry | Complete list of teachable subjects organized by teaching syllabus (教学大纲) and education stage; Stage 1: Primary (Grades 1-6); Stage 2: Junior Secondary (Grades 7-9); Stage 3: Senior Secondary (Grades 10-12); Syllabus ID mapping and crosswalk references |
| Instructional Workflow | Five-phase teaching cycle (Diagnose -> Select -> Deliver -> Assess -> Remediate); Each phase: one-line trigger condition and one-line output descriptor |
| Quick Reference: Tier Selection Logic | Decision table mapping learner profile to instructional tier; Inputs: grade level, subject, learner performance band; Output: tier designation and corresponding depth parameter |
| Quick Reference: Cross-Reference Index | Pointer to references/method-patterns.md for code templates; Pointer to references/knowledge-base.md for syllabus-based subject content; Pointer to references/syllabus-registry.md for syllabus version tracking; Pointer to scripts/knowledge-base-update.sh for update procedure; Pointer to prompts/ folder for user-facing deliverables |
| Boundary Conditions | What this skill does NOT do (e.g., does not replace licensed therapists, does not provide medical diagnosis, does not generate official certifications); Escalation triggers (when to recommend human professional intervention) |

### 5.3 references/method-patterns.md

Purpose: Central repository for ALL code templates, algorithmic patterns, and reusable instructional structures.

Constraint: This is the ONLY file that may contain code templates, pseudocode, and structured algorithmic patterns.

Required sections:

#### Section A: Instructional Strategy Patterns

**Pattern A-1: Direct Instruction Pattern**
- Input parameters: subject, topic, grade level, time allocation
- Output: structured lesson plan with objectives, sequence, and assessment
- Pseudocode for the five-phase teaching cycle

**Pattern A-2: Inquiry-Based Learning Pattern**
- Input parameters: subject, driving question, grade level
- Output: inquiry sequence with hypothesis formation, investigation, and conclusion
- Pseudocode for the inquiry cycle

**Pattern A-3: Differentiated Instruction Pattern**
- Input parameters: learner performance band (below/at/above level), subject, topic
- Output: three-tier differentiated task set
- Pseudocode for differentiation branching logic

**Pattern A-4: Socratic Dialogue Pattern**
- Input parameters: topic, target cognitive level (Bloom taxonomy), learner response history
- Output: sequenced question chain with expected response patterns
- Pseudocode for adaptive questioning loop

**Pattern A-5: Scaffolded Problem-Solving Pattern**
- Input parameters: subject, problem type, scaffold depth (1-4 levels)
- Output: step-by-step guided solution with fading support
- Pseudocode for scaffold construction and removal

#### Section B: Assessment Construction Patterns

**Pattern B-1: Formative Assessment Generator**
- Input: learning objective, cognitive level, item count
- Output: item set with rubric

**Pattern B-2: Diagnostic Pre-Assessment**
- Input: upcoming unit topics, prerequisite map
- Output: readiness diagnostic with gap analysis

**Pattern B-3: Performance Task Rubric**
- Input: task description, dimension list, performance levels
- Output: analytic rubric matrix

#### Section C: Classroom Management Patterns

**Pattern C-1: Behavior Response Ladder**
- Input: behavior severity level (1-5)
- Output: proportional response protocol

**Pattern C-2: Group Formation Algorithm**
- Input: class roster, grouping criteria, group size
- Output: optimized group assignments

#### Section D: Curriculum Mapping Patterns

**Pattern D-1: Unit Plan Generator**
- Input: subject, unit theme, duration, standards alignment
- Output: day-by-day unit plan

**Pattern D-2: Scope and Sequence Builder**
- Input: grade level, subject, academic year duration
- Output: term-by-term content distribution

### 5.4 references/knowledge-base.md

**Build Priority: LOW (Deferred -- Phase 3 of Build Sequence)**

Purpose: Subject matter registry organized by teaching syllabus (教学大纲) rather than by grade level alone. Each teaching syllabus published by the Ministry of Education (or equivalent regional authority) maps to one or more grade levels and subjects, and the knowledge base is structured to allow retrieval by syllabus identifier.

**Deferred Construction Notice:** Due to the massive scope of the K-12 knowledge base (covering three education stages, 12 grade levels, multiple subjects per grade, and multiple teaching syllabi per jurisdiction), this file is intentionally constructed last in the build sequence. The initial build creates the file with its structural skeleton and high-level outline; subsequent compilation passes populate the detailed syllabus-by-syllabus content.

#### Syllabus-Based Organization

The knowledge base is organized by teaching syllabus rather than by grade level. Each syllabus entry contains:

- Syllabus ID (e.g., `MOE-2022-MATH-PRIMARY`)
- Syllabus title and version
- Issuing authority (e.g., Ministry of Education / 教育部)
- Effective date and expiration date
- Applicable grade levels and subjects
- Topic-by-topic content outline
- Recommended teaching hours
- Assessment standards and competencies

#### Structural Skeleton

The initial skeleton includes:

- **Syllabus Registry**: Index of all known teaching syllabi (by issuing authority, year, subject, grade level) -- stored in `references/syllabus-registry.md`
- **Syllabus Content**: For each syllabus, the complete topic outline mapped to knowledge-base entries -- stored in `references/knowledge-base.md`
- **Grade-Level Crosswalk**: Mapping between grade-level organization and syllabus organization (for backward compatibility and legacy references) -- stored in `references/grade-crosswalk.md`

#### Knowledge Base Update Mechanism

This skill supports automatic updating of the knowledge base by downloading teaching syllabi from official sources (e.g., Ministry of Education website). The update mechanism comprises:

- **Download Script**: `scripts/knowledge-base-update.sh` -- downloads syllabus documents, parses them, and updates the knowledge base files
- **Syllabus Registry**: `references/syllabus-registry.md` -- living registry of all downloaded syllabi with version tracking and change history
- **Update Triggers**: Manual execution, cron job scheduling, or CI/CD pipeline trigger
- **Validation**: Post-update validation via `scripts/validate-structure.sh` to ensure quality gates pass

See Section 15 (Knowledge Base Update Procedure) for detailed step-by-step instructions.

Build Strategy:
- Pass 1 (Initial Compile): Create file with syllabus registry skeleton, grade-level crosswalk headers, and subject category outlines only (skeleton)
- Pass 2+ (Content Population): Fill in syllabus-specific content, referencing official curriculum standards
- Each content pass should be tracked in CHANGELOG.md with scope description
- Each syllabus update should create a new version entry in `references/syllabus-registry.md`
- Download and update operations should be logged in `CHANGELOG.md` under the "Changed" or "Added" sections as appropriate

### 5.5 prompts/ Folder

Purpose: Dual-mode deliverable files. These are NOT invoked automatically by the agent. They are standalone prompt documents that end users copy and paste into any AI conversation window.

Constraint: No agent-autoinvoke markers. No system prompt syntax. Pure natural language instructions.

#### prompts/01-implement-method.md

Purpose: A self-contained prompt that instructs any AI to execute the full instructional methodology for a given teaching scenario.

Required structure:
- Role assignment paragraph (you are a K-12 teacher)
- Input specification (what the user must provide: grade, subject, topic, learner profile)
- Step-by-step execution instructions (the five-phase teaching cycle)
- Output format specification (structured lesson delivery)
- Boundary conditions and escalation rules
- Example invocation with sample input and expected output shape

#### prompts/02-robustness-checks.md

Purpose: A self-contained prompt that instructs any AI to validate and stress-test any teaching output for correctness, completeness, age-appropriateness, and pedagogical soundness.

Required structure:
- Role assignment paragraph (you are a pedagogical quality auditor)
- Input specification (the teaching output to be validated)
- Validation checklist (factual accuracy, cognitive level alignment, misconception prevention, inclusivity, safety)
- Scoring rubric (pass/fail per dimension with severity levels)
- Remediation instructions (what to fix and how)
- Example invocation with sample input and expected output shape

### 5.6 tests/test-cases.md

Purpose: Validation test cases for the compiled skill.

Required structure:
- Test case ID
- Input scenario (grade, subject, topic, learner profile)
- Expected behavior (which tier activates, which template fires)
- Expected output shape (structural requirements)
- Edge cases (multi-grade classroom, special needs learner, advanced learner, language barrier)
- Boundary violations (requests outside K-12 scope, requests for non-academic advice)

### 5.7 scripts/validate-structure.sh

Purpose: Automated build validation script.

Note: This script must be set as executable before running (see Build Sequence Phase 0): `chmod +x scripts/validate-structure.sh`

Required checks:
- Verify all required files exist
- Verify SKILL.md is under 200 lines
- Verify no emoji characters in any file (grep for Unicode emoji ranges)
- Verify all files are English (basic heuristic check)
- Verify no code templates exist outside references/method-patterns.md
- Verify prompts/ files contain no agent-autoinvoke syntax
- Verify LICENSE contains GPLv3 canonical text
- Report pass/fail with line references for any violations

### 5.8 scripts/knowledge-base-update.sh

Purpose: Automated script for downloading, parsing, and integrating teaching syllabi from official sources (e.g., Ministry of Education website) into the knowledge base.

Constraint: This script must support both online download and offline fallback modes.

Required capabilities:
- **Download mode**: `--download <syllabus-id>` fetches syllabus from configured official sources
- **Local mode**: `--local <path-to-file>` processes a manually downloaded syllabus document
- **Parse**: Extract topic outlines, learning objectives, teaching hours, and assessment standards
- **Map**: Associate extracted content to syllabus-based organization structure
- **Validate**: Run post-update validation via `scripts/validate-structure.sh`
- **Log**: Record all operations in CHANGELOG.md under appropriate sections

### 5.9 references/syllabus-registry.md

Purpose: Living index of all downloaded teaching syllabi with version tracking and change history.

Required structure per entry:
- Syllabus ID and title
- Version number and release date
- Issuing authority
- Status (active, deprecated, superseded)
- Last download timestamp
- Change log reference

Maintenance rule: Every update operation must synchronize this registry with the actual state of the knowledge base.

### 5.10 references/grade-crosswalk.md

Purpose: Mapping between grade-level organization and syllabus-based organization, providing backward compatibility and supporting legacy references that use grade-level addressing.

Required structure:
- Grade level to syllabus ID mapping (one-to-many allowed)
- Subject-level crosswalk entries
- Jurisdiction tags for regional variations
- Deprecated mappings with replacement references

## 6. Five-Tier Capability Model

The skill implements five progressive instructional tiers modeled on the professional teacher certification ladder. Each tier defines the depth, autonomy, and sophistication of instructional output.

### Tier 0: Qualification Level

Descriptor: Foundational knowledge delivery. The agent delivers factual content with basic explanation. No adaptive instruction. No assessment design.

Trigger condition: Learner is at entry level, requesting introductory exposure to a new topic.

Depth parameter: 1 (surface-level, definitional)

### Tier 1: Developing Practitioner

Descriptor: Structured lesson delivery with basic differentiation. The agent follows a lesson plan, checks for understanding, and adjusts pace.

Trigger condition: Learner has basic familiarity, needs guided practice.

Depth parameter: 2 (procedural, application-level)

### Tier 2: Competent Practitioner

Descriptor: Independent instructional design. The agent constructs lessons, designs assessments, manages pacing, and provides targeted feedback.

Trigger condition: Learner is at grade-level, needs enrichment or targeted remediation.

Depth parameter: 3 (analytical, strategic)

### Tier 3: Senior Practitioner

Descriptor: Expert instructional design with research-informed methodology. The agent integrates cross-disciplinary connections, designs project-based learning, and mentors other instructional agents.

Trigger condition: Learner is above grade-level or preparing for competitive examinations.

Depth parameter: 4 (evaluative, creative)

### Tier 4: Principal-Level Expert

Descriptor: Thought leadership in education. The agent develops original curricula, conducts pedagogical research, publishes instructional frameworks, and provides systemic educational consulting.

Trigger condition: User is an educator seeking curriculum design, policy guidance, or professional development.

Depth parameter: 5 (synthetic, generative)

## 7. Instructional Workflow

Every teaching interaction follows a mandatory five-phase cycle. The detailed template specifications for each phase are maintained in references/method-patterns.md under the Instructional Strategy Templates section.

**Phase 1: DIAGNOSE**
- Input: Learner query, performance history, stated goals
- Process: Map learner state to capability tier; identify knowledge gaps
- Output: Learner profile snapshot with tier assignment

**Phase 2: SELECT**
- Input: Learner profile, subject, topic
- Process: Select instructional strategy template from references/method-patterns.md
- Output: Strategy designation with parameter bindings

**Phase 3: DELIVER**
- Input: Strategy, content from references/knowledge-base.md
- Process: Generate instructional content at appropriate depth
- Output: Structured lesson content

**Phase 4: ASSESS**
- Input: Lesson content, learning objectives
- Process: Generate formative check aligned to objectives
- Output: Assessment items with expected responses

**Phase 5: REMEDIATE**
- Input: Assessment results (or predicted misconceptions)
- Process: Select remediation strategy; loop back to Phase 2 if needed
- Output: Adjusted instruction or advancement to next topic

For complete pseudocode and parameterized templates, see references/method-patterns.md.

## 8. Harness Engineering Compliance

Every module in this skill must satisfy the following harness engineering requirements:

| Requirement | Description |
|---|---|
| Defined Input Contract | Each module declares its required inputs with type and constraints |
| Defined Output Contract | Each module declares its output format and success criteria |
| Boundary Conditions | Each module specifies what it does NOT handle |
| Failure Mode | Each module specifies behavior when inputs are invalid or missing |
| Idempotency | Repeated invocation with same inputs produces same output |
| Stateless Design | No module maintains state across invocations |
| Composability | Modules can be chained without modification |

## 9. Standardization, Generalization, Modularity, Minimization, Automation

### 9.1 Standardization

- All files follow consistent heading hierarchy (H1 for title, H2 for sections, H3 for subsections)
- All templates use identical parameter naming conventions
- All test cases follow identical structure
- All documentation uses imperative mood for instructions

### 9.2 Generalization

- No jurisdiction-specific content is hardcoded; curriculum references use parameterized jurisdiction tags
- No specific textbook edition is referenced; content is standard-aligned, not textbook-aligned
- Templates accept any subject, grade, or topic within the K-12 envelope

### 9.3 Modularity

- Each file has exactly one responsibility
- No file exceeds 300 lines without documented justification
- Cross-file references use explicit path pointers, never implicit coupling
- The prompts/ folder is fully decoupled from the agent runtime

### 9.4 Minimization

- SKILL.md is capped at 200 lines
- No redundant content across files; each fact lives in exactly one location
- Code templates are deduplicated; shared patterns are defined once and referenced

### 9.5 Automation

- validate-structure.sh runs all build checks without human intervention
- All templates are parameterized for programmatic invocation
- Test cases are structured for automated execution
- CHANGELOG.md is updated via commit-hook automation

## 10. Build Sequence

When an AI agent is tasked with compiling this skill, it must execute the following sequence in strict order. The build is organized into three phases to manage complexity and respect dependency ordering:

### Phase 0: Pre-build Preparation
Before executing any build steps, ensure the validation script is executable:

```
chmod +x scripts/validate-structure.sh
```

### Phase 1:
Establish the project skeleton, licensing, and foundational documentation.

```
Step 1:  Create directory structure (all folders and empty files)
Step 2:  Write .gitignore
Step 3:  Write .editorconfig
Step 4:  Write LICENSE (GPLv3 canonical text)
Step 5:  Write README.md (project overview for human readers)
```

### Phase 2: Capability & Instructional Engine (Steps 6-12)
Build the core teaching intelligence: method patterns, skill index, prompts, tests, and validation infrastructure.

```
Step 6:  Write references/method-patterns.md (all code templates and instructional strategies)
Step 7:  Write SKILL.md (index and quick-reference, under 200 lines)
Step 8:  Write prompts/01-implement-method.md
Step 9:  Write prompts/02-robustness-checks.md
Step 10: Write tests/test-cases.md
Step 11: Write scripts/validate-structure.sh
Step 12: Write CONTRIBUTING.md
```

### Phase 3: Knowledge Base Population (Steps 13-15)
**IMPORTANT: The K-12 knowledge base is intentionally deferred to the final phase.** Due to the massive scope covering three education stages (primary grades 1-6, junior secondary grades 7-9, senior secondary grades 10-12) across all subjects for each grade level, populating references/knowledge-base.md requires extensive curriculum research and is best performed as a separate, focused compilation pass. The initial build creates the file with its structural skeleton; subsequent passes fill in syllabus-by-syllabus content.

```
Step 13: Write references/knowledge-base.md (syllabus registry -- skeleton first, then populate)
Step 14: Write references/syllabus-registry.md (downloaded syllabi index with version tracking)
Step 14.5: Write references/grade-crosswalk.md (grade-to-syllabus mapping)
Step 15: Run scripts/validate-structure.sh and verify all checks pass
```

### Final Step
```
Step 16: Commit with message: "feat: initial skill compilation v1.0.0"
```

### Build Phase Dependency Summary

| Phase | Files Produced | Dependencies | Notes |
|---|---|---|---|
| Phase 0: Pre-build Preparation | (none -- setup step) | None | Ensure validate-structure.sh is executable via `chmod +x` |
| Phase 1: Core Structure | .gitignore, .editorconfig, LICENSE, README.md | None | Foundation layer; no external dependencies |
| Phase 2: Capability Engine | method-patterns.md, SKILL.md, prompts/*, tests/*, scripts/*, CONTRIBUTING.md | Phase 1 files | Core intelligence; method-patterns.md is independent (does NOT require knowledge-base.md content) |
| Phase 3: Knowledge Base | knowledge-base.md, syllabus-registry.md, grade-crosswalk.md | Phase 2 files (for cross-reference) | Deferred due to scale; skeleton created in Phase 3 Steps 1-2, content populated in follow-up passes; supports download-based updates via knowledge-base-update.sh |
| Final Step | (git commit) | Phase 3 files | Commit with message: "feat: initial skill compilation v1.0.0" |

## 11. Quality Gates

The skill compilation is considered complete only when ALL of the following pass:

| Gate ID | Check | Method |
|---|---|---|
| G-01 | All files in file tree exist and are non-empty | validate-structure.sh |
| G-02 | SKILL.md is under 200 lines | Line count check |
| G-03 | Zero emoji characters across all files | Unicode range scan |
| G-04 | All files are in English | Language heuristic |
| G-05 | No code templates outside references/method-patterns.md | Pattern scan |
| G-06 | prompts/ files contain no agent-autoinvoke syntax | Syntax scan |
| G-07 | LICENSE contains GPLv3 full text | String match |
| G-08 | All five capability tiers are defined in SKILL.md | Content check |
| G-09 | All five workflow phases are defined in SKILL.md | Content check |
| G-10 | references/knowledge-base.md exists and contains syllabus-based skeleton (Phase 3 may add content later); references/syllabus-registry.md exists | File existence + syllabus skeleton check |

## 12. Escalation and Boundary Rules

The skill must refuse or escalate in the following scenarios:

| Scenario | Action |
|---|---|
| Request for medical diagnosis or treatment | Refuse; recommend licensed medical professional |
| Request for psychological diagnosis | Refuse; recommend licensed mental health professional |
| Request for legal advice | Refuse; recommend licensed attorney |
| Request to generate official certification or diploma | Refuse; explain this requires accredited institution |
| Content request outside K-12 scope (e.g., graduate-level research) | Decline with explanation; suggest appropriate resource |
| Request for content that violates child safety standards | Refuse unconditionally |
| Request to bypass assessment or cheat on examinations | Refuse; redirect to legitimate study support |

## 13. Versioning Policy

- Semantic versioning (MAJOR.MINOR.PATCH)
- MAJOR: Breaking changes to capability model or tier structure; major syllabus overhaul requiring knowledge base rebuild
- MINOR: New subjects, new templates, new grade levels added; new syllabus versions downloaded and integrated
- PATCH: Bug fixes, typo corrections, template parameter adjustments; minor syllabus topic corrections
- All version changes recorded in CHANGELOG.md
- Knowledge base updates via syllabus download should also update references/syllabus-registry.md with version metadata

## 14. Glossary

| Term | Definition |
|---|---|
| Tier | A level in the five-tier capability model defining instructional depth |
| Depth Parameter | Numeric value (1-5) controlling cognitive complexity of output |
| Instructional Strategy Template | A reusable pattern for structuring teaching interactions |
| Learner Profile | A snapshot of learner state including grade, subject, performance band, and tier assignment |
| Five-Phase Cycle | The mandatory Diagnose-Select-Deliver-Assess-Remediate workflow |
| Harness | The input/output/boundary/failure contract that each module must satisfy |
| Dual-Mode File | A file in prompts/ designed for both agent-internal reference and external copy-paste use |
| Jurisdiction Tag | A label indicating which regional curriculum standard a topic belongs to |

## 15. Knowledge Base Update Procedure

This skill supports updating the knowledge base by downloading teaching syllabi from official sources such as the Ministry of Education (教育部) website. This ensures the knowledge base remains current with the latest curriculum standards.

### Update Workflow

1. **Identify Target Syllabus**: Determine which teaching syllabus needs updating (e.g., new version released by Ministry of Education). Check `references/syllabus-registry.md` for currently tracked syllabi and their versions.

2. **Download**: Run `scripts/knowledge-base-update.sh --download <syllabus-id>` to fetch the latest syllabus document from the official source. The script supports multiple sources configured in its settings.

3. **Parse**: The script parses the downloaded document and extracts topic outlines, learning objectives, recommended teaching hours, and assessment standards. It maps content to the syllabus-based organization structure.

4. **Validate**: Run `scripts/validate-structure.sh` to ensure the updated knowledge base passes all quality gates (G-01 through G-10).

5. **Review**: Manually review the changes to `references/knowledge-base.md` and `references/syllabus-registry.md` for accuracy. Automated parsing may require human verification for nuanced curriculum content.

6. **Commit**: Commit changes with message format: `docs(kb): update <syllabus-id> to version <x.y>`

7. **Changelog**: Update CHANGELOG.md with the update scope under the "Changed" or "Added" section as appropriate.

### Supported Sources

- Ministry of Education (教育部) official website: https://www.moe.gov.cn
- Provincial education department websites
- Locally adopted curriculum standards documents
- Custom sources configured via script parameters

### Update Frequency

- Monitor for new syllabus releases quarterly
- Major syllabus revisions (e.g., new curriculum framework) trigger a MINOR version bump
- Minor topic adjustments trigger a PATCH version bump
- Emergency updates for critical errors trigger an immediate PATCH

### Fallback Procedure

If automated download fails:
1. Manually download the syllabus document
2. Place it in the `downloads/syllabus/` directory
3. Run `scripts/knowledge-base-update.sh --local <path-to-file>`
4. Review and merge changes
5. Run full validation suite (`scripts/validate-structure.sh`)
6. Commit and update CHANGELOG.md

### Syllabus Registry Maintenance

The file `references/syllabus-registry.md` maintains a living index of all downloaded syllabi. Each entry includes:
- Syllabus ID and title
- Version number and release date
- Issuing authority
- Status (active, deprecated, superseded)
- Last download timestamp
- Change log reference

Every update operation must synchronize this registry with the actual state of the knowledge base.

### Security Considerations

- Always verify the authenticity of downloaded syllabus documents against official sources
- Validate file integrity (checksums) before processing
- Review parsed content before merging into the knowledge base
- Maintain audit trail of all download and update operations in CHANGELOG.md
