---
name: haresh-cart-management
description: "Manage shopping cart operations via n8n webhook integration"
user-invocable: true
---

# Cart Management Skill

## Purpose
Handles all shopping cart operations including adding items, removing items, and updating quantities.

## When to Use
- User wants to add a product to their cart
- User wants to remove an item from cart
- User wants to change item quantity

## Supported Actions

### Add to Cart
1. Extract product_id from user message
2. Validate product_id format
3. Check quantity (default to 1)
4. Call n8n webhook at http://localhost:5678/webhook/cart-add
5. Confirm success to user

### Remove from Cart
1. Extract product_id to remove
2. Check current quantity
3. If quantity greater than 1, ask user for confirmation
4. Call n8n webhook at http://localhost:5678/webhook/cart-remove
5. ALWAYS confirm with user before removing

### Update Quantity
1. Extract product_id and new quantity
2. Validate quantity is positive integer
3. Call n8n webhook at http://localhost:5678/webhook/cart-update
4. Confirm update to user

## Safety Rules
- NEVER allow negative quantities
- ALWAYS confirm before removing items
- Validate product_id exists before operations
