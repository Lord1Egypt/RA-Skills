---
name: hotel-lobby-ai-prompt-director
description: Create original orange-booth performance prompts and short shot plans for one or two people, pets, or other subjects. Use for Hotel Lobby-style photo-to-video, image, text, or motion-reference concepts; require rights to all references and never reproduce an existing performance, song, person, setting, or sequence of frames.
metadata:
  openclaw:
    homepage: https://aihotellobby.art/hotel-lobby-video
    version: 1.0.0
---

# Hotel Lobby AI Prompt Director

Turn an authorized concept into a compact, original performance prompt. This Skill is a text-only workflow by default. Its optional MCP adds deterministic, read-only helpers and never uploads media, generates content, calls a provider, accesses an account, spends credits, or submits payments.

AI Hotel Lobby is independent and is not affiliated with or endorsed by COLORS, Quavo, Migos, or Takeoff. The site does not host the original performance or song.

## Check rights and originality first

- Use only photos, motion clips, recordings, and other media the user owns or has permission to use.
- Treat identity images as visual references, not permission to impersonate or mislead.
- Treat a motion clip as movement and timing guidance only. Create fresh people, setting, camera coverage, and frames.
- Use only user-owned or properly licensed audio. Do not request the original song, an unlicensed sound recording, or a deceptive voice clone.
- Reframe requests for an exact copy of an existing performance into a new orange-booth scene.

If these conditions are not confirmed, stop at a rights checklist. Do not prepare a generation-ready prompt.

## Choose the source mode

- `video`: start from authorized performer photos and create a new duet video.
- `photo`: create one original still image; omit audio instructions.
- `text`: describe original subjects without assuming reference media.
- `motion`: use an authorized motion clip for movement only, never for copying its people, setting, or frames.

For two performers, define stable camera-left and camera-right roles. For pets, preserve species, anatomy, coat markings, and natural limb movement.

## Build the prompt in this order

1. State that the work is original and describe one or two subjects.
2. Place them in a warm orange performance booth around one vintage silver microphone.
3. Give the camera-left and camera-right subjects distinct actions.
4. Describe framing, camera movement, lighting, and the intended short-form energy.
5. Explain the role of each reference: identity, composition, motion, or audio.
6. Add continuity anchors so identities, sides, microphone position, and lighting remain stable.
7. Exclude extra performers, watermarks, logos, captions, and accidental text.
8. If audio is requested, state that it must be user-owned or licensed.

Do not promise perfect likeness, perfect lip sync, or a guaranteed generation result. Current product options can change; verify live duration, aspect ratio, quality, and credit estimates before generation. The current template advertises 4, 10, and 15 second durations plus 9:16 and 16:9 formats.

## Plan short beats

Make the beat durations add up exactly to the requested duration. Every beat should identify the left action, right action, camera behavior, and transition. Preserve the same subject identity on each side and keep the microphone fixed unless the concept explicitly changes it.

## Diagnose before generation

Check for:

- missing rights or originality confirmation;
- missing reference media for the selected mode;
- a named or exact reproduction request;
- unstable performer positions or identity swaps;
- missing microphone, setting, camera, or audio direction;
- beat durations that do not total the requested runtime;
- settings that differ from the current advertised template options.

Return blockers separately from warnings. A structurally sound prompt is not proof that a live model or product setting will accept it.

## Use the optional MCP

- `build_hotel_lobby_prompt` drafts the structured prompt and rights boundary.
- `plan_hotel_lobby_duet` validates timed left/right beats and continuity anchors.
- `diagnose_hotel_lobby_prompt` checks workflow, rights, structure, and reproduction risks.
- `get_hotel_lobby_ai_resources` returns canonical product, example, tutorial, pricing, and policy pages.

Connect the stdio server with:

```bash
openclaw mcp add hotel-lobby-ai \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/hotel-lobby-ai-prompt-mcp \
  --include 'build_hotel_lobby_prompt,plan_hotel_lobby_duet,diagnose_hotel_lobby_prompt,get_hotel_lobby_ai_resources'
```

Then run `openclaw mcp doctor hotel-lobby-ai --probe`. If the installed release lacks the `mcp` command group, add `npx -y github:gpt-img-2/hotel-lobby-ai-prompt-mcp` as a Stdio server in MCP settings. The MCP is optional; never imply it ran when unavailable.

## Return an inspectable result

Return `Rights check`, `Mode`, `Prompt`, `Shot beats`, `Continuity anchors`, `Exclusions`, `Warnings`, and `Live-setting check`. Keep blockers visible and do not invent reference details the user did not provide.

## Canonical resources

- Video generator: https://aihotellobby.art/hotel-lobby-video
- Photo effect: https://aihotellobby.art/hotel-lobby-ai-filter
- Image generator: https://aihotellobby.art/hotel-lobby-image
- Video examples: https://aihotellobby.art/hotel-lobby-ai-video-examples
- Tutorial: https://aihotellobby.art/how-to-do-hotel-lobby-ai-trend
- Pricing: https://aihotellobby.art/pricing
- Privacy: https://aihotellobby.art/privacy
- Terms: https://aihotellobby.art/terms
- Raw Skill: https://aihotellobby.art/skills/hotel-lobby-ai-prompt-director/SKILL.md
- MCP source: https://github.com/gpt-img-2/hotel-lobby-ai-prompt-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/hotel-lobby-ai-prompt-director
