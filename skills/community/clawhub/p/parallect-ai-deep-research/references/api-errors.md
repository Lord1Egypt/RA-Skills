# Parallect API Error Reference

Read this file when a Parallect MCP tool returns an error response.

## Error Codes

### INSUFFICIENT_BALANCE

The user's credit balance is too low for the requested budget tier and
they have no payment method on file for auto-top-up.

**Response fields:**
- `balanceCents` — current balance
- `requiredCents` — minimum balance needed for the tier

**What to tell the user:**
"Your balance is $X.XX but this [tier] research needs at least $Y.YY.
You can add credits at https://parallect.ai/settings/billing"

**Recovery:** User must add credits or a payment method. You cannot
proceed without sufficient funds.

### PAYMENT_FAILED

The user has a payment method on file but the charge was declined.

**What to tell the user:**
"Your payment method was declined. Please update it at
https://parallect.ai/settings/billing"

**Recovery:** User must update their payment method.

### JOB_NOT_FOUND

The job ID doesn't exist or doesn't belong to the user's project.

**Common causes:**
- Typo in the job ID
- Job was from a different account
- Job was deleted

**Recovery:** Call `list_threads` to find recent jobs and verify the
correct job ID.

### JOB_NOT_COMPLETE

You called `get_results` before the job finished.

**Response fields:**
- `status` — current job status (e.g., "running", "synthesizing")

**Recovery:** Continue polling with `research_status`. Do not call
`get_results` again until status is "completed".

### INVALID_TOPIC

You tried to use a follow-on suggestion index that doesn't exist.

**Response fields:**
- `availableSuggestions` — array of valid follow-on topics

**Recovery:** Use a valid `topicIndex` from the suggestions array,
or provide a `customQuery` instead.

### RATE_LIMITED

Too many requests in a short period.

**Recovery:** Wait 60 seconds before retrying. Reduce polling frequency
if this happens during status checks.

## HTTP Status Codes

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 201 | Created (new thread/job) |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (bad or missing API key) |
| 402 | Payment required (insufficient balance) |
| 404 | Not found (invalid ID) |
| 409 | Conflict (duplicate operation) |
| 429 | Rate limited |
| 500 | Server error (retry once after 30s) |
