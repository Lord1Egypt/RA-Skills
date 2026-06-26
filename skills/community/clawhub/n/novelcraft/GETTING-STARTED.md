# NovelCraft - Getting Started Guide

**Welcome to NovelCraft!** This guide will help you create your first book - safely and step by step.

---

## 📋 Before You Start

### 1. Check System Requirements

```bash
# Required programs
which pandoc    # Document conversion
which xelatex   # PDF generation (optional but recommended)

# If not installed:
# Ubuntu/Debian: sudo apt-get install pandoc texlive-xetex
# macOS: brew install pandoc --with-cask mactex
# Windows: https://pandoc.org/installing.html
```

### 2. Choose Safe Mode

For your first project, we recommend **step-by-step**:
```
/novelcraft setup
→ Select: "step-by-step" (not autonomous)
```

This keeps you in control of every step.

---

## 🚀 Your First Project (15 Minutes)

### Step 1: Create Project

```
/novelcraft project

Name: My First Book
Location: ~/.openclaw/workspace/novelcraft/Books/projects/my-first-book/
```

### Step 2: Select Target Audience

```
/novelcraft setup

Profile: early-readers (ages 6-8)
  → 800-1,200 words per chapter
  → Large font (14pt)
  → Chapter images: yes

Or: adult (25+)
  → 5,000-8,000 words per chapter
  → Normal font (10pt)
  → Chapter images: no
```

### Step 3: Create Concept (Phase 1)

NovelCraft will ask you for:
- **Genre**: Fantasy, Sci-Fi, Mystery, Romance...
- **Title**: Your book name
- **Main Characters**: 3-5 characters
- **Plot**: Brief summary

**Example Input:**
```
Genre: Fantasy Adventure
Title: The Lost Key
Characters: 
  - Lisa (12, brave, curious)
  - Max (11, smart, cautious)
  - Professor Zahn (old, wise, mysterious)
Plot: Lisa and Max find an old key and discover a hidden world in their basement.
```

### Step 4: Configure Images (Optional)

```
/novelcraft setup images

Provider: none        # No images (safest start)
# OR
Provider: mflux-webui  # Local MFLUX (if installed)
  → Endpoint: 192.168.2.150:7861
```

**Recommendation for first tests:** `none`

### Step 5: Write Chapters (Phase 4)

NovelCraft now creates chapters **one after the other**:

```
Chapter 1: "The Discovery"
  → Subagent started...
  → Waiting for completion...
  → Review in progress...
  → Your decision: [APPROVE] or [REVISION]

Chapter 2: "The Secret Door"
  → (Starts only after Chapter 1)
```

**You control every chapter!**

---

## ✅ Checklist: First Project

- [ ] `pandoc` installed
- [ ] Project created with `/novelcraft project`
- [ ] Setup with `step-by-step` selected
- [ ] Target audience configured
- [ ] Concept created
- [ ] Images: `none` (first project)
- [ ] Chapter 1 written & approved
- [ ] PDF generated

---

## 🆘 Common Issues

### "pandoc not found"
```bash
# Solution
sudo apt-get install pandoc
# or
brew install pandoc
```

### "Subagent timeout"
```
→ No problem! NovelCraft saves automatically.
→ Resumption will be attempted automatically.
→ See WORKFLOW-FIXES.md for details.
```

### "Wrong chapter created"
```
→ NovelCraft validates every output.
→ On errors: automatic retry (max 3x).
→ Then: manual review.
```

---

## 🎯 Next Steps

After your first successful project:

1. **Autonomous Mode**: `novelcraft setup` → autonomous
2. **Enable Images**: `novelcraft setup images`
3. **Custom Templates**: Adjust `module-*.md` files
4. **More Chapters**: 10-15 chapters for longer stories

---

## 📚 Additional Resources

| File | Content |
|------|---------|
| `SKILL.md` | Complete documentation |
| `setup.md` | Detailed setup guide |
| `SECURITY.md` | Security guidelines |
| `WORKFLOW-FIXES.md` | Technical details |
| `CHANGELOG.md` | Version history |

---

## 💡 Tips from Users

> **Ronny**: "Start with 3-5 chapters for the first test. This gives you a feel for the workflow."

> **ClawHub Team**: "Step-by-step for tests, autonomous for production."

---

**Happy Writing!** 📝✨

*For questions: See SKILL.md or open an issue on GitHub.*
