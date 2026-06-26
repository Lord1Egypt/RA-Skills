# Database Schema

## Overview

SQLite database per user with foreign key constraints enabled.

## ER Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     users       │     │  body_metrics   │     │     meals       │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)         │◄────┤ user_id (FK)    │     │ user_id (FK)    │
│ username (UQ)   │     │ id (PK)         │     │ id (PK)         │
│ display_name    │     │ weight_kg       │     │ meal_type       │
│ gender          │     │ height_cm       │     │ eaten_at        │
│ birth_date      │     │ body_fat_pct    │     │ notes           │
│ height_cm       │     │ bmi             │     │ total_calories  │
│ target_weight_kg│     │ recorded_at     │     │ total_protein_g │
│ activity_level  │     │ source          │     │ total_carbs_g   │
│ goal_type       │     └─────────────────┘     │ total_fat_g     │
│ bmr_formula     │              │              │ created_at      │
│ bmr             │              │              └─────────────────┘
│ tdee            │              │                        │
│ created_at      │              │                        │
│ updated_at      │              │              ┌─────────────────┐
└─────────────────┘              │              │   food_items    │
                                 │              ├─────────────────┤
                                 │              │ id (PK)         │
                                 │              │ meal_id (FK)    │
                                 │              │ food_name       │
                                 │              │ quantity_g      │
                                 │              │ calories        │
                                 │              │ protein_g       │
                                 │              │ carbs_g         │
                                 │              │ fat_g           │
                                 │              │ fiber_g         │
                                 │              │ source          │
                                 │              └─────────────────┘
                                 │
                    ┌────────────┘
                    │
         ┌─────────────────┐
         │  custom_foods   │
         ├─────────────────┤
         │ id (PK)         │
         │ user_id (FK)    │
         │ name            │
         │ category        │
         │ calories_per_100g│
         │ protein_per_100g│
         │ carbs_per_100g  │
         │ fat_per_100g    │
         │ fiber_per_100g  │
         │ is_public       │
         │ barcode         │
         │ brand           │
         │ source          │
         │ updated_at      │
         │ storage_method  │
         │ food_group      │
         │ default_shelf_life_days│
         │ created_at      │
         └─────────────────┘
                                 │
                    ┌────────────┘
                    │
         ┌─────────────────┐     │
         │     pantry      │     │
         ├─────────────────┤     │
         │ id (PK)         │     │
         │ user_id (FK)    │     │
         │ food_name       │     │
         │ food_id (FK)────┘     │
         │ quantity_g            │
         │ quantity_desc         │
         │ remaining_g           │
         │ category              │
         │ location              │
         │ purchase_date         │
         │ expiry_date           │
         │ notes                 │
         │ created_at            │
         │ updated_at            │
         └─────────────────┘     │
                                   │
         ┌─────────────────┐      │
         │  pantry_usage   │      │
         ├─────────────────┤      │
         │ id (PK)         │      │
         │ pantry_id (FK)──┘      │
         │ user_id (FK)           │
         │ used_g                 │
         │ remaining_after_g      │
         │ used_for_meal_id (FK)──┘
         │ notes                  │
         │ used_at                │
         └─────────────────┘
```

## Table Definitions

### users

User profile and metabolic calculations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 用户ID |
| username | TEXT | UNIQUE NOT NULL | 用户名（英文，用于文件名） |
| display_name | TEXT | | 显示名称 |
| gender | TEXT | CHECK (gender IN ('male', 'female')) | 性别 |
| birth_date | DATE | | 出生日期 |
| height_cm | REAL | CHECK (height_cm > 0) | 身高（厘米） |
| target_weight_kg | REAL | | 目标体重（公斤） |
| activity_level | TEXT | CHECK (activity_level IN ('sedentary', 'light', 'moderate', 'active', 'very_active')) | 活动水平 |
| goal_type | TEXT | CHECK (goal_type IN ('lose', 'maintain', 'gain')) | 目标类型 |
| bmr_formula | TEXT | DEFAULT 'mifflin_st_jeor' | BMR计算公式 |
| bmr | REAL | | 基础代谢率（千卡） |
| tdee | REAL | | 每日总能量消耗（千卡） |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 更新时间 |

**Indexes:**
- `idx_users_username` ON username

### body_metrics

Time-series body measurements.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 记录ID |
| user_id | INTEGER | FOREIGN KEY users(id) ON DELETE CASCADE | 用户ID |
| weight_kg | REAL | NOT NULL CHECK (weight_kg > 0) | 体重（公斤） |
| height_cm | REAL | | 身高（厘米，快照） |
| body_fat_pct | REAL | CHECK (body_fat_pct >= 0 AND body_fat_pct <= 100) | 体脂率（%） |
| bmi | REAL | | BMI（自动计算） |
| recorded_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 记录时间 |
| source | TEXT | DEFAULT 'manual' | 数据来源 |
| notes | TEXT | | 备注 |

**Indexes:**
- `idx_metrics_user_date` ON user_id, recorded_at
- `idx_metrics_recorded` ON recorded_at

### meals

Daily meal records with aggregated nutrition.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 餐食ID |
| user_id | INTEGER | FOREIGN KEY users(id) ON DELETE CASCADE | 用户ID |
| meal_type | TEXT | CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')) | 餐食类型 |
| eaten_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 进食时间 |
| notes | TEXT | | 备注 |
| total_calories | REAL | DEFAULT 0 | 总热量（千卡） |
| total_protein_g | REAL | DEFAULT 0 | 总蛋白质（克） |
| total_carbs_g | REAL | DEFAULT 0 | 总碳水（克） |
| total_fat_g | REAL | DEFAULT 0 | 总脂肪（克） |
| total_fiber_g | REAL | DEFAULT 0 | 总纤维（克） |
| total_sodium_mg | REAL | DEFAULT 0 | 总钠（毫克） |
| total_calcium_mg | REAL | DEFAULT 0 | 总钙（毫克） |
| total_trans_fat_g | REAL | DEFAULT 0 | 总反式脂肪（克） |
| total_saturated_fat_g | REAL | DEFAULT 0 | 总饱和脂肪（克） |
| total_sugar_g | REAL | DEFAULT 0 | 总糖（克） |
| total_vitamin_a_ug | REAL | DEFAULT 0 | 总维生素A（微克） |
| total_vitamin_c_mg | REAL | DEFAULT 0 | 总维生素C（毫克） |
| total_iron_mg | REAL | DEFAULT 0 | 总铁（毫克） |
| total_zinc_mg | REAL | DEFAULT 0 | 总锌（毫克） |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**Indexes:**
- `idx_meals_user_date` ON user_id, eaten_at
- `idx_meals_type` ON meal_type

### food_items

Individual food items within a meal.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 食物项ID |
| meal_id | INTEGER | FOREIGN KEY meals(id) ON DELETE CASCADE | 餐食ID |
| food_name | TEXT | NOT NULL | 食物名称 |
| quantity_g | REAL | NOT NULL CHECK (quantity_g > 0) | 重量（克） |
| calories | REAL | NOT NULL | 热量（千卡） |
| protein_g | REAL | DEFAULT 0 | 蛋白质（克） |
| carbs_g | REAL | DEFAULT 0 | 碳水（克） |
| fat_g | REAL | DEFAULT 0 | 脂肪（克） |
| fiber_g | REAL | DEFAULT 0 | 纤维（克） |
| sodium_mg | REAL | DEFAULT 0 | 钠（毫克） |
| calcium_mg | REAL | DEFAULT 0 | 钙（毫克） |
| trans_fat_g | REAL | DEFAULT 0 | 反式脂肪（克） |
| saturated_fat_g | REAL | DEFAULT 0 | 饱和脂肪（克） |
| sugar_g | REAL | DEFAULT 0 | 糖（克） |
| vitamin_a_ug | REAL | DEFAULT 0 | 维生素A（微克） |
| vitamin_c_mg | REAL | DEFAULT 0 | 维生素C（毫克） |
| iron_mg | REAL | DEFAULT 0 | 铁（毫克） |
| zinc_mg | REAL | DEFAULT 0 | 锌（毫克） |
| source | TEXT | DEFAULT 'database' | 数据来源 |

**Indexes:**
- `idx_food_items_meal` ON meal_id
- `idx_food_items_name` ON food_name

### custom_foods

User-defined or imported food items.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 食物ID |
| user_id | INTEGER | FOREIGN KEY users(id) ON DELETE CASCADE | 用户ID |
| name | TEXT | NOT NULL | 食物名称 |
| category | TEXT | | 分类 |
| unit | TEXT | DEFAULT 'g' | 计量单位（'g'克或'ml'毫升） |
| calories_per_100g | REAL | NOT NULL | 每100克/毫升热量 |
| protein_per_100g | REAL | DEFAULT 0 | 每100克/毫升蛋白质 |
| carbs_per_100g | REAL | DEFAULT 0 | 每100克/毫升碳水 |
| fat_per_100g | REAL | DEFAULT 0 | 每100克/毫升脂肪 |
| fiber_per_100g | REAL | DEFAULT 0 | 每100克/毫升纤维 |
| sodium_per_100g | REAL | DEFAULT 0 | 每100克/毫升钠（毫克） |
| calcium_mg | REAL | DEFAULT 0 | 每100克/毫升钙（毫克） |
| trans_fat_g | REAL | DEFAULT 0 | 每100克/毫升反式脂肪（克） |
| saturated_fat_g | REAL | DEFAULT 0 | 每100克/毫升饱和脂肪（克） |
| sugar_g | REAL | DEFAULT 0 | 每100克/毫升糖（克） |
| vitamin_a_ug | REAL | DEFAULT 0 | 每100克/毫升维生素A（微克） |
| vitamin_c_mg | REAL | DEFAULT 0 | 每100克/毫升维生素C（毫克） |
| iron_mg | REAL | DEFAULT 0 | 每100克/毫升铁（毫克） |
| zinc_mg | REAL | DEFAULT 0 | 每100克/毫升锌（毫克） |
| barcode | TEXT | | 条形码 |
| brand | TEXT | | 品牌 |
| source | TEXT | DEFAULT 'custom' | 数据来源 |
| storage_method | TEXT | | 储存方式 |
| default_shelf_life_days | INTEGER | | 默认保质期（天） |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | | 更新时间 |

**Indexes:**
- `idx_custom_foods_user` ON user_id
- `idx_custom_foods_name` ON name
- `idx_custom_foods_barcode` ON barcode

## SQL Initialization

```sql
-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    display_name TEXT,
    gender TEXT CHECK (gender IN ('male', 'female')),
    birth_date DATE,
    height_cm REAL CHECK (height_cm > 0),
    target_weight_kg REAL,
    activity_level TEXT CHECK (activity_level IN ('sedentary', 'light', 'moderate', 'active', 'very_active')),
    goal_type TEXT CHECK (goal_type IN ('lose', 'maintain', 'gain')),
    bmr_formula TEXT DEFAULT 'mifflin_st_jeor',
    bmr REAL,
    tdee REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

