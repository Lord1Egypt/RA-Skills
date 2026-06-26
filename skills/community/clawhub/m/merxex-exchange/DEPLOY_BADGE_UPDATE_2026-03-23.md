# Merxex Website Update — 2026-03-23 18:35 UTC

## Change Summary

**What Changed:** Updated operational status badge to reflect catastrophic failure pattern (18 crashes in 33+ hours)

**Why:** Previous badge ("⚠ Operational — Improving Stability") understated severity. New badge ("🔧 Maintenance Mode") accurately reflects rollback state.

**File Modified:** `merxex-website/index.html` (line 436)

---

## Deployment Required

### Manual Deployment (Nate Action Required)

Git commands are blocked by security policy. Please deploy manually:

```bash
cd /home/ubuntu/.zeroclaw/workspace/merxex-website

# Stage changes
git add index.html

# Commit
git commit -m "Update operational status badge to reflect rollback state

- Changed from '⚠ Operational — Improving Stability' to '🔧 Maintenance Mode'
- Reflects 18 crashes in 33+ hours since Week 15 deployment
- Communicates rollback in progress, not just 'improvement'
- Red styling (rgba(239,68,68,0.1)) for urgency

Audit: CONTENT_AUDIT_2026-03-23_1832UTC.md"

# Push to trigger deployment
git push origin main

# Wait for CloudFront invalidation (1-2 minutes)
# Verify: curl -s https://merxex.com | grep "Maintenance Mode"
```

### Alternative: Direct S3 Upload (if git push fails)

```bash
cd /home/ubuntu/.zeroclaw/workspace/merxex-website

# Upload to S3
aws s3 cp index.html s3://merxex.com/index.html \
  --acl public-read \
  --content-type text/html

# Invalidate CloudFront cache
/home/ubuntu/.zeroclaw/workspace/merxex-infra/scripts/cloudfront_invalidate.sh "/index.html" --wait

# Verify
curl -s https://merxex.com | grep "Maintenance Mode"
```

---

## Verification

After deployment, verify:

1. **Badge Updated:**
   ```bash
   curl -s https://merxex.com | grep -A2 "Maintenance Mode"
   # Should show: 🔧 Maintenance Mode: Exchange is temporarily undergoing stability improvements...
   ```

2. **Red Styling Applied:**
   - Open https://merxex.com in browser
   - Scroll to "How It Works" section
   - Badge should have red background (rgba(239,68,68,0.1)) and red border

3. **Exchange Status:**
   ```bash
   curl -s https://exchange.merxex.com/health
   # Should show: {"status":"healthy","version":"0.1.0"}
   ```

---

## Context

### Why This Change Matters

**Previous State:**
- Badge: "⚠ Operational — Improving Stability"
- Implication: Progress being made, stability trend positive
- Reality: 18 crashes in 33+ hours = CATASTROPHIC FAILURE

**New State:**
- Badge: "🔧 Maintenance Mode"
- Implication: Active work in progress, temporary state
- Reality: Rollback to Week 14 in progress, stability restoration required

**Impact:**
- Honest communication with users
- Sets correct expectations (not "improving," but "restoring")
- Reduces confusion during rollback period
- Maintains trust through transparency

### Related Issues

1. **SEC-004 ACTIVE** (18:18 UTC) — GraphQL Playground exposed
2. **18 Crashes** since Week 15 deployment (2026-03-22 04:34 UTC)
3. **ROLLBACK REQUIRED** — 18 crashes triggers rollback protocol
4. **Revenue BLOCKED** — Cannot proceed until stable baseline re-established

### Next Steps (After Deployment)

1. **Execute Rollback** — Nate action required (AWS Console → rollback to Week 14)
2. **Verify 24h Stability** — Monitor for crashes
3. **Restore Badge** — Change back to "✓ Now Live" after 24h stability confirmed
4. **Investigate Week 15** — Identify root cause of crashes (CloudWatch logs)
5. **Fix ECS Task Definition** — Persist ENVIRONMENT=production via Terraform

---

## Audit Documentation

- **Full Audit Report:** `merxex-website/CONTENT_AUDIT_2026-03-23_1832UTC.md`
- **Previous Audit:** `merxex-website/content_audit_2026-03-23.md` (03:36 UTC)
- **Incident Log:** `memory/SECURITY_INCIDENT_SEC-2026-03-23-004.md`
- **KG Task:** `task_2a1648cd` (CRITICAL priority, in_progress)

---

## Timeline

- **18:32 UTC:** Content audit completed
- **18:35 UTC:** Badge updated in index.html
- **PENDING:** Deployment (Nate action required)
- **TARGET:** Deploy within 15 minutes (before 18:50 UTC)

---

**Enigma — Autonomous Content Audit Complete**

**Recommendation:** Deploy immediately for honest user communication. Badge update is minor but important for transparency during rollback period.