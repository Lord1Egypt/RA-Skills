#!/usr/bin/env python3
"""
Report generation for Health Coach.
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, List


def get_db_path(username: str) -> str:
    """Get database file path for a user."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(skill_dir, 'data')
    return os.path.join(data_dir, f"{username}.db")


def weekly_report(args) -> Dict[str, Any]:
    """Generate weekly report."""
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
        
        # Calculate week range
        if args.week_start:
            start_date = datetime.strptime(args.week_start, '%Y-%m-%d')
        else:
            today = datetime.now()
            start_date = today - timedelta(days=today.weekday())  # Monday
        
        end_date = start_date + timedelta(days=6)
        
        # Get weight data
        cursor.execute('''
            SELECT recorded_at, weight_kg FROM body_metrics
            WHERE user_id = ? AND DATE(recorded_at) BETWEEN ? AND ?
            ORDER BY recorded_at
        ''', (user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        
        weight_rows = cursor.fetchall()
        weights = [r[1] for r in weight_rows]
        
        # Get nutrition data
        cursor.execute('''
            SELECT DATE(eaten_at) as date,
                   SUM(total_calories), SUM(total_protein_g), SUM(total_carbs_g), SUM(total_fat_g)
            FROM meals
            WHERE user_id = ? AND DATE(eaten_at) BETWEEN ? AND ?
            GROUP BY DATE(eaten_at)
        ''', (user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        
        nutrition_rows = cursor.fetchall()
        
        # Calculate averages
        avg_calories = sum(r[1] for r in nutrition_rows) / len(nutrition_rows) if nutrition_rows else 0
        avg_protein = sum(r[2] for r in nutrition_rows) / len(nutrition_rows) if nutrition_rows else 0
        avg_carbs = sum(r[3] for r in nutrition_rows) / len(nutrition_rows) if nutrition_rows else 0
        avg_fat = sum(r[4] for r in nutrition_rows) / len(nutrition_rows) if nutrition_rows else 0
        
        # Weight change
        weight_change = None
        if len(weights) >= 2:
            weight_change = round(weights[-1] - weights[0], 2)
        
        report = {
            "status": "success",
            "data": {
                "period": {
                    "start": start_date.strftime('%Y-%m-%d'),
                    "end": end_date.strftime('%Y-%m-%d')
                },
                "weight": {
                    "measurements": len(weights),
                    "start": weights[0] if weights else None,
                    "end": weights[-1] if weights else None,
                    "change_kg": weight_change,
                    "average": round(sum(weights) / len(weights), 2) if weights else None
                },
                "nutrition": {
                    "days_logged": len(nutrition_rows),
                    "average_daily": {
                        "calories": round(avg_calories, 1),
                        "protein_g": round(avg_protein, 1),
                        "carbs_g": round(avg_carbs, 1),
                        "fat_g": round(avg_fat, 1)
                    },
                    "target_calories": tdee,
                    "vs_target": round(avg_calories - tdee, 1) if tdee else None
                }
            }
        }
        
        # Text format
        if args.format == 'text':
            text = f"""# Weekly Report ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})

## Weight
- Measurements: {len(weights)}
- Average: {report['data']['weight']['average']} kg
- Change: {weight_change or 'N/A'} kg

## Nutrition
- Days logged: {len(nutrition_rows)}
- Avg daily calories: {round(avg_calories)} / {tdee} kcal
- Protein: {round(avg_protein)}g | Carbs: {round(avg_carbs)}g | Fat: {round(avg_fat)}g
"""
            report['text'] = text
        
        return report
        
    except sqlite3.Error as e:
        return {"status": "error", "error": "database_error", "message": str(e)}
    finally:
        conn.close()


def nutrition_analysis(args) -> Dict[str, Any]:
    """Analyze nutrition over a period."""
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
        
        days = args.days or 30
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT SUM(total_calories), SUM(total_protein_g), SUM(total_carbs_g), SUM(total_fat_g),
                   AVG(total_calories), AVG(total_protein_g), AVG(total_carbs_g), AVG(total_fat_g),
                   COUNT(DISTINCT DATE(eaten_at))
            FROM meals
            WHERE user_id = ? AND eaten_at >= ?
        ''', (user_id, start_date))
        
        row = cursor.fetchone()
        
        if not row or row[0] is None:
            return {"status": "success", "data": {"message": "No nutrition data found for this period"}}
        
        total_cals, total_protein, total_carbs, total_fat = row[0], row[1], row[2], row[3]
        avg_cals, avg_protein, avg_carbs, avg_fat = row[4], row[5], row[6], row[7]
        days_logged = row[8]
        
        # Calculate macro percentages
        total_macros = avg_protein + avg_carbs + avg_fat
        protein_pct = round((avg_protein / total_macros) * 100, 1) if total_macros > 0 else 0
        carbs_pct = round((avg_carbs / total_macros) * 100, 1) if total_macros > 0 else 0
        fat_pct = round((avg_fat / total_macros) * 100, 1) if total_macros > 0 else 0
        
        return {
            "status": "success",
            "data": {
                "period_days": days,
                "days_logged": days_logged,
                "totals": {
                    "calories": round(total_cals),
                    "protein_g": round(total_protein, 1),
                    "carbs_g": round(total_carbs, 1),
                    "fat_g": round(total_fat, 1)
                },
                "daily_averages": {
                    "calories": round(avg_cals, 1),
                    "protein_g": round(avg_protein, 1),
                    "carbs_g": round(avg_carbs, 1),
                    "fat_g": round(avg_fat, 1)
                },
                "macro_distribution": {
                    "protein_pct": protein_pct,
                    "carbs_pct": carbs_pct,
                    "fat_pct": fat_pct
                },
                "vs_target": {
                    "target_calories": tdee,
                    "difference": round(avg_cals - tdee, 1) if tdee else None
                }
            }
        }
        
    except sqlite3.Error as e:
        return {"status": "error", "error": "database_error", "message": str(e)}
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='Report generator')
    parser.add_argument('--user', required=True, help='Username')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Weekly report
    weekly_parser = subparsers.add_parser('weekly', help='Generate weekly report')
    weekly_parser.add_argument('--week-start', help='Week start date (YYYY-MM-DD)')
    weekly_parser.add_argument('--format', choices=['json', 'text'], default='json', help='Output format')
    
    # Nutrition analysis
    nutrition_parser = subparsers.add_parser('nutrition', help='Nutrition analysis')
    nutrition_parser.add_argument('--days', type=int, default=30, help='Number of days to analyze')
    nutrition_parser.add_argument('--format', choices=['json', 'text'], default='json', help='Output format')
    
    args = parser.parse_args()
    
    if args.command == 'weekly':
        result = weekly_report(args)
    elif args.command == 'nutrition':
        result = nutrition_analysis(args)
    else:
        parser.print_help()
        sys.exit(1)
    
    # Output
    if args.format == 'text' and 'text' in result:
        print(result['text'])
    else:
        print(json.dumps(result, indent=2, default=str))
    
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
