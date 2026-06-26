# Hardcoding Audit Report

## Summary

**Total hardcoded row indices found**: 142 occurrences across 15 files

## Issues Found

### 1. Database Column Indices (Critical)

Files with hardcoded `row[n]` indices:
- `pantry_manager.py`: ~25 occurrences
- `meal_logger.py`: ~20 occurrences  
- `export_data.py`: ~18 occurrences
- `food_analyzer.py`: ~15 occurrences
- `diet_recommender.py`: ~12 occurrences
- `body_metrics.py`: ~10 occurrences
- Other files: ~42 occurrences

**Risk**: If table schema changes, all indices become wrong.

### 2. Magic Numbers

- Port numbers: `5000` (now fixed to `8080`)
- Default heights: `170.0` cm
- Shelf life defaults: `7`, `90`, `30`, `5` days
- Activity multipliers: `1.2`, `1.375`, `1.55`, etc.
- Macro splits: `30`, `40`, `30` percent

### 3. String Literals

- Location names: `'fridge'`, `'freezer'`, `'pantry'`, `'counter'`
- Category names: `'protein'`, `'vegetable'`, `'carb'`, etc.
- Meal types: `'breakfast'`, `'lunch'`, `'dinner'`, `'snack'`

## Solution Implemented

### 1. Created `db_schema.py` (New File)

Centralized schema definitions:
- `USERS_COLUMNS`: Column name -> index mapping
- `BODY_METRICS_COLUMNS`: Column name -> index mapping
- `CUSTOM_FOODS_COLUMNS`: Column name -> index mapping
- `MEALS_COLUMNS`: Column name -> index mapping
- `FOOD_ITEMS_COLUMNS`: Column name -> index mapping
- `PANTRY_COLUMNS`: Column name -> index mapping
- `PANTRY_USAGE_COLUMNS`: Column name -> index mapping
- `get_col(table, column)`: Helper function

### 2. Created `config.py` (Consolidated)

Already exists in `scripts/web/config.py`, should be moved to root:
- `LOCATION_MAP`: Chinese -> English mapping
- `REVERSE_LOCATION_MAP`: English -> Chinese mapping
- `FOOD_STORAGE_DEFAULTS`: Food -> storage location
- `ACTIVITY_MULTIPLIERS`: Activity level -> TDEE multiplier
- `GOAL_ADJUSTMENTS`: Goal type -> calorie adjustment

### 3. Default Values

Should be centralized:
- `DEFAULTS['user_height_cm']`: 170.0
- `DEFAULTS['location_shelf_life']`: {fridge: 7, freezer: 90, pantry: 30, counter: 5}
- `DEFAULTS['macro_split']`: {protein: 30, carbs: 40, fat: 30}

## Migration Plan

### Phase 1: Core Files (High Priority)
- [ ] `pantry_manager.py` - Use `db_schema.PANTRY_COLUMNS`
- [ ] `meal_logger.py` - Use `db_schema.MEALS_COLUMNS` and `db_schema.FOOD_ITEMS_COLUMNS`
- [ ] `body_metrics.py` - Use `db_schema.BODY_METRICS_COLUMNS`

### Phase 2: Supporting Files (Medium Priority)
- [ ] `food_analyzer.py` - Use `db_schema.CUSTOM_FOODS_COLUMNS`
- [ ] `diet_recommender.py` - Use `db_schema.CUSTOM_FOODS_COLUMNS`
- [ ] `export_data.py` - Use all relevant schemas

### Phase 3: Remaining Files (Low Priority)
- [ ] `user_profile.py`
- [ ] `report_generator.py`
- [ ] `smart_recipe.py`
- [ ] Other utility scripts

## Example Migration

**Before**:
```python
items.append({
    "id": row[0],
    "food_name": row[1],
    "quantity": row[2],
    "location": row[5],
})
```

**After**:
```python
from db_schema import PANTRY_COLUMNS as PC

items.append({
    "id": row[PC['id']],
    "food_name": row[PC['food_name']],
    "quantity": row[PC['quantity_g']],
    "location": row[PC['location']],
})
```

Or using helper:
```python
from db_schema import get_col

items.append({
    "id": row[get_col('pantry', 'id')],
    "food_name": row[get_col('pantry', 'food_name')],
})
```

## Prevention

Add to AGENTS.md:
- Never hardcode `row[n]` indices
- Always use schema definitions from `db_schema.py`
- When modifying SQL queries, update `db_schema.py` first
