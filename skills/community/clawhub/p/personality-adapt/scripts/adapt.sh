#!/bin/bash
# Adaptation engine: review observations and update personality model
# Usage: bash adapt.sh [--dry-run]

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OBS_LOG="${SKILL_DIR}/observations.json"
PERSONALITY_FILE="${SKILL_DIR}/PERSONALITY.md"
DRY_RUN="${1}"

echo "=== Personality Adaptation Engine ==="

if [ ! -f "$OBS_LOG" ]; then
  echo "No observations found: ${OBS_LOG}"
  exit 0
fi

python3 - "$OBS_LOG" "$PERSONALITY_FILE" "$DRY_RUN" << 'PYEOF'
import json, sys, os
from collections import Counter
from datetime import datetime

obs_log = sys.argv[1]
personality_file = sys.argv[2]
dry_run = sys.argv[3] if len(sys.argv) > 3 else None

# Load all observations
with open(obs_log, "r") as f:
    observations = json.load(f)

with open(personality_file, "r") as f:
    personality_content = f.read()

print(f"Total observations loaded: {len(observations)}")

# --- Analyze observations ---
# Count observations by category and specific observation text
by_category = Counter(o["category"] for o in observations)
by_observation = Counter(o["observation"] for o in observations)

print("\nBy category:")
for cat, count in by_category.most_common():
    print(f"  {cat}: {count}")

print("\nTop observations (by count):")
for obs, count in by_observation.most_common(10):
    print(f"  - {obs}: {count}x")

# Identify high-confidence patterns (seen 2 or more times)
# These are candidates for explicit mention or adaptation rules
high_confidence_patterns = {obs: count for obs, count in by_observation.items() if count >= 2}
print(f"\nHigh-confidence patterns (2+ instances): {len(high_confidence_patterns)}")

# Extract direct suggestions for adaptation
adaptation_suggestions = []

# Communication style adaptations
if by_observation.get("dislikes verbosity", 0) >= 2:
    adaptation_suggestions.append("→ Keep responses even shorter. Lead with the answer or most critical info.")
if by_observation.get("prefers conciseness", 0) >= 1:
    adaptation_suggestions.append("→ Cut filler words like 'Great question!' or 'I'd be happy to help!'")
if by_observation.get("wants directness", 0) >= 2:
    adaptation_suggestions.append("→ When Eric asks 'should I...', provide a direct recommendation with brief reasoning.")
if by_observation.get("dislikes over-explanation", 0) >= 2:
    adaptation_suggestions.append("→ Avoid explaining common concepts. Assume technical familiarity.")
if by_observation.get("values precision/accuracy", 0) >= 2:
    adaptation_suggestions.append("→ Strive for precision in facts and figures. Double-check when possible.")

# Decision-making habits
if by_observation.get("action-oriented", 0) >= 2:
    adaptation_suggestions.append("→ When Eric asks 'should I...', provide a direct recommendation with brief reasoning (overlaps with comms style).") # Example of overlap
if by_observation.get("reversibility-aware", 0) >= 2:
    adaptation_suggestions.append("→ Frame suggestions cautiously if they seem irreversible. Mention reversibility if applicable.")
if by_observation.get("bias toward action", 0) >= 2:
    adaptation_suggestions.append("→ When Eric seems stuck, suggest a small, actionable first step.")

# Values / Interests
if by_observation.get("values privacy/local-first", 0) >= 3:
    adaptation_suggestions.append("→ Always prioritize local/self-hosted solutions. Highlight privacy benefits.")
if by_observation.get("values pragmatism/efficiency", 0) >= 2:
    adaptation_suggestions.append("→ Focus on practical, efficient solutions. Avoid overly complex or theoretical approaches.")
if by_observation.get("values open source/community", 0) >= 2:
    adaptation_suggestions.append("→ Highlight open-source aspects when relevant.")

# Frustrations
if by_observation.get("frustration signal", 0) >= 3:
    adaptation_suggestions.append("→ Eric seems frustrated. Be more direct and concise; skip pleasantries.")
if by_observation.get("impatient with inefficiency", 0) >= 2:
    adaptation_suggestions.append("→ Speed up responses where possible. Offer quick summaries.")
if by_observation.get("dislikes external dependencies/locks", 0) >= 2:
    adaptation_suggestions.append("→ Avoid suggesting cloud services or API keys unless absolutely necessary, and only if local alternatives are worse.")

# --- Update PERSONALITY.md ---
if not dry_run:
    update_made = False
    new_personality_lines = personality_content.split('\n')

    # Add recurring observations to relevant sections if not already present
    section_map = {
        "communication_style": "Communication Style",
        "decision_making": "Decision-Making",
        "values": "Values & Interests",
        "frustrations": "Boundaries", # Frustrations map to Boundaries
        "interests": "Values & Interests",
        "emotional_state": "Personality Traits",
        "prioritization": "Decision-Making", # Or a new section? Mapping to Decision-Making for now.
    }

    # Group recurring observations by the PERSONALITY.md section they belong to
    section_updates = {}
    for obs, count in high_confidence_patterns.items():
        # Find the category for this observation
        obs_category = None
        for o in observations:
            if o["observation"] == obs:
                obs_category = o["category"]
                break
        
        if obs_category:
            section_name = section_map.get(obs_category, "Personality Traits") # Default section
            if section_name not in section_updates:
                section_updates[section_name] = []
            
            # Check if the observation is already mentioned in the personality file
            # Simple check: does the observation text appear in the section?
            section_start, section_end = find_section_in_personality(section_name, personality_content)
            if section_start and section_end:
                section_text = personality_content[section_start:section_end]
                if obs.lower() not in section_text.lower():
                    section_updates[section_name].append(f"- {obs} (seen {count}x)")
                    update_made = True
            else: # Section doesn't exist yet, placeholder
                section_updates[section_name].append(f"- {obs} ({count}x)")
                update_made = True
    
    # Inject updates into the PERSONALITY.md structure
    final_lines = []
    current_section = None
    inserted_updates = set()

    for line in new_personality_lines:
        if line.startswith("## "):
            section_title = line[3:].strip()
            final_lines.append(line)
            if section_title in section_updates:
                # Insert updates for this section
                for update in section_updates[section_title]:
                    final_lines.append(f"  {update}")
                inserted_updates.add(section_title)
            current_section = section_title
        else:
            final_lines.append(line)
            current_section = current_section # Maintain current section

    # Append sections that didn't exist but have updates
    for section_title, updates in section_updates.items():
        if section_title not in inserted_updates:
            final_lines.append(f"\n## {section_title}")
            for update in updates:
                final_lines.append(f"  {update}")
            update_made = True


    if update_made:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        update_note = f"\n\n_Adapted at {timestamp} based on recurring patterns ({len(high_confidence_patterns)} identified)._"
        final_lines.append(update_note)

        with open(personality_file, "w") as f:
            f.write("\n".join(final_lines))
        print(f"\nPERSONALITY.md updated.")
    else:
        print("\nNo new recurring patterns to add — PERSONALITY.md is current.")

else: # Dry run output
    print("\n[DRY RUN] Recurring patterns identified:")
    if high_confidence_patterns:
        for obs, count in high_confidence_patterns.items():
            print(f"  - {obs} (seen {count}x)")
    else:
        print("  No recurring patterns found.")

# --- Adaptation Suggestions ---
print("\n=== Adaptation Suggestions ===")
if adaptation_suggestions:
    for s in adaptation_suggestions:
        print(s)
else:
    print("No strong adaptation signals yet. Keep observing.")

PYEOF

echo "=== Done ==="
