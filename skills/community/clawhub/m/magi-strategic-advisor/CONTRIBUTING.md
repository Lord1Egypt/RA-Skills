# Contributing to MAGI Strategic Advisor

First off, thank you for considering contributing to MAGI Strategic Advisor! It is through people like you that this project can thrive.

This document provides guidelines and information for contributing to this project. Please read it carefully before submitting any contributions.

---

## Code of Conduct

This project and all participants are expected to uphold the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) version 2.1. Please report unacceptable behavior to the project maintainers.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior include:

- The use of sexualized language or imagery and unwelcome sexual attention or advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

### Enforcement

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct, or to ban temporarily or permanently any contributor for other behaviors that they deem inappropriate, threatening, offensive, or harmful.

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find that you do not need to create one. When you are creating a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps which reproduce the problem in as many details as possible
- Describe the behavior you observed after following the steps and why it is problematic
- Explain which behavior you expected to see instead and why
- Include screenshots if possible

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- Use a clear and descriptive title
- Provide a step-by-step description of the suggested enhancement
- Provide specific examples to illustrate the steps
- Describe the current behavior and explain which behavior you would like to see instead
- Explain why this enhancement would be useful to most project users

### Submitting Pull Requests

Before submitting a pull request:

1. Fork the repository and create your branch from `main`
2. Make sure your code follows the project's coding standards
3. Run `make validate` (or `python scripts/validate-project.py`) and ensure it passes
4. Update documentation as needed
5. Update the CHANGELOG.md with your changes
6. Submit the pull request with a clear description of the changes

---

## Development Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git

### Setting Up the Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/magi-advisor.git
cd magi-advisor

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# No third-party dependencies are required: every script uses the
# Python standard library only (see README FOR AI.md).

# Run the scripts to verify setup
python scripts/weighted-scoring.py
python scripts/risk-matrix-gen.py
```

### Project Structure

```
magi-advisor/
|-- LICENSE
|-- .gitignore
|-- README.md
|-- README FOR AI.md
|-- CHANGELOG.md
|-- CONTRIBUTING.md
|-- CODE_OF_CONDUCT.md
|-- SECURITY.md
|-- .editorconfig
|-- SKILL.md
|-- references/
|   |-- magi-framework.md
|   |-- decision-matrix.md
|   |-- method-patterns.md
|-- prompts/
|   |-- 01-implement-method.md
|   |-- 02-robustness-checks.md
|-- scripts/
|   |-- weighted-scoring.py
|   |-- risk-matrix-gen.py
|   |-- validate-project.py
```

---

## Coding Standards

### Python Code

- Follow [PEP 8](https://pep8.org/) style guide
- Use 4-space indentation (no tabs)
- Use snake_case for variables, functions, and file names
- Use meaningful variable and function names
- All comments and docstrings must be in English
- No emoji characters in any code or documentation (enforced by HC-02)
- Include docstrings for all public functions and classes
- Include interface contracts in all scripts (see Section 7.1 of README FOR AI.md)

### Markdown Documentation

- Use consistent heading hierarchy (H1 for title, H2 for sections, H3 for subsections)
- Use tables for structured data where appropriate
- Keep lines under 100 characters where possible
- All content must be in English
- No emoji characters

### Commit Conventions

This project follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (formatting)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Changes to the build process or auxiliary tools

Examples:
```
feat(prompts): add 03-decision-synthesis prompt
fix(scripts): correct weight calculation in weighted-scoring.py
docs: update file tree in README FOR AI.md
```

---

## Pull Request Process

1. Update the README.md or CHANGELOG.md with details of changes if applicable
2. Update the version numbers in the CHANGELOG.md following SemVer
3. The PR must be reviewed by at least one maintainer before merging
4. Maintainers will check that:
   - All hard constraints (HC-01 through HC-08) are satisfied
   - Code follows PEP 8 and project conventions
   - Documentation is up to date
   - Tests pass (if applicable)
   - No emoji characters are present
5. Once approved, the maintainer will squash-merge and update the CHANGELOG.md

---

## License

By contributing to MAGI Strategic Advisor, you agree that your contributions will be licensed under the GNU General Public License v3.0.
