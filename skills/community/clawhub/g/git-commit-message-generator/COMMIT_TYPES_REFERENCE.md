# Commit Types Quick Reference

This is a quick reference guide for conventional commit types. Use this when you need a reminder of which type to use.

## Type Selection Flowchart

```
Does it add new user-facing functionality?
  YES → feat:
  NO ↓

Does it fix a bug?
  YES → fix:
  NO ↓

Does it only change documentation?
  YES → docs:
  NO ↓

Does it only change code formatting/style?
  YES → style:
  NO ↓

Does it restructure code without changing behavior?
  YES → refactor:
  NO ↓

Does it improve performance?
  YES → perf:
  NO ↓

Does it only affect tests?
  YES → test:
  NO ↓

Does it change build process or dependencies?
  YES → build:
  NO ↓

Does it change CI/CD configuration?
  YES → ci:
  NO ↓

Anything else (tooling, configs, etc.)
  → chore:
```

## Type Reference Table

| Type | When to Use | Examples | Version Impact |
|------|-------------|----------|----------------|
| **feat** | New user-facing feature | New component, new API endpoint, new command | MINOR (0.x.0) |
| **fix** | Bug fix | Fix crash, fix incorrect output, fix memory leak | PATCH (0.0.x) |
| **docs** | Documentation only | README updates, JSDoc, code comments, guides | None |
| **style** | Code style/formatting | Prettier, ESLint auto-fixes, whitespace, semicolons | None |
| **refactor** | Code restructure, no behavior change | Rename variables, extract functions, reorganize files | None |
| **perf** | Performance improvement | Optimize algorithm, reduce memory, add caching | PATCH (0.0.x) |
| **test** | Test changes only | Add tests, update test utilities, fix test flakes | None |
| **build** | Build system or dependencies | package.json, webpack config, npm scripts | None |
| **ci** | CI/CD changes | GitHub Actions, .yml files, deployment scripts | None |
| **chore** | Maintenance tasks | Update .gitignore, tooling configs, misc cleanup | None |
| **revert** | Revert previous commit | `revert: feat(api): add endpoint` | Depends |

## Common Scopes by Project Type

### Frontend Projects
- `(ui)` - UI components
- `(components)` - React/Vue/etc components
- `(auth)` - Authentication
- `(api)` - API integration
- `(routing)` - Routing/navigation
- `(state)` - State management
- `(hooks)` - React hooks
- `(styles)` - Styling/CSS
- `(assets)` - Images, fonts, etc.

### Backend Projects
- `(api)` - API endpoints
- `(db)` - Database
- `(auth)` - Authentication/authorization
- `(middleware)` - Middleware
- `(services)` - Business logic services
- `(models)` - Data models
- `(controllers)` - Route controllers
- `(utils)` - Utility functions
- `(validation)` - Input validation

### Full-Stack Projects
- `(frontend)` - Frontend changes
- `(backend)` - Backend changes
- `(shared)` - Shared code
- `(types)` - TypeScript types
- `(config)` - Configuration

### Library/Package Projects
- `(core)` - Core functionality
- `(cli)` - Command-line interface
- `(plugin)` - Plugin system
- `(exports)` - Public API
- `(types)` - Type definitions

## Breaking Changes

Mark breaking changes with `!` or `BREAKING CHANGE:` footer:

### When to mark as breaking:

✅ **DO mark as breaking:**
- Function signature changes (parameters added/removed/reordered)
- Removed public API functions or exports
- Changed behavior of existing functionality
- Renamed classes, functions, or modules
- Updated minimum version requirements (Node, React, etc.)
- Changed data structure or schema
- Removed configuration options

❌ **DON'T mark as breaking:**
- Internal refactoring (no API changes)
- Bug fixes (even if behavior changes)
- New optional parameters (backwards compatible)
- Deprecated features (still works, just warned)
- Documentation updates

### Breaking Change Format

**Option 1: ! in type**
```
feat(api)!: remove deprecated endpoints
```

**Option 2: BREAKING CHANGE footer**
```
feat(api): update user API

BREAKING CHANGE: The getUser function now returns a Promise.
Update all synchronous calls to use await.
```

**Option 3: Both (for clarity)**
```
feat(api)!: update user API

BREAKING CHANGE: The getUser function now returns a Promise.
Update all synchronous calls to use await.

Migration guide:
- Before: const user = getUser(id);
- After: const user = await getUser(id);
```

## Real Examples

### feat (Feature)

```
feat(auth): add OAuth 2.0 support

Implements OAuth 2.0 authentication flow with support for
Google, GitHub, and Microsoft providers. Includes token
refresh and revocation.
```

### fix (Bug Fix)

