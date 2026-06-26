# Investor Relations Manager Skill

AI-powered Investor Relations Manager for automated video generation of earnings reports, financial updates, and stakeholder communications.

## Description

Transform financial data and business updates into professional video presentations for investors, stakeholders, and the financial community. This skill automates the entire pipeline from data to polished IR videos.

## Features

- 📊 **Professional IR Video Generation** - Earnings reports, quarterly updates, shareholder communications
- 💼 **Financial Metric Detection** - Intelligent recognition of revenue, profit, growth rates, and KPIs
- 🎨 **Corporate Visual Style** - Professional blue/green color scheme suitable for investor presentations
- 🎤 **Professional Business Voice** - Default alloy voice, optimized for professional settings
- 📈 **IR-Optimized Scene Types** - Specialized animations for financial data presentation
- 🔒 **Compliance Awareness** - Built-in warnings for data accuracy and regulatory compliance

## Installation

```bash
clawhub install investor-relations-manager
```

## Quick Start

```bash
# Clone the project
git clone https://github.com/ZhenRobotics/openclaw-investor-relations-manager.git ~/openclaw-investor-relations-manager
cd ~/openclaw-investor-relations-manager

# Install dependencies
npm install

# Configure API key
echo 'OPENAI_API_KEY="sk-your-key-here"' > .env

# Generate your first IR video
./agents/ir-cli.sh generate "Q3 earnings report. Revenue reached 2.3 billion dollars, up 45%. Net profit 35 million dollars, up 60%."
```

## Usage Examples

### Quarterly Earnings Report
```bash
./agents/ir-cli.sh generate "Q3营收增长45%，达到2.3亿美元。净利润提升60%，至3500万美元。用户规模突破500万。"
```

### Annual Shareholder Update
```bash
./scripts/script-to-video.sh scripts/example-annual-report.txt --voice alloy --speed 1.0
```

### Product Launch Announcement
```bash
./agents/ir-cli.sh generate "重磅新品发布。AI驱动的企业解决方案正式上线。预计贡献年收入5000万美元。"
```

## Configuration

### Voice Options
- `alloy` (Recommended) - Neutral, professional
- `echo` - Clear and authoritative
- `onyx` - Deep, executive-style

### Speed
- `1.0` (Recommended) - Professional pace for investor presentations
- `0.9` - Slower, more emphasis
- `1.1` - Slightly faster

## Use Cases

✓ Quarterly earnings reports (Q1, Q2, Q3, Q4)
✓ Annual shareholder meetings
✓ Business milestone communications
✓ Product launch announcements (investor-focused)
✓ Financial guidance updates
✓ M&A announcements

## Video Specifications

- **Resolution**: 1080 x 1920 (Portrait, configurable)
- **Frame Rate**: 30 fps
- **Format**: MP4 (H.264 + AAC)
- **Style**: Professional corporate with financial color scheme
- **Duration**: Auto-calculated (typically 30-90 seconds)

## Cost

Per 60-second IR video: **~$0.012** (about 1 cent)
- OpenAI TTS: ~$0.004
- OpenAI Whisper: ~$0.008
- Remotion rendering: Free (local)

## Documentation

- **Full README**: [GitHub Repository](https://github.com/ZhenRobotics/openclaw-investor-relations-manager)
- **Quick Start Guide**: [QUICKSTART.md](https://github.com/ZhenRobotics/openclaw-investor-relations-manager/blob/main/QUICKSTART.md)
- **Transformation Summary**: [IR_TRANSFORMATION_SUMMARY.md](https://github.com/ZhenRobotics/openclaw-investor-relations-manager/blob/main/IR_TRANSFORMATION_SUMMARY.md)

## Requirements

- Node.js >= 18
- npm or pnpm
- OpenAI API Key (with TTS + Whisper access)

## Important Notes

⚠️ **Data Accuracy**: All financial data must be verified before official release
⚠️ **Compliance**: Ensure content complies with financial disclosure regulations
⚠️ **Legal Review**: Recommend legal review for material investor communications

This tool generates presentation videos only - users are responsible for data accuracy and regulatory compliance.

## Support

- **GitHub Issues**: https://github.com/ZhenRobotics/openclaw-investor-relations-manager/issues
- **Documentation**: https://github.com/ZhenRobotics/openclaw-investor-relations-manager
- **ClawHub Page**: https://clawhub.ai/ZhenStaff/investor-relations-manager

## License

MIT

## Author

@ZhenStaff

## Version

1.0.0 - Initial Release
