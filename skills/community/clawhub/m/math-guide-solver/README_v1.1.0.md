# 🧮 Math-Solver Skill

<div align="center">

**Intelligent Mathematical Problem Solver with Formula Rendering**

[![Version](https://img.shields.io/badge/version-1.1.0-blue)](https://github.com/yshajoy-star/math-solver/releases/tag/v1.1.0)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-orange)](https://github.com/openclaw)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

[English](#english) | [中文](#中文)

</div>

---

## 📌 Latest Version: v1.1.0

**Release Date**: March 21, 2026

### ✨ What's New in v1.1.0

🎨 **Formula Rendering**
- LaTeX formulas now automatically render as beautiful PNG images
- Formulas embed directly in solution steps (not collected at the end)
- No more raw LaTeX code in the output

🎭 **Visual Themes**
- Support for 4 professional themes: light, dark, sepia, chalk
- Responsive HTML design with professional styling
- Configurable DPI (150, 300, 600)

🔍 **Smart Formula Processing**
- Automatic LaTeX extraction from problem text
- Automatic formula positioning within solution steps
- Support for complex mathematical expressions

📊 **Output Formats**
- HTML format with embedded formulas
- JSON format with formula separation
- Base64 encoded images for portability

[🔄 View full changelog](CHANGELOG.md)

---

## 🚀 Installation

### Option 1: Register from GitHub

```bash
openclaw skill register https://github.com/yshajoy-star/math-solver
```

### Option 2: Register Locally

```bash
cd /path/to/math-solver
openclaw skill register ./
```

### Requirements

- Python 3.8+
- OpenClaw framework
- Dependencies: see `skill.config.json`

---

## 💡 Usage

### Basic Usage

```python
from scripts.formula_image_generator import (
    StepEmbeddedSolutionFormatter,
    SolutionRenderer
)

# Create formatter
formatter = StepEmbeddedSolutionFormatter(theme='light', dpi=300)

# Your solution data
solution = {
    'problem_text': 'Mathematical problem with $formula$',
    'steps': [
        {
            'title': 'Step 1',
            'text': 'Explanation with $equation$'
        },
        # ... more steps
    ]
}

# Generate HTML with embedded formulas
result = formatter.format_solution_with_embedded_images(solution)
html = SolutionRenderer.render_to_html(result)

# Save or display
with open('solution.html', 'w') as f:
    f.write(html)
```

### Themes

Choose from 4 visual themes:

```python
# Light theme (white background, black text) - default
formatter = StepEmbeddedSolutionFormatter(theme='light')

# Dark theme (dark background, white text)
formatter = StepEmbeddedSolutionFormatter(theme='dark')

# Sepia theme (vintage style)
formatter = StepEmbeddedSolutionFormatter(theme='sepia')

# Chalk theme (blackboard style)
formatter = StepEmbeddedSolutionFormatter(theme='chalk')
```

### DPI Settings

```python
# High quality (600 DPI) - larger file size
formatter = StepEmbeddedSolutionFormatter(dpi=600)

# Medium quality (300 DPI) - balanced
formatter = StepEmbeddedSolutionFormatter(dpi=300)

# Low quality (150 DPI) - smaller file size
formatter = StepEmbeddedSolutionFormatter(dpi=150)
```

---

## 📚 Features

### Mathematical Problem Types

✅ **Inequality Proofs**
- Direct proof and contradiction
- AM-GM inequality applications
- Complex inequality systems

✅ **Condition Analysis**
- Sufficient and necessary conditions
- Logical equivalence testing
- Multi-part condition verification

✅ **General Mathematical Problems**
- Algebraic equations and systems
- Geometric proofs
- Calculus problems
- Number theory

### Solution Modes

- **Socratic**: Guided questioning approach
- **Detailed**: Step-by-step comprehensive solution
- **Quick**: Fast solution with key steps

### Problem Classification

- **Domain Detection**: Algebra, Geometry, Calculus, etc.
- **Difficulty Assessment**: Easy, Medium, Hard
- **Strategy Recommendation**: Optimal solving method

---

## 🎨 Formula Rendering

### Before (v1.0.0)

```
Step 1: Analysis
Problem: $a + b + c = 1$, prove $b > \frac{1}{3}$

─────────────────────────────────────
[All formulas collected at the end]
$a + b + c = 1$
$b > \frac{1}{3}$
$c > \frac{1}{3}$
```

### After (v1.1.0)

```
Step 1: Analysis
Problem: [Beautiful rendered formula image for a + b + c = 1]
Proof: [Beautiful rendered formula image for b > 1/3]

Step 2: Proof
Assume: [Formula image embedded here]
Result: [Formula image embedded here]
```

---

## 📁 Project Structure

```
math-solver/
├── README.md                           # This file
├── CHANGELOG.md                        # Version history
├── LICENSE                             # MIT License
├── skill.config.json                   # Skill configuration
├── SKILL.md                            # Skill documentation
│
├── scripts/
│   ├── formula_image_generator.py     # v2: Formula rendering & embedding
│   ├── generate_solution.py           # Solution generation
│   ├── process_math_problem.py        # Problem processing
│   └── ...
│
├── references/
│   ├── QUICKSTART.md                  # Quick start guide
│   ├── EXAMPLES.md                    # Usage examples
│   └── ...
│
└── tests/
    └── test_embedded_solution.py      # Test suite
```

---

## 🔧 Configuration

### skill.config.json

```json
{
  "name": "math-solver",
  "version": "1.1.0",
  "dependencies": {
    "paddleocr-doc-parsing": ">=1.0.0",
    "math-images": ">=1.0.0",
    "matplotlib": ">=3.5.0",
    "Pillow": ">=9.0.0"
  }
}
```

---

## 📊 Examples

### Example 1: Inequality Proof

**Problem**: Given a+b+c=1, 0<a<b<c<1, prove b>1/3

**Output**: Beautiful HTML with:
- Problem statement with rendered formula
- 5 detailed steps
- Each step has embedded formula images
- Light/Dark/Sepia/Chalk theme options

### Example 2: Condition Analysis

**Problem**: Is "abc=1" sufficient/necessary for "a+b+c≥1/√a+1/√b+1/√c"?

**Output**:
- Problem analysis
- P→Q verification with formulas
- Q→P counterexample with formulas
- Clear conclusion

---

## 🚀 Performance

| Metric | Value |
|--------|-------|
| Average solve time | <1 second |
| Formula rendering time | <100ms per formula |
| HTML output size | 300-500 KB |
| Supported formula complexity | High |
| DPI quality | 150-600 (configurable) |

---

## 🛠️ Development

### Running Tests

```bash
cd /path/to/math-solver
python scripts/test_embedded_solution.py
```

### Building from Source

```bash
git clone https://github.com/yshajoy-star/math-solver.git
cd math-solver
openclaw skill register ./
```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Support

### Documentation

- [📖 Quick Start Guide](references/QUICKSTART.md)
- [💡 Usage Examples](references/EXAMPLES.md)
- [📚 Full Changelog](CHANGELOG.md)
- [🔧 Skill Documentation](SKILL.md)

### Issues & Questions

- 🐛 [Report Issues](https://github.com/yshajoy-star/math-solver/issues)
- 💬 [Discussions](https://github.com/yshajoy-star/math-solver/discussions)

---

## 👨‍💻 Author

**Jayson Yin** (yshajoy-star)

- GitHub: [@jayson-tech](https://github.com/jayson-tech)
- Email: yshajoy@gmail.com

---

## 🌟 Acknowledgments

Built with:
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) for document parsing
- [Matplotlib](https://matplotlib.org/) for formula rendering
- [OpenClaw](https://github.com/openclaw) framework

---

## 📈 Version History

| Version | Date | Notes |
|---------|------|-------|
| [1.1.0](https://github.com/yshajoy-star/math-solver/releases/tag/v1.1.0) | 2026-03-21 | LaTeX rendering & formula embedding |
| [1.0.0](https://github.com/yshajoy-star/math-solver/releases/tag/v1.0.0) | 2026-03-20 | Initial release |

---

<div align="center">

**Made with ❤️ for math education**

[⬆ back to top](#-math-solver-skill)

</div>
