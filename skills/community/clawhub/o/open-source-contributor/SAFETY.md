# Safety Documentation

## Risk Assessment

This skill makes **public commits under your GitHub identity**. This is a high-risk automation that requires understanding.

## What Could Go Wrong

### 1. Code Quality
- AI may misunderstand issue
- Fix may introduce subtle bugs
- Tests may pass but logic be wrong

**Mitigation:** Graduated complexity, test validation, human review recommended for first 5 PRs.

### 2. Reputation Risk
- Low-quality PRs reflect on your profile
- Maintainers may block you
- Future contributions scrutinized more

**Mitigation:** Auto-pause on rejection rate >30%, start with simple fixes.

### 3. Token Security
- Token with `public_repo` can write to all your public repos
- If compromised, attacker can push malicious code under your name

**Mitigation:** 
- Use `public_repo` scope only (not `repo`)
- Store token in environment variable, never commit
- Rotate token regularly

### 4. Scope Creep
- May touch files outside intended scope
- Could modify critical files accidentally

**Mitigation:** Blocked file patterns, pre-flight checklist, security scan.

## Recommended Workflow

1. **Dry Run Mode** (first week)
   - Scout and analyze only
   - Log what would be done
   - Review manually

2. **Human Review Mode** (next 2 weeks)
   - Draft PRs presented for approval
   - You submit manually
   - Track approval rate

3. **Full Autonomy** (only after >70% approval rate)
   - Enable automatic PR submission
   - Continue monitoring

## Emergency Stop

If things go wrong:

```bash
# Stop all pending jobs
pkill -f contrib-pipeline

# Revoke GitHub token
# Go to: GitHub Settings → Developer settings → Personal access tokens → Delete

# Review recent commits
git log --author="your-email" --since="1 week ago"
```

## Best Practices

- ✅ Start with Level 1 (typo fixes) for 2 weeks
- ✅ Review every PR before it goes out (first 10)
- ✅ Use dedicated GitHub account if possible
- ✅ Enable 2FA on your GitHub account
- ✅ Monitor email for PR responses
- ❌ Never grant `repo` scope (includes private repos)
- ❌ Don't skip test validation
- ❌ Don't increase complexity too fast

## Getting Help

If you encounter issues:
1. Check logs: `~/.openclaw/workspace/contrib-scout/logs/`
2. Review recent contributions
3. Open issue at: https://github.com/wahajahmed010/open-source-contributor

## Liability

You are responsible for all contributions made under your GitHub account. This tool is provided as-is with no warranty.
