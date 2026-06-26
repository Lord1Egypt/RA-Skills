---
name: go-next-move
description: Analyze a Go/Weiqi position from an image or board state, use KataGo to recommend the next move at beginner, intermediate, or advanced playing strength. Use when the user asks where black or white should play next, wants a move matched to an opponent's level, or wants AI-assisted handicap-like balancing without changing the board.
---

# Go Next Move

## Current Scope

This skill is being built as a separate move-selection layer from `count-go-black-stones`.

The intended workflow is:

1. Convert a board photo into a 19x19 position.
2. Ask the user or infer who is to move when possible.
3. Send the position to KataGo using Chinese rules and a fixed visit budget.
4. Return a recommended move matched to the requested playing-strength level.
5. Include candidate moves and enough analysis data to explain or audit the choice.
6. For no-capture continuation, preserve the original recognized board and add numbered AI/user move overlays before asking for the next move.

## Local KataGo Defaults

KataGo is installed through Homebrew and verified on this machine:

```bash
katago version
```

Expected important line:

```text
Using Metal backend
```

Use this project config after KataGo's bundled GTP config:

```bash
katago gtp \
  -model /opt/homebrew/share/katago/g170e-b20c256x2-s5303129600-d1228401921.bin.gz \
  -config /opt/homebrew/share/katago/configs/gtp_example.cfg \
  -config katago/gtp_skill.cfg
```

Set komi through GTP, not the config file:

```gtp
boardsize 19
komi 7.5
clear_board
genmove b
```

For scripted next-move analysis, prefer the JSON analysis engine:

```bash
python3 scripts/next_move.py /path/to/board.jpg \
  --input image \
  --side-to-move black \
  --level intermediate \
  --visits 400 \
  --overlay /tmp/go-next-overlay.jpg \
  --source-overlay /tmp/go-source-overlay.jpg \
  --source-result-image /tmp/go-source-result.jpg \
  --result-image /tmp/go-next-result.jpg
```

For photo input, the default user-facing image should be the combined original-photo result. It marks existing white stones with black `W`, existing black stones with white `B`, and the recommended move as a numbered stone so the user can compare the recognition against the real board at a glance. Use `--result-image` only when you explicitly want the clean warped-board rendering with a red ring/dot.

Use `--source-overlay` for user-facing recognition verification. It marks detected stones on the original photo. `--overlay` is a warped/cropped board view for debugging and may not look like the original photo.

For photo input, the tool should surface the combined original-photo result by default. It is the verification/result image: existing white stones are marked with black `W`, existing black stones are marked with white `B`, and the recommended move is drawn as a new stone with the numbered label `1`. This makes recognition mistakes easier to spot and leaves room for future multi-step labels. Use `--result-image` only when you explicitly want the clean warped-board rendering.

For no-capture continuation, pass confirmed post-photo moves with repeatable `--move-overlay source:color:move:label` arguments:

```bash
python3 scripts/next_move.py /path/to/board.jpg \
  --input image \
  --side-to-move white \
  --level intermediate \
  --move-overlay ai:W:Q4:1 \
  --move-overlay user:B:D16:2 \
  --source-result-image /tmp/go-step-3.jpg
```

This preserves the original recognized board in `base_board_ascii`, stores confirmed post-photo moves in `move_overlays`, sends the composed board in `board_ascii` to KataGo, and draws all confirmed moves plus the new recommendation in `display_move_overlays`. Do not use this mode after captures; re-shoot/reset the board and analyze one move from the new photo.

Coordinates default to standard GTP letters, which skip `I`. When the user's physical board uses sequential `A-S` letters including `I`, pass `--coordinate-style sequential`. Use that same style for every `--move-overlay`; the returned recommendation, candidate moves, PVs, explanations, and numbered overlays will use it consistently. KataGo communication remains GTP internally.

For an already recognized board:

```bash
python3 scripts/next_move.py /path/to/board_ascii.txt \
  --input ascii \
  --side-to-move white \
  --level beginner
```

`board_ascii` is 19 rows of 19 characters:

- `X` or `B`: black stone
- `O` or `W`: white stone
- `.`: empty point

The script returns JSON containing:

- `board_ascii`
- `coordinate_style`
- `base_board_ascii`
- `move_overlays`
- `display_move_overlays`
- `recommendation`
- `reason`
- `recommendations_by_level`
- `candidate_moves`
- `root_info`
- optional `result_image` when `--result-image` is passed
- default `source_result_image` for photo input, or optional `source_result_image` when `--source-result-image` is passed explicitly
- optional `recognition` metadata when input is an image

## HTTP Interaction Mode (optional, faster than LLM round trips)

This is an *additional* entry point. The LLM/CLI workflow above is unchanged and
still fully supported. When the user wants to iterate quickly without a slow LLM
round trip for every photo, serve a web page behind a public tunnel and hand
them a link. The page lets them pick the side to move (black/white) and playing
strength (beginner/intermediate/advanced), upload a board photo, and get the
recommended-move image back over HTTP. The page calls the same
`scripts/next_move.py` under the hood.

The design has two parts:

