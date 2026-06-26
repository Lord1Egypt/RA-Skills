#!/usr/bin/env python3
"""
Diet recommendation engine for NutriCoach.
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime
from typing import Dict, Any, List

from db_schema import (
    USERS_COLUMNS as UC,
    CUSTOM_FOODS_COLUMNS as FC,
    DEFAULTS
)


def get_db_path(username: str) -> str:
    """Get database file path for a user."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(skill_dir, 'data')
    return os.path.join(data_dir, f"{username}.db")


def get_user_targets(conn: sqlite3.Connection, username: str) -> Dict[str, Any]:
    """Get user's nutrition targets."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tdee, goal_type, target_weight_kg, height_cm
        FROM users WHERE username = ?
    ''', (username,))
    row = cursor.fetchone()
    
    if not row:
        return None
    
    tdee, goal_type, target_weight, height_cm = row
    
    # Adjust calories based on goal
    if goal_type == 'lose':
        target_calories = tdee - 500  # 500 cal deficit for ~0.5kg/week loss
    elif goal_type == 'gain':
        target_calories = tdee + 300  # 300 cal surplus for muscle gain
    else:
        target_calories = tdee
    
    # Default macro split (40/30/30)
    protein_pct = 30
    carbs_pct = 40
    fat_pct = 30
    
    # Calculate macros
    protein_g = round((target_calories * protein_pct / 100) / 4)
    carbs_g = round((target_calories * carbs_pct / 100) / 4)
    fat_g = round((target_calories * fat_pct / 100) / 9)
    
    return {
        "target_calories": round(target_calories),
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fat_g": fat_g,
        "goal_type": goal_type
    }


def get_today_intake(conn: sqlite3.Connection, user_id: int) -> Dict[str, float]:
    """Get today's nutrition intake."""
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT SUM(total_calories), SUM(total_protein_g), SUM(total_carbs_g), SUM(total_fat_g)
        FROM meals
        WHERE user_id = ? AND DATE(eaten_at) = ?
    ''', (user_id, today))
    
    row = cursor.fetchone()

    # Query: SUM(total_calories), SUM(total_protein_g), SUM(total_carbs_g), SUM(total_fat_g)
    return {
        "calories": row[0] or 0,
        "protein_g": row[1] or 0,
        "carbs_g": row[2] or 0,
        "fat_g": row[3] or 0
    }


def get_remaining_budget(targets: Dict[str, Any], intake: Dict[str, float]) -> Dict[str, float]:
    """Calculate remaining nutrition budget for the day."""
    return {
        "calories": max(0, targets["target_calories"] - intake["calories"]),
        "protein_g": max(0, targets["protein_g"] - intake["protein_g"]),
        "carbs_g": max(0, targets["carbs_g"] - intake["carbs_g"]),
        "fat_g": max(0, targets["fat_g"] - intake["fat_g"])
    }


def get_food_by_category(conn: sqlite3.Connection, category: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Get foods by category."""
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g
        FROM custom_foods
        WHERE category = ?
        ORDER BY name
        LIMIT ?
    ''', (category, limit))
    
    rows = cursor.fetchall()
    
    foods = []
    for row in rows:
        foods.append({
            "name": row[FC['name']],
            "calories_per_100g": row[FC['calories_per_100g']],
            "protein_per_100g": row[FC['protein_per_100g']],
            "carbs_per_100g": row[FC['carbs_per_100g']],
            "fat_per_100g": row[FC['fat_per_100g']]
        })
    
    return foods


