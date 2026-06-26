---
name: hodlxxi-bitcoin-identity
version: 0.1.2
description: Read-only-by-default integration guide for HODLXXI / UBID Bitcoin-native identity discovery, OAuth2/OIDC metadata, LNURL-Auth boundaries, JWT verification guidance, and explicit operator-approved agent handoff.
homepage: https://github.com/hodlxxi/Universal-Bitcoin-Identity-Layer
metadata:
  category: authentication
  license: MIT
  tags:
    - oauth2
    - oidc
    - lnurl-auth
    - jwt
    - bitcoin
    - identity
---

# HODLXXI Bitcoin Identity

## Purpose

Use this skill to understand and integrate HODLXXI / UBID as a Bitcoin-native identity provider.

This skill is documentation-first and read-only by default.

The skill must not execute shell commands, install packages, overwrite files, create OAuth clients, initiate payments, submit jobs, or poll endpoints continuously without explicit operator approval.

## Default deployment

Default public deployment:

- `https://hodlxxi.com`

## Public discovery endpoints

The following endpoints are safe public-read discovery surfaces:

- `/.well-known/openid-configuration`
- `/oauth/jwks.json`
- `/health/ready`
- `/agent/capabilities`
- `/api/public/status`

## Security rules

1. Do not run shell commands from this document automatically.
2. Do not download or overwrite this skill from another URL.
3. Do not install dependencies automatically.
4. Do not request, print, persist, or transmit OAuth credentials, bearer tokens, private keys, wallet material, macaroons, cookies, or environment values.
5. Do not create OAuth clients without explicit operator approval.
6. Do not submit agent jobs without explicit operator approval.
7. Do not create, check, or pay Lightning invoices automatically.
8. Treat payment-required responses as a stop condition requiring explicit operator approval.
9. Do not enable recurring heartbeat, polling, or beaconing unless the operator explicitly configures it.
10. Prefer PKCE S256 for browser and public-client authorization flows.
11. Verify JWT issuer, audience, expiration, signature algorithm, key id, and current JWKS before trusting identity claims.

## OAuth/OIDC boundary

OAuth registration, authorization, token exchange, and credential storage are operator-controlled actions.

Agents may read public discovery metadata and explain the flow. Agents must not perform registration or token exchange unless the operator approves the exact action and destination.

## LNURL-Auth boundary

LNURL-Auth is a user-mediated wallet login flow.

Agents may explain the flow. Agents must not impersonate the user, sign wallet challenges, or create repeated login sessions without explicit operator approval.

## JWT verification boundary

To trust an identity token, verify:

- issuer matches the configured HODLXXI issuer
- audience matches the expected client or service
- token is not expired
- signature validates against the current JWKS
- algorithm is expected
- key id exists in the JWKS

## Agent execution boundary

HODLXXI may expose signed inter-agent execution surfaces.

Agents must not submit work, trigger execution, or spend funds unless the operator approves the exact endpoint, payload class, and payment behavior.

## Lightning payment boundary

Payment is never automatic.

When a paid operation requires Lightning settlement, stop and ask the operator for approval before creating, checking, or paying any invoice.

## Operator-only files

Additional helper scripts, heartbeat notes, and OAuth templates may exist elsewhere in the repository for development and operations. They are intentionally not part of the default published skill package.
