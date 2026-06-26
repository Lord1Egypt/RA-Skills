#!/usr/bin/env python3
"""
Food analysis and nutrition lookup for NutriCoach.
"""

import argparse
import json
import os
import sqlite3
import sys
import tempfile
import subprocess
from typing import Dict, Any, List, Optional

from db_schema import (
    USERS_COLUMNS as UC,
    CUSTOM_FOODS_COLUMNS as FC
)


def get_db_path(username: str) -> str:
    """Get database file path for a user."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(skill_dir, 'data')
    return os.path.join(data_dir, f"{username}.db")


def search_food(conn: sqlite3.Connection, query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search food database."""
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, category, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g
        FROM custom_foods
        WHERE name LIKE ? OR category LIKE ?
        LIMIT ?
    ''', (f'%{query}%', f'%{query}%', limit))
    
    rows = cursor.fetchall()
    
    foods = []
    for row in rows:
        foods.append({
            "name": row[FC['name']],
            "category": row[FC['category']],
            "calories_per_100g": row[FC['calories_per_100g']],
            "protein_per_100g": row[FC['protein_per_100g']],
            "carbs_per_100g": row[FC['carbs_per_100g']],
            "fat_per_100g": row[FC['fat_per_100g']],
            "fiber_per_100g": row[FC['fiber_per_100g']]
        })
    
    return foods


def add_custom_food(args) -> Dict[str, Any]:
    """Add custom food to database."""
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
        
        cursor.execute('''
            INSERT INTO custom_foods 
            (user_id, name, category, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            args.name,
            args.category,
            args.calories,
            args.protein or 0,
            args.carbs or 0,
            args.fat or 0,
            args.fiber or 0
        ))
        
        food_id = cursor.lastrowid
        conn.commit()
        
        return {
            "status": "success",
            "data": {"food_id": food_id, "name": args.name},
            "message": f"Added custom food: {args.name}"
        }
        
    except sqlite3.Error as e:
        return {"status": "error", "error": "database_error", "message": str(e)}
    finally:
        conn.close()


def search_command(args) -> Dict[str, Any]:
    """Search food database command."""
    db_path = get_db_path(args.user)
    
    if not os.path.exists(db_path):
        return {"status": "error", "error": "database_not_found", "message": "Database not found"}
    
    conn = sqlite3.connect(db_path)
    try:
        foods = search_food(conn, args.query, args.limit or 10)
        
        return {
            "status": "success",
            "data": {
                "query": args.query,
                "count": len(foods),
                "foods": foods
            }
        }
    finally:
        conn.close()


def identify_from_photo(args) -> Dict[str, Any]:
    """Identify food from photo (placeholder for vision model integration)."""
    if not os.path.exists(args.image):
        return {"status": "error", "error": "file_not_found", "message": f"Image not found: {args.image}"}
    
    # TODO: Integrate with vision model for food identification
    # For now, return a placeholder response
    
    return {
        "status": "success",
        "data": {
            "image_path": args.image,
            "identified_foods": [
                {"name": "待识别食物", "confidence": 0.0, "suggested_quantity_g": args.quantity_g or 300}
            ],
            "note": "Vision model integration pending. Please use --foods to manually specify."
        },
        "message": "Photo analysis placeholder. Manual entry recommended."
    }


def list_categories(args) -> Dict[str, Any]:
    """List food categories."""
    db_path = get_db_path(args.user)
    
    if not os.path.exists(db_path):
        return {"status": "error", "error": "database_not_found", "message": "Database not found"}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT DISTINCT category FROM custom_foods WHERE category IS NOT NULL ORDER BY category')
        rows = cursor.fetchall()
        
        categories = [row[0] for row in rows if row[0]]
        
        return {
            "status": "success",
            "data": {"categories": categories}
        }
    finally:
        conn.close()


