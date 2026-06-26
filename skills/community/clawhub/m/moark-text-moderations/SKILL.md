---
name: moark-text-moderations
description: Perform text review on user-specified input text that may be inappropriate or offensive.
metadata:
  {
    "openclaw":
      {
        "emoji":"🛡️",
        "requires": { "env": ["GITEEAI_API_KEY"]},
        "primaryEnv": "GITEEAI_API_KEY"
      }
  }
---

# Text Moderation
This skill allows users to perform text review on user-specified input text that may be inappropriate or offensive using an external GITEE AI API.

## Usage

Ensure you have installed the required dependencies (`pip install openai`). Use the bundled script to perform text moderation.

```bash
python {baseDir}/scripts/perform_text_moderation.py --text "User-specified input text" --api-key YOUR_API_KEY
```

## Options
No additional parameters are required for this skill.

## Workflow

1. Execute the perform_text_moderation.py script with the parameters from the user.
2. Parse the script output and find the line starting with `MODERATION_RESULT:`.
3. Extract the moderation result from that line (format: `MODERATION_RESULT: ...`).
4. Display the moderation result to the user using markdown syntax: `🛡️[Moderation Result]`

## Notes
- If GITEEAI_API_KEY is none, you should remind user to provide --api-key argument
- You should not only return the moderation result but also provide a brief summary of the moderation result based on the user's input text.
- When you add prompt, you should honestly repeat the requirements from user without any additional imaginations.
- The script prints `MODERATION_RESULT:` in the output - extract this result and display it using markdown image syntax:`🛡️[Moderation Result]`.
- Always look for the line starting with `MODERATION_RESULT:` in the script output.