# NutriCoach Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface                          │
│              (CLI Scripts / Agent Conversation)              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Core Services Layer                       │
├─────────────┬─────────────┬─────────────┬───────────────────┤
│   User      │   Body      │   Meal      │   Diet            │
│   Profile   │   Metrics   │   Logger    │   Recommender     │
│   Service   │   Service   │   Service   │   Service         │
└──────┬──────┴──────┬──────┴──────┬──────┴─────────┬─────────┘
       │             │             │                │
       └─────────────┴──────┬──────┴────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Access Layer                         │
│              (SQLite with repository pattern)                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Storage Layer                        │
│         (User-isolated SQLite databases)                     │
│    ~/.openclaw/workspace/skills/nutricoach/data/*.db       │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Profile Setup Flow

```
User Input → Validation → Calculate BMR/TDEE → Store in users table
                                              ↓
                                    Initialize related tables
```

### 2. Daily Weight Logging Flow

```
Weight Input → Validate → Calculate BMI → Store in body_metrics
                ↓                              ↓
            Check range                  Update user stats
            anomalies
```

### 3. Meal Logging Flow

```
Food Input → Parse foods → Query nutrition DB → Calculate totals
    ↓                                              ↓
Photo? → Vision API → Identify food → Confirm → Store in meals
                                                food_items
```

### 4. Recommendation Flow

```
User Goal + History → Calculate needs → Query suitable foods
         ↓                                    ↓
   Current intake                      Filter by preferences
         ↓                                    ↓
   Remaining budget → Generate options → Rank by nutrition
```

## Extensibility Points

### 1. Nutrition Data Sources

```python
# Interface: NutritionProvider
class NutritionProvider:
    def search(self, food_name: str) -> List[FoodItem]
    def get_by_id(self, food_id: str) -> FoodItem
    def batch_import(self, data: List[Dict]) -> int

# Implementations:
# - USDAFoodProvider (USDA FoodData Central API)
# - CNFoodProvider (中国食物成分表)
# - CustomFoodProvider (用户自定义)
```

### 2. Recommendation Algorithms

```python
# Interface: RecommendationEngine
class RecommendationEngine:
    def recommend(self, user: User, meal_type: str, constraints: Dict) -> List[MealOption]

# Implementations:
# - BalancedMacroEngine (均衡宏量营养素)
# - LowCarbEngine (低碳)
# - HighProteinEngine (高蛋白)
# - CalorieDeficitEngine (热量缺口)
```

### 3. Analysis Reports

```python
# Interface: ReportGenerator
class ReportGenerator:
    def generate(self, user: User, period: str) -> Report

# Implementations:
# - WeeklySummaryReport
# - MonthlyTrendReport
# - NutritionAnalysisReport
# - GoalProgressReport
```

## Multi-User Isolation

Each user has a dedicated database file:

```
data/
├── robert.db          # Robert's health data
├── alice.db           # Alice's health data
└── bob.db             # Bob's health data
```

Benefits:
- True data isolation
- Easy backup/restore per user
- No schema migration complexity
- Portable (single file per user)

## Configuration

### User Configuration

User-specific config: `data/user_config.yaml` (not in git)

```yaml
# Vision OCR Configuration (Optional)
vision:
  api_key: "your-api-key"
  base_url: "https://api.moonshot.cn/v1"
  model: "kimi-k2.5"
```

**Priority**: Environment variable > Config file > Default (local OCR)

### Global Defaults

Default values are hardcoded in scripts:
- BMR formula: Mifflin-St Jeor
- Activity multipliers: standard values
- Macro split: 30/40/30 (protein/carbs/fat)
- Data retention: 365 days
