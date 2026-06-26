#!/usr/bin/env python3
"""
Export user data for backup or migration.
"""

import argparse
import csv
import json
import os
import sqlite3
import sys
from datetime import datetime
from typing import Dict, Any

from db_schema import (
    USERS_COLUMNS as UC,
    MEALS_COLUMNS as MC,
    FOOD_ITEMS_COLUMNS as FIC
)


def get_db_path(username: str) -> str:
    """Get database file path for a user."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(skill_dir, 'data')
    return os.path.join(data_dir, f"{username}.db")


def export_user_profile(conn: sqlite3.Connection, username: str) -> Dict[str, Any]:
    """Export user profile."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    
    if not row:
        return None
    
    columns = [description[0] for description in cursor.description]
    return dict(zip(columns, row))


def export_body_metrics(conn: sqlite3.Connection, user_id: int) -> list:
    """Export body metrics history."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT recorded_at, weight_kg, height_cm, body_fat_pct, bmi, notes
        FROM body_metrics
        WHERE user_id = ?
        ORDER BY recorded_at
    ''', (user_id,))
    
    columns = [description[0] for description in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def export_meals(conn: sqlite3.Connection, user_id: int) -> list:
    """Export meal history."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.id, m.meal_type, m.eaten_at, m.notes, 
               m.total_calories, m.total_protein_g, m.total_carbs_g, m.total_fat_g,
               f.food_name, f.quantity_g, f.calories, f.protein_g, f.carbs_g, f.fat_g
        FROM meals m
        LEFT JOIN food_items f ON m.id = f.meal_id
        WHERE m.user_id = ?
        ORDER BY m.eaten_at DESC
    ''', (user_id,))
    
    meals = {}
    for row in cursor.fetchall():
        meal_id = row[0]
        if meal_id not in meals:
            meals[meal_id] = {
                "meal_type": row[1],
                "eaten_at": row[2],
                "notes": row[3],
                "total_calories": row[4],
                "total_protein_g": row[5],
                "total_carbs_g": row[6],
                "total_fat_g": row[7],
                "foods": []
            }
        # food_items columns start at index 8 (after meals columns)
        if row[8]:  # food_name
            meals[meal_id]["foods"].append({
                "name": row[8],
                "quantity_g": row[9],
                "calories": row[10],
                "protein_g": row[11],
                "carbs_g": row[12],
                "fat_g": row[13]
            })
    
    return list(meals.values())


def export_custom_foods(conn: sqlite3.Connection, user_id: int) -> list:
    """Export custom foods."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, brand, barcode, category, calories_per_100g, protein_per_100g,
               carbs_per_100g, fat_per_100g, fiber_per_100g, source, created_at
        FROM custom_foods
        WHERE user_id = ?
        ORDER BY created_at
    ''', (user_id,))
    
    columns = [description[0] for description in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def export_to_json(username: str, output_path: str) -> dict:
    """Export all data to JSON."""
    db_path = get_db_path(username)
    
    if not os.path.exists(db_path):
        return {"status": "error", "error": "database_not_found", "message": f"Database not found: {db_path}"}
    
    conn = sqlite3.connect(db_path)
    
    try:
        # Get user ID
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_row = cursor.fetchone()
        
        if not user_row:
            return {"status": "error", "error": "user_not_found", "message": "User not found"}
        
        user_id = user_row[UC["id"]]
        
        # Export all data
        data = {
            "export_info": {
                "username": username,
                "exported_at": datetime.now().isoformat(),
                "version": "1.0"
            },
            "profile": export_user_profile(conn, username),
            "body_metrics": export_body_metrics(conn, user_id),
            "meals": export_meals(conn, user_id),
            "custom_foods": export_custom_foods(conn, user_id)
        }
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        return {
            "status": "success",
            "output_path": output_path,
            "data_summary": {
                "body_metrics_count": len(data["body_metrics"]),
                "meals_count": len(data["meals"]),
                "custom_foods_count": len(data["custom_foods"])
            }
        }
        
    except Exception as e:
        return {"status": "error", "error": "export_failed", "message": str(e)}
    finally:
        conn.close()


def export_to_csv(username: str, output_dir: str) -> dict:
    """Export data to CSV files."""
    db_path = get_db_path(username)
    
    if not os.path.exists(db_path):
        return {"status": "error", "error": "database_not_found", "message": f"Database not found: {db_path}"}
    
    os.makedirs(output_dir, exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]
        
        exported_files = []
        
        # Export body metrics
        metrics = export_body_metrics(conn, user_id)
        if metrics:
            metrics_path = os.path.join(output_dir, 'body_metrics.csv')
            with open(metrics_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=metrics[0].keys())
                writer.writeheader()
                writer.writerows(metrics)
            exported_files.append(metrics_path)
        
        # Export custom foods
        foods = export_custom_foods(conn, user_id)
        if foods:
            foods_path = os.path.join(output_dir, 'custom_foods.csv')
            with open(foods_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=foods[0].keys())
                writer.writeheader()
                writer.writerows(foods)
            exported_files.append(foods_path)
        
        return {
            "status": "success",
            "output_dir": output_dir,
            "exported_files": exported_files
        }
        
    except Exception as e:
        return {"status": "error", "error": "export_failed", "message": str(e)}
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='Export user data')
    parser.add_argument('--user', required=True, help='Username')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Export format')
    parser.add_argument('--output', '-o', help='Output file (JSON) or directory (CSV)')
    
    args = parser.parse_args()
    
    # Default output path
    if not args.output:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if args.format == 'json':
            args.output = f"{args.user}_export_{timestamp}.json"
        else:
            args.output = f"{args.user}_export_{timestamp}"
    
    # Export
    if args.format == 'json':
        result = export_to_json(args.user, args.output)
    else:
        result = export_to_csv(args.user, args.output)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
