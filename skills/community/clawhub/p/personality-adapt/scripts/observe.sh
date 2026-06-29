#!/bin/bash
# Extract personality observations from daily notes and assistant logs
# Usage: bash observe.sh [--days 7] [--dry-run]

set -e

WORKSPACE="/root/.openclaw/workspace"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DAYS="${1:-7}"
DRY_RUN="${2}"

echo "=== Personality Observation Engine ==="
echo "Scanning last ${DAYS} days of daily notes and assistant logs..."

python3 - "${WORKSPACE}" "${SKILL_DIR}" "${DAYS}" "${DRY_RUN}" << 'PYEOF'
import json, os, glob, sys, re
from datetime import datetime, timedelta
from collections import Counter

workspace = sys.argv[1]
skill_dir = sys.argv[2]
days = int(sys.argv[3])
dry_run = sys.argv[4] if len(sys.argv) > 4 else None

daily_dir = f"{workspace}/memory"
personality_file = f"{skill_dir}/PERSONALITY.md"
obs_log_file = f"{skill_dir}/observations.json"

# --- Observation Patterns ---
# These patterns capture signals related to personality traits, preferences, and behaviors.
# They are categorized for structured learning.
OBSERVATION_PATTERNS = {
    "communication_style": [
        (r'\b(no|don\'t|stop|quit)\s+(?:the|with the)\s+(?:long|verbose|wordy|fluff|unnecessary|extra)\s*(?:words|explanations)?', 'dislikes verbosity'),
        (r'\b(keep it|make it|be)\s+(?:short|concise|brief|tight|direct)', 'prefers conciseness'),
        (r'\b(just|get to)\s+(?:the point|it|it)\b', 'wants directness'),
        (r'\b(don\'t|do not)\s+(?:over.?explain|elaborate|dwell on)', 'dislikes over-explanation'),
        (r'\b(perfect|great|exactly|that\'s it|spot on)\s*[!！]', 'values precision/accuracy'),
        (r'\b(sounds good|alright|okay)\s*[!！]', 'acceptance/acknowledgement'),
        (r'\b(let\'s see|hmm|i wonder)', 'contemplative/curious'),
        (r'\b(i agree|exactly|precisely)', 'agreement/alignment'),
    ],
    "decision_making": [
        (r'\b(let\'s|i\'ll|we should)\s+(?:try|test|experiment|ship|deploy|build|do|start|move|go)\b', 'action-oriented'),
        (r'\b(don\'t overthink|just do it|ship it|move fast|make a call)', 'bias toward action'),
        (r'\b(we can always|can revert|is reversible|undo|change it later)', 'reversibility-aware'),
        (r'\b(plan out|think through|analyze|consider all options|research first)', 'analytical pre-decision'),
        (r'\b(impulsive|quick decision|gut feeling)', 'intuitive decision-making'),
    ],
    "values": [
        (r'\b(local|self.?hosted|no cloud|no API key|no external|offline)\b', 'values privacy/local-first'),
        (r'\b(no fluff|no bs|no nonsense|pragmatic|practical|efficient)\b', 'values pragmatism/efficiency'),
        (r'\b(elegant|clean|simple|minimal|minimalist)\b', 'values simplicity'),
        (r'\b(secure|privacy|private|encrypt|confidential)\b', 'values security'),
        (r'\b(free.?and.?open|FOSS|open source|community)\b', 'values open source/community'),
        (r'\b(reliable|robust|stable|well-tested)\b', 'values reliability'),
    ],
    "frustrations": [
        (r'\b(annoying|frustrat|irritat|tired of|sick of|hate|dislike)\b', 'frustration signal'),
        (r'\b(why does|this shouldn\'t|this is broken|this does not work|doesn\'t make sense)', 'frustration with tools/logic'),
        (r'\b(takes too long|too slow|waste of time|inefficient)\b', 'impatient with inefficiency'),
        (r'\b(API key|paywall|vendor lock|proprietary|closed source)\b', 'dislikes external dependencies/locks'),
        (r'\b(jargon|complex|confusing|unclear)\b', 'dislikes obscurity'),
    ],
    "interests": [
        (r'\b(TypeScript|Node\.js|npm|package|JavaScript)\b', 'interested in JS ecosystem'),
        (r'\b(Docker|container|Kubernetes|deploy|server|VM|host|cloud|AWS|GCP|Azure)\b', 'interested in infrastructure/devops'),
        (r'\b(API|webhook|endpoint|REST|GraphQL|schema)\b', 'interested in APIs/integrations'),
        (r'\b(automation|cron|script|workflow|pipeline)\b', 'interested in automation'),
        (r'\b(database|SQL|Mongo|Postgres|Meili|Lance|vector|AI|ML)\b', 'interested in data/AI systems'),
        (r'\b(OpenClaw|skill|agent|CLI)\b', 'interested in AI agent tech'),
        (r'\b(security|crypto|privacy|encryption)\b', 'interested in security'),
    ],
    "emotional_state": [
        (r'\b(excited|pumped|love this|this is great|fantastic|amazing|awesome|cool)\b', 'positive/enthusiastic'),
        (r'\b(confused|unsure|not sure|what do you think|lost|stuck)\b', 'uncertain/seeking input'),
        (r'\b(busy|tired|late night|early morning|exhausted|overwhelmed)\b', 'energy level signal'),
        (r'\b(frustrated|annoyed|upset|ugh)\b', 'negative emotional signal'),
        (r'\b(curious|wondering|explore|interested)\b', 'curiosity'),
        (r'\b(satisfied|happy|good job|well done)\b', 'satisfaction signal'),
    ],
    "prioritization": [
        (r'\b(urgent|immediate|priority)\b', 'high priority'),
        (r'\b(later|maybe|eventually|sometime)\b', 'low priority'),
        (r'\b(first|initially|start with)\b', 'sequential prioritization'),
        (r'\b(fix this first|resolve this now)\b', 'urgent task'),
    ]
}

