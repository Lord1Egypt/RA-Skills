# OData v4 query syntax

Use this reference when translating a request into an OData URL. All examples are relative to a service root and use portable v4.0 spelling.

## Resource paths and keys

```text
Products
Products(42)
People('alice@example.com')
OrderLines(OrderId=10,LineNo=2)
Customers('ALFKI')/Orders
```

Derive key names and EDM types from metadata. Quote string keys with single quotes and escape an embedded quote by doubling it: `People('O''Neil')`. Do not quote numeric or Boolean keys. Date/time/GUID literal syntax depends on the EDM type and OData v4 rules; do not reuse v2/v3 prefixes such as `guid'...'` or `datetime'...'`.

## Core system query options

```text
Products?$select=Id,Name,Price
Products?$filter=Price gt 10 and Discontinued eq false
Products?$orderby=Price desc,Name asc&$top=20
Products?$count=true&$top=0
Customers?$expand=Orders($select=Id,Total;$filter=Total gt 100;$top=5)
```

- `$select`: return only required structural properties. Include keys when they help identify or join results.
- `$filter`: retain entities for which the Boolean expression evaluates to true.
- `$orderby`: make top-N and paged requests deterministic by adding a unique key as a final tie-breaker when the service permits it.
- `$top`: cap returned members. The service may still return fewer and provide a next link.
- `$skip`: request an offset only if supported; prefer service-issued next links for traversal.
- `$count=true`: request the total matching collection count inline. `EntitySet/$count` requests only the integer count.
- `$expand`: inline related entities. Keep depth and nested collection sizes bounded.
- `$search`: service-defined full-text matching; support and semantics are provider-specific.
- `$compute` and `$apply`: useful 4.01/aggregation features only when advertised or documented.
- `$format`: prefer HTTP `Accept`; use this only where headers cannot express the requirement.

Never repeat the same system query option at one resource level. Nested options inside `$expand` are separated with semicolons, not ampersands.

## Filter operators and nulls

Comparison: `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `has`, `in` (support/version dependent).

Boolean/arithmetic: `and`, `or`, `not`, `add`, `sub`, `mul`, `div`, `mod`.

```text
$filter=Status eq 'Open' and Total ge 100
$filter=DeletedAt eq null
$filter=Category/Name eq 'Books'
$filter=Tags/any(t:t eq 'featured')
$filter=Lines/all(l:l/Quantity gt 0)
```

Do not translate `null` into an empty string or zero. Parenthesize mixed Boolean expressions so intent is obvious.

## Common functions

Frequently implemented v4 functions include:

```text
contains(Name,'bike')
startswith(Name,'A')
endswith(Name,'Ltd')
tolower(Code) eq 'abc'
length(Name) gt 10
year(CreatedAt) eq 2026
round(Price) eq 10
```

Function support and backend translation vary. Use metadata capabilities or a small probe. Do not assume locale-aware or case-insensitive string behavior.

## Literals and escaping

- Strings: single-quoted; escape `'` as `''` before URL encoding.
- Boolean/null: `true`, `false`, `null`.
- Integer/decimal: invariant decimal notation; match the declared EDM type and precision.
- Date: `2026-09-03` for `Edm.Date`.
- DateTimeOffset: ISO 8601 such as `2026-09-03T10:30:00Z`.
- TimeOfDay: e.g. `10:30:00`.
- GUID: canonical form such as `01234567-89ab-cdef-0123-456789abcdef` in OData v4.
- Enum: qualified enum literal, commonly `Namespace.Color'Red'`; confirm in metadata.

Parameter aliases can keep repeated/complex literals separate from expressions:

```text
Products?$filter=Price gt @min&@min=10
```

Construct the query as name/value pairs and percent-encode once. Do not encode the entire completed URL a second time. Never concatenate raw user text into `$filter`; first resolve allowed fields, operators, and typed literals.

## Natural-language translation checklist

For “latest 10 paid orders for customer X, with line product names”:

1. Resolve the order entity set and exact status/customer/date/key properties.
2. Express customer and paid-state predicates with typed literals.
3. Order descending by date and then by the unique key.
4. Set `$top=10`.
5. Select only order fields needed for the answer.
6. Expand lines/products with nested `$select`, if capability annotations permit it.
7. Verify whether “latest” means creation, payment, or update timestamp rather than guessing.
