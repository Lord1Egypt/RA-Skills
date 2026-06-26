---
name: overleaf-latex
description: "Manage Overleaf LaTeX projects via git integration or native agent tools. Install the @wahajahmed010/openclaw-overleaf plugin for 6 native tools (clone, branch, compile, push, status, health). Skill covers manual git workflow; plugin provides the same as native agent tools. Triggers on: overleaf, latex, resume version, compile latex, push to overleaf, overleaf git, overleaf project, latex resume, overleaf plugin."
metadata:
  openclaw:
    requires:
      bins: [git, pdflatex]
---

# Overleaf Skill

## OpenClaw Plugin Available

For full agent tool integration (6 native tools: overleaf_clone, overleaf_branch, overleaf_compile, overleaf_push, overleaf_status, overleaf_health), install the Overleaf plugin:

```bash
openclaw plugins install clawhub:@wahajahmed010/openclaw-overleaf
```

Plugin on ClawHub: `@wahajahmed010/openclaw-overleaf`

The skill below covers the manual workflow. The plugin provides the same functionality as native agent tools.

Manage Overleaf LaTeX projects through git integration. Clone projects, create branches for tailored versions, edit LaTeX, compile locally, and push back.

## Prerequisites

- Git (2.30+)
- TeX Live or MiKTeX (for local compilation)
- Overleaf account with git access enabled

## Setup

### 1. Store Overleaf credentials

```bash
# Create credentials file
echo "OVERLEAF_EMAIL=your@email.com" > ~/.openclaw/.overleaf_credentials
echo "OVERLEAF_PASSWORD=your_password_or_token" >> ~/.openclaw/.overleaf_credentials
chmod 600 ~/.openclaw/.overleaf_credentials
```

Or use a personal access token (recommended):

```bash
echo "OVERLEAF_EMAIL=your@email.com" > ~/.openclaw/.overleaf_credentials
echo "OVERLEAF_TOKEN=your_personal_access_token" >> ~/.openclaw/.overleaf_credentials
chmod 600 ~/.openclaw/.overleaf_credentials
```

### 2. Install LaTeX (if not installed)

```bash
# Ubuntu/Debian
sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended

# macOS
brew install --cask mactex

# Verify
which pdflatex && pdflatex --version
```

### 3. Configure git credential helper

```bash
# Store credentials so you don't get prompted
git config --global credential.helper store
```

## Workflow

### Clone a Project

```bash
# Get the project ID from the Overleaf URL
# e.g., https://www.overleaf.com/project/abc123def456 → project ID is abc123def456
PROJECT_ID="abc123def456"

# Clone
git clone "https://git.overleaf.com/${PROJECT_ID}" my-resume
cd my-resume
```

### Create a Branch for a Tailored Version

```bash
# Branch per company/role
git checkout -b resume/company-slug
```

### Edit LaTeX

Edit the `.tex` files as needed. See [references/latex-patterns.md](references/latex-patterns.md) for common resume edit patterns.

### Compile Locally (Always Before Pushing)

```bash
# Compile to verify no errors
pdflatex -interaction=nonstopmode main.tex

# If the resume uses bibtex:
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

If compilation fails, fix errors before pushing. Never push broken LaTeX.

### Push to Overleaf

```bash
git add -A
git commit -m "tailor: resume for Company Name"
git push origin resume/company-slug
```

Overleaf will auto-compile on push. The compiled PDF will be available on the Overleaf web interface.

### List Branches (All Resume Versions)

```bash
git branch -a
```

### Switch Back to Base Resume

```bash
git checkout master
```

### Merge Tailored Changes Back (Optional)

```bash
git checkout master
git merge resume/company-slug
```

## Health Check

Run the health check to verify Overleaf git access and LaTeX compilation:

```bash
python3 scripts/overleaf_health.py
```

This verifies:
- Overleaf credentials are stored
- Git can reach overleaf.com
- pdflatex is available
- A test compile succeeds

## Common Operations

| Task | Command |
|------|---------|
| Clone project | `git clone https://git.overleaf.com/<id>` |
| Create version branch | `git checkout -b resume/<slug>` |
| Compile locally | `pdflatex -interaction=nonstopmode main.tex` |
| Push to Overleaf | `git push origin <branch>` |
| View PDF | Open in Overleaf web UI |
| Delete branch | `git push origin --delete resume/<slug>` |
| Pull latest | `git pull origin master` |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Authentication failed` | Wrong credentials or expired token | Update `~/.openclaw/.overleaf_credentials` |
| `LaTeX compilation error` | Broken .tex file | Fix errors locally before pushing |
| `Merge conflict` | Parallel edits on Overleaf web | Pull first, resolve conflicts, then push |
| `Push rejected` | Remote has diverged | `git pull --rebase origin <branch>` then push |
| `pdflatex not found` | TeX Live not installed | Install texlive-latex-base |
| `Connection refused` | Network/firewall | Check internet access to git.overleaf.com |

## Constraints

- **Never push without local compilation** — always run `pdflatex` first
- **Never force push to master** — the base resume must stay intact
- **One branch per company** — don't mix tailored versions
- **Pull before push** — Overleaf web edits can cause conflicts
- **Keep credentials in `~/.openclaw/.overleaf_credentials`** with `chmod 600`