def scan_and_match(args) -> Dict[str, Any]:
    """Scan packaging with OCR and match with database.
    
    OCR priority:
    1. If running in agent context (image data available), use agent vision
    2. Otherwise, use external OCR (local or cloud)
    """
    import subprocess
    import tempfile
    
    # Step 1: OCR
    # Check if we have direct image access (agent context)
    if hasattr(args, '_image_data') and args._image_data:
        # Use agent vision - already processed
        ocr_data = {
            "status": "success",
            "engine": "agent_vision",
            "structured": args._image_data,
            "text": None
        }
    else:
        # Use external OCR
        ocr_cmd = [
            'python3', 
            os.path.join(os.path.dirname(__file__), 'food_ocr.py'),
            '--image', args.image,
            '--engine', args.engine
        ]
        
        try:
            ocr_result = subprocess.run(ocr_cmd, capture_output=True, text=True, timeout=60)
            if ocr_result.returncode != 0:
                return {
                    "status": "error",
                    "error": "ocr_failed",
                    "message": f"OCR failed: {ocr_result.stderr}\n\n提示：如需使用云端 OCR，请配置 data/user_config.yaml 或设置 OPENAI_API_KEY 环境变量。"
                }
            
            ocr_data = json.loads(ocr_result.stdout)
            
            if ocr_data.get("status") != "success":
                error_msg = ocr_data.get("error", "OCR failed")
                if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                    error_msg += "\n\n提示：请配置 OCR API key：\n1. 复制 data/user_config.example.yaml → data/user_config.yaml\n2. 填入你的 API key\n\n或使用本地 OCR：--engine macos"
                return {
                    "status": "error",
                    "error": "ocr_failed",
                    "message": error_msg
                }
            
        except Exception as e:
            return {
                "status": "error",
                "error": "ocr_error",
                "message": str(e)
            }
    
    # Step 2: Match with database
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(ocr_data, f)
        temp_path = f.name
    
    try:
        match_cmd = [
            'python3',
            os.path.join(os.path.dirname(__file__), 'food_matcher.py'),
            '--user', args.user,
            '--ocr-result', temp_path,
            '--format', 'json'
        ]
        
        match_result = subprocess.run(match_cmd, capture_output=True, text=True, timeout=30)
        match_data = json.loads(match_result.stdout)
        
    finally:
        os.unlink(temp_path)
    
    # Step 3: Silent mode logic
    return process_scan_result(args, ocr_data, match_data)


def process_scan_result(args, ocr_data: dict, match_data: dict) -> dict:
    """Process scan result in silent mode."""
    import sys
    
    match_type = match_data.get("match_type")
    action = match_data.get("action")
    ocr_structured = ocr_data.get("structured", {})
    product_name = ocr_structured.get("product_name", "未知商品")
    barcode = ocr_structured.get("barcode")
    nutrition = ocr_structured.get("nutrition_per_100g", {})
    
    # Case 1: Barcode exact match
    if match_type == "barcode_exact":
        existing = match_data.get("matches", [{}])[0]
        comparison = match_data.get("comparison", {})
        significant_changes = comparison.get("significant_changes", [])
        
        # Check if changes exceed threshold
        max_diff = 0
        for key in ["calories", "protein", "carbs", "fat", "fiber"]:
            diff_info = comparison.get("nutrition_diff", {}).get(key, {})
            diff_pct = abs(diff_info.get("diff_pct", 0))
            max_diff = max(max_diff, diff_pct)
        
        if max_diff < args.threshold:
            # Small changes, use existing silently
            result = {
                "status": "success",
                "action": "used_existing",
                "product": existing.get("name"),
                "barcode": barcode,
                "message": f"✓ 已使用数据库数据: {existing.get('name')} (差异 {max_diff:.1f}% < 阈值 {args.threshold}%)"
            }
            if args.verbose:
                result["details"] = match_data
            return result
        else:
            # Significant changes, suggest update
            result = {
                "status": "success",
                "action": "suggest_update",
                "product": existing.get("name"),
                "barcode": barcode,
                "message": f"⚠️ 检测到显著变化 ({max_diff:.1f}% > {args.threshold}%)，建议更新",
                "significant_changes": significant_changes,
                "update_command": f"python3 scripts/food_analyzer.py --user {args.user} update-by-barcode --barcode {barcode} --calories {nutrition.get('calories')} --protein {nutrition.get('protein')} --carbs {nutrition.get('carbs')} --fat {nutrition.get('fat')} --fiber {nutrition.get('fiber')}"
            }
            if args.verbose:
                result["comparison"] = comparison
            return result
    
    # Case 2: Name match (no barcode)
    elif match_type in ["name_exact", "similar"] and match_data.get("matches"):
        existing = match_data["matches"][0]
        result = {
            "status": "success",
            "action": "suggest_confirm",
            "ocr_product": product_name,
            "matched_product": existing.get("name"),
            "barcode": barcode,
            "existing_barcode": existing.get("barcode"),
            "message": f"⚠️ 名称匹配但无条形码确认，建议核实是否为同一商品",
            "suggestion": "如为同一商品，建议添加条形码；如为不同商品，请使用 add-custom 添加"
        }
        if args.verbose:
            result["details"] = match_data
        return result
    
    # Case 3: No match - auto add
    else:
        # Auto add new food
        add_result = add_food_from_ocr(args.user, ocr_structured)
        return {
            "status": "success",
            "action": "added_new",
            "product": product_name,
            "barcode": barcode,
            "message": f"✓ 已新增商品: {product_name}",
            "food_id": add_result.get("food_id") if add_result.get("status") == "success" else None
        }


