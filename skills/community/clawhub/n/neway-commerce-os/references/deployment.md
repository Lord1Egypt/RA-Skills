# Deployment

## Target

Primary deployment target: EdgeOne Pages

## Build assumptions

Frontend:
- Vite build output in `dist/`

Functions:
- edge-style handlers in `functions/api/`
- node-style handlers in `functions/node/`

## Environment variables

Typical variables:
- VITE_SITE_NAME
- VITE_DEFAULT_CURRENCY
- VITE_PAYMENT_MODE
- STRIPE_SECRET_KEY
- STRIPE_WEBHOOK_SECRET
- AI_API_BASE
- AI_API_KEY
- AI_MODEL

## Local workflow

1. install dependencies
2. run dev server
3. validate environment variables
4. test catalog page
5. test cart interactions
6. test mock checkout
7. optionally test assistant endpoint with mock response

## Production workflow

1. set environment variables in EdgeOne Pages
2. switch payment mode to `stripe`
3. configure webhook endpoint
4. deploy frontend and function handlers
5. verify hosted checkout redirect
6. verify webhook receipt
7. verify account/order state

## Minimum deployment checklist

- homepage renders
- products load
- cart updates
- checkout endpoint responds
- assistant endpoint responds
- webhook endpoint exists
- admin page is reachable
- environment placeholders are documented

## Notes

This skill should always generate deployment notes that distinguish:
- scaffold-ready
- demo-ready
- production-ready
