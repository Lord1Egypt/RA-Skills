# OutputForge — AI Output Formatter

**Transform raw AI output into platform-ready content with proper formatting, metadata, and cleanup.**

Author: Shadow Rose  
License: MIT  
Quality: quality-verified

---

## What It Does

You've just gotten great output from your AI assistant. Now what? Copy-pasting into WordPress, Medium, or social media means:

- Manual formatting cleanup
- Removing "As an AI..." disclaimers
- Splitting long content into threads
- Adding metadata and structure
- Converting to platform-specific formats

**OutputForge does all of this automatically.**

Paste raw AI text → get platform-ready content in seconds.

---

## Quick Start

```bash
# Basic usage - format for WordPress
python output_forge.py my_ai_output.txt -f wordpress -o post.html

# Clean AI-isms and format for Medium
python output_forge.py raw_output.txt -f medium --title "My Article" --author "Jane Doe"

# Split long content into Twitter thread
python output_forge.py long_article.txt -f twitter -o thread.txt

# Batch process an entire directory
python output_forge.py --batch input_dir/ output_dir/ -f markdown

# Read from stdin
cat ai_response.txt | python output_forge.py -f plain
```

---

## Features

### 📝 Multiple Output Formats

- **WordPress** — HTML with proper block editor structure
- **Medium** — Clean markdown with formatting that renders perfectly
- **Email Newsletter** — Responsive HTML with inline CSS
- **Twitter/X** — Smart thread splitting with numbering
- **LinkedIn** — Professional formatting with hashtags
- **Markdown** — Clean markdown with frontmatter metadata
- **LaTeX** — Academic document format
- **Plain Text** — Minimal formatting for anywhere

### 🧹 AI-ism Cleanup

Automatically removes common AI hedging and disclaimers:

- "As an AI language model..."
- "It's important to note that..."
- "I don't have personal opinions, but..."
- Repetitive "However," transitions
- Excessive hedging ("perhaps maybe possibly might")
- Unnecessary disclaimers about training cutoffs

**Your content sounds more natural and confident.**

### 🎯 Smart Features

- **Thread Splitting** — Breaks long content into tweet-sized chunks intelligently (by paragraph/sentence)
- **Metadata Injection** — Add title, author, date, tags, description to any format
- **Template System** — Create custom output formats for your specific needs
- **Batch Mode** — Process hundreds of files at once
- **Image Placeholders** — Mark where images should go with platform-specific syntax
- **Link Formatting** — Automatically format links for each platform

### ⚙️ Highly Configurable

