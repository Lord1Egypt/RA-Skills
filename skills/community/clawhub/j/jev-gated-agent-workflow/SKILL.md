---
name: jev-gated-agent-workflow
description: "Design and implement a JEV decision gate before expensive or privacy-sensitive agent tools, using natural-language intent, fixed allowlists, default-deny permits, and token-efficient retrieval. Use when an agent must route requests through TypeSafe JEV or another constrained classifier before reading data or invoking costly tools."
---

# JEV Gated Agent Workflow

Use JEV as a small, explicit decision gate before an expensive, privacy-sensitive, or irreversible tool call. The gate decides whether a request belongs to one of a small set of predeclared branches; it does not execute the action, invent identifiers, grant broad permissions, or replace the agent's final validation.

## Core principles

1. Keep the user interface natural-language-only. Users describe intent; internal IDs, account IDs, and group IDs stay in local configuration and are never requested from the user or published.
2. Keep routing closed-world. Define the candidate branches and their internal targets in a local allowlist. Accept only a JEV choice that maps to that allowlist.
3. Default to deny. Deny on missing intent, missing credentials, timeout, malformed output, low confidence, an out-of-policy choice, a target mismatch, or an expired permit.
4. Separate decision from execution. JEV returns a constrained route; the host validates it and then calls the minimum necessary tool.
5. Scope permits narrowly. Bind a permit to the natural-language request, session, tool, target, and short TTL. Do not reuse a permit for unrelated requests or tools.
6. Optimize token use deliberately. Route before loading history, searching documents, opening browser pages, or assembling large context. Retrieve only the smallest evidence set needed to answer, then summarize and discard the raw material when policy allows.
7. Never publish secrets or private routing data. The skill may document how to obtain and configure a user's own key, but must not contain keys, cookies, real group IDs, private paths, or local policy files.

## Standard workflow

1. Identify the high-cost or sensitive action and the small set of allowed branches.
2. Capture the current natural-language request and bind it to the session without asking the user for an internal identifier.
3. Call the local router; the router calls TypeSafe JEV with only the request and branch descriptions.
4. Validate the response locally: choice is allowlisted, confidence meets the configured threshold, returned target matches the allowlist, and no confirmation flag is set.
5. Mint a one-time permit scoped to the exact tool and target. If any check fails, explain the denial and stop before the protected tool.
6. Invoke the minimum tool call. Inject the internal target from the allowlist; do not pass through a user-supplied target.
7. Return a concise result, record only redacted diagnostics, and expire the permit.

Read [references/implementation-checklist.md](references/implementation-checklist.md) when implementing the hook or reviewing an integration. Read [references/router-contract.md](references/router-contract.md) when defining the router response or writing tests.

## Credential setup

The runtime host must expose `JEV_API_KEY` before it starts the agent gateway. Store the key in the host's local secret store or process/user environment, never in this skill directory. After changing the environment, restart the gateway so the child process inherits it. A missing key must produce a safe denial, not a fallback to unconstrained model routing.

## What success means

An integration is complete only when a valid natural-language request is routed to the correct allowlisted branch, a missing/invalid/low-confidence request is blocked before the protected tool, internal IDs never need to be supplied by the user, and token usage is reduced by avoiding irrelevant retrieval. Test the gate with a fake tool adapter first; do not send real messages or read production history merely to prove the hook.
