---
name: go-next-move
description: 从围棋/Weiqi 棋盘照片或文本棋盘分析当前局面，调用本地 KataGo 按初级、中级、高级强度推荐下一手。适用于用户询问黑棋或白棋下一手应下哪里、希望按对手水平选择落点，或想在不改变棋盘的情况下获得更均衡的 AI 辅助建议。
version: 0.1.2
metadata: {"openclaw":{"requires":{"bins":["python3","katago"]}}}
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

## 安装与数据边界

此 Skill 需要 Python 3.10 或更高版本。安装已锁定版本的 Python 依赖：

```bash
python3 -m pip install -r {baseDir}/requirements.txt
```

这个 Skill 只在本机运行：读取用户明确指定的棋盘图片或文本，启动本地 `katago` 子进程，并只向用户指定的结果路径、系统临时目录或本机识别标注目录写入文件。它不调用 H5、微信、飞书或其他远程 API，也不读取账号凭据或保存用户身份、完整分析历史。

普通图片识别只使用本地 OpenCV。只有用户明确表示识别不准确时，才允许宿主智能体直接用自身视觉 LLM 复核原图；Skill 不得为此再调用 `codex exec` 或其他嵌套 LLM。复核产生的候选棋盘、原 OpenCV 棋盘和差异点会作为本地候选标注保存，默认目录为 `~/.go-next-move/recognition-labels`，可用 `GO_NEXT_MOVE_RECOGNITION_LABEL_DIR` 或 `--recognition-label-dir` 修改。候选标注不是人工确认的 ground truth。

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
  -config {baseDir}/config/gtp_skill.cfg
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
python3 {baseDir}/scripts/next_move.py /path/to/board.jpg \
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

For no-capture continuation, pass confirmed post-photo moves with repeatable `--move-overlay source:color:move:label` arguments:

```bash
python3 {baseDir}/scripts/next_move.py /path/to/board.jpg \
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
python3 {baseDir}/scripts/next_move.py /path/to/board_ascii.txt \
  --input ascii \
  --side-to-move white \
  --level beginner
```

## 用户认为识别错误时的重试

仅当用户明确指出识别结果与真实棋盘不符时，使用下面的纠错流程：

1. 宿主智能体直接查看用户的原始棋盘图片，逐一复核 19×19 共 361 个交叉点。不要调用本地 Codex CLI，也不要让语言模型代替 KataGo 选择下一手。
2. 生成严格的 19 行 `board_ascii`：每行 19 个字符，`X` 为黑子、`O` 为白子、`.` 为空点；从照片上边缘到下边缘排列，不得把待推荐落点写进棋盘。
3. 将这 19 行写入系统临时文件，然后以原始图片为输入，通过 `--board-override-file` 传给脚本。脚本会严格校验数组、保留原图的棋盘几何、用修正棋盘调用 KataGo、生成修正后的原图结果，并保存本地候选标注。

```bash
python3 {baseDir}/scripts/next_move.py /path/to/original-board.jpg \
  --input image \
  --side-to-move black \
  --level intermediate \
  --board-override-file /tmp/go-agent-board.txt \
  --source-result-image /tmp/go-agent-corrected-result.jpg
```

如需指定标注库目录，再加：

```bash
--recognition-label-dir /path/to/recognition-labels
```

返回 JSON 中的 `recognition_retry` 包含 `detector_board_ascii`、智能体提供的 `board_ascii`、`changed_points`、`label_id` 和 `label_path`。向用户展示修正后的结果图，并明确这是 LLM 候选标注；若图上棋子仍与实物不符，不要宣称修正成功，也不要采纳该次 KataGo 推荐。

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
- optional `recognition_retry` metadata when `--board-override-file` is used

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
- In the Skill entry point, recognition retry uses the current host agent's visual LLM directly. Never spawn a nested Codex process for this path.
- White-stone classification includes center low-saturation and center/ring contrast checks to reduce false positives from glare or bright wood grain.
