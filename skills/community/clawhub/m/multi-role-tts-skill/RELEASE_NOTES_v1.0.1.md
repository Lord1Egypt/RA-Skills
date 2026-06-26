# Multi-role TTS Skill v1.0.1 - Complete Bundle Edition

## 🎉 Release Highlights

### 🚀 Major Update: From Specific to Universal
We've completely transformed this skill from a specific-purpose tool into a **universal, professional multi-role audio generator**. All hardcoded inappropriate content has been thoroughly removed, making this a clean, neutral, and professional tool for everyone.

### 🔧 Core Improvements

#### 1. **Complete Neutralization**
- **Removed all hardcoded explicit content filenames** - No more inappropriate references
- **Cleaned up all example content** - Now provides purely professional dialogue examples
- **Universal role recognition** - Supports any character names, not specific ones

#### 2. **Enhanced Command-line Interface**
- **Full argument support** - Customize input/output files, voices, rates
- **Improved error handling** - Better user feedback and debugging support
- **Flexible configuration** - Adjust all parameters via command line

#### 3. **Professional Toolchain**
- **Complete installation script** - One-command setup with dependency checking
- **Comprehensive documentation** - Detailed guides and examples
- **Testing suite** - Built-in validation and testing tools

### 📦 What's in the Complete Bundle?

#### 🎯 Core Components
- `generate-audio.py` - Main Python script (completely rewritten)
- `install.sh` - Automated installation script
- `package.json` - Updated to v1.0.1 with complete bundle metadata

#### 📚 Documentation Suite
- `README.md` / `README-EN.md` - Bilingual documentation
- `SKILL.md` - OpenClaw skill specification
- `CHANGELOG.md` - Complete version history
- `usage-instructions.txt` - Quick start guide
- `docs/` - Detailed technical documentation

#### 🎭 Example Resources
- `examples/basic-dialogue.txt` - Basic conversation template
- `examples/neutral-dialogue.txt` - English dialogue example
- `examples/service-dialogue.txt` - Professional scenario example

#### 🛠️ Development Tools
- `scripts/` - Utility scripts for advanced usage
- `tests/` - Testing and validation tools
- `venv/` - Python virtual environment with all dependencies

### 🚀 Quick Start

#### Installation
```bash
# One-command installation
./install.sh --install

# Check dependencies
./install.sh --check

# Test installation
./install.sh --test
```

#### Basic Usage
```bash
# Generate audio from default example
python generate-audio.py

# Use custom script
python generate-audio.py -i my_script.txt -o my_audio.mp3

# Customize voices
python generate-audio.py --role-a-voice zh-CN-XiaoxiaoNeural --role-b-voice zh-CN-XiaoyiNeural
```

#### Script Format
```
# Comment lines are ignored
CharacterA: Hello, I am Character A
CharacterB: I am Character B, nice to meet you
Narrator: Conversation begins

CharacterA: The weather is nice today
CharacterB: Yes, perfect for going out
Narrator: Conversation ends
```

### 🔧 Technical Details

#### System Requirements
- **Python 3.x** - Runtime environment
- **edge-tts** >= 6.1.0 - Microsoft Edge TTS service
- **ffmpeg** - Audio processing tool

#### Supported Role Identifiers
- English: `CharacterA:`, `RoleB:`, `Narrator:`
- Chinese: `角色A:`, `角色B:`, `旁白:`
- Legacy support: `花花:`, `小霞:`, `观察者:` (for backward compatibility)

#### Audio Features
- **Multi-role dialogue generation** - Natural conversation flow
- **Neural TTS voices** - High-quality Microsoft Edge TTS
- **Audio merging** - Professional ffmpeg-based concatenation
- **Rate adjustment** - Customizable speech speed

### 🎯 Why This Update Matters

#### For Existing Users
- **Smooth upgrade path** - Backward compatibility maintained
- **Better performance** - Improved error handling and feedback
- **More flexibility** - Customizable via command-line arguments

#### For New Users
- **Clean start** - No inappropriate content
- **Professional tool** - Ready for serious projects
- **Complete package** - Everything needed in one bundle

#### For Developers
- **Clean codebase** - Well-structured and documented
- **Extensible design** - Easy to modify and extend
- **Testing framework** - Built-in validation tools

### 📝 Changelog Summary

#### v1.0.1 Complete Bundle Edition (2026-03-26)
- ✅ **Complete neutralization** - Removed all hardcoded explicit content
- ✅ **Universal tool transformation** - From specific to general purpose
- ✅ **Enhanced CLI interface** - Full argument support and error handling
- ✅ **Complete bundle packaging** - All tools and documentation included
- ✅ **Professional examples** - Clean, neutral dialogue templates
- ✅ **Improved documentation** - Bilingual guides and technical docs

#### v1.0.0 (Initial Release)
- Initial multi-role audio generator skill
- Edge TTS integration with spatial audio effects
- Basic configuration management system

### 🔮 Future Roadmap

#### Planned Improvements
- **Web interface** - GUI for non-technical users
- **More TTS engines** - Support for additional voice services
- **Advanced audio effects** - More spatial positioning options
- **Batch processing** - Handle multiple scripts at once

#### Community Contributions
- We welcome bug reports, feature requests, and pull requests
- See `CONTRIBUTING.md` for guidelines
- Join our community for support and collaboration

### 📞 Support & Resources

#### Documentation
- Complete usage guide: `docs/usage-guide.md`
- Technical specifications: `SKILL.md`
- Quick start: `usage-instructions.txt`

#### Community
- GitHub repository: [yourusername/multirole-tts-skill](https://github.com/yourusername/multirole-tts-skill)
- Issue tracker: For bug reports and feature requests
- Discussions: Community support and ideas

#### License
- MIT License - Free for personal and commercial use

---

**Thank you for choosing Multi-role TTS Skill v1.0.1 Complete Bundle Edition!** 🎉

We're committed to providing professional, reliable tools for audio generation. Your feedback helps us improve - please share your experience and suggestions with our community.

*Happy audio generating!* 🎧✨