### pantry

食材库存管理表。

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 库存ID |
| user_id | INTEGER | FOREIGN KEY users(id) ON DELETE CASCADE | 用户ID |
| food_name | TEXT | NOT NULL | 食物名称 |
| food_id | INTEGER | FOREIGN KEY custom_foods(id) ON DELETE SET NULL | 关联的自定义食物ID |
| quantity_g | REAL | | 总量（克） |
| quantity_desc | TEXT | | 数量描述（如：2个，1盒） |
| remaining_g | REAL | | 剩余量（克） |
| category | TEXT | DEFAULT 'other' | 分类 |
| location | TEXT | | 存放位置 |
| purchase_date | DATE | | 购买日期 |
| expiry_date | DATE | | 过期日期 |
| notes | TEXT | | 备注 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 更新时间 |

**Indexes:**
- `idx_pantry_user` ON user_id
- `idx_pantry_expiry` ON expiry_date
- `idx_pantry_location` ON location

### pantry_usage

食材使用记录表。

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 使用记录ID |
| pantry_id | INTEGER | FOREIGN KEY pantry(id) ON DELETE CASCADE | 库存ID |
| user_id | INTEGER | FOREIGN KEY users(id) ON DELETE CASCADE | 用户ID |
| used_g | REAL | NOT NULL | 使用量（克） |
| remaining_after_g | REAL | | 使用后剩余量 |
| used_for_meal_id | INTEGER | FOREIGN KEY meals(id) ON DELETE SET NULL | 关联的餐食ID |
| notes | TEXT | | 备注 |
| used_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 使用时间 |

