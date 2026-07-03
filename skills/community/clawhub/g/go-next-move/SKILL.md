---
name: go-next-move
description: 从围棋/Weiqi 棋盘照片或文本棋盘分析当前局面，调用本地 KataGo 按初级、中级、高级强度推荐下一手。适用于用户询问黑棋或白棋下一手应下哪里、希望按对手水平选择落点，或想在不改变棋盘的情况下获得更均衡的 AI 辅助建议。
---

# 围棋下一手推荐

## 当前范围

这个 skill 是独立于 `count-go-black-stones` 的围棋落点推荐层。

预期流程：

1. 将棋盘照片转换成 19 路局面。
2. 在可能时询问或推断轮到黑棋还是白棋行棋。
3. 使用中国规则和固定访问数预算，将局面发送给 KataGo。
4. 根据用户请求的落子强度返回推荐手。
5. 附带候选手和足够的分析数据，方便解释或复核选择。
6. 对于无提子的连续推演，保留原始识别棋盘，并在询问下一手前叠加带编号的 AI/用户落子。

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
