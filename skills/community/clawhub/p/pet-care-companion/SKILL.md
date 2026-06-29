---
name: Pet Care Companion
slug: pet-care-companion
description: 宠物护理全能伴侣。覆盖犬猫/鸟类/爬宠/水族等品类，提供健康监测、疫苗接种日历、营养配餐、行为训练指导、宠物医院地图、品种百科。让AI帮你科学养宠，毛孩子健康更安心。
version: 1.0.0
author: ai-gaoqian
tags:
  - pet-care
  - veterinary
  - pet-health
  - animal-welfare
  - pet-nutrition
metadata:
  openclaw:
    requires: []
    pricing:
      amount: 0.50
      currency: CNY
      interval: per-use
---

# Pet Care Companion

科学养宠AI助手。从接回家第一天到晚年护理，覆盖宠物全生命周期的健康管理。

## 使用场景

- **健康监测**：记录体重、食量、排泄、活动量数据，异常波动预警
- **疫苗接种日历**：根据宠物品类/年龄自动生成疫苗日程，到期提醒
- **营养配餐**：基于品种、年龄、体重、健康状况推荐每日喂食量和营养配比（干粮/湿粮/生骨肉/自制）
- **行为训练**：定点排便、随行、拒食、社会化等训练方案，分步骤指导
- **症状初步分析**：输入宠物异常表现（呕吐/腹泻/瘙痒/跛行等），提供可能原因和就医紧急度建议（非诊断，仅作参考）
- **宠物医院地图**：搜索附近有资质的宠物医院，按评分/专科筛选
- **品种百科**：200+ 犬猫品种的性情、护理要点、常见遗传病知识库

## 覆盖品类

| 品类 | 覆盖项 |
|------|--------|
| 犬 | 150+ 品种，按体型/能量等级/训练难度分级 |
| 猫 | 70+ 品种，室内/室外生活建议 |
| 鸟类 | 鹦鹉/文鸟/金丝雀 饲养指南 |
| 小型哺乳 | 兔子/仓鼠/龙猫/豚鼠 |
| 爬宠 | 乌龟/蜥蜴/蛇 温湿度管理 |
| 水族 | 淡水/海水观赏鱼，水质参数管理 |

## 配置

```yaml
skills:
  pet-care-companion:
    pets:
      - name: 旺财
        species: dog
        breed: 金毛寻回犬
        birth_date: "2024-03-15"
        weight_kg: 28.5
        neutered: true
    default_location: beijing
    reminder_advance_days: 3
```

## 示例指令

- "旺财该打今年的疫苗了吗？列出需要接种的项目"
- "我家猫最近频繁呕吐毛球，正常吗？"
- "给我推荐附近评分最高的猫专科医院"
- "3个月大的柯基幼犬每天应该喂几次、每次多少克？"
