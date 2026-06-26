# Synder Importer API — Full Reference

## Response Schemas

### GET /account
```json
{
  "id": "5",
  "email": "user@company.com",
  "firstName": "Jane",
  "lastName": "Doe",
  "status": "ACTIVE",
  "companiesAmount": 2,
  "successfulImports": 142,
  "subscription": {"plan": "Professional", "active": true}
}
```

### GET /companies
```json
[
  {
    "id": "9",
    "companyName": "Acme Corp",
    "provider": "intuit",
    "companyAddress": "123 Main St, San Francisco, CA",
    "status": "ACTIVE",
    "settings": {
      "dateFormat": "MM/dd/yyyy",
      "incrementDocNumber": false,
      "sendDocNumberToProvider": true
    }
  }
]
```
Providers: `intuit` (QuickBooks Online), `xero` (Xero). No other providers supported.

### GET /companies/{id}/entities
```json
[
  {"id": "42", "name": "Invoice", "provider": "intuit"},
  {"id": "43", "name": "Bill", "provider": "intuit"}
]
```

### GET /companies/{id}/entities/{name}/fields
```json
[
  {
    "id": "231",
    "title": "DocNumber",
    "type": "String",
    "isRequired": false,
    "isForGrouping": true,
    "maxSize": 21,
    "childElemName": null,
    "alternativeTitles": ["Invoice Number", "Invoice #", "Inv No"],
    "predefinedValues": [],
    "enablingGuideUrl": null,
    "orderNumber": 1
  }
]
```
Field types: `String`, `Boolean`, `Date`, `Decimal`, `Integer`, `DateTime`, `CustomerRef`, `Array`

### POST /companies/{id}/mappings
Request:
```json
{
  "title": "My Mapping",
  "entityName": "Invoice",
  "fields": [
    {"sourceFieldTitle": "Invoice #", "targetFieldId": "231"},
    {"sourceFieldTitle": null, "targetFieldId": "234", "fixedValue": "constant"}
  ]
}
```
Response (201):
```json
{
  "id": "31",
  "title": "My Mapping",
  "entityName": "Invoice",
  "active": true,
  "createdAt": "2026-03-11T10:30:00Z",
  "fields": [
    {"sourceFieldTitle": "Invoice #", "targetFieldId": "231", "fixedValue": null},
    {"sourceFieldTitle": null, "targetFieldId": "234", "fixedValue": "constant"}
  ]
}
```

### POST /companies/{id}/imports
Multipart form: `file` (CSV/XLSX) + `mappingId` (string). Header: `Idempotency-Key`.

Response (202):
```json
{
  "id": "42",
  "status": "SCHEDULED",
  "mappingId": "31",
  "entityName": "Invoice",
  "company": {"id": "9", "name": "Acme Corp"}
}
```

### POST /companies/{id}/imports/auto
Multipart form: `file` + `entityName` + `dryRun` (true/false, default true).

Response (200, dryRun=true):
```json
{
  "entityName": "Invoice",
  "fileHeaders": ["Invoice #", "Customer", "Date", "Amount"],
  "proposedFields": [
    {"sourceFieldTitle": "Invoice #", "targetFieldId": "231", "targetFieldName": "DocNumber", "confidence": "high", "isRequired": false},
    {"sourceFieldTitle": "Amount", "targetFieldId": "237", "targetFieldName": "Line.Amount", "confidence": "medium", "isRequired": true}
  ],
  "missingRequired": [],
  "totalFieldsMapped": 4,
  "totalEntityFields": 67
}
```
Confidence: `high` (exact title match), `medium` (matched via alternativeTitles).

### GET /companies/{id}/imports/{iid}
```json
{
  "id": "42",
  "status": "FINISHED",
  "entityName": "Invoice",
  "mappingId": "31",
  "dateCreated": "2026-03-11T10:35:00Z",
  "dateFinished": "2026-03-11T10:35:18Z",
  "summary": {"total": 25, "succeeded": 23, "failed": 2, "warnings": 1}
}
```

### GET /companies/{id}/imports/{iid}/results
Query params: `type` (INFO/WARNING/ERROR), `page`, `perPage` (max 100).
```json
{
  "data": [
    {
      "orderNumber": 1,
      "type": "INFO",
      "text": "Invoice #1001 created successfully",
      "objectProviderId": "438",
      "objectInfo": "Invoice #1001 for Acme Corp",
      "isReverted": false,
      "isUpdated": false
    }
  ],
  "pagination": {"page": 1, "perPage": 20, "total": 25, "totalPages": 2}
}
```

### POST /companies/{id}/imports/{iid}/cancel
No body required. Returns 202. Only works on SCHEDULED or IN_PROGRESS imports.

### POST /companies/{id}/imports/{iid}/revert
Optional body: `{"reason": "..."}`. Returns 202. Only works on FINISHED imports. Deletes all created entities from the accounting system.

### PUT /companies/{id}/mappings/{mid}
Same body as POST. Returns 200.

### DELETE /companies/{id}/mappings/{mid}
Soft delete (sets active=false). Returns 204.

### GET/POST /companies/{id}/settings
GET returns current settings. POST updates them.

Settings fields (intuit): `dateFormat`, `incrementDocNumber`, `sendDocNumberToProvider`, `createProducts`, `productType`, `productIncomeAccount`, `createPersons`, `createAccounts`, `skipDuplicatedImports`, `gstRegistered`, etc.

## Status Lifecycle

```
SCHEDULED → IN_PROGRESS → FINISHED
                        → FINISHED_WITH_WARNINGS
                        → FAILED
                        → CANCELED
FINISHED               → REVERTING → REVERTED
```

## QBO Entity Guide

| Entity | Use For | Key Required Fields |
|--------|---------|-------------------|
| Invoice | Sales invoices | CustomerRef, Line.Amount, Line.ItemRef |
| Bill | Vendor bills | VendorRef.name, Line.Amount |
| JournalEntry | Journal entries | DocNumber, Line.Amount, Line.AccountRef.name |
| Customer | Customer records | DisplayName |
| Vendor | Vendor records | DisplayName |
| Expense | Expenses | AccountRef.name, Line.Amount |
| SalesReceipt | Cash sales | CustomerRef, Line.Amount |
| Payment | Customer payments | CustomerRef, TotalAmt |
| CreditMemo | Credit memos | CustomerRef, Line.Amount |
| Estimate | Estimates/quotes | CustomerRef, Line.Amount |
| PurchaseOrder | Purchase orders | VendorRef.name, Line.Amount |
