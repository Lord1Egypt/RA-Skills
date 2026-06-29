---
name: Moving Checklist
slug: moving-checklist
description: Generate a personalized moving timeline & checklist based on your home info, timeline, and moving distance.
tags: [moving, relocation, checklist, planning, household, china]
version: 1.0.0
license: MIT-0
---

# Moving Checklist (搬家清单助手)

Generate a personalized, printable moving handbook with a countdown timeline, categorized task lists, budget estimates, and roommate/family role assignments.

## Scripts

| Path | Description |
|------|-------------|
| `scripts/checklist.py` | Main CLI script — interactive or profile-based checklist generation |
| `schemas/input.schema.json` | JSON Schema for input (moving profile) |
| `schemas/output.schema.json` | JSON Schema for output (handbook, timeline, budget) |
| `references/task_templates.json` | Task template library for all categories |
| `references/budget_tiers.json` | Budget reference by city tier and distance |

### CLI Usage

```bash
# Generate checklist from JSON profile
python scripts/checklist.py --profile '{"current":"整租","new_address":"上海浦东","move_date":"2025-07-15","distance":"同城","household_size":"solo"}'

# Interactive mode (step-by-step)
python scripts/checklist.py --interactive

# JSON output for programmatic use
python scripts/checklist.py --profile '{"distance":"跨城","household_size":"family","special_items":["钢琴","猫"]}' --output json
```

## 🚀 First-Success Path (3 Steps)

1. **Step 1**: Run `python scripts/checklist.py --interactive` or provide a profile
2. **Step 2**: Answer 3 quick questions (date? furniture owned? household size?)
3. **Step 3**: Receive personalized countdown timeline + categorized checklist in <20 seconds

## Core Capabilities

- **Countdown timeline**: Auto-generate tasks from D-30 through D+7 post-move
- **Categorized checklists**: Admin (address changes, utilities), packing (declutter, boxing order), logistics (mover comparison, elevator booking), cleaning (move-out + move-in)
- **Roommate/family mode**: Assign tasks to household members with deadlines
- **Budget estimation**: Mover quotes, packing materials, cleaning fees, deposit expectations
- **Inter-city vs intra-city**: Tailor logistics based on distance
- **Printable handbook**: Export as formatted Markdown

## Workflow (7 Steps)

### Step 1: Gather Moving Context
**Input**: User answers a short questionnaire (interactive or one-shot):
- Current residence type: 整租 (rental whole) / 合租 (shared) / 自有 (owned)
- New address (city + district, or "same city")
- Moving date
- Moving distance: 同城 (same city) / 跨城 (inter-city) / 跨国 (international)
- Furniture/appliances: owned or landlord's?
- Household size: solo / couple / family (specify members)
- Special items: piano, pet, plants, fragile collection?

**Output**: Structured moving profile JSON.
**Logic**: Ask missing fields one by one if user provides incomplete info.

### Step 2: Generate Countdown Timeline
**Input**: Moving profile.
**Output**: Timeline from D-30 to D+7 with task buckets.

| Period | Focus | Example Tasks |
|--------|-------|---------------|
| D-30~D-14 | Planning | Research movers, declutter, notify landlord |
| D-14~D-7 | Preparation | Book movers, start packing non-essentials, change address |
| D-7~D-3 | Packing | Pack room by room, label boxes, arrange utilities transfer |
| D-3~D-1 | Final Prep | Defrost fridge, pack essentials bag, confirm mover time |
| D-Day | Move Day | Supervise loading, final walkthrough, key handover |
| D+1~D+7 | Settling | Unpack priorities, register at new community, update ID address |

**Logic**: Adjust density based on timeline length. Urgent move (<7 days) → compressed mode.

### Step 3: Categorize Tasks into 4 Pillars
**Input**: Moving profile + timeline.
**Output**: Tasks organized into 4 categories.

#### A. Admin Tasks
- Change address: bank, social security (社保), delivery apps, subscriptions
- Rental: notice to landlord, deposit negotiation, contract termination
- Utilities: water, electricity, gas, internet transfer or cancellation
- Documentation: 居住证 (residence permit) update if inter-city

#### B. Packing Tasks
- Declutter list: sell/donate/discard by room
- Packing order: off-season clothes → books → decorations → daily items
- Valuables list: documents, jewelry, electronics (keep with you)
- Box labeling system: room name + content summary + fragile flag

#### C. Logistics Tasks
- Mover comparison: 货拉拉 (HuoLala) vs 快狗 (Kuaigou) vs traditional movers
- Box count estimation: 1BR ≈ 15-20 boxes, 2BR ≈ 25-35, 3BR ≈ 40-55
- Elevator booking: reserve freight elevator if applicable
- Parking permit for moving truck
- Insurance: check mover insurance coverage, consider supplemental

#### D. Cleaning Tasks
- Move-out: wall marks, kitchen grease, bathroom mold, floor, window tracks
- Move-in: sanitize kitchen/bathroom, check for pests, test all appliances

### Step 4: Household Role Assignment (Multi-person Mode)
**Input**: Household members.
**Output**: Responsibility matrix.

| Task | Owner | Deadline | Status |
|------|-------|----------|--------|
| Book movers | 小王 | D-14 | ⬜ |
| Pack kitchen | 小李 | D-3 | ⬜ |

**Logic**: Default assignment by room or by category. User can override.

### Step 5: Budget Estimation
**Input**: Moving profile.
**Output**: Estimated cost breakdown.

| Category | Item | Est. Cost |
|----------|------|-----------|
| Movers | 货拉拉 (within city, 1BR) | ¥300-500 |
| Packing | Boxes ×20, tape, bubble wrap | ¥80-150 |
| Cleaning | Move-out deep clean | ¥200-400 |
| Deposit | Expected deductions | ¥0-1000 |

