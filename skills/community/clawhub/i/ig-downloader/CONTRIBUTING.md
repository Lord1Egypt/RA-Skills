# Contributing to Instagram Downloader Skill

First off, thank you for considering contributing! 🎉

This project is open source under the GPLv2 license, and contributions of all kinds are welcome — whether it's bug reports, feature requests, documentation improvements, or code changes.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Improving Documentation](#improving-documentation)
  - [Submitting Code](#submitting-code)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Pull Request Process](#pull-request-process)
- [Getting Help](#getting-help)

---

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. Harassment, trolling, and aggressive behavior will not be tolerated.

---

## How to Contribute

### Reporting Bugs

Before submitting a bug report, please:

1. **Search existing issues** — your bug may already be reported
2. **Check the FAQ and troubleshooting sections** in [README.md](README.md)
3. **Try the latest version** — the bug may already be fixed

When reporting a bug, use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md) and include:

- **Python version** and **OS** (run `python --version`)
- **Full command** you ran (with arguments)
- **Full error output** (copy-paste, not screenshot)
- **What you expected** vs what happened
- **Steps to reproduce** — be as specific as possible

### Suggesting Features

Use the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md). Good feature requests include:

- **A clear use case** — what problem does this solve?
- **Expected behavior** — how should it work?
- **Relevant context** — any prior discussion, similar tools, or references

### Improving Documentation

Documentation improvements are always welcome! This includes:

- Fixing typos or unclear language
- Adding examples for edge cases
- Translating to other languages
- Improving code comments

Simply open a Pull Request with your changes.

### Submitting Code

1. **Find or create an issue** that describes what you're working on
2. **Comment on the issue** to let others know you're working on it
3. **Fork the repository**
4. **Create a branch** with a descriptive name:
   - `fix/description-of-bug`
   - `feature/description-of-feature`
   - `docs/description-of-change`
5. **Commit your changes** (see [Coding Guidelines](#coding-guidelines))
6. **Open a Pull Request** (see [Pull Request Process](#pull-request-process))

---

## Development Setup

```powershell
# Clone your fork
git clone https://github.com/cripterhack/ig-downloader-skill.git
cd ig-downloader-skill

# (Recommended) Create a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate  # Linux/macOS

# Install development dependencies
pip install -r requirements.txt
pip install pytest  # For running tests
```

### Running Tests

```powershell
pytest tests/
```

---

## Coding Guidelines

### Python Style

- Target **Python 3.10+**
- Follow **PEP 8** conventions
- Use **4-space indentation** (no tabs)
- Maximum line length of **100 characters**
- Use **type hints** for function signatures
- Write **descriptive variable names** (no single-letter names except in comprehensions)

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): brief description

Optional body explaining the change
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`

Examples:
```
feat(carousel): add instagrapi GQL fallback for older posts
fix(download): handle 403 on fbcdn.net by retrying with public.get()
docs(readme): clarify --own-only vs --mentions-only behavior
```

### Testing

- Write tests for new functionality
- Run existing tests to ensure nothing breaks
- Test on both Windows and Linux if possible

---

## Pull Request Process

1. **Ensure your fork is up to date** with the main branch
2. **Run all tests** before opening your PR
3. **Fill out the PR template** completely
4. **Keep PRs focused** — one feature or fix per PR
5. **Small PRs are preferred** — they're easier to review
6. **Respond to review feedback** promptly

### Review Criteria

Your PR will be evaluated on:

- **Correctness**: Does the code work as described?
- **Quality**: Is the code clean, readable, and maintainable?
- **Tests**: Are there tests for new functionality?
- **Documentation**: Are README/docs updated as needed?
- **No regressions**: Do existing tests still pass?

### After Approval

Once approved, a maintainer will merge your PR. You'll be credited in the release notes.

---

## Getting Help

- **Issues**: Use [GitHub Issues](https://github.com/cripterhack/ig-downloader-skill/issues) for bug reports and feature requests
- **Discussions**: Use [GitHub Discussions](https://github.com/cripterhack/ig-downloader-skill/discussions) for questions and general discussion

---

*Thank you for contributing to open source!* 🌟
