---
name: devto-post
description: Post articles to DEV.to using AppleScript Chrome control. Use when user wants to publish technical blog posts, showdev articles, or open source project announcements to DEV.to. Triggers on "post to dev.to", "publish on dev.to", "devto article", "write dev.to post", or any DEV.to publishing request.
homepage: https://canlah.ai
---

# DEV.to Article Posting Skill (AppleScript Chrome Control)

Publish articles to DEV.to by controlling the user's real Chrome via AppleScript. No Playwright needed.

---

## How It Works

```
Claude Code → osascript → Chrome (logged into DEV.to) → CSRF API → Published
```

---

## Prerequisites

- **macOS only** (AppleScript is a macOS technology)
- Chrome: View → Developer → Allow JavaScript from Apple Events (restart after enabling)
- User logged into DEV.to in Chrome

---

## Method Detection

```bash
WINDOWS=$(osascript -e 'tell application "Google Chrome" to return count of windows' 2>/dev/null)
if [ "$WINDOWS" = "0" ] || [ -z "$WINDOWS" ]; then
    echo "METHOD 2 (System Events + Console)"
else
    echo "METHOD 1 (execute javascript)"
fi
```

---

## Recommended: DEV.to Internal API (CSRF Token)

**This is the most reliable method.** The editor form has React state issues (tags concatenate, auto-save drafts persist bad state across reloads). Use the CSRF-protected internal API instead:

### Step 1: Navigate to DEV.to

```bash
osascript -e 'tell application "Google Chrome" to tell active tab of first window to set URL to "https://dev.to"'
sleep 3
```

### Step 2: Publish via CSRF API

```javascript
(async()=>{
  try {
    var csrf = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    var resp = await fetch('/articles', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': csrf
      },
      credentials: 'include',
      body: JSON.stringify({
        article: {
          title: "Your Title",
          body_markdown: "# Full markdown content here...",
          tags: ["opensource", "showdev", "tutorial", "programming"],
          published: true
        }
      })
    });
    var result = await resp.json();
    if (result.current_state_path) {
      document.title = "OK:" + result.current_state_path;
    } else {
      document.title = "ERR:" + JSON.stringify(result);
    }
  } catch(e) {
    document.title = "ERR:" + e.message;
  }
})()
```

### Step 3: Get Published URL

```bash
sleep 3
osascript -e 'tell application "Google Chrome" to return title of active tab of first window'
```

The title will contain `OK:/username/article-slug` — prepend `https://dev.to` to get the full URL.

### Step 4: Session Summary

**Always end with the article link:**

| Platform | Title | Link |
|----------|-------|------|
| DEV.to | "Your Article Title" | https://dev.to/username/article-slug |

---

## For Long Articles: File-Based Approach

For articles too long to inline in JS, write the body to a temp file and inject:

```bash
# Write article content to temp JSON file
python3 -c "
import json
with open('/tmp/devto_body.md') as f:
    body = f.read()
with open('/tmp/devto_body.json', 'w') as f:
    json.dump(body, f)
"

# Use JXA to read the file and publish
osascript -l JavaScript -e '
var chrome = Application("Google Chrome");
var tab = chrome.windows[0].activeTab;
var body = JSON.parse($.NSString.alloc.initWithContentsOfFileEncodingError("/tmp/devto_body.json", $.NSUTF8StringEncoding, null).js);
tab.execute({javascript: "(async()=>{try{var csrf=document.querySelector(\"meta[name=csrf-token]\").getAttribute(\"content\");var resp=await fetch(\"/articles\",{method:\"POST\",headers:{\"Content-Type\":\"application/json\",\"X-CSRF-Token\":csrf},credentials:\"include\",body:JSON.stringify({article:{title:\"YOUR TITLE\",body_markdown:" + JSON.stringify(body) + ",tags:[\"tag1\",\"tag2\"],published:true}})});var r=await resp.json();document.title=r.current_state_path?\"OK:\"+r.current_state_path:\"ERR:\"+JSON.stringify(r)}catch(e){document.title=\"ERR:\"+e.message}})()"});
'
```

---

## Important Gotchas

### Never start body with `---`

DEV.to parses standalone `---` lines as YAML front matter delimiters. Strip them:

```python
import re
body = re.sub(r'^---$', '', body, flags=re.MULTILINE)
```

