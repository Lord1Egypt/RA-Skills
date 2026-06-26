---
name: latex-writer
description: Generate professional LaTeX documents from templates. Supports academic papers (IEEE/ACM), Chinese thesis (CTeX), CVs (moderncv), and custom templates. Auto-compile to PDF.
version: 1.0.0
author: OpenClaw
---

# LaTeX Writer

Intelligent LaTeX document generator with template management and PDF compilation.

## Features

- 📄 **Academic Templates**: IEEE, ACM, Springer, Elsevier
- 📝 **Chinese Support**: CTeX for thesis and reports
- 👤 **CV/Resume**: moderncv, altacv templates
- 🎨 **Custom Templates**: Import your own .cls files
- 🔧 **Auto Compilation**: xelatex/lualatex with error handling
- 📊 **Figure/Table Support**: Auto-convert markdown tables to LaTeX

## Trigger Conditions

Use this skill when:
1. User asks to "write a paper" with specific format
2. User mentions "LaTeX", "PDF", "typesetting"
3. User needs CV/resume generation
4. User provides content and asks for professional formatting

## Usage Examples

### Academic Paper
```
User: 帮我写一篇 IEEE 格式的机器学习论文，主题是深度学习在医学影像中的应用

Skill Actions:
1. Select IEEEtran template
2. Generate structure: Abstract → Intro → Method → Experiments → Conclusion
3. Ask user for key content points
4. Generate LaTeX with proper math formulas
5. Compile to PDF
```

### Chinese Thesis
```
User: 我要写硕士毕业论文，学校要求用 LaTeX

Skill Actions:
1. Select CTeX template (ctexrep)
2. Configure Chinese fonts (SimSun, SimHei)
3. Setup school-specific requirements
4. Generate chapter structure
```

### CV Generation
```
User: 帮我生成一份软件工程师的英文简历

Skill Actions:
1. Select moderncv template (banking style)
2. Collect user information
3. Format with proper sections
4. Generate PDF
```

## Implementation

See `scripts/` directory for implementation:
- `latex_writer.py` - Main entry point
- `template_manager.py` - Template library management
- `content_parser.py` - Parse user input to structured content
- `latex_generator.py` - Generate LaTeX code
- `pdf_builder.py` - Compile LaTeX to PDF

## Requirements

- Python 3.10+
- TeX Live or MiKTeX (with xelatex)
- CJK fonts for Chinese support
