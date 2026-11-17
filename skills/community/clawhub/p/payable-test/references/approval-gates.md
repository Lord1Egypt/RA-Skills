# Approval gates for payable tests

Run Authorization permits private payable-test design, drafting, analysis, and
artifact creation without another approval. It never authorizes an external
action. Return private artifacts to `moneyprinter` for Money Machine Run
continuation until an exact action is ready.

## Required gate

- Drafting is reversible and may proceed.
- Sending, posting, publishing, purchasing, charging, signing, submitting, or
  changing an account is an external action.
- Approval is valid only when the approver controls the named account or action,
  any third-party data has an authorized consent or lawful-use basis, and any
  required regulated review has passed for the named jurisdiction and scope.
- Immediately before an external action, show the action, exact payload,
  destination, channel, account, timing, scope, volume, tool, expected cost,
  evidence label, rollback or correction path, and prerequisite statuses.
- Before exact approval, keep the action staged. After an immediately preceding
  exact approval, the current host may perform only that approved action with
  its available tools, record an `Action receipt`, and return the result to
  `moneyprinter`.

Route selection, offer approval, a prior approval, and permission to draft do
not authorize an external action. Do not batch unrelated actions under one
approval. Treat `Unknown` or `Fail` in authority, third-party-data, or
regulated-review status as a hard stop; do not ask the human to approve around
the missing prerequisite.

## Approval checkpoint format

Immediately before execution, present:

```markdown
Action: [send/post/publish/purchase/charge/sign/submit/account change]
Exact payload: [the final text, asset, order, charge amount, agreement, or setting]
Destination: [named recipient, audience, platform, vendor, or system]
Channel: [email/DM/post/listing/payment rail/contract flow/account surface]
Account: [named sending, publishing, purchasing, payment, or system account]
Timing: [execution date/time or bounded window]
Scope: [one exact action and its included payload, audience, or commitment]
Volume: [one recipient/item or exact bounded count]
Tool: [host tool, connector, browser, CLI, or service used for execution]
Expected cost: [cash amount/currency, staff time, fee, or "none known"]
Evidence label: [label that the action could support]
Rollback or correction path: [how it can be withdrawn, corrected, refunded, reversed, or remediated]
Approver authority status: [Pass + basis / Unknown / Fail]
Third-party data status: [None used / Pass + consent or lawful-use basis and minimum data / Unknown / Fail]
Regulated-review status: [Not applicable / Pass + qualified reviewer, jurisdiction, and approved scope / Unknown / Fail]
Approval requested: Approve this exact action now? [yes/no]
```

Keep the asset staged until the human explicitly approves the exact action.
Do not put credentials, raw personal data, confidential files, or unnecessary
identifiers in the checkpoint; record a redacted basis instead. If any required
status is `Unknown` or `Fail`, replace the approval request with
`Execution blocked — prerequisite unresolved`.
For a charge, preorder, deposit, or booking, include the price, currency,
payment timing, delivery obligation, cancellation/refund terms, and who has
authority to fulfill or correct it.

## Reapproval

Require a new immediate approval if any checkpoint field changes, including the
action, payload, destination, channel, account, timing, scope, volume, tool,
cost, evidence label, rollback/correction path, approver authority status,
third-party data status, data basis or minimization, or regulated-review status.
Recipient/audience, price, spend, fee, payment timing, delivery terms, legal or
policy status, data used, and fulfillment authority are also material execution
facts. If the rollback path or a prerequisite status is unavailable or
uncertain, stop rather than execute.
Broad, batch, or stale permission is never valid, and one approval cannot cover
multiple actions. The `Action receipt` must record the approved action, actual
payload and destination, channel and account, timing, scope, volume, tool,
execution time, actual cost, prerequisite statuses, observed result or error,
evidence label, and rollback or correction taken or available.
