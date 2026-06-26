---
name: local-skill-installer
description: Install a local OpenClaw skill from a zip file by unzipping, validating, moving it into the active Skills directory, and verifying the result.
---

# Local Skill Installer

Use this skill when the user wants to install a local OpenClaw skill package from a zip file on the current Linux system.

## What this skill does

This skill helps install a local skill package safely.

Expected user input:
- A Linux-accessible zip path, for example:
  `/mnt/c/Users/user/Downloads/skill-vetter-1.0.0.zip`

## Rules

- Only work with local zip files.
- Prefer Linux paths, not Windows `C:\...` paths.
- Use `move`, not `copy`, to avoid duplicate files.
- Do not overwrite an existing skill folder without checking first.
- If the same skill name already exists, stop and report the conflict.
- Clean up temporary files after finishing.
- Do not run scripts inside the zip.
- Briefly report each important step.

## Steps

1. Confirm the zip file exists.
2. Create a temporary extraction directory.
3. Unzip the package into the temporary directory.
4. Inspect the extracted content.
5. Validate that it looks like an OpenClaw skill:
   - must contain `SKILL.md`
   - may also contain `_meta.json`, `assets`, `agents`, `references`
6. Determine the correct active Skills directory for this OpenClaw installation.
   - Prefer `~/.openclaw/skills/` for shared local skills if appropriate.
   - If the current workspace has a dedicated `skills/` directory and the context indicates workspace-local installation, use that instead.
7. Determine the final skill folder name.
8. If the target folder already exists:
   - do not overwrite
   - report the existing path and stop
9. Move the extracted skill folder into the Skills directory.
10. Verify the final folder and key files exist.
11. Clean up temporary files.
12. Tell the user:
   - whether installation succeeded
   - the final installed path
   - whether reload or restart is needed

## Output format

Always report:
- Source zip path
- Extracted skill folder name
- Final installed path
- Validation result
- Conflict result if any
- Whether reload/restart is recommended
