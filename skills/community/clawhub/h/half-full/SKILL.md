---
name: half-full
description: 半饱 — 生活的高潮所在。A mindful eating companion for desk workers. Track meals with photos, understand your body's needs, no gym guilt.
version: 0.1.4
author: oak lee
tags: [nutrition, health, diet, mindful-eating, 减脂, 饮食, 健康]
metadata:
  openclaw:
    emoji: "🍃"
    requires:
      bins: ["python3"]
    scripts:
      - scripts/log.py
      - scripts/profile.py
      - scripts/food_db.py
      - scripts/health_sync.py
    commands:
      - "python3 scripts/log.py add --meal 早餐 --items '鸡蛋,燕麦'"
      - "python3 scripts/log.py today"
      - "python3 scripts/profile.py show"
      - "python3 scripts/profile.py update --weight 60"
      - "python3 scripts/health_sync.py parse '[半饱数据] 步数：8000 步，活动消耗：300 千卡'"
      - "python3 scripts/health_sync.py today"
    install: "pip3 install -q"
---

# 半饱 🍃

生活的高潮所在。

不是教练，不是健身搭子，是你幸福生活的陪伴。
