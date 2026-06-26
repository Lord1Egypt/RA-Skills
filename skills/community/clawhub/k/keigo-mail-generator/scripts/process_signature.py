#!/usr/bin/env python3

import os
import sqlite3
import json
import sys
import argparse
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple, List
import re


# ====================== Database Path Configuration (Auto-Adaptive) ======================
# Get the absolute path of the current script（skills/keigo-mail-generator/scripts/process_signature.py）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Database directory： skills/keigo-mail-generator/users/
# Use ".." to go up one level, then enter the "users" folder
DB_DIR = os.path.join(SCRIPT_DIR, "..", "users")
DB_DIR = os.path.abspath(DB_DIR)
DB_PATH = os.path.join(DB_DIR, "user_signatures.db")


def init_db():
    """Initialize the database (run once only)"""
    try:
        # Ensure the directory exists
        os.makedirs(DB_DIR, exist_ok=True)
        
        # IMPORTANT: Grant read/write permissions to the directory for database operation
        os.chmod(DB_DIR, 0o700)
        
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_signatures (
                user_id TEXT PRIMARY KEY,
                signature TEXT NOT NULL,        -- Store JSON string
                updated_at TEXT
            )
        """)
        conn.commit()
        conn.close()
        
        print(f"[DEBUG] Database initialized successfully → {DB_PATH}")
    except Exception as e:
        print(f"[ERROR] init_db failed: {type(e).__name__}: {e}")
        # Do not raise; allow it to continue running


def normalize_signature_keys(sig: dict) -> dict:
    """Unify possible Japanese/mixed keys into English keys"""
    if not sig:
        return {}

    key_map = {
        # High-frequency core fields
        "氏名": "name", "名前": "name", "お名前": "name",
        "会社名": "company", "会社": "company",
        "役職": "position", "肩書き": "position", "職位": "position",
        "部署": "department", "部署名": "department","部門": "department", "事業部": "department",
        "携帯": "mobile", "携帯電話": "mobile", "携帯番号": "mobile",
        "電話": "phone", "TEL": "phone", "電話番号": "phone","tel": "phone","Tel": "phone",
        "FAX": "fax", "ファックス": "fax",
        "メール": "email", "メールアドレス": "email", "Email": "email",
        "住所": "address", "会社住所": "address",
        "郵便番号": "postal_code", "〒": "postal_code",
        "ウェブサイト": "website", "HP": "website", "URL": "website",
        "所属": "affiliation", 
        "チーム": "team",
        "フリガナ": "furigana",
        "直通": "direct_phone", 
        "内線": "extension",
    }
        
    normalized = {}
    for k, v in sig.items():
        new_key = key_map.get(k.strip(), k.strip().lower().replace(" ", "_"))
        if v:  # Keep only if value is not empty
            normalized[new_key] = str(v).strip()
    
    return normalized

def prune_dict(data: Dict) -> Dict:
    """
    辞書から value が文字列 "rm"（大文字小文字問わず）のキーと値のペアを削除する。
    
    例:
        {"name": "田中太郎", "mobile": "rm", "email": "", "fax": "rm"} 
        → {"name": "田中太郎", "email": ""}
    """
    if not isinstance(data, dict):
        return data
    
    cleaned = {}
    for key, value in data.items():
        # 文字列 "rm" の場合のみ削除（大文字小文字を無視）
        if isinstance(value, str) and value.strip().upper() == "RM":
            continue
        
        cleaned[key] = value
    
    return cleaned


def calculate_changed_fields(old: Dict, new: Dict) -> List[str]:
    """Calculate the fields that have actually changed and return a list of user-friendly strings suitable for email display.
    
    Return format example：
    [
        "氏名：未提供 -> 佐藤花子",
        "携帯電話：未提供 -> 090-1234-5678",
        "会社名：会社ABC -> 会社XYZ"
    ]
    """
    changed = []
    
    # Display Mapping Table
    key_display = {
        "name": "氏名",
        "company": "会社名",
        "position": "役職",
        "department": "部署",
        "mobile": "携帯電話",
        "phone": "電話番号",
        "fax": "FAX",
        "email": "Email",
        "address": "住所",
        "postal_code": "郵便番号",
        "website": "URL",
        "affiliation": "所属",
        "team": "チーム",
        "furigana": "フリガナ",
        "direct_phone": "直通電話",
        "extension": "内線",
    }
    
    for key, new_value in new.items():
        if key == "updatedAt":
            continue
            
        old_value = old.get(key, None)  # Explicitly use None if not found
        
        # if old value is empty and new value is string 'rm'/'Rm'/'RM'/'rM', then skip (treat as no change)
        if old_value in (None, "", {}) and new_value.strip().upper() == 'RM':
            continue

        # Only record if the value has changed (including transitions from/to None or empty)
        if old_value != new_value:
            old_display = old_value if old_value not in (None, "", {}) else "未提供"
            new_display = new_value if new_value not in (None, "", {}) else "空"
            
            # If the new value is the string 'rm'/'Rm'/'RM'/'rM', set the display as "空"
            if new_display.strip().upper() == 'RM':
                new_display = "空"


            # Get display name; use the original key if no mapping exists
            display_key = key_display.get(key, key)
            
            changed.append(f"{display_key}：{old_display} -> {new_display}")
    
    return changed



def normalize_user_id(raw_id: str) -> str:
    """normalize user_id
    
    Rules:
    - If raw_id is empty, None, or clearly a session ID (contains '@' or is too long), return the default value "0000000000"
    - Otherwise, return after basic cleanup
    """
    if not raw_id or raw_id == "None" or raw_id.strip() == "":
        return "0000000000"
    
    raw_id = str(raw_id).strip()
    
    # If it contains '@' or exceeds 60 characters, it is highly likely a session ID or conversation ID
    if '@' in raw_id or len(raw_id) > 60:
        return "0000000000"
    
    # Perform character cleanup only for IDs that appear normal
    clean_id = re.sub(r'[^a-zA-Z0-9_-]', '', raw_id)
    
    return clean_id if clean_id else "0000000000"


def format_signature(signature: Dict) -> str:
    """Format signature into the specified business email signature format"""
    if not signature:
        return "氏名：未提供"

    lines = []

    company = signature.get("company", "")
    affiliation = signature.get("affiliation", "")
    department = signature.get("department", "")
    team = signature.get("team", "")
    position = signature.get("position", "")
    name = signature.get("name", "")
    furigana = signature.get("furigana", "")

    if company:
        lines.append(company)
    if affiliation or department or team:
        dept_part = " ".join(filter(None, [affiliation, department, team]))
        if dept_part:
            lines.append(dept_part)
    
    position_name = " ".join(filter(None, [position, name]))

    if furigana:
        if name:
            position_name_furigana = " ".join(filter(None, [position_name, f"（{furigana}）"])) 
        else:
            position_name_furigana = " ".join(filter(None, [position_name, f"{furigana}"])) 
    else:
        position_name_furigana = position_name
    
    if position_name_furigana:
        lines.append(position_name_furigana)
    
    # Insert a blank line between the first and second line.
    lines.append("")

    if signature.get("postal_code"):
        lines.append(f"〒{signature['postal_code']}")
    if signature.get("address"):
        lines.append(signature['address'])

    # contact info
    phone_num = signature.get("phone", "")
    ext_num = signature.get("extension", "")
    if ext_num:
        phone_ext_num = f"{phone_num}（内線：{ext_num}）" if phone_num else f"内線：{ext_num}"
    else:
        phone_ext_num = phone_num

    if phone_ext_num:    
        lines.append(f"TEL：{phone_ext_num}")


    if signature.get("direct_phone"):
        lines.append(f"直通：{signature['direct_phone']}")
    if signature.get("fax"):
        lines.append(f"FAX：{signature['fax']}")
    if signature.get("mobile"):
        lines.append(f"Mobile：{signature['mobile']}")
    if signature.get("email"):
        lines.append(f"Email：{signature['email']}")
    if signature.get("website"):
        lines.append(f"URL：{signature['website']}")

    return "\n".join(lines)

def process_user_signature(
    raw_user_id: str, 
    provided_signature: Optional[Dict] = None
    ) -> Tuple[Dict, bool, List[str]]:
    """
    Core processing function
    Returns: (The signature dictionary to be used, whether a database write occurred, the list of changed fields)
    
    Note：
    - If user_id = "0000000000", handle only in memory and do not write to the database.
    - For regular user_ids, perform a create or merge update based on whether a record exists.
    - Always return changed_fields to display "which items were changed" at the beginning of the email.


    """
    
    # Normalize user_id (to prevent passing in session IDs)
    user_id = normalize_user_id(raw_user_id)
    
    init_db()  # Ensure the table exists
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    now = datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z'
    
    # Unify possible Japanese/mixed keys into English keys
    provided_signature = normalize_signature_keys(provided_signature) if provided_signature else {}

    # ==================== Special user_id Handling ====================
    if user_id == "0000000000":

        # remove key & value pairs with "rm" string value in provided_signature 
        provided_signature = prune_dict(provided_signature)

        if provided_signature:   
            # Merge update (In-memory only, do not save to database)
            existing = {}        # Special ID does not load history; starts from empty
            updated = {**existing, **provided_signature}
            conn.close()
            # Special ID does not return changed fields 
            changed_fields = []

            return updated, False, changed_fields
        else:
            default_sig = {"氏名": "未提供", "会社名": "未提供"}
                        
            conn.close()

            # Special ID does not return changed fields 
            changed_fields = []
            return default_sig, False, changed_fields

    # ==================== Regular user_id Handling ====================
    # Query existing record
    cur.execute("SELECT signature FROM user_signatures WHERE user_id = ?", (user_id,))
    row = cur.fetchone()

    if row is None:
        
        # remove key & value pairs with "rm" string value in provided_signature
        provided_signature = prune_dict(provided_signature)

        # ---------- Does not exist → Create new ----------
        if provided_signature:
            new_sig = {**provided_signature, "updatedAt": now}
            sig_json = json.dumps(new_sig, ensure_ascii=False)
            
            cur.execute(
                "INSERT INTO user_signatures (user_id, signature, updated_at) VALUES (?, ?, ?)",
                (user_id, sig_json, now)
            )

            conn.commit()
            conn.close()
            return new_sig, True, calculate_changed_fields({}, new_sig)   
        else:
            # No information provided → Use default values, but do not save
            default_sig = {"氏名": "未提供", "会社名": "未提供"}

            conn.close()
            changed_fields = []
            return default_sig, False, changed_fields

    else:
        # ---------- Already exists → Merge update ----------
        existing = json.loads(row[0])
    
        if provided_signature:
            # Only overwrite provided fields; fully preserve unprovided ones
            updated = {**existing, **provided_signature}
            updated["updatedAt"] = now
            
            # Calculate the fields that actually changed this time
            changed_fields = calculate_changed_fields(existing, updated)
            
            if len(changed_fields) != 0:

                # remove key & value pairs with "rm" string value for the final updated signature
                updated = prune_dict(updated)

                sig_json = json.dumps(updated, ensure_ascii=False)
                cur.execute(
                    "UPDATE user_signatures SET signature = ?, updated_at = ? WHERE user_id = ?",
                    (sig_json, now, user_id)
                )

                conn.commit()
                conn.close()
                return updated, True, changed_fields
            else:
                # No actual changes after pruning → Treat as no update
                conn.close()
                return existing, False, []

            
        else:
            # No new information provided → Use existing values directly (no update)

            conn.close()
            changed_fields = []
            return existing, False, changed_fields


# ==================== Command Line Support (For OpenClaw Exec) ====================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process user signature information")
    parser.add_argument("--user_id", type=str, required=True, help="用户ID")
    parser.add_argument("--provided_signature", type=str, default="{}", 
                        help="Provided signature info (JSON string)")
    
    args = parser.parse_args()
    
    try:
        provided = json.loads(args.provided_signature)
    except json.JSONDecodeError:
        print(json.dumps({"error": "provided_signature argument is not a valid JSON"}, ensure_ascii=False))
        sys.exit(1)
    
    # Call the core function
    latest_signature, did_write, changed_fields = process_user_signature(args.user_id, provided)
    
    # Generate the formatted signature string
    formatted_signature = format_signature(latest_signature)

    # Must print JSON output; otherwise, OpenClaw cannot retrieve the results
    result = {
        "latest_signature": latest_signature,
        "formatted_signature": formatted_signature,
        "did_write": did_write,
        "changed_fields": changed_fields,
    }
    
    print(json.dumps(result, ensure_ascii=False))

