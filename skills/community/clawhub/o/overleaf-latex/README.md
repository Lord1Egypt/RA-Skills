# Overleaf LaTeX Skill for OpenClaw

Manage Overleaf LaTeX projects through git integration. Clone projects, create branches for tailored versions, edit LaTeX, compile locally, and push back.

## Features

- **Git integration** — Clone, branch, push Overleaf projects via git
- **Local compilation** — Verify LaTeX compiles before pushing
- **Resume versioning** — One branch per company/role
- **Health check** — Verify Overleaf credentials, connectivity, and LaTeX setup
- **Common patterns** — Reference guide for tailoring LaTeX resumes

## Install

```bash
clawhub install overleaf-latex
```

## Quick Start

```bash
# Clone your Overleaf project
git clone https://git.overleaf.com/<project-id> my-resume

# Create a tailored version
cd my-resume
git checkout -b resume/company-slug

# Edit, compile, push
pdflatex -interaction=nonstopmode main.tex
git add -A && git commit -m "tailor: resume for Company" && git push origin resume/company-slug
```

## Health Check

```bash
python3 scripts/overleaf_health.py
```

Verifies: Overleaf credentials, git connectivity, pdflatex availability, test compilation.

## What's Included

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill instructions and workflow |
| `scripts/overleaf_health.py` | Health check script |
| `references/latex-patterns.md` | Common LaTeX resume edit patterns |

## Constraints

- Never push without local compilation
- Never force push to master
- One branch per company
- Pull before push (avoid conflicts with web edits)

## License

MIT-0