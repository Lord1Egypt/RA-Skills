# Publishing to npm

This guide explains how to publish the Knowfun CLI tool to npm.

## Prerequisites

1. **npm account**: Create one at https://www.npmjs.com/signup
2. **npm CLI**: Already installed with Node.js
3. **Authentication**: Log in to npm

## Step 1: Login to npm

```bash
npm login
```

Enter your npm credentials:
- Username
- Password
- Email
- One-time password (if 2FA enabled)

## Step 2: Verify package.json

Check that all information is correct:

```bash
cat package.json
```

Key fields:
- `name`: `knowfun-skills` (must be unique on npm)
- `version`: `1.0.0`
- `description`: Clear description
- `bin`: Points to CLI script
- `files`: Lists included files

## Step 3: Test the package locally

```bash
# Dry run to see what will be published
npm publish --dry-run

# Check package contents
npm pack
tar -tzf knowfun-skills-*.tgz
rm knowfun-skills-*.tgz
```

## Step 4: Publish to npm

### Public package (free):

```bash
npm publish --access public
```

### Scoped package (recommended for organization):

If you want to publish under `@mindstarai` scope:

1. Update package.json name to: `@mindstarai/knowfun-skills`
2. Publish:

```bash
npm publish --access public
```

## Step 5: Verify publication

```bash
# View on npm
npm view knowfun-skills

# Test installation
npm install -g knowfun-skills
knowfun --help
```

## Step 6: Update documentation

After publishing, update README.md with npm installation:

```markdown
### Installation via npm

\`\`\`bash
npm install -g knowfun-skills
\`\`\`

Then configure your API key:

\`\`\`bash
export KNOWFUN_API_KEY="kf_your_api_key_here"
\`\`\`
```

## Publishing Updates

When releasing new versions:

1. Update version in package.json:
   ```bash
   npm version patch  # 1.0.0 -> 1.0.1
   npm version minor  # 1.0.0 -> 1.1.0
   npm version major  # 1.0.0 -> 2.0.0
   ```

2. Update CHANGELOG.md

3. Commit and tag:
   ```bash
   git add .
   git commit -m "chore: bump version to x.x.x"
   git push
   git push --tags
   ```

4. Publish to npm:
   ```bash
   npm publish
   ```

5. Create GitHub Release for the new version

## Package Naming Options

Choose one:

### Option A: Unscoped (simple)
- Name: `knowfun-skills`
- Installation: `npm install -g knowfun-skills`
- Command: `knowfun`

### Option B: Scoped under organization
- Name: `@mindstarai/knowfun-skills`
- Installation: `npm install -g @mindstarai/knowfun-skills`
- Command: `knowfun`

### Option C: Official Knowfun scope
- Name: `@knowfun/cli`
- Installation: `npm install -g @knowfun/cli`
- Command: `knowfun`
- Note: Requires npm organization setup

## Troubleshooting

### Name already taken
```bash
npm search knowfun-skills
```
If taken, try:
- `knowfun-io`
- `@mindstarai/knowfun`
- `knowfunio-cli`

### Permission errors
```bash
sudo npm install -g knowfun-skills
# Or fix npm permissions:
# https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally
```

### 2FA issues
Enable 2FA on npm account:
```bash
npm profile enable-2fa auth-and-writes
```

## Resources

- npm Documentation: https://docs.npmjs.com/
- Publishing Guide: https://docs.npmjs.com/packages-and-modules/contributing-packages-to-the-registry
- Package.json Guide: https://docs.npmjs.com/cli/v9/configuring-npm/package-json
