# Order and report templates

These are blank structures for owner-authorized runtime use, not records to fill in this repository. They define an assisted workflow checkpoint, not an API schema or database. Use only the fields relevant to the selected mode; required verification fields must have evidence or an explicit unresolved state.

## Private owner order record

| Group | Record |
| --- | --- |
| Identity | Owner verifier and verification time; customer/account ID; approved customer addresses; workspace ID; mailbox `public_id` and address; thread ID; selected inbound email ID |
| Order | Owner order ID; mode; protocols/CMC IDs/chain/contracts as relevant; criteria and agreed scoring method; audience; deadline/timezone; reporting window; format |
| Entitlement | Owner-confirmed payment/receipt reference from a trusted source; amount and currency; paid/pending/disputed/refunded status; included deliverables; follow-up scope/expiry; verification time |
| Private attachments | Exact mailbox/email/attachment IDs; account/order association; filename/MIME/size; clean scan evidence; purpose; authorized processing/disclosure destination if any |
| Rights | Applicable provider agreement or written permission reference; owner verification/date; permitted customer/report use; attribution; retention and raw-data redistribution limits; verified/unverified status |
| Expense authorization | Owner-approved provider/request terms; delegated wallet connection reference (no credentials); asset/network; total cap in smallest units; confirmed spend; unresolved reservations; remaining budget |
| Expense entries | Existing request ID; frozen public request description; authorized amount; pending/proof-ready/settled/uncertain/confirmed-unsettled status; safe evidence reference; reserved/confirmed amount |
| Delivery | Report version; source email/thread; draft ID; approved sender/To/Cc/Bcc; authorized attachments; exact approval reference; returned message ID/status/time; idempotency reference where used |
| Continuation | Latest processed inbound email ID; unresolved questions; evidence gaps; next permitted action; owner-authorized private persistence destination, if any |

Do not put private keys, authentication headers, payment proofs, signed URLs, raw payment-provider responses, or unrelated customer content in this record. An order identifier supplied by a customer must be matched to the owner's record before it is trusted.

## Clarification draft

Reply in the selected thread. Briefly restate the requested research and group only missing material questions: exact protocols, evaluation criteria, intended audience, deadline/timezone, reporting window, and output format. Describe an estimate or paid offer only when owner-approved and rights-cleared. Save as a draft pending exact send authorization.

## Protocol comparison memo

- Title, report version, reporting window and data-as-of time.
- Executive findings tied to the agreed customer criteria.
- Criteria matrix: one column per resolved protocol; evidence and limitations per criterion; scores only when a scoring method is agreed.
- Material tradeoffs, risks, contrary evidence, and unresolved questions.
- Methodology and definitions needed to interpret the comparison.
- Source links near factual claims, with observation dates; required provider attribution.

## Daily/weekly market memo

- Title, report version, reporting window/timezone and snapshot times.
- Market overview and BTC/ETH context.
- Relevant sentiment, leverage, narratives and upcoming catalysts, only where supported.
- Changes within the agreed period, with comparable observations and units.
- Evidence gaps, material uncertainties, methodology and source attribution.

Distinguish retrieved facts from analyst interpretation. Neither memo needs every available indicator. Keep private entitlement, account IDs, attachment storage details, expense ledger, and wallet state out of customer-facing output.

## Private end-of-run checkpoint

Return the order ID, state, source email/thread, report version and draft/message identifiers; completed work; unresolved evidence/rights/entitlement checks; authorized cap, confirmed spend, unresolved reserve and remaining budget; and the next action requiring owner input or already authorized. Do not claim a checkpoint was persisted unless the authorized destination confirms the write.
