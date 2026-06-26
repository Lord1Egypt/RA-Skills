---
name: huo15-comic-dub
displayName: 火15 漫剧-TTS 配音
description: 读 script.json 对白，按角色分配音色，调火山方舟 Seed-TTS 生成每条对白的 wav，命名 {sceneId}_{charId}_{idx}.wav。触发词：对白配音、TTS 配音、角色配音。
version: 0.1.0
---

# 火15 漫剧-TTS 配音 Skill

> 每条 dialogue → 一个 wav，角色音色固定。

---

## 输入 / 输出

```bash
python scripts/dub.py \
  --script output/demo/script.json \
  --out-dir output/demo/audio
```

输出：

```
audio/
├── S01_C1_0.wav
├── S02_C1_0.wav
├── S02_C2_0.wav
├── ...
└── manifest.json
```

## 音色库（Seed-TTS 已内置）

- 男：`zh_male_qingnian`（青年）/ `zh_male_shenchen`（沉稳） / `zh_male_wennuan`（温暖）
- 女：`zh_female_qingxin`（清新）/ `zh_female_wenrou`（温柔） / `zh_female_ganxing`（感性）

若 script.json 的 character.voice 为空，按角色 age/personality 自动分配。

## 成本

字数 × ¥0.0008/字。200 字对白 ≈ ¥0.16。