def recommend_meal(args) -> Dict[str, Any]:
    """Generate meal recommendations."""
    db_path = get_db_path(args.user)
    
    if not os.path.exists(db_path):
        return {"status": "error", "error": "database_not_found", "message": "Database not found"}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get user info
        cursor.execute('SELECT id FROM users WHERE username = ?', (args.user,))
        user_row = cursor.fetchone()
        
        if not user_row:
            return {"status": "error", "error": "user_not_found", "message": "User not found"}
        
        user_id = user_row[UC["id"]]
        
        # Get targets and current intake
        targets = get_user_targets(conn, args.user)
        intake = get_today_intake(conn, user_id)
        remaining = get_remaining_budget(targets, intake)
        
        # Estimate meal calorie target
        meal_targets = {
            'breakfast': 0.25,
            'lunch': 0.35,
            'dinner': 0.30,
            'snack': 0.10
        }
        
        meal_ratio = meal_targets.get(args.meal_type, 0.25)
        target_meal_calories = (targets["target_calories"] * meal_ratio) if not args.calories else args.calories
        
        # Don't exceed remaining budget
        target_meal_calories = min(target_meal_calories, remaining["calories"])
        
        # Get foods by category
        proteins = get_food_by_category(conn, 'protein')
        grains = get_food_by_category(conn, 'grain')
        vegetables = get_food_by_category(conn, 'vegetable')
        
        # Generate simple meal combinations
        recommendations = []
        
        for i in range(min(args.count or 3, 5)):
            if not proteins or not grains:
                break
            
            protein = proteins[i % len(proteins)]
            grain = grains[i % len(grains)]
            veg = vegetables[i % len(vegetables)] if vegetables else None
            
            # Calculate portions to hit target calories
            # Simplified: assume 150g protein, 200g grain, 150g veg
            portion_protein_g = 150
            portion_grain_g = 200
            portion_veg_g = 150 if veg else 0
            
            protein_cals = (protein["calories_per_100g"] * portion_protein_g / 100)
            grain_cals = (grain["calories_per_100g"] * portion_grain_g / 100)
            veg_cals = (veg["calories_per_100g"] * portion_veg_g / 100) if veg else 0
            
            total_cals = protein_cals + grain_cals + veg_cals
            
            meal = {
                "name": f"{protein['name']} + {grain['name']}" + (f" + {veg['name']}" if veg else ""),
                "foods": [
                    {"name": protein["name"], "quantity_g": portion_protein_g, "calories": round(protein_cals)},
                    {"name": grain["name"], "quantity_g": portion_grain_g, "calories": round(grain_cals)}
                ],
                "total_calories": round(total_cals),
                "protein_g": round((protein["protein_per_100g"] * portion_protein_g / 100)),
                "carbs_g": round((grain["carbs_per_100g"] * portion_grain_g / 100))
            }
            
            if veg:
                meal["foods"].append({"name": veg["name"], "quantity_g": portion_veg_g, "calories": round(veg_cals)})
            
            recommendations.append(meal)
        
        return {
            "status": "success",
            "data": {
                "meal_type": args.meal_type,
                "target_calories": round(target_meal_calories),
                "remaining_daily": {
                    "calories": round(remaining["calories"]),
                    "protein_g": round(remaining["protein_g"]),
                    "carbs_g": round(remaining["carbs_g"]),
                    "fat_g": round(remaining["fat_g"])
                },
                "recommendations": recommendations
            }
        }
        
    except sqlite3.Error as e:
        return {"status": "error", "error": "database_error", "message": str(e)}
    finally:
        conn.close()


def daily_plan(args) -> Dict[str, Any]:
    """Generate full daily meal plan."""
    db_path = get_db_path(args.user)
    
    if not os.path.exists(db_path):
        return {"status": "error", "error": "database_not_found", "message": "Database not found"}
    
    conn = sqlite3.connect(db_path)
    
    try:
        targets = get_user_targets(conn, args.user)
        
        if not targets:
            return {"status": "error", "error": "profile_not_found", "message": "User profile not found"}
        
        # Simple daily plan distribution
        plan = {
            "breakfast": {"target_calories": round(targets["target_calories"] * 0.25), "suggested_foods": ["燕麦粥", "鸡蛋", "牛奶"]},
            "lunch": {"target_calories": round(targets["target_calories"] * 0.35), "suggested_foods": ["米饭", "鸡胸肉", "西兰花"]},
            "dinner": {"target_calories": round(targets["target_calories"] * 0.30), "suggested_foods": ["红薯", "三文鱼", "菠菜"]},
            "snack": {"target_calories": round(targets["target_calories"] * 0.10), "suggested_foods": ["苹果", "杏仁"]}
        }
        
        return {
            "status": "success",
            "data": {
                "daily_targets": targets,
                "meal_plan": plan
            }
        }
        
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='Diet recommender')
    parser.add_argument('--user', required=True, help='Username')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Recommend meal
    rec_parser = subparsers.add_parser('recommend', help='Recommend meal')
    rec_parser.add_argument('--meal-type', required=True,
                           choices=['breakfast', 'lunch', 'dinner', 'snack'],
                           help='Meal type')
    rec_parser.add_argument('--calories', type=float, help='Target calories for this meal')
    rec_parser.add_argument('--count', type=int, default=3, help='Number of recommendations')
    
    # Daily plan
    subparsers.add_parser('daily-plan', help='Generate daily meal plan')
    
    args = parser.parse_args()
    
    if args.command == 'recommend':
        result = recommend_meal(args)
    elif args.command == 'daily-plan':
        result = daily_plan(args)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2, default=str))
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
