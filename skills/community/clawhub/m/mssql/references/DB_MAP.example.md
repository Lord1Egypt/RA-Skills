# DB MAP - YOUR_DATABASE_NAME

## Architecture
- Source database: `YOUR_SOURCE_DB` (description of role)
- Working database: `YOUR_WORKING_DB`
- `schema_a.*` = description of schema A
- `schema_b.*` = description of schema B
- `dbo.*` = final business-ready tables for reporting and analysis

## Tables to use
- `dbo.customers`
- `dbo.orders`
- `dbo.products`
- `dbo.invoices`
- `dbo.payments`
- `dbo.stock`

## Usage rules
- For routine business queries, use the final tables listed above first.
- Use other schemas only when debugging or when the final tables do not cover the need.
- Permissions are controlled at the database user level.
