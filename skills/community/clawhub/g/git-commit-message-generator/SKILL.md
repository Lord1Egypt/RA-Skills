---
name: git-commit-message-generator
description: Generate conventional commit messages by analyzing staged changes automatically
version: 1.0.0
metadata:
  openclaw:
    emoji: "📝"
    homepage: https://www.conventionalcommits.org
    requires:
      bins:
        - git
    os: ["macos", "linux", "windows"]
---

# Git Commit Message Generator

Automatically generates high-quality conventional commit messages by analyzing your staged Git changes. No more staring at a blank commit message wondering what to write - this skill reads your `git diff`, understands the context, and creates a properly formatted commit message following the Conventional Commits specification.

## What This Skill Does

This skill analyzes your staged changes and generates commit messages that follow the Conventional Commits format:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

It intelligently detects:
- **Change type** (feat, fix, docs, style, refactor, test, chore, perf, ci, build)
- **Affected scope** (component, module, or file area)
- **Breaking changes** (from API signature changes, removed exports, etc.)
- **Related issues** (from branch names or file patterns)
- **Appropriate detail level** (when to add body/footer sections)

## Why Use This Skill

### Saves Time
- No more thinking "what should I write?" for 2-3 minutes per commit
- Eliminates typos and formatting inconsistencies
- Reduces commit message review comments in PRs

### Improves Quality
- Consistent conventional commit format across your team
- Accurate change type detection (feat vs fix vs refactor)
- Proper scope identification (which module/component changed)
- Captures breaking changes automatically
- Follows best practices (imperative mood, 50-char title, 72-char body)

### Enables Automation
- Conventional commits enable automated changelog generation
- Semantic versioning can be automated from commit types
- CI/CD pipelines can trigger based on commit types
- Git history becomes machine-readable

## When to Use This Skill

Use this skill whenever you're about to commit code:

- ✅ After staging changes with `git add`
- ✅ When working on feature branches
- ✅ During bug fixes
- ✅ For documentation updates
- ✅ When refactoring code
- ✅ For dependency updates
- ✅ During code reviews (helping others improve commits)

## When NOT to Use This Skill

- ❌ For merge commits (use default merge messages)
- ❌ For revert commits (use `git revert` auto-messages)
- ❌ When you have NO staged changes (nothing to analyze)
- ❌ For initial commits (use "chore: initial commit" or "feat: initial implementation")

## How It Works

### Step-by-Step Process

1. **Reads staged changes**: Executes `git diff --staged` to see what you're about to commit
2. **Analyzes file patterns**: Identifies which files changed (components, tests, docs, config)
3. **Detects change type**: Determines if it's a feature, fix, refactor, etc.
4. **Identifies scope**: Extracts the affected module/component name
5. **Checks for breaking changes**: Looks for API changes, removed exports, major refactors
6. **Generates message**: Creates a properly formatted conventional commit message
7. **Validates format**: Ensures it follows best practices (length, mood, structure)

### Detection Logic

**Type Detection:**
- `feat:` - New files in src/, new functions/classes, new exports
- `fix:` - Changes to existing logic, bug-related file names, error handling
- `docs:` - Changes to .md files, JSDoc/comments, README updates
- `test:` - Changes to test files, spec files, test utilities
- `refactor:` - Code restructuring without behavior change, renaming, cleanup
- `style:` - Formatting, linting fixes, whitespace, semicolons
- `perf:` - Performance optimizations, caching, algorithm improvements
- `build:` - package.json, webpack, build scripts, dependencies
- `ci:` - GitHub Actions, .yml files, CI config
- `chore:` - Tooling, configs, gitignore, minor maintenance

**Scope Detection:**
- Extracts component name from file path: `src/components/Button.tsx` → `(button)`
- Uses directory name for modules: `src/auth/login.ts` → `(auth)`
- Detects common scopes: `(api)`, `(ui)`, `(db)`, `(tests)`, `(docs)`
- Falls back to primary changed directory if ambiguous

**Breaking Change Detection:**
- Function signature changes (parameters added/removed/reordered)
- Removed exports or public API functions
- Major refactors affecting multiple files
- Migration-requiring dependency updates
- When detected, adds `BREAKING CHANGE:` footer

## Usage Examples

### Example 1: Feature Addition

**You run:**
```bash
# Stage your changes
git add src/components/UserProfile.tsx

# Ask Claude:
"Generate a commit message for my staged changes"
```

**Claude analyzes:**
```diff
+ export function UserProfile({ userId }: Props) {
+   const user = useUser(userId);
+   return <div>{user.name}</div>;
+ }
```

