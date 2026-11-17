---
name: imagekind
description: "Find artist-credited art prints and canvas, made to order by Image Kind’s studio. Use it for art prints through Image Kind's MCP server."
---

# Image Kind

Find artist-credited art prints and canvas, made to order by Image Kind’s studio.

## Connect

Add Image Kind's MCP server: https://imagekind.auto-units.com/mcp (Streamable HTTP, no sign-in).

## Offers

### art prints

Search Image Kind’s starting collection by artwork title, artist or subject. Returns real artwork pages, artist credits, sizes and finishes. All listed works are available to print to order. Prices and shipping require studio confirmation. This reads the catalog; it does not place an order or take payment.

1. Call `find_prints`. It returns an id.
2. Call `get_prints` with the id. The catalog entry is available immediately.
3. Give the person the result and its link.

## On the website

- The art collection: Browse the starting collection and request a print from the studio. The person decides and buys it at https://imagekind.auto-units.com/prints.
- Print guide: Choose a print size and compare paper and canvas. The person decides and buys it at https://imagekind.auto-units.com/journal/choosing-your-print.
