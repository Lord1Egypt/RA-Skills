---
name: math-solver
description: |
  Complete mathematical problem solving workflow with OCR, LaTeX formula extraction, PNG rendering, and guided solutions.
  
  Use this skill when users want to:
  - Upload math problem images and automatically extract formulas as clean LaTeX
  - Convert LaTeX formulas to beautifully rendered PNG images with customizable themes
  - Get guided step-by-step problem-solving hints (Socratic method)
  - View detailed solutions with mathematical reasoning
  
  Handles single images, batches of images, and markdown files with embedded LaTeX. Supports multiple visual styles and provides both exploratory and detailed explanation modes.
---

# Math Solver Skill

A comprehensive skill for solving math problems from images with formula extraction, rendering, and guided learning.

## Quick Start

### Use Case 1: Image to Solution
```
User: "I have a math problem photo. Can you help me solve it?"
Flow: Image → OCR → LaTeX extraction → Formula PNG → Guided hints → Solution
```

### Use Case 2: LaTeX to PNG
```
User: "Render this LaTeX formula beautifully"
Flow: LaTeX code → math-images skill → PNG with custom styling
```

### Use Case 3: Problem Batch Processing
```
User: "Extract all formulas from my homework photos"
Flow: Multiple images → OCR all → Extract LaTeX → Render PNG grid
```

---

## Core Workflow

### 1. Image Recognition & OCR
When user uploads math problem image(s):
- Use PaddleOCR Document Parsing skill to extract text and formulas
- Identify mathematical expressions, layout, and problem structure
- Output structured markdown with extracted content

**Supported formats:** JPG, PNG, BMP, TIFF, PDF

### 2. LaTeX Extraction & Normalization
- Convert recognized formulas to proper LaTeX syntax
- Handle common variations (fractions, exponents, subscripts, Greek letters)
- Validate LaTeX syntax before rendering
- Preserve mathematical meaning and formatting

**Examples of auto-corrected formats:**
```
Input: "a/b + c/d"          → LaTeX: \frac{a}{b} + \frac{c}{d}
Input: "x^2 + 2x + 1"        → LaTeX: x^{2} + 2x + 1
Input: "sqrt(2) + pi"        → LaTeX: \sqrt{2} + \pi
Input: "∑(i=1 to n)"         → LaTeX: \sum_{i=1}^{n}
```

### 3. Formula Rendering to PNG
Use `math-images` skill to convert LaTeX to high-quality PNG:
- Support multiple themes (light, dark, sepia, chalk)
- Configurable text sizes and colors
- Batch rendering for multiple formulas
- DPI optimization for different use cases

**Output file naming:** `formula_<problem_number>_<formula_id>.png`

### 4. Guided Solution Modes

#### Mode A: Socratic (Exploratory Learning)
Strategy: Ask guiding questions, don't reveal answers directly

Process:
1. **Problem Analysis** - "What does this problem ask you to find?"
2. **Concept Check** - "Which mathematical concept applies here?"
3. **Method Hint** - "What approach would you use?"
4. **Progress Check** - "Show me your work so far. What's the next step?"
5. **Verification** - "Does your answer make sense?"

**When to use:** Student wants to learn, not just get answers

#### Mode B: Detailed Explanation
Strategy: Full step-by-step solution with reasoning

Process:
1. **Problem Understanding** - Restate the problem in clear terms
2. **Formula Extraction** - Identify relevant mathematical formulas
3. **Step-by-Step Solution** - Each step with LaTeX rendering and explanation
4. **Verification** - Check answer validity
5. **Alternative Methods** - Show other approaches if applicable

**When to use:** Student wants complete understanding

#### Mode C: Quick Answer (Minimum Guidance)
Just the answer with brief verification

---

## Configuration Options

