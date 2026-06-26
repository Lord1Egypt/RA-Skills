#!/usr/bin/env python3
"""
Meal logging for Health Coach.
"""

import argparse
import json
import os
import sqlite3
import sys
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple

from db_schema import (
    USERS_COLUMNS as UC,
    MEALS_COLUMNS as MC,
    FOOD_ITEMS_COLUMNS as FIC,
    CUSTOM_FOODS_COLUMNS as FC,
    DEFAULTS
)


def get_db_path(username: str) -> str:
    """Get database file path for a user."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(skill_dir, 'data')
    return os.path.join(data_dir, f"{username}.db")


def parse_food_string(food_str: str) -> List[Tuple[str, float]]:
    """Parse food string like '米饭:150g, 鸡胸肉:100g' into list of tuples."""
    foods = []
    # Split by comma or Chinese comma
    items = re.split(r'[,，]', food_str)
    
    for item in items:
        item = item.strip()
        if not item:
            continue
        
        # Match pattern: name:quantity or name:quantityg or name:数量g
        match = re.match(r'(.+?)[:：]\s*(\d+(?:\.\d+)?)\s*[g克]?', item)
        if match:
            name = match.group(1).strip()
            quantity = float(match.group(2))
            foods.append((name, quantity))
        else:
            # Try to extract just the name, assume 100g
            foods.append((item, 100))
    
    return foods


def search_food_nutrition(conn: sqlite3.Connection, food_name: str) -> Dict[str, Any]:
    """Search for food nutrition in database."""
    cursor = conn.cursor()
    
    # Try exact match first - use all columns to match db_schema
    cursor.execute('''
        SELECT *
        FROM custom_foods
        WHERE name = ? OR name LIKE ?
        LIMIT 1
    ''', (food_name, f'%{food_name}%'))
    
    row = cursor.fetchone()
    
    if row:
        return {
            "name": row[FC['name']],
            "unit": row[FC['unit']] or 'g',
            "calories_per_100g": row[FC['calories_per_100g']],
            "protein_per_100g": row[FC['protein_per_100g']],
            "carbs_per_100g": row[FC['carbs_per_100g']],
            "fat_per_100g": row[FC['fat_per_100g']],
            "fiber_per_100g": row[FC['fiber_per_100g']] or 0,
            "sodium_per_100g": row[FC['sodium_per_100g']] or 0,
            "calcium_mg": row[FC['calcium_mg']] or 0,
            "trans_fat_g": row[FC['trans_fat_g']] or 0,
            "saturated_fat_g": row[FC['saturated_fat_g']] or 0,
            "sugar_g": row[FC['sugar_g']] or 0,
            "vitamin_a_ug": row[FC['vitamin_a_ug']] or 0,
            "vitamin_c_mg": row[FC['vitamin_c_mg']] or 0,
            "iron_mg": row[FC['iron_mg']] or 0,
            "zinc_mg": row[FC['zinc_mg']] or 0
        }
    
    # Return default/unknown
    return {
        "name": food_name,
        "unit": 'g',
        "calories_per_100g": 0,
        "protein_per_100g": 0,
        "carbs_per_100g": 0,
        "fat_per_100g": 0,
        "fiber_per_100g": 0,
        "sodium_per_100g": 0,
        "calcium_mg": 0,
        "trans_fat_g": 0,
        "saturated_fat_g": 0,
        "sugar_g": 0,
        "vitamin_a_ug": 0,
        "vitamin_c_mg": 0,
        "iron_mg": 0,
        "zinc_mg": 0,
        "unknown": True
    }


def calculate_nutrition(food_nutrition: Dict[str, Any], quantity_g: float) -> Dict[str, float]:
    """Calculate nutrition for a specific quantity."""
    ratio = quantity_g / 100
    return {
        "calories": round(food_nutrition["calories_per_100g"] * ratio, 2),
        "protein_g": round(food_nutrition["protein_per_100g"] * ratio, 2),
        "carbs_g": round(food_nutrition["carbs_per_100g"] * ratio, 2),
        "fat_g": round(food_nutrition["fat_per_100g"] * ratio, 2),
        "fiber_g": round(food_nutrition.get("fiber_per_100g", 0) * ratio, 2),
        "sodium_mg": round(food_nutrition.get("sodium_per_100g", 0) * ratio, 2),
        "calcium_mg": round(food_nutrition.get("calcium_mg", 0) * ratio, 2),
        "trans_fat_g": round(food_nutrition.get("trans_fat_g", 0) * ratio, 2),
        "saturated_fat_g": round(food_nutrition.get("saturated_fat_g", 0) * ratio, 2),
        "sugar_g": round(food_nutrition.get("sugar_g", 0) * ratio, 2),
        "vitamin_a_ug": round(food_nutrition.get("vitamin_a_ug", 0) * ratio, 2),
        "vitamin_c_mg": round(food_nutrition.get("vitamin_c_mg", 0) * ratio, 2),
        "iron_mg": round(food_nutrition.get("iron_mg", 0) * ratio, 2),
        "zinc_mg": round(food_nutrition.get("zinc_mg", 0) * ratio, 2)
    }


def log_meal(args) -> Dict[str, Any]:
    """Log a meal."""
    db_path = get_db_path(args.user)
    
    if not os.path.exists(db_path):
        return {
            "status": "error",
            "error": "database_not_found",
            "message": f"Database not found. Run: python3 scripts/init_db.py --user {args.user}"
        }
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get user ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (args.user,))
        user_row = cursor.fetchone()
        
        if not user_row:
            return {"status": "error", "error": "user_not_found", "message": "User not found"}
        
        user_id = user_row[UC["id"]]
        
        # Parse foods
        foods = parse_food_string(args.foods)
        
        if not foods:
            return {"status": "error", "error": "invalid_foods", "message": "Could not parse food string"}
        
        # Determine meal time
        if args.time:
            today = datetime.now().strftime('%Y-%m-%d')
            eaten_at = f"{today} {args.time}:00"
        else:
            eaten_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insert meal record
        cursor.execute('''
            INSERT INTO meals (user_id, meal_type, eaten_at, notes, total_calories, total_protein_g, total_carbs_g, total_fat_g, total_fiber_g, total_sodium_mg)
            VALUES (?, ?, ?, ?, 0, 0, 0, 0, 0, 0)
        ''', (user_id, args.meal_type, eaten_at, args.notes))
        
        meal_id = cursor.lastrowid
        
        # Process each food item
        food_items = []
        totals = {"calories": 0, "protein_g": 0, "carbs_g": 0, "fat_g": 0, "fiber_g": 0, "sodium_mg": 0}
        unknown_foods = []
        
        for food_name, quantity_input in foods:
            nutrition_info = search_food_nutrition(conn, food_name)
            unit = nutrition_info.get("unit", "g")
            # For now, treat ml same as g for calculation (1ml ≈ 1g for most liquids)
            quantity_g = quantity_input
            calculated = calculate_nutrition(nutrition_info, quantity_g)
            
            if nutrition_info.get("unknown"):
                unknown_foods.append(food_name)
            
            # Insert food item
            cursor.execute('''
                INSERT INTO food_items (meal_id, food_name, quantity_input, unit, quantity_g, calories, protein_g, carbs_g, fat_g, fiber_g, sodium_mg, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                meal_id,
                nutrition_info["name"],
                quantity_input,
                unit,
                quantity_g,
                calculated["calories"],
                calculated["protein_g"],
                calculated["carbs_g"],
                calculated["fat_g"],
                calculated["fiber_g"],
                calculated["sodium_mg"],
                "database" if not nutrition_info.get("unknown") else "unknown"
            ))
            
            food_items.append({
                "name": nutrition_info["name"],
                "quantity_input": quantity_input,
                "unit": unit,
                "quantity_g": quantity_g,
                "nutrition": calculated
            })
            
            # Accumulate totals
            for key in totals:
                totals[key] += calculated[key]
        
        # Update meal totals
        cursor.execute('''
            UPDATE meals SET
                total_calories = ?,
                total_protein_g = ?,
                total_carbs_g = ?,
                total_fat_g = ?,
                total_fiber_g = ?,
                total_sodium_mg = ?
            WHERE id = ?
        ''', (
            round(totals["calories"], 2),
            round(totals["protein_g"], 2),
            round(totals["carbs_g"], 2),
            round(totals["fat_g"], 2),
            round(totals["fiber_g"], 2),
            round(totals["sodium_mg"], 2),
            meal_id
        ))
        
        conn.commit()
        
        result = {
            "status": "success",
            "data": {
                "meal_id": meal_id,
                "meal_type": args.meal_type,
                "eaten_at": eaten_at,
                "foods": food_items,
                "totals": {k: round(v, 2) for k, v in totals.items()}
            },
            "message": f"Logged {args.meal_type} with {len(food_items)} items, {round(totals['calories'])} kcal"
        }
        
        if unknown_foods:
            result["data"]["unknown_foods"] = unknown_foods
            result["message"] += f". Unknown foods: {', '.join(unknown_foods)}"
        
        return result
        
    except sqlite3.Error as e:
        return {"status": "error", "error": "database_error", "message": str(e)}
    finally:
        conn.close()


def list_meals(args) -> Dict[str, Any]:
    """List meals."""
    db_path = get_db_path(args.user)
    
    if not os.path.exists(db_path):
        return {"status": "error", "error": "database_not_found", "message": "Database not found"}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT id FROM users WHERE username = ?', (args.user,))
        user_row = cursor.fetchone()
        
        if not user_row:
            return {"status": "error", "error": "user_not_found", "message": "User not found"}
        
        user_id = user_row[UC["id"]]
        
        # Build query
        query = '''
            SELECT id, user_id, meal_type, eaten_at, notes, total_calories, total_protein_g, total_carbs_g, total_fat_g,
                   total_fiber_g, total_sodium_mg, total_calcium_mg, total_trans_fat_g, total_saturated_fat_g,
                   total_sugar_g, total_vitamin_a_ug, total_vitamin_c_mg, total_iron_mg, total_zinc_mg
            FROM meals
            WHERE user_id = ?
        '''
        params = [user_id]
        
        if args.date:
            query += ' AND DATE(eaten_at) = ?'
            params.append(args.date)
        elif args.days:
            start_date = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')
            query += ' AND eaten_at >= ?'
            params.append(start_date)
        
        if args.meal_type:
            query += ' AND meal_type = ?'
            params.append(args.meal_type)
        
        query += ' ORDER BY eaten_at DESC'
        
        if not args.days and not args.date:
            query += ' LIMIT 20'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        meals = []
        for row in rows:
            meals.append({
                "id": row[MC['id']],
                "meal_type": row[MC['meal_type']],
                "eaten_at": row[MC['eaten_at']],
                "notes": row[MC['notes']],
                "total_calories": row[MC['total_calories']],
                "total_protein_g": row[MC['total_protein_g']],
                "total_carbs_g": row[MC['total_carbs_g']],
                "total_fat_g": row[MC['total_fat_g']]
            })
        
        return {
            "status": "success",
            "data": {
                "count": len(meals),
                "meals": meals
            }
        }
        
    except sqlite3.Error as e:
        return {"status": "error", "error": "database_error", "message": str(e)}
    finally:
        conn.close()


def daily_summary(args) -> Dict[str, Any]:
    """Get daily nutrition summary."""
    db_path = get_db_path(args.user)
    
    if not os.path.exists(db_path):
        return {"status": "error", "error": "database_not_found", "message": "Database not found"}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT id, tdee FROM users WHERE username = ?', (args.user,))
        user_row = cursor.fetchone()
        
        if not user_row:
            return {"status": "error", "error": "user_not_found", "message": "User not found"}
        
        user_id, tdee = user_row
        
        date = args.date or datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT meal_type, total_calories, total_protein_g, total_carbs_g, total_fat_g, total_sodium_mg
            FROM meals
            WHERE user_id = ? AND DATE(eaten_at) = ?
        ''', (user_id, date))
        
        rows = cursor.fetchall()
        
        totals = {"calories": 0, "protein_g": 0, "carbs_g": 0, "fat_g": 0, "sodium_mg": 0}
        by_meal = {}
        
        for row in rows:
            meal_type = row[0]
            by_meal[meal_type] = {
                "calories": row[1],
                "protein_g": row[2],
                "carbs_g": row[3],
                "fat_g": row[4],
                "sodium_mg": row[5]
            }
            totals["calories"] += (row[1] or 0)
            totals["protein_g"] += (row[2] or 0)
            totals["carbs_g"] += (row[3] or 0)
            totals["fat_g"] += (row[4] or 0)
            totals["sodium_mg"] += (row[5] or 0)
        
        remaining = (tdee or 2000) - totals["calories"]
        
        return {
            "status": "success",
            "data": {
                "date": date,
                "totals": {k: round(v, 2) for k, v in totals.items()},
                "by_meal": by_meal,
                "tdee": tdee,
                "remaining_calories": round(remaining, 2),
                "meals_count": len(rows)
            }
        }
        
    except sqlite3.Error as e:
        return {"status": "error", "error": "database_error", "message": str(e)}
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='Meal logging')
    parser.add_argument('--user', required=True, help='Username')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Log meal
    log_parser = subparsers.add_parser('log', help='Log a meal')
    log_parser.add_argument('--meal-type', required=True, 
                           choices=['breakfast', 'lunch', 'dinner', 'snack'],
                           help='Meal type')
    log_parser.add_argument('--foods', required=True, 
                           help='Foods (format: "name:gram,name:gram")')
    log_parser.add_argument('--time', help='Time (HH:MM)')
    log_parser.add_argument('--notes', help='Notes')
    
    # List meals
    list_parser = subparsers.add_parser('list', help='List meals')
    list_parser.add_argument('--date', help='Specific date (YYYY-MM-DD)')
    list_parser.add_argument('--meal-type', choices=['breakfast', 'lunch', 'dinner', 'snack'])
    list_parser.add_argument('--days', type=int, help='Last N days')
    
    # Daily summary
    summary_parser = subparsers.add_parser('daily-summary', help='Get daily summary')
    summary_parser.add_argument('--date', help='Date (YYYY-MM-DD), defaults to today')
    
    args = parser.parse_args()
    
    if args.command == 'log':
        result = log_meal(args)
    elif args.command == 'list':
        result = list_meals(args)
    elif args.command == 'daily-summary':
        result = daily_summary(args)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2, default=str))
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
