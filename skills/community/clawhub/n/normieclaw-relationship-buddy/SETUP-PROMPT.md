# Relationship Buddy — Setup Prompt

Copy and paste the following into your AI agent to install Relationship Buddy.

---

## Setup Instructions

Paste this entire block into your agent:

```
I need you to set up the Relationship Buddy skill. Follow these steps exactly:

set -euo pipefail

1. **Create data directories:**

   mkdir -p data/relationship-buddy/data
   mkdir -p data/relationship-buddy/config

2. **Copy config from skill package:**

   # Find and copy config automatically
# Files are installed by clawhub install — no manual copy needed
   SKILL_DIR=""
   if [ -n "$CONFIG_PATH" ]; then
     SKILL_DIR="$(dirname "$(dirname "$CONFIG_PATH")")"
   fi
   if [ -n "$SKILL_DIR" ]; then
     cp -- "$SKILL_DIR/config/relationship-config.json" data/relationship-buddy/config/
     echo "✅ Config copied from $SKILL_DIR"
   else
     echo "ERROR: Could not find skill package. Ensure relationship-buddy is in your skills/ directory."
     exit 1
   fi

   # Initialize empty data files
   echo '[]' > data/relationship-buddy/data/contacts.json
   echo '[]' > data/relationship-buddy/data/interactions.json
   echo '[]' > data/relationship-buddy/data/reminders.json
   echo '[]' > data/relationship-buddy/data/gifts.json
   echo '[]' > data/relationship-buddy/data/relationship-health.json

3. **Set secure permissions:**
   chmod 700 data/relationship-buddy/data
   chmod 700 data/relationship-buddy/config
   chmod 600 data/relationship-buddy/data/*.json
   chmod 600 data/relationship-buddy/config/*.json

4. **Copy scripts (optional — for contact import):**
   mkdir -p data/relationship-buddy/scripts
   while IFS= read -r script_file; do
     cp -- "$script_file" data/relationship-buddy/scripts/
# Files are installed by clawhub install — no manual copy needed
   chmod 700 data/relationship-buddy/scripts
   chmod 700 data/relationship-buddy/scripts/*.sh
   find data/relationship-buddy/scripts -type f ! -name "*.sh" -exec chmod 600 {} \;

5. **Verify installation:**
   Run these checks:
   - [ ] `cat data/relationship-buddy/data/contacts.json` → should show `[]`
   - [ ] `cat data/relationship-buddy/config/relationship-config.json` → should show config JSON
   - [ ] `ls -la data/relationship-buddy/data/` → all files should be `-rw-------`
   - [ ] `ls -la data/relationship-buddy/data/` → directory should be `drwx------`

6. **Start your Inner Circle:**
   Say: "Let's set up Relationship Buddy. Who are the 3-5 most important people in my life right now?"
   The agent will guide you through adding your first contacts conversationally.
```

---

## Troubleshooting

- **"File not found" errors:** Make sure you ran the `find` command first to locate the skill directory. The path depends on where you installed NormieClaw skills.
- **Permission denied:** Run the `chmod` commands again. Data files need `600`, directories need `700`.
- **Empty data on first run:** This is normal! All data files start as empty arrays `[]`. They'll populate as you add contacts and log interactions.
