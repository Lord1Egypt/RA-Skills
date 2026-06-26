# GitHub Push Anti-Patterns Guide

## ❌ Don't Do This

### 1. Frequent Pushes

```bash
# ❌ Wrong: Push every 30 seconds
while true; do
  python scripts/github_upload.py --repo o/r --path ./f --message "Update"
  sleep 30
done
```

**Correct:**
- Min push interval: 180s
- Max pushes/hour: 50
- Use `--dry-run` for testing

### 2. Simultaneous Script Pushes

```bash
# ❌ Wrong: Multiple scripts push simultaneously
script1.py &
script2.py &
script3.py &
```

**Correct:**
- Use queue system to manage push
- Single entry point for push control

### 3. Rate Limit Violation

```python
# ❌ Wrong: Disable safe mode for fast push
uploader = SmartUpload(repo="o/r", path=".", safe=False)
```

**Correct:**
- Always enable `safe=True`
- Request authorization for high-frequency push

### 4. Unverified Large Batches

```bash
# ❌ Wrong: Push without verification
python scripts/github_upload.py --repo o/r --path ./large-dir --force
```

**Correct:**
```bash
# Test dry run first
python scripts/github_upload.py --repo o/r --path ./large-dir --dry-run

# Review files to be pushed
# Confirm before actual push
```

### 5. Bot-Style Commit Messages

```bash
# ❌ Wrong: automated style
python scripts/github_upload.py --message "commit 12345"
```

**Correct:**
```bash
# Use descriptive messages
python scripts/github_upload.py --message "Update documentation [2026-03-06]"
```

## ✅ Do This

1. Use `--dry-run` before push
2. Monitor push frequency
3. Keep commit history
4. Configure SSH keys properly
5. Clean large files regularly

## Common Error Scenarios

| Error | Symptom | Solution |
|-------|---------|----------|
| SSH key not loaded | `Permission denied (publickey)` | `ssh-add ~/.ssh/id_ed25519` |
| Remote not found | `remote origin not found` | Auto-add or manual `git remote add origin ...` |
| Conflict unhandled | `rejected by upstream` | Use `--force` or manual rebase |
| File too large | `file exceeds 100MB limit` | Exclude large files or use LFS |