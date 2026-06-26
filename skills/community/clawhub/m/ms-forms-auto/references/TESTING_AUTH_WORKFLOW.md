# Authentication Workflow Fix - Testing & Verification

## Problem
The original `submit-with-mfa.js` script **always required** an MFA code, even when the login could succeed with just username and password. This was inflexible and caused failures when MFA wasn't actually needed.

## Solution Implemented
Rewrote the script with **smart authentication** that:
1. Auto-detects whether MFA is required after credentials entry
2. Accepts optional `--code` argument (only used if MFA appears)
3. Handles both scenarios gracefully:
   - **No MFA needed**: Credentials alone suffice → submits directly
   - **MFA needed**: Uses provided code (if any) or waits 30s for manual entry

## Testing Plan

### Prerequisites
- ✅ Skill installed at `~/.openclaw/skills/ms-forms-auto`
- ✅ `config/credentials.json` exists with valid M365 email/password
- ✅ `config/storageState.json` may exist (cached session) or be absent
- ✅ `daily-entries/2026-03-20.json` exists (backfilled entry for testing)

---

### Test Case 1: Credential-Only Login (No MFA)
**Scenario:** Storage state is invalid/absent, and this particular login does NOT trigger MFA.

**Steps:**
```bash
cd /home/ubuntu/.openclaw/workspace/skills/ms-forms-auto
node scripts/submit-with-mfa.js --date 2026-03-20
```

**Expected Behavior:**
1. Browser opens (headed via xvfb)
2. Navigates to form URL → redirects to login.microsoftonline.com
3. Enters email and password automatically
4. **No MFA prompt appears** (or disappears quickly)
5. Redirects to form page
6. Fills March 20 entry from `daily-entries/2026-03-20.json`
7. Submits form successfully
8. Exit code: `0`
9. Auth state saved to `config/storageState.json`

**Success Criteria:** Form submits without requiring any MFA code interaction.

---

### Test Case 2: MFA Required - Code Provided
**Scenario:** Storage state invalid, and MFA is triggered. Code provided via `--code`.

**Steps:**
```bash
cd /home/ubuntu/.openclaw/workspace/skills/ms-forms-auto
node scripts/submit-with-mfa.js --code 123456 --date 2026-03-20
```

**Expected Behavior:**
1. Browser opens
2. Enters email and password
3. Detects MFA input field
4. Enters the provided 6-digit code
5. Clicks submit on MFA screen
6. Handles "Stay signed in?" prompt (clicks Yes)
7. Redirects to form
8. Fills and submits March 20 entry
9. Exit code: `0`
10. Auth state saved

**Success Criteria:** Form submits successfully using the provided MFA code.

---

### Test Case 3: MFA Required - No Code (Manual Entry)
**Scenario:** MFA triggered but no code provided upfront. Browser stays open for 30s for manual entry.

**Steps:**
```bash
cd /home/ubuntu/.openclaw/workspace/skills/ms-forms-auto
node scripts/submit-with-mfa.js --date 2026-03-20
```

**Expected Behavior:**
1. Enters email and password
2. Detects MFA input field
3. **No code provided**, so:
   - Prints: "❌ MFA required but no code provided. Use --code flag."
   - Waits 30 seconds with browser open
   - If you manually type code during wait, it will proceed
   - If not, exits with code `2`

**Success Criteria:** Graceful handling, no crash, clear error message, exit code 2 if no manual intervention.

---

### Test Case 4: Already Authenticated (Cached Session)
**Scenario:** `config/storageState.json` contains a valid session cookie. No login needed.

**Steps:**
1. Ensure you have a valid `storageState.json` (from any previous successful login)
2. Run:
```bash
node scripts/submit-with-mfa.js --date 2026-03-20
```

**Expected Behavior:**
1. Browser opens, navigates to form URL
2. Already on form page (not redirected to login)
3. Skips credential entry entirely
4. Immediately fills and submits the form
5. Exit code: `0`

**Success Criteria:** Direct navigation to form, no login steps, fast submission.

---

### Test Case 5: Invalid Credentials
**Scenario:** Wrong email or password in `config/credentials.json`.

**Steps:**
```bash
node scripts/submit-with-mfa.js --date 2026-03-20 --code 123456
```

**Expected Behavior:**
1. Enters email and password
2. Detects error message on page ("Incorrect", "Invalid", "error")
3. Throws exception, closes browser
4. Exit code: `1`
5. Error message: "Login failed: Invalid email/password or account locked"

**Success Criteria:** Clear error, proper exit code, no false success.

---

## Warm/Cache Handling
**Important:** The script saves the auth state after every successful submission. This means:
- Next run will use cached session → no MFA (Test Case 4)
- To force fresh login for testing, delete `config/storageState.json` before Test Cases 1-3.

```bash
rm /home/ubuntu/.openclaw/workspace/skills/ms-forms-auto/config/storageState.json
```

---

## Integration Testing with Daily Cron

After verifying manual tests pass, we should also verify the cron job works:

### Cron Job Reference
- **Pre-Fill:** 5:45 PM SGT (Mon-Fri) → isolated agent → `calendar-fetch.js`
- **Submit:** 6:00 PM SGT (Mon-Fri) → main session → asks for MFA code → runs `submit-with-mfa.js --code [CODE]`

The cron's behavior is unchanged. It will still ask Master for the 6-digit code at 6 PM. The improved script will:
- Use the code if MFA appears
- Ignore it if no MFA needed
- Still succeed in either case

**Test with cron simulation:**
```bash
# In main session (simulating 6 PM trigger):
cd /home/ubuntu/.openclaw/workspace/skills/ms-forms-auto
node scripts/submit-with-mfa.js --code 123456 --date 2026-03-20
```

---

## Additional Edge Cases to Consider

1. **Conditional MFA**: Sometimes MFA is required based on IP/device. If testing from a different network than usual, MFA may always be required.

2. **"Stay signed in?" Prompt**: The script automatically clicks "Yes" if detected. If Microsoft changes the button text, detection might fail but it won't break the flow.

3. **Form Layout Changes**: The script relies on input field ordering. If the form changes, field mapping could break. Verify after any form edit by running calendar-fetch.js first to see the data.

4. **Network Timeouts**: Playwright timeouts are set at 60s for goto, 5-8s for waits. Adjust if your connection is slow.

---

## Rollback Plan

If something goes wrong, revert to previous version:
```bash
cd /home/ubuntu/.openclaw/workspace/skills/ms-forms-auto
git checkout HEAD -- scripts/submit-with-mfa.js
```

The old version is still in git history (commit before March 21 changes).

---

## Success Checklist

- [ ] Test Case 1 passes (no MFA, no code)
- [ ] Test Case 2 passes (MFA with code)
- [ ] Test Case 4 passes (cached session)
- [ ] Test Case 5 passes (invalid credentials error)
- [ ] No regressions in other scripts (calendar-fetch, pre-fill cron)
- [ ] March 20 entry submitted successfully at least once
- [ ] March 21 pre-fill generated correctly (already working per MEMORY.md)

---

## Next Steps After Testing

1. Run through all test cases that apply to your scenario
2. Document any failures or unexpected behaviors
3. If all pass, the skill is fixed and ready for daily cron
4. Update MEMORY.md with testing results and final status

---

**Testing Date:** _____________
**Tester:** _____________
**Result:** [ ] PASS  [ ] FAIL  [ ] NEEDS REVISION
**Notes:**
