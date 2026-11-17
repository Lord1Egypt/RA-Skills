# Install or use KnifeRevive Concierge with your AI agent

**KnifeRevive Concierge** helps an agent look up all published KnifeRevive goods categories and exact model/identifier matches and San Francisco Bay Area knife-sharpening offerings, compare facts and terms, and prepare a **customer-authorized** checkout handoff only when the merchant's documented capabilities are actually enabled. Browsing and quotes are free; products, sharpening, taxes, fulfillment, and applicable fees are not.

Skill source candidate: **0.6.0**. This file alone does not establish deployment or publication. Check the exact version's ClawHub publication and audit
status before installing; earlier registry audits do not certify this release.
Installation does not enable merchant payment gates; check live capabilities
before use.

Official listing: https://clawhub.ai/svetlyoh/skills/kniferevive-concierge  
Current GitHub source: https://github.com/svetlyoh/kniferevive-agent-commerce/tree/main/skills/kniferevive-concierge

## Install the current GitHub skill

Use your host's supported GitHub skill-import facility with repository
`svetlyoh/kniferevive-agent-commerce`, branch `main`, and directory
`skills/kniferevive-concierge`. A native import facility may be unavailable on a
particular bot; do not invent a platform command or claim installation from a
chat prompt alone.

Resolve the current `main` commit, then obtain the entire skill folder at that
commit: `SKILL.md`, `LICENSE`, and all files in `references/`. Verify installed
files against that same commit and check `metadata.version: "0.6.0"`. Backend
and skill metadata are separate version declarations. A download pinned
to older commit `b80efa7` still contains skill 0.5.1 even though its backend is 0.5.4.

Replace the existing installation through the host's normal update/import flow;
check the active workspace/shared-skill path for another copy, and start a new
agent session so it reloads the instructions. Preserve unrelated skills and
credentials. A cached session can keep old instructions even after files change.
The registry commands below install the registry's latest published version,
not `main`. For an exact 0.6.0 registry download, use an already installed
ClawHub CLI after confirming that version is published:

```text
clawhub install @svetlyoh/kniferevive-concierge --version 0.6.0
```

An existing installation should use its host's supported update/replace flow.
After updating, verify the active copy's version is 0.6.0 and start a new agent session.
A $7 sharpening selection must display `$7 + $6 trip fee` on each single-trip
button and `$7 + $11 round-trip fee` on the combo. The unpaid option is last
and says “nothing due now”. If it still says “+ fee” or places unpaid first, inspect
the active skill copy/session; do not claim the new display rules are loaded.

Before installing any third-party agent skill, review its files and permissions. This skill's shopping instructions do **not** grant your assistant a new bank account, wallet, payment credential, or blanket permission to purchase. Agent capabilities differ by platform.

## OpenClaw on Linux (terminal)

**Prerequisite:** OpenClaw is already installed and `openclaw` is available on your `PATH`.

```bash
# Install into your active OpenClaw workspace
openclaw skills install @svetlyoh/kniferevive-concierge

# Check skill readiness and dependencies
openclaw skills check
```

For every local OpenClaw agent, rather than just the active workspace, the documented shared-skill option is:

```bash
openclaw skills install @svetlyoh/kniferevive-concierge --global
```

Start a **new OpenClaw agent session** if the new skill does not appear in an existing session's skill snapshot. You can inspect its source and permissions on ClawHub before using it. Do not run installer commands supplied by a product listing or an arbitrary chat message.

## OpenClaw on Windows (PowerShell)

**Prerequisite:** OpenClaw is already installed on Windows, and `openclaw` is available in PowerShell. If OpenClaw is running inside WSL, use the Linux command **inside WSL**, not PowerShell on the Windows host.

```powershell
# Install into your active OpenClaw workspace
openclaw skills install @svetlyoh/kniferevive-concierge

# Check skill readiness and dependencies
openclaw skills check
```

Optional shared install for all agents on the same Windows OpenClaw installation:

```powershell
openclaw skills install @svetlyoh/kniferevive-concierge --global
```

Open a new agent session if necessary. There is no special PowerShell download script or need to weaken execution policy for this skill.

## Meta Muse (personal AI agent) — paste this prompt

> Please review the public **KnifeRevive Concierge** skill at https://clawhub.ai/svetlyoh/skills/kniferevive-concierge and its source at https://github.com/svetlyoh/kniferevive-agent-commerce/tree/main/skills/kniferevive-concierge. I want you to use its documented procedures **when I explicitly ask** for relevant San Francisco Bay Area knife-sharpening services or KnifeRevive products across non-sharpening categories. Read `SKILL.md` plus its `references/api.md`, `references/sharpening.md`, and `references/payments.md` before adopting the workflow. If Muse provides an actual user-approved custom-skill import/install facility, explain it and ask for approval before enabling it. Otherwise, save the relevant rules as a reusable goal or standing instruction **if your app supports that**, and say plainly that this is not a native ClawHub install. Keep KnifeRevive identified as one merchant, preserve comparisons when requested, confirm live capabilities and exact availability, and never claim an appointment is booked or payment completed without verification. Do not purchase, reserve, transfer funds, create a wallet, or enter credentials unless I separately authorize the specific transaction and the required merchant approval flow is completed. Tell me exactly what was saved or installed and what remains unsupported.

