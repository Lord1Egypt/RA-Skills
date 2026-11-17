# Photo Imprint (印痕)

> 留住那张照片，只换一种笔触去记。

[English](README.md) | [繁體中文](README.zh-TW.md)

你从日本回来，手机里一堆杯子、机舱、六本木街头的照片，想发小红书 / IG 成一套手帐轮播。直接丢给模型，好看但小杯变大杯，街景还给你编个东京塔，你的那张不见了。

`locoda/photo-imprint-skill` · 英文 skill，中文名印痕

```
请帮我安装这个 skill：https://github.com/locoda/photo-imprint-skill
```

![license MIT](https://img.shields.io/badge/license-MIT-green) ![version 1.6.0](https://img.shields.io/badge/version-1.6.0-blue) ![tests 34 gates](https://img.shields.io/badge/tests-34%20gates-lightgrey)

| 印痕（下方居中，上方 caption 示例） | 原片已模糊，保护隐私 |
|---|---|
| ![印痕01](assets/samples/01-sjc-small-cup-paper-locked-v11.webp) | ![原片01](assets/samples/source-01.webp) |
| 小杯保持小，盖子锁死，50%纸白，下方居中 | SJC 小杯（12px模糊） |
| ![印痕02](assets/samples/02-in-flight-paper-locked-v11.webp) | ![原片02](assets/samples/source-02.webp) |
| 机舱简化成冷色块，不编天空 | 飞机上（已模糊） |
| ![印痕03](assets/samples/03-roppongi-paper-locked-v11.webp) | ![原片03](assets/samples/source-03.webp) |
| 背景强简化，不编东京塔 | 六本木街头（已模糊） |

样张 webp <100KB 在 `assets/samples/`，终版 1152×2048 jpg ~400KB，无 EXIF。

## 一堆旅行照终于像一本手帐的时候

**你：** 有10张日本的照片，想做成一套水彩手帐轮播发出去，但原片太杂，不想露脸，也不想让模型瞎编东京塔。试过一个 prompt 渲所有，小杯第2张就变大杯了。

**印痕：** 把轮廓、比例、盖子、logo 位置全部锁住。甩8张真实风格小图给你选，选一种后只渲第1页，把 `production-plan.md` + 6字段 style contract + 样张一起给你看，等你原话批准才批量 2..N。

**现在你可以：** 用第1张判断整套，小杯保持小，4张全是暖纸 #F1EBDD、55%顶留白、下方居中，没有编造的地点/日期，拿到的 ZIP 已双维 QA 过。

## 怎么跟 AI 说

你不用跑脚本，AI 跑。

**装一次：**
```
请帮我安装这个 skill：https://github.com/locoda/photo-imprint-skill
```

**开一套：**
> 我有10张日本照片在 /path/to/photos，帮我做成水彩手帐，小杯保持小，下方居中，上面55%留白，不要字，保留杯高和logo位置。

**选风格：**
> 用 sumi-e-ink / 你定 / 用默认水彩

**批准：**
> 批准第1张，继续

**改一页：**
> 第2张背景太满，简化一下

**换风格（会退回风格门，符合预期）：**
> 换成广重去雨版

小技巧：小杯保持小是默认锁死的，不用反复说。caption 只认 EXIF，不想要就说“不要字”。私人参考图只存本地，除非你说“可以上传到 X”。

## 怎么做到

### 锁住该留的，只在笔触上抽象

原片是权威。Template A/B 现在都走下方居中：主体 y=0.72 居中，1152×2048，暖纸，50%空白保底。shape-lock 锁杯/瓶轮廓、高度、盖子、logo，抽象只在笔触和贴边2-3处 ≤10%宽度溶色，颜色从主图取，不自己发明。不带手/布/相框/三联画。

### 单选风格，冻住合同，不混搭

已打包8个：`watercolor-journal`（默认，下方居中）、`blue-lavender-watercolor`、`highway-485-lithograph`、`sumi-e-ink`（芝田浙信1847 疏朗墨线）、`hiroshige-bokashi`（广重1833去雨 平涂+bokashi）、`seurat-conte`（修拉1882 无硬轮廓 Conté排线）。选一种写进 `work/style_choice.json`，冻进 `work/sample_style_contract.json`，批量时 hash-lock。要求混搭会拒掉。

### 先 plan+样张，再批量，你说了算

不是 prompt 合集，是带门禁的生产流：EXIF 排序 → 每页 `production_brief`（保留/简化/省略）→ `production-plan.md` → 只渲第1页 → 讨论 → 明确批准 → 批量 2..N 用冻结合同 → 洗版 → 确定性合成 → 双维 QA → 已验证 ZIP。你跟 AI 说人话就行：

> 我有10张日本照片在 /path/to/photos，帮我做成水彩手帐，小杯保持小，下方居中，上面55%留白，不要字。

AI 按 EXIF 排序，缺 EXIF 会问是否授权 draft，甩8张风格，你说“你定”就用默认，渲样张，等你说“批准第1张，继续”。改图说“第2张背景太满，简化一下”只重渲第2张。私人参考图只存本地，除非你说“可以上传到 X”。

<details>
<summary>给 AI 看的实现细节（人不用看）</summary>

6层：Config → Plan → Gate → Render → QA → Package。Invariants：EXIF不可变、样张仅第1张、样张不作参考、每张 plate 有 receipt、无 EXIF/GPS/XMP、不编造。

默认值：9:16 1152×2048、纸 #F1EBDD 50%留白、默认 watercolor-journal、EXIF升序、QA 全尺寸+360×640。

工作流：`check_environment.py` → `resolve_config.py` + `preprocess.py` → `build_render_plan.py` + `build_production_plan.py` + `build_render_plan.py + build_production_plan.py (sample scope)` → 风格门 → 样张 → `review_gate.py approve` + `compose.py batch` → 批量合成 → QA → revision → `package_verified.py`

验证：`python3 -m unittest discover -s tests -v` / `python3 bin/validate_skill.py --json`

</details>

## 参考

- 行为和边界：`SKILL.md`、`references/configuration.md`、`references/review-gate.md`、`references/quality-checks.md`
- 回归和边界用例：`tests/`（34个门禁/回归）、`references/test-cases.md`、`bin/validate_skill.py`
- 存储和归档：`work/resolved-config.json`（SHA256）、`work/manifest.json`（EXIF排序）、`work/style_choice.json`、`work/composition-manifest.json`、`work/verify-report.json`
- 未使用需额外授权的字体或图片，风格包为 Smithsonian 公开域 `assets/style-packs/`，样张 webp <100KB，原片 12px 模糊保护隐私，终版无 EXIF/GPS/XMP，不含受版权保护原文

## License

MIT License — Copyright (c) 2026 locoda。代码与文档 MIT，风格包遵循各自 Smithsonian 公开域条款，样张同仓库许可，原片已模糊处理。

---
Made by [1mether](https://1mether.me).

*留住那张照片，只换一种笔触去记。*
