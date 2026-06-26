# Hemlane Financials HAR Summary

Source captures:
- `~/Downloads/har/financials_hemlane.com.har`
- `~/Downloads/har/financials_pages_hemlane.com.har`

These files are runtime captures and are not copied into the skill because they may contain browser/session data.

Combined GraphQL operation coverage:

- `BankTransactionsPageFiltersQuery` (query, 2 request(s)); variables: none
- `FinancialsScheduledActionPanelStats` (query, 5 request(s)); variables: paymentCategoryId, paymentSubcategoryId, propertyId, propertyUnitId, portfolioId, ownerUserId, sourceTenantGroupId, sourceUserId, destinationUserId, dueDateBegin, dueDateEnd, status
- `GetPaymentCategoriesAndSubCat` (query, 1 request(s)); variables: billToUserId
- `GetPaymentCategoriesMui` (query, 1 request(s)); variables: none
- `GetPlaidSyncItems` (query, 4 request(s)); variables: none
- `GetSubcategoryBillToUsers` (query, 1 request(s)); variables: none
- `GetTransactionsNextDestinationUserIds` (query, 2 request(s)); variables: status, dueDateBegin, dueDateEnd, paymentCategoryId, paymentReferenceNumber, paymentSubcategoryId, propertyId, propertyUnitId, userId
- `GetTransactionsNextSourceTenantGroupIds` (query, 2 request(s)); variables: status, dueDateBegin, dueDateEnd, paymentCategoryId, paymentReferenceNumber, paymentSubcategoryId, propertyId, propertyUnitId, destinationUserId
- `GetTransactionsNextSourceUserIds` (query, 2 request(s)); variables: status, dueDateBegin, dueDateEnd, paymentCategoryId, paymentReferenceNumber, paymentSubcategoryId, propertyId, propertyUnitId, destinationUserId
- `MyAppNotificationStats` (query, 1 request(s)); variables: none
- `OD2ManagementFeeOverview2` (query, 1 request(s)); variables: page, limit, accountPropertyOwnerId
- `OD2ManagementFeeOverviewAvailableAccountPropertyOwners` (query, 1 request(s)); variables: none
- `OD2PropertiesAndPortfolios` (query, 1 request(s)); variables: none
- `OD2Session` (query, 1 request(s)); variables: none
- `OD2TasksCount` (query, 1 request(s)); variables: none
- `ODGetContextValues` (query, 1 request(s)); variables: none
- `Od2MyAppNotificationStats` (query, 1 request(s)); variables: none
- `PageFiltersOwnerUserFilterQuery` (query, 3 request(s)); variables: none
- `PageFiltersPortfolioFilterQuery` (query, 3 request(s)); variables: none
- `PageFiltersPropertySearchQuery` (query, 14 request(s)); variables: search, id, propertyOnly, ownerUserId, portfolioId, isDeleted, searchAlgo
- `PagedFinancialTransactions` (query, 10 request(s)); variables: page, plaidAccountId, minAbsAmountInCents, maxAbsAmountInCents, paymentSubcategoryId, paymentCategoryId, keyword, portfolioId, ownerUserId, propertyId, propertyUnitId, view
- `RecurringNextCursorQuery` (query, 7 request(s)); variables: pagination, propertyId, propertyUnitId, portfolioId, ownerUserId
- `TasksCount` (query, 2 request(s)); variables: none
- `TransactionsNextCursorQuery` (query, 6 request(s)); variables: paymentReferenceNumber, dueDateBegin, dueDateEnd, propertyId, propertyUnitId, portfolioId, ownerUserId, pagination, status, paymentCategoryId, paymentSubcategoryId, destinationUserId, sourceUserId, sourceTenantGroupId, sortOrder

Implemented wrappers:

- `scripts/query_recurring_payment_requests.py`: typed helper around `RecurringNextCursorQuery` for active/expired recurring rent/payment requests.
- `scripts/query_financials_operation.py`: generic read-oriented Financials GraphQL replay helper. It loads query + sample variables from the financials HARs, merges `--variables-json`, and supports `--page`, `--limit`, and `--all-pages` for known paged operations.
- MCP tool `query_recurring_payment_requests`: typed recurring request summaries.
- MCP tool `query_financials_operation`: generic Financials operation replay/page navigation.

Useful operations:

- `RecurringNextCursorQuery`: recurring rent / PM fee requests.
- `TransactionsNextCursorQuery`: Hemlane payment requests/transactions cursor.
- `PagedFinancialTransactions`: bank/financial transaction ledger page.
- `FinancialsScheduledActionPanelStats`: scheduled/action stats for a filtered financials view.
- `BankTransactionsPageFiltersQuery`, `GetPlaidSyncItems`, `GetTransactionsNextSourceTenantGroupIds`, `GetTransactionsNextSourceUserIds`, `GetTransactionsNextDestinationUserIds`: filters/support lookups.

Auth note: use `capture_hemlane_auth_via_cdp.py --endpoint-kind financials-recurring --out-file /tmp/hemlane-auth.json`. Runtime cookies/tokens must not be stored in the skill.
