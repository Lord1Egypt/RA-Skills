import json
import datetime
import os
import sys
import re

# Ensure the current directory is in sys.path to import local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from pregnancy_checklist import CHECKLIST_DATA
except ImportError:
    # Fallback if running from a different directory structure
    try:
        from scripts.pregnancy_checklist import CHECKLIST_DATA
    except ImportError:
        CHECKLIST_DATA = {} # Should not happen in correct setup

# Use a writable directory for data storage
# The user specified: workspace/data/pregnancy-care
# We'll use an absolute path based on the environment or a safe default
if os.name == 'nt':
    # Windows environment
    WORKSPACE_ROOT = r"d:\workspace"
else:
    # Linux/Unix environment
    WORKSPACE_ROOT = os.path.expanduser("~/workspace")

DATA_DIR = os.path.join(WORKSPACE_ROOT, "data", "pregnancy-care")
DATA_FILE = os.path.join(DATA_DIR, 'user_data.json')

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
        except OSError as e:
            print(f"Error creating data directory: {e}", file=sys.stderr)

def load_all_data():
    ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}", file=sys.stderr)
        return {}

def save_all_data(data):
    ensure_data_dir()
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving data: {e}", file=sys.stderr)

def get_user_data(user_id):
    all_data = load_all_data()
    return all_data.get(user_id, {})

def update_user_data(user_id, updates):
    all_data = load_all_data()
    user_data = all_data.get(user_id, {})
    user_data.update(updates)
    all_data[user_id] = user_data
    save_all_data(all_data)
    return user_data

def parse_date(date_str):
    """
    Parses date string using regex. Returns datetime.date object or None.
    Supports: YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD, MM-DD, MM/DD
    """
    if not date_str:
        return None
        
    # Patterns for YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD
    full_date_patterns = [
        r'(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})',
        r'(\d{4})年(\d{1,2})月(\d{1,2})日'
    ]
    
    for pattern in full_date_patterns:
        match = re.search(pattern, date_str)
        if match:
            try:
                year, month, day = map(int, match.groups())
                return datetime.date(year, month, day)
            except ValueError:
                continue

    # Patterns for MM-DD, MM/DD (assumes current year or next occurrence if passed)
    short_date_patterns = [
        r'(\d{1,2})[-/.](\d{1,2})',
        r'(\d{1,2})月(\d{1,2})日'
    ]
    
    for pattern in short_date_patterns:
        match = re.search(pattern, date_str)
        if match:
            try:
                month, day = map(int, match.groups())
                year = datetime.date.today().year
                return datetime.date(year, month, day)
            except ValueError:
                continue
                
    return None

def calculate_weeks(lmp_date):
    """
    Calculates weeks and days since LMP.
    """
    if not lmp_date:
        return None, None
    today = datetime.date.today()
    delta = today - lmp_date
    weeks = delta.days // 7
    days = delta.days % 7
    return weeks, days

def get_trimester_key(weeks):
    if weeks < 13:
        return "first_trimester"
    elif weeks < 28:
        return "second_trimester"
    else:
        return "third_trimester"

def get_checklist_status(user_data, current_weeks):
    """
    Identifies upcoming milestones (standard + custom) and filters out completed ones.
    """
    completed_tasks = user_data.get("completed_tasks", [])
    upcoming_tasks = []
    
    # 1. Standard Milestones
    for trimester_key, trimester_data in CHECKLIST_DATA.items():
        for milestone in trimester_data.get("milestones", []):
            task_id = milestone["id"]
            if task_id in completed_tasks:
                continue
                
            start = milestone["week_start"]
            reminder_weeks = milestone.get("reminder_weeks_before", 1)
            
            is_upcoming = (start - reminder_weeks) <= current_weeks <= (start + 1)
            is_overdue = current_weeks > (start + 1)
            
            if is_upcoming:
                m_copy = milestone.copy()
                m_copy["status"] = "upcoming"
                upcoming_tasks.append(m_copy)
            elif is_overdue:
                if current_weeks - start < 4: # Only remind if recently overdue
                    m_copy = milestone.copy()
                    m_copy["status"] = "overdue"
                    upcoming_tasks.append(m_copy)

    # 2. Custom Milestones
    custom_milestones = user_data.get("custom_milestones", [])
    for cm in custom_milestones:
        task_id = cm.get("id")
        if task_id in completed_tasks:
            continue
            
        target_week = cm.get("week")
        if target_week is None:
            continue
            
        # Simple logic for custom reminders: 1 week before
        if (target_week - 1) <= current_weeks <= (target_week + 1):
             cm_copy = cm.copy()
             cm_copy["status"] = "upcoming"
             upcoming_tasks.append(cm_copy)
        elif current_weeks > (target_week + 1) and (current_weeks - target_week < 4):
             cm_copy = cm.copy()
             cm_copy["status"] = "overdue"
             upcoming_tasks.append(cm_copy)
             
    return upcoming_tasks

