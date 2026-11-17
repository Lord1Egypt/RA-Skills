# Model discovery, addressing, and queries

## Discover the contract

GET the service root for the service document and `{service-root}/$metadata` for CSDL. Map:

- `EntityContainer` → entity sets, singletons, function/action imports.
- `EntityType`/`ComplexType` → exact properties, EDM types, nullability, inheritance, open types.
- `Key` → key property names, order, and literal types.
- `NavigationProperty` and `NavigationPropertyBinding` → relationship cardinality and target sets.
- `ContainsTarget=true` → contained resources have no independent top-level set and are addressed through the parent.
- operation definitions → binding parameter, overloads, parameters, return types, and composability.
- `Org.OData.Capabilities.V1.*` annotations → supported reads/writes/query options, required properties, restrictions, and permissions.

Absence of a capability annotation does not prove support. Probe optional features with the smallest safe request. Names may be case-sensitive.

## Address resources

```text
Products
Products(42)
People('O''Neil')
OrderLines(OrderId=10,LineNo=2)
Customers('ALFKI')/Orders
Accounts(1)/Namespace.PremiumAccount
Orders(1)/Lines(2)
```

Use CSDL types for key literals. In v4, do not use legacy v2/v3 literal prefixes such as `guid'...'` or `datetime'...'`. Prefer canonical/edit URLs returned by the service when available.

## Query

Use lower-case dollar-prefixed options:

```text
Products?$select=Id,Name&$filter=Price gt 10&$orderby=Name,Id&$top=20
Customers?$expand=Orders($select=Id,Total;$filter=Total gt 100;$top=5)
Products?$count=true&$top=0
```

Core options include `$select`, `$filter`, `$orderby`, `$top`, `$skip`, `$count`, `$expand`, `$search`, and `$format`; v4.01 or extensions may add `$compute`, `$index`, `$apply`, and `$schemaversion`. Use only advertised/supported options. Nested expand options use semicolons.

Escape a string literal by doubling `'`, then percent-encode the query exactly once. Validate user-supplied fields, operators, and typed values instead of concatenating raw text into `$filter`. Use parameter aliases for reusable literals or function parameters when appropriate.

For full retrieval, follow top-level `@odata.nextLink` exactly, resolve relative links against the response URL, reject origin changes with credentials, detect loops, and enforce page/item/time limits. Do not append the original query or construct `$skiptoken`. Expanded collections can have separate nested next links.

When order matters, add a unique key as a final `$orderby` tie-breaker if supported. Do not perform client-side filtering or aggregation on a partial page and present it as complete.
