---
name: inventory-waste-optimizer
version: 1.0.1
description: "Autonomous inventory management and waste reduction agent for QSRs. Cross-references sales data with inventory levels to forecast ordering and flag excessive waste. Hardened with ThumbGate to prevent over-ordering."
author: "Igor Ganapolsky (ex-Subway Mobile App Team Lead)"
tags: ["inventory", "waste-reduction", "qsr", "analytics", "thumbgate"]
price: 197
---

# Autonomous Inventory & Waste Optimizer with ThumbGate Safety

## What This Agent Does
- Monitors sales logs and inventory levels in Google Sheets.
- Detects patterns of excessive waste (e.g., high prep-to-sale variance).
- Generates weekly restock recommendations.
- Flags "at-risk" inventory about to expire.
- Uses ThumbGate to ensure no single order exceeds historical norms by >50%.

## Critical ThumbGate Rules
- **Sanity Check:** Block any restock recommendation that is >50% higher than the 4-week average without manual override.
- **Zero-Sum Validation:** Ensure Prep + Beginning Inventory - End Inventory = Sales. If variance > 5%, trigger an alert.
- **Price Guard:** Block any supply order where unit price has jumped >20% since last week.

## Setup
1. Link your 'Sales' and 'Inventory' sheets.
2. Load skill: `openclaw skill load inventory-waste-optimizer`
