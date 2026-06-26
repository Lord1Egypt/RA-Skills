# LangChain Integration

How to wrap the memegen skill as a [LangChain](https://langchain.com/) Tool.

## Quick Setup

```python
import subprocess
import tempfile
from urllib.parse import quote

from langchain.tools import Tool


def generate_meme(input_text: str) -> str:
    """
    Generate a meme image. Input format: 'template|top_text|bottom_text'
    Example: 'drake|Writing documentation|Writing memes'
    
    For custom backgrounds: 'custom|top_text|bottom_text|background_url'
    """
    parts = input_text.split("|")
    if len(parts) < 2:
        return "Error: Use format 'template|top_text|bottom_text'"
    
    template = parts[0].strip()
    top = parts[1].strip().replace(" ", "_")
    bottom = parts[2].strip().replace(" ", "_") if len(parts) > 2 else "_"
    
    # Build URL
    url = f"https://api.memegen.link/images/{template}/{top}/{bottom}.png"
    
    # Add custom background if provided
    if template == "custom" and len(parts) > 3:
        bg = quote(parts[3].strip(), safe=":/")
        url += f"?background={bg}&width=800"
    else:
        url += "?width=800"
    
    # Download to temp file
    output = tempfile.mktemp(suffix=".png")
    result = subprocess.run(
        ["curl", "-s", "-o", output, url],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        return f"Error downloading meme: {result.stderr}"
    
    return f"Meme saved to: {output}"


meme_tool = Tool(
    name="meme_generator",
    description=(
        "Generate a meme image from a template. "
        "Input: 'template|top_text|bottom_text'. "
        "Templates: drake, fry, rollsafe, spongebob, fine, harold, "
        "gru, pigeon, pooh, db, handshake, same, cmm, wonka, etc. "
        "Use 'custom|top|bottom|image_url' for custom backgrounds."
    ),
    func=generate_meme,
)
```

## Usage with an Agent

```python
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

agent = initialize_agent(
    tools=[meme_tool],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

agent.run("Make a Drake meme about writing tests vs writing code")
```

## Enhanced Version with Template Knowledge

For better template selection, include the template guide from `SKILL.md` in your agent's system prompt:

```python
from pathlib import Path

# Load the skill knowledge
skill_content = Path("SKILL.md").read_text()

system_prompt = f"""You are a meme generation assistant. Use the meme_generator tool.

{skill_content}

When asked to make a meme:
1. Identify the rhetorical pattern (comparison, sarcasm, panic, etc.)
2. Pick the best template for that pattern
3. Write short, punchy text (max ~30 chars per line)
4. Call the tool with 'template|top_text|bottom_text'
"""
```

## With LangChain's Structured Tools

```python
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


class MemeInput(BaseModel):
    template: str = Field(description="Template ID (e.g., 'drake', 'fry', 'fine')")
    top_text: str = Field(description="Top text / first panel")
    bottom_text: str = Field(default="_", description="Bottom text / second panel")
    background_url: str = Field(default=None, description="Custom background URL (use with template='custom')")


def generate_meme_structured(
    template: str,
    top_text: str,
    bottom_text: str = "_",
    background_url: str = None,
) -> str:
    top = top_text.replace(" ", "_")
    bottom = bottom_text.replace(" ", "_") if bottom_text else "_"
    
    url = f"https://api.memegen.link/images/{template}/{top}/{bottom}.png?width=800"
    if background_url and template == "custom":
        bg = quote(background_url, safe=":/")
        url += f"&background={bg}"
    
    output = tempfile.mktemp(suffix=".png")
    subprocess.run(["curl", "-s", "-o", output, url], capture_output=True)
    return f"Meme saved to: {output}"


meme_tool = StructuredTool.from_function(
    func=generate_meme_structured,
    name="meme_generator",
    description="Generate a meme image from a template with top and bottom text.",
    args_schema=MemeInput,
)
```