1. A **resident HTTP service** (`scripts/launch_skill_server.py`). Start it once;
   it is lightweight and stays up. It serves the page + `/api/analyze`, keeps a
   Cloudflare quick tunnel alive, and writes the current public tunnel URL to a
   state file (`~/.go-next-move/tunnel_url`). If the tunnel reconnects with a new
   hostname, the file is updated.
2. A small **one-shot link minter** (`scripts/mint_link.py`). This is what the
   agent runs whenever the user needs a link. It signs a fresh token (default
   5 hours) with the shared secret, reads the current tunnel URL from the state
   file, and prints `https://<tunnel-host>/?token=<token>`. The token changes on
   every call; the tunnel URL is whatever the resident service currently has.

Start the resident service (once, on the host where KataGo lives):

```bash
python3 scripts/launch_skill_server.py
```

Mint a link to hand to the user (fast, does not start anything):

```bash
python3 scripts/mint_link.py
```

Operational rules:

- Tokens expire after the TTL (default 5 hours). When a link expires, just run `mint_link.py` again and send the new link.
- The tunnel URL can change when the resident service / cloudflared restarts. `mint_link.py` always reads the current URL, so a freshly minted link is always correct.
- To revoke every outstanding link before expiry, run `mint_link.py --rotate-secret` (rotates the shared secret).
- The token is a stateless HMAC (see `scripts/skill_token.py`); the server validates it without storing per-token state. The secret persists at `~/.go-next-move/secret` (override with `GO_NEXT_MOVE_SECRET` or `--secret-path`).
- Requires `cloudflared` on PATH for the default tunnel (`brew install cloudflared`). KataGo must still be installed locally because the server shells out to `next_move.py`. Use `--no-tunnel` for LAN/testing.

### OpenClaw sandbox deployment

When the agent runs inside an OpenClaw Docker sandbox, KataGo and `cloudflared`
live on the host, not in the sandbox. Follow the same host-bridge pattern as the
existing `~/.openclaw/bin/go-next-move-host`:

1. Start the resident service on the host once. Either run `python3 scripts/launch_skill_server.py` manually / via launchd, or install `scripts/go-next-move-serve-host.example` to `~/.openclaw/bin/go-next-move-serve` (it launches the service detached so it survives the elevated call).
2. Install `scripts/go-next-move-link-host.example` to `~/.openclaw/bin/go-next-move-link` and add its absolute path to the agent's allowlist in `~/.openclaw/exec-approvals.json` (same as `go-next-move-host`).
3. When the user needs a link, the agent runs `go-next-move-link` elevated (`exec` with `elevated: true`); it prints a fresh `https://<tunnel-host>/?token=<token>` to hand over. Pass `--rotate-secret` to revoke old links.

Both wrappers hardcode the host's absolute Python/KataGo/model paths because
elevated `system.run` strips `PATH`/`PYTHON*` from the environment.

## Playing-Strength Levels

The level controls move strength, not explanation depth.

- Beginner: choose a plausible but intentionally softer move from KataGo's candidates. It should usually be playable, but may lose several points compared with the best move.
- Intermediate: choose a solid near-top candidate. It should be close to the best move but not always the engine's first choice.
- Advanced: choose KataGo's top searched candidate.

Use `--level all` when the caller wants all three recommendations at once. Use `recommendation` for the selected level and `recommendations_by_level` to compare the three outputs.

The current script chooses levels by candidate rank plus score/winrate loss from KataGo's best move. These thresholds are a practical first pass, not calibrated ranks. The next improvement should tune them with real game examples.

## User-Facing Response

When answering a user, include:

1. The recommended coordinate.
2. The generated `source_result_image` for photo input, or `result_image` for ASCII input.
3. Why this move was chosen, using `reason.summary` plus the bullet-like items in `reason.explanation`.
4. Technical parameters from `reason.technical_parameters`, especially winrate, score lead, visits, score loss vs best, and PV.
5. Candidate comparison from `reason.comparison_candidates` when there are meaningful alternatives.
6. The `recognition.source_overlay` image when available.
7. A recognition caveat if the rendered board or source overlay does not match the real photo.

Do not only return the coordinate. The user-facing answer should always include enough engine data to audit the recommendation: winrate, score lead, visits, and whether the chosen move is the top KataGo move or a deliberately softer level-based move.

Do not invent tactical explanations that are not supported by KataGo data or visible board context. If recognition looks wrong, say the recommendation is not reliable until the board is corrected.

## Notes

- Do not rely on the language model alone for high-strength move choice.
- Use KataGo for candidate moves; use the requested level to choose the playing strength of the move.
- A board photo usually does not prove whose turn it is. Ask or require the side to move unless the surrounding context makes it clear.
- Use `--move-overlay` only for no-capture continuation. If there are captures, ko/state ambiguity, or an overlay point is occupied, ask the user to re-shoot/reset the board and analyze one move.
- If board recognition is uncertain, surface the uncertainty before giving a move recommendation.
- White-stone classification includes center low-saturation and center/ring contrast checks to reduce false positives from glare or bright wood grain.
