---
name: openmandate
description: >-
  Post mandates and find matches on OpenMandate — ongoing matching for cofounders and early teams.
  Use when creating mandates, answering intake questions, reviewing matches,
  or integrating OpenMandate into applications. Works via MCP tools (preferred),
  Python/JS SDKs, or the bundled shell helper. Requires OPENMANDATE_API_KEY.
version: 0.6.0
homepage: https://openmandate.ai
license: MIT
metadata:
  author: openmandate
  version: "0.6.0"
  openclaw:
    emoji: "handshake"
    requires:
      env:
        - OPENMANDATE_API_KEY
        - OPENMANDATE_BASE_URL
      bins:
        - python3
    primaryEnv: OPENMANDATE_API_KEY
---

# OpenMandate

Post a mandate — what you need and what you offer. OpenMandate keeps working on your behalf and introduces both sides when there is strong mutual fit.

## Setup

**1. Get an API key.** Your user signs up at [openmandate.ai](https://openmandate.ai) and creates a key on the API Keys page.

**2. Set the environment variable:**

```bash
export OPENMANDATE_API_KEY="om_live_..."
```

If `OPENMANDATE_API_KEY` is not set, stop and ask the user to create one at https://openmandate.ai/api-keys

## How to Interact with OpenMandate

**Preferred: MCP tools.** If your coding agent supports MCP, configure the OpenMandate MCP server ([setup guide](https://github.com/openmandate/skills#mcp-setup)). You get 15 tools: `list_contacts`, `add_contact`, `verify_contact`, `update_contact`, `delete_contact`, `resend_otp`, `create_mandate`, `get_mandate`, `list_mandates`, `submit_answers`, `close_mandate`, `list_matches`, `get_match`, `respond_to_match`, `submit_outcome`. Use them directly.

**Fallback: Shell helper.** For agents without MCP support, use the bundled Python script:

```bash
python3 {baseDir}/scripts/openmandate.py <command> [args]
```

No pip dependencies. Stdlib only. Python 3.8+.

**For developers: SDKs.** Python (`pip install openmandate`) or JavaScript (`npm install openmandate`). See `references/sdks.md`.

## Workflow

```
check/add contacts → create mandate (want + offer) → answer follow-up questions → mandate goes active
→ OpenMandate keeps working on your behalf → match found → you get notified → review match
→ accept or decline → if both accept, contact info revealed → report outcome
```

Before creating a mandate, ensure the user has at least one verified contact. Use `list contacts` to check. If none exist, use `add-contact` to add an email and `verify-contact` with the OTP code.

One mandate = one match. The agent keeps looking until it finds the right one.

## MCP Tools Reference

All tools are prefixed with `openmandate_`:

| Tool | Purpose |
|------|---------|
| `openmandate_list_contacts` | List verified contacts. Check before creating a mandate. |
| `openmandate_add_contact` | Add an email contact. Sends a verification code (OTP). |
| `openmandate_verify_contact` | Verify a contact with the OTP code from email. |
| `openmandate_update_contact` | Update display label or set a contact as primary. |
| `openmandate_delete_contact` | Permanently delete a contact. |
| `openmandate_resend_otp` | Resend verification code for a pending contact. |
| `openmandate_create_mandate` | Create a new mandate. Auto-selects primary verified contact. |
| `openmandate_get_mandate` | Get mandate details by ID. |
| `openmandate_list_mandates` | List open mandates (default). Pass `status` to filter (e.g. `closed` for history). |
| `openmandate_submit_answers` | Submit answers to intake questions. Check response for more `pending_questions`. |
| `openmandate_close_mandate` | Permanently close a mandate. |
| `openmandate_list_matches` | List all matches. |
| `openmandate_get_match` | Get match details — grade, strengths, concerns. Contact info after mutual accept. |
| `openmandate_respond_to_match` | Accept or decline a match. Pass `action`: `"accept"` or `"decline"`. |
| `openmandate_submit_outcome` | Report how a confirmed match went. Pass `outcome`: `"succeeded"`, `"ongoing"`, or `"failed"`. |

## Shell Commands Reference

### Contact Management

```bash
python3 {baseDir}/scripts/openmandate.py contacts                          # List contacts
python3 {baseDir}/scripts/openmandate.py add-contact user@example.com      # Add email contact (sends OTP)
python3 {baseDir}/scripts/openmandate.py verify-contact vc_abc123 12345678 # Verify with OTP code
python3 {baseDir}/scripts/openmandate.py update-contact vc_abc123 --label "Work" --primary  # Update contact
python3 {baseDir}/scripts/openmandate.py delete-contact vc_abc123          # Delete a contact
python3 {baseDir}/scripts/openmandate.py resend-otp vc_abc123              # Resend verification code
```

### Create a Mandate

```bash
python3 {baseDir}/scripts/openmandate.py create "Looking for a UX agency for our B2B dashboard" "Series A fintech, $1.8M ARR, two frontend engineers ready"
```

- Two required positional arguments: `want` (what you're looking for) and `offer` (what you bring).
- Primary verified contact is auto-selected.

Returns the mandate with `status: "intake"` and `pending_questions`.

### Answer Intake Questions

```bash
python3 {baseDir}/scripts/openmandate.py answer mnd_abc123 '[{"question_id":"q_xxx","value":"We need a UX agency for our B2B dashboard. Budget $40-60K, 8 weeks."}]'
```

**This is the critical loop.** After each answer submission:
1. Check `pending_questions` in the response
2. If not empty — read the new questions, answer them, submit again
3. If empty and `status` is `"active"` — intake is done, an agent starts working on your behalf

Question types:
- `text`: Write a substantive answer. Respect `min_length` in constraints. Give specifics.
- `single_select`: Pick one `value` from the `options` array. Use the option `value` field, not the `label`.
- `multi_select`: Comma-separated `value` strings from `options`, e.g. `"option_a, option_b"`.

**Answer each question distinctly.** "What are you looking for?" and "What do you bring to the table?" are different questions — give different answers.

### Other Commands

```bash
python3 {baseDir}/scripts/openmandate.py get mnd_abc123       # Get mandate details
python3 {baseDir}/scripts/openmandate.py list                  # List all mandates
python3 {baseDir}/scripts/openmandate.py list --status active  # Filter by status
python3 {baseDir}/scripts/openmandate.py close mnd_abc123      # Close a mandate
python3 {baseDir}/scripts/openmandate.py matches               # List all matches
python3 {baseDir}/scripts/openmandate.py match m_xyz789        # Get match details
python3 {baseDir}/scripts/openmandate.py accept m_xyz789       # Accept a match
python3 {baseDir}/scripts/openmandate.py decline m_xyz789      # Decline a match
python3 {baseDir}/scripts/openmandate.py outcome m_xyz789 succeeded  # Report match outcome
```

## Full Example (Shell)

```bash
# 1. Add and verify a contact
python3 {baseDir}/scripts/openmandate.py add-contact alice@company.com
# → contact_id: vc_abc123, status: "pending", OTP sent to email

python3 {baseDir}/scripts/openmandate.py verify-contact vc_abc123 12345678
# → status: "verified"

# 2. Create mandate with want + offer (auto-selects verified contact)
python3 {baseDir}/scripts/openmandate.py create \
  "We need a UX design agency for our B2B analytics dashboard. 120 enterprise customers, React frontend. Budget $40-60K, 8 weeks." \
  "Series A fintech SaaS, $1.8M ARR. Two frontend engineers ready to implement."
# → mandate_id: mnd_abc123, pending_questions: [{id: "q_3", ...}]

# 3. Answer follow-up questions (read each question carefully, answer specifically)
python3 {baseDir}/scripts/openmandate.py answer mnd_abc123 '[
  {"question_id":"q_3","value":"deep_user_research"},
  {"question_id":"q_4","value":"Filtering system is the biggest pain point. Users need to slice across 12 dimensions."}
]'
# → status: "active", pending_questions: [] — intake done

# 4. Check for matches (user will be emailed when one is found)
python3 {baseDir}/scripts/openmandate.py matches

# 5. Review and respond
python3 {baseDir}/scripts/openmandate.py match m_xyz789
python3 {baseDir}/scripts/openmandate.py accept m_xyz789

# 6. After both accept, check for revealed contact
python3 {baseDir}/scripts/openmandate.py match m_xyz789
# → contact: {email: "bob@agency.com"}

# 7. Report how it went
python3 {baseDir}/scripts/openmandate.py outcome m_xyz789 succeeded
```

## Tips

- The user gets emailed when a match is found. No need to poll.
- OpenMandate may ask follow-up questions. Detailed answers lead to better matches.
- Matches are graded: Good Match, Strong Match, or Exceptional Match. Review strengths and concerns before accepting.
- For SDK usage patterns and API reference, see the `references/` directory.
