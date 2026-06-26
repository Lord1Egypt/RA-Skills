# OutputForge — Limitations

This document outlines what OutputForge **does NOT do** and known constraints.

---

## What It Doesn't Do

### ❌ Content Generation
OutputForge **formats existing content**. It does not:
- Generate new content from prompts
- Expand short content into long articles
- Rewrite content for different audiences
- Translate languages

**What to do instead:** Use your AI assistant to generate content first, then use OutputForge to format it.

---

### ❌ Image Handling
OutputForge does not:
- Upload images to platforms
- Resize or optimize images
- Extract images from documents
- Convert image formats

**What it does:** Insert image placeholders with platform-specific syntax. You still need to upload actual images separately.

---

### ❌ Platform API Integration
OutputForge does not:
- Directly publish to WordPress, Medium, etc.
- Authenticate with platform APIs
- Upload content automatically
- Schedule posts

**What it does:** Generate properly formatted output that you can copy-paste or upload manually.

---

### ❌ Advanced Text Processing
OutputForge does not:
- Check grammar or spelling
- Detect plagiarism
- Verify facts
- Check for logical consistency
- Perform semantic analysis

**What it does:** Format and clean text. Content quality is your responsibility.

---

### ❌ Real-Time Collaboration
OutputForge does not:
- Support multi-user editing
- Track changes like Google Docs
- Resolve merge conflicts
- Provide version control

**What it does:** Process files one at a time. Use Git for version control if needed.

---

### ❌ Complex Document Structures
OutputForge does not handle:
- Tables (converts to text approximations)
- Footnotes/endnotes
- Cross-references
- Table of contents generation
- Index generation
- Bibliography management

**What it does:** Format simple text with headers, paragraphs, lists, and basic formatting.

---

## Known Constraints

### Text Format Support
- **Input:** Plain text only (.txt files or stdin)
- **No support for:** DOCX, PDF, RTF, ODT, Google Docs
- **Workaround:** Copy-paste from those formats to .txt first, or use external conversion tools

### Character Encoding
- **Default:** UTF-8
- **No automatic detection** of other encodings
- **Workaround:** Convert files to UTF-8 before processing

### Markdown Parsing
- **Simple markdown only:** Headers, bold, italic, code, links
- **No support for:** Tables, task lists, extended syntax (mermaid, etc.)
- **Workaround:** Use dedicated markdown processors for complex documents

### LaTeX Output
- **Basic document structure only**
- **No support for:** Complex math equations, bibliographies, custom packages
- **Workaround:** Use OutputForge for initial structure, then enhance manually

### Thread Splitting Intelligence
- Splits by paragraphs and sentences
- **Does NOT:**
  - Understand narrative flow
  - Preserve dramatic tension
  - Keep related ideas together beyond sentence boundaries
- **Workaround:** Review threads and manually adjust if needed

### Platform-Specific Features
- **WordPress:** Generates HTML, not native Gutenberg blocks
- **Medium:** No direct import — manual paste required
- **LinkedIn:** No rich media embeds
- **Workaround:** Manual adjustments for advanced platform features

---

## Performance Constraints

### File Size
- **Recommended max:** 10 MB per file
- **Large files (>10 MB):** May be slow, risk memory issues
- **Workaround:** Split large files before processing

### Batch Processing
- **No parallelization:** Processes files one at a time
- **Large batches (>1000 files):** May be slow
- **Workaround:** Split into smaller batches or use shell scripting for parallel execution

### Cleanup Accuracy
- **Pattern-based:** Uses regex, not semantic understanding
- **False positives possible:** Legitimate phrases may be removed if they match patterns
- **False negatives possible:** Some AI-isms may not be caught
- **Workaround:** Review output, adjust custom rules in config

---

## Security & Privacy

### No Cloud Processing
- **All processing is local** — good for privacy
- **No spell-check APIs** or cloud services
- **No analytics or telemetry**

### Input Trust
- **Assumes input is safe text**
- **No sanitization for malicious content** (e.g., script injection in HTML formats)
- **Workaround:** Only process content you trust

### Output Trust
- **Generated HTML/LaTeX/etc. is not sanitized** for all possible injection attacks
- **Do not paste into admin panels** without reviewing if input source is untrusted
- **Workaround:** Review output before publishing to production systems

---

## Platform Limitations

### Python Version
- **Requires Python 3.7+**
- **Not tested on Python 2.x** (EOL anyway)
- **No backwards compatibility** for older Python versions

### Operating Systems
- **Tested on:** Linux, macOS, Windows 10+
- **Windows:** Line endings may differ (`\r\n` vs `\n`)
- **Workaround:** Configure line endings in config file

### File System
- **Requires write permissions** to output directory
- **No cloud storage integration** (Google Drive, Dropbox, etc.)
- **Workaround:** Use local filesystem, sync with cloud manually

---

## Customization Limits

### Template System
- **Python code required** for custom templates
- **No visual template editor**
- **No template marketplace**
- **Workaround:** Copy and modify existing templates from output_templates.py

### AI-ism Detection
- **Pattern-based only** — not ML-powered
- **New AI phrases** won't be caught until added to patterns
- **Workaround:** Add custom patterns to config as you discover new AI-isms

---

## What We Might Add (Future Considerations)

These are **not promises**, just ideas for future versions:

- 📊 Basic table support (ASCII/markdown tables)
- 🌐 HTML/Markdown input parsing
- 🔄 Round-trip format conversion
- 📈 Content statistics (readability scores, etc.)
- 🎨 CSS theme customization for HTML outputs
- 🔌 Plugin system for third-party templates
- 📱 Platform API integrations (opt-in)

**No timeline for these. Use the tool as-is.**

---

## Bottom Line

OutputForge is a **focused tool** that does one thing well: format AI output for platforms.

It's not:
- A CMS
- A publishing platform
- A content generator
- An all-in-one content suite

**If you need those features, use OutputForge as one part of your workflow, not the whole solution.**

---

## Reporting Issues

If you find a bug or limitation not listed here:

1. Check if it's a configuration issue (see config_example.json)
2. Try adjusting cleanup rules or templates
3. Document the issue clearly with example input/output
4. Share with the community

**Remember:** This is a community tool. Contributions welcome.

---

**Know the limits. Use the tool effectively.**