### Visual Themes
```yaml
themes:
  light:
    background: white
    text: black
    accent: blue
    
  dark:
    background: "#1e1e1e"
    text: white
    accent: cyan
    
  sepia:
    background: "#f4f1de"
    text: "#2d2d2d"
    accent: "#d4a574"
    
  chalk:
    background: "#2c2c2c"
    text: "#e0e0e0"
    accent: "#ffeb3b"
```

### Rendering Options
```yaml
formula_size: "medium"  # small, medium, large
dpi: 300                 # 150 (fast), 300 (quality), 600 (print)
background_transparent: false
include_explanation: true  # Show formula explanation below
```

---

## Supported Mathematical Domains

### Algebra
- Linear equations: `ax + b = c`
- Quadratic equations: `ax^2 + bx + c = 0`
- Polynomial operations
- Rational expressions
- Systems of equations

### Geometry
- Area and perimeter formulas
- Trigonometric relationships
- Vector operations
- 3D transformations

### Calculus
- Limits and continuity
- Derivatives and integrals
- Series and sequences
- Differential equations

### Statistics
- Mean, variance, standard deviation
- Probability distributions
- Hypothesis testing
- Regression analysis

### Linear Algebra
- Matrix operations
- Eigenvalues and eigenvectors
- Linear transformations
- Determinants

---

## Input & Output Examples

### Example 1: Simple Fraction Problem
**Input Image:** Photo of "Simplify: (1/2) + (1/3)"

**Output:**
```markdown
## Problem Extracted
Simplify: (1/2) + (1/3)

## LaTeX Formula
\frac{1}{2} + \frac{1}{3}

## Rendered Formula
[PNG image with formula]

## Solution Guidance (Socratic Mode)
1. What do we need to do to add fractions?
   → We need a common denominator
2. What's the LCD of 2 and 3?
   → 6
3. Rewrite each fraction with denominator 6...
```

### Example 2: Complex Expression
**Input:** Handwritten quadratic equation image

**LaTeX Extraction:**
```latex
\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
```

**Themed Renderings:**
- Light theme PNG
- Dark theme PNG
- Chalk board theme PNG

---

## API Integration

### Internal Integrations
- **PaddleOCR Document Parsing** - Image to text/formula extraction
- **math-images** - LaTeX to PNG rendering
- **Claude API** - Problem analysis and guidance generation

### External Support
- **Mathpix API** (optional) - High-accuracy formula recognition
- **Wolfram Alpha API** (optional) - Answer verification

---

## Limitations & Edge Cases

### Known Limitations
1. **Handwriting Quality** - Works best with clear, print-like handwriting
2. **Complex Diagrams** - May struggle with embedded geometry diagrams
3. **Incomplete Problems** - Needs full problem statement in image
4. **Multiple Languages** - Optimized for English/Chinese; others may vary

### Error Handling
- If OCR confidence < 70%, ask user to retake clearer photo
- If LaTeX syntax invalid, suggest manual correction
- If problem type unsupported, suggest alternative approaches

---

## User Preferences

When user specifies preferences, save and apply consistently:

```yaml
user_preferences:
  solution_mode: "detailed"  # or "socratic" or "quick"
  theme: "dark"
  language: "en"  # or "zh" for Chinese
  include_diagrams: true
  step_detail_level: "medium"  # high, medium, low
```

---

## Troubleshooting

### "OCR failed to recognize formula"
- Request clearer image
- Try different angle/lighting
- Manually paste LaTeX if available

### "PNG rendering looks wrong"
- Check LaTeX syntax validity
- Try different theme/size settings
- Use math-images skill directly for advanced options

### "I don't understand the guidance"
- Switch to Detailed Explanation mode
- Ask for more specific hints
- Request step-by-step walkthrough

---

## Next Steps

1. **Quick Demo?** Upload a math problem image to test
2. **Configure Preferences?** Choose solution style and theme
3. **Batch Processing?** Upload multiple problem images
4. **Custom Styling?** Specify color/size/format preferences

