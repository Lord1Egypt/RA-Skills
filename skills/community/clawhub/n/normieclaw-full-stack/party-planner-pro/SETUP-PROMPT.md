# Party Planner Pro — Setup Prompt

Copy and paste the following block into your AI agent's chat to install Party Planner Pro automatically.

---

## Setup Instructions

Paste this entire block to your agent:

```
I need you to install the Party Planner Pro skill. Run these commands exactly:

# 1. Create the skill directory structure
mkdir -p skills/party-planner-pro/config
mkdir -p skills/party-planner-pro/scripts
mkdir -p skills/party-planner-pro/examples
mkdir -p skills/party-planner-pro/dashboard-kit

# 2. Copy the skill files into place
find . -path "*/party-planner-pro/SKILL.md" -exec cp {} skills/party-planner-pro/SKILL.md \;
find . -path "*/party-planner-pro/config/settings.json" -exec cp {} skills/party-planner-pro/config/settings.json \;
find . -path "*/party-planner-pro/scripts/setup.sh" -exec cp {} skills/party-planner-pro/scripts/setup.sh \;
find . -path "*/party-planner-pro/scripts/export-plan.sh" -exec cp {} skills/party-planner-pro/scripts/export-plan.sh \;
find . -path "*/party-planner-pro/scripts/budget-report.sh" -exec cp {} skills/party-planner-pro/scripts/budget-report.sh \;
find . -path "*/party-planner-pro/examples/birthday-party-30th.md" -exec cp {} skills/party-planner-pro/examples/birthday-party-30th.md \;
find . -path "*/party-planner-pro/examples/baby-shower.md" -exec cp {} skills/party-planner-pro/examples/baby-shower.md \;
find . -path "*/party-planner-pro/examples/holiday-dinner-party.md" -exec cp {} skills/party-planner-pro/examples/holiday-dinner-party.md \;
find . -path "*/party-planner-pro/dashboard-kit/manifest.json" -exec cp {} skills/party-planner-pro/dashboard-kit/manifest.json \;
find . -path "*/party-planner-pro/dashboard-kit/DASHBOARD-SPEC.md" -exec cp {} skills/party-planner-pro/dashboard-kit/DASHBOARD-SPEC.md \;

# 3. Run the setup script to initialize data directories
chmod 700 skills/party-planner-pro/scripts/*.sh
bash skills/party-planner-pro/scripts/setup.sh

# 4. Verify the installation
echo "--- Party Planner Pro Installation Verification ---"
echo "Checking core files..."
test -f skills/party-planner-pro/SKILL.md && echo "✅ SKILL.md" || echo "❌ SKILL.md MISSING"
echo "Checking config..."
test -f skills/party-planner-pro/config/settings.json && echo "✅ settings.json" || echo "❌ settings.json MISSING"
echo "Checking data directories..."
test -d skills/party-planner-pro/data && echo "✅ data/" || echo "❌ data/ MISSING"
test -d skills/party-planner-pro/data/events && echo "✅ data/events/" || echo "❌ data/events/ MISSING"
test -d skills/party-planner-pro/data/templates && echo "✅ data/templates/" || echo "❌ data/templates/ MISSING"
echo "Checking scripts..."
test -f skills/party-planner-pro/scripts/setup.sh && echo "✅ setup.sh" || echo "❌ setup.sh MISSING"
test -f skills/party-planner-pro/scripts/export-plan.sh && echo "✅ export-plan.sh" || echo "❌ export-plan.sh MISSING"
test -f skills/party-planner-pro/scripts/budget-report.sh && echo "✅ budget-report.sh" || echo "❌ budget-report.sh MISSING"
echo "Checking examples..."
test -d skills/party-planner-pro/examples && echo "✅ examples/" || echo "❌ examples/ MISSING"
echo "Checking dashboard kit..."
test -f skills/party-planner-pro/dashboard-kit/manifest.json && echo "✅ manifest.json" || echo "❌ manifest.json MISSING"
test -f skills/party-planner-pro/dashboard-kit/DASHBOARD-SPEC.md && echo "✅ DASHBOARD-SPEC.md" || echo "❌ DASHBOARD-SPEC.md MISSING"
echo "--- Installation complete! ---"
echo ""
echo "🎉 Party Planner Pro is ready! Try: 'Help me plan a birthday party' or 'I'm hosting a dinner party for 12.'"
```

---

## What This Does

1. **Creates** the skill directory structure in your workspace.
2. **Copies** all skill files from the downloaded package into place.
3. **Runs** the setup script to create `data/` directories for storing your event data.
4. **Verifies** everything installed correctly with a checklist.

## Customizing Your Settings

Before planning your first event, you can optionally edit `skills/party-planner-pro/config/settings.json`:

- **Currency:** Change `"currency"` and `"currency_symbol"` to your local currency (e.g., `"EUR"`, `"€"`)
- **Units:** Change `"measurement_units"` to `"metric"` if you prefer grams/liters over ounces/cups
- **Guest categories:** Add or rename the default guest groups (family, friends, coworkers, etc.)
- **Budget allocations:** Adjust default percentage splits per event type to match your priorities

Most users won't need to change anything — the defaults work great for US-based planning.

## After Setup

Just start talking to your agent about your event! Try:
- "Help me plan a 30th birthday party for 40 people"
- "I'm hosting a baby shower in 6 weeks"
- "Plan a holiday dinner party — budget is $500"
- "I need a guest list for my housewarming"

Your agent will read `skills/party-planner-pro/SKILL.md` and handle everything from there.

## Uninstalling

To remove Party Planner Pro and all its data:
```
rm -rf skills/party-planner-pro/
```

Your event data lives inside `skills/party-planner-pro/data/` — back it up first if you want to keep it.
