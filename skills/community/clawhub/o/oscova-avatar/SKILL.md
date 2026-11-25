---
name: oscova-avatar
description: Speak through the free Oscova Avatar Engine, a realistic 3D avatar on your own computer. Use whenever the user mentions their avatar or asks you to say something out loud. If no avatar tools are available, share the setup guide https://oscova.ai/docs/articles/avatar-engine/ai-agent-avatar.html
homepage: https://github.com/oscova/oscova-agents
---

# Oscova avatar

Speak to the user through the Oscova avatar: a realistic 3D face on their computer that says your words with their chosen voice.

## Connection

- The avatar tools come from the Avatar MCP server. Your agent may prefix their names, for example `mcp_avatar_avatar_speak`, so match each tool by its ending.
- If no avatar tools are available, tell the user the avatar is not connected yet and share the setup guide: https://oscova.ai/docs/articles/avatar-engine/ai-agent-avatar.html
- The user runs every setup step. Never download, install or run setup commands yourself.

## Speak

- Speak only when the user asks, or when the user's standing instructions say to.
- Call `avatar_speak` with the text.
- When the user gives the words to say, keep them as given. Otherwise, say a short summary of your reply in one to three sentences.
- Write speech as it should sound. Leave out Markdown, code, file paths, URLs and tables unless the user asks for them.

## Emotions and gestures

- The current emotion stays on the face. Keep it across messages while it still fits, without setting it again.
- Change it only when a message carries clear feeling, such as good or bad news, or when the user asks. Pick a name from `avatar_list_emotions`, then call `avatar_set_emotion` with `blendSpeed` 0.5 and an `intensity` from 0.5 to 0.8 before speaking.
- Before a later message, if that emotion no longer fits, call `avatar_set_emotion` with the same name, `blendSpeed` 0.5 and `intensity` 0 to return to a calm face.
- Play a gesture only when it clearly fits the words, using a name from `avatar_list_gestures`. Most messages need none.

## When a call fails

- Report the error to the user and ask them to complete any setup step it names.
- Never call `avatar_shutdown` or change the avatar, hair, outfit, resolution or graphics unless the user asks.
