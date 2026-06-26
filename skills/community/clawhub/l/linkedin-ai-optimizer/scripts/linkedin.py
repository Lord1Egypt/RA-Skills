# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
#     "python-dotenv",
#     "rich",
# ]
# ///

import os
import json
import time
import argparse
import requests
import mimetypes
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

# Load environment variables
load_dotenv()
console = Console()

API_URL = "https://api.linkedin.com/v2/ugcPosts"
REGISTER_UPLOAD_URL = "https://api.linkedin.com/v2/assets?action=registerUpload"
HISTORY_FILE = "linkedin_history.jsonl"

def get_person_urn(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try /v2/userinfo (openid scope)
    try:
        response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
        if response.status_code == 200:
             return f"urn:li:person:{response.json()['sub']}"
    except Exception as e:
        console.print(f"[yellow]Debug: /v2/userinfo failed: {e}[/yellow]")

    # Try /v2/me (legacy/profile scope)
    try:
        response = requests.get("https://api.linkedin.com/v2/me", headers=headers)
        if response.status_code == 200:
            return f"urn:li:person:{response.json()['id']}"
    except Exception as e:
        console.print(f"[yellow]Debug: /v2/me failed: {e}[/yellow]")
    
    # If both fail, raise the last error from userinfo for clarity
    response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
    response.raise_for_status()

# ... (rest of the file stays same, but I'll write the whole thing to be safe)

def analyze_post_with_gemini(draft_text):
    """Runs the feedback loop using Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[yellow]⚠️  Feedback Loop Skipped:[/yellow] GEMINI_API_KEY not found.")
        return

    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    SYSTEM_PROMPT = """
You are a LinkedIn Viral Content Expert. 
Your goal is to analyze a draft post and provide a feedback loop to maximize reach and engagement.

Steps:
1. **Analyze**: Identify the hook, core value proposition, and call to action (CTA).
2. **Compare**: Compare this draft against the style and structure of top-performing LinkedIn posts in the same niche (based on your training data).
3. **Critique**: List 3 specific weaknesses (e.g., "Hook is too weak", "Wall of text", "Passive voice").
4. **Improve**: Rewrite the post in 2 variations:
    - Variation A: "The Storyteller" (Focus on narrative/emotion).
    - Variation B: "The Value Bomb" (Focus on actionable insights/lists).

Output Format: Markdown.
"""
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Here is my draft LinkedIn post:\n\n---\n{draft_text}\n---\n\n{SYSTEM_PROMPT}"}]
        }]
    }

    with console.status("[bold green]Analyzing post against top-performers..."):
        try:
            response = requests.post(GEMINI_API_URL, params=params, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            content = result['candidates'][0]['content']['parts'][0]['text']
            
            console.print(Panel(Markdown(content), title="🤖 Feedback Loop Analysis", border_style="blue"))
            
        except Exception as e:
            console.print(f"[bold red]Analysis Failed:[/bold red] {e}")

def register_upload(token, person_urn, file_path):
    """Registers an upload with LinkedIn and returns the upload URL and asset URN."""
    file_type = mimetypes.guess_type(file_path)[0]
    is_video = file_type and file_type.startswith("video")
    
    # Correct recipe URNs
    register_type = "urn:li:digitalmediaRecipe:feedshare-video" if is_video else "urn:li:digitalmediaRecipe:feedshare-image"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    # The registerUpload endpoint requires the Owner URN in the request body
    payload = {
        "registerUploadRequest": {
            "recipes": [register_type],
            "owner": person_urn,
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }
    
    response = requests.post(REGISTER_UPLOAD_URL, headers=headers, json=payload)
    if response.status_code != 200:
         console.print(f"[red]Upload Register Error:[/red] {response.text}")
         response.raise_for_status()

    data = response.json()
    
    upload_url = data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    asset_urn = data['value']['asset']
    
    return upload_url, asset_urn

def upload_file(upload_url, file_path, token):
    """Uploads the file content to the registered URL."""
    headers = {"Authorization": f"Bearer {token}"}
    with open(file_path, "rb") as f:
        response = requests.put(upload_url, headers=headers, data=f)
        if response.status_code != 201 and response.status_code != 200:
            console.print(f"[red]File Upload Error:[/red] {response.text}")
            response.raise_for_status()

def log_success(post_id, author_urn, text, media_path=None):
    """Logs the successful post to a history file."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "post_id": post_id,
        "author": author_urn,
        "text": text,
        "media": media_path,
        "status": "published"
    }
    
    try:
        with open(HISTORY_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
        console.print(f"[green]📝 Post logged to {HISTORY_FILE}[/green]")
    except Exception as e:
        console.print(f"[red]⚠️ Failed to log post history: {e}[/red]")

def create_post(token, person_urn, text, media_path=None):
    """Creates a post on LinkedIn."""
    asset_urn = None
    
    if media_path:
        with console.status(f"[bold green]Uploading media: {media_path}..."):
            try:
                upload_url, asset_urn = register_upload(token, person_urn, media_path)
                upload_file(upload_url, media_path, token)
                console.print(f"[green]Media uploaded successfully. Asset URN: {asset_urn}[/green]")
            except Exception as e:
                console.print(f"[bold red]Media Upload Failed:[/bold red] {e}")
                return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    share_content = {
        "shareCommentary": {"text": text},
        "shareMediaCategory": "NONE"
    }
    
    if asset_urn:
        file_type = mimetypes.guess_type(media_path)[0]
        # Robust video check
        is_video = file_type and file_type.startswith("video")
        category = "VIDEO" if is_video else "IMAGE"
        
        share_content["shareMediaCategory"] = category
        share_content["media"] = [
            {
                "status": "READY",
                "description": {"text": "Architecture Diagram"},
                "media": asset_urn,
                "title": {"text": "Clean Core Pattern"}
            }
        ]

    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": share_content
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    with console.status("[bold green]Publishing post..."):
        response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 201:
        post_id = response.json()['id']
        console.print(f"[bold green]✅ Post created successfully! Post ID: {post_id}[/bold green]")
        log_success(post_id, person_urn, text, media_path)
    else:
        console.print(f"[bold red]❌ Failed to create post: {response.status_code} - {response.text}[/bold red]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post to LinkedIn")
    parser.add_argument("text", help="Text content of the post")
    parser.add_argument("--media", help="Path to an image or video file to attach")
    parser.add_argument("--confirm", action="store_true", help="Actually post to LinkedIn (default is preview only)")
    parser.add_argument("--no-feedback", action="store_true", help="Skip the feedback loop")
    
    args = parser.parse_args()
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not token:
        console.print("[bold red]Error: LINKEDIN_ACCESS_TOKEN environment variable is required.[/bold red]")
        exit(1)
        
    person_urn = os.getenv("LINKEDIN_PERSON_URN")
    if not person_urn:
        with console.status("[yellow]Fetching Person URN..."):
            try:
                person_urn = get_person_urn(token)
                console.print(f"[green]Using Person URN: {person_urn}[/green]")
            except Exception as e:
                console.print(f"[bold red]Error fetching Person URN: {e}[/bold red]")
                exit(1)

    if not args.confirm:
        # Run Feedback Loop unless disabled
        if not args.no_feedback:
            analyze_post_with_gemini(args.text)

        console.print("\n[bold yellow]--- 📝 PREVIEW MODE ---[/bold yellow]")
        console.print(f"Author: [cyan]{person_urn}[/cyan]")
        console.print(Panel(args.text, title="Content"))
        if args.media:
            console.print(f"Media: [blue]{args.media}[/blue]")
        console.print("\n[bold red]❌ Post NOT sent. Run with --confirm to publish.[/bold red]")
    else:
        create_post(token, person_urn, args.text, args.media)