Edit `config_example.json` (copy config.json`) to customize:

- Default author and metadata
- Custom cleanup rules (regex patterns)
- Custom output templates
- Thread length limits per platform
- Cleanup aggressiveness (conservative/moderate/aggressive)
- Platform-specific preferences

---

## Usage Examples

### Example 1: WordPress Blog Post

```bash
python output_forge.py ai_draft.txt \
  -f wordpress \
  -o blog_post.html \
  --title "10 Tips for Better Productivity" \
  --author "Alex Johnson" \
  --tags "productivity, tips, work" \
  --description "Discover proven techniques to boost your daily productivity"
```

**Output:** Clean WordPress HTML with proper blocks, metadata, and tags ready to paste into the editor.

### Example 2: Twitter Thread

```bash
python output_forge.py long_article.txt -f twitter -o thread.txt
```

**Input:** 2000-word article  
**Output:** Automatically split into 8 numbered tweets, each under 280 characters, breaking at natural sentence boundaries.

```
1/8 First tweet content here...

---THREAD BREAK---

2/8 Second tweet continues the thought...

---THREAD BREAK---

...
```

### Example 3: Medium Article with Cleanup

```bash
python output_forge.py ai_output.txt \
  -f medium \
  --title "Understanding Quantum Computing" \
  --tags "science, technology, quantum"
```

**Before:**
> As an AI language model, I think that quantum computing is fascinating. However, it's important to note that this field is complex. I don't have personal opinions, but I can explain...

**After:**
> Quantum computing is fascinating. This field is complex, but understandable...

Clean, confident, professional.

### Example 4: Batch Process Directory

```bash
# Process all .txt files in drafts/ and output to published/
python output_forge.py --batch drafts/ published/ -f markdown --author "Team Blog"
```

Processes every file automatically, maintaining filenames with new extensions.

### Example 5: Email Newsletter

```bash
python output_forge.py newsletter_draft.txt \
  -f email \
  -o newsletter.html \
  --title "Weekly Insights - Feb 2026"
```

**Output:** Responsive HTML email with proper styling, ready to send or paste into your email platform.

---

## Command-Line Options

```
positional arguments:
  input                 Input file (or - for stdin)

required arguments:
  -f, --format         Output format: wordpress, medium, email, twitter,
                       linkedin, markdown, latex, plain

optional arguments:
  -o, --output         Output file (default: stdout)
  --batch              Batch mode: input_dir output_dir

metadata options:
  --title              Content title
  --author             Content author
  --date               Publication date (default: today)
  --tags               Comma-separated tags
  --description        SEO description

processing options:
  --no-clean           Disable AI-ism cleanup
  --max-thread-length  Max length for thread posts (default: 280)
  --image-placeholders Add image placeholder markers
```

---

## Custom Templates

Create your own output formats by editing `config_example.json`:

```python
def custom_blog_template(content, metadata, options):
    title = metadata.get('title', 'Untitled')
    author = metadata.get('author', 'Anonymous')
    
    return f"""
# {title}
*by {author}*

{content}

---
Published with OutputForge
    """.strip()

# Register your template
CUSTOM_TEMPLATES['myblog'] = custom_blog_template
```

Then use it:
```bash
python output_forge.py input.txt -f myblog -o output.md
```

---

## AI-ism Cleanup Details

The cleanup engine removes common patterns that make AI-generated text obvious:

### Removed Patterns

✅ **Direct AI references**
- "As an AI language model..."
- "I'm an AI assistant and..."

✅ **Hedging phrases**
- "It's important to note that..."
- "It should be noted that..."
- "Keep in mind that..."

✅ **Unnecessary disclaimers**
- "I don't have personal opinions, but..."
- "I can't access the internet, but..."
- "My training data ends in..."

✅ **Excessive caveats**
- Repetitive "However," transitions (reduces to 2-3 max)
- "That being said," when overused

✅ **Filler words**
- "very very" → "very"
- "really really" → "really"

### Analysis Mode

Want to see what would be cleaned WITHOUT modifying the text?

```bash
python output_clean.py "Your AI text here"
```

Shows:
- Pattern counts
- Hedging ratio
- Passive voice detection
- Suggestions for improvement

---

## Use Cases

### Content Creators
- Convert AI drafts to blog posts
- Generate newsletter HTML
- Format social media content

### Writers
- Clean up AI-assisted writing
- Export to multiple formats
- Maintain consistent metadata

### Marketers
- Process campaign content in bulk
- Format for different platforms
- Remove AI tells from copy

### Developers
- Document generation
- Format code comments to docs
- Batch process documentation

### Teams
- Standardize output formats
- Share custom templates
- Batch process team content

---

## Requirements

**Python 3.7+** (standard library only — no external dependencies)

---

## Installation

```bash
# Clone or download the files
cd output-forge/

# That's it! No dependencies to install.

# Run directly
python output_forge.py --help

# Or make executable (Linux/Mac)
chmod +x output_forge.py
./output_forge.py --help
```

---

## File Structure

```
output-forge/
├── output_forge.py       # Main formatting engine
├── output_templates.py   # Platform templates (WordPress, Medium, etc.)
├── output_clean.py       # AI-ism detection and cleanup
├── config_example.json     # Configuration template
├── README.md             # This file
├── LIMITATIONS.md        # What this tool doesn't do
└── LICENSE               # MIT License
```

---

## Tips & Best Practices

### 1. Start Conservative
Use default cleanup settings first. If output is still too "AI-sounding," increase aggressiveness in config.

### 2. Review Before Publishing
Always review output before publishing. Cleanup is good, but human judgment is better.

### 3. Custom Templates
If you publish to the same platform repeatedly, create a custom template with your exact formatting preferences.

### 4. Batch Processing
When processing directories, use consistent input filenames for easier organization.

### 5. Metadata Matters
Include title, author, tags, and description — most platforms use this for SEO and organization.

### 6. Thread Splitting
For Twitter threads, start with max 260 characters (not 280) to leave room for links/images.

---

## Contributing

This is an open-source tool under the MIT License. Feel free to:

- Fork and modify for your needs
- Submit improvements
- Share custom templates
- Report issues

---

## License

MIT License — see LICENSE file for details.

Free to use commercially and personally.

---

## Author

**Shadow Rose**


---

## FAQ

**Q: Does this work with any AI output?**  
A: Yes — ChatGPT, Claude, Gemini, local models, anything that produces text.

**Q: Can I add my own cleanup rules?**  
A: Absolutely. Edit `config_example.json` and add regex patterns to `DEFAULT_CLEANUP_RULES`.

**Q: Will cleanup remove ALL hedging?**  
A: No. It targets obvious AI patterns and excessive hedging. Legitimate uncertainty expressions remain.

**Q: Can I use this in commercial projects?**  
A: Yes! MIT License allows commercial use.

**Q: What if I need a format not included?**  
A: Create a custom template (see Custom Templates section) or request it as a feature.

**Q: Does it modify my original files?**  
A: Never. Original input files are never modified. Output goes to stdout or a new file you specify.

---

**Ready to transform your AI output? Start with:**

```bash
python output_forge.py --help
```


---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
