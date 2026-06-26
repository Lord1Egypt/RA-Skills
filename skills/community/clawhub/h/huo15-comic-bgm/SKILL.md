---
name: huo15-comic-bgm
displayName: 火15 漫剧-背景音乐
description: 根据剧本整体 mood 生成一首 BGM（Suno v5），时长匹配总时长，国风优先（古筝/琵琶/笛子）。触发词：BGM 生成、背景音乐、配乐。
version: 0.1.0
---

# 火15 漫剧-背景音乐 Skill

> 整片一首 BGM，FFmpeg 混音时压到 -20dB。

---

## 输入 / 输出

```bash
python scripts/bgm.py \
  --script output/demo/script.json \
  --duration 240 \
  --out output/demo/bgm.mp3
```

## Suno prompt 模板

```python
# 从 scenes 抽取 mood 词频，取 top 3
moods = ["苍凉", "壮阔", "激昂"]  # e.g.
prompt = f"国风古风纯音乐，{', '.join(moods)}氛围，古筝为主旋律，点缀琵琶和笛子，时长 {duration}秒"
```

## 降级

Suno 不可用时，fallback 到 `templates/bgm_library/国风/{mood}.mp3` 本地素材。

## 成本

¥3/首，整片固定。
