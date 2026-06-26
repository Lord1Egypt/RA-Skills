#!/usr/bin/env python3
"""
User profile management for Health Coach.
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime
from typing import Optional, Dict, Any


def get_db_path(username: str) -> str:
    """Get database file path for a user."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(skill_dir, 'data')
    return os.path.join(data_dir, f"{username}.db")


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str, formula: str = 'mifflin_st_jeor') -> float:
    """Calculate Basal Metabolic Rate."""
    if formula == 'mifflin_st_jeor':
        if gender == 'male':
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    elif formula == 'harris_benedict':
        if gender == 'male':
            bmr = 88.362 + 13.397 * weight_kg + 4.799 * height_cm - 5.677 * age
        else:
            bmr = 447.593 + 9.247 * weight_kg + 3.098 * height_cm - 4.330 * age
    else:
        raise ValueError(f"Unknown BMR formula: {formula}")
    
    return round(bmr, 2)


def calculate_tdee(bmr: float, activity_level: str) -> float:
    """Calculate Total Daily Energy Expenditure."""
    multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    multiplier = multipliers.get(activity_level, 1.2)
    return round(bmr * multiplier, 2)


def calculate_age(birth_date: str) -> int:
    """Calculate age from birth date."""
    birth = datetime.strptime(birth_date, '%Y-%m-%d')
    today = datetime.now()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))


def get_user_profile(conn: sqlite3.Connection, username: str) -> Optional[Dict[str, Any]]:
    """Get user profile from database."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    
    if row:
        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))
    return None


def set_profile(args) -> Dict[str, Any]:
    """Create or update user profile."""
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
        age = calculate_age(args.birth_date)
        current_weight = args.target_weight_kg or 70.0
        
        bmr = calculate_bmr(
            current_weight, 
            args.height_cm, 
            age, 
            args.gender, 
            args.bmr_formula or 'mifflin_st_jeor'
        )
        
        tdee = calculate_tdee(bmr, args.activity_level)
        
        cursor.execute('SELECT id FROM users WHERE username = ?', (args.user,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute('''
                UPDATE users SET
                    display_name = ?, gender = ?, birth_date = ?, height_cm = ?,
                    target_weight_kg = ?, activity_level = ?, goal_type = ?,
                    bmr_formula = ?, bmr = ?, tdee = ?, updated_at = CURRENT_TIMESTAMP
                WHERE username = ?
            ''', (
                args.name or args.user, args.gender, args.birth_date, args.height_cm,
                args.target_weight_kg, args.activity_level, args.goal_type,
                args.bmr_formula or 'mifflin_st_jeor', bmr, tdee, args.user
            ))
            user_id = existing[0]
            message = "Profile updated successfully"
        else:
            cursor.execute('''
                INSERT INTO users 
                (username, display_name, gender, birth_date, height_cm, 
                 target_weight_kg, activity_level, goal_type, bmr_formula, bmr, tdee)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                args.user, args.name or args.user, args.gender, args.birth_date,
                args.height_cm, args.target_weight_kg, args.activity_level,
                args.goal_type, args.bmr_formula or 'mifflin_st_jeor', bmr, tdee
            ))
            user_id = cursor.lastrowid
            message = "Profile created successfully"
        
        conn.commit()
        profile = get_user_profile(conn, args.user)
        
        return {
            "status": "success",
            "data": {
                "user_id": user_id,
                "profile": profile,
                "calculated": {"age": age, "bmr": bmr, "tdee": tdee}
            },
            "message": message
        }
        
    except sqlite3.Error as e:
        return {"status": "error", "error": "database_error", "message": str(e)}
    finally:
        conn.close()


def get_profile(args) -> Dict[str, Any]:
    """Get user profile."""
    db_path = get_db_path(args.user)
    
    if not os.path.exists(db_path):
        return {
            "status": "error",
            "error": "database_not_found",
            "message": f"Database not found. Run: python3 scripts/init_db.py --user {args.user}"
        }
    
    conn = sqlite3.connect(db_path)
    try:
        profile = get_user_profile(conn, args.user)
        
        if profile:
            if profile.get('birth_date'):
                profile['current_age'] = calculate_age(profile['birth_date'])
            return {"status": "success", "data": profile}
        else:
            return {
                "status": "error",
                "error": "profile_not_found",
                "message": f"Profile not found for user: {args.user}"
            }
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='User profile management')
    parser.add_argument('--user', required=True, help='Username')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Set profile
    set_parser = subparsers.add_parser('set', help='Create or update profile')
    set_parser.add_argument('--name', help='Display name')
    set_parser.add_argument('--gender', required=True, choices=['male', 'female'], help='Gender')
    set_parser.add_argument('--birth-date', required=True, help='Birth date (YYYY-MM-DD)')
    set_parser.add_argument('--height-cm', type=float, required=True, help='Height in cm')
    set_parser.add_argument('--target-weight-kg', type=float, help='Target weight in kg')
    set_parser.add_argument('--activity-level', required=True, 
                           choices=['sedentary', 'light', 'moderate', 'active', 'very_active'],
                           help='Activity level')
    set_parser.add_argument('--goal-type', required=True, 
                           choices=['lose', 'maintain', 'gain'],
                           help='Goal type')
    set_parser.add_argument('--bmr-formula', choices=['mifflin_st_jeor', 'harris_benedict'],
                           help='BMR calculation formula')
    
    # Get profile
    subparsers.add_parser('get', help='Get profile')
    
    args = parser.parse_args()
    
    if args.command == 'set':
        result = set_profile(args)
    elif args.command == 'get':
        result = get_profile(args)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2, default=str))
    sys.exit(0 if result['status'] == 'success' else 1)



if __name__ == "__main__":
    main()
