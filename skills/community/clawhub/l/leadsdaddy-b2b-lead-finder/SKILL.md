---
name: leadsdaddy-b2b-lead-finder
description: Find global B2B prospects with LeadsDaddy via MCP. Use this skill when the user wants to find importers, distributors, wholesalers, restaurant supply buyers, packaging buyers, regional channel partners, or other commercial prospects in any country or city. Best for export sales, supplier prospecting, market entry, and lead generation workflows that need product profiling, task creation, lead review, and selective lead unlocking.
metadata:
  {
    "openclaw":
      {
        "emoji": "🌍",
        "homepage": "https://www.leads-daddy.com",
        "primaryEnv": "LEADSDADDY_TOKEN",
        "requires":
          {
            "bins": ["leadsdaddy-mcp"],
            "env": ["LEADSDADDY_TOKEN", "LEADSDADDY_API_URL", "LEADSDADDY_WEB_URL"],
          },
        "install":
          [
            {
              "id": "node-leadsdaddy-mcp",
              "kind": "node",
              "package": "@leadsdaddy/mcp",
              "bins": ["leadsdaddy-mcp"],
              "label": "Install LeadsDaddy MCP (npm)",
            },
          ],
      },
  }
---

# LeadsDaddy B2B Lead Finder

## Overview

Use this skill to find **global potential customers** with LeadsDaddy through MCP.
It is designed for export sales, B2B lead generation, distributor discovery, importer discovery, and market expansion workflows.

This skill is appropriate when the user wants to:
- find buyers in a specific country, city, or region
- find distributors, wholesalers, importers, resellers, or channel partners
- discover likely commercial buyers for a product category
- generate leads for packaging, restaurant supply, foodservice, industrial, or other B2B verticals
- review task output and decide which leads are worth unlocking

This skill is **global by design**. It is not limited to one country or one market.
It can be used for North America, Europe, the Middle East, Southeast Asia, Latin America, Africa, and other markets wherever LeadsDaddy has useful coverage.

## Preconditions

Before using this skill, make sure LeadsDaddy MCP is installed and configured:

```bash
npm install -g @leadsdaddy/mcp
```

Typical MCP configuration:

```json
{
  "mcpServers": {
    "leadsdaddy": {
      "command": "leadsdaddy-mcp",
      "env": {
        "LEADSDADDY_TOKEN": "ldat_...",
        "LEADSDADDY_API_URL": "https://edge.leads-daddy.com",
        "LEADSDADDY_WEB_URL": "https://www.leads-daddy.com"
      }
    }
  }
}
```

If MCP is not configured, stop and ask the user for setup or credentials.

## Workflow

### 1. Clarify the targeting goal
Identify these inputs before creating anything:
- product or product family
- target geography (country, city, metro, region, or global region)
- desired buyer type
- exclusions if any

Good buyer types include:
- importer
- distributor
- wholesaler
- retailer with wholesale intent
- restaurant supply company
- packaging supplier
- food service supplier
- hospitality supplier
- regional channel partner

If the user gives only a product, ask one concise follow-up question for geography and buyer type.

### 2. Create or select the product in LeadsDaddy
Use MCP to:
- list existing products
- create a product if needed
- avoid duplicate product entries when a suitable one already exists

### 3. Write a strong product profile
Use `product_profile_upsert` with a profile that includes:
- the product name
- plain-English description
- target buyer types
- use cases
- disqualifiers
- country/region focus

A good profile should help LeadsDaddy understand the commercial context, not just the product label.

### 4. Generate globally relevant buyer-intent targeting
When choosing search direction, optimize for **commercial entities**, not consumer shopping intent.

Preferred targeting patterns:
- exact product + distributor + location
- exact product + wholesaler + location
- broader category + supplier + location
- foodservice / packaging / hospitality / industrial category variants

Examples:
- paper cup distributor Toronto
- disposable food packaging supplier New York
- restaurant supply wholesaler Vancouver
- bakery packaging distributor Dubai
- private label skincare importer Germany

### 5. Create the lead-discovery task
Use `task_create` and make the task clearly reflect:
- geography
- buyer type
- product context
- commercial targeting intent

After creation, keep the task id and monitor status.

### 6. Review task output before unlocking
Use task output and lead listing tools to evaluate quality first.
Do **not** blindly unlock leads.

Check for:
- whether the result is a commercial business rather than a consumer listing
- whether the company appears to operate in the target vertical
- whether it is a likely buyer, distributor, importer, or reseller
- whether the lead is too generic or unrelated

### 7. Classify leads into three groups
When reporting results, separate them into:
- **High-fit**: strong target, worth unlocking now
- **Possible-fit**: related commercial player, but needs review
- **Low-fit / Noise**: wrong vertical, wrong buyer type, too generic, or clearly off-target

### 8. Unlock selectively
Use `lead_unlock` only for high-fit or clearly promising leads.
If the user wants a budget-aware workflow, unlock a small batch first, review quality, then continue.

## Recommended Output Style

When presenting results, keep the report short and decision-oriented.

Suggested format:

### Targeting Summary
- product
- geography
- buyer type

### Best Leads to Review
- company name
- why it looks relevant
- whether to unlock now

### Caution / Noise Notes
- patterns of false positives
- examples of over-broad categories
- keyword or targeting adjustments for the next run

## Quality Rules

Use these rules to improve results:

### Prefer
- distributors
- importers
- wholesalers
- packaging suppliers
- food service suppliers
- restaurant supply companies
- hospitality suppliers
- commercial operators with recurring purchasing needs

### Treat with caution
- companies with very broad "equipment" positioning
- event rental businesses
- heavy machinery vendors
- general directories
- consumer-only retail shops
- companies with no sign of B2B purchasing relevance

### Do not over-reject
Some companies with words like `equipment`, `supply`, or `restaurant supply` may still be valid buyers or channel partners if they also sell smallwares, tableware, disposables, packaging, or other repeat-purchase items.

## Example User Requests

- Find paper cup and paper plate distributors in Canada.
- Find food packaging importers in Germany.
- Find restaurant supply wholesalers in New York that may buy disposable containers.
- Find potential channel partners for custom printed cups in Australia.
- Find global B2B buyers for biodegradable takeaway packaging.
- Find wholesale buyers for hotel disposable amenities in the UAE.

## MCP Tool Mapping

This skill is built around LeadsDaddy MCP tools such as:
- `leadsdaddy_products_list`
- `leadsdaddy_product_create`
- `leadsdaddy_product_profile_upsert`
- `leadsdaddy_tasks_list`
- `leadsdaddy_task_create`
- `leadsdaddy_task_get`
- `leadsdaddy_task_output`
- `leadsdaddy_leads_list`
- `leadsdaddy_lead_get`
- `leadsdaddy_lead_unlock`

## Boundaries

- Do not promise perfect lead accuracy; review is still required.
- Do not frame every result as a confirmed buyer.
- Distinguish likely buyer/channel partner from low-fit noise.
- Use unlock budget carefully.
- Prefer business contact workflows and public business profiles; do not present private personal data scraping as the core value proposition.

## Positioning for Distribution

This skill should be presented as:

> A global B2B prospecting skill powered by LeadsDaddy MCP that helps agents find potential customers, distributors, importers, wholesalers, and channel partners across worldwide markets.

That positioning is important: the skill is **not only for one niche or one country**. It supports global commercial lead discovery.
