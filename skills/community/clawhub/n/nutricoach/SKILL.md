---
name: nutricoach
description: |
  Personal health data management and intelligent diet recommendation system.
  Use when users need to:
  - Record and track body metrics (weight, height, BMI, body fat)
  - Log daily meals and dietary intake
  - Query food nutrition information
  - Get personalized diet recommendations based on health goals
  - Analyze nutrition trends and generate reports
  - Identify foods from photos and estimate nutritional content
  - Manage pantry inventory and track food expiration
  - Get smart recipe recommendations based on available ingredients
  - Export data and create backups

  Supports multi-user data isolation, time-series tracking, extensible food database,
  OCR food recognition, and web dashboard visualization.
---

# NutriCoach Skill

A comprehensive personal health management system for tracking body metrics, logging meals, analyzing nutrition, managing pantry inventory, and receiving intelligent diet recommendations.

## Quick Start

### 1. Initialize Database

```bash
python3 scripts/init_db.py --user <username>
```

Creates isolated SQLite database for the user with all required tables.

### 2. Set Up User Profile

```bash
python3 scripts/user_profile.py --user <username> set \
  --name "Robert" \
  --gender male \
  --birth-date 1994-05-15 \
  --height-cm 175 \
  --target-weight 70 \
  --activity-level moderate \
  --goal-type maintain
```

### 3. Log Daily Weight

```bash
python3 scripts/body_metrics.py --user <username> log-weight --weight 72.5
```

### 4. Log a Meal

```bash
python3 scripts/meal_logger.py --user <username> log \
  --meal-type lunch \
  --foods "米饭:150g, 鸡胸肉:100g, 西兰花:100g"
```

### 5. Get Diet Recommendation

```bash
python3 scripts/diet_recommender.py --user <username> recommend --meal-type dinner
```

### 6. Launch Web Dashboard

```bash
python3 scripts/launch_dashboard.py --user <username>
```

Opens browser at http://127.0.0.1:5000 with visual health data overview.

## Core Features

### 📊 Body Metrics Tracking
- Weight logging with automatic BMI calculation
- Body fat percentage tracking
- 7/30-day trend analysis
- TDEE (Total Daily Energy Expenditure) calculation

### 🍽️ Meal Logging
- Natural language food entry: `米饭:150g, 鸡胸肉:100g`
- Automatic nutrition calculation
- Daily summary with remaining calories vs TDEE
- 569 built-in Chinese foods database

### 📷 OCR Food Recognition
- Scan food packaging with camera
- Extract nutrition facts automatically
- Barcode matching for existing products
- Support for Kimi Vision and macOS Vision engines

### 🥬 Pantry Management
- Track inventory by storage location (fridge/freezer/dry goods/counter)
- Expiration date tracking with alerts
- Automatic quantity deduction when logging meals
- Category-based organization (protein/vegetable/carb/fruit/dairy)

### 🍳 Smart Recipe Recommendations
- Generate recipes based on available pantry items
- Prioritize ingredients nearing expiration
- Match recipes to nutritional gaps
- Dynamic threshold adjustment based on inventory levels

### 📈 Web Dashboard (v2)
- Tabbed interface: Overview / Pantry / Weight History
- Visual charts for weight and nutrition trends
- Interactive pantry management
- One-click recipe generation

### 💾 Data Management
- JSON/CSV export
- Automatic database backups (keeps last 10)
- Easy restore from backup
- Multi-user data isolation

## Architecture

See [references/ARCHITECTURE.md](references/ARCHITECTURE.md) for system design and data flow.

## Database Schema

See [references/DATABASE_SCHEMA.md](references/DATABASE_SCHEMA.md) for complete ER diagram and table definitions.

## Feature Guide

See [references/FEATURE_GUIDE.md](references/FEATURE_GUIDE.md) for detailed user-facing documentation including:
- Complete feature descriptions
- OCR food recognition workflow
- Pantry management guide
- Smart recipe recommendations
- Web dashboard usage
- Quick command reference

## Developer Guide

See [references/DEVELOPER_GUIDE.md](references/DEVELOPER_GUIDE.md) for:
- Complete API reference for all scripts
- Food database structure
- Database schema details
- Extension guidelines

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and breaking changes.

## Available Scripts

