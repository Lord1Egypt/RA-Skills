---
name: howtoletmyagent_installer
description: "Install companion OpenClaw skills from howtoletmyagent.xyz article URLs or skill manifests."
---

# Howtoletmyagent Installer

Use this skill when the user wants to install or learn a companion skill from a Howtoletmyagent article.

Accepted inputs:

- An article URL like https://howtoletmyagent.xyz/articles/<slug>
- A manifest URL like https://howtoletmyagent.xyz/api/skills/<slug>
- A plain request such as "learn the skill from this page" when the article URL is present in context

Required workflow:

1. Verify that the source URL belongs to https://howtoletmyagent.xyz or another explicitly approved preview host.
2. Resolve the manifest URL:
   - article URL -> /api/skills/<slug>
   - manifest URL -> use it directly
3. Fetch the manifest JSON.
4. Explain what will be installed and ask for approval before writing files or running install commands.
5. If the manifest says the source is `clawhub`, prefer the provided install command.
6. If a ClawHub install is unavailable or fails, create a local workspace skill folder and write the manifest files exactly as provided.
7. After install, tell the user to start a new session with `/new` or restart the gateway so OpenClaw reloads the skill.

Safety rules:

- Only trust manifests from https://howtoletmyagent.xyz unless the user explicitly approves another domain.
- Never execute arbitrary code from the manifest. This manifest is for skill files, not shell scripts.
- Show the target install path before writing files.
- If a manifest looks malformed or unsafe, stop and explain the issue instead of guessing.

Implementation notes:

- Prefer using browser or web-fetch tools to read the manifest.
- If a CLI install is approved, use the exact command supplied by the manifest.
- If you must install from files, write each file under `skills/<skill-name>/` using the manifest `files` array.

Success condition:

- The requested companion skill is installed.
- The user gets the exact prompt they can use next to trigger it.
