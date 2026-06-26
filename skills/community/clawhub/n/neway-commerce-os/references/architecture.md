# Architecture

## Purpose

Neway Commerce OS is a reusable commerce operating system for digital products, creator storefronts, and multi-product studios. It is optimized for short-prompt generation and fast deployment, not for deep backend implementation by default.

## System Layers

### 1. Presentation layer
- React + Vite + TypeScript
- Modern landing page composition
- Lightweight motion and hover interactions
- Product grid, cart drawer/page, checkout view, account view, admin view
- AI sales assistant entry point

### 2. Application layer
- Client-side routing
- Shared state for cart, catalog, and assistant visibility
- Fetch wrappers for API access
- Mock-first data flow with upgrade path to live APIs

### 3. API layer
- Hono-style edge API handlers
- Product catalog endpoint
- Checkout endpoint
- AI assistant endpoint
- Stripe webhook endpoint in node runtime

### 4. Commerce layer
- Product records
- Cart state
- Checkout session creation
- Payment provider switching between mock and stripe
- Order lifecycle hooks

### 5. Deployment layer
- EdgeOne Pages static hosting
- Edge Functions for lightweight APIs
- Node Functions for webhook-style handlers
- Environment-variable-driven configuration

## Recommended Project Shape

```text
src/
  components/
  pages/
  lib/
  store/
functions/
  api/
  node/
```

## Defaults

- Default business mode: multi-product NewayStudio matrix
- Default assistant mode: AI sales concierge
- Default payment mode: mock in dev, stripe in production
- Default visual language: dark-neutral premium cards, soft gradients, light motion

## Implementation Philosophy

This skill should generate:
- a complete directory structure
- working page scaffolds
- named backend entrypoints
- environment placeholders
- deployment files
- obvious extension points for production implementation

It should not pretend to include deep production logic when only placeholders exist. Generated handoff notes should be explicit about what is scaffolded and what still needs implementation.