```
fix(pagination): correct page count calculation

Fixes off-by-one error in pagination component that caused
the last page to be inaccessible when total items was
exactly divisible by page size.

Fixes #234
```

### docs (Documentation)

```
docs(api): add examples for file upload endpoint

Includes curl examples, JavaScript fetch examples, and
common error responses with solutions.
```

### style (Formatting)

```
style(components): apply Prettier formatting

No functional changes, only code formatting updates
to match project style guide.
```

### refactor (Code Restructure)

```
refactor(user-service): extract validation to separate module

Moves user input validation logic from UserService to new
ValidationService for better separation of concerns and
reusability.
```

### perf (Performance)

```
perf(api): add Redis caching for user queries

Reduces database load by caching user data in Redis with
5-minute TTL. Improves response time from 200ms to 20ms
for cached requests.
```

### test (Testing)

```
test(auth): add integration tests for login flow

Adds comprehensive integration tests covering successful
login, invalid credentials, and rate limiting scenarios.
Increases test coverage from 65% to 85%.
```

### build (Build System)

```
build(deps): upgrade webpack to v5

Updates webpack from v4 to v5 for improved build performance
and tree-shaking. Updates related plugins and loaders.
```

### ci (Continuous Integration)

```
ci: add automatic deployment to staging

Adds GitHub Actions workflow to automatically deploy to
staging environment on merge to develop branch. Includes
smoke tests before deployment.
```

### chore (Maintenance)

```
chore: update .gitignore with IDE files

Adds IntelliJ IDEA, VS Code, and Vim swap files to gitignore
to prevent accidental commits of local configuration.
```

## Subject Line Best Practices

### DO ✅

- Use imperative mood: "add feature" not "added feature"
- Start with lowercase after type
- No period at the end
- Keep under 50 characters (hard limit: 72)
- Be specific: "fix login form validation" not "fix bug"

### DON'T ❌

- Use past tense: ~~"added feature"~~
- Use -ing form: ~~"adding feature"~~
- Be vague: ~~"update code"~~ ~~"fix issue"~~
- Include issue numbers in subject (use footer instead)
- Use technical jargon when simple words work

## Body Best Practices

### When to Add a Body

Add a body when:
- The change needs explanation (why, not just what)
- There are side effects or implications
- You want to explain the approach taken
- Multiple things changed together
- Breaking changes need migration instructions

### Body Format

- Separate from subject with blank line
- Wrap at 72 characters
- Use bullet points for multiple changes
- Explain WHY not just WHAT (code shows what)
- Include before/after examples for complex changes

### Example with Body

```
refactor(cache): switch from LRU to LFU eviction strategy

The LRU (Least Recently Used) strategy was causing issues with
our access patterns where frequently-needed data was being
evicted due to occasional bulk operations.

LFU (Least Frequently Used) better matches our usage:
- Configuration data accessed constantly
- Bulk reports accessed rarely
- Better hit rate: 65% → 89%

Maintains same cache size limit (1000 items) and API.
No breaking changes.
```

## Footer Reference

### Common Footers

```
Fixes #123
Closes #123, #456
Refs #123
Co-authored-by: Name <email@example.com>
Reviewed-by: Name <email@example.com>
Signed-off-by: Name <email@example.com>
BREAKING CHANGE: description
```

### Multiple Footers

```
feat(api): add webhook support

Implements webhook delivery system with retry logic
and signature verification.

Closes #789
Co-authored-by: Jane Doe <jane@example.com>
```

## Common Mistakes

### ❌ Wrong

```
Fix
update readme
WIP
changes
fix stuff
added new feature for users to login
```

### ✅ Correct

```
fix(auth): prevent null pointer in session handler
docs: update README installation steps
feat(auth): add user login functionality
refactor(api): extract error handling middleware
test(user): add unit tests for validation
```

## Tips for Consistent Commits

1. **Read the diff first** - `git diff --staged` before committing
2. **Commit often** - Small, focused commits are easier to describe
3. **One concern per commit** - Don't mix features and fixes
4. **Use a template** - `git config commit.template ~/.gitmessage`
5. **Review before push** - `git log --oneline` to check consistency
6. **Setup validation** - Use commitlint to enforce format
7. **Learn from others** - `git log` in well-maintained projects

## Git Config Template

Create `~/.gitmessage`:

```
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>
#
# Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore
# Scope: Optional, name of module/component
# Subject: Imperative mood, lowercase, no period, <50 chars
# Body: Optional, wrap at 72 chars, explain WHY
# Footer: Optional, reference issues, breaking changes
```

Set it:
```bash
git config --global commit.template ~/.gitmessage
```

Now every commit opens with this template!
