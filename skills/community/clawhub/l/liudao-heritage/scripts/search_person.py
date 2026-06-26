import sys
import json
import os

bot_dir = "/home/admin/.openclaw/workspace/liudao-bot"
sys.path.append(bot_dir)
os.chdir("/home/admin/.openclaw/workspace")

try:
    from db_manager import DBManager
except ImportError:
    print(json.dumps({"error": "Could not import DBManager"}))
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing query argument"}))
        sys.exit(1)
        
    query = sys.argv[1]
    viewer_id = None
    
    # Parse optional --viewer_id
    if len(sys.argv) > 3 and sys.argv[2] == "--viewer_id":
        viewer_id = sys.argv[3]
        
    db = DBManager()
    results = db.search_person(query, viewer_id=viewer_id)
    
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
