#!/usr/bin/env python3
"""
Initialize Health Coach database for a user.
"""

import argparse
import os
import re
import sqlite3
import sys

# Database schema SQL
SCHEMA_SQL = """
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
    quantity_input REAL,
    unit TEXT DEFAULT 'g',
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
    unit TEXT DEFAULT 'g',
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

-- Pantry (home ingredients inventory)
CREATE TABLE IF NOT EXISTS pantry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    food_name TEXT NOT NULL,
    food_id INTEGER,  -- Reference to custom_foods if matched
    quantity_g REAL,
    quantity_desc TEXT,  -- e.g., "2个", "半颗"
    location TEXT,  -- fridge, freezer, pantry, etc.
    purchase_date DATE,
    expiry_date DATE,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES custom_foods(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_pantry_user ON pantry(user_id);
CREATE INDEX IF NOT EXISTS idx_pantry_expiry ON pantry(expiry_date);
CREATE INDEX IF NOT EXISTS idx_pantry_location ON pantry(location);

-- Insert default user placeholder (will be updated by user_profile.py)
-- This ensures foreign key constraints work even before profile is set
"""

# Common foods seed data
SEED_FOODS_SQL = """
-- Common Chinese foods
INSERT OR IGNORE INTO custom_foods (user_id, name, category, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g) VALUES
(1, '米饭', 'grain', 116, 2.6, 25.0, 0.3),
(1, '馒头', 'grain', 223, 7.0, 47.0, 1.1),
(1, '面条(煮)', 'grain', 110, 4.5, 22.0, 0.5),
(1, '小米粥', 'grain', 46, 1.4, 9.0, 0.3),
(1, '红薯', 'grain', 86, 1.6, 20.0, 0.1),
(1, '鸡胸肉', 'protein', 165, 31.0, 0, 3.6),
(1, '鸡蛋(全蛋)', 'protein', 143, 12.6, 0.7, 9.5),
(1, '鸡蛋白', 'protein', 52, 11.0, 0.7, 0.2),
(1, '牛肉(瘦)', 'protein', 106, 20.2, 0, 2.3),
(1, '猪肉(瘦)', 'protein', 143, 20.3, 1.5, 6.2),
(1, '豆腐(北)', 'protein', 98, 12.2, 1.9, 4.8),
(1, '三文鱼', 'protein', 208, 20.0, 0, 13.0),
(1, '虾仁', 'protein', 85, 20.0, 0, 0.5),
(1, '西兰花', 'vegetable', 34, 2.8, 7.0, 0.4),
(1, '菠菜', 'vegetable', 23, 2.9, 3.6, 0.4),
(1, '西红柿', 'vegetable', 18, 0.9, 3.9, 0.2),
(1, '黄瓜', 'vegetable', 15, 0.7, 3.6, 0.1),
(1, '胡萝卜', 'vegetable', 41, 0.9, 9.6, 0.2),
(1, '白菜', 'vegetable', 13, 1.0, 2.2, 0.2),
(1, '苹果', 'fruit', 52, 0.3, 13.8, 0.2),
(1, '香蕉', 'fruit', 89, 1.1, 22.8, 0.3),
(1, '橙子', 'fruit', 47, 0.9, 11.8, 0.1),
(1, '蓝莓', 'fruit', 57, 0.7, 14.5, 0.3),
(1, '牛奶(全脂)', 'dairy', 61, 3.2, 4.8, 3.3),
(1, '酸奶(原味)', 'dairy', 59, 10.0, 3.6, 0.4),
(1, '橄榄油', 'fat', 884, 0, 0, 100.0),
(1, '花生油', 'fat', 884, 0, 0, 100.0),
(1, '牛油果', 'fat', 160, 2.0, 8.5, 14.7),
(1, '杏仁', 'fat', 579, 21.0, 22.0, 49.9);
"""


def get_data_dir():
    """Get the data directory path."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(skill_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_db_path(username: str) -> str:
    """Get database file path for a user."""
    data_dir = get_data_dir()
    return os.path.join(data_dir, f"{username}.db")


def init_database(db_path: str) -> bool:
    """Initialize database with schema."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute schema
        cursor.executescript(SCHEMA_SQL)
        
        # Create a system user for common foods (id=1)
        cursor.execute('''
            INSERT OR IGNORE INTO users (id, username, display_name) 
            VALUES (1, '__system__', 'System')
        ''')
        
        # Seed common foods
        cursor.executescript(SEED_FOODS_SQL)
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description='Initialize Health Coach database')
    parser.add_argument('--user', required=True, help='Username for database')
    parser.add_argument('--force', action='store_true', help='Overwrite existing database')
    
    args = parser.parse_args()
    
    # Validate username (alphanumeric + underscore + hyphen)
    if not re.match(r'^[a-zA-Z0-9_-]+$', args.user):
        print(json.dumps({
            "status": "error",
            "error": "invalid_username",
            "message": "Username must contain only letters, numbers, underscore, or hyphen"
        }))
        sys.exit(1)
    
    db_path = get_db_path(args.user)
    
    # Check if exists
    if os.path.exists(db_path) and not args.force:
        print(json.dumps({
            "status": "error",
            "error": "database_exists",
            "message": f"Database already exists: {db_path}. Use --force to overwrite."
        }))
        sys.exit(1)
    
    # Remove if force
    if args.force and os.path.exists(db_path):
        os.remove(db_path)
    
    # Initialize
    if init_database(db_path):
        print(json.dumps({
            "status": "success",
            "data": {"database_path": db_path},
            "message": f"Created database: {db_path}"
        }))
    else:
        print(json.dumps({
            "status": "error",
            "error": "init_failed",
            "message": "Failed to initialize database"
        }))
        sys.exit(1)


if __name__ == '__main__':
    import json
    main()