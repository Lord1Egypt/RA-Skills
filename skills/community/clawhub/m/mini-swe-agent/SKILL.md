# mini-swe-agent

Run complex software engineering tasks autonomously using the mini-swe-agent CLI.

## Description
Use this skill when the user asks to fix a bug, implement a feature, or resolve a GitHub issue that requires end-to-end codebase exploration and editing. This acts as a "sub-contractor" to do the heavy lifting for complex tasks.

## Usage
When a complex coding task is requested, formulate a concise, descriptive problem statement and run the `mini` CLI using a bash tool.

```bash
mini --yolo "Fix the authentication logic in /src/auth.py to ensure tokens expire after 3600 seconds"
Rules
Autonomy: Always use the --yolo flag so the agent runs autonomously without waiting for user input.

Formatting: Escape double quotes inside the problem statement if necessary.

Verification: Monitor the output. Once mini finishes, verify the changes if requested by the user.

Scope Limitation: Do NOT use this for simple one-line text replacements or minor typo fixes. Use standard file editing tools for those to save time and compute.


---

### 2. How to Build/Install It

Instead of creating it manually, you can run this single command in your terminal. It will create the necessary OpenClaw skills directory (if it doesn't already exist) and write the `SKILL.md` file directly into it.

```bash
mkdir -p ~/.openclaw/skills/mini-swe-agent && cat << 'EOF' > ~/.openclaw/skills/mini-swe-agent/SKILL.md
# mini-swe-agent

Run complex software engineering tasks autonomously using the mini-swe-agent CLI.

## Description
Use this skill when the user asks to fix a bug, implement a feature, or resolve a GitHub issue that requires end-to-end codebase exploration and editing. This acts as a "sub-contractor" to do the heavy lifting for complex tasks.

## Usage
When a complex coding task is requested, formulate a concise, descriptive problem statement and run the `mini` CLI using a bash tool.

` ` `bash
mini --yolo "Fix the authentication logic in /src/auth.py to ensure tokens expire after 3600 seconds"
` ` `

## Rules
* **Autonomy:** Always use the `--yolo` flag so the agent runs autonomously without waiting for user input.
* **Formatting:** Escape double quotes inside the problem statement if necessary.
* **Verification:** Monitor the output. Once `mini` finishes, verify the changes if requested by the user.
* **Scope Limitation:** Do NOT use this for simple one-line text replacements or minor typo fixes. Use standard file editing tools for those to save time and compute.
EOF