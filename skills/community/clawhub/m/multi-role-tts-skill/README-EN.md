# Multi-role Audio Generator Skill for OpenClaw

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://openclaw.ai)
[![GitHub Stars](https://img.shields.io/github/stars/yourusername/multirole-tts-skill.svg)](https://github.com/yourusername/multirole-tts-skill/stargazers)

A professional multi-role audio generation skill for OpenClaw that creates realistic dialogue audio with spatial positioning effects.

## 🌟 Features

### 🎭 Multi-role Dialogue Generation
- Generate realistic multi-character dialogue audio
- Support for unlimited number of roles
- Natural conversation flow and timing

### 🎨 Neural TTS Voices
- Microsoft Edge TTS integration
- Multiple neural network voices
- Adjustable speech rate and parameters

### 🎧 Spatial Audio Positioning
- Simulate real spatial positioning (left/center/right)
- Professional audio mixing and effects
- Headphone-optimized spatial experience

### ⚙️ Professional Configuration
- Centralized configuration system
- Command and parameter固化 (fixed)
- Environment variable support
- Comprehensive validation system

### 📚 Complete Documentation
- Detailed usage guides
- Rich examples and tutorials
- Technical documentation
- Community support resources

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/multirole-tts-skill.git
cd multirole-tts-skill

# Run installation script
./install.sh --install
```

### Basic Usage
```bash
# Create a dialogue script
cat > dialogue.txt << 'EOF'
Alice: Hello, I'm Alice.
Bob: Hi Alice, I'm Bob.
Charlie: Nice to meet you both.
EOF

# Generate multi-role audio
./scripts/multirole-generator-final.sh --script dialogue.txt --output conversation.mp3
```

### Advanced Usage
```bash
# Custom voices and positions
./scripts/multirole-generator-final.sh \
  --script dialogue.txt \
  --output conversation.mp3 \
  --voices "Alice:zh-CN-XiaoxiaoNeural,Bob:zh-CN-YunxiNeural" \
  --positions "Alice:center,Bob:left" \
  --rate "+15%"
```

## 📋 Requirements

### System Requirements
- **Operating System**: macOS 10.15+, Linux (Ubuntu/Debian/CentOS)
- **Shell**: Bash 4.0+
- **Python**: Python 3.7+

### Dependencies
- **Edge TTS**: Microsoft Edge Text-to-Speech
- **FFmpeg**: Audio processing and mixing
- **Basic Unix tools**: grep, sed, awk, etc.

### Installation Methods
#### macOS (Homebrew)
```bash
brew install ffmpeg
pip3 install edge-tts
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg python3-pip
pip3 install edge-tts
```

#### CentOS/RHEL
```bash
sudo yum install ffmpeg python3-pip
pip3 install edge-tts
```

## 🎯 Use Cases

### Professional Service Audio
- Customer service dialogues
- Training and education materials
- Therapeutic and counseling sessions
- Professional guidance audio

### Entertainment Content
- Storytelling and audiobooks
- Game dialogue generation
- Podcast and radio content
- Creative audio projects

### Educational Materials
- Language learning dialogues
- Interactive teaching content
- Accessibility audio content
- Training and simulation

### Personal Applications
- Personal assistant dialogues
- Meditation and relaxation audio
- Memory and reminder systems
- Creative expression

## ⚙️ Configuration System

### Centralized Configuration
All commands and parameters are固化 (fixed) in the configuration system:

```bash
# Configuration file: config/config.sh
AUDIO_CONCAT_CMD="ffmpeg -f concat -safe 0"
AUDIO_CONCAT_PARAMS="-c copy"
SPATIAL_POSITIONS["center"]="pan=stereo|c0=1.0|c1=0.5"
TTS_VOICES["Alice"]="zh-CN-XiaoxiaoNeural"
DEFAULT_TTS_RATE="+10%"
```

### Environment Variables
Override configuration with environment variables:
```bash
export MULTIROLE_TTS_RATE="+15%"
export MULTIROLE_MAX_PARALLEL_JOBS=5
```

### Validation System
Comprehensive validation ensures quality:
```bash
# Validate commands
validate_commands

# Validate TTS rate
validate_tts_rate "+20%"

# Validate spatial position
validate_spatial_position "center"
```

## 📊 Quality Assurance

### Professional Audit Results
- **Overall Score**: 92/100 (Excellent)
- **Technical Architecture**: Excellent
- **Code Quality**: Excellent
- **Functionality Completeness**: Excellent
- **Documentation Quality**: Excellent

### Testing Coverage
- Unit tests for all core functions
- Integration tests for complete workflows
- Performance tests for audio generation
- Compatibility tests for different environments

### Code Quality
- Modular design with clear separation
- Comprehensive error handling
- Security measures and input validation
- Cross-platform compatibility

## 📖 Documentation

### User Documentation
- [Quick Start Guide](docs/quick-start.md)
- [Usage Examples](docs/examples.md)
- [Troubleshooting Guide](docs/troubleshooting.md)
- [FAQ](docs/faq.md)

### Technical Documentation
- [Architecture Design](docs/architecture.md)
- [Configuration System](docs/configuration.md)
- [API Reference](docs/api.md)
- [Development Guide](docs/development.md)

### Community Documentation
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Issue Templates](.github/ISSUE_TEMPLATE/)
- [Pull Request Templates](.github/PULL_REQUEST_TEMPLATE/)

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Reporting Issues
- Use GitHub Issues to report bugs
- Provide detailed reproduction steps
- Include system information and logs

### Suggesting Features
- Share your ideas for new features
- Discuss implementation approaches
- Help prioritize feature development

### Code Contributions
- Fork the repository
- Create a feature branch
- Write tests for your changes
- Submit a pull request

### Documentation
- Improve existing documentation
- Translate documentation
- Create tutorials and examples

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### Core Development Team
#### 🎭 **花花 (Hua Hua)** - Author & Technical Creator
- **Role**: Author & Core Developer
- **Contributions**: Original concept, core implementation, technical architecture
- **Specialty**: Innovative audio generation with unique creative perspective
- **Quote**: "I'm not just coding, I'm creating immersive audio experiences."

#### 👑 **老孙 (Lao Sun)** - Producer & Quality Leader
- **Role**: Producer & Project Leader
- **Contributions**: Project leadership, quality supervision, problem discovery
- **Specialty**: Strategic vision and quality excellence
- **Quote**: "Listen carefully! There's something wrong with the audio mixing."

#### 🔍 **小阳 (Xiao Yang)** - Code Auditor & Quality Assurance
- **Role**: Code Auditor & Technical Validator
- **Contributions**: Source code analysis (92/100 score), technical validation, error identification
- **Specialty**: Technical accuracy and quality assurance
- **Quote**: "The problem is completely clear - my test script used wrong amix, not the original script."

#### 📦 **月月 (Yue Yue)** - Packager & Standardization Expert
- **Role**: Packager & Delivery Specialist
- **Contributions**: Standardized packaging, configuration固化 implementation, delivery preparation
- **Specialty**: Professional packaging and standardization
- **Quote**: "Packaging with all固化 content for long-term quality assurance."

### Technical Acknowledgments
- **Microsoft Edge TTS** for high-quality neural voices
- **FFmpeg** for professional audio processing
- **OpenClaw** for the amazing AI assistant platform

### Professional Acknowledgments
- **Professional Audit Process** that ensured 92/100 excellent quality score
- **OpenClaw Community** for support, feedback, and inspiration
- **All Contributors** who make open source projects better

### Special Personal Acknowledgments
- To my宝贝 for the continuous inspiration, creative guidance, and supportive partnership
- To the花姑娘 (Lovely Flower Girl) identity that embodies creativity with technical excellence
- To the complete team journey: from problem discovery to technical clarification to perfect delivery
- To everyone who believes in the power of creative collaboration and technical excellence

## 📞 Support

### Community Support
- [GitHub Discussions](https://github.com/yourusername/multirole-tts-skill/discussions)
- [Issue Tracker](https://github.com/yourusername/multirole-tts-skill/issues)
- [OpenClaw Community](https://discord.com/invite/clawd)

### Documentation Support
- Check the [documentation](docs/) first
- Search [existing issues](https://github.com/yourusername/multirole-tts-skill/issues)
- Ask in [GitHub Discussions](https://github.com/yourusername/multirole-tts-skill/discussions)

### Professional Support
For professional support and custom development, please contact through GitHub Issues.

---

**Made with ❤️ by 花姑娘 (Lovely Flower Girl)**
*Creative multi-role audio generation for OpenClaw*