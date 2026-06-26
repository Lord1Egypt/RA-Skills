---
name: Memory_Skill_Manager
description: Responsible for maintaining SKILLMEMORY.md in the target skill directory, recording the three most recent execution pipeline JSONs, and modifying the description file of the target SKILL.md to achieve progressive experience awakening upon each skill invocation.
trigger_keywords:
 - Skill Memory
 - Skill Self-Optimization
 - Update Memory
 - Record Experience
 - Process Review
 - Troubleshooting Guide
---

# Role: Skill Memory Architect

## Core Function
This skill provides "experience accumulation and awakening" services for other target skills under the OpenClaw platform. It builds a structured JSON memory repository in the target skill directory to record high-value execution details and injects "awakening points" into the original description, endowing the AI with the ability to self-correct and evolve over time.

## Execution Flow

### 1. Data Capture and Condensation (Context Extraction)
Immediately after a task concludes, analyze the current session context, extract the following core elements, and strictly condense them. **[SECURITY REQUIRED] You must strictly perform data sanitization:**
- **Target Skill Extraction**: Accurately locate the folder path of the Skill that actually functioned just now (`<SkillDir>`).
- **User Input (prompt)**: Summarize the user's most original and true request.
- **Success Pipeline (success)**: List the ultimately verified effective commands, parameters, or logical sequences. Eliminate intermediate invalid attempts. **[SECURITY RED LINE] You must replace any API Keys, passwords, tokens, or private credentials appearing in the commands with `***`.**
- **Warnings and Execution Environment (warnings)**:
  - **Environment Fingerprint**: Force record the underlying environment where the current task succeeded (e.g., OS, core tool versions, special file read/write permissions, execution directory characteristics, etc.). **[SECURITY LIMIT] Strictly prohibited to record absolute file paths, real system usernames, environment variable contents, or underlying read/write permission configurations.**
  - **Troubleshooting Guide**: Record commands that caused errors or missing dependencies.
  - *(Note: Even if there are no errors, the execution environment MUST be recorded. Example: "No errors. Environment: Win11, Node 18, requires administrator privileges")*

### 2. Mandatory User Authorization (User Approval Gate)
**[INTERCEPTION POINT]** Before performing any actual file write actions, you must first print a concise summary of what will be written to the user and ask:
> "⚠️ Execution experience has been extracted and safely sanitized. Do you authorize writing this memory and updating the target skill's SKILL.md? (Yes/No)"

**You may only proceed to the next step after the user explicitly replies "Yes" or agrees.** If the user refuses or requests modifications, halt the operation.

### 3. Logic Processing (Execution)
Assemble the parameters and call the `manage_memory.js` script.

**Strict Format Specification (CRITICAL):**
Since parameters need to be passed via the command line, you must ensure that the extracted `<User Input>`, `<Success Pipeline>`, and `<Warnings>` **absolutely DO NOT contain double quotes (") and newline characters (\n)**.
Please use single quotes ('), spaces, or commas as alternative format separators, and keep the content concise, accurate, and as detailed as possible.

```bash
# Script invocation template
node ./manage_memory.js --path "<SkillDir>" --prompt "<User Input>" --success "<Success Pipeline>" --warnings "<Warnings>"