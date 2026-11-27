---
name: play-dispersed-3d
description: "Play the free overlanding game Dispersed 3D with your AI assistant: it makes the camping calls, you watch. Use when someone says Dispersed 3D, wants to play a camping game with their AI, asks to send my AI to camp, take an AI seat, or make a Call. Picks the smallest way in that fits what the assistant can do (one Call with no browser, a seat by links, or a browser tab), plays by the game's own menu, gives each reason in a line, and hands the wheel back whenever the person takes it."
license: MIT-0. Credit is welcome, never required.
compatibility: Needs internet access to https://momatio.com. scripts/call.py needs Python 3.8 or newer and nothing else. A full trip needs a browser tab the person keeps on screen; one Call needs nothing. Works with the davelalande.com MCP connector (tool one_call) when present.
metadata:
  author: Dave Lalande (American Adventurer)
  version: "1.0.0"
  home: https://tinycorp.ai/install
---

# Play Dispersed 3D with your agent

Dispersed 3D is a free browser game about a four-night overlanding trip on real public land. This skill helps an assistant play it with its person watching. It holds manners and the way in, not rules: the game changes with each release, so the game is the single source.

## Step 1: read the game's own page, live

Fetch `https://momatio.com/dispersed3d/llms.txt` before you do anything else. If it disagrees with this skill, the page wins. In play, `state().commands` (the menu) wins over anything written here.

Do not quote a price, a token cost or a turn count from memory. Today's cost note is on `https://momatio.com/dispersed3d/agent/`; send the person there.

## Step 2: offer the smallest thing first

1. **One Call** (about 30 seconds, no browser). The connector tool `one_call`, or `python scripts/call.py today`, gives one decision from a checked run: a situation line and a numbered menu, never the checked AI's pick. Pick one move, say your reason in a line, then make the reveal link with `python scripts/call.py link --challenge C --run R --at N --pick KEY --by claude`. Send the person that link. Its shape:
   `https://momatio.com/dispersed3d/?watch=<challenge>/<run>&at=<n>&call=1#c=<key>&by=<name>`
   `by` is one of: claude, chatgpt, grokbot, gemini, perplexity, copilot, other. Use the one that is your real name.
2. **A seat by links** (you can follow links, not run a browser). Ask the person to go to `https://momatio.com/dispersed3d/agent/`, which makes a seat and gives you one link. Read the plain-text turn, answer by following the move link with a number and a short reason. One move per turn. The person keeps their game tab on screen.
3. **A browser** (you control one). Load `https://momatio.com/dispersed3d/?ai=1` and press Play. Use `D3.ai.state()` and `D3.ai.act({...cmd, why})`, or the page tools `dispersed3d_state`, `dispersed3d_menu`, `dispersed3d_move` and `dispersed3d_pack`.

Exact links and the steps for each way are in [references/ways-in.md](references/ways-in.md). If the person has no preference, start with the Call.

## Play like a careful overlander

Light, gas back to town, water, the weather and the fire rule: each turn, read those from the game, then choose. Scout more than one camp, look on foot, turn the engine off and listen, level the truck, put a fire dead out, keep to mapped roads. A camp marked Free is the one you want. The short list is in [references/careful-overlander.md](references/careful-overlander.md).

Say each reason in one or two plain sentences, as you go. Short, because every word is a token someone pays for.

## Manners and fair play

- If `driver` is "human", the person has the wheel. Wait and watch. You cannot take it back, and you should not try.
- One run per trip. Only moves the menu offers. Never change the game's state or its storage.
- Name your real model.
- Ask the person before pressing "Submit to the leaderboard". On a no, send nothing.
- Never claim a ranking. At the end, quote only the end card.
- If `state()` does not hold a number, say you do not know it.
- A camp fact comes from the game or the connector, never from memory.
- Never plan or describe snow or winter. The trip is spring, summer and fall.
- Do not argue with the person. Do not say a place is open, legal, passable or safe.

## What to say when you finish

Tell the person how it went in the game's own words from the end card, then offer a second Call or another trip. Nothing else.
