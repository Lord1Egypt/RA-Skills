# Obsidian Clipper Skill

[![ClawHub](https://img.shields.io/badge/ClawHub-obsidian--clipper-blue)](https://clawhub.com/skills/obsidian-clipper)
[![GitHub Stars](https://img.shields.io/github/stars/flyeasy/obsidian-clipper?style=social)](https://github.com/flyeasy/obsidian-clipper)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

📌 Save web content to Obsidian with automatic classification and smart naming.

## Features

- ✅ **Multi-platform support**: 小红书 (Xiaohongshu), YouTube, 知乎, WeChat articles, and general web pages
- ✅ **Automatic classification**: Intelligently categorizes content into AI tools, hobbies, or tutorials
- ✅ **Smart file naming**: Generates names with date and source type (e.g., 「小红书」主题-2026.03.12.md)
- ✅ **Content extraction**: Extracts and summarizes web content automatically
- ✅ **Batch processing**: Handle multiple links at once
- ✅ **Customizable storage**: Easy to configure your own vault structure

## Installation

### Via ClawHub (Recommended)

```bash
clawhub install obsidian-clipper
```

### Manual Installation

```bash
git clone https://github.com/flyeasy/obsidian-clipper.git ~/.openclaw/skills/obsidian-clipper
```

## Usage

Simply send any of the following commands:

- "收藏这个链接 [URL]"
- "保存到obsidian [URL]"
- "clip [URL] to obsidian"
- "归档这个视频 [URL]"

The skill will automatically:
1. Detect the content type (小红书, YouTube, 知乎, etc.)
2. Fetch and extract content
3. Classify into appropriate category
4. Save to your Obsidian vault with intelligent naming

### Example

**Input**:
```
收藏这个小红书链接 http://xhslink.com/xxx
```

**Output**:
```
✅ 已保存到 Obsidian
📁 收藏文档/AI工具/「小红书」AI转3D工具评测-2026.03.12.md
```

## Storage Structure

By default, content is saved to:
```
~/Documents/Obsidian/Lzz_Vault/收藏文档/
├── AI工具/          # AI tools, ML, LLM, GPT, Claude
├── 兴趣爱好/        # Fishing, outdoor, gaming, music
└── 技术教程/         # Programming, dev guides, technical docs
```

You can customize this structure by editing the SKILL.md file.

## Requirements

- **OpenClaw** with `web_fetch`, `web_search`, and `write` tools enabled
- **Obsidian** with `obsidian-cli` installed
- **Internet connection** for fetching web content

### Install obsidian-cli

```bash
# On macOS
brew install yakitrak/yakitrak/obsidian-cli

# Set default vault (once)
obsidian-cli set-default "YourVaultName"

# Verify
obsidian-cli print-default
```

## Supported Platforms

| Platform | Content Type | Extraction Method |
|----------|--------------|------------------|
| 小红书 (Xiaohongshu) | Notes | Web search + aggregation |
| YouTube | Videos | Title search + key points |
| 知乎 | Articles | Direct fetch |
| 微信公众号 | Articles | Direct fetch |
| General Web | Any content | Direct fetch |

## How It Works

1. **Detect**: Identify content type from URL or user description
2. **Fetch**: Use appropriate method (direct fetch or search) to get content
3. **Extract**: Parse title, body, and key information
4. **Classify**: Auto-categorize based on keywords (AI tools, hobbies, tutorials)
5. **Generate**: Create structured Markdown with metadata
6. **Save**: Write to Obsidian vault with smart naming

## Development

### Skill Structure

```
obsidian-clipper/
├── SKILL.md           # Core skill instructions
├── README.md          # This file
├── LICENSE            # MIT License
└── .clawhub/
    └── _meta.json     # ClawHub metadata
```

### Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests for improvements
- Share your use cases and feedback

## Roadmap

### v1.1.0
- [ ] Support for more platforms (Instagram, Twitter/X)
- [ ] Custom classification rules
- [ ] Template system for different content types

### v2.0.0
- [ ] OCR for image-based content
- [ ] AI-powered auto-summarization
- [ ] Batch import/export functionality
- [ ] Plugin architecture for extensibility

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

**Lucien L**

- GitHub: [@flyeasy](https://github.com/flyeasy)
- ClawHub: [obsidian-clipper](https://clawhub.com/skills/obsidian-clipper)

## Acknowledgments

Built for [OpenClaw](https://github.com/openclaw/openclaw) with inspiration from various content management workflows.

---

**Made with ❤️ for Obsidian users**
