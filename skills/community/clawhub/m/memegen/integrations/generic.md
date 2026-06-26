# Generic Integration

How to use the memegen skill with any LLM or AI agent framework.

## The Simplest Approach

**Just include `SKILL.md` in your system prompt.** That's it.

The skill is written as plain markdown that any LLM can read and follow. It contains:
- URL format and encoding rules
- Template catalog with rhetorical patterns
- Known issues and workarounds
- Pillow fallback renderer

```python
# Load the skill into your agent's context
with open("SKILL.md") as f:
    meme_knowledge = f.read()

system_prompt = f"""You are a helpful assistant that can generate memes.

{meme_knowledge}

When asked to make a meme, generate the URL and download the image.
"""
```

## How to Generate a Meme (Any Language)

### Step 1: Build the URL

```
https://api.memegen.link/images/{template}/{top_text}/{bottom_text}.png
```

Replace spaces with `_`, special chars with their codes (see SKILL.md).

### Step 2: Download the Image

```bash
curl -s -o /tmp/meme.png "https://api.memegen.link/images/drake/Writing_docs/Writing_memes.png?width=800"
```

### Step 3: Verify

```bash
file /tmp/meme.png  # Should say "PNG image data"
ls -la /tmp/meme.png  # Should be >10KB
```

### Step 4: Deliver

How you deliver depends on your framework. The meme is just a PNG file at this point.

## Python Example (No Framework)

```python
import subprocess
from urllib.parse import quote

def make_meme(template, top, bottom="", width=800):
    """Generate a meme and return the local file path."""
    top_enc = top.replace(" ", "_").replace("?", "~q")
    bottom_enc = bottom.replace(" ", "_").replace("?", "~q") if bottom else "_"
    
    url = f"https://api.memegen.link/images/{template}/{top_enc}/{bottom_enc}.png?width={width}"
    output = "/tmp/meme.png"
    
    subprocess.run(["curl", "-s", "-o", output, url], check=True)
    return output

# Usage
path = make_meme("drake", "Manual testing", "Writing unit tests")
print(f"Meme saved to {path}")
```

## JavaScript/Node.js Example

```javascript
const { execSync } = require('child_process');

function makeMeme(template, top, bottom = '', width = 800) {
  const topEnc = top.replace(/ /g, '_').replace(/\?/g, '~q');
  const bottomEnc = bottom ? bottom.replace(/ /g, '_').replace(/\?/g, '~q') : '_';
  
  const url = `https://api.memegen.link/images/${template}/${topEnc}/${bottomEnc}.png?width=${width}`;
  const output = '/tmp/meme.png';
  
  execSync(`curl -s -o ${output} "${url}"`);
  return output;
}

// Usage
const path = makeMeme('drake', 'Manual testing', 'Writing unit tests');
console.log(`Meme saved to ${path}`);
```

## Custom Background (Any Template Image)

Use the `custom` template with a `background` URL parameter:

```python
from urllib.parse import quote

bg_url = "https://i.imgflip.com/30b1gx.jpg"  # Drake template from Imgflip
bg_encoded = quote(bg_url, safe=":/")

url = f"https://api.memegen.link/images/custom/Top_text/Bottom_text.png?background={bg_encoded}&width=800"
```

## With OpenAI Function Calling

```python
tools = [{
    "type": "function",
    "function": {
        "name": "generate_meme",
        "description": "Generate a meme image from a template with top and bottom text",
        "parameters": {
            "type": "object",
            "properties": {
                "template": {
                    "type": "string",
                    "description": "Template ID: drake, fry, rollsafe, fine, harold, gru, pooh, etc."
                },
                "top_text": {
                    "type": "string",
                    "description": "Text for the top/first panel (keep under 30 chars)"
                },
                "bottom_text": {
                    "type": "string",
                    "description": "Text for the bottom/second panel (keep under 30 chars)"
                }
            },
            "required": ["template", "top_text"]
        }
    }
}]
```

## With Anthropic Claude Tool Use

```python
tools = [{
    "name": "generate_meme",
    "description": "Generate a meme image. Use the template guide to pick the right template for the joke's rhetorical pattern.",
    "input_schema": {
        "type": "object",
        "properties": {
            "template": {
                "type": "string",
                "description": "Template ID (drake, fry, rollsafe, fine, harold, gru, pooh, db, etc.)"
            },
            "top_text": {
                "type": "string", 
                "description": "Top/first panel text (max ~30 chars)"
            },
            "bottom_text": {
                "type": "string",
                "description": "Bottom/second panel text (max ~30 chars)"
            }
        },
        "required": ["template", "top_text"]
    }
}]
```

## Tips for Any Integration

1. **Include the template guide** — The rhetorical pattern taxonomy in SKILL.md dramatically improves template selection
2. **Keep text short** — Max ~30 characters per line
3. **Download, don't embed** — memegen.link returns 404 status codes; many HTTP clients reject them. Always download the image first
4. **Use `?width=800`** — Default images can be small
5. **Verify the file** — If it's <1KB, the template ID was probably wrong
6. **Custom backgrounds** — Use `custom` template + `?background=URL` for any Imgflip image
