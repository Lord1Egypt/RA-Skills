# Chargebee

Chargebee MCP Pack — wraps the Chargebee API v2

## chargebee_list_subscriptions

List all subscriptions with optional filtering by status (e.g., 'active', 'cancelled'). Returns subs

## chargebee_get_subscription

Get full subscription details by ID. Returns plan, status, billing dates, customer info, and all cha

## chargebee_list_customers

List all customers with pagination. Returns customer IDs, names, emails, billing addresses, and crea

## chargebee_get_customer

Get complete customer profile by ID. Returns name, email, address, payment methods, subscription cou

## chargebee_list_invoices

List invoices filtered by status (e.g., 'paid', 'pending') and/or customer ID. Returns invoice numbe

```json
{
  "mcpServers": {
    "chargebee": {
      "url": "https://gateway.pipeworx.io/chargebee/mcp"
    }
  }
}
```
