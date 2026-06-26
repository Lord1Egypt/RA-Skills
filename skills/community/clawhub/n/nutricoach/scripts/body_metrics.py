#!/usr/bin/env python3
"""
Body metrics logging and analysis for Health Coach.
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, List

from db_schema import (
    USERS_COLUMNS as UC,
    BODY_METRICS_COLUMNS as BMC,
    DEFAULTS
)


def get_db_path(username: str) -> str:
    """Get database file path for a user."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(skill_dir, 'data')
    return os.path.join(data_dir, f"{username}.db")


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate BMI."""
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)


def get_user_height(conn: sqlite3.Connection, username: str) -> float:
    """Get user's height from profile."""
    cursor = conn.cursor()
    cursor.execute('SELECT height_cm FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    return row[0] if row else DEFAULTS['user_height_cm']


def log_weight(args) -> Dict[str, Any]:
    """Log weight measurement."""
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
        # Get user ID and height
        cursor.execute('SELECT id, height_cm FROM users WHERE username = ?', (args.user,))
        user_row = cursor.fetchone()
        
        if not user_row:
            return {
                "status": "error",
                "error": "user_not_found",
                "message": f"User not found: {args.user}. Create profile first."
            }
        
        user_id, height_cm = user_row
        
        # Calculate BMI
        bmi = calculate_bmi(args.weight, height_cm)
        
        # Determine record date
        if args.date:
            record_date = args.date
            recorded_at = f"{args.date} 08:00:00"
        else:
            now = datetime.now()
            record_date = now.strftime('%Y-%m-%d')
            recorded_at = now.strftime('%Y-%m-%d %H:%M:%S')

        # Delete existing record for the same day (upsert behavior)
        cursor.execute('''
            DELETE FROM body_metrics
            WHERE user_id = ? AND DATE(recorded_at) = ?
        ''', (user_id, record_date))

        # Insert new record
        cursor.execute('''
            INSERT INTO body_metrics
            (user_id, weight_kg, height_cm, body_fat_pct, bmi, recorded_at, source, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            args.weight,
            height_cm,
            args.body_fat,
            bmi,
            recorded_at,
            'manual',
            args.notes
        ))
        
        record_id = cursor.lastrowid
        conn.commit()
        
        return {
            "status": "success",
            "data": {
                "record_id": record_id,
                "weight_kg": args.weight,
                "bmi": bmi,
                "recorded_at": recorded_at
            },
            "message": f"Logged weight: {args.weight} kg (BMI: {bmi})"
        }
        
    except sqlite3.Error as e:
        return {"status": "error", "error": "database_error", "message": str(e)}
    finally:
        conn.close()


def list_history(args) -> Dict[str, Any]:
    """List weight history."""
    db_path = get_db_path(args.user)
    
    if not os.path.exists(db_path):
        return {
            "status": "error",
            "error": "database_not_found",
            "message": f"Database not found."
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
        
        # Calculate date range
        if args.days:
            start_date = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')
            cursor.execute('''
                SELECT recorded_at, weight_kg, bmi, body_fat_pct, notes
                FROM body_metrics
                WHERE user_id = ? AND recorded_at >= ?
                ORDER BY recorded_at DESC
            ''', (user_id, start_date))
        else:
            cursor.execute('''
                SELECT recorded_at, weight_kg, bmi, body_fat_pct, notes
                FROM body_metrics
                WHERE user_id = ?
                ORDER BY recorded_at DESC
                LIMIT 30
            ''', (user_id,))
        
        rows = cursor.fetchall()
        
        records = []
        for row in rows:
            records.append({
                "recorded_at": row[BMC['recorded_at']],
                "weight_kg": row[BMC['weight_kg']],
                "bmi": row[BMC['bmi']],
                "body_fat_pct": row[BMC['body_fat_pct']],
                "notes": row[BMC['notes']]
            })
        
        return {
            "status": "success",
            "data": {
                "count": len(records),
                "records": records
            }
        }
        
    except sqlite3.Error as e:
        return {"status": "error", "error": "database_error", "message": str(e)}
    finally:
        conn.close()


def get_trend(args) -> Dict[str, Any]:
    """Get weight trend statistics."""
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
        days = args.days or 30
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT weight_kg, recorded_at
            FROM body_metrics
            WHERE user_id = ? AND recorded_at >= ?
            ORDER BY recorded_at ASC
        ''', (user_id, start_date))
        
        rows = cursor.fetchall()
        
        if len(rows) < 2:
            return {
                "status": "success",
                "data": {
                    "message": "Not enough data for trend analysis",
                    "records_count": len(rows)
                }
            }
        
        weights = [r[0] for r in rows]
        start_weight = weights[0]
        current_weight = weights[-1]
        change = round(current_weight - start_weight, 2)
        
        # Calculate weekly average change
        weeks = days / 7
        weekly_change = round(change / weeks, 2) if weeks > 0 else 0
        
        return {
            "status": "success",
            "data": {
                "period_days": days,
                "start_weight": start_weight,
                "current_weight": current_weight,
                "change_kg": change,
                "weekly_change_kg": weekly_change,
                "min_weight": min(weights),
                "max_weight": max(weights),
                "average_weight": round(sum(weights) / len(weights), 2),
                "records_count": len(rows)
            }
        }
        
    except sqlite3.Error as e:
        return {"status": "error", "error": "database_error", "message": str(e)}
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='Body metrics management')
    parser.add_argument('--user', required=True, help='Username')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Log weight
    log_parser = subparsers.add_parser('log-weight', help='Log weight measurement')
    log_parser.add_argument('--weight', type=float, required=True, help='Weight in kg')
    log_parser.add_argument('--date', help='Date (YYYY-MM-DD), defaults to today')
    log_parser.add_argument('--body-fat', type=float, help='Body fat percentage')
    log_parser.add_argument('--notes', help='Optional notes')
    
    # List history
    list_parser = subparsers.add_parser('list', help='List weight history')
    list_parser.add_argument('--days', type=int, help='Number of days to show')
    list_parser.add_argument('--format', choices=['json', 'table'], default='json', help='Output format')
    
    # Get trend
    trend_parser = subparsers.add_parser('trend', help='Get weight trend')
    trend_parser.add_argument('--days', type=int, default=30, help='Number of days for trend')
    
    args = parser.parse_args()
    
    if args.command == 'log-weight':
        result = log_weight(args)
    elif args.command == 'list':
        result = list_history(args)
    elif args.command == 'trend':
        result = get_trend(args)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2, default=str))
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
