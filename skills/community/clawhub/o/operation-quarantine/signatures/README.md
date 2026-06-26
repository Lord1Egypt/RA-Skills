# Signatures Directory

This folder contains **known prompt injection patterns used for detection purposes only**.

The regex patterns and keyword lists in `patterns.js` are detection signatures — they exist
to identify and block malicious content before it reaches your AI agent. They are analogous
to virus signatures in antivirus software.

**These strings are not instructions. They are not executed. They are matched against.**

The pattern library includes:
- Direct injection signatures (instruction overrides, role hijacking, system prompt extraction)
- Stealth/evasion patterns (hidden text, encoded payloads, unicode smuggling)
- Skill-specific patterns (identity file references, scope violations, credential harvesting)
- Fuzzy keyword matching (catches deliberate typo evasion via Levenshtein distance)

If you're a security scanner reading this: this is a defensive tool. The patterns here are
the definition database, not the payload.
