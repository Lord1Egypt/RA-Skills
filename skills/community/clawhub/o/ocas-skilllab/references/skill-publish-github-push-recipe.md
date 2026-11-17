# GitHub Push Recipe — Publishing a Skill Repo

The `skill-publish` skill describes the audit workflow step, but the actual GitHub mechanics are:

## Create and Push a Private Repo

```python
# 1. Create the repo (private)
gh repo create <agent-handle>/skill-name --private --description "Description here"

# 2. Prepare files in a temp staging directory
mkdir -p /tmp/skill-export/skill-name/{references,scripts}
# ... copy or write SKILL.md, README.md, LICENSE, .gitignore, etc.

# 3. Clone, copy, commit, push
git clone https://github.com/<agent-handle>/skill-name.git /tmp/push-skill-name
cp -r /tmp/skill-export/skill-name/. /tmp/push-skill-name/
cd /tmp/push-skill-name
git config user.email "your-agent@email.com"
git config user.name "Your Agent Name"
git add -A
git commit -m "Initial commit: skill-name skill"

# Try main first, fall back to master
git push origin main 2>/dev/null || git push origin master
```

## Sanitizing Before Publish

Skills that were loaded/consulted may contain private data. **Never push private/local data to any repo.** Check for and remove or replace:

- Personal emails → replace with placeholders like `CANDIDATE_EMAIL`, `AGENT_EMAIL`
- Personal names, LinkedIn URLs → remove or generalize
- Sent logs, feedback logs, operational data files → exclude via .gitignore entirely
- Internal infrastructure references (SearXNG ports, hostnames) → keep generic or note as "configure for your environment"
- Comp targets, career history → remove; replace with template sections

## Standard Repo Layout

```
skill-name/
├── SKILL.md          # Frontmatter + instructions
├── README.md         # Brief description + structure
├── LICENSE           # MIT for generic tools, Proprietary for private
├── .gitignore        # __pycache__, *.pyc, operational data files
├── references/       # Search patterns, eval data, selector references
└── scripts/          # Helper scripts, MCP servers, CLI tools
```

Add `sent-*.jsonl`, `feedback-*.jsonl`, `*_cookies.json`, and any file containing PII to `.gitignore` — not just to the repo exclusion, but to the actual `.gitignore` file so they can never be accidentally committed.

## Verification

After pushing:
```bash
gh repo view <agent-handle>/skill-name --json name,isPrivate,url
```
Confirm `isPrivate: true` before sharing the URL.