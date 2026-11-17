# Install Miao Vision Plugin for Claude Code

Miao Vision requires an environment where Claude can run local shell commands. For local files and the `miao-viz` CLI, Claude Code is the recommended surface.

## 1. Plugin marketplace (recommended)

```bash
claude plugin marketplace add miaoshou-dev/miao-vision
claude plugin install miao-vision@miao-vision
```

The standalone Skill remains available as a temporary compatibility channel:

```bash
npx skills add miaoshou-dev/miao-vision --global --agent claude-code --yes
```

## 2. Global CLI and optional exports

Miao Vision uses the global `miao-viz` on PATH. The bundled
`node scripts/check-miao-viz.mjs --print-path` checks compatibility and returns
its absolute path. A compatible CLI is accepted even when its version differs
from the recommendation. If missing or incompatible, approve the bundled
installer, which runs `npm install -g @miao-vision/cli` at the fixed recommended
version. It does not use sudo or change shell configuration. Old binaries in
`~/.miao-vision/bin` remain untouched and are no longer selected automatically.

PNG/PDF export requires Playwright and matching Chromium. Run
`node scripts/setup-export.mjs --host claude-code` to check without installing;
after approval add `--install`. It reuses host dependencies first, then
`~/.miao-vision/playwright`, then workspace dependencies. Claude Code checks
project and user `.claude` directories; other hosts may specify their actual
root with `--host-root`. Downloads use the selected Playwright's own installer.
Business-project dependencies are never modified. No API key is required.

## 3. Claude App / Web ZIP Install

If your Claude app supports uploaded Skills, package the skill as a ZIP:

```bash
cd skills
zip -r miao-vision-skill.zip miao-vision
```

Upload the ZIP through Claude's Skills UI.

Important: browser/app-hosted Claude environments may not be able to execute local shell commands or read arbitrary local files. Use Claude Code for full local-file visualization workflows.

## 4. Use

```text
Use miao-vision to analyze ~/data/sales.csv and generate an HTML visualization report, a single-page ranking poster, an article infographic, or a browser deck.
```

Data remains local. PDF browser dependencies are optional and separate. Remove the global CLI explicitly with `npm uninstall -g @miao-vision/cli`.
