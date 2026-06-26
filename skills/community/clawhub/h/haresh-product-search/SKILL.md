---
name: haresh-product-search
description: "Search e-commerce products via n8n webhook integration"
user-invocable: true
---

# Product Search Skill

## Purpose
Enables users to search for products in the e-commerce catalog using natural language queries.

## When to Use
- User asks to find products, search inventory, or browse catalog
- User mentions specific product types, categories, or brands
- User provides price constraints or filtering requirements

## Workflow
1. Parse user intent to extract search parameters:
   - Product category (e.g., "running shoes", "laptops")
   - Price constraints (e.g., "under $100", "between $50-$200")
   - Sort preferences (e.g., "cheapest first", "highest rated")

2. Transform parameters into JSON payload with category, price_min, price_max, sort_by

3. Use exec tool to POST to n8n webhook at http://localhost:5678/webhook/product-search

4. Parse n8n response and present results to user in friendly format

## Parameter Mapping
- Category synonyms: "gym shoes" becomes "fitness", "sneakers" becomes "footwear"
- Price parsing: "under X" sets price_max to X
- Sort options: "cheapest" sorts price ascending, "best" sorts by rating

## Error Handling
- If no results: Suggest broader search terms
- If webhook fails: Inform user search service is unavailable
- If timeout: Ask if user wants to wait or retry
