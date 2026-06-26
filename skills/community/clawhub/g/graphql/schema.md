# Schema Design Traps

## Nullability Traps

- Non-null field error bubbles up to parent—entire parent becomes null
- `[User!]!` vs `[User]!` vs `[User!]`—each fails differently
- Changing nullable to non-null is breaking—existing queries may fail
- Default nullable is safer—non-null when truly guaranteed

## List Traps

- Empty list `[]` is valid for `[Type!]!`—only `null` for list fails
- Nested lists `[[Int]]` need explicit handling—clients may not expect
- Unbounded lists kill performance—always paginate
- List of nullable `[User]` can have null holes—client must handle

## Input Type Traps

- Input types can't have fields returning types—only scalars and other inputs
- Same field name in input and output types—different objects, different validation
- Required input field can't be added later—breaks existing clients
- Nested input types make validation complex—flatten when possible

## Connection/Pagination Traps

- `first` + `after` OR `last` + `before`—not all four together
- Cursor is opaque string—don't parse or generate client-side
- `totalCount` requires extra query—consider making nullable/optional
- `edges` vs direct `nodes`—Relay expects `edges[].node`

## Union/Interface Traps

- Can't query fields without fragment—`... on Type { field }`
- `__typename` needed for client caching—always include
- Adding type to union is semi-breaking—clients with exhaustive switches fail
- Interface field added = all implementers must add—coordinated change

## Deprecation Traps

- `@deprecated` doesn't hide field—still works, just warns
- Removing deprecated field is breaking—wait for clients to migrate
- No built-in usage tracking—need logging to know when safe to remove
