---
name: greenhelix-bundle-x402-commerce-kit
version: "1.3.1"
description: "Launch a crypto-native storefront from scratch. Includes the x402 Merchant Starter Kit (deployable code), agent payment rails playbook, and commerce security hardening guide. Deploy in 15 minutes. 2 guides + production code."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: bundle
includes: [x402-merchant-starter-kit, agent-payment-rails-playbook, agent-commerce-security]
price_usd: 99.0
tags: [bundle, code, x402, payments, security, starter-kit, guide, greenhelix, openclaw, ai-agent]
executable: false
install: none
credentials: [GITHUB_TOKEN, WALLET_ADDRESS, DASHBOARD_SECRET, GREENHELIX_API_KEY, AGENT_SIGNING_KEY, STRIPE_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - GITHUB_TOKEN
        - WALLET_ADDRESS
        - DASHBOARD_SECRET
        - GREENHELIX_API_KEY
        - AGENT_SIGNING_KEY
        - STRIPE_API_KEY
    primaryEnv: GITHUB_TOKEN
---
# x402 Commerce Kit: Merchant Starter Kit + Payment Rails Guide + Security Hardening

## Included Guides
| Guide | Individual Price |
|-------|-----------------|
| x402 Merchant Starter Kit: Deploy Your Own Crypto-Native Storefront | $99.00 |
| The Agent Payment Rails Playbook | $29.00 |
| Locking Down Agent Commerce: The OWASP-Aligned Security Guide for Autonomous AI Agents on GreenHelix | $29.00 |

## Total Value: $157.00 | Bundle Price: $99.00
