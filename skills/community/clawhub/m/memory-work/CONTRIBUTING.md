# Contributing to Memory Work v2

Thank you for your interest in contributing to the Memory Work v2 project! This document outlines how to get started and what we're looking for.

## How to Contribute

### Reporting Issues
If you find a bug or have a feature request:
1. Check the existing issues to avoid duplicates
2. Create a new issue with a clear title and description
3. Include steps to reproduce (if applicable)
4. Add relevant labels (bug, feature request, documentation, etc.)

### Submitting Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/memory-work-v2.git
   cd memory-work-v2
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the file conventions below
   - Keep commits focused and atomic
   - Write clear commit messages

4. **Test your changes**
   - Verify new files follow the correct format
   - Check YAML frontmatter syntax
   - Ensure links work correctly

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   - Link to any related issues
   - Describe what your change does and why

## File Conventions

### Markdown Files
- Use UTF-8 encoding
- Include YAML frontmatter for all new files
- Follow standard Markdown syntax
- Use clear headings hierarchy (H1 → H2 → H3)
- Keep line length reasonable (80-120 chars)

### YAML Frontmatter Format
All content files should include:
```yaml
---
title: Descriptive Title
description: Brief description of content
category: Category Name (if applicable)
version: 1.0
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

### Naming Conventions
- Folders: `NUMBER\ Category\ Name/` (e.g., `01\ Materials/`)
- Agent files: `00.category_agent.md`
- Content files: `Descriptive-Name.md` (Title Case with hyphens)
- Scripts: `kebab-case.sh` or `kebab-case.py`

### Language
- **Default**: English (for open-source collaboration)
- **Comments**: English for code, can mix with native language for documentation
- **Commit messages**: English

## Submitting New Skills

When adding a new skill:

1. Create the skill folder:
   ```
   06 Skills/new-skill-name/
   ├── SKILL.md
   ├── scripts/
   │   └── [executable files]
   ├── references/
   │   └── [documentation]
   └── assets/
       └── [templates]
   ```

2. Write comprehensive SKILL.md:
   - Include all required frontmatter
   - Explain purpose and trigger mechanism
   - Document inputs and outputs
   - Provide at least one example
   - List dependencies clearly

3. Add scripts with clear comments

4. Register in the appropriate parent documentation

## Code of Conduct

We're committed to creating a welcoming, inclusive community. When contributing:
- Be respectful and constructive
- Assume good intent
- Provide constructive feedback
- Report problems via the issue tracker, not in public
- No discrimination, harassment, or hate speech

## Questions?

- Open an issue with the `question` label
- Check existing documentation
- Review the project README for overview

## Recognition

Contributors are recognized in:
- The commit history
- The project contributors list
- Release notes for significant contributions

Thank you for helping make Memory Work v2 better!
