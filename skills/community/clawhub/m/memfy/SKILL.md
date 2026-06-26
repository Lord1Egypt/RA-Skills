---
name: memfy
description: Capture durable user-approved memory when the user says memfy, without storing secrets or transient chatter.
metadata:
  openclaw:
    envVars:
      - name: MEMFY_MEMORY_FILE
        required: false
        description: Optional path to the durable memory markdown file. If unset, infer the user's preferred memory file from local instructions or ask before writing.
    skillKey: memfy
    emoji: "🧠"
---

# Memfy

Use this skill when the user says `memfy`, asks you to remember something for future chats, or asks you to persist durable local context.

## Core Behavior

`memfy` is an explicit save-memory command. Treat it as permission to persist the important current-task details into the user's durable memory location.

Save only information that will help future agents avoid making the user repeat themselves:

- Stable preferences, workflows, decisions, contacts, project facts, IDs, URLs, file paths, and follow-up rules.
- Current task outcomes that future sessions should know.
- Corrections the user made that should change future behavior.
- Non-secret configuration names or environment variable names.

Do not save:

- Raw passwords, API keys, tokens, private keys, cookies, recovery codes, or full credentials.
- One-off emotional reactions, temporary drafting text, or noisy conversation.
- Sensitive personal data unless the user clearly wants it remembered and it is necessary for future work.
- Unsupported guesses. Mark uncertain facts as uncertain or do not save them.

## Workflow

1. Identify the durable memory target.
   - Prefer `MEMFY_MEMORY_FILE` if it is set.
   - Otherwise read local project or agent instructions for a memory file path.
   - If no target is discoverable, ask the user where to save memory before writing.

2. Distill the memory.
   - Write concise bullet points under a dated heading.
   - Include exact file paths, URLs, IDs, and commands only when they are useful and non-secret.
   - Summarize secrets as location pointers such as "stored in `.env` under `SERVICE_API_KEY`"; never write the raw value.

3. Write safely.
   - Append to the existing memory file unless the user explicitly asks to edit or reorganize it.
   - Preserve the file's encoding when possible.
   - Do not overwrite unrelated memory.
   - If the memory file is unreadable because of encoding, use a safe append method that does not rewrite the full file.

4. Confirm briefly.
   - Tell the user what category of memory was saved.
   - Mention any important thing deliberately not saved, especially secrets.

## Suggested Format

```markdown
## Short Topic (YYYY-MM-DD)

- Stable fact, preference, or outcome.
- Relevant path or URL: `...`
- Secret handling note: raw credentials are stored only in `.env`, not in memory.
```

## Quality Bar

A good memfy entry should be:

- Short enough to scan quickly.
- Specific enough for a future agent to act on.
- Free of raw secrets.
- Written in the user's own durable context, not only in the chat.

