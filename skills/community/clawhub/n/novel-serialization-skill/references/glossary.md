# Glossary — Domain Terminology & Conventions

> **Purpose**: This glossary defines all domain-specific terms used across the **GitHub Novel Serialization Skill** project. It serves as a reference for AI agents, human contributors, and automated verification tools to ensure consistent understanding and usage of terminology.
>
> **Version**: 1.0.3
> **Last Updated**: 2026-09-14
> **License**: GPL-3.0 (infrastructure) / CC BY-NC-SA 4.0 (novel content)

---

## 1. Novel Serialization Terminology

Terms related to the craft and structure of novel writing and serialization.

| Term | Definition |
|------|-----------|
| **arc** | A major narrative arc is a sustained storyline or thematic thread that spans multiple chapters or even entire parts of a novel. Arcs provide long-term structure and reader investment. Types include plot arcs, character arcs, and thematic arcs. |
| **beat** | The smallest unit of dramatic action in a scene. A beat represents a single emotional shift, revelation, or action that moves the scene forward. Multiple beats compose a scene. |
| **chapter** | A primary structural division of a novel, typically containing one or more scenes. In this Skill, chapters are serialized and published incrementally via GitHub. Chapter files follow the naming convention `ch-{number}-{title}.md`. |
| **continuity** | The consistent maintenance of narrative facts across chapters — including character names, relationships, timelines, locations, magic system rules, and plot threads. Continuity is verified by the `continuity-check` module (see [continuity-check](#6-project-structure-terminology)). |
| **dialogue formatting** | The standardized convention for writing character dialogue, including attribution style, action beats interspersed with speech, and voice differentiation per character. |
| **foreshadowing** | A narrative technique where the author gives hints or clues about events that will occur later in the story. Foreshadowing must be tracked and paid off to maintain reader trust. |
| **pacing** | The rate at which the story unfolds. Pacing is controlled through the arrangement of scenes, beats, and sequels. This Skill tracks pacing via scene-to-sequel ratio and tension curve analysis. |
| **POV (Point of View)** | The narrative perspective from which a story is told. Common POVs include first-person ("I"), third-person limited ("he/she" focusing on one character's thoughts), and third-person omniscient. Each chapter should specify its POV. |
| **scene** | A unit of narrative action that takes place in a single location and time frame, advancing the plot or developing character. A chapter typically contains multiple scenes. |
| **scene-to-sequel ratio** | A pacing metric that measures the balance between action scenes (scene) and reaction/reflection segments (sequel). An imbalanced ratio can indicate pacing issues. |
| **serialization** | The practice of releasing a novel in installments (chapters) over time, rather than as a complete work. This Skill is designed specifically to support AI-assisted serialization workflows on GitHub. |
| **sequel** | A narrative segment that follows a scene, focusing on the character's emotional reaction, processing, and decision-making before the next action sequence. |
| **tension curve** | A visualization or model of rising and falling tension across chapters or arcs. Healthy tension curves avoid flat periods (boredom) and constant peaks (exhaustion). |
| **theme** | The underlying subject or message of a work. Themes are explored through character arcs, plot events, and world-building details. |
| **voice profile** | A structured description of a character's distinctive speech patterns, vocabulary, tone, and mannerisms, used to ensure consistent characterization across chapters. |
| **world-building** | The process of constructing an imaginary world, including its geography, history, cultures, magic/technology systems, politics, and ecology. World-building documents serve as reference material for consistent storytelling. |

---

## 2. Git & GitHub Terminology

Terms related to version control and GitHub workflows as used in this project.

| Term | Definition |
|------|-----------|
| **branch** | A parallel version of the repository. In this project, branches follow naming conventions such as `feature/`, `fix/`, or `chapter/` prefixes to organize development work. |
| **CHANGELOG** | A file (`CHANGELOG.md`) that documents all notable changes to the project, following the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format. It provides a human-readable history of versions. |
| **commit** | A snapshot of repository changes, tagged with a message describing the change. Commit messages in this project should follow conventional commit format (e.g., `feat: add world-building template`). |
| **dependabot** | An automated tool (configured via `.github/dependabot.yml`) that monitors dependencies and creates pull requests for updates, helping keep the project secure and up-to-date. |
| **GitHub Actions** | GitHub's CI/CD platform. This project uses GitHub Actions workflows (in `.github/workflows/`) to automate chapter validation, license compliance checks (see [license compliance](#5-license--legal-terminology)), and release creation. |
| **issue template** | Pre-defined templates (in `.github/ISSUE_TEMPLATE/`) for bug reports and feature requests, ensuring consistent and complete issue reporting. |
| **PR (Pull Request)** | A GitHub feature for proposing changes to a repository. PRs in this project must include a checklist confirming Harness Engineering compliance and license compliance. |
| **release** | A tagged version of the repository that represents a published milestone. Releases are created via Git tags (e.g., `v1.0.0`, `chapter-01`) and can trigger automated GitHub Actions workflows. |
| **semantic versioning** | A versioning scheme (`MAJOR.MINOR.PATCH`) where each increment has specific meaning: MAJOR for incompatible changes, MINOR for backwards-compatible additions, PATCH for backwards-compatible fixes. |
| **tag** | A named reference to a specific commit, used to mark releases (e.g., `v1.2.3`). Tags trigger the automated release workflow in `.github/workflows/novel-release.yml`. |
| **workflow** | An automated process defined in `.github/workflows/` that runs on specific events (e.g., tag push). The `novel-release.yml` workflow validates chapter format, verifies license compliance (see [license compliance](#5-license--legal-terminology)), runs continuity checks, and creates GitHub Releases. |

---

## 3. State Tracking Terminology

Terms related to the persistence and management of narrative state across sessions.

| Term | Definition |
|------|-----------|
| **continuity file** | A structured Markdown file that records the canonical state of the narrative universe — including timeline events, character statuses, location descriptions, and magic/technology rules. It serves as the single source of truth for continuity verification. |
| **state snapshot** | A point-in-time capture of all state files (timeline, character states, thread ledger) that allows the system to identify the exact divergence point when continuity errors are detected. State snapshots enable error recovery by providing rollback points. |
| **state tracking** | The practice of persisting narrative state in structured Markdown files (rather than conversation context) to maintain continuity across multiple AI sessions and editing rounds. Managed by the `continuity-tracker` module (see [continuity-tracker](#6-project-structure-terminology)). |
| **thread ledger** | A structured record of all active narrative threads — plot threads, character arcs, mysteries, and foreshadowing clues — including their current status (active, resolved, abandoned) and last appearance. Used to ensure no thread is forgotten. |
| **timeline** | A chronological record of events in the story world, including dates, chapter references, and cause-effect relationships. The timeline is a core component of the continuity file and is used to detect chronological inconsistencies. |
| **unresolved threads** | Narrative threads (plot questions, character arcs, mysteries) that have been introduced but not yet resolved. These must be tracked explicitly to avoid abandoning reader investments. |

---

## 4. Harness Engineering Terminology

Terms related to the engineering principles that govern how this Skill system is designed and operated.

| Term | Definition |
|------|-----------|
| **automation** | One of the five core design principles. Systems and checks should be automated where possible (e.g., license compliance verification, continuity checks) to reduce manual overhead and human error. |
| **constraint-before-generation** | A Harness Engineering principle stating that all rules, constraints, and boundaries must be defined and enforced *before* any content generation begins. In this Skill, this is implemented via the `## Constraints & Boundaries` section in SKILL.md. |
| **context budget management** | A Harness Engineering principle that limits the context window consumption by enforcing file size limits (max 500 lines per file) and progressive disclosure. SKILL.md targets ~170 lines with a hard ceiling of 500 lines. |
| **error recovery** | A Harness Engineering principle ensuring the system can identify and recover from errors. Implemented via state snapshots in the continuity tracker, allowing identification of the exact divergence point when continuity breaks. |
| **feedback loops** | A Harness Engineering principle where output from verification stages feeds back into the next iteration of generation. In this Skill, `02-robustness-checks.md` produces structured feedback that informs the next drafting cycle. |
| **generalization** | One of the five core design principles. Modules and templates should be general enough to apply across different novel genres and settings, not hardcoded to a single story. |
| **harness engineering** | The discipline of designing AI interaction systems that constrain, guide, and verify LLM output to produce reliable, stateful, multi-session results. This Skill project is itself a harness-engineered system. Core principles include: constraint-before-generation, structured memory, verification gates, modular decomposition, feedback loops, progressive disclosure, context budget management, human-in-the-loop, error recovery, role isolation, and license compliance. |
| **human-in-the-loop** | A Harness Engineering principle ensuring human oversight at critical points. In this Skill, the `prompts/` folder enables human copy-paste control, and the publishing workflow requires manual Git tag creation. |
| **miniaturization** | One of the five core design principles. Each module should be as small as possible while still being functional, reducing complexity and improving focus. |
| **modular decomposition** | A Harness Engineering principle requiring that the system be broken into independently usable, composable modules with no circular dependencies. Each `modules/*/SKILL.md` is independently loadable. |
| **modularization** | One of the five core design principles. The system should be organized into distinct modules, each with a single responsibility, independently usable and verifiable. |
| **progressive disclosure** | A Harness Engineering principle where information is layered from high-level overview to deep detail: SKILL.md (Layer 1: index) → references/ (Layer 2: templates) → examples/ (Layer 3: worked examples). Users access depth only when needed. |
| **role isolation** | A Harness Engineering principle ensuring each module has a single responsibility. The worldbuilding module does not write chapters; the chapter module does not design characters. This prevents scope creep and ensures focused verification. |
| **standardization** | One of the five core design principles. Consistent formatting, naming conventions, and file structures reduce cognitive load and enable automation. |
| **structured memory** | A Harness Engineering principle requiring that all narrative state be persisted in structured files (Markdown) rather than relying on conversation context, which is ephemeral. |
| **verification gates** | A Harness Engineering principle mandating mandatory checks before publishing. In this Skill, implemented via the `## Verification Gates` section in SKILL.md and the `02-robustness-checks.md` prompt template. No chapter publishes without passing all checks. |

---

## 5. License & Legal Terminology

Terms related to the dual-licensing model and legal framework of this project.

| Term | Definition |
|------|-----------|
| **CC BY-NC-SA 4.0** | Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International. The license applied to all generated novel content (chapters, character sheets, world-building documents). Users may share and adapt the content for non-commercial purposes with attribution, under the same license. |
| **dual licensing** | A licensing strategy that applies different licenses to different components of a project. In this Skill: GPL-3.0 for infrastructure code/templates and CC BY-NC-SA 4.0 for generated novel content. This separates code governance from creative content freedom. |
| **GPL-3.0** | GNU General Public License v3.0. The license applied to all Skill infrastructure files (SKILL.md, references/, prompts/, modules/, GitHub workflows, configuration files). Users may use, modify, and distribute the infrastructure under GPL-3.0 terms; modified versions must also be released under GPL-3.0. |
| **generated novel content** | All narrative content produced by the Skill — chapters, character descriptions, world-building documents, and story outlines. Licensed under CC BY-NC-SA 4.0, separate from the GPL-3.0 infrastructure. |
| **license compliance** | The requirement that all generated files include appropriate license headers. Infrastructure files must comply with GPL-3.0; novel content files must begin with a CC BY-NC-SA 4.0 license header block. Verified automatically in the GitHub Actions release workflow. |
| **skill infrastructure** | All files that constitute the Skill system itself: SKILL.md, references/, prompts/, modules/, .github/, .gitignore, .editorconfig, LICENSE, etc. Licensed under GPL-3.0. |

---

## 6. Project Structure Terminology

Terms related to the file system organization and file types used in this project.

| Term | Definition |
|------|-----------|
| **.editorconfig** | A configuration file (`/.editorconfig`) that defines coding style rules (indentation, charset, trailing whitespace) consistent across editors and IDEs. |
| **.gitignore** | A configuration file (`/.gitignore`) that specifies intentionally untracked files to ignore (e.g., OS files, editor swap files, temp files, AI tool caches). |
| **chapter-writing** | A functional sub-skill module (`modules/chapter-writing/SKILL.md`) responsible for drafting chapters following established style and continuity rules, including scene structure, POV rules, and pacing. |
| **character-design** | A functional sub-skill module (`modules/character-design/SKILL.md`) responsible for generating and maintaining character sheets, including identity, psychology, arc, relationships, and voice profile definitions. |
| **CODE_OF_CONDUCT.md** | A project governance file (`CODE_OF_CONDUCT.md`) that establishes community behavior standards and expectations for contributors and maintainers. Uses the Contributor Covenant template. |
| **continuity-check** | A functional sub-skill module (`modules/continuity-check/SKILL.md`) responsible for verifying narrative continuity and consistency across chapters, including character name consistency, timeline verification, and plot thread coherence. |
| **continuity-tracker** | A functional sub-skill module (`modules/continuity-tracker/SKILL.md`) responsible for managing narrative state persistence and memory across sessions, including state snapshots, thread ledgers, and timeline management. |
| **CONTRIBUTING.md** | A project guidance file (`CONTRIBUTING.md`) that documents how to report bugs, suggest features, submit pull requests, and follow development setup and code style guidelines. |
| **dual-mode** | The design pattern used for files in the `prompts/` directory: they can be used either by AI agents (auto-invocation) or by humans (copy-paste into any AI chat window). In practice, they are designed as standalone copy-paste templates. |
| **LICENSE** | The root-level license file (`/LICENSE`) containing the full text of the GPL-3.0 license, governing the Skill infrastructure components. Must be present at the project root. |
| **LICENSES/** | A directory (`/LICENSES/`) containing additional license texts not included in the root LICENSE file. Currently holds `CC-BY-NC-SA-4.0.txt` for the novel content license. |
| **meta-instruction** | A high-level directive document that instructs an AI agent on how to generate other files. `README FOR AI.md` is the meta-instruction/seed file for this project. |
| **method-patterns.md** | The master template file (`references/method-patterns.md`) that serves as the single source of truth for all structural templates, code patterns, and long-form methodology. If it exceeds 500 lines, it is split into sub-modules (worldbuilding, character, chapter, continuity, publishing). |
| **module** | An independently usable sub-skill located under `modules/`, each with its own `SKILL.md` containing YAML frontmatter, triggers, and references. Modules follow the same index-only pattern as the root SKILL.md. |
| **prompt template** | A structured text file in `prompts/` that, when pasted into an AI chat window, instructs the AI to perform specific tasks. Templates use `{{VARIABLE}}` placeholders for user customization. |
| **publishing-workflow** | A functional sub-skill module (`modules/publishing-workflow/SKILL.md`) responsible for managing the Git-based publishing pipeline for serialized chapters, including tag creation, release notes, and GitHub Actions integration. |
| **SECURITY.md** | A project policy file (`SECURITY.md`) that documents the security policy, including supported versions, vulnerability reporting procedures, response timeline expectations, and disclosure policy. |
| **seed file** | The initial file (`README FOR AI.md`) that serves as the authoritative generation specification. All other project files are generated based on its instructions. |
| **SKILL.md** | The core instruction file for a Skill or sub-skill. Contains YAML frontmatter (metadata) and a body with sections defining purpose, triggers, workflow, constraints, and cross-references. Root SKILL.md is an index; module SKILL.md files are functional specifications. |
| **worldbuilding** | A functional sub-skill module (`modules/worldbuilding/SKILL.md`) responsible for generating and maintaining world-building documents, including geography, history, cultures, magic/technology systems, politics, and ecology. Note: distinct from the novel-term `world-building` (Section 1), this entry refers specifically to the module name. |
| **YAML frontmatter** | A block of YAML metadata at the top of Markdown files (delimited by `---`), used to declare properties like `name`, `description`, `license`, `version`, and `compatibility`. Parsed by AI tools to understand Skill context. |

## 7. Variable & Placeholder Terminology

Terms related to runtime variables and template placeholders used across the project.

| Term | Definition |
|------|-----------|
| **{{OUTPUT_LANGUAGE}}** | A runtime variable specifying the language for all generated novel content. Default: `English`. Supported: any language the underlying LLM supports. Scope: narrative content only (not infrastructure files). Must appear in all prompt templates and module SKILL.md files. |
| **{{GENRE}}** | A user-customizable variable specifying the novel genre (e.g., fantasy, sci-fi, romance). Used in prompt templates for context setting. |
| **{{SETTING}}** | A user-customizable variable specifying the story setting (time period, location, world). Used in prompt templates for context setting. |
| **{{THEMES}}** | A user-customizable variable specifying the thematic elements of the novel. Used in prompt templates for context setting. |
| **{{TARGET_CHAPTERS}}** | A user-customizable variable specifying the target number of chapters. Used in prompt templates for planning. |
| **{{TONE}}** | A user-customizable variable specifying the desired tone (e.g., dark, humorous, suspenseful). Used in prompt templates for style guidance. |
| **{{POV_STYLE}}** | A user-customizable variable specifying the point-of-view style (e.g., first-person, third-person limited). Used in prompt templates for narrative guidance. |

---

## 8. Cross-Reference Index

Cross-category terms — terms that span multiple domains within this project. Only terms with verified cross-references across sections are included.

| Term | Referenced In |
|------|--------------|
| **arc** | Novel Serialization, State Tracking |
| **chapter** | Novel Serialization, Git & GitHub |
| **continuity** | Novel Serialization, State Tracking |
| **license compliance** | Git & GitHub, License & Legal |

---

> **Notes**:
> - This glossary is a living document. Terms should be added when new domain-specific vocabulary is introduced.
> - Definitions are context-specific to this Skill project and may differ from general-purpose definitions.
> - See [method-patterns.md](./method-patterns.md) for detailed templates and methodology.
> - See [prompts/README.md](../prompts/README.md) for prompt usage instructions.
