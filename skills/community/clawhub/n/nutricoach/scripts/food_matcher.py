#!/usr/bin/env python3
"""
Match OCR results with database and compare differences.
"""

import json
import os
import sqlite3
from difflib import SequenceMatcher
from typing import Dict, Any, List, Tuple, Optional


def get_db_path(username: str) -> str:
    """Get database file path for a user."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(skill_dir, 'data')
    return os.path.join(data_dir, f"{username}.db")


def similarity(a: str, b: str) -> float:
    """Calculate string similarity (0-1)."""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_matches(conn: sqlite3.Connection, product_name: str, barcode: Optional[str] = None, 
                 threshold: float = 0.6) -> List[Dict[str, Any]]:
    """Find matching foods in database. Barcode match has highest priority."""
    cursor = conn.cursor()
    matches = []
    
    # First priority: exact barcode match
    if barcode:
        cursor.execute('''
            SELECT id, name, brand, barcode, category, calories_per_100g, protein_per_100g, 
                   carbs_per_100g, fat_per_100g, fiber_per_100g
            FROM custom_foods
            WHERE barcode = ?
        ''', (barcode,))
        
        row = cursor.fetchone()
        if row:
            # Barcode exact match - return immediately as highest priority
            return [{
                "id": row[0],
                "name": row[1],
                "brand": row[2],
                "barcode": row[3],
                "category": row[4],
                "nutrition": {
                    "calories": row[5],
                    "protein": row[6],
                    "carbs": row[7],
                    "fat": row[8],
                    "fiber": row[9]
                },
                "match_type": "barcode_exact",
                "similarity": 1.0
            }]
    
    # Second priority: name similarity (only if no barcode match)
    cursor.execute('''
        SELECT id, name, brand, barcode, category, calories_per_100g, protein_per_100g, 
               carbs_per_100g, fat_per_100g, fiber_per_100g
        FROM custom_foods
    ''')
    
    for row in cursor.fetchall():
        db_name = row[1]
        sim = similarity(product_name, db_name)
        
        if sim >= threshold:
            matches.append({
                "id": row[0],
                "name": db_name,
                "brand": row[2],
                "barcode": row[3],
                "category": row[4],
                "nutrition": {
                    "calories": row[5],
                    "protein": row[6],
                    "carbs": row[7],
                    "fat": row[8],
                    "fiber": row[9]
                },
                "match_type": "name",
                "similarity": round(sim, 3)
            })
    
    # Sort by similarity
    matches.sort(key=lambda x: x["similarity"], reverse=True)
    
    # Remove duplicates (keep highest similarity)
    seen_names = set()
    unique_matches = []
    for m in matches:
        if m["name"] not in seen_names:
            seen_names.add(m["name"])
            unique_matches.append(m)
    
    return unique_matches[:5]  # Return top 5


def calculate_diff(new_nutrition: Dict[str, Any], existing_nutrition: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate differences between nutrition values."""
    diff = {}
    
    for key in ["calories", "protein", "carbs", "fat", "fiber"]:
        new_val = new_nutrition.get(key)
        old_val = existing_nutrition.get(key)
        
        if new_val is None or old_val is None:
            diff[key] = {"status": "missing", "new": new_val, "old": old_val}
        elif new_val == 0 and old_val == 0:
            diff[key] = {"status": "same", "value": 0, "diff_pct": 0}
        else:
            if old_val == 0:
                diff_pct = 100 if new_val > 0 else 0
            else:
                diff_pct = round(((new_val - old_val) / old_val) * 100, 1)
            
            diff[key] = {
                "status": "same" if abs(diff_pct) < 5 else ("increased" if diff_pct > 0 else "decreased"),
                "new": new_val,
                "old": old_val,
                "diff_pct": diff_pct
            }
    
    return diff


def classify_match(ocr_result: Dict[str, Any], matches: List[Dict[str, Any]]) -> str:
    """Classify match type: barcode_exact, name_exact, similar, none."""
    if not matches:
        return "none"
    
    top_match = matches[0]
    
    # Barcode exact match is the highest priority
    if top_match.get("match_type") == "barcode_exact":
        return "barcode_exact"
    
    # Name similarity levels
    if top_match["similarity"] >= 0.95:
        return "name_exact"
    elif top_match["similarity"] >= 0.7:
        return "similar"
    else:
        return "weak"


