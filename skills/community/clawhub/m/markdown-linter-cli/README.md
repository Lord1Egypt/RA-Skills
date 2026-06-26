# Markdown Linter

A CLI tool to lint Markdown files for formatting issues, broken links, and style consistency.

## Quick Start

```bash
# Lint a single file
./scripts/main.py run --input README.md

# Lint multiple files
./scripts/main.py run --input "docs/*.md"
```

## Installation

This skill is installed via OpenClaw. Once installed, you can use it directly from your OpenClaw agent.

## Features

- **Header hierarchy validation**
- **Image alt text checking**
- **Internal link validation**
- **Line length checking**
- **Trailing whitespace detection**
- **List consistency checking**
- **Code block language recommendation**
- **Empty link detection**
- **Duplicate header warnings**
- **External link checking** (optional)

## Configuration

Customize linting behavior with command-line options:

- `--max-line-length`: Set maximum line length (default: 80)
- `--check-external-links`: Enable external URL validation
- `--ignore-rules`: Comma-separated list of rule IDs to ignore

## Output

The tool outputs JSON with detailed issue reports, including line numbers, severity levels, and suggested fixes.

## Contributing

Issues and pull requests welcome. See the source code in `scripts/main.py`.

## License

MIT