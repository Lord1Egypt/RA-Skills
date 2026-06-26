# Publish Ichiro-Mind to ClawHub

## Quick Publish

```bash
# From skill directory
cd ~/.openclaw/workspace/skills/ichiro-mind

# Publish to ClawHub
clawhub publish . --name "Ichiro-Mind" --version 1.0.0 --tags "memory,unified,neural,ichiro"
```

## GitHub Setup

```bash
# Initialize git (if not already)
git init

# Add remote
git remote add origin https://github.com/hudul/ichiro-mind.git

# Commit and push
git add .
git commit -m "Initial release: Ichiro-Mind v1.0.0"
git push -u origin main
```

## Version Updates

```bash
# Update version in package.json
# Update CHANGELOG.md
# Then republish
clawhub publish . --name "Ichiro-Mind" --version 1.1.0 --tags "memory,unified,neural,ichiro"
```
