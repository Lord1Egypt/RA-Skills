# Commerce and recovery

Author: Daniel Hallman

GISDB private tools require the connected GISDB account and the applicable `gisdb:read`, `gisdb:write`, `gisdb:checkout` or `gisdb:billing` permission. Untax owner/VA grants, cookies and payment credentials cannot authorize GISDB.

## Save and purchase

1. Read the saved search before resuming. Keep its latest revision, explicit answers and skipped question IDs.
2. If the source or offer changed, show the change and ask the user to confirm before continuing.
3. For an identical retry, reuse its idempotency key. Changed inputs need a new key.

Saving a search does not start a payment or subscription.

Show the returned offer's amount, currency, coverage, billing interval, source-check cadence and limitations. A recurring offer must be configured and match the selected saved search. Invoke `gisdb_create_checkout` only after the user requests that reviewed purchase. Retain its returned order ID. Payment details belong on the hosted checkout page; a checkout link or browser return is not payment evidence.

After browser return, an uncertain failure or a claimed payment, call `gisdb_get_order` for the same order ID. If checkout returned no order ID, retry with the original idempotency key. Read payment, subscription activity, entitlement and download availability separately. Pending, refunded, disputed or unverified payments must not be described as delivered purchases.

Keep the original search, offer, request and retry key together through the browser handoff. Do not change those inputs under an unresolved checkout attempt or create a replacement checkout to recover it. If both order ID and original key are lost, explain the missing recovery information and use only an actually returned account recovery path; do not invent an order-search tool.

## Verify delivery

Retrieve paid lead CSV files through the GISDB account inbox. Use only protected download paths returned for that account's order. County-record packages are a separate ZIP product. The first lead delivery uses the exact source selected at checkout, even if newer county data is available. Later recurring checks may use newer records under the same package terms.

Report an artifact only when its delivery state supports that claim; a URL or active subscription alone does not prove downloaded bytes. When testing delivery, verify the downloaded artifact against its returned identity. Share only the user's own order and download links. Do not promise email, activation, CSV delivery or no-new-leads without corresponding verified evidence.

## Manage updates and billing

Use `gisdb_get_lead_updates` for owned update status and available records. A successful empty or unchanged check differs from a failed source check. A failure preserves the last successful checkpoint; do not turn it into a claimed zero or reset the checkpoint.

For a requested update change, call `gisdb_set_lead_updates` with `action=pause` or `action=resume`, the returned delivery revision and a stable retry key. Resume requires current entitlement and source checks. Read the resulting update state. Pausing updates does not cancel billing.

Use `gisdb_cancel_subscription` only when the user requests stopping renewal; explain the returned period-end status and verify the same order. For requested billing management, use `gisdb_open_billing_portal`, then reread that order after browser changes. Do not substitute a delivery pause for cancellation.

On a revision conflict, read the current workflow or update state before proceeding; do not overwrite a newer choice blindly. Preserve returned source/offer holds and use the retry-key rules for the actual request. Distinguish returned authentication, permission, capability and source failures. A missing capability is not an empty search or proof of no new records, and another product's grant cannot resolve it.