def parse_shelf_life(shelf_life_text: str) -> int:
    """Parse shelf life text to days."""
    if not shelf_life_text:
        return None
    
    text = str(shelf_life_text).lower().strip()
    
    # Match patterns like "6个月", "12个月", "180天", "6 month", "12 months"
    import re
    
    # Chinese patterns
    month_match = re.search(r'(\d+)\s*个?月', text)
    if month_match:
        return int(month_match.group(1)) * 30
    
    day_match = re.search(r'(\d+)\s*天', text)
    if day_match:
        return int(day_match.group(1))
    
    # English patterns
    month_match_en = re.search(r'(\d+)\s*months?', text)
    if month_match_en:
        return int(month_match_en.group(1)) * 30
    
    day_match_en = re.search(r'(\d+)\s*days?', text)
    if day_match_en:
        return int(day_match_en.group(1))
    
    return None


def add_food_from_ocr(username: str, ocr_structured: dict) -> dict:
    """Add food to database from OCR result."""
    db_path = get_db_path(username)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_row = cursor.fetchone()
        
        if not user_row:
            return {"status": "error", "error": "user_not_found"}
        
        user_id = user_row[UC["id"]]
        nutrition = ocr_structured.get("nutrition_per_100g", {})
        
        # Parse shelf life
        shelf_life_text = ocr_structured.get("shelf_life")
        shelf_life_days = parse_shelf_life(shelf_life_text)
        
        # Get storage method
        storage_method = ocr_structured.get("storage_method")
        
        cursor.execute('''
            INSERT INTO custom_foods 
            (user_id, name, brand, barcode, category, calories_per_100g, protein_per_100g, 
             carbs_per_100g, fat_per_100g, fiber_per_100g, sodium_per_100g, source,
             default_shelf_life_days, storage_method)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            ocr_structured.get("product_name"),
            ocr_structured.get("brand"),
            ocr_structured.get("barcode"),
            "snack",  # Default category, could be inferred
            nutrition.get("calories", 0),
            nutrition.get("protein", 0),
            nutrition.get("carbs", 0),
            nutrition.get("fat", 0),
            nutrition.get("fiber", 0),
            nutrition.get("sodium", 0),
            "ocr",
            shelf_life_days,
            storage_method
        ))
        
        food_id = cursor.lastrowid
        conn.commit()
        
        return {
            "status": "success", 
            "food_id": food_id,
            "shelf_life_days": shelf_life_days,
            "storage_method": storage_method
        }
        
    except sqlite3.Error as e:
        return {"status": "error", "error": str(e)}
    finally:
        conn.close()


def update_by_barcode(args) -> dict:
    """Update food nutrition by barcode."""
    db_path = get_db_path(args.user)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Find food by barcode
        cursor.execute('''
            SELECT id, name FROM custom_foods 
            WHERE barcode = ? AND user_id = (SELECT id FROM users WHERE username = ?)
        ''', (args.barcode, args.user))
        
        row = cursor.fetchone()
        
        if not row:
            return {
                "status": "error",
                "error": "barcode_not_found",
                "message": f"未找到条形码: {args.barcode}"
            }
        
        food_id, old_name = row
        
        # Update nutrition
        cursor.execute('''
            UPDATE custom_foods SET
                name = COALESCE(?, name),
                calories_per_100g = ?,
                protein_per_100g = ?,
                carbs_per_100g = ?,
                fat_per_100g = ?,
                fiber_per_100g = ?,
                source = 'ocr_updated',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            args.name,
            args.calories,
            args.protein or 0,
            args.carbs or 0,
            args.fat or 0,
            args.fiber or 0,
            food_id
        ))
        
        conn.commit()
        
        return {
            "status": "success",
            "food_id": food_id,
            "name": args.name or old_name,
            "barcode": args.barcode,
            "message": f"✓ 已更新: {args.name or old_name}"
        }
        
    except sqlite3.Error as e:
        return {"status": "error", "error": "database_error", "message": str(e)}
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='Food analyzer')
    parser.add_argument('--user', required=True, help='Username')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Search food
    search_parser = subparsers.add_parser('search', help='Search food database')
    search_parser.add_argument('--query', required=True, help='Search query')
    search_parser.add_argument('--limit', type=int, help='Max results')
    
    # Add custom food
    add_parser = subparsers.add_parser('add-custom', help='Add custom food')
    add_parser.add_argument('--name', required=True, help='Food name')
    add_parser.add_argument('--calories', type=float, required=True, help='Calories per 100g')
    add_parser.add_argument('--protein', type=float, help='Protein per 100g')
    add_parser.add_argument('--carbs', type=float, help='Carbs per 100g')
    add_parser.add_argument('--fat', type=float, help='Fat per 100g')
    add_parser.add_argument('--fiber', type=float, help='Fiber per 100g')
    add_parser.add_argument('--category', help='Food category')
    
    # Identify from photo
    identify_parser = subparsers.add_parser('identify', help='Identify food from photo')
    identify_parser.add_argument('--image', required=True, help='Image file path')
    identify_parser.add_argument('--quantity-g', type=float, help='Estimated total weight in grams')
    
    # OCR scan and add (silent mode by default)
    scan_parser = subparsers.add_parser('scan', help='Scan food packaging with OCR')
    scan_parser.add_argument('--image', required=True, help='Image file path')
    scan_parser.add_argument('--engine', choices=['auto', 'custom', 'macos'], default='auto', 
                            help='OCR engine: auto (uses custom if API key set, else macOS), custom (cloud API, requires key), macos (local, free)')
    scan_parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed comparison even if matched')
    scan_parser.add_argument('--threshold', type=float, default=10.0, help='Nutrition change threshold %% to prompt update (default: 10)')
    
    # Update existing food by barcode
    update_parser = subparsers.add_parser('update-by-barcode', help='Update food nutrition by barcode')
    update_parser.add_argument('--barcode', required=True, help='Product barcode')
    update_parser.add_argument('--name', help='New name (optional)')
    update_parser.add_argument('--calories', type=float, required=True, help='Calories per 100g')
    update_parser.add_argument('--protein', type=float, help='Protein per 100g')
    update_parser.add_argument('--carbs', type=float, help='Carbs per 100g')
    update_parser.add_argument('--fat', type=float, help='Fat per 100g')
    update_parser.add_argument('--fiber', type=float, help='Fiber per 100g')
    
    # List categories
    subparsers.add_parser('categories', help='List food categories')
    
    args = parser.parse_args()
    
    if args.command == 'search':
        result = search_command(args)
    elif args.command == 'add-custom':
        result = add_custom_food(args)
    elif args.command == 'identify':
        result = identify_from_photo(args)
    elif args.command == 'scan':
        result = scan_and_match(args)
    elif args.command == 'update-by-barcode':
        result = update_by_barcode(args)
    elif args.command == 'categories':
        result = list_categories(args)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2, default=str))
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
