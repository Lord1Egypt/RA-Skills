# md-wechat

A tool for converting Markdown documents to WeChat Official Account format. Supports custom themes, fonts, colors, code highlighting, and more. The generated HTML can be directly copied and pasted into the WeChat Official Account editor.

## Features

- Full support for Markdown basic syntax and GFM extensions
- Math formula rendering (KaTeX)
- Mermaid diagram rendering
- Mac-style code blocks (red/yellow/green decorative buttons)
- Code syntax highlighting (highlight.js)
- Extended syntax support: strikethrough, highlight, underline, Ruby annotations
- Extract configuration from styled documents for style reuse
- Automatic detection and installation of missing dependencies

## Quick Start

### Requirements

- Node.js >= 18.0.0

### Installation

```bash
git clone https://github.com/italks/md-wechat.git
cd md-wechat
npm install
```

### Basic Usage

```bash
# Convert Markdown file
node scripts/convert.js your-article.md
```

After conversion, a `your-article-wechat.html` file will be generated in the same directory.

## Main Workflow

### 1. Direct Markdown to WeChat Format Conversion

**On first use**, if no configuration file exists, a default configuration file `md-config.json` will be automatically generated:

```bash
node scripts/convert.js article.md
```

Output:
- `article-wechat.html` - Styled HTML file
- `md-config.json` - Default configuration file (if not exists)

### 2. Extract Custom Configuration

Extract style configuration from a styled HTML file:

```bash
node scripts/extract-config.js article-wechat.html -o my-style.json
```

Extractable style parameters:

| Parameter | Description |
|-----|------|
| Primary Color | Color for links, headings, etc. |
| Font Family | Article body font |
| Font Size | Body font size |
| Code Block Theme | highlight.js theme name |
| Mac-style Code Block | Enable red/yellow/green button decoration |
| Background/Text Color | Article background and text colors |
| Line Height | Text line height |

### 3. Use Custom Configuration for Styling

Use the extracted configuration file for styling:

```bash
# Use configuration file
node scripts/convert.js new-article.md -c my-style.json

# Override configuration with command line arguments
node scripts/convert.js new-article.md -c my-style.json --color "#009874"
```

## Configuration File

Configuration file `md-config.json` structure:

```json
{
  "version": "1.0.0",
  "theme": {
    "name": "default"
  },
  "style": {
    "fontFamily": "-apple-system-font, BlinkMacSystemFont, Helvetica Neue, PingFang SC, sans-serif",
    "fontSize": "16px",
    "primaryColor": "#0F4C81",
    "textColor": "#3f3f3f",
    "bgColor": "#ffffff",
    "lineHeight": 1.75
  },
  "codeBlock": {
    "themeName": "atom-one-dark",
    "isMacStyle": true
  },
  "content": {
    "countStatus": true,
    "useIndent": false,
    "useJustify": false,
    "padding": "20px"
  }
}
```

## Command Line Interface

### convert.js - Markdown Conversion

```bash
node scripts/convert.js <input> [options]

Arguments:
  input                  Input Markdown file path

Options:
  -o, --output <path>    Output HTML file path
  -c, --config <path>    Configuration file path (default: md-config.json)
  --color <color>        Primary color (override config file)
  --font <font>          Font family (override config file)
  --font-size <size>     Font size (override config file)
  --bg-color <color>     Background color (override config file)
  --text-color <color>   Text color (override config file)
  --no-auto-install      Disable automatic dependency installation
```

### extract-config.js - Configuration Extraction

```bash
node scripts/extract-config.js <input> [options]

Arguments:
  input                  Rendered HTML file path

Options:
  -o, --output <path>    Output configuration file path
  -m, --markdown <path>  Corresponding Markdown file (enhanced analysis)
  --name <name>          Configuration name (default: extracted)
```

## Feature Support

| Feature | Support |
|---------|:--------:|
| Basic Markdown | ✅ |
| GFM Extensions (tables, task lists, etc.) | ✅ |
| Code Syntax Highlighting | ✅ |
| Mac-style Code Blocks | ✅ |
| Math Formulas (KaTeX) | ✅ |
| Mermaid Diagrams | ✅ |
| Strikethrough/Highlight/Underline | ✅ |
| Ruby Annotations | ✅ |
| Inline Styles | ✅ |
| Configuration Extraction & Reuse | ✅ |

## Comparison with doocs/md

This project is inspired by [doocs/md](https://github.com/doocs/md). Here's a feature comparison:

| Feature | doocs/md | md-wechat |
|---------|:--------:|:---------:|
| **Runtime Environment** | Browser/Online | Node.js CLI |
| **Usage** | Online Editor | CLI Batch Processing |
| Basic Markdown | ✅ | ✅ |
| GFM Extensions | ✅ | ✅ |
| Code Syntax Highlighting | ✅ | ✅ |
| Mac-style Code Blocks | ✅ | ✅ |
| Math Formulas (LaTeX) | ✅ | ✅ KaTeX |
| Mermaid Diagrams | ✅ | ✅ |
| PlantUML Diagrams | ✅ | ⚠️ Partial |
| Infographic Charts | ✅ | ⚠️ Partial |
| Strikethrough/Highlight/Underline | ✅ | ✅ |
| Ruby Annotations | ✅ | ✅ |
| **Configuration Extraction** | ❌ | ✅ |
| **Configuration Reuse** | ❌ | ✅ |
| **Batch Processing** | ❌ | ✅ |
| **CLI Automation** | ❌ | ✅ |
| **Auto Dependency Installation** | ❌ | ✅ |

### Use Cases

**doocs/md is better for:**
- Real-time online editing and preview
- Quick styling of single articles
- Visual operations

**md-wechat is better for:**
- Batch article processing
- Automated workflows
- CI/CD integration
- Style configuration reuse
- Team collaboration on styling

## Project Structure

```
md-wechat/
├── README.md                    # Project documentation (Chinese)
├── README_EN.md                 # Project documentation (English)
├── skill.md                     # Detailed skill documentation
├── package.json                 # Node.js dependency configuration
├── md-config.json               # Default configuration file
├── scripts/
│   ├── convert.js               # Core conversion script
│   └── extract-config.js        # Configuration extraction script
└── example.md                   # Example Markdown file
```

## Using with WeChat Official Account

1. Convert Markdown file using this tool to generate HTML
2. Open the generated HTML file in a browser
3. Select all and copy (Ctrl+A / Cmd+A)
4. Paste into WeChat Official Account editor

## Acknowledgments

This project was inspired by [doocs/md](https://github.com/doocs/md). Thanks to that project for providing excellent ideas and implementation references.

Also thanks to the following open source projects:

- [marked](https://marked.js.org/) - Markdown parser
- [KaTeX](https://katex.org/) - Math formula rendering
- [highlight.js](https://highlightjs.org/) - Code syntax highlighting
- [Mermaid](https://mermaid.js.org/) - Diagram rendering

## License

MIT License
