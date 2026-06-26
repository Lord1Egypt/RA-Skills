---
name: haresh-checkout-flow
description: "Process e-commerce checkout via n8n webhook integration"
user-invocable: true
---

# Checkout Flow Skill

## Purpose
Manages the complete checkout process including validation, authentication, shipping, and payment.

## When to Use
- User wants to checkout or place an order
- User asks to proceed to payment
- User wants to complete their purchase

## Workflow

### Step 1: Validate Cart
Call n8n webhook at http://localhost:5678/webhook/checkout-validate to check cart items availability and inventory status

### Step 2: Check Authentication
Determine if user is authenticated from context. If guest, present login options or continue as guest.

### Step 3: Collect Shipping Information
Show saved addresses for authenticated users or collect details for guests.

### Step 4: Payment Processing
Present payment options and call n8n webhook at http://localhost:5678/webhook/checkout-process

### Step 5: Order Confirmation
Display order summary and get final confirmation from user.

## Security Requirements
- Verify authentication status from JWT claims
- Never store or log full payment details
- Validate all inputs before sending to backend

## Error Handling
- If cart validation fails, show specific errors
- If payment fails, allow retry with different method
- If inventory changes, notify user
