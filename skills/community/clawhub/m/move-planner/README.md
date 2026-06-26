# Move Planner

A conversational OpenClaw skill that manages every detail of a residential move. Smart templates for buying, selling, renting, relocating, and downsizing. Built-in address change checklist with 30+ common accounts. Tracks tasks, vendors, budgets, and timelines.

## What It Does

- **Smart Move Templates** -- planning timelines for sell-and-buy, first home purchase, rent-to-rent, job relocation, and downsizing
- **Task Tracking** -- checklists with due dates calculated from your move day
- **Address Change Checklist** -- pre-loaded list of 30+ accounts organized by category (government, financial, medical, subscriptions, etc.)
- **Vendor Management** -- movers, agents, lenders, inspectors, cleaners, with quotes and booking status
- **Move Budget** -- track spending against a budget with line items
- **Buy/Sell Milestones** -- light tracking of closing dates, inspections, appraisals, and mortgage milestones
- **Proactive Nudges** -- flags critical items as move day approaches

## Example Usage

**Start a move:**
> "We're selling our house and buying a new one. Moving June 15."

**Check status:**
> "Where are we on the move?"

**Log address changes:**
> "Updated the bank and credit cards today."

**Track spending:**
> "Movers quoted $2,800. Spent $120 on boxes."

## Installation

Copy the `move-planner` folder into your OpenClaw skills directory and restart your agent.

## Permissions and Privacy (read before installing)

This skill is instruction-only — it directs the assistant to read and write a single local file. It does not bundle any executable code, runs no background processes, makes no network calls of its own, and has no telemetry.

**What the skill touches**

- **Local file write**: creates and updates `move-data.json` in your working directory. No writes outside that directory.
- **No external tool calls**: the skill does not direct the assistant to use Gmail, browser automation, web search, or any third-party API. If your assistant has those tools, the skill simply doesn't reach for them.
- **No transmission**: nothing is sent to the skill's author, ClawHub, or any third party.

**Sensitive data the skill will refuse to store**

- Social Security numbers
- Full bank, credit card, or loan account numbers (institution + last 4 is plenty)
- Mortgage application materials (pay stubs, W-2s, tax returns) — only high-level milestone status
- Full driver's license or passport numbers — "updated / not updated" status is enough for the checklist

If you volunteer any of the above, the assistant will redirect you and skip the storage.

**Sharing or exporting**

When you ask for a printable timeline, vendor list, or move-day plan, the assistant generates it locally or in chat. Nothing is auto-shared anywhere.
