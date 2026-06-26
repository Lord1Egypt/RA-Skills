---
name: huo15-comic-storyboard
displayName: 火15 漫剧-分镜关键帧
description: 读 script.json + 角色卡，每个镜头生成 1 张关键帧（Seedream 4.0 图生图，传入该镜出场角色的三联卡做多图参考保持角色一致性）。触发词：分镜关键帧、storyboard、漫剧分镜图。
version: 0.1.0
---

# 火15 漫剧-分镜关键帧 Skill

> 一镜一图，角色锁定由 Seedream 4.0 多图参考保证。

---

## 输入 / 输出

```bash
python scripts/storyboard.py \
  --script output/demo/script.json \
  --char-dir output/demo/characters \
  --out-dir output/demo/storyboard
```

输出：

```
storyboard/
├── S01.png
├── S02.png
├── ...
└── manifest.json  # {"S01": {"path": "...", "prompt": "..."}}
```

## 提示词模板

```python
prompt = f"{STYLE_PREFIX}，{scene.location}，{scene.time}。{scene.action}。{scene.camera}。{scene.mood}氛围。"
reference_images = [char_full for char_id in scene.characters]  # 多图参考保角色一致
```

Seedream 4.0 支持最多 4 张 reference_image，超过时只取全身立绘。

## 细节规则

- 竖屏 9:16，尺寸 `768x1344`（比 1024x1792 省成本）
- 失败重试 2 次
- 每个 scene 的 prompt 中**不带对白**（对白后面 TTS 环节加）