def mark_task_complete(user_id, task_id):
    user_data = get_user_data(user_id)
    completed = user_data.get("completed_tasks", [])
    
    if task_id not in completed:
        completed.append(task_id)
        update_user_data(user_id, {"completed_tasks": completed})
        return True
    return False

def add_custom_milestone(user_id, title, week, description=""):
    user_data = get_user_data(user_id)
    custom = user_data.get("custom_milestones", [])
    
    new_id = f"custom_{len(custom)}_{int(datetime.datetime.now().timestamp())}"
    new_milestone = {
        "id": new_id,
        "title": title,
        "week": week,
        "description": description,
        "created_at": str(datetime.date.today())
    }
    
    custom.append(new_milestone)
    update_user_data(user_id, {"custom_milestones": custom})
    return new_milestone

def set_user_role(user_id, role, relationship=None):
    """
    Sets the user's role (pregnant_person, partner, family, etc.) and relationship.
    """
    update_user_data(user_id, {
        "role": role,
        "relationship": relationship
    })

def archive_pregnancy(user_id):
    """
    Archives the current pregnancy data and returns a summary.
    """
    user_data = get_user_data(user_id)
    if not user_data:
        return {"error": "NO_DATA"}
        
    summary = {
        "lmp": user_data.get("lmp"),
        "completed_tasks": len(user_data.get("completed_tasks", [])),
        "custom_milestones": len(user_data.get("custom_milestones", [])),
        "archived_at": str(datetime.date.today())
    }
    
    update_user_data(user_id, {
        "status": "archived",
        "archived_at": str(datetime.date.today())
    })
    
    return summary

def get_pregnancy_context(user_id, lmp_input=None):
    """
    Main entry point.
    user_id: Unique identifier for the user.
    lmp_input: Optional date string or description.
    """
    user_data = get_user_data(user_id)
    
    # Check if archived
    if user_data.get("status") == "archived":
        return {"status": "archived", "message": "This pregnancy tracking has been completed."}

    # Handle LMP update
    if lmp_input:
        parsed_date = parse_date(lmp_input)
        if parsed_date:
            user_data = update_user_data(user_id, {"lmp": str(parsed_date)})
        else:
            # If input provided but cannot parse, return error to let Agent handle via LLM
            if not user_data.get("lmp"):
                 return {"error": "INVALID_DATE_FORMAT", "input": lmp_input}

    stored_lmp_str = user_data.get("lmp")
    if not stored_lmp_str:
        return {"error": "LMP_MISSING"}

    try:
        stored_lmp = datetime.datetime.strptime(stored_lmp_str, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "CORRUPTED_DATA"}

    weeks, days = calculate_weeks(stored_lmp)
    
    # Check for completion (e.g., > 42 weeks)
    if weeks > 42:
        return {
            "status": "post_term", 
            "weeks": weeks, 
            "message": "Pregnancy duration has exceeded 42 weeks. Consider archiving."
        }

    trimester_key = get_trimester_key(weeks)
    trimester_data = CHECKLIST_DATA.get(trimester_key, {})
    
    upcoming_tasks = get_checklist_status(user_data, weeks)
    
    return {
        "user_id": user_id,
        "role": user_data.get("role", "unknown"),
        "relationship": user_data.get("relationship", ""),
        "weeks": weeks,
        "days": days,
        "trimester": trimester_key,
        "advice": trimester_data.get("advice", {}),
        "upcoming_tasks": upcoming_tasks,
        "completed_tasks": user_data.get("completed_tasks", []),
        "custom_milestones": user_data.get("custom_milestones", [])
    }

if __name__ == "__main__":
    # Simple CLI test
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        u_id = sys.argv[2] if len(sys.argv) > 2 else "test_user"
        
        if cmd == "context":
            val = sys.argv[3] if len(sys.argv) > 3 else None
            print(json.dumps(get_pregnancy_context(u_id, val), indent=2, ensure_ascii=False))
        elif cmd == "complete":
            task = sys.argv[3]
            print(mark_task_complete(u_id, task))
        elif cmd == "add_custom":
            title = sys.argv[3]
            week = int(sys.argv[4])
            print(add_custom_milestone(u_id, title, week))
        elif cmd == "archive":
            print(archive_pregnancy(u_id))
    else:
        print("Usage: python pregnancy_helper.py [context|complete|add_custom|archive] [user_id] [args...]")
