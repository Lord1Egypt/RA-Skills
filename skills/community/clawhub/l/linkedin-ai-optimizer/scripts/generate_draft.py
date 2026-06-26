import os
import sys
import json
import argparse
from rich.console import Console
from rich.panel import Panel
import requests
from dotenv import load_dotenv

load_dotenv()
console = Console()

# Configuration
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
RESEARCH_FILE = os.path.join(MEMORY_DIR, "research_notes.md")
DRAFT_FILE = os.path.join(MEMORY_DIR, "draft_post.md")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

SYSTEM_PROMPT = """
You are a LinkedIn Viral Content Expert. 
Write a high-impact LinkedIn post based on the research notes provided.

Structure:
1. **Hook**: Grab attention in the first line (no clickbait, just value).
2. **Body**: 2-3 short paragraphs explaining the trend and why it matters. Use bullet points if applicable.
3. **Takeaway**: One sentence actionable advice or insight.
4. **CTA**: A simple question to spark discussion.

Tone: Professional, insightful, slightly provocative but grounded in facts.
Max Length: 150-200 words.
Output Format: Plain text (no markdown code blocks).
"""

def generate_draft():
    if not os.path.exists(RESEARCH_FILE):
        console.print(f"[bold red]Error:[/bold red] Research file not found at {RESEARCH_FILE}")
        sys.exit(1)

    with open(RESEARCH_FILE, 'r') as f:
        research_notes = f.read()

    if not GEMINI_API_KEY:
        console.print("[bold red]Error:[/bold red] GEMINI_API_KEY not found.")
        sys.exit(1)

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{SYSTEM_PROMPT}\n\nResearch Notes:\n{research_notes}"}]
        }]
    }

    with console.status("[bold green]Generating draft post..."):
        try:
            response = requests.post(API_URL, params=params, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            draft_content = result['candidates'][0]['content']['parts'][0]['text']
            
            with open(DRAFT_FILE, 'w') as f:
                f.write(draft_content)
                
            console.print(Panel(draft_content, title="📝 Generated Draft", border_style="blue"))
            console.print(f"[green]Draft saved to {DRAFT_FILE}[/green]")
            
        except Exception as e:
            console.print(f"[bold red]Generation Failed:[/bold red] {e}")
            sys.exit(1)

if __name__ == "__main__":
    generate_draft()
