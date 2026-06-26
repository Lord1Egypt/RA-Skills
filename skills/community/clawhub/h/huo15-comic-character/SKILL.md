---
name: huo15-comic-character
displayName: 火15 漫剧-角色三联卡
description: 根据剧本 characters 字段，用 Seedream 4.0 生成每个角色的全身立绘/半身特写/Q 版三联卡。后续分镜用这三张图做多图参考保证角色一致性。触发词：生成角色卡、角色立绘、人物设定图。
version: 0.1.0
aliases:
  - 角色卡
  - 角色立绘
---

# 火15 漫剧-角色三联卡 Skill

> 读 script.json → 调 Seedream 4.0 → 每个角色输出 3 张图 → 后续 storyboard 用作参考。

---

## 输入 / 输出

```bash
python scripts/character.py \
  --script output/demo/script.json \
  --out-dir output/demo/characters
```

输出目录结构：

```
characters/
├── C1_full.png      # 全身立绘
├── C1_close.png     # 半身特写（表情基准）
├── C1_chibi.png     # Q 版头像
├── C2_full.png
├── ...
└── manifest.json    # {"C1": {"name": "顾青崖", "images": [...]}}
```

## 提示词模板

每个角色构建三条 prompt：

```python
full_prompt  = f"{STYLE_PREFIX}，角色全身立绘，{char.visual}，{char.personality}气质，站姿，居中构图，纯色背景"
close_prompt = f"{STYLE_PREFIX}，角色半身特写，{char.visual}，{char.personality}表情，肩部以上，正面"
chibi_prompt = f"{STYLE_PREFIX}，Q版头像，{char.visual}简化版，可爱风格，圆润线条"
```

`STYLE_PREFIX` 取自 `_shared/config.py` 的 `STYLE_PRESETS[style].prefix`。

## 成本

3 张 × N 角色 × ¥0.08/张。典型 3 角色 = ¥0.72。
