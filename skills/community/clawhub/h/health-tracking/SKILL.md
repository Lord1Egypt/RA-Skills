---
name: health-tracking
description: Record health data (meals, weight, water, workout, sleep) to CSV files. Analyze food photos for nutrition.
metadata:
  {
    "openclaw":
      {
        "emoji": "🏥",
        "requires": { "scripts": ["scripts/health_record.js", "scripts/nutrition_append.js"] },
      },
  }
---

# health-tracking

Record health data to CSV files and analyze food photos for nutritional content.

## Scripts

### health_record.js — 健康データ記録

```bash
# 朝の記録（体重・睡眠・気分・安静時心拍）
node scripts/health_record.js morning --weight=70 --sleep=7 --mood=4 --hr=60

# 夜の記録（体重・気分）
node scripts/health_record.js night --weight=69.5 --mood=3

# 水分記録
node scripts/health_record.js water --amount=500 --source=water

# 運動記録
node scripts/health_record.js workout --activity=running --duration=30 --intensity=3 --cal=300

# テキストベースの食事記録
node scripts/health_record.js meal --type=lunch --desc="鶏胸肉サラダ" --cal=450 --p=35 --c=20 --f=15

# 日報
node scripts/health_record.js report --text="今日は集中できた"
```

### nutrition_append.js — 栄養データ追記（写真分析後）

食事画像を分析した後、推定値を記録する:

```bash
node scripts/nutrition_append.js \
  --desc="鶏胸肉サラダ" \
  --cal=450 --p=35 --c=20 --f=15 \
  --fiber=5 --sugar=3 --sodium=800 --satfat=2 \
  --photo_ref=file_id \
  --notes="confidence=0.85"
```

## 食事画像分析ワークフロー

ユーザーが食事画像を送信した場合:

1. 画像をビジョン機能で分析
2. 以下のJSON形式で推定:
   - summary: 日本語で料理名と内容を2-3文で説明
   - estimated_kcal, estimated_protein_g, estimated_carbs_g, estimated_fat_g
   - estimated_fiber_g, estimated_sugar_g, estimated_sodium_mg, estimated_saturated_fat_g
   - confidence: 0-1（明確な画像は0.8以上、不鮮明なら0.5以下）
3. `nutrition_append.js` で記録
4. ユーザーに分析結果を返信

## CSV スキーマ

- `data/daily.csv`: ts,date,weight_kg,sleep_hours,resting_hr,mood_1to5,notes
- `data/hydration.csv`: ts,date,time,amount_ml,source,notes
- `data/workout.csv`: ts,date,time,activity,duration_min,intensity_1to5,calories_estimate,notes
- `data/nutrition_meals.csv`: ts,date,time,meal_type,description,photo_ref,cal,p,c,f,water,notes

## デイリースレッド管理

`#health` チャネルで日付ごとのスレッドを作成し、その日の食事記録をスレッド内にまとめる。
スレッドの親メッセージ例: `:plate_with_cutlery: 2026-02-24 の食事記録`

## 体調フィードバック

食事分析の返信後、ユーザーは以下の形式で体調を記録できる:
`体調 睡眠:7h 疲労:2 水分:1500ml 運動:中 メモ:集中OK`
