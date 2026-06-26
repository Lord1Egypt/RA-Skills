# 开发者指南

> 面向开发者的技术文档，包含 API 参考和数据库规范。

---

## 目录

1. [API 参考](#api-参考)
2. [食物数据库](#食物数据库)
3. [数据库 Schema](#数据库-schema)

---

## API 参考

### init_db.py

初始化数据库。

```bash
python3 scripts/init_db.py --user <username> [--force]
```

**参数：**
- `--user` (必需): 用户名
- `--force`: 覆盖现有数据库

---

### user_profile.py

用户档案管理。

```bash
# 设置档案
python3 scripts/user_profile.py --user <name> set \
  --gender male --birth-date 1994-05-15 \
  --height-cm 175 --activity-level moderate --goal-type maintain

# 查看档案
python3 scripts/user_profile.py --user <name> get
```

**选项：**
- `--gender`: male/female
- `--birth-date`: YYYY-MM-DD
- `--height-cm`: 身高(cm)
- `--target-weight-kg`: 目标体重
- `--activity-level`: sedentary/light/moderate/active/very_active
- `--goal-type`: lose/maintain/gain

---

### body_metrics.py

身体数据记录。

```bash
# 记录体重
python3 scripts/body_metrics.py --user <name> log-weight \
  --weight 72.5 --body-fat 18.5

# 查看趋势
python3 scripts/body_metrics.py --user <name> trend --days 30
```

---

### meal_logger.py

饮食日志。

```bash
# 记录一餐
python3 scripts/meal_logger.py --user <name> log \
  --meal-type lunch --foods "米饭:150g,鸡胸肉:100g"

# 今日摘要
python3 scripts/meal_logger.py --user <name> daily-summary
```

---

### food_analyzer.py

食物分析。

```bash
# 搜索食物
python3 scripts/food_analyzer.py --user <name> search --query "牛肉"

# 添加自定义食物
python3 scripts/food_analyzer.py --user <name> add-custom \
  --name "红烧肉" --calories 350 --protein 15

# OCR 扫描
python3 scripts/food_analyzer.py --user <name> scan --image chips.jpg
```

---

### pantry_manager.py

食材库存管理。

```bash
# 添加食材
python3 scripts/pantry_manager.py --user <name> add \
  --food "鸡胸肉" --quantity 500 --location 冰箱

# 记录使用
python3 scripts/pantry_manager.py --user <name> use \
  --item-id 1 --amount 200

# 查看剩余
python3 scripts/pantry_manager.py --user <name> remaining
```

**储藏位置：** 冰箱、冷冻、干货区、台面

---

### smart_recipe.py

智能菜谱推荐。

```bash
python3 scripts/smart_recipe.py --user <name> --count 3
```

---

### export_data.py

数据导出。

```bash
# JSON 格式
python3 scripts/export_data.py --user <name> --format json

# CSV 格式
python3 scripts/export_data.py --user <name> --format csv
```

---

### backup_db.py

数据库备份。

```bash
# 备份
python3 scripts/backup_db.py --user <name> backup

# 列出备份
python3 scripts/backup_db.py --user <name> list

# 恢复
python3 scripts/backup_db.py --user <name> restore --file <backup>
```

---

## 食物数据库

### 数据结构

```json
{
  "name": "食物名称",
  "category": "protein|vegetable|carb|fruit|dairy|fat",
  "calories_per_100g": 100,
  "protein_per_100g": 10,
  "carbs_per_100g": 20,
  "fat_per_100g": 5,
  "fiber_per_100g": 2
}
```

### 内置分类

| 分类 | 示例 |
|-----|------|
| protein | 鸡胸肉、牛肉、鸡蛋、豆腐 |
| vegetable | 西兰花、菠菜、西红柿 |
| carb | 米饭、燕麦、红薯 |
| fruit | 苹果、香蕉、橙子 |
| dairy | 牛奶、酸奶、奶酪 |
| fat | 橄榄油、坚果、牛油果 |

### 扩展方式

```bash
# 添加自定义食物
python3 scripts/food_analyzer.py --user <name> add-custom \
  --name "新食物" --calories 200 --protein 10 --carbs 25 --fat 8
```

---

## 数据库 Schema

### 核心表

#### users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    display_name TEXT,
    gender TEXT,
    birth_date DATE,
    height_cm REAL,
    target_weight_kg REAL,
    activity_level TEXT,
    goal_type TEXT,
    bmr REAL,
    tdee REAL
);
```

#### body_metrics
```sql
CREATE TABLE body_metrics (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    weight_kg REAL,
    bmi REAL,
    recorded_at DATETIME
);
```

#### meals
```sql
CREATE TABLE meals (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    meal_type TEXT,
    eaten_at DATETIME,
    total_calories REAL,
    total_protein_g REAL,
    total_carbs_g REAL,
    total_fat_g REAL
);
```

#### pantry
```sql
CREATE TABLE pantry (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    food_name TEXT,
    category TEXT,
    location TEXT,  -- 冰箱/冷冻/干货区/台面
    quantity_g REAL,
    remaining_g REAL,
    expiry_date DATE
);
```

#### custom_foods
```sql
CREATE TABLE custom_foods (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    name TEXT,
    barcode TEXT,
    category TEXT,
    calories_per_100g REAL,
    protein_per_100g REAL,
    carbs_per_100g REAL,
    fat_per_100g REAL
);
```

---

*开发者文档，面向技术用户*
