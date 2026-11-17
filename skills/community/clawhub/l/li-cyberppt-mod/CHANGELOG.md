# Changelog

All notable changes to CyberPPT will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-23

### Added - Multi-Platform Support 🎉

This is a major release that transforms CyberPPT from a single-platform skill to a **multi-platform compatible AI Agent Skill**.

#### New Platform Support

- **OpenCode** - Full support with optimized configuration (`agents/opencode.yaml`)
  - Interactive skill execution mode
  - Auto-save and progress tracking
  - Custom tool integration
  - Recommended models: GPT-4-turbo, GPT-4, Claude-3-opus
  
- **Hermes** - Native workflow engine support (`agents/hermes.yaml`)
  - Native workflow engine integration
  - Task orchestration with checkpoint support
  - Exponential backoff retry policy
  - Priority queue for task management
  
- **OpenClaw** - Tool chain and pipeline support (`agents/openclaw.yaml`)
  - Tool chain support for complex workflows
  - Pipeline execution mode
  - Plugin system for extensions
  - Modular design with extension points
  
- **Anthropic/Claude** - Extended context optimization (`agents/anthropic.yaml`)
  - Extended context support (up to 200K tokens)
  - Artifact support for large documents
  - Semantic chunk strategy
  - Hierarchical processing for long documents
  - Recommended models: Claude-3-opus, Claude-3-sonnet, Claude-3-haiku
  
- **Generic Platform** - Universal compatibility template (`agents/generic.yaml`)
  - Universal compatibility mode
  - Minimal platform requirements
  - Customizable workflow and gates
  - Platform abstraction layer

#### Platform-Specific Optimizations

Each platform now has tailored configurations:

- **OpenCode**: Streaming output, custom tool integration, debug mode
- **OpenAI Codex**: Code Interpreter integration, DALL-E support, 512MB file upload
- **Hermes**: Event-driven architecture, resource pooling, concurrent task management
- **OpenClaw**: Modular design, custom validators, extension points
- **Anthropic/Claude**: Long document optimization, semantic chunking, artifact support

#### Multi-Language Trigger Support

Added English trigger patterns to all platform configurations:
- "create PPT"
- "generate presentation"
- "make slides"

#### Documentation

- **PLATFORM_COMPATIBILITY.md** - Comprehensive multi-platform compatibility guide (Chinese)
- **PLATFORM_COMPATIBILITY.en.md** - English version of compatibility guide
- Updated **SKILL.md** with YAML front matter compatibility declarations
- Updated **README.md** with multi-platform installation and usage instructions
- Updated **README.en.md** with English multi-platform documentation

#### Configuration Architecture

- Unified YAML configuration format across all platforms
- Platform-agnostic core layer (SKILL.md, scripts/, references/, assets/)
- Platform-specific adaptation layer (agents/*.yaml)
- 16 quality gates enforced consistently across all platforms

### Changed

- **Breaking**: `agents/openai.yaml` extended from 4 lines to full configuration format
- All platform configs now include `platform_specific` and `advanced_features` sections
- Enhanced trigger patterns with multi-language support
- Improved configuration structure with semantic grouping

### Technical Details

#### File Structure

```
agents/
├── opencode.yaml      # 79 lines - OpenCode optimized
├── openai.yaml        # 68 lines - OpenAI Codex native
├── hermes.yaml        # 67 lines - Hermes workflow engine
├── openclaw.yaml      # 62 lines - OpenClaw tool chain
├── anthropic.yaml     # 66 lines - Claude long context
└── generic.yaml       # 61 lines - Universal template
```

#### Configuration Schema

All configurations follow this structure:
```yaml
interface:           # Skill metadata
compatibility:       # Platform compatibility
configuration:       # Core settings
  trigger_patterns:  # Multi-language triggers
  file_types:        # Supported inputs
  workflow:          # Three-stage process
  quality_gates:     # 16 quality gates
  platform_specific: # Platform optimizations
  advanced_features: # Advanced capabilities
```

### Migration Guide

#### From Single-Platform to Multi-Platform

If you were using CyberPPT on OpenAI Codex only:

1. **No Breaking Changes** - Existing usage remains compatible
2. **Optional Upgrade** - Can now migrate to other platforms
3. **Enhanced Features** - New platform-specific optimizations available

#### Installing on Different Platforms

```bash
# OpenCode
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.opencode/skills/cyber-ppt"

# Hermes
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.hermes/skills/cyber-ppt"

# OpenClaw
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.openclaw/skills/cyber-ppt"

# Anthropic/Claude
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.anthropic/skills/cyber-ppt"
```

### Platform Comparison

| Feature | OpenCode | Codex | Hermes | OpenClaw | Anthropic |
|---------|----------|-------|--------|----------|-----------|
| Interactive Mode | ✅ | ✅ | ✅ | ✅ | ✅ |
| Extended Context | ✅ 128K | ❌ | ❌ | ❌ | ✅ 200K |
| Code Interpreter | ❌ | ✅ | ❌ | ❌ | ✅ |
| DALL-E Integration | ❌ | ✅ | ❌ | ❌ | ❌ |
| Plugin System | ✅ | ❌ | ❌ | ✅ | ❌ |
| Streaming Output | ✅ | ✅ | ✅ | ✅ | ✅ |
| Progress Tracking | ✅ | ❌ | ✅ | ❌ | ❌ |

### Known Issues

- None at this time

### Future Roadmap

- [ ] Add more language support for trigger patterns (Japanese, Korean, etc.)
- [ ] Implement cross-platform workflow synchronization
- [ ] Add automated platform compatibility testing
- [ ] Create platform-specific performance benchmarks
- [ ] Develop platform migration tools

---

## [0.9.0] - 2026-07-22 (Pre-Release)

### Added

- Initial multi-platform architecture design
- Generic platform configuration template
- Platform compatibility documentation draft

### Note

This was an internal development version, not publicly released.

---

## [0.1.0] - Initial Release

### Added

- Core CyberPPT functionality for OpenAI Codex
- Three-stage workflow: Analysis → Blueprint → Reconstruction
- 16 quality gates system
- 8 visual styles
- Evidence chain extraction from source materials
- ImageGen blueprint generation
- Editable PPTX reconstruction
- Visual QA system
- Python validation scripts

---

For more details on each release, see the [GitHub Releases](https://github.com/crazyykhllc-bit/CyberPPT/releases) page.
