"""
Database Schema Definitions
Centralized column indices to avoid hardcoding throughout the codebase.
"""

# ============================================================================
# Users Table
# ============================================================================
USERS_COLUMNS = {
    'id': 0,
    'username': 1,
    'name': 2,
    'gender': 3,
    'birth_date': 4,
    'height_cm': 5,
    'target_weight_kg': 6,
    'activity_level': 7,
    'goal_type': 8,
    'bmr': 9,
    'tdee': 10,
    'created_at': 11,
    'updated_at': 12,
}

# ============================================================================
# Body Metrics Table - for SELECT recorded_at, weight_kg, bmi, body_fat_pct, notes
# ============================================================================
BODY_METRICS_COLUMNS = {
    'recorded_at': 0,
    'weight_kg': 1,
    'bmi': 2,
    'body_fat_pct': 3,
    'notes': 4,
}

# ============================================================================
# Custom Foods Table
# ============================================================================
CUSTOM_FOODS_COLUMNS = {
    'id': 0,
    'user_id': 1,
    'name': 2,
    'category': 3,
    'unit': 4,
    'calories_per_100g': 5,
    'protein_per_100g': 6,
    'carbs_per_100g': 7,
    'fat_per_100g': 8,
    'fiber_per_100g': 9,
    'sodium_per_100g': 10,
    'barcode': 11,
    'brand': 12,
    'source': 13,
    'storage_method': 14,
    'default_shelf_life_days': 15,
    'created_at': 16,
    'updated_at': 17,
    'calcium_mg': 18,
    'trans_fat_g': 19,
    'saturated_fat_g': 20,
    'sugar_g': 21,
    'vitamin_a_ug': 22,
    'vitamin_c_mg': 23,
    'iron_mg': 24,
    'zinc_mg': 25,
}

# ============================================================================
# Meals Table
# ============================================================================
MEALS_COLUMNS = {
    'id': 0,
    'user_id': 1,
    'meal_type': 2,
    'eaten_at': 3,
    'notes': 4,
    'total_calories': 5,
    'total_protein_g': 6,
    'total_carbs_g': 7,
    'total_fat_g': 8,
    'total_fiber_g': 9,
    'total_sodium_mg': 10,
    'total_calcium_mg': 11,
    'total_trans_fat_g': 12,
    'total_saturated_fat_g': 13,
    'total_sugar_g': 14,
    'total_vitamin_a_ug': 15,
    'total_vitamin_c_mg': 16,
    'total_iron_mg': 17,
    'total_zinc_mg': 18,
}

# ============================================================================
# Food Items Table (meal_foods)
# ============================================================================
FOOD_ITEMS_COLUMNS = {
    'id': 0,
    'meal_id': 1,
    'food_id': 2,
    'food_name': 3,
    'quantity_input': 4,
    'unit': 5,
    'quantity_g': 6,
    'calories': 7,
    'protein_g': 8,
    'carbs_g': 9,
    'fat_g': 10,
    'fiber_g': 11,
    'sodium_mg': 12,
    'calcium_mg': 13,
    'trans_fat_g': 14,
    'saturated_fat_g': 15,
    'sugar_g': 16,
    'vitamin_a_ug': 17,
    'vitamin_c_mg': 18,
    'iron_mg': 19,
    'zinc_mg': 20,
}

# ============================================================================
# Pantry Table - Column indices for SELECT queries
# Note: These map to query column positions, not table schema positions
# ============================================================================
PANTRY_COLUMNS = {
    'id': 0,
    'food_name': 1,
    'quantity_g': 2,
    'remaining_g': 3,
    'quantity_desc': 4,
    'location': 5,
    'purchase_date': 6,
    'expiry_date': 7,
    # Joined columns from custom_foods:
    'calories_per_100g': 8,
    'protein_per_100g': 9,
    'category': 10,
    'unit': 11,
}

# ============================================================================
# Pantry Usage Table
# ============================================================================
PANTRY_USAGE_COLUMNS = {
    'id': 0,
    'pantry_id': 1,
    'user_id': 2,
    'used_g': 3,
    'remaining_after_g': 4,
    'used_for_meal_id': 5,
    'notes': 6,
    'used_at': 7,
}

# ============================================================================
# Default Values
# ============================================================================
DEFAULTS = {
    'location_shelf_life': {
        'fridge': 7,      # 冰箱：7天
        'freezer': 90,    # 冷冻：3个月
        'pantry': 180,    # 干货区：6个月
        'counter': 3,     # 台面：3天
    }
}
