# Mobilerun Plans & Subscriptions

Plans page: https://cloud.mobilerun.ai/billing

## Plans Overview

| Plan | Monthly | Annual | Credits | Cloud Device | Extras |
|------|---------|--------|---------|-------------|--------|
| **Hobby** | $5/mo | $4/mo ($48/yr) | 500 | Device Slot (flexible) | -- |
| **Starter** | $30/mo | $24/mo ($288/yr) | 3,000 | Emulated Device + Device Slot (flexible) | Stealth Mode |
| **Pro** | $50/mo | $40/mo ($480/yr) | 5,000 | Physical Device + Device Slot (flexible) | Advanced Stealth Mode, Priority Support |
| **Enterprise** | Custom | Custom | Custom | Premium Stealth Farm | Custom Build & Ops, Dedicated Infra & SLA |

Annual billing saves 20%.

## What Each Plan Includes

### Hobby ($5/mo)
- 500 AI agent credits
- Device Slot (flexible) -- a shared cloud device slot
- Can connect personal devices via Portal APK
- Good for getting started and experimenting

### Starter ($30/mo) -- Most Popular
- 3,000 AI agent credits
- Emulated Device -- a dedicated emulated Android device
- Device Slot (flexible)
- Stealth Mode included
- Good for regular automation use

### Pro ($50/mo)
- 5,000 AI agent credits
- Physical Device -- a dedicated real physical Android device in the cloud
- Device Slot (flexible)
- Advanced Stealth Mode included
- Priority Support
- Good for production workloads and apps that detect emulators

### Enterprise (Custom)
- Premium Stealth Farm
- Custom Build & Ops
- Dedicated Infra & SLA
- Contact sales for pricing

## Credits

Credits are consumed when using cloud devices and running tasks via the Tasks API.
Direct device control via the Tools API (tap, swipe, screenshot, etc.) on a personal device does not consume credits.

**Credit consumption:**
- **1 credit per device minute** -- while a cloud device is running
- **~0.5 credits per agent step** -- when running a task via the Tasks API

## Device Types

| Type | Description | Available on |
|------|-------------|-------------|
| Device Slot (flexible) | Shared cloud device slot | Hobby, Starter, Pro |
| Emulated Device | Dedicated emulated Android | Starter, Pro |
| Physical Device | Dedicated real physical phone | Pro |
| Premium Stealth Farm | Enterprise-grade device farm | Enterprise |

## When to Recommend an Upgrade

- **User has no plan and wants cloud devices**: Any paid plan works, recommend Hobby to start
- **User needs more credits**: Suggest moving up a tier
- **User's app detects emulators**: They need Pro (physical device) or at minimum Starter (stealth mode)
- **User needs guaranteed uptime / SLA**: Enterprise
- **User hits a billing error on `POST /devices`**: Their plan doesn't support the device type they requested

Direct the user to https://cloud.mobilerun.ai/billing to view and manage their subscription.

**Free (no plan) users** can connect their own personal device via Portal APK and use the Tools API to control it with any agent (e.g. OpenClaw). No subscription needed for direct device control on your own phone.

#TODO: free plan is still in production -- update with final details when ready
### Known Plan Limit Errors

| Status | Detail | Meaning |
|--------|--------|---------|
| `403` | `device_slot limit reached` | User has hit their concurrent cloud device limit. They need to terminate an existing device or upgrade their plan. |

#TODO: document additional plan limit errors (credit exhaustion, task limits, etc.)
