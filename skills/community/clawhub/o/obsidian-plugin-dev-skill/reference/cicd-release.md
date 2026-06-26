# CI/CD & Release

## GitHub Actions Workflows

### Lint + Build (on push/PR)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [20, 22]

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm lint

      - name: Type check
        run: pnpm typecheck

      - name: Build
        run: pnpm build
```

### Tests

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Run tests
        run: pnpm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

### Release (on tag push)

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - '*'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v4
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm lint

      - name: Type check
        run: pnpm typecheck

      - name: Build
        run: pnpm build

      - name: Verify release assets exist
        run: |
          test -f main.js || { echo "main.js not found"; exit 1; }
          test -f manifest.json || { echo "manifest.json not found"; exit 1; }

      - name: Verify manifest version matches tag
        run: |
          TAG_VERSION="${GITHUB_REF#refs/tags/}"
          MANIFEST_VERSION=$(node -p "require('./manifest.json').version")
          if [ "$TAG_VERSION" != "$MANIFEST_VERSION" ]; then
            echo "Error: Tag ($TAG_VERSION) != manifest.json ($MANIFEST_VERSION)"
            exit 1
          fi

      - name: Create release
        uses: softprops/action-gh-release@v2
        with:
          files: |
            main.js
            manifest.json
            styles.css
          draft: false
          generate_release_notes: true
          fail_on_unmatched_files: false
```

**Why lint + typecheck in release workflow?** Catches issues that CI might miss due to caching or race conditions. Release should be self-verified.

## Release Workflow

### Standard Release

```bash
# 1. Update version (runs version-bump.mjs)
npm version patch   # 1.0.0 → 1.0.1
npm version minor   # 1.0.1 → 1.1.0
npm version major   # 1.1.0 → 2.0.0

# 2. Push code + tag
git push && git push --tags

# 3. GitHub Actions builds and creates release automatically
```

### Pre-release / Beta (BRAT)

```bash
# Beta release
npm version prerelease --preid=beta
# Result: 1.0.0 → 1.0.1-beta.0

git push && git push --tags

# Upgrade to stable
npm version minor
# Result: 1.0.1-beta.0 → 1.1.0
```

**BRAT Requirements:**
- Release tag, Release name, and `manifest.json` version must all match
- Assets (`main.js`, `manifest.json`, `styles.css`) must be attached to the release

### Version Bump Script

```javascript
// version-bump.mjs
import { readFileSync, writeFileSync } from 'fs'

const targetVersion = process.env.npm_package_version

// Update manifest.json
const manifest = JSON.parse(readFileSync('manifest.json', 'utf8'))
const { minAppVersion } = manifest
manifest.version = targetVersion
writeFileSync('manifest.json', JSON.stringify(manifest, null, '\t'))

// Update versions.json (maps plugin version → min Obsidian version)
const versions = JSON.parse(readFileSync('versions.json', 'utf8'))
versions[targetVersion] = minAppVersion
writeFileSync('versions.json', JSON.stringify(versions, null, '\t'))

console.log(`Version bumped to ${targetVersion}`)
```

## Community Plugin Submission

### Prerequisites Checklist

- [ ] Plugin source published on GitHub
- [ ] `README.md` with description and usage
- [ ] `LICENSE` file present
- [ ] `manifest.json` correct:
  - `id` does not contain "obsidian"
  - `name` does not contain "Obsidian" or end with "Plugin"
  - `description` does not contain "Obsidian" or "This plugin", ends with period
  - `minAppVersion` set
  - `isDesktopOnly: true` only if using Node/Electron APIs
- [ ] GitHub release with `main.js`, `manifest.json`, `styles.css`
- [ ] All sample/template code removed
- [ ] No `console.log` in production
- [ ] ESLint passes with `eslint-plugin-obsidianmd`

### Submission Steps

1. Create GitHub release:
   ```bash
   npm version patch && git push && git push --tags
   ```

2. Fork [obsidian-releases](https://github.com/obsidianmd/obsidian-releases)

3. Add entry to `community-plugins.json`:
   ```json
   {
     "id": "my-plugin",
     "name": "My Plugin",
     "author": "Author Name",
     "description": "Does something useful.",
     "repo": "username/my-obsidian-plugin"
   }
   ```

4. Create PR with title: `Add plugin: My Plugin`

5. Bot validates automatically:
   - Manifest format
   - Naming rules
   - File presence
   
6. Human review follows. Address any requested changes.

### Common Rejection Reasons

| Issue | Fix |
|-------|-----|
| ID contains "obsidian" | Rename to something unique |
| Name ends with "Plugin" | Remove "Plugin" suffix |
| Description starts with "This plugin" | Start with action verb |
| No `minAppVersion` | Add to manifest.json |
| `innerHTML` used | Switch to `createEl()` |
| Default hotkeys set | Remove; let users configure |
| Sample code not removed | Clean up `MyPlugin`, `SampleSettingTab` |
| `styles.css` missing | Create empty file if no styles |

## Security & Release Policies

### Allowed
- Static ads (disclosed in README)
- Server-side telemetry (with privacy policy)
- Network use (disclosed in README)
- Closed source (case by case)

### NOT Allowed
- Obfuscated code
- Dynamic/remote-loaded ads
- Client-side telemetry
- Self-update mechanisms
- Themes loading network assets

## Best Practices

1. **Automate releases** — GitHub Actions on tag push
2. **Version bump script** — keep manifest.json and versions.json in sync
3. **Test before release** — CI must pass before creating tag
4. **Use semantic versioning** — patch/minor/major
5. **Beta via BRAT** — test with users before stable release
6. **Clean manifest** — no obsidian in id, no Plugin in name
7. **Empty styles.css** — create it even if no styles (avoids submission issues)