### Tag Rules
- Maximum 4 tags per article
- Tags must be lowercase
- Pass as array: `tags: ["tag1", "tag2", "tag3", "tag4"]`

### Why NOT to Use the Editor Form

The DEV.to editor has multiple issues:
- **Tag input concatenation**: Enter key doesn't separate tags in the React component
- **Auto-save draft persistence**: Bad state (e.g., malformed tags) persists across page reloads
- **React controlled component conflicts**: Native value setters can corrupt React state

The CSRF API bypasses all of these. **Always prefer the API.**

---

## Alternative: Editor Form (Fallback Only)

If the API doesn't work for some reason, you can fill the editor form directly:

### Fill Title

```bash
osascript -e 'tell application "Google Chrome" to tell active tab of first window to execute javascript "
  var titleInput = document.querySelector(\"#article-form-title\");
  if (!titleInput) titleInput = document.querySelector(\"input[placeholder*=\\\"title\\\"]\");
  if (titleInput) {
    var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, \"value\").set;
    nativeInputValueSetter.call(titleInput, \"Your Article Title Here\");
    titleInput.dispatchEvent(new Event(\"input\", { bubbles: true }));
    document.title = \"TITLE_SET\";
  } else {
    document.title = \"TITLE_NOT_FOUND\";
  }
"'
```

### Fill Body

```bash
osascript -e 'tell application "Google Chrome" to tell active tab of first window to execute javascript "
  var textarea = document.querySelector(\"#article_body_markdown\");
  if (!textarea) textarea = document.querySelector(\"textarea\");
  if (textarea) {
    var nativeTextareaSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, \"value\").set;
    nativeTextareaSetter.call(textarea, \"YOUR MARKDOWN CONTENT\");
    textarea.dispatchEvent(new Event(\"input\", { bubbles: true }));
    document.title = \"BODY_SET\";
  }
"'
```

### Publish Button

```bash
osascript -e 'tell application "Google Chrome" to tell active tab of first window to execute javascript "
  var publishBtn = document.querySelector(\"button[aria-label*=\\\"Publish\\\"]\");
  if (!publishBtn) {
    var buttons = document.querySelectorAll(\"button\");
    for (var b of buttons) { if (b.textContent.trim() === \"Publish\") { publishBtn = b; break; } }
  }
  if (publishBtn) { publishBtn.click(); document.title = \"PUBLISHED\"; }
  else { document.title = \"PUBLISH_NOT_FOUND\"; }
"'
```

---

## Article Template for Open Source Projects

```markdown
[Opening hook - 1-2 sentences about what you built and why]

## The Problem

[Describe the pain point you're solving]
- Bullet point 1
- Bullet point 2
- Bullet point 3

## The Solution: [Project Name]

[Brief description of your solution]

1. **Feature 1** - description
2. **Feature 2** - description
3. **Feature 3** - description

## Getting Started

\`\`\`bash
git clone https://github.com/username/repo
cd repo
pip install -r requirements.txt
\`\`\`

## Key Features

### Feature Name
[Code example]

## Why Open Source?

[Personal story about why you're sharing this]

## Links

- **GitHub**: https://github.com/username/repo

Got questions or suggestions? Drop a comment below!
```

---

## Tag Recommendations

| Project Type | Suggested Tags |
|--------------|----------------|
| Python library | `python`, `opensource`, `api`, `showdev` |
| JavaScript/Node | `javascript`, `node`, `opensource`, `showdev` |
| AI/ML | `ai`, `machinelearning`, `python`, `opensource` |
| DevOps | `devops`, `docker`, `automation`, `opensource` |
| Web app | `webdev`, `react`, `opensource`, `showdev` |
| Tutorial | `tutorial`, `beginners`, `programming`, `webdev` |

---

## Error Handling

| Issue | Solution |
|-------|----------|
| Not logged in | Navigate to dev.to/enter, user logs in manually |
| CSRF token not found | Make sure you're on dev.to domain first |
| Tags error | Max 4 tags, all lowercase, no spaces |
| Content too long | Split into series with `series: "Series Name"` in API body |
| `---` YAML error | Strip standalone `---` lines from body |

---

## Why AppleScript (Not Playwright)

| Tool | Problem |
|------|---------|
| Playwright | Extra setup, may fail on editor interactions |
| **AppleScript** | Controls real Chrome, uses existing login, reliable |

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
