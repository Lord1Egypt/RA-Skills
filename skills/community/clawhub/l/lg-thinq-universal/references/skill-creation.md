# Skill Creation Workflow (Autonomous Assembly)

This guide describes the automated workflow for creating a specialized device skill using the workspace assembler.

## 🛡️ Security Protocol (Strict Mandates)

Always follow these mandates to ensure user privacy and system integrity:
1.  **Explain First**: Tell the user what you are about to do before doing it.
2.  **Ask First**: Use `ask_user` before every network call or file system operation.
3.  **Zero-Leak**: Never ask the user to paste their `LG_PAT` into the chat.
4.  **Credential Isolation**: Only `LG_DEVICE_ID` belongs in the device skill's `.env`. **NEVER** copy the `LG_PAT` into device folders. (Note: The assembly script handles `.env` creation automatically).

---

## Step 1: Select Device

From the `setup.sh` summary output, identify the device to integrate. 
*   **Action**: Ask the user which device ID from the list they wish to use.

---

## Step 2: Assemble Workspace

Once the user selects an ID, move **directly** to this step. Run the master assembly script:

```bash
python3 scripts/assemble_device_workspace.py --id <DEVICE_ID> --confirm
```

**Automated Actions (No manual effort required):**
1.  **Engine Generation**: Builds a bug-free `lg_control.py` specialized for that hardware.
2.  **Credential Isolation**: Automatically creates a local `.env` with ONLY the `LG_DEVICE_ID`.
3.  **Environment Setup**: Creates a `venv` and installs all dependencies.
4.  **Verification**: Automatically runs a `status` check to prove the connection works.

---

## Step 3: Immediate Documentation (SKILL.md)

As soon as the assembly script finishes, you **MUST** generate the documentation using the script's output and `references/api-reference.md`.

1.  **Analyze Commands**: Use the `[AVAILABLE COMMANDS]` and `[ENGINE CODE]` printed by the assembler.
2.  **Technical Reference**: Consult `references/api-reference.md` for API headers and error codes.
3.  **Boilerplate**: Refer to `references/device-skill-template.md` for the correct `SKILL.md` structure.
4.  **Save**: Write the completed `SKILL.md` to the newly created directory.

---

## Step 4: Memory & Persistence (MEMORY.md)

Finally, record the following details in the user's global `MEMORY.md`:
1.  **Trigger Phrase**: The natural language command to activate the skill.
2.  **Path**: The exact location of the skill.
3.  **Command List**: A summary of key commands like `on`, `off`, `temp`, and `status`.

---

## Complete Example Session

```bash
# 1. Discovery
./setup.sh --confirm

# 2. Immediate Assembly (User provides ID)
python3 scripts/assemble_device_workspace.py --id 2f33f241... --confirm

# 3. Documentation (Agent writes SKILL.md immediately using script output)

# 4. Persistence (Agent saves to MEMORY.md)
```