**Generated message:**
```
feat(user-profile): add user profile component

Implements new UserProfile component that displays user information
based on userId prop. Integrates with useUser hook for data fetching.
```

### Example 2: Bug Fix

**You run:**
```bash
git add src/api/auth.ts

# Ask Claude:
"Create a commit message"
```

**Claude analyzes:**
```diff
- if (token == null) {
+ if (token === null || token === undefined) {
    throw new Error('Invalid token');
  }
```

**Generated message:**
```
fix(auth): use strict equality check for token validation

Fixes bug where token with value 0 or empty string would incorrectly
pass validation. Now uses strict equality to properly check for null
or undefined values.
```

### Example 3: Breaking Change

**You run:**
```bash
git add src/api/users.ts

# Ask Claude:
"Generate commit message"
```

**Claude analyzes:**
```diff
- export async function getUser(id: string): Promise<User> {
+ export async function getUser(id: string, options?: GetUserOptions): Promise<UserResponse> {
```

**Generated message:**
```
feat(api)!: add options parameter to getUser function

Extends getUser API to accept optional configuration object for
including related data. Return type changed to UserResponse for
better type safety.

BREAKING CHANGE: getUser now returns UserResponse instead of User.
Update all callers to access user data via response.data property.
```

### Example 4: Documentation Update

**You run:**
```bash
git add README.md docs/api.md

# Ask Claude:
"Generate commit"
```

**Generated message:**
```
docs: update API documentation and README

- Add authentication examples to API docs
- Update installation instructions in README
- Fix typos in configuration section
```

### Example 5: Dependency Update

**You run:**
```bash
git add package.json package-lock.json

# Ask Claude:
"Make commit message"
```

**Claude analyzes:**
```diff
- "react": "^17.0.2"
+ "react": "^18.2.0"
```

**Generated message:**
```
build(deps): upgrade react to v18.2.0

Updates React from v17 to v18 for improved concurrent rendering
features and automatic batching. No breaking changes in our usage.
```

## Configuration

### Optional: Customize Commit Style

While this skill uses Conventional Commits by default, you can customize the style in your conversation:

```
"Generate a commit message following Angular style"
"Create a commit using Gitmoji format with emojis"
"Write a detailed commit message with bullet points in the body"
```

### Optional: Set Default Scope

If you're working in a monorepo or specific module:

```
"Generate commit messages with scope 'frontend' for this session"
"All my commits should have scope 'api'"
```

### Optional: Link to Issue Tracker

If your branch name includes issue numbers:

```bash
# Branch: feature/USER-123-add-profile
# Generated message will include:
#
# feat(user-profile): add user profile component
#
# Closes USER-123
```

## Best Practices

### For Best Results

1. **Stage related changes together**: Don't mix features and fixes in one commit
2. **Review the generated message**: Claude generates smart defaults, but you can refine
3. **Add context if needed**: Mention "this fixes a race condition" for better descriptions
4. **Use meaningful branch names**: Branch names help Claude understand context
5. **Keep commits atomic**: One logical change per commit works best

### Tips for Teams

- **Enforce with git hooks**: Use husky + commitlint to validate format
- **Document your scopes**: Maintain a list of valid scopes for your project
- **Review in PRs**: Check commit messages during code review
- **Generate changelogs**: Use `conventional-changelog` to automate release notes
- **Semantic versioning**: Use `semantic-release` to version from commits

## Conventional Commit Format Reference

### Structure

```
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat:` - New feature for users (triggers MINOR version)
- `fix:` - Bug fix for users (triggers PATCH version)
- `docs:` - Documentation only changes
- `style:` - Formatting, missing semicolons, etc. (no code change)
- `refactor:` - Code change that neither fixes a bug nor adds a feature
- `perf:` - Performance improvement
- `test:` - Adding or updating tests
- `build:` - Changes to build system or dependencies
- `ci:` - Changes to CI configuration files and scripts
- `chore:` - Other changes that don't modify src or test files
- `revert:` - Reverts a previous commit

### Breaking Changes

Add `!` after type/scope OR include `BREAKING CHANGE:` in footer:

```
feat(api)!: remove deprecated endpoints

BREAKING CHANGE: The /v1/users endpoint has been removed.
Use /v2/users instead.
```

## Troubleshooting

### Issue: "No staged changes found"

**Cause**: You haven't run `git add` yet.

**Solution**:
```bash
# Stage your changes first
git add .

# Or stage specific files
git add src/components/Button.tsx

# Then ask for commit message
```

### Issue: Generated message is too generic

**Cause**: Changes are ambiguous or too broad.

**Solution**: Provide more context:
```
"Generate a commit message - this change fixes a memory leak in the cache"
"Create a commit - this adds JWT authentication support"
```

