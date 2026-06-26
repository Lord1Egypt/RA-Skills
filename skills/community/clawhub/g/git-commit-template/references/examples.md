# Commit Message Examples and Guidelines

## Template Structure

All commit messages follow this format:

```
[Type] Short descriptive title

Optional detailed body with more context, implementation details,
breaking changes, migration notes, or any other relevant information.
```

## Commit Types Reference

### Added
For new features, functionality, or capabilities.

**Examples:**
```
[Added] user authentication with JWT tokens

Implemented JWT-based authentication system with:
- Login/logout endpoints
- Token refresh mechanism
- Password hashing with bcrypt
- Rate limiting on auth endpoints
```

```
[Added] dark mode support

Added system-wide dark mode with theme toggle in settings.
Respects system preferences by default.
```

```
[Added] file upload progress indicator

Shows upload progress with percentage and estimated time remaining.
Includes cancel button to abort uploads.
```

### Changed
For changes in existing functionality, refactoring, or improvements.

**Examples:**
```
[Changed] improved database query performance

Optimized user lookup queries by adding composite indexes on
(email, created_at) and (username, status) columns.
Average query time reduced from 250ms to 15ms.
```

```
[Changed] updated payment flow to use new API

Migrated from v1 to v2 payment API with improved error handling
and support for additional payment methods.
```

```
[Changed] refactored authentication middleware

Extracted auth logic into reusable middleware functions.
Improved type safety and added comprehensive unit tests.
```

### Deprecated
For features that will be removed in future releases.

**Examples:**
```
[Deprecated] legacy API endpoints

The following endpoints are deprecated and will be removed in v3.0:
- GET /api/v1/users (use /api/v2/users instead)
- POST /api/v1/auth/login (use /api/v2/auth/login instead)

Migration guide: docs/migration-v2-to-v3.md
```

```
[Deprecated] old configuration format

The YAML configuration format is deprecated in favor of TOML.
Support will be removed in version 2.0.

Current configs will continue to work with deprecation warnings.
```

### Removed
For removed features, code, or dependencies.

**Examples:**
```
[Removed] support for Python 3.7

Python 3.7 reached end-of-life. Minimum supported version is now 3.8.
Updated CI/CD pipelines and documentation accordingly.
```

```
[Removed] unused analytics tracking code

Removed Google Analytics integration as we've migrated to Plausible.
Deleted 3 components and 2 utility functions.
```

```
[Removed] legacy user profile page

Replaced by new profile redesign in v2.5.
All users have been migrated to the new interface.
```

### Fixed
For bug fixes and error corrections.

**Examples:**
```
[Fixed] memory leak in WebSocket connections

Fixed unclosed connections in the WebSocket handler that were
causing memory to grow unbounded over time.

Closes #1234
```

```
[Fixed] incorrect timezone handling in reports

Reports now correctly respect user timezone settings instead of
always using UTC. Historical data has been recalculated.
```

```
[Fixed] race condition in concurrent file uploads

Added proper locking mechanism to prevent file corruption when
multiple uploads target the same resource simultaneously.
```

## Best Practices

### Title Guidelines
- Keep titles under 72 characters
- Use imperative mood ("add" not "added" or "adds")
- Be specific and descriptive
- Don't end with a period
- Focus on *what* changed, not *how*

### Body Guidelines
- Wrap body text at 72 characters for readability
- Separate title and body with a blank line
- Explain *why* the change was made, not just *what*
- Reference issue numbers when applicable (Closes #123, Fixes #456)
- Include breaking changes prominently
- Add migration instructions for deprecations
- Describe performance impacts if relevant

### When to Add a Body
- Complex changes that need context
- Breaking changes
- Performance-critical changes
- Security fixes
- Deprecations or removals
- Changes affecting multiple systems

### When Title Alone is Sufficient
- Simple bug fixes
- Typo corrections
- Formatting changes
- Small refactorings
- Documentation updates

## Common Patterns

### Breaking Changes
Always call out breaking changes prominently:

```
[Changed] restructured API response format

BREAKING CHANGE: Response structure for /api/users has changed.
Old: { "user": {...} }
New: { "data": {...}, "meta": {...} }

Migration: Update client code to access response.data instead of response.user
```

### Multiple Related Changes
Group related changes under one commit:

```
[Added] comprehensive logging system

- Structured logging with contextual information
- Log rotation and archival
- Integration with monitoring dashboard
- Performance metrics collection
```

### Security Fixes
Be careful with security details:

```
[Fixed] authentication bypass vulnerability

Fixed vulnerability in token validation. Details withheld per
responsible disclosure policy. See security advisory SA-2024-001.
```

## Anti-Patterns to Avoid

### Too Vague
❌ `[Changed] updated code`
✓ `[Changed] improved error handling in payment processor`

### Multiple Types
❌ `[Added/Fixed] new feature and bug fix`
✓ Split into two commits

### Missing Type
❌ `updated dependencies`
✓ `[Changed] updated dependencies to latest versions`

### Mixing Concerns
❌ `[Added] user dashboard and fixed login bug`
✓ Split into separate commits

## Automation Notes

The `scripts/commit.py` helper supports both interactive and command-line modes:

```bash
# Interactive mode (recommended)
python scripts/commit.py

# Direct mode
python scripts/commit.py Added "user authentication"
python scripts/commit.py Fixed "memory leak" "Fixed buffer overflow in parser"
```
