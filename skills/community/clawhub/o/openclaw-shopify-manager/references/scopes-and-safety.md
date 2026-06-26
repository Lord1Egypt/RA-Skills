# Shopify scopes and safety

## Principle

Request the smallest set of scopes that can do the job.

## Common scopes

### Read-heavy setup

- `read_products`
- `read_content`
- `read_orders`
- `read_customers`

### Product editing

Add:

- `write_products`

### Blog/content editing

Add:

- `write_content`

### Inventory workflows

Add only if needed:

- `read_inventory`
- `write_inventory`

## Suggested operating modes

### `read-only`

- no mutations
- best default for initial verification

### `require-confirmation-for-mutations`

- allow reads freely
- ask before any write
- recommended default for most real stores

### `allow-approved-operations`

- permit only a specific allowlist of mutation classes
- still keep scopes narrow

## Mutation policy

Before using a mutation command:

1. confirm exactly what will change
2. ensure the config mode permits it
3. ensure the mutation is in `allowedMutations` when that control is used
4. prefer preview or dry-run semantics where possible

## Avoid these anti-patterns

- granting broad scopes “just in case”
- editing live store data without confirmation
- storing API secrets in committed config files
- exposing the connector directly on a public bind when local bind + proxy works