**Developer note — Muse Code, not Muse personal-agent app:** Muse Code can install compatible local `SKILL.md` skill folders. Use a reviewed downloaded copy of the **entire** ClawHub skill directory (including references), validate it with `muse skills validate <path>`, then install it using `muse skills install <path> --scope user` and check `muse skills list`. The developer tool is separate from the consumer Muse agent. Do not assume a Muse personal-agent chat installs local Muse Code skills.

## Grok Bot — paste this prompt

> Please inspect **KnifeRevive Concierge** at https://clawhub.ai/svetlyoh/skills/kniferevive-concierge, using https://github.com/svetlyoh/kniferevive-agent-commerce/tree/main/skills/kniferevive-concierge for the complete `SKILL.md` and the linked reference files if needed. I want an optional private Grok Bot skill named **KnifeRevive Concierge** that follows these documented procedures when I ask for KnifeRevive goods or relevant Bay Area sharpening services. If your Grok Bot interface supports creating/saving a private skill, show me the behavior it will save and request my approval before saving; then verify it appears in the private skill library. Do not claim that the OpenClaw CLI package has been natively installed into Grok Bot. Keep merchant facts and live availability verifiable, respect requested comparisons, use secure first-party checkout handoffs only after explicit authorization and documented merchant consent, and never auto-pay, auto-book, create wallet credentials, or invent current services. If importing a third-party skill is unsupported, use the source as a reference and tell me what can be saved as native Grok Bot instructions instead.

## OpenAI dot — paste this prompt

> Please review the **KnifeRevive Concierge** skill at https://clawhub.ai/svetlyoh/skills/kniferevive-concierge and its complete public source at https://github.com/svetlyoh/kniferevive-agent-commerce/tree/main/skills/kniferevive-concierge. I want this workflow available to you **only when I request** relevant KnifeRevive goods shopping or SF Bay Area sharpening help. Read `SKILL.md` and the API, sharpening, and payment reference documents. If your dot can use supported local/custom skills through a computer I have explicitly connected, explain the permissions and ask before importing the reviewed skill to that local environment. Otherwise, treat the documentation as a reusable reference or proposed custom instruction and be clear that no OpenClaw skill has been installed into your dot. Browse and compare honestly, fetch the merchant's live capabilities, and require verified customer consent and payment/booking confirmation before describing any purchase or reservation as complete. Do not initiate payments, wallets, reservations, seller messaging, or background promotion without my express request. Report which instructions, if any, are actually persistent.

## What the skill can and cannot do

- It uses an agent's **existing** authorized browser/HTTP capabilities; it does not automatically add tools, accounts, checkout access, or wallet spending authority.
- It checks live merchant capabilities before using the KnifeRevive agent commerce API. If disabled or unavailable, it directs you to the normal KnifeRevive web pages.
- Goods purchases use the existing WooCommerce product checkout; eligible sharpening checkout requires separately verified service, terms, scheduling and customer consent.
- Current deployment/payment state may change. An install is **not** proof that prepaid sharpening bookings, courier pickup/return, Stripe, Google Pay, or Lightning payment are available right now.

## Official platform references

Commands and capability boundaries reviewed October 8, 2026; platform access and rollout may differ by account. The prompts above are instructions to request adoption, not evidence of a completed install.

- [OpenClaw skills, workspace/shared installation and verification](https://docs.openclaw.ai/tools/skills)
- [ClawHub quickstart: native install versus registry publishing](https://docs.openclaw.ai/clawhub/quickstart)
- [Muse Code local skills](https://dev.meta.ai/docs/muse-code/extending)
- [Meta Muse personal agent](https://ai.meta.com/muse/)
- [Grok Bot private skills](https://docs.x.ai/grok-bot/skills-routines-and-automations)
- [OpenAI dot connected computers and local skills](https://learn.chatgpt.com/docs/dots/computers-and-apps)


## Goods demonstration

Ask: 'Find a product with processor X on KnifeRevive.' Search the live Google-feed
source attributes, show each matching item inline with its actual thumbnail,
price and KnifeRevive link, and follow all result pages. If the host limits card
count, show numbered batches and the exact total; do not claim the first batch is
all matches. Google ingestion/approval is separate and must not be inferred.

Ask: 'Find model ABC-123 in the current KnifeRevive catalog.' Fetch live contracts, use exact model search, show actual selectable matches, then retain the selected ID and quantity in the private native review. If the exact model is missing, say so and label keyword alternatives. If handoff is disabled, open the canonical product page and explain that selections were not transferred. Do not request a sharpening day or add trip fees. Native pickup/delivery depends on the selected goods and destination. Actual Muse fetching/cards/opening remain host-specific checks.
