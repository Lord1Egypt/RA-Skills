# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-03-21

### Added
- ✨ LaTeX formula automatic rendering to PNG images
- ✨ Formula embedding directly in solution steps (not collected at end)
- ✨ `StepEmbeddedSolutionFormatter` class for step-level formula processing
- ✨ `SolutionRenderer` class for HTML/JSON output
- 🎨 Support for 4 visual themes: light, dark, sepia, chalk
- 📊 Support for multiple DPI settings (150, 300, 600)
- 🔍 Auto LaTeX extraction from problem text and solution steps
- 🎯 Responsive HTML design with professional styling

### Changed
- 📦 Updated dependencies: added matplotlib >= 3.5.0, Pillow >= 9.0.0
- 🔄 Improved solution output format with embedded formulas
- 📈 Enhanced formula image quality with configurable DPI

### Technical Details
- Formula images embed as base64 in HTML
- No external formula image files needed
- Responsive HTML design with CSS styling
- Support for complex mathematical expressions
- Automatic formula positioning within solution steps

### Bug Fixes
- Fixed LaTeX escape sequence handling
- Improved formula extraction from mixed text

## [1.0.0] - 2026-03-20

### Added
- Initial release of Math-Solver Skill
- 📸 OCR recognition with PaddleOCR Doc Parsing Skill
- 🎓 Mathematical problem classification (domain and difficulty detection)
- 💡 Multi-mode solution generation (socratic, detailed, quick)
- 📚 Problem domain and difficulty detection
- 🔧 Skill configuration with multiple parameters
- 📋 Complete documentation and examples

### Features
- Supports various mathematical problem types
- Customizable solution modes
- Integration with OpenClaw framework
- Extensible architecture for future enhancements

---

## Version Comparison

| Feature | v1.0.0 | v1.1.0 |
|---------|--------|--------|
| LaTeX Rendering | ❌ | ✅ |
| Formula Embedding | ❌ | ✅ |
| HTML Output | ❌ | ✅ |
| Visual Themes | ❌ | ✅ (4 themes) |
| Step Integration | ❌ | ✅ |

---

## Installation

```bash
# Register from GitHub
openclaw skill register https://github.com/yshajoy-star/math-solver

# Or register locally
cd /path/to/math-solver
openclaw skill register ./
```

## Usage

See [README.md](./README.md) for detailed usage instructions.

## Contributing

Contributions are welcome! Please follow the [GitHub Flow](https://guides.github.com/introduction/flow/).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
