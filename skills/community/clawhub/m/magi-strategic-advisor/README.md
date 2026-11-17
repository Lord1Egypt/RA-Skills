# MAGI Strategic Advisor

A modular, harness-engineered skill package providing multi-perspective strategic decision analysis powered by the MAGI three-wise-man decision framework.

Inspired by the MAGI supercomputer system from Neon Genesis Evangelion, this project implements three independent decision cores that produce high-quality judgments through voting and deliberation:

- **MELCHIOR** -- The rational-scientist persona: data-driven, logic-first analysis
- **BALTHASAR** -- The prudent-guardian persona: risk-averse, bottom-line-oriented analysis
- **CASPER** -- The intuitive-observer persona: holistic, pattern-recognition analysis

[![CI](https://github.com/JohnSmithfan/MAGI-Strategic-Advisor/actions/workflows/ci.yml/badge.svg)](https://github.com/JohnSmithfan/MAGI-Strategic-Advisor/actions/workflows/ci.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Changelog](https://img.shields.io/badge/changelog-Keep%20a%20Changelog-orange.svg)](https://keepachangelog.com/en/1.1.0/)

## Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Design Principles](#design-principles)
- [Hard Constraints](#hard-constraints)
- [Disclaimer](#disclaimer)
- [Acknowledgments](#acknowledgments)
- [Licensing](#licensing)

---

## Features

- **Multi-perspective analysis**: Every decision is examined through three independent lenses (rational, prudent, intuitive)
- **Structured decision matrices**: Quantitative scoring with weighted dimensions and veto conditions
- **Risk assessment**: Six-domain risk scanning with probability-impact matrix and severity classification
- **Multi-option comparison**: Systematic side-by-side evaluation of competing proposals
- **Modular architecture**: Each component is independently testable with defined interfaces (harness engineering)
- **Progressive disclosure**: SKILL.md provides routing; detailed content loads on demand
- **Dual-mode prompts**: User-facing prompts portable to any AI conversation window
- **Executable tools**: Python scripts for weighted scoring and risk matrix generation
- **Open source**: Licensed under GNU GPL V3

---

## Project Structure

```
magi-advisor/
|-- LICENSE                    (GNU GPL V3 license)
|-- .gitignore                 (Git ignore patterns)
|-- .gitattributes             (Git line-ending and binary rules)
|-- README.md                  (This file - GitHub front page)
|-- README FOR AI.md           (AI agent build instructions)
|-- CHANGELOG.md               (Version history)
|-- CONTRIBUTING.md            (Contribution guidelines)
|-- CODE_OF_CONDUCT.md        (Community standards)
|-- SECURITY.md               (Security policy)
|-- SUPPORT.md                 (Support channels)
|-- .editorconfig             (Editor defaults)
|-- Makefile                   (Development entry points)
|-- SKILL.md                   (Skill entry index)
|-- .github/
|   |-- CODEOWNERS             (Automatic reviewer assignment)
|   |-- dependabot.yml         (Dependency update automation)
|   |-- PULL_REQUEST_TEMPLATE.md (Pull request checklist)
|   |-- ISSUE_TEMPLATE/
|   |   |-- bug_report.yml     (Structured bug report form)
|   |   |-- feature_request.yml (Structured feature request form)
|   |   |-- config.yml         (Issue chooser configuration)
|   |-- workflows/
|       |-- ci.yml             (CI: syntax and contract validation)
|-- references/
|   |-- magi-framework.md      (Three-wise-man decision framework)
|   |-- decision-matrix.md     (Scoring matrix templates)
|   |-- method-patterns.md     (Code templates and patterns)
|-- prompts/
|   |-- 01-implement-method.md (Method implementation prompt)
|   |-- 02-robustness-checks.md (Robustness validation prompt)
|-- scripts/
|   |-- weighted-scoring.py    (Weighted scoring calculator)
|   |-- risk-matrix-gen.py     (Risk matrix generator)
|   |-- validate-project.py    (Repository contract validator)
```

---

## Quick Start

### For AI Agents

1. Read [`README FOR AI.md`](README%20FOR%20AI.md) -- this is the authoritative build instruction
2. Follow the Generation Workflow (Section 8) to generate the complete project
3. Run validation checks to ensure all constraints are satisfied

### For Human Users

1. Clone this repository
2. No environment variables or third-party dependencies are required; all scripts run on the Python standard library
3. Explore the [`scripts/`](scripts/) directory for executable tools:
   - `python scripts/weighted-scoring.py` -- Run weighted scoring with sample data
   - `python scripts/risk-matrix-gen.py` -- Generate risk matrix (terminal output)
   - `python scripts/risk-matrix-gen.py --html` -- Generate HTML risk matrix visualization
   - `python scripts/risk-matrix-gen.py --json` -- Output risk data in JSON format
4. Use the `prompts/` files by copying them into any AI conversation window
5. Run `make validate` to check the repository contract

### For Contributors

1. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution guidelines
2. Follow the coding standards and commit conventions
3. Run `make validate` to ensure all constraints are satisfied
4. Submit pull requests using the provided template

---

## Design Principles

This project adheres to five core design principles:

1. **Standardized**: Consistent formatting, naming, and structure across all files
2. **Generic**: No domain-specific assumptions; parameterized thresholds and weights
3. **Modular**: Each file has a single responsibility; modules are independently testable
4. **Compact**: No redundant information; SKILL.md under 120 lines
5. **Automated**: Scripts include CLI interfaces; validation can be automated

---

## Hard Constraints

The project enforces language, no-emoji, compact-index, code-placement,
prompt-portability, harness-engineering, design, and licensing requirements.
See `README FOR AI.md` for the authoritative contract and audit record.

---

## Disclaimer

This software is provided "as is", without warranty of any kind, express or implied. The authors and contributors shall not be liable for any claims, damages, or other liability arising from the use of this software. The decision analysis provided by this tool is for informational purposes only and should not be construed as professional advice. Users should consult qualified professionals before making significant business decisions.

---

## Acknowledgments

- MAGI supercomputer system concept inspired by *Neon Genesis Evangelion*
- Harness engineering principles applied throughout the architecture
- Keep a Changelog format adopted for version history
- Contributor Covenant Code of Conduct adopted for community standards

---

## Licensing

This project is licensed under the GNU General Public License v3.0. See the [`LICENSE`](LICENSE) file for the full text.

By contributing to this project, you agree that your contributions will be licensed under the same terms.
