---
name: nutrition-planner
description: "Personal nutrition and meal planning system with calorie tracking and recipe recommendations"
version: "1.0.1"
---


- 👤 **饮食需求分析**: 根据年龄、体重、身高、活动量计算营养需求
- 🍽️ **个性化菜谱推荐**: 基于目标的智能食谱推荐
- 📊 **营养成分计算**: 自动计算每餐热量、蛋白质、碳水、脂肪
- 📅 **周/月饮食计划**: 自动生成多天的完整饮食计划
- 🛒 **智能购物清单**: 根据计划自动生成购物清单

## 使用

### 创建用户档案

```bash
# 基础档案
${SKILL_DIR}/scripts/nutrition-planner profile-create \
  --name "张三" \
  --age 30 \
  --gender male \
  --weight 70 \
  --height 175 \
  --goal lose

# 完整档案（含饮食限制和过敏）
${SKILL_DIR}/scripts/nutrition-planner profile-create \
  --name "李四" \
  --age 25 \
  --gender female \
  --weight 55 \
  --height 160 \
  --activity moderate \
  --goal maintain \
  --restrictions vegetarian \
  --allergies peanuts shellfish
```

### 活动量选项

- `sedentary` - 久坐（办公室工作）
- `light` - 轻度活动（每周1-2天运动）
- `moderate` - 中度活动（每周3-5天运动）
- `active` - 高度活动（每周6-7天运动）
- `very_active` - 极高活动（体力劳动/运动员）

### 目标选项

- `lose` - 减脂（每日-500kcal）
- `maintain` - 维持（基础代谢）
- `gain` - 增肌（每日+500kcal）

### 生成饮食计划

```bash
# 生成7天计划（默认）
${SKILL_DIR}/scripts/nutrition-planner plan-generate

# 生成14天计划
${SKILL_DIR}/scripts/nutrition-planner plan-generate --days 14
```

### 查看饮食计划

```bash
# 查看今日计划
${SKILL_DIR}/scripts/nutrition-planner plan-show

# 查看指定日期
${SKILL_DIR}/scripts/nutrition-planner plan-show --date 2024-01-15
```

### 生成购物清单

```bash
# 生成未来7天购物清单
${SKILL_DIR}/scripts/nutrition-planner shopping-list

# 生成未来14天购物清单
${SKILL_DIR}/scripts/nutrition-planner shopping-list --days 14
```

### 查询食物营养

```bash
# 查询单一食物
${SKILL_DIR}/scripts/nutrition-planner nutrition 鸡胸肉

# 模糊查询
${SKILL_DIR}/scripts/nutrition-planner nutrition 鸡
```

## 数据存储

数据存储在 `~/.openclaw/data/nutrition-planner/`:
- `nutrition_planner.db` - SQLite 数据库

## 内置食物数据库

包含以下类别的食物营养数据：
- 主食：米饭、面条、馒头、燕麦、红薯、玉米、全麦面包
- 蛋白质：鸡胸肉、鸡蛋、牛肉、三文鱼、豆腐、牛奶、虾仁
- 蔬菜：西兰花、菠菜、胡萝卜、番茄、黄瓜、青椒、生菜、芹菜
- 水果：苹果、香蕉、橙子、蓝莓、猕猴桃
- 坚果油脂：杏仁、核桃、橄榄油

## 技术栈

- Python 3.8+
- SQLite
- argparse
