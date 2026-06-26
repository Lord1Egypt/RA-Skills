#!/usr/bin/env python3
"""
Import Chinese foods nutrition data into database.
"""

import argparse
import json
import os
import sqlite3
import sys

# Import the food data
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'references'))
from chinese_foods_nutrition import CHINESE_FOODS


def get_db_path(username: str) -> str:
    """Get database file path for a user."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(skill_dir, 'data')
    return os.path.join(data_dir, f"{username}.db")


def import_foods(username: str, clear_existing: bool = False) -> dict:
    """Import Chinese foods into database."""
    db_path = get_db_path(username)
    
    if not os.path.exists(db_path):
        return {
            "status": "error",
            "error": "database_not_found",
            "message": f"Database not found: {db_path}"
        }
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get system user ID
        cursor.execute('SELECT id FROM users WHERE username = ?', ('__system__',))
        row = cursor.fetchone()
        
        if not row:
            # Create system user if not exists
            cursor.execute(
                'INSERT INTO users (id, username, display_name) VALUES (1, ?, ?)',
                ('__system__', 'System')
            )
            system_user_id = 1
        else:
            system_user_id = row[0]
        
        # Clear existing system foods if requested
        if clear_existing:
            cursor.execute('DELETE FROM custom_foods WHERE user_id = ?', (system_user_id,))
            print(f"Cleared existing foods for system user")
        
        # Check for duplicates
        cursor.execute('SELECT name FROM custom_foods WHERE user_id = ?', (system_user_id,))
        existing_names = set(row[0] for row in cursor.fetchall())
        
        # Insert foods
        inserted = 0
        skipped = 0
        
        for food in CHINESE_FOODS:
            name, category, calories, protein, carbs, fat, fiber = food
            
            if name in existing_names:
                skipped += 1
                continue
            
            cursor.execute('''
                INSERT INTO custom_foods 
                (user_id, name, category, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (system_user_id, name, category, calories, protein, carbs, fat, fiber))
            
            inserted += 1
            existing_names.add(name)
        
        conn.commit()
        
        return {
            "status": "success",
            "data": {
                "total_foods": len(CHINESE_FOODS),
                "inserted": inserted,
                "skipped": skipped
            },
            "message": f"Imported {inserted} foods, skipped {skipped} duplicates"
        }
        
    except sqlite3.Error as e:
        return {
            "status": "error",
            "error": "database_error",
            "message": str(e)
        }
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='Import Chinese foods nutrition data')
    parser.add_argument('--user', required=True, help='Username')
    parser.add_argument('--clear', action='store_true', help='Clear existing foods before import')
    
    args = parser.parse_args()
    
    result = import_foods(args.user, args.clear)
    print(json.dumps(result, indent=2))
    
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