**Logic**: Use city-tier multipliers (Tier 1 cities +30%).

### Step 6: Generate Printable Handbook
**Input**: All previous outputs.
**Output**: Complete moving handbook in structured Markdown, ready for print/export.
**Sections**: Cover page → Countdown calendar → Admin checklist → Packing guide → Logistics plan → Cleaning checklist → Budget sheet → Emergency contacts.

### Step 7: Post-Move Follow-up
**Input**: Move completed.
**Output**: D+1 through D+7 settling tasks, community registration guide, utility setup checklist.
**Logic**: Triggered by user confirming "move complete".

## Sample Prompts

### Prompt 1: Solo Move (Same City)
**User:**
```bash
python scripts/checklist.py --profile '{"current":"整租","new_address":"上海浦东","move_date":"2025-07-15","distance":"同城","household_size":"solo"}'
```
**Expected Output:**
```
  Moving Profile: 整租 → 上海浦东
  Date: 2025-07-15 | Distance: 同城
  Household: solo | City tier: Tier 1

  [Step 2/7] Generating countdown timeline...
  -> 6 timeline periods generated

  [Step 3/7] Categorizing tasks into 4 pillars...
  -> 35 tasks across 4 categories

  [Step 4/7] Assigning roles...
  -> You

  [Step 5/7] Estimating budget...
  -> Estimated: ¥923-1690

  [Step 6/7] Generating printable handbook...
  -> Handbook generated (4230 chars)

============================================================
# Moving Handbook / 搬家手册

**Generated**: 2025-07-01 ...
**Move Date**: 2025-07-15
**From → To**: 整租 → 上海浦东
**Distance**: 同城
**Household**: solo
...
============================================================

  Step 7/7: Post-move follow-up available after move confirmation

  Handbook complete! Save the output for your move.
```

### Prompt 2: Inter-City Family Move with Special Items
**User:**
```bash
python scripts/checklist.py --profile '{"distance":"跨城","household_size":"family","special_items":["钢琴","猫"],"move_date":"2025-08-01","new_address":"杭州滨江"}'
```
**Expected Output:**
```
  Moving Profile: 整租 → 杭州滨江
  Date: 2025-08-01 | Distance: 跨城
  Household: family | City tier: Tier 2

  [Step 2/7] Generating countdown timeline...
  -> 7 timeline periods generated (including special items)

  [Step 3/7] Categorizing tasks into 4 pillars...
  -> 40 tasks across 4 categories (with inter-city extras)

  [Step 5/7] Estimating budget...
  -> Estimated: ¥3790-7900

  Budget includes special item surcharges (piano mover + pet transport)
```

### Prompt 3: Couple Move with Full Furniture
**User:**
```bash
python scripts/checklist.py --profile '{"current":"自有","new_address":"北京朝阳","move_date":"2025-09-01","household_size":"couple","furniture":"全部自有","household_members":["Alice","Bob"]}'
```
**Expected Output:**
```
  Moving Profile: 自有 → 北京朝阳
  Date: 2025-09-01 | Distance: 同城
  Household: couple | City tier: Tier 1

  [Step 4/7] Assigning roles...
  -> Team (with Alice and Bob having default category assignments)

  [Step 5/7] Estimating budget...
  -> Box estimate: 20-30 boxes (couple with all furniture)
  -> Estimated: ¥1372-2600

  Handbook includes role assignment matrix for couple
```

### Prompt 4: Urgent Solo Move (Short Notice)
**User:**
```bash
python scripts/checklist.py --profile '{"current":"合租","new_address":"深圳南山","distance":"同城","move_date":"2025-07-10","household_size":"solo"}'
```
**Expected Output:**
```
  Moving Profile: 合租 → 深圳南山
  Date: 2025-07-10 | Distance: 同城
  Household: solo | City tier: Tier 1

  [Step 2/7] Generating countdown timeline...
  -> 5 timeline periods (compressed mode, < 7 days to move)

  Features compressed/urgent timeline with fewer, prioritized tasks
```

### Prompt 5: JSON Output for Programmatic Use
**User:**
```bash
python scripts/checklist.py --profile '{"current":"整租","new_address":"成都高新区","move_date":"2025-08-15","distance":"同城","household_size":"solo"}' --output json
```
**Expected Output:**
```json
{
  "version": "1.0.0",
  "profile": {
    "current": "整租",
    "new_address": "成都高新区",
    "move_date": "2025-08-15",
    "distance": "同城",
    "household_size": "solo",
    "city_tier": "Tier 2"
  },
  "timeline": [...],
  "categories": {...},
  "role_assignment": {"owner": "You", "note": "Solo move — all tasks assigned to you."},
  "budget": {
    "city_tier": "Tier 2",
    "multiplier": 1.0,
    "box_count_estimate": "15-20",
    "total_range": "¥610-1320"
  },
  "handbook": "..."
}
```

### Prompt 6: Interactive Mode
**User:**
```bash
python scripts/checklist.py --interactive
```
**Expected Output:**
```
== Moving Checklist — Interactive Setup ==

Current residence type (整租/合租/自有):
New address (city + district):
Move date (YYYY-MM-DD):
Distance (同城/跨城/跨国):
Household size (solo/couple/family):
Furniture (房东提供/部分自有/全部自有):
Special items (comma-separated, or leave blank):
...
```
Followed by the same complete handbook output.

## Boundary Conditions

[Boundary conditions unchanged from design doc]

## Error Handling

[Error handling unchanged from design doc]

## Security Requirements

- **Address privacy**: Use city+district level only; never store full street address
- **No financial data**: Budget estimates are generic ranges; no actual bank/payment info
- **Household member names**: Allow pseudonyms/nicknames; never require real names
- **Export sanitization**: Strip metadata from generated PDFs
