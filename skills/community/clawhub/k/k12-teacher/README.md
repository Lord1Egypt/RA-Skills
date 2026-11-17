# k12-teacher

**An AI-powered K-12 educator skill that transforms any AI agent into a licensed teacher capable of delivering instruction across every subject in the primary and secondary curriculum.**

---

## Features

- **Comprehensive K-12 Coverage** -- Instruction across all subjects for grades 1 through 12 (primary, junior secondary, and senior secondary).
- **Five-Tier Capability Model** -- Progressive instructional depth from foundational knowledge delivery (Tier 0) to thought leadership in education (Tier 4), automatically scaling output complexity to match learner level.
- **Structured Teaching Methodology** -- Mandatory five-phase cycle: Diagnose learner state, Select instructional strategy, Deliver content, Assess understanding, and Remediate gaps.
- **Syllabus-Based Organization** -- Content organized by official teaching syllabi (教学大纲) rather than grade level alone, ensuring alignment with Ministry of Education (教育部) standards.
- **Modular and Automation-Ready** -- Every module has defined input/output contracts, boundary conditions, and failure modes. All templates are parameterized for programmatic invocation.
- **Dual-Mode Prompts** -- Standalone prompt documents in the `prompts/` folder that end users can copy and paste into any AI conversation window.
- **Automated Validation** -- Build validation script (`validate-structure.sh`) ensures code quality, language consistency, and structural integrity at every compile step.
- **Knowledge Base Update Mechanism** -- Support for downloading, parsing, and integrating teaching syllabi from official sources with version tracking and change history.

## Quick Start

### Prerequisites

- A Git-compatible environment
- A shell with standard Unix utilities (for validation scripts)

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/JohnSmithfan/K12-Teacher.git
   cd k12-teacher
   ```

2. Ensure the validation script is executable:

   ```
   chmod +x scripts/validate-structure.sh
   ```

3. Run the build validation to verify structural integrity:

   ```
   ./scripts/validate-structure.sh
   ```

### Using the Skill

To invoke the instructional methodology, use the prompt deliverables in the `prompts/` folder:

- **`prompts/01-implement-method.md`** -- A self-contained prompt that instructs any AI to execute the full five-phase teaching cycle for a given teaching scenario. Provide grade level, subject, topic, and learner profile as input.

- **`prompts/02-robustness-checks.md`** -- A self-contained prompt that instructs any AI to validate and stress-test any teaching output for correctness, completeness, age-appropriateness, and pedagogical soundness.

For detailed build instructions and file specifications, see [README_FOR_AI.md](README_FOR_AI.md).

## File Structure Overview

```
k12-teacher/
|
|-- .editorconfig               Coding style rules for editor consistency
|-- .gitattributes              Line-ending normalization and binary-file rules
|-- .gitignore                  Exclude build artifacts and editor temp files
|-- LICENSE                     GNU General Public License v3 (GPLv3)
|-- CONTRIBUTING.md             Contribution workflow and guidelines
|-- CODE_OF_CONDUCT.md          Community standards (Contributor Covenant)
|-- CHANGELOG.md                Chronological release history
|-- SECURITY.md                 Security policy and vulnerability reporting
|-- SUPPORT.md                  Support channels and response expectations
|-- GOVERNANCE.md               Roles, decision process, and release policy
|-- README.md                   This file -- project overview for human readers
|-- README_FOR_AI.md            Master build instruction set for AI compilation
|
|-- SKILL.md                    Agent-facing index and quick-reference (max 200 lines)
|
|-- references/
|   |-- method-patterns.md      Code templates and instructional strategy patterns
|   |-- knowledge-base.md       Syllabus-based subject matter registry
|   |-- syllabus-registry.md    Downloaded syllabi index with version tracking
|   |-- grade-crosswalk.md      Grade-level to syllabus mapping
|
|-- prompts/
|   |-- 01-implement-method.md  Teaching methodology execution prompt
|   |-- 02-robustness-checks.md Pedagogical quality audit prompt
|
|-- tests/
|   |-- test-cases.md           Validation test cases
|
|-- scripts/
|   |-- validate-structure.sh   Automated build validation
|   |-- knowledge-base-update.sh Syllabus download and update script
|
|-- downloads/
|   |-- syllabus/               [Optional] Locally downloaded syllabus documents
|
|-- .github/                    GitHub platform configuration
|   |-- ISSUE_TEMPLATE/
|   |   |-- bug_report.yml      Structured bug report form
|   |   |-- feature_request.yml Structured feature request form
|   |   |-- config.yml          Issue form configuration and contact links
|   |-- PULL_REQUEST_TEMPLATE.md Pull request checklist
|   |-- workflows/
|   |   |-- ci.yml              CI: structure validation, ShellCheck, PR title lint
|   |-- CODEOWNERS              Review ownership for all paths
|   |-- dependabot.yml          Weekly GitHub Actions updates
|   |-- FUNDING.yml             Sponsorship options
```

## License

This project is licensed under the **GNU General Public License v3.0** (GPLv3). See the [LICENSE](LICENSE) file for the full canonical text.

By using, distributing, or modifying this software, you agree to the terms of the GPLv3 license.

---

## Links

- **[README_FOR_AI.md](README_FOR_AI.md)** -- Complete AI compilation instructions, file specifications, build sequence, and quality gates.
- **[CONTRIBUTING.md](CONTRIBUTING.md)** -- Contribution guidelines, branch naming conventions, commit message format, and pull request template.
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** -- Community conduct standards.
- **[CHANGELOG.md](CHANGELOG.md)** -- Release history and version changes.
- **[SECURITY.md](SECURITY.md)** -- Security policy and vulnerability disclosure process.
- **[SUPPORT.md](SUPPORT.md)** -- Support channels and response expectations.
- **[GOVERNANCE.md](GOVERNANCE.md)** -- Roles, decision process, and release policy.