### Issue: Wrong change type detected

**Cause**: File patterns don't clearly indicate intent.

**Solution**: Specify the type:
```
"Generate a 'fix' commit message"
"Create a 'refactor' commit for these changes"
```

### Issue: Scope is incorrect

**Cause**: File path doesn't match your project structure.

**Solution**: Specify the scope:
```
"Generate commit with scope 'auth'"
"Create commit message for the API module"
```

### Issue: Want to include co-authors

**Solution**: Ask Claude to add co-author footer:
```
"Generate commit and add co-author: Jane Doe <jane@example.com>"
```

Result:
```
feat(user): add profile page

Co-authored-by: Jane Doe <jane@example.com>
```

## Integration with Tools

### Commitlint

Validate generated messages:

```bash
npm install -g @commitlint/cli @commitlint/config-conventional

# .commitlintrc.json
{
  "extends": ["@commitlint/config-conventional"]
}
```

### Husky

Enforce validation on commit:

```bash
npm install -g husky

# .husky/commit-msg
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx --no -- commitlint --edit "$1"
```

### Semantic Release

Automate versioning and changelog:

```bash
npm install -g semantic-release

# Automatically generates:
# - Version numbers from commit types
# - CHANGELOG.md from commit messages
# - Git tags
# - GitHub releases
```

### Conventional Changelog

Generate changelog manually:

```bash
npm install -g conventional-changelog-cli

conventional-changelog -p angular -i CHANGELOG.md -s
```

## Examples of Good vs Bad Commits

### ❌ Bad (Before this skill)

```
update stuff
fix bug
wip
changes
asdf
updated component
```

### ✅ Good (With this skill)

```
feat(auth): implement JWT token refresh mechanism

Adds automatic token refresh before expiration to prevent
session interruptions. Includes retry logic and error handling.

fix(api): prevent race condition in user data fetch

Adds mutex lock to ensure sequential processing of concurrent
user data requests. Fixes issue where stale data could overwrite
fresh data.

docs(readme): add installation instructions for Windows

Includes PowerShell-specific commands and troubleshooting
section for common Windows installation issues.
```

## Advanced Usage

### Multi-file Commits

When you stage multiple files:

```bash
git add src/components/Button.tsx src/components/Input.tsx src/styles/forms.css
```

Claude will:
1. Identify the common scope (e.g., `forms` or `components`)
2. List major changes in the body
3. Keep the subject line focused on the primary change

### Monorepo Support

For monorepos, specify the workspace:

```
"Generate commit for the @myapp/frontend package"
"Create commit scoped to the api workspace"
```

Result:
```
feat(frontend): add dark mode toggle

or

feat(api): add rate limiting middleware
```

### Branch Name Context

Claude uses your branch name for additional context:

- `feature/USER-123` → Adds "Closes USER-123" footer
- `fix/login-error` → Prefers `fix` type
- `docs/api-reference` → Prefers `docs` type

## Why Conventional Commits Matter

### For Your Team

- **Consistent history**: Easy to scan git log and understand changes
- **Better reviews**: Reviewers know what type of change to expect
- **Faster onboarding**: New team members can follow commit patterns
- **Clear releases**: Know exactly what changed between versions

### For Automation

- **Automated versioning**: Commits drive semantic version bumps
- **Auto-generated changelogs**: Release notes write themselves
- **CI/CD triggers**: Run different pipelines for feat vs fix
- **Breaking change detection**: Automated detection of major versions

### For You

- **Less mental load**: No more "what should I write?"
- **Faster commits**: 30 seconds instead of 3 minutes
- **Better documentation**: Your past self will thank you
- **Professional portfolio**: Clean commit history impresses employers

## Related Resources

- [Conventional Commits Specification](https://www.conventionalcommits.org)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
- [Semantic Versioning](https://semver.org)
- [Commitlint Documentation](https://commitlint.js.org)
- [Semantic Release](https://semantic-release.gitbook.io)

## Real-World Examples

### Linux Kernel Style (Adapted)

```
fix(mm): prevent use-after-free in page cache

The page cache could reference freed memory under heavy load.
Add proper reference counting to prevent the issue.

Fixes: abc1234 ("mm: optimize page cache")
Reported-by: security@kernel.org
```

### React Repository Style

```
feat(hooks): add useTransition hook

Adds new concurrent rendering hook for deferring state updates.
Includes TypeScript types and comprehensive test coverage.

Related: #18796
```

### Your Projects

This skill adapts to your project's style while maintaining conventional commits structure.

---

**Pro Tip**: After using this skill for a week, you'll start writing better commit messages naturally - it's a great learning tool!

**License**: MIT-0 (Public Domain)