# --- Helper functions ---
def find_section_in_personality(section_name, personality_content):
    """Finds the start and end of a section in PERSONALITY.md"""
    start_marker = f"\n\n## {section_name}\n"
    start_index = personality_content.find(start_marker)
    if start_index == -1:
        return None, None # Section not found

    end_marker_index = personality_content.find("\n\n## ", start_index + len(start_marker))
    if end_marker_index == -1:
        end_index = len(personality_content) # Last section
    else:
        end_index = end_index

    return start_index + len(start_marker), end_index

def clean_line(line):
    """Cleans a line to extract potential personality signals"""
    line = line.strip()
    # Remove markdown formatting for pattern matching
    line = re.sub(r'\*\*(.+?)\*\*', r'\1', line) # Bold
    line = re.sub(r'\*(.+?)\*', r'\1', line)  # Italic
    line = re.sub(r'`(.+?)`', r'\1', line)   # Inline code
    line = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', line) # Links
    line = re.sub(r'^- |\* |- ', '', line) # Remove list markers
    return line

# --- Main logic ---
cutoff = datetime.now() - timedelta(days=days)
observations_data = []
files_scanned = 0

# Load existing observations to avoid duplicates
existing_obs_keys = set()
if os.path.exists(obs_log_file):
    with open(obs_log_file, "r") as f:
        try:
            existing_obs_list = json.load(f)
            existing_obs_keys = {o["key"] for o in existing_obs_list}
        except json.JSONDecodeError:
            print(f"Warning: Could not parse {obs_log_file}. Starting fresh observations.")

for fname in sorted(glob.glob(f"{daily_dir}/*.md")):
    try:
        file_date = datetime.strptime(os.path.basename(fname)[:10], "%Y-%m-%d")
    except:
        continue # Skip files with invalid date format
    if file_date < cutoff:
        continue

    files_scanned += 1
    with open(fname, "r") as f:
        content = f.read()
    if len(content) < 50: # Skip very short files
        continue

    lines = content.split("\n")
    for line in lines:
        line_content = clean_line(line)
        if not line_content:
            continue

        # Analyze based on who is speaking
        speaker = None
        message_text = line_content
        if line.startswith("user:") or line.startswith("> "):
            speaker = "user"
            message_text = line.split(":", 1)[-1].strip() if ":" in line else line[2:].strip()
        elif line.startswith("assistant:") or line.startswith("⚔️"):
            speaker = "assistant"
            message_text = line.split(":", 1)[-1].strip() if ":" in line else line[2:].strip()
        elif line.startswith("tool_call:") or line.startswith("tool_result:"):
            speaker = "tool"
            message_text = line.split(":", 1)[-1].strip()
        else:
            # Try to infer context if it's not clearly marked
            # This is heuristic and might need tuning
            if "user:" in line_content.lower() or "> " in line_content.lower():
                speaker = "user"
                message_text = line_content # Keep full line if not clearly delineated
            elif "assistant:" in line_content.lower() or "⚔️" in line_content.lower():
                speaker = "assistant"
                message_text = line_content
            else:
                continue # Skip lines without clear speaker context

        if not message_text or len(message_text) < 10:
            continue

        # Extract personality signals from the relevant speaker's message
        if speaker == "user" or speaker == "assistant":
            for category, patterns in OBSERVATION_PATTERNS.items():
                for pattern_regex, observation in patterns:
                    if re.search(pattern_regex, message_text, re.IGNORECASE):
                        obs_key = f"{category}:{observation}"
                        # Avoid duplicate observations from the same source/message segment
                        if obs_key not in existing_obs_keys:
                            existing_obs_keys.add(obs_key) # Add to set to avoid duplicates in this run
                            observations_data.append({
                                "key": obs_key, # Unique identifier for deduping
                                "category": category,
                                "observation": observation,
                                "evidence": message_text[:100], # Snippet of evidence
                                "source": os.path.basename(fname),
                                "date": file_date.strftime("%Y-%m-%d"),
                                "speaker": speaker # Track who said it
                            })

print(f"Files scanned: {files_scanned}")
print(f"Potential new observations: {len(observations_data)}")

if observations_data and not dry_run:
    # Append to observations.json, managing duplicates
    all_obs = []
    if os.path.exists(obs_log_file):
        with open(obs_log_file, "r") as f:
            try:
                all_obs = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {obs_log_file}. Starting fresh observations.")

    # Add new, unique observations
    initial_count = len(all_obs)
    existing_keys = {o["key"] for o in all_obs}
    for obs in observations_data:
        if obs["key"] not in existing_keys:
            all_obs.append(obs)
            existing_keys.add(obs["key"]) # Add immediately to avoid adding same observation multiple times if found in logs

    with open(obs_log_file, "w") as f:
        json.dump(all_obs, f, indent=2)

    print(f"Logged {len(all_obs) - initial_count} new observations to {obs_log_file}")

elif observations_data and dry_run:
    print("\n[DRY RUN] Potential new observations:")
    for o in observations_data[:10]: # Show a sample
        print(f"  - [{o['category']}] {o['observation']} (from {o['source']})")

else:
    print("No new observations collected.")

# --- Adaptation Trigger ---
# This part is more about signalling for adapt.sh to run, not direct action here.
# The cron job for adapt.sh runs independently based on time.
PYEOF

echo "=== Done ==="
