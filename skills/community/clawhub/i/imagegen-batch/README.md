# imagegen-batch

> 用 ImageGen 等文生图工具**安全地批量生成多张图片**。把「防覆盖 / 避水印 / 防塌脸」这三件事的处理顺序和判断标准固定下来。

## Features

- **防覆盖：唯一前缀 + run 目录 + manifest.jsonl** —— 工具文件名是「prompt **前 30 字符** + 秒级时间戳」，同前缀 + 同一秒 = 静默互相覆盖，所以唯一标记必须落在前 30 字内。一次批量一个带 uuid 的 run 目录；生成时可直接把 `output_dir` 指进去（2026-11-09 实测已生效，仍要 `ls` 复核），再改名、追加 manifest。**文件名固定 `NN-<prompt摘要>.png`**，摘要取 prompt 开头的中文场景词，不许只留 uuid。
- **量水印：自动优先，人工兜底** —— 右下角 AI 水印优先用 `--auto-crop` 自动量上沿；量不到（极淡水印实测存在）时脚本**仍按尺寸经验值裁**并打印 `FALLBACK`，再退回「放大刻度 + `max` 突变 250+」的人工验真。**测不到 ≠ 没有水印**，绝不跳过裁切。
- **失败退避 + 重出上限** —— 没落盘的失败按 5/15/45s 重发、最多 3 次；出图但不达标的重出，单张默认最多 4 版（用户可指定），到上限交付最不坏的一版并附未达标清单。
- **留白相框可选** —— prompt 里写「四周留白」模型基本不遵守，要留白边只能用 `scripts/add_frame.py` 后期加。**默认不加框**，用户明确要求时才传 `--frame`；要加就用 `--line 0`（纯留白、不画黑线框）。
- **人物「标识包」防塌脸** —— 同组图里每个角色固定五个维度（脸型骨相 / 五官 / 发型 / 体态 / 标志物），跨图复用同一套措辞。只写「一个方脸一个瘦脸」会塌成同一张脸。
- **风格库** —— 已命名 `白纸速写`（`paper-sketch`）、`水墨文艺风`（`ink-wash`）、`白描水墨`（`baimiao-ink`，含「线描主导」「漫画夸张」两个变体）、`都市淡水彩`（`city-watercolor`，写实水彩 + 现代城市）。配方、后缀原文、分镜与失败复盘**只在库里维护一份**，SKILL.md 只留名字索引。
- **实测避坑** —— 转义拼中文会写错字、想让物件变小得改形状而不是给数值、古代人物只写朝代名会出来民国装；`ECONNRESET` 有 2026-10-06 / 2026-11-09 两次实测。每条都注明日期和当时踩的具体细节。

## 什么场景用它

| 场景 | 说明 |
|---|---|
| 公众号 / 博客 封面 + 正文插图 | 一张封面立主题，其余按小标题顺序各配一张 |
| 同风格系列图 | 需要多张图看起来像一套（同风格、同人物） |
| 卡片 / 长图 / 信息图素材 | 批量出图，统一尺寸与留白 |
| 单张图的重出与微调 | 改白边宽度、换比例、去水印不必重新生图 |

## Quick Start

```bash
# Install (clawhub)
clawhub install imagegen-batch

# Or clone the mono-repo; the skill lives in skills/imagegen-batch/
git clone https://github.com/Songhonglei/better-office-work.git
```

## Usage

详细规则见 [SKILL.md](./SKILL.md)，风格档案见 [references/style-library.md](./references/style-library.md)。

触发示例：

- 「给这篇文章生成封面和 5 张插图」→ 分镜 + 批量生成 + 归档
- 「用白纸速写风格做一套」→ 直接调风格库里的 `paper-sketch` 配方
- 「图片右下角有水印」→ `--auto-crop` 自动量 → 按 CUT 裁 → 验真（量不到走 FALLBACK）
- 「这几张图的人物长得一样」→ 上「标识包」重出（默认最多 4 版）
- 「这张重出三版了还不对」→ 到上限就交付最不坏的一版 + 未达标清单

## 后期脚本

`scripts/add_frame.py`（依赖 Pillow）—— 裁水印（必做）+ 可选的留白边框。

```bash
python3 -m pip install Pillow          # 唯一依赖

S=scripts/add_frame.py

# 默认：优先自动量水印，不加框
python3 "$S" in.png out.png --auto-crop
python3 "$S" in.png out.png --auto-crop --ratio 2.35             # 头条封面（2.35:1），再 sips -z 383 900

# 已知 CUT（脚本 AUTO-CROP 行给出）→ 同批其余图直接复用
python3 "$S" in.png out.png --crop-bottom 80
python3 "$S" in.png out.png --crop-bottom 70 --ratio 2.35

# 用户明确要求留白边时，才加 --frame
python3 "$S" in.png out.png --crop-bottom 80 --frame --line 0
python3 "$S" in.png out.png --crop-bottom 70 --frame --ratio 1 --pad 0.04 --line 0   # 方形次条封面
```

| 参数 | 默认 | 说明 |
|---|---|---|
| `--auto-crop` | 关 | **自动量测水印上沿并裁底边**；量不到时按尺寸经验值裁并打印 `FALLBACK`。与 `--crop-bottom` 互斥 |
| `--frame` | 关 | **加框总开关，默认不加**；用户要求留白边时才传 |
| `--pad` | 0.06 | 外侧白边，取**短边**的比例；5%~6% 观感最好 |
| `--gap` | 11 | 图像与线框之间的白隙（px）；`--line 0` 时它就是图像到外沿的留白 |
| `--line` | 3 | 线框粗细（px）；**传 0 = 只留白边不画线**（推荐） |
| `--crop-bottom` | 0 | 先裁掉底部 N px（去水印） |
| `--ratio` | — | 裁到指定比例，用二分拟合、不用手算；不加框时指图像本身，加框时指含框后的整体 |

> **加框会改变整体比例**，且 `pad` 依赖短边、短边又随裁切变化——手算必然错。要精确到目标比例请用脚本内置的 `fit_ratio()`。

## Install in your AI agent

| Agent | Install |
|---|---|
| WorkBuddy | 复制到 `~/.workbuddy/skills/` |
| Claude Code | 复制到 `~/.claude/skills/` |
| Cursor | 复制到 `.cursor/skills/` |
| OpenClaw | `clawhub install imagegen-batch` |

## License

MIT (see [LICENSE](./LICENSE))

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for the full version history.
