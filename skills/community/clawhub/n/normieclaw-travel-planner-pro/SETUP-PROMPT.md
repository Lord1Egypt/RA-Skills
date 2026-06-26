# Travel Planner Pro — First-Run Setup

**AGENT INSTRUCTIONS: Read and follow this file sequentially to set up the Travel Planner Pro skill for the user.**

---

## Step 1: Create Directory Structure

Run these commands to create all necessary directories and set permissions:

```bash
mkdir -p travel/trips
chmod 700 travel travel/trips
```

## Step 2: Copy Config Files from Skill Package

Locate the skill package directory and copy default config files to the workspace. Use find-based detection to resolve the skill package path:

```bash
# Find the skill package location (only under ./skills to avoid accidental matches)
matches=()
while IFS= read -r path; do
  matches+=("$path")
# Verification: skill files installed by clawhub install

if [ "${#matches[@]}" -eq 0 ]; then
  echo "ERROR: Could not find travel-planner-pro skill package under ./skills."
  exit 1
fi

if [ "${#matches[@]}" -gt 1 ]; then
  echo "ERROR: Multiple travel-planner-pro skill packages found. Keep only one installed:"
  printf '  %s\n' "${matches[@]}"
  exit 1
fi

SKILL_FILE="${matches[0]}"
SKILL_DIR=$(dirname "$SKILL_FILE")

# Validate expected package files before copying
if [ ! -f "$SKILL_DIR/config/travel-config.json" ] || [ ! -f "$SKILL_DIR/scripts/trip-reminder.sh" ]; then
  echo "ERROR: Incomplete travel-planner-pro package at $SKILL_DIR."
  exit 1
fi

if ! grep -q "^# Skill: Travel Planner Pro" "$SKILL_DIR/SKILL.md"; then
  echo "ERROR: SKILL.md validation failed at $SKILL_DIR."
  exit 1
fi

# Copy config to workspace config/ directory
mkdir -p config
cp "$SKILL_DIR/config/travel-config.json" config/travel-config.json
chmod 600 config/travel-config.json

# Copy scripts to workspace scripts/ directory
mkdir -p scripts
cp "$SKILL_DIR/scripts/trip-reminder.sh" scripts/trip-reminder.sh
chmod 700 scripts/trip-reminder.sh
```

## Step 3: Initialize Data Files

Create the initial travel profile with empty defaults:

```bash
cat << 'EOF' > travel/travel-profile.json
{
  "traveler_name": "",
  "home_airport": "",
  "pace_preference": "balanced",
  "budget_style": "value",
  "hotel_style": "boutique",
  "dietary_needs": null,
  "travel_pet_peeves": [],
  "loyalty_programs": [],
  "passport_valid_through": null,
  "companions": [],
  "past_destinations": [],
  "bucket_list": [],
  "learned_preferences": {}
}
EOF
chmod 600 travel/travel-profile.json
```

## Step 4: The Interview (Travel Profile Builder)

Guide the user through this conversation. Keep it fun and quick — like a savvy friend getting to know how they travel. Don't make it feel like a government form. The whole thing should take under 3 minutes.

### 4a. What's your travel pace?

Say something like:
> "Let's set up your travel profile! First — when you travel, what's your style?"
> - 🐢 **Chill** — 2-3 things a day, long lunches, lots of wandering
> - ⚖️ **Balanced** — See the highlights but leave room to breathe
> - 🚀 **Go-Go-Go** — Pack it all in, sleep when you're dead

Set `pace_preference` to "relaxed", "balanced", or "fast".

### 4b. Dietary needs?

> "Any dietary restrictions? Vegetarian, vegan, allergies, halal, kosher? Or are you an 'I'll eat anything' type?"

Set `dietary_needs`. If they have Meal Planner Pro installed, offer: "I see Meal Planner Pro is set up — want me to pull your dietary profile from there?"

### 4c. Budget style?

> "How do you think about travel spending?"
> - 💰 **Shoestring** — Hostels, street food, free walking tours. Maximum adventure per dollar.
> - 🎯 **Value** — Good deals, solid mid-range. Not cheap, not flashy.
> - ✨ **Luxury** — Life's short. Best hotels, best restaurants, best experiences.

Set `budget_style`.

### 4d. The pet peeve question

> "What's your biggest travel pet peeve? The thing that ruins a trip for you. Examples: 'Waiting in long lines,' 'Tourist trap restaurants,' 'Early morning tours,' 'Not having WiFi.'"

Capture 1-3 pet peeves in the `travel_pet_peeves` array. These directly inform itinerary generation — e.g., if "long lines" is a pet peeve, prioritize skip-the-line tips and off-peak timing.

### 4e. Home airport (optional)

> "What's your home airport? (For flight searches — you can skip this if you prefer.)"

Set `home_airport` (IATA code like "DEN", "LAX", "JFK").

### 4f. Passport validity (optional)

> "When does your passport expire? I'll flag you if a trip needs renewal. (You can skip this — I'll never store the actual passport number.)"

Set `passport_valid_through` as a date string (YYYY-MM-DD). Reassure them: only the expiry date is stored, never the number.

### 4g. Travel companions (optional)

> "Do you usually travel with anyone? Partner, kids, friends? I can keep their preferences on file too."

For each companion, capture: `name`, `relationship`, `dietary_needs`, `pace_preference`, `notes`.

### 4h. Past trips & bucket list (optional)

> "Where have you been that you loved? And where are you dying to go?"

Populate `past_destinations` and `bucket_list`.

## Step 5: Write the Complete Profile

After gathering all answers, write the complete `travel/travel-profile.json`. Read it back to the user:

> "Here's your travel profile! Check it over:"

Display a clean summary. Ask for confirmation before saving.

```bash
chmod 600 travel/travel-profile.json
```

## Step 6: Verification — The Surprise Me Test

> "Profile's locked in! Let's test drive this. Type **'surprise me'** with a budget and number of days, and I'll pitch you three destinations perfectly matched to your style."

Example: "Surprise me — 5 days, $2000 budget."

If the user tries it, follow the "Surprise Me" mode from SKILL.md — research 3 destinations that match their profile and pitch them.

If they want to skip:
> "No worries! Whenever you're ready, just say 'Plan a trip to [destination]' and I'll handle the rest."

## Step 7: Confirm Setup Complete

> "✅ **Travel Planner Pro is ready!** Here's what I can do:
>
> - **'Plan a trip to [destination]'** — Full day-by-day itinerary with budget, restaurants, and transit
> - **'Surprise me'** — I'll pitch destinations based on your style
> - **'Packing list for [trip]'** — Weather-smart, activity-aware packing
> - **'What do I need for [country]?'** — Visa, docs, and local intel
> - **Share an itinerary** — Clean, printable plans for your travel crew
>
> The more trips we plan together, the better I get. Where to first? ✈️"