| Script | Purpose |
|--------|---------|
| `init_db.py` | Initialize user database |
| `user_profile.py` | Manage user profile and goals |
| `body_metrics.py` | Log weight and track trends |
| `meal_logger.py` | Log meals and view daily summary |
| `diet_recommender.py` | Get meal recommendations |
| `food_analyzer.py` | Search foods, OCR scan, add custom |
| `pantry_manager.py` | Manage ingredient inventory |
| `smart_recipe.py` | Generate recipes from pantry |
| `launch_dashboard.py` | Start web dashboard |
| `report_generator.py` | Generate weekly/nutrition reports |
| `export_data.py` | Export to JSON/CSV |
| `backup_db.py` | Backup and restore database |
| `food_ocr.py` | OCR engine wrapper |
| `food_matcher.py` | Match OCR results to database |
| `migrate_db.py` | Database migration tool |

## Data Storage

Each user has an isolated SQLite database stored at:
```
~/.openclaw/workspace/skills/nutricoach/data/<username>.db
```

Backups are stored in:
```
~/.openclaw/workspace/skills/nutricoach/data/backups/
```

## Common Workflows

### Daily Logging Workflow
1. Morning: Log weight with `body_metrics.py log-weight`
2. After meals: Log food with `meal_logger.py log`
3. Evening: Review daily nutrition summary

### Weekly Review Workflow
1. Generate weekly report with `report_generator.py weekly`
2. Check weight trend
3. Adjust targets if needed with `user_profile.py update`

### Photo Food Recognition Workflow
1. Save food photo to accessible path
2. Run: `python3 scripts/food_analyzer.py --user <username> scan --image <path>`
3. Review identified foods and confirm/edit quantities
4. Log confirmed foods with `meal_logger.py log`

### Pantry Management Workflow
1. Add groceries: `pantry_manager.py add --food "鸡胸肉" --quantity 500`
2. Log meals (auto-deducts from pantry)
3. Check expiring items: `pantry_manager.py list --expiring 3`
4. Get recipe ideas: `smart_recipe.py --count 3`

### Web Dashboard Workflow
1. Launch: `launch_dashboard.py --user <username>`
2. Browse Overview tab for trends
3. Manage Pantry tab for inventory
4. Use smart recipe buttons directly from pantry view

## Configuration

### OCR Engine Setup

OCR 食品包装识别支持多种方式，**零配置即可使用**。

#### 方式一：AI 助手识别（推荐，零配置）

如果你使用 AI 助手（如 OpenClaw），直接发送食品包装图片：

```
[发送图片]
"录入这个食材，生产日期 2025-01-15"
```

助手会直接识别图片并录入，**无需任何配置**。

#### 方式二：本地识别（命令行，免费）

使用 macOS 内置 Vision 框架，无需配置：
```bash
python3 scripts/food_analyzer.py --user <name> scan --image food.jpg --engine macos
```

#### 方式三：云端识别（命令行，可选）

如需更高识别精度，配置云端 Vision API：

**步骤 1：创建配置文件**
```bash
cp data/user_config.example.yaml data/user_config.yaml
```

**步骤 2：填入 API key**
```yaml
vision:
  api_key: "your-api-key"
  base_url: "https://api.moonshot.cn/v1"  # 或其他兼容 OpenAI 的 API
  model: "kimi-k2.5"
```

**步骤 3：使用**
```bash
python3 scripts/food_analyzer.py --user <name> scan --image food.jpg
```

**支持的 API 提供商：**
- Moonshot (Kimi)
- OpenAI
- 阿里 DashScope
- 其他兼容 OpenAI 接口的服务

**说明：**
- `user_config.yaml` 已被加入 `.gitignore`，不会意外提交
- 云端 OCR 仅在命令行模式下需要配置
- AI 助手模式始终优先使用助手内置的视觉能力

## Food Database

Built-in database includes 569 Chinese foods across categories:
- **Proteins**: 鸡胸肉, 牛肉, 鸡蛋, 豆腐, etc.
- **Vegetables**: 西兰花, 菠菜, 西红柿, etc.
- **Carbs**: 米饭, 燕麦, 红薯, etc.
- **Fruits**: 苹果, 香蕉, 橙子, etc.
- **Dairy**: 牛奶, 酸奶, 奶酪, etc.

Add custom foods via OCR scan or manual entry.

---

*Last updated: 2026-03-28 (v2.0: Added pantry management, smart recipes, OCR, web dashboard)*
