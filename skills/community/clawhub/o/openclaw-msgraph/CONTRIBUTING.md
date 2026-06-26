# Contributing to OpenClaw Microsoft Graph Skill

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

1. **Clone and navigate:**

   ```bash
   git clone https://github.com/openclaw/msgraph-skill.git
   cd msgraph-skill
   ```

2. **Set up Python environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # or: venv\Scripts\activate on Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements-test.txt
   ```

4. **Configure for testing:**
   ```bash
   cp config.example.ini config.ini
   # Set a test CLIENT_ID if you want to test auth flows
   ```

## Testing

**Run tests:**

```bash
python -m pytest tests/ -v
```

**With coverage:**

```bash
python -m pytest tests/ --cov=scripts --cov-report=html
```

**Coverage requirements:** Maintain 80%+ overall coverage. Target modules:

- `auth.py`: PKCE flow, token management (64% baseline—browser flow hard to test)
- `cal.py`: Calendar operations (93% baseline)
- `graph_api.py`: HTTP utilities (100% target)
- `mail.py`: Email operations (83% baseline)
- `utils.py`: Formatting helpers (100% target)

## Code Style

- **Type hints:** Add to all function signatures
- **Docstrings:** Include module, function, and class docstrings (Google style)
- **Linting:** No external linters configured; follow PEP 8
- **Line length:** Keep under 100 characters where practical

## Making Changes

1. **Create a feature branch:**

   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes:**
   - Update code in `scripts/`
   - Add/update tests in `tests/`
   - Update docs in `references/` or root

3. **Test thoroughly:**

   ```bash
   python -m pytest tests/ -v --cov=scripts
   ```

4. **Commit with clear messages:**

   ```bash
   git commit -m "feat: add support for new calendar feature"
   ```

5. **Push and create a pull request**

## What to Contribute

### Good First Issues

- Test coverage improvements
- Documentation fixes or clarifications
- Error message improvements
- New test cases for edge cases
- Performance optimizations in HTTP utilities

### Feature Ideas

- Support for additional Microsoft Graph endpoints
- Better error diagnostics
- Folder recursion improvements
- Timezone handling enhancements
- Batch operation support

### Documentation

- Real-world usage examples
- Troubleshooting guides
- Video tutorials or walkthroughs
- API reference improvements

## Pull Request Process

1. **Ensure all tests pass** with 80%+ coverage
2. **Write clear PR description** explaining what and why
3. **Reference any related issues** (e.g., "Fixes #42")
4. **Add tests** for new functionality
5. **Update documentation** if behavior changes
6. **Keep commits clean** (consider squashing if many small commits)

## Reporting Issues

Found a bug? Please include:

- Python version (`python --version`)
- OS (Windows, macOS, Linux)
- Steps to reproduce
- Expected vs actual behavior
- Relevant error messages or logs

## Module Guide

### `scripts/auth.py`

- PKCE OAuth flow implementation
- Token storage/loading from `~/.openclaw/`
- Automatic token refresh
- **Key functions:** `generate_pkce()`, `build_auth_url()`, `exchange_code()`, `get_access_token()`

### `scripts/mail.py`

- Email operations via Graph API
- Folder resolution (well-known names + custom lookups)
- Message reading, moving, searching
- **Key functions:** `cmd_inbox()`, `cmd_read()`, `cmd_move()`, `resolve_folder_id()`

### `scripts/cal.py`

- Calendar operations via Graph API
- Event listing, creation, deletion
- Calendar selection and event details
- **Key functions:** `cmd_list()`, `cmd_create()`, `cmd_get()`, `cmd_delete()`

### `scripts/graph_api.py` (Shared)

- HTTP utilities for Graph API calls
- Request/response handling
- Error handling and logging
- **Key functions:** `graph_get()`, `graph_post()`, `graph_patch()`, `graph_delete()`

### `scripts/utils.py` (Shared)

- DateTime formatting with timezone support
- DateTime parsing (flexible input formats)
- HTML to text conversion (strips tags and excess whitespace)
- **Key functions:** `format_datetime()`, `parse_local_datetime()`, `strip_html()`

## Documentation

Go through the docs before making changes:

- [README.md](README.md) — Quick start and overview
- [SETUP.md](references/SETUP.md) — Azure setup, troubleshooting
- [SKILL.md](skill.md) — Command reference, workflows
- [API.md](references/api.md) — Microsoft Graph endpoints and scopes

## Questions?

- Check existing issues for Q&A
- Review test files for usage examples
- Look at docstrings in source files

Thanks for contributing! 🎉
