# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
#     "python-dotenv",
#     "rich",
# ]
# ///

import os
import argparse
import requests
import json
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

load_dotenv()
console = Console()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

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

def analyze_post(draft_text):
    if not GEMINI_API_KEY:
        console.print("[bold red]Error:[/bold red] GEMINI_API_KEY not found in environment.")
        return

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Here is my draft LinkedIn post:\n\n---\n{draft_text}\n---\n\n{SYSTEM_PROMPT}"}]
        }]
    }

    with console.status("[bold green]Analyzing post against top-performers..."):
        try:
            response = requests.post(API_URL, params=params, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            content = result['candidates'][0]['content']['parts'][0]['text']
            
            console.print(Panel(Markdown(content), title="🤖 Feedback Loop Analysis", border_style="blue"))
            
        except Exception as e:
            console.print(f"[bold red]Analysis Failed:[/bold red] {e}")
            if 'response' in locals():
                console.print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LinkedIn Post Optimizer & Feedback Loop")
    parser.add_argument("text", help="Draft text of your post")
    args = parser.parse_args()

    analyze_post(args.text)