**Indexes:**
- `idx_pantry_usage_pantry` ON pantry_id
- `idx_pantry_usage_date` ON used_at

## SQL Initialization

```sql
-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    display_name TEXT,
    gender TEXT CHECK (gender IN ('male', 'female')),
    birth_date DATE,
    height_cm REAL CHECK (height_cm > 0),
    target_weight_kg REAL,
    activity_level TEXT CHECK (activity_level IN ('sedentary', 'light', 'moderate', 'active', 'very_active')),
    goal_type TEXT CHECK (goal_type IN ('lose', 'maintain', 'gain')),
    bmr_formula TEXT DEFAULT 'mifflin_st_jeor',
    bmr REAL,
    tdee REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Body metrics table
CREATE TABLE IF NOT EXISTS body_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    weight_kg REAL NOT NULL CHECK (weight_kg > 0),
    height_cm REAL,
    body_fat_pct REAL CHECK (body_fat_pct >= 0 AND body_fat_pct <= 100),
    bmi REAL,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    source TEXT DEFAULT 'manual',
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_metrics_user_date ON body_metrics(user_id, recorded_at);
CREATE INDEX IF NOT EXISTS idx_metrics_recorded ON body_metrics(recorded_at);

-- Meals table
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    meal_type TEXT CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
    eaten_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    total_calories REAL DEFAULT 0,
    total_protein_g REAL DEFAULT 0,
    total_carbs_g REAL DEFAULT 0,
    total_fat_g REAL DEFAULT 0,
    total_fiber_g REAL DEFAULT 0,
    total_sodium_mg REAL DEFAULT 0,
    total_calcium_mg REAL DEFAULT 0,
    total_trans_fat_g REAL DEFAULT 0,
    total_saturated_fat_g REAL DEFAULT 0,
    total_sugar_g REAL DEFAULT 0,
    total_vitamin_a_ug REAL DEFAULT 0,
    total_vitamin_c_mg REAL DEFAULT 0,
    total_iron_mg REAL DEFAULT 0,
    total_zinc_mg REAL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_meals_user_date ON meals(user_id, eaten_at);
CREATE INDEX IF NOT EXISTS idx_meals_type ON meals(meal_type);

-- Food items table
CREATE TABLE IF NOT EXISTS food_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_id INTEGER NOT NULL,
    food_name TEXT NOT NULL,
    quantity_g REAL NOT NULL CHECK (quantity_g > 0),
    calories REAL NOT NULL,
    protein_g REAL DEFAULT 0,
    carbs_g REAL DEFAULT 0,
    fat_g REAL DEFAULT 0,
    fiber_g REAL DEFAULT 0,
    sodium_mg REAL DEFAULT 0,
    calcium_mg REAL DEFAULT 0,
    trans_fat_g REAL DEFAULT 0,
    saturated_fat_g REAL DEFAULT 0,
    sugar_g REAL DEFAULT 0,
    vitamin_a_ug REAL DEFAULT 0,
    vitamin_c_mg REAL DEFAULT 0,
    iron_mg REAL DEFAULT 0,
    zinc_mg REAL DEFAULT 0,
    source TEXT DEFAULT 'database',
    FOREIGN KEY (meal_id) REFERENCES meals(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_food_items_meal ON food_items(meal_id);
CREATE INDEX IF NOT EXISTS idx_food_items_name ON food_items(food_name);

-- Custom foods table
CREATE TABLE IF NOT EXISTS custom_foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    category TEXT,
    calories_per_100g REAL NOT NULL,
    protein_per_100g REAL DEFAULT 0,
    carbs_per_100g REAL DEFAULT 0,
    fat_per_100g REAL DEFAULT 0,
    fiber_per_100g REAL DEFAULT 0,
    sodium_per_100g REAL DEFAULT 0,
    calcium_mg REAL DEFAULT 0,
    trans_fat_g REAL DEFAULT 0,
    saturated_fat_g REAL DEFAULT 0,
    sugar_g REAL DEFAULT 0,
    vitamin_a_ug REAL DEFAULT 0,
    vitamin_c_mg REAL DEFAULT 0,
    iron_mg REAL DEFAULT 0,
    zinc_mg REAL DEFAULT 0,
    barcode TEXT,
    brand TEXT,
    source TEXT DEFAULT 'custom',
    storage_method TEXT,
    default_shelf_life_days INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_custom_foods_user ON custom_foods(user_id);
CREATE INDEX IF NOT EXISTS idx_custom_foods_name ON custom_foods(name);
CREATE INDEX IF NOT EXISTS idx_custom_foods_barcode ON custom_foods(barcode);

-- Pantry table
CREATE TABLE IF NOT EXISTS pantry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    food_name TEXT NOT NULL,
    food_id INTEGER,
    quantity_g REAL,
    quantity_desc TEXT,
    location TEXT,
    purchase_date DATE,
    expiry_date DATE,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    remaining_g REAL,
    category TEXT DEFAULT 'other',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES custom_foods(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_pantry_user ON pantry(user_id);
CREATE INDEX IF NOT EXISTS idx_pantry_expiry ON pantry(expiry_date);
CREATE INDEX IF NOT EXISTS idx_pantry_location ON pantry(location);

-- Pantry usage table
CREATE TABLE IF NOT EXISTS pantry_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pantry_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    used_g REAL NOT NULL,
    remaining_after_g REAL,
    used_for_meal_id INTEGER,
    notes TEXT,
    used_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pantry_id) REFERENCES pantry(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (used_for_meal_id) REFERENCES meals(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_pantry_usage_pantry ON pantry_usage(pantry_id);
CREATE INDEX IF NOT EXISTS idx_pantry_usage_date ON pantry_usage(used_at);

-- Trigger: Auto-update pantry remaining_g when usage is logged
CREATE TRIGGER IF NOT EXISTS update_pantry_remaining
AFTER INSERT ON pantry_usage
BEGIN
    UPDATE pantry 
    SET remaining_g = remaining_g - NEW.used_g,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.pantry_id;
END;
```

## 计量单位说明

### unit 字段

`custom_foods.unit` 和 `food_items.unit` 支持两种计量单位：

| 单位 | 含义 | 适用食物 |
|------|------|---------|
| 'g' | 克（重量） | 固体食物：米饭、肉类、蔬菜 |
| 'ml' | 毫升（体积） | 液体食物：牛奶、饮料、汤 |

### 使用规则

1. **营养成分标注**：无论 unit 是 'g' 还是 'ml'，营养成分都按 **每100单位** 计算
   - 牛奶：`unit='ml'`, `calories_per_100g=47` 表示每100ml 47千卡
   - 米饭：`unit='g'`, `calories_per_100g=116` 表示每100g 116千卡

2. **记录餐食时**：
   - 用户输入 `牛奶:250` → 系统记录 `quantity_input=250`, `unit='ml'`
   - 计算时：250ml ≈ 250g（简化处理，忽略密度差异）

3. **默认设置**：
   - 乳制品（dairy）：'ml'
   - 饮料（beverage）：'ml'
   - 其他：'g'