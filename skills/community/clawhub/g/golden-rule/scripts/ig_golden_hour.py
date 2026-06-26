# /// script
# dependencies = ["requests"]
# ///
import os
import time
import requests
import argparse

def golden_hour_monitor(media_id, keyword, dm_text, duration_minutes=60):
    token = os.environ.get("IG_ACCESS_TOKEN")
    account_id = os.environ.get("IG_ACCOUNT_ID")
    
    if not token or not account_id:
        print("🚨 Error: Missing IG_ACCESS_TOKEN or IG_ACCOUNT_ID.")
        return

    print(f"🕵️‍♂️ Starting Golden Hour Monitor on Post ID: {media_id}")
    print(f"🕒 Monitoring for exactly {duration_minutes} minutes.")
    print(f"🎯 Keyword Trigger: '{keyword}'")
    
    # Store replied comment IDs
    processed_comments = set()
    start_time = time.time()
    
    while (time.time() - start_time) < (duration_minutes * 60):
        try:
            url = f"https://graph.facebook.com/v19.0/{media_id}/comments"
            params = {
                'access_token': token,
                'fields': 'id,text,from'
            }
            response = requests.get(url, params=params)
            comments = response.json().get('data', [])
            
            for comment in comments:
                c_id = comment.get('id')
                c_text = comment.get('text', '').lower()
                
                if c_id not in processed_comments and keyword.lower() in c_text:
                    print(f"🚨 Keyword Detected! Processing comment: '{c_text}'")
                    
                    # 1. Send the Private DM Reply
                    print(f"📨 Sliding into DMs: {dm_text}")
                    payload = { "recipient": { "comment_id": c_id }, "message": { "text": dm_text }, "access_token": token }
                    requests.post(f"https://graph.facebook.com/v19.0/me/messages", json=payload)
                    
                    # 2. Reply publicly to double the engagement
                    print(f"💬 Replying publicly to the comment ID: {c_id}")
                    payload_reply = { "message": "Just sent you a DM with the link! 🚀", "access_token": token }
                    requests.post(f"https://graph.facebook.com/v19.0/{c_id}/replies", data=payload_reply)
                    
                    # 3. Notify Neo (OpenClaw)
                    try:
                        os.system(f"openclaw message send --target webchat --message '🚨 SUCCESS! I just sent the Mock Trading DM to an Instagram user who commented \"BOT\".'")
                    except:
                        pass
                    
                    processed_comments.add(c_id)
            
        except Exception as e:
            print(f"Error querying Graph API: {e}")
        
        # Poll every 2 minutes
        time.sleep(120)
        
    print(f"✅ Golden Hour Monitor finished successfully! Replying to {len(processed_comments)} targeted comments.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instagram Golden Hour Engagement Automator")
    parser.add_argument("--media_id", type=str, required=True, help="The Instagram Media ID to monitor.")
    parser.add_argument("--keyword", type=str, default="interested", help="The keyword to trigger the DM.")
    parser.add_argument("--dm_text", type=str, required=True, help="The text payload you want to DM the user.")
    parser.add_argument("--duration", type=int, default=60, help="Minutes to run the watcher.")
    args = parser.parse_args()
    
    golden_hour_monitor(args.media_id, args.keyword, args.dm_text, args.duration)
