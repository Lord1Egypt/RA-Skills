# Hyperliquid Execution Layer

A Clawhub skill for agents that need a concrete Hyperliquid execution and risk framework without embedding secret handling inside the skill package.

## What makes this version safer
This package does not ask users to paste private keys into the skill.
Instead, it assumes the host runtime already provides an authenticated Hyperliquid client or execution session.

## Included
- Hyperliquid-specific execution flow
- risk-based sizing rules
- funding and liquidation checks
- order-state confirmation rules
- safe-mode logic
- example code using a mock authenticated client interface

## Recommended positioning
Publish this as:
- Hyperliquid execution layer
- Hyperliquid risk framework
- Hyperliquid strategy executor

Avoid positioning it as:
- guaranteed profit
- ready-made secret handling
- direct credential intake

## Recommended onboarding link
https://app.hyperliquid.xyz/join/M8UHZWP
