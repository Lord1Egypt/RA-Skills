---
name: huo15-comic-orchestrator
displayName: 火15 AI 漫剧编排器
description: 一键生成 3-5 分钟国风 AI 漫剧。主题→分幕剧本→角色卡→分镜关键帧→图生视频→TTS 配音→对口型→BGM→字幕→拼接成片。自带三级成本熔断（硬限/预警/降级建议），支持失败续跑。触发词：AI 漫剧、生成漫剧、国风漫剧、仙侠短剧、comic drama、做漫剧。
version: 0.1.0
aliases:
  - AI漫剧
  - 国风漫剧
  - 仙侠短剧
  - 漫画短剧
  - comic-drama
---

# 火15 AI 漫剧编排器

> 主入口 skill，串起家族其他 8 个子 skill 完成 3-5 分钟国风漫剧生成。

---

## ⚠️ 硬规则

1. **成本熔断优先**：开工前估算超 `cost_cap` 立即阻止，不得强行继续
2. **用户确认闸门**：估算出来后**必须**等用户"确认"/"开始"再执行
3. **国风为默认**：不强制改风格时默认 `三渲二国风` + `仙侠`
4. **Checkpoint 续跑**：任何失败都从 `.checkpoint.json` 恢复，不重做已完成步骤

---

## 一、家族依赖

| 子 skill | Step | 本 skill 如何调用 |
|---|---|---|
| huo15-comic-script | 1 | `python ../huo15-comic-script/scripts/script_gen.py` |
| huo15-comic-character | 2 | `python ../huo15-comic-character/scripts/character.py` |
| huo15-comic-storyboard | 3 | `python ../huo15-comic-storyboard/scripts/storyboard.py` |
| huo15-comic-video | 4 | `python ../huo15-comic-video/scripts/video.py` |
| huo15-comic-dub | 5 | `python ../huo15-comic-dub/scripts/dub.py` |
| huo15-comic-lipsync | 6 | `python ../huo15-comic-lipsync/scripts/lipsync.py` |
| huo15-comic-bgm | 7 | `python ../huo15-comic-bgm/scripts/bgm.py` |
| huo15-comic-edit | 8 | `python ../huo15-comic-edit/scripts/edit.py` |

---

## 二、Agent 工作流

### Step 0：收集输入

必填：`theme`（主题一句话）、`duration_total`（秒数，180/240/300）
可选：`style`、`genre`、`character_hints`、`cost_cap`、`enable_lipsync`

### Step 1：预估成本（硬熔断点）

```python
from _shared.cost_guard import estimate_total, CostGuard, BudgetExceeded

n_scenes = duration_total // 5
est = estimate_total(
    n_scenes=n_scenes, n_characters=3, total_chars=800,
    resolution=resolution,   # 720p 默认 / 1080p 贵 2.3×
    fast=fast_mode,          # seedance-fast 打 5 折
    enable_lipsync=enable_lipsync,
    enable_bgm=enable_bgm,
)
guard = CostGuard(cap=cost_cap or 600.0, project_dir=project_dir)
try:
    guard.preflight(est["total"])
except BudgetExceeded as e:
    # 立即报给用户降级建议，等用户选择
    report_to_user(str(e))
    return
```

### Step 2：向用户确认

```
收到！将生成 {duration_total}s 国风漫剧（{n_scenes} 镜头）
主题：{theme}
风格：{style} / 类型：{genre}
预估成本：
  · 剧本  ¥0.00（本地）
  · 角色  ¥{image}
  · 视频  ¥{video}
  · TTS   ¥{tts}
  · 口型  ¥{lipsync}
  · BGM   ¥{bgm}
  · 合计  ¥{total}（熔断上限 ¥{cap}）
确认开始吗？
```

### Step 3-10：按顺序调用子 skill

每步前 checkpoint 查重（`if cp.is_done(step): skip`），每步后 `guard.charge(step, item, cost)`，触发预警即告知用户，触发熔断即停并给降级方案。

### Step 11：交付

输出 `output/{project_slug}/final.mp4` 路径、实际成本、耗时。

---

## 三、主入口脚本

`scripts/run.py`：

```bash
python scripts/run.py \
  --theme "少年剑仙三年归来" \
  --duration 240 \
  --style 三渲二国风 \
  --genre 仙侠 \
  --cap 600
```

详见 [scripts/run.py](./scripts/run.py)。

---

## 四、熔断降级策略

`_shared/cost_guard.py` 的 `BudgetExceeded` 抛出时，默认提供 5 选 1：

1. 缩短总时长
2. 减少镜头数
3. 关闭对口型（省 ~10%，Kling 2.6 便宜后此项影响小）
4. 启用 `--fast`（seedance-fast 打 5 折，视频占大头，省 ~40%）
5. 降 resolution：1080p → 720p 省 ~60% 视频费；720p → 480p 再省 ~50%
6. 提升 cost_cap

**Agent 必须让用户二次确认任何降级**，不得自动降级。

### 成本主导因素（720p 基线）

视频占比最高（~85%）→ 优先调视频参数：
- `fast=True` → 视频减半
- `resolution=480p` → 视频再减半
- `scene_duration=4` → 视频线性减 20%

Lipsync 成本从 2026-04 起大幅下降（Kling 2.6: ¥0.72/5s），不再是大头。

---

## 五、Agent 直写剧本模式（推荐）

**不建议**让 `scripts/script_gen.py` 调 Anthropic SDK 生成剧本，因为：
1. Claude（即本 Agent）就是 LLM 本体，再开 SDK 调自己是冗余
2. `script_gen.py` 走 SDK 要消耗 token，Agent 直写不花钱

**推荐流程**：Agent 按 `huo15-comic-script/SKILL.md` 的 JSON schema **直接写** `script.json` 到 `output/{slug}/`，然后：

```bash
# 跳过 LLM 调用，只校验
python huo15-comic-script/scripts/script_gen.py \
  --theme "..." --duration 240 \
  --input-json output/{slug}/script.json \
  --out output/{slug}/script.json
```

run.py 支持 `SCRIPT_PREWRITTEN=1` 环境变量跳过 SDK 调用路径。

Demo 见 `examples/demo-xianxia-180s.json`。

---

## 六、Checkpoint 续跑

`output/{project}/.checkpoint.json` 记录每步与镜头级状态：

```json
{
  "script": "done",
  "characters": "done",
  "storyboard": "done",
  "videos": "running",
  "videos.S01": "done",
  "videos.S02": "done",
  "videos.S03": "running",
  ...
}
```

重启时扫描，从 `next_pending()` 续跑，已完成镜头不重做。
