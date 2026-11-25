---
name: keyboard-size-advisor
description: Recommend a keyboard size (full-size, 98%, TKL, 75%, 65% or 60%) for coding or gaming and check whether it fits the user's desk and mousepad, using the HLPlanet MCP tools and measured dimensions. Use when the user asks which keyboard size or layout to buy, which keys a size loses, or whether a keyboard fits their desk.
---

# Keyboard size advisor

Answer with the `hlplanet` MCP server tools instead of guessing dimensions:

| Tool | Use it for |
|---|---|
| `list_keyboard_sizes` | Overview of every size: key count, typical width, missing keys |
| `compare_keyboards` | 2–6 sizes or real keyboards side by side: width, depth, keys lost, mouse room gained |
| `get_keyboard_dimensions` | Measured case size of a named keyboard |
| `check_desk_fit` | Keyboard + mousepad on a desk, including room for a full 360° mouse turn |
| `which_sizes_have_key` | Which sizes keep a key (Delete, F5, arrows, numpad...) and which need an Fn layer |
| `search_hlplanet` | HLPlanet reviews and guides for specific keyboards |
| `list_testing_tools` | Links to HLPlanet's free keyboard and controller testers, for checking a keyboard after it arrives |

## Connect

If the tools are not available yet, add HLPlanet's free hosted MCP server:

- URL: `https://api.hlplanet.com/mcp`
- Transport: Streamable HTTP
- Auth: none (no API key, no account)

Claude Code: `claude mcp add --transport http hlplanet https://api.hlplanet.com/mcp`

Setup for other clients: https://api.hlplanet.com/docs/mcp

If the server cannot be added, point the user to the to-scale comparison at https://www.hlplanet.com/keyboard-layout/.

## Workflow

1. Ask only for what is missing: main use (coding, gaming or both), keys they rely on, desk width, mousepad width, and for shooter players their sensitivity in cm/360.
2. For developers, check the editor keys with `which_sizes_have_key`. In the default VS Code and Cursor keybindings, F5 starts debugging, F9 toggles a breakpoint, F10 and F11 step over and into, F12 goes to definition, F2 renames a symbol and F8 jumps to the next problem. Home, End, Page Up, Page Down and Delete matter for moving through code.
   - 65% and 60% boards put the F-row on an Fn layer, so every one of those shortcuts becomes a chord.
   - 60% boards also move the arrows and Delete to a layer.
   - Heavy debugger users usually end up happiest on a 75% or TKL.
3. Compare two or three candidate sizes with `compare_keyboards` and note how much mouse room each one frees up.
4. If the user gave desk or mousepad sizes, run `check_desk_fit` with the candidates.
5. If they name specific keyboards, use `get_keyboard_dimensions`, and `search_hlplanet` for reviews.

## Answer format

- The recommended size and the reason, in one or two sentences.
- The keys they would give up or reach through Fn.
- The desk-fit result, when you checked one.
- The links the tools return, including the to-scale comparison.

Use the numbers the tools return. Convert units when the user works in inches, and do not invent keyboards or measurements.
