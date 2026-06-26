---
name: github-push
description: "Secure GitHub push automation with auto SSH and remote config. Use when git push, automated push, or conflict handling needed."
---

# GitHub Push - Secure Auto-Push Tool

Automated GitHub push with:

- **Auto SSH Config**: Auto-detect and load SSH keys
- **Auto Remote Config**: Auto-add git remote origin
- **Auto Conflict Resolution**: Auto pull + rebase + force
- **Anti-Ban Mechanism**: Rate limiting + commit batching + smart validation

## Installation

No external dependencies required. Uses standard Git CLI (always available).

## Usage Examples

```bash
# Quick push (auto-configures everything)
python3 scripts/github_upload.py --repo owner/repo --path ./files --message "Update"

# Dry run test (no actual push)
python3 scripts/github_upload.py --repo owner/repo --path ./files --dry-run

# Force push (auto-resolves conflicts)
python3 scripts/github_upload.py --repo owner/repo --path ./files --force

# Show version info
python3 scripts/github_upload.py --version
```

## Configuration

Create `config.yaml` for persistent settings:

```yaml
defaults:
  safe_mode: true
  min_delay: 3  # seconds between operations
  max_delay: 5  # seconds between operations
  batch_commits: true
  enable_validation: true
  dry_run: false
  
safety:
  max_commits_per_hour: 100
  max_pushes_per_hour: 50
  min_time_between_pushes: 180  # 3 minutes cooldown
```

## Safety Thresholds

| Metric | Default | Description |
|--------|---------|-------------|
| Delay between ops | 3-5s | Randomized delay |
| Push cooldown | 180s | Min time between pushes |
| Max pushes/hour | 50 | Anti-spam limit |
| Max commits/hour | 100 | Anti-automation limit |

## Troubleshooting

### Error: "Too frequent pushes"

**Solution**: Wait at least 3 minutes before next push.

### Error: "Repository not found"

**Solution**: Check repository exists and you have push access. Verify SSH key is added to GitHub.

### Error: "Permission denied (publickey)"

**Solution**: 
```bash
# Load SSH key
ssh-add ~/.ssh/id_ed25519

# Verify SSH connection
ssh -T git@github.com
```

### Error: "Merge conflict"

**Solution**: The script handles this automatically with `pull + rebase + force`. Check repository state if issue persists.

### Error: "Validation failed"

**Solution**: 
- Check path exists and is accessible
- Verify files don't exceed 100MB (GitHub limit)
- Check for suspicious patterns (e.g., .env, id_rsa)

## When Not to Use

- Just viewing GitHub content
- Creating issues or PRs
- Code review

## References

- `references/` - Detailed config and API docs
- `scripts/` - Full code examples

---

**MIT License - OpenClaw Skill Standard**
