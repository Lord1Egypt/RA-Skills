# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
#     "python-dotenv",
#     "tabulate",
# ]
# ///

import os
import json
import argparse
import requests
from dotenv import load_dotenv
from tabulate import tabulate

# Load environment variables
load_dotenv()

def get_social_actions(token, post_urn):
    """
    Fetches aggregated likes and comments for a given share URN.
    """
    # The URN in the URL needs to be the object we are querying.
    # For a share, it's /socialActions/{shareUrn}
    url = f"https://api.linkedin.com/v2/socialActions/{post_urn}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 403:
            return {"error": "403 Forbidden (Check 'r_member_social' scope)"}
        if response.status_code != 200:
            return {"error": f"{response.status_code} {response.text}"}
            
        data = response.json()
        return {
            "likes": data.get("likesSummary", {}).get("totalLikes", 0),
            "comments": data.get("commentsSummary", {}).get("totalFirstLevelComments", 0)
        }
    except Exception as e:
        return {"error": str(e)}

def analyze_history(token, history_file):
    if not os.path.exists(history_file):
        print(f"No history file found at {history_file}")
        return

    print(f"📊 Analyzing posts from {history_file}...\n")
    
    table_data = []
    
    with open(history_file, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                urn = entry.get('post_id')
                timestamp = entry.get('timestamp', '')[:16].replace('T', ' ')
                snippet = (entry.get('text', '')[:30] + '...') if len(entry.get('text', '')) > 30 else entry.get('text', '')
                
                if not urn: continue
                
                stats = get_social_actions(token, urn)
                
                if "error" in stats:
                    # If 403, we might stop spamming the API, or just report error
                    if "403" in stats["error"]:
                        table_data.append([timestamp, urn, snippet, "N/A", "N/A", "Missing Scope"])
                    else:
                        table_data.append([timestamp, urn, snippet, "?", "?", stats["error"]])
                else:
                    table_data.append([timestamp, urn, snippet, stats['likes'], stats['comments'], "OK"])
                
            except json.JSONDecodeError:
                pass

    print(tabulate(table_data, headers=["Date", "Post ID", "Content", "Likes", "Comments", "Status"], tablefmt="simple"))
    
    # Check for scope issues
    if any("Missing Scope" in row for row in table_data):
        print("\n⚠️  Note: 'Missing Scope' usually means your token lacks `r_member_social`.")
        print("   This permission is required to read analytics but is often restricted to Marketing Partners.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get LinkedIn Post Analytics")
    parser.add_argument("--post", help="Specific Post URN to analyze")
    parser.add_argument("--history", default="linkedin_history.jsonl", help="Path to history file")
    args = parser.parse_args()
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not token:
        print("Error: LINKEDIN_ACCESS_TOKEN not found.")
        exit(1)

    if args.post:
        stats = get_social_actions(token, args.post)
        print(json.dumps(stats, indent=2))
    else:
        analyze_history(token, args.history)
