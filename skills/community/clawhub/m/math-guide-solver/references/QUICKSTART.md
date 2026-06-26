---
title: Math Solver Installation & Quick Start
---

# Math Solver Skill - Installation Guide

## Prerequisites

- OpenClaw installed and running
- Python 3.8+
- PaddleOCR Document Parsing skill (automatic dependency)
- math-images skill (automatic dependency)

## Installation Methods

### Method 1: From ClawHub (Easiest)

```bash
npx clawhub@latest install math-solver
```

OpenClaw will automatically:
- Download the skill
- Install dependencies (PaddleOCR, math-images)
- Register with your OpenClaw gateway
- Configure default settings

### Method 2: Manual Installation

1. **Clone the skill repository**
```bash
git clone https://github.com/openclaw/math-solver-skill.git
cd math-solver
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Register with OpenClaw**
```bash
openclaw skill register ./
```

### Method 3: From .skill File

```bash
openclaw skill install /path/to/math-solver.skill
```

## Configuration

### Set User Preferences

Create `~/.openclaw/skills/math-solver/config.json`:

```json
{
  "defaultMode": "socratic",
  "defaultTheme": "light",
  "autoDetectDomain": true,
  "supportedLanguages": ["en", "zh"],
  "renderingDPI": 300,
  "ocrConfidenceThreshold": 0.7
}
```

### Configure Per-Use

You can override defaults when calling the skill:

```
User: "Solve this problem [image] - detailed mode, dark theme"
→ Skill uses: mode=detailed, theme=dark
```

## Quick Start Examples

### Example 1: Simple Problem Image

**User Input:**
```
User: "Here's my math homework problem"
[Uploads image of: "Solve: (x+1)² = 0"]
```

**Skill Flow:**
1. ✓ OCR recognizes: "(x+1)² = 0"
2. ✓ Converts to LaTeX: (x+1)^{2} = 0
3. ✓ Identifies domain: algebra
4. ✓ Renders formula as PNG
5. ✓ Provides Socratic guidance

**Output:**
```
📐 Problem Detected
Domain: Algebra | Difficulty: Easy

Formula (LaTeX):
(x+1)^{2} = 0

[Formula rendered as PNG in light theme]

Socratic Guidance:
1️⃣  What form is this equation?
    → It's a perfect square
2️⃣  What does this equal?
    → Zero
3️⃣  What's the solution?
    → When x + 1 = 0

Need more hints? Ask!
Want full solution? Just say so.
```

### Example 2: LaTeX Input

**User Input:**
```
User: "Render this formula beautifully"
User: "\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}"
```

**Skill Output:**
```
🎨 Rendering Formula...

Recognized: Quadratic Formula

[High-quality PNG with customizable theme]

Available themes:
- Light (default)
- Dark
- Sepia  
- Chalk

Want to change? Just ask!
```

### Example 3: Batch Processing

**User Input:**
```
User: "Extract formulas from all these homework photos"
[Uploads 5 images]
```

**Skill Output:**
```
📦 Processing 5 problems...

Problem 1: Fraction Addition
  LaTeX: \frac{1}{2} + \frac{1}{3}
  Rendered: ✓ formula_001.png

Problem 2: Quadratic Equation
  LaTeX: x^{2} - 5x + 6 = 0
  Rendered: ✓ formula_002.png

Problem 3: Trigonometry
  LaTeX: \sin^{2}(x) + \cos^{2}(x) = 1
  Rendered: ✓ formula_003.png

Problem 4: Calculus
  LaTeX: \lim_{x \to \infty} \frac{1}{x} = 0
  Rendered: ✓ formula_004.png

Problem 5: Statistics
  LaTeX: \sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \mu)^2}
  Rendered: ✓ formula_005.png

✅ All done! Download formulas or ask for solutions.
```

### Example 4: Multi-Stage Solution

**User Progression:**

```
Stage 1: Student uploads image
User: "Can you help me understand this?"
[Image of quadratic equation]

Stage 2: Skill provides hints
Skill: "Socratic mode activated. First hint: What's the variable in this problem?"

Stage 3: Student works through hints
User: "So the variable is x?"
Skill: "Right! Now, what form is this equation in?"

Stage 4: Student gets stuck
User: "I'm stuck. Give me more help."
Skill: "Switching to detailed mode..."
[Shows complete step-by-step solution]

Stage 5: Verification
User: "Is my answer x = 3 correct?"
Skill: "Let me check... Yes, x = 3 works!"
```

## Troubleshooting

### "OCR failed to recognize the formula"

**Cause:** Image quality too low
**Solution:** 
- Retake photo with better lighting
- Ensure handwriting is clear
- Try providing LaTeX manually

```
User: "The photo is too blurry. Here's the LaTeX:"
User: "x^2 + 2x + 1 = 0"
Skill: "Perfect! Processing LaTeX..."
```

### "Unsupported problem type"

**Cause:** Problem domain not recognized
**Solution:** Specify the domain

```
User: "This is a geometry problem about triangles"
Skill: "Got it! Using geometry mode..."
```

### "Formula rendering looks wrong"

**Cause:** Invalid LaTeX syntax
**Solution:** Use alternative notation

```
Original: "sqrt(2)"
Try: "\sqrt{2}"
Or: "√2"
```

## Advanced Usage

### Custom Theme Configuration

```json
{
  "customTheme": {
    "name": "myTheme",
    "backgroundColor": "#1a1a1a",
    "textColor": "#ffffff",
    "accentColor": "#00ff00",
    "fontSize": 16,
    "fontFamily": "TeX Gyre Termes"
  }
}
```

### Batch Processing with Export

```
User: "Process all problems and export to PDF"
Skill: 
1. Processes all images
2. Extracts formulas
3. Renders PNGs
4. Generates PDF report
```

### Integration with Learning Platform

```
OpenClaw Agent can:
- Forward math problems to skill
- Collect formatted solutions
- Generate study materials
- Track student progress
```

## Performance Tips

### For Fast Processing
```json
{
  "dpi": 150,           // Lower quality, faster
  "theme": "light",     // Simpler rendering
  "skipVerification": false
}
```

### For High Quality
```json
{
  "dpi": 600,           // High quality for printing
  "theme": "sepia",     // More complex rendering
  "backgroundColor": "transparent"
}
```

### For Large Batches
```bash
# Process with parallel rendering
openclaw skill call math-solver --batch --parallel=4 *.jpg
```

## Getting Help

### In Conversation
```
User: "How do I use this skill?"
Skill: [Displays this quick start guide]
```

### View Skill Documentation
```
User: "Show me the full documentation"
Skill: [Loads SKILL.md with all details]
```

### Report Issues
```
User: "This formula rendered incorrectly"
Skill: [Collects error details and provides workarounds]
```

## Next Steps

1. **Try a simple example** - Upload a basic math problem
2. **Explore themes** - See different rendering styles
3. **Set preferences** - Customize default behavior
4. **Integrate** - Use with your OpenClaw workflows
5. **Provide feedback** - Help improve the skill

---

**Questions?** Ask OpenClaw: `"Help with math-solver skill"`

**Ready to start?** Upload a math problem image now!
