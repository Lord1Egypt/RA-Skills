#!/usr/bin/env python3
"""
Smart recipe recommendation based on pantry and nutrition gaps.
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from db_schema import (
    USERS_COLUMNS as UC,
    CUSTOM_FOODS_COLUMNS as FC,
    PANTRY_COLUMNS as PC
)


def get_db_path(username: str) -> str:
    """Get database file path for a user."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(skill_dir, 'data')
    return os.path.join(data_dir, f"{username}.db")


def get_nutrition_gap(conn: sqlite3.Connection, user_id: int, days: int = 7) -> Dict[str, float]:
    """Calculate nutrition gap based on recent intake vs targets."""
    cursor = conn.cursor()
    
    # Get user targets
    cursor.execute('SELECT tdee FROM users WHERE id = ?', (user_id,))
    tdee = cursor.fetchone()[0] or 2000
    
    # Calculate daily targets (simplified 40/30/30 split)
    targets = {
        "calories": tdee,
        "protein_g": tdee * 0.3 / 4,  # 30% from protein
        "carbs_g": tdee * 0.4 / 4,    # 40% from carbs
        "fat_g": tdee * 0.3 / 9       # 30% from fat
    }
    
    # Get recent actual intake
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT AVG(total_calories), AVG(total_protein_g), 
               AVG(total_carbs_g), AVG(total_fat_g)
        FROM meals
        WHERE user_id = ? AND DATE(eaten_at) >= ?
    ''', (user_id, start_date))
    
    row = cursor.fetchone()
    actual = {
        "calories": row[0] or 0,
        "protein_g": row[1] or 0,
        "carbs_g": row[2] or 0,
        "fat_g": row[3] or 0
    }
    
    # Calculate gaps (positive = need more)
    gaps = {}
    for key in targets:
        gaps[key] = max(0, targets[key] - actual[key])
    
    return gaps


def get_pantry_items(conn: sqlite3.Connection, user_id: int, expiring_days: int = 3, min_threshold: int = 50) -> List[Dict]:
    """Get pantry items, prioritizing expiring ones."""
    cursor = conn.cursor()
    
    future = (datetime.now() + timedelta(days=expiring_days)).strftime('%Y-%m-%d')
    
    # First try: items with sufficient remaining
    cursor.execute('''
        SELECT p.food_name, p.remaining_g, p.quantity_desc, p.location,
               c.calories_per_100g, c.protein_per_100g, c.carbs_per_100g, c.fat_per_100g,
               c.category, p.expiry_date
        FROM pantry p
        LEFT JOIN custom_foods c ON p.food_id = c.id
        WHERE p.user_id = ? AND (p.remaining_g IS NULL OR p.remaining_g > ?)
        ORDER BY 
            CASE WHEN p.expiry_date <= ? THEN 0 ELSE 1 END,
            p.expiry_date ASC
    ''', (user_id, min_threshold, future))
    
    rows = cursor.fetchall()
    
    # If not enough items, lower threshold
    if len(rows) < 3:
        cursor.execute('''
            SELECT p.food_name, p.remaining_g, p.quantity_desc, p.location,
                   c.calories_per_100g, c.protein_per_100g, c.carbs_per_100g, c.fat_per_100g,
                   c.category, p.expiry_date
            FROM pantry p
            LEFT JOIN custom_foods c ON p.food_id = c.id
            WHERE p.user_id = ? AND (p.remaining_g IS NULL OR p.remaining_g > 20)
            ORDER BY p.remaining_g DESC
        ''', (user_id,))
        rows = cursor.fetchall()
    
    # If still not enough, include all remaining > 0
    if len(rows) < 2:
        cursor.execute('''
            SELECT p.food_name, p.remaining_g, p.quantity_desc, p.location,
                   c.calories_per_100g, c.protein_per_100g, c.carbs_per_100g, c.fat_per_100g,
                   c.category, p.expiry_date
            FROM pantry p
            LEFT JOIN custom_foods c ON p.food_id = c.id
            WHERE p.user_id = ? AND (p.remaining_g IS NULL OR p.remaining_g > 0)
            ORDER BY p.remaining_g DESC
        ''', (user_id,))
        rows = cursor.fetchall()
    
    items = []
    today = datetime.now().date()
    
    for row in rows:
        expiry = row[9]
        days_left = None
        if expiry:
            expiry_date = datetime.strptime(expiry, '%Y-%m-%d').date()
            days_left = (expiry_date - today).days
        
        remaining = row[1] if row[1] is not None else 0
        
        items.append({
            "name": row[0],
            "remaining_g": remaining,
            "quantity_desc": row[2],
            "location": row[3],
            "calories_per_100g": row[4] or 0,
            "protein_per_100g": row[5] or 0,
            "carbs_per_100g": row[6] or 0,
            "fat_per_100g": row[7] or 0,
            "category": row[8] or "unknown",
            "expiry_days_left": days_left,
            "expiring_soon": days_left is not None and days_left <= expiring_days
        })
    
    return items


def generate_recipe_suggestions(pantry: List[Dict], gaps: Dict[str, float], count: int = 3) -> List[Dict]:
    """Generate recipe suggestions based on pantry and gaps."""
    
    # Categorize pantry items
    proteins = [i for i in pantry if i['category'] in ['protein', 'beef', 'pork', 'poultry', 'seafood', 'egg', 'soy']]
    grains = [i for i in pantry if i['category'] in ['grain', 'starch']]
    vegetables = [i for i in pantry if i['category'] in ['vegetable', 'mushroom']]
    
    # Determine priority nutrient
    gap_ratios = {
        "protein": gaps.get("protein_g", 0) / max(gaps.get("calories", 1), 1) * 4,
        "carbs": gaps.get("carbs_g", 0) / max(gaps.get("calories", 1), 1) * 4,
        "fat": gaps.get("fat_g", 0) / max(gaps.get("calories", 1), 1) * 9
    }
    
    priority = max(gap_ratios, key=gap_ratios.get)
    
    suggestions = []
    
    for i in range(min(count, 5)):
        if not proteins or not grains:
            break
        
        # Select ingredients (use remaining_g instead of quantity_g)
        protein = proteins[i % len(proteins)]
        grain = grains[i % len(grains)]
        veg = vegetables[i % len(vegetables)] if vegetables else None
        
        # Calculate nutrition (based on actual remaining)
        p_qty = min(150, protein.get('remaining_g', 100) or 100)
        g_qty = min(200, grain.get('remaining_g', 150) or 150)
        v_qty = min(100, veg.get('remaining_g', 100) or 100) if veg else 0
        
        total_cal = (protein['calories_per_100g'] * p_qty / 100 +
                    grain['calories_per_100g'] * g_qty / 100 +
                    (veg['calories_per_100g'] * v_qty / 100 if veg else 0))
        
        total_protein = (protein['protein_per_100g'] * p_qty / 100 +
                        grain['protein_per_100g'] * g_qty / 100 +
                        (veg['protein_per_100g'] * v_qty / 100 if veg else 0))
        
        # Check if helps with gap
        helps_gap = ""
        if priority == "protein" and total_protein > 20:
            helps_gap = f"补充蛋白质缺口 ({gaps.get('protein_g', 0):.0f}g)"
        elif protein.get('expiring_soon') or (veg and veg.get('expiring_soon')):
            helps_gap = "优先使用快过期食材"
        
        suggestion = {
            "name": f"{protein['name']} + {grain['name']}" + (f" + {veg['name']}" if veg else ""),
            "ingredients": [
                {"name": protein['name'], "qty": f"{p_qty}g", "expiring": protein.get('expiring_soon')},
                {"name": grain['name'], "qty": f"{g_qty}g", "expiring": grain.get('expiring_soon')}
            ],
            "nutrition": {
                "calories": round(total_cal),
                "protein_g": round(total_protein, 1)
            },
            "helps_with": helps_gap,
            "priority": priority
        }
        
        if veg:
            suggestion["ingredients"].append({
                "name": veg['name'], 
                "qty": f"{v_qty}g",
                "expiring": veg.get('expiring_soon')
            })
        
        suggestions.append(suggestion)
    
    return suggestions


def recommend(args) -> Dict[str, Any]:
    """Main recommendation function."""
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
        
        # Get data
        gaps = get_nutrition_gap(conn, user_id, args.days)
        
        # Check pantry status at different thresholds
        cursor.execute('''
            SELECT COUNT(*) FROM pantry 
            WHERE user_id = ? AND (remaining_g IS NULL OR remaining_g > 50)
        ''', (user_id,))
        sufficient_count = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM pantry 
            WHERE user_id = ? AND (remaining_g IS NULL OR remaining_g > 0)
        ''', (user_id,))
        total_count = cursor.fetchone()[0]
        
        # Get pantry items with dynamic threshold
        pantry = get_pantry_items(conn, user_id, args.expiring)
        
        if not pantry:
            return {
                "status": "success",
                "data": {
                    "gaps": gaps,
                    "pantry_count": 0,
                    "suggestions": [],
                    "message": "pantry 为空，请先添加食材"
                }
            }
        
        # Determine pantry status
        pantry_status = "sufficient"
        if sufficient_count < 3 and total_count >= 3:
            pantry_status = "low"
        elif total_count < 3:
            pantry_status = "critical"
        
        # Generate suggestions
        suggestions = generate_recipe_suggestions(pantry, gaps, args.count)
        
        # Get expiring items
        expiring_items = [p for p in pantry if p.get('expiring_soon')]
        
        # Build message based on status
        messages = {
            "sufficient": f"基于 {sufficient_count} 种充足食材推荐",
            "low": f"食材不足（仅 {total_count} 种），建议组合使用或补货",
            "critical": f"食材严重不足（仅 {total_count} 种），建议尽快购买"
        }
        
        return {
            "status": "success",
            "data": {
                "nutrition_gaps": {k: round(v, 1) for k, v in gaps.items()},
                "pantry_status": pantry_status,
                "pantry_count": {
                    "sufficient": sufficient_count,
                    "total": total_count
                },
                "expiring_count": len(expiring_items),
                "expiring_items": [{"name": e['name'], "days_left": e['expiry_days_left'], "remaining_g": e.get('remaining_g')} for e in expiring_items[:5]],
                "suggestions": suggestions,
                "priority_nutrient": max(gaps, key=gaps.get) if max(gaps.values()) > 0 else None,
                "message": messages.get(pantry_status, "")
            }
        }
        
    except sqlite3.Error as e:
        return {"status": "error", "error": "database_error", "message": str(e)}
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='Smart recipe recommendation')
    parser.add_argument('--user', required=True, help='Username')
    parser.add_argument('--count', type=int, default=3, help='Number of suggestions')
    parser.add_argument('--days', type=int, default=7, help='Days to analyze for nutrition gap')
    parser.add_argument('--expiring', type=int, default=3, help='Days to consider as expiring soon')
    
    args = parser.parse_args()
    
    result = recommend(args)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
