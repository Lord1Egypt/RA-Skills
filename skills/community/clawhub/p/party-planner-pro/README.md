# Party Planner Pro 🎉

**AI-powered party planning from first idea to last thank-you note.**

Party Planner Pro turns your AI agent into a full-service event coordinator. Plan any party or gathering — birthdays, baby showers, holiday dinners, BBQs, graduations, and more — with guest management, budget tracking, menu planning, timeline generation, vendor coordination, and day-of logistics. All from your chat.

---

## What It Does

- 🎂 **Any Event Type** — Birthday, baby shower, bridal shower, graduation, holiday party, dinner party, housewarming, BBQ, corporate event, reunion, and more. 18+ event types supported.
- 👥 **Guest Management** — Track RSVPs, dietary restrictions, allergies, +1s, groups, and seating. Never lose track of who's coming.
- 💰 **Budget Tracking** — Set budgets, allocate by category, log expenses, track cost-per-head. AI recommends allocation percentages based on your event type.
- 🍽️ **Menu Planning** — AI-generated menus that accommodate every guest's dietary needs. Quantity calculators for food, drinks, and ice. Potluck coordination.
- 📋 **Timeline & Checklists** — Auto-generated planning timeline based on your event date. Assign tasks to helpers. Smart milestone reminders.
- 🎨 **Theme & Decor** — AI-suggested themes with color palettes, decoration checklists, and supply quantity calculators.
- 📋 **Vendor Management** — Track vendor contacts, compare quotes, monitor booking and payment status.
- 📅 **Day-Of Coordination** — Hour-by-hour schedule, setup checklists, helper assignments, emergency contacts, weather backup plans.
- 🎁 **Post-Party Wrap-Up** — Expense reconciliation, thank-you note tracking, photo sharing, lessons learned.

## How to Install

1. Download the `party-planner-pro/` folder into your agent's workspace.
2. Open `SETUP-PROMPT.md` and paste the setup block into your agent's chat.
3. Your agent handles the rest — creates directories, sets permissions, verifies installation.
4. Start planning: "Help me plan a birthday party for 30 people" or "I'm hosting a dinner party next month."

**That's it.**

## What You'll Need

- An AI agent that supports OpenClaw skills (Claude Code, etc.)
- Python 3.8+ (for export and report scripts)
- Playwright (optional — for generating visual budget reports as images)

## Security

🛡️ **Security-Audited**

- Package contains no embedded API keys or credentials.
- Prompt injection defenses built in — imported guest data can't hijack your agent.
- All scripts use input validation and path traversal protection.
- Formal audit details in `CODEX-SECURITY-AUDIT.md` and policy notes in `SECURITY.md`.

## You Might Also Like

- **Budget Buddy Pro** — Track how party spending fits into your overall monthly budget.
- **Dashboard Builder** — See your event data in interactive charts.

---

*Party Planner Pro is an event organization tool. It does not book vendors, sign contracts, or make financial commitments on your behalf. For large-scale or high-stakes events, consider hiring a professional event planner.*
