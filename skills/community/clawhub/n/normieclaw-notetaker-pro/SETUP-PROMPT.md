# NoteTaker Pro — Setup Prompt

Copy and paste this ENTIRE block into your agent's chat to install NoteTaker Pro.

---

**Paste this:**

```
I just purchased NoteTaker Pro. Please set it up for me. Here are the steps:

1. Find the skill files:
# Files are installed by clawhub install — no manual copy needed
# Files are installed by clawhub install — no manual copy needed
# Files are installed by clawhub install — no manual copy needed
# Files are installed by clawhub install — no manual copy needed

2. Read the SKILL.md file and internalize all instructions, schemas, and rules.

3. Create the data directories with secure permissions:
   mkdir -p data/notes data/exports
   chmod 700 data data/notes data/exports

4. Initialize empty data files with secure permissions:
   echo '[]' > data/notes-index.json && chmod 600 data/notes-index.json
   echo '{"tags":{}}' > data/tags-index.json && chmod 600 data/tags-index.json

5. Copy the config directory and set permissions:
# Files are installed by clawhub install — no manual copy needed
   chmod 700 config/notetaker-pro
   chmod 600 config/notetaker-pro/*

6. Copy the export script and set permissions:
   # Files are installed by clawhub install — no manual copy needed
   chmod 700 scripts/export-notes.sh

7. Verify the installation by confirming:
   - [ ] SKILL.md was read and understood
   - [ ] data/notes/ directory exists with chmod 700
   - [ ] data/notes-index.json exists and contains []
   - [ ] data/tags-index.json exists and contains {"tags":{}}
   - [ ] config/notetaker-pro/notes-config.json exists with chmod 600
   - [ ] scripts/export-notes.sh exists with chmod 700

8. Send me a confirmation message that looks like:
   "✅ NoteTaker Pro installed! Your second brain is ready. Send me a thought, paste something, or snap a photo — I'll handle the rest."
```

---

## Troubleshooting

- **"File not found"** — Make sure you extracted the skill package into your agent's skills directory. The `find` commands above will locate the files wherever they are.
- **"Permission denied"** — Run the `chmod` commands again. Directories need `700`, files need `600`.
- **"Empty search results"** — The data files are empty at first. Start capturing notes and the index builds automatically.
