# Hemlane runbooks

## Referral submit
1. Use `references/graphql-operations.md` and locate `HubspotFormSubmit`.
2. Reconstruct the mutation payload with fields for first name, last name, phone, email, referrer name, and referrer email.
3. Preserve the captured `formId` from the HAR-derived sample unless a newer form capture supersedes it.
4. Submit to `https://api.hemlane.com/graphql` with fresh browser session cookies and any CSRF/header requirements available at runtime.
5. Validate success by checking `hubspotFormSubmission.id` and empty `errors`.

Key operation:
- `HubspotFormSubmit`

## Tenant reply
1. Identify the target tenant group ID from `ODTenantsAndLeasesTenantGroups` or an existing message thread.
2. Optionally re-read context with:
   - `TGTenantGroup`
   - `OwnerTenancyMessages`
3. Send the reply with the confirmed HAR-derived mutation:
   - `ODProspectiveTenantGroupMessageCreate`
4. Use `scripts/send_hemlane_tenant_reply.py` for the live wrapper.
5. Confirm by re-querying `OwnerTenancyMessages` after submit.

Confirmed live mutation:
- `ODProspectiveTenantGroupMessageCreate`
- field alias: `tenantGroupMessageAdd: tenantGroupMessageAdd2(input: $input)`

## Maintenance / work-order comment
1. Find the maintenance request or work order ID from the UI or prior query.
2. Query request/work-order details first to confirm the record:
   - `OwnerDashboardMaintenanceMaintenanceRequest`
   - `OwnerDashboardMaintenanceMaintenanceRequestComments`
   - `OwnerDashboardMaintenanceMaintenanceRequestWorkOrders`
   - `OwnerMaintenanceWorkOrder`
   - `OwnerMaintenanceWorkOrderComments`
3. Post the comment using the matching create mutation:
   - `OwnerDashboardMaintenanceMaintenanceRequestCommentCreate`
   - or `OwnerMaintenanceWorkOrderCommentCreate`
4. Include visibility flags exactly as captured (`isHiddenFromTenants`, `isHiddenFromOwners`) when applicable.
5. Re-query comments after submit to verify persistence.

## Transaction lookup
1. Use `PagedFinancialTransactions` or `TransactionsNextCursorQuery` to page through transactions.
2. Use `FinancialsScheduledActionPanelStats` for summary context and `GetPlaidSyncItems` if bank-sync state matters.
3. Preserve pagination variables/cursors from the captured pattern.
4. Re-run query with tighter filters (property, owner, due date, category) when narrowing a result set.
5. Validate by comparing total count / next cursor / returned transaction IDs.

## Workflow-specific wrappers
- `scripts/submit_hemlane_referral.py`
- `scripts/post_hemlane_workorder_comment.py`
- `scripts/post_hemlane_maintenance_request_comment.py`
- `scripts/send_hemlane_tenant_reply.py`