def match_and_compare(username: str, ocr_result: Dict[str, Any]) -> Dict[str, Any]:
    """Main matching and comparison function."""
    db_path = get_db_path(username)
    
    if not os.path.exists(db_path):
        return {
            "status": "error",
            "error": "database_not_found",
            "message": f"Database not found: {db_path}"
        }
    
    conn = sqlite3.connect(db_path)
    
    try:
        structured = ocr_result.get("structured", {})
        
        product_name = structured.get("product_name") or "未知商品"
        barcode = structured.get("barcode")
        new_nutrition = structured.get("nutrition_per_100g", {})
        
        # Find matches
        matches = find_matches(conn, product_name, barcode)
        
        # Classify match
        match_type = classify_match(ocr_result, matches)
        
        result = {
            "status": "success",
            "ocr_data": {
                "product_name": product_name,
                "brand": structured.get("brand"),
                "net_weight": structured.get("net_weight"),
                "barcode": barcode,
                "nutrition": new_nutrition
            },
            "match_type": match_type,
            "matches": matches
        }
        
        # Handle different match types
        if match_type == "barcode_exact" and matches:
            # Same barcode - check if nutrition data needs update
            top_match = matches[0]
            diff = calculate_diff(new_nutrition, top_match["nutrition"])
            result["comparison"] = {
                "with": top_match["name"],
                "existing_barcode": top_match.get("barcode"),
                "nutrition_diff": diff,
                "significant_changes": [
                    k for k, v in diff.items() 
                    if v.get("status") in ["increased", "decreased"] and abs(v.get("diff_pct", 0)) > 5
                ]
            }
            
            # Generate suggestion for barcode match
            if result["comparison"]["significant_changes"]:
                result["suggestion"] = f"条形码匹配：同一商品，但营养数据有变化，建议更新数据库"
                result["action"] = "update"
            else:
                result["suggestion"] = f"条形码匹配：同一商品，数据一致，无需更新"
                result["action"] = "use_existing"
                
        elif match_type in ["name_exact", "similar"] and matches:
            # Name match only (no barcode or barcode mismatch)
            top_match = matches[0]
            diff = calculate_diff(new_nutrition, top_match["nutrition"])
            result["comparison"] = {
                "with": top_match["name"],
                "existing_barcode": top_match.get("barcode"),
                "nutrition_diff": diff,
                "significant_changes": [
                    k for k, v in diff.items() 
                    if v.get("status") in ["increased", "decreased"] and abs(v.get("diff_pct", 0)) > 10
                ]
            }
            
            # Generate suggestion for name match
            if top_match.get("barcode") and barcode and top_match["barcode"] != barcode:
                result["suggestion"] = f"名称相似但条形码不同，可能是不同规格/版本，建议新增"
                result["action"] = "add_new"
            elif result["comparison"]["significant_changes"]:
                result["suggestion"] = "名称匹配但数据有差异，建议确认是否为同一商品"
                result["action"] = "confirm"
            else:
                result["suggestion"] = "名称匹配且数据一致，可能是同一商品"
                result["action"] = "use_existing"
                
        elif match_type == "none":
            result["suggestion"] = "数据库中无匹配，建议新增"
            result["action"] = "add_new"
        else:
            result["suggestion"] = "匹配度较低，请确认是否为同一商品"
            result["action"] = "confirm"
        
        return result
        
    except sqlite3.Error as e:
        return {
            "status": "error",
            "error": "database_error",
            "message": str(e)
        }
    finally:
        conn.close()


def format_comparison(result: Dict[str, Any]) -> str:
    """Format comparison result for human reading."""
    lines = []
    
    ocr = result.get("ocr_data", {})
    lines.append(f"识别商品: {ocr.get('product_name')}")
    if ocr.get('brand'):
        lines.append(f"品牌: {ocr['brand']}")
    if ocr.get('net_weight'):
        lines.append(f"规格: {ocr['net_weight']}")
    if ocr.get('barcode'):
        lines.append(f"条形码: {ocr['barcode']}")
    lines.append("")
    
    match_type = result.get("match_type")
    matches = result.get("matches", [])
    action = result.get("action", "")
    
    # Barcode exact match
    if match_type == "barcode_exact" and matches:
        lines.append("✅ 条形码完全匹配")
        top = matches[0]
        lines.append(f"   数据库商品: {top['name']}")
        if top.get('brand'):
            lines.append(f"   品牌: {top['brand']}")
        lines.append(f"   现有条形码: {top.get('barcode', '无')}")
        lines.append(f"   动作: {action}")
        lines.append("")
        
    elif match_type == "none":
        lines.append("❌ 数据库中无匹配商品")
        lines.append("建议: 作为新商品添加")
        lines.append(f"   动作: {action}")
    elif matches:
        top = matches[0]
        match_type_str = "名称匹配" if match_type == "name_exact" else "相似匹配"
        lines.append(f"{match_type_str}: {top['name']} (相似度: {top['similarity']:.0%})")
        if top.get('barcode'):
            lines.append(f"   现有条形码: {top['barcode']}")
        lines.append(f"   动作: {action}")
        lines.append("")
        
        if "comparison" in result:
            comp = result["comparison"]
            lines.append("营养对比 (每100g):")
            lines.append("-" * 50)
            
            for key, diff in comp["nutrition_diff"].items():
                key_name = {
                    "calories": "热量",
                    "protein": "蛋白质",
                    "carbs": "碳水",
                    "fat": "脂肪",
                    "fiber": "纤维"
                }.get(key, key)
                
                if diff["status"] == "missing":
                    lines.append(f"  {key_name}: 数据缺失")
                else:
                    new_val = diff["new"]
                    old_val = diff["old"]
                    diff_pct = diff.get("diff_pct", 0)
                    
                    status_icon = "✓" if diff["status"] == "same" else ("↑" if diff["status"] == "increased" else "↓")
                    lines.append(f"  {status_icon} {key_name}: {new_val} vs {old_val} ({diff_pct:+.1f}%)")
            
            lines.append("")
            if comp["significant_changes"]:
                lines.append(f"⚠️ 显著差异项: {', '.join(comp['significant_changes'])}")
            else:
                lines.append("✓ 数据基本一致")
            
            lines.append("")
            lines.append(f"建议: {result.get('suggestion', '')}")
    
    return "\n".join(lines)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Match OCR result with database')
    parser.add_argument('--user', required=True, help='Username')
    parser.add_argument('--ocr-result', required=True, help='OCR result JSON string or file path')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='Output format')
    
    args = parser.parse_args()
    
    # Load OCR result
    if os.path.exists(args.ocr_result):
        with open(args.ocr_result, 'r', encoding='utf-8') as f:
            ocr_result = json.load(f)
    else:
        try:
            ocr_result = json.loads(args.ocr_result)
        except json.JSONDecodeError as e:
            print(f"Error parsing OCR result: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Match and compare
    result = match_and_compare(args.user, ocr_result)
    
    # Output
    if args.format == 'text' and result.get("status") == "success":
        print(format_comparison(result))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == '__main__':
    main()
