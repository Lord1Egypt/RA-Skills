# CyberPPT Multi-Platform Compatibility Documentation

[简体中文](PLATFORM_COMPATIBILITY.md) | [English](PLATFORM_COMPATIBILITY.en.md)

## Overview

Starting from version 1.0.0, CyberPPT supports multiple AI Agent platforms. This document details the architecture design, configuration methods, and usage guidelines for multi-platform support.

## Supported Platforms

### Fully Supported Platforms

| Platform | Config File | Installation Path | Verification Status |
|---|---|---|---|
| **OpenCode** | `agents/opencode.yaml` | `~/.opencode/skills/cyber-ppt` | ✅ Verified |
| **OpenAI Codex** | `agents/openai.yaml` | `~/.codex/skills/cyber-ppt` | ✅ Verified |
| **Hermes** | `agents/hermes.yaml` | `~/.hermes/skills/cyber-ppt` | ✅ Supported |
| **OpenClaw** | `agents/openclaw.yaml` | `~/.openclaw/skills/cyber-ppt` | ✅ Supported |
| **Anthropic/Claude** | `agents/anthropic.yaml` | `~/.anthropic/skills/cyber-ppt` | ✅ Supported |

### Generic Support

- **Generic Platform** - `agents/generic.yaml` - Suitable for any AI Agent platform that supports skill mechanisms

## Architecture Design

### Platform-Agnostic Layer

CyberPPT's core functionality is completely platform-agnostic:

```
├── SKILL.md                    # Core skill logic (platform-agnostic)
├── scripts/                    # Python scripts (platform-agnostic)
│   ├── validate_pptx.py       # PPTX validation script
│   ├── build_visual_qa_gate.py
│   ├── compare_render.py
│   └── ...
├── references/                 # Reference docs (platform-agnostic)
│   ├── source-analysis.md
│   ├── storyline.md
│   ├── visual-system.md
│   ├── ppt-production.md
│   └── quality-assurance.md
└── assets/                     # Asset files (platform-agnostic)
    ├── palette-samples/
    └── ...
```

### Platform Adaptation Layer

Platform-specific configurations are in the `agents/` directory:

```
agents/
├── opencode.yaml              # OpenCode platform config
├── openai.yaml                # OpenAI Codex config
├── hermes.yaml                # Hermes config
├── openclaw.yaml              # OpenClaw config
├── anthropic.yaml             # Anthropic/Claude config
└── generic.yaml               # Generic platform template
```

## Configuration File Structure

### YAML Configuration Format

Each platform's configuration file follows a unified structure:

```yaml
interface:
  display_name: "CyberPPT"
  short_description: "Generate evidence-based, editable consulting-style PPTs"
  default_prompt: "Use $cyber-ppt to turn my source documents into high-density, editable consulting-style PPTs."
  skill_type: "presentation_generation"
  version: "1.0.0"
  
compatibility:
  platforms:
    - [platform-name]
  min_version: "1.0.0"
  
configuration:
  trigger_patterns:
    - "create PPT"
    - "generate presentation"
    - "make slides"
    - "CyberPPT"
    - "consulting-style PPT"
    
  file_types:
    - ".docx"
    - ".pdf"
    - ".txt"
    - ".xlsx"
    
  output_format: ".pptx"
  
  workflow:
    stages:
      - name: "analysis"
        description: "Material analysis and evidence chain construction"
        required: true
      - name: "blueprint"
        description: "Style selection and blueprint generation"
        required: true
      - name: "reconstruction"
        description: "PPT reconstruction and quality assurance"
        required: true
        
  quality_gates:
    - reference_gate
    - evidence_gate
    - storyline_gate
    - density_gate
    - style_gate
    - blueprint_gate
    - asset_admission_gate
    - editable_layer_gate
    - visual_semantics_gate
    - curve_trace_gate
    - spatial_registration_gate
    - container_overflow_gate
    - typography_gate
    - render_qa_gate
    - strict_qa_gate
```

### Configuration Field Descriptions

#### interface Section

| Field | Type | Description | Required |
|---|---|---|---|
| `display_name` | string | Skill display name | ✅ Required |
| `short_description` | string | Brief description | ✅ Required |
| `default_prompt` | string | Default prompt | ✅ Required |
| `skill_type` | string | Skill type identifier | ✅ Required |
| `version` | string | Version number (semantic versioning) | ✅ Required |

#### compatibility Section

| Field | Type | Description | Required |
|---|---|---|---|
| `platforms` | array | List of supported platforms | ✅ Required |
| `min_version` | string | Minimum compatible version | ✅ Required |

#### configuration Section

| Field | Type | Description | Required |
|---|---|---|---|
| `trigger_patterns` | array | List of trigger keywords | ✅ Required |
| `file_types` | array | Supported input file types | ✅ Required |
| `output_format` | string | Output file format | ✅ Required |
| `workflow` | object | Workflow definition | ✅ Required |
| `quality_gates` | array | Quality gates list | ✅ Required |

## Installation Guide

### Automatic Installation

#### OpenCode

```powershell
# Windows
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.opencode\skills\cyber-ppt"

# macOS/Linux
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.opencode/skills/cyber-ppt"
```

#### OpenAI Codex

```powershell
# Windows
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.codex\skills\cyber-ppt"

# macOS/Linux
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.codex/skills/cyber-ppt"
```

#### Hermes

```powershell
# Windows
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.hermes\skills\cyber-ppt"

# macOS/Linux
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.hermes/skills/cyber-ppt"
```

#### OpenClaw

```powershell
# Windows
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.openclaw\skills\cyber-ppt"

# macOS/Linux
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.openclaw/skills/cyber-ppt"
```

#### Anthropic/Claude

```powershell
# Windows
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.anthropic\skills\cyber-ppt"

# macOS/Linux
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$HOME/.anthropic/skills/cyber-ppt"
```

### Manual Installation

1. Download the project:
   ```bash
   # Using git
   git clone https://github.com/crazyykhllc-bit/CyberPPT.git
   
   # Or download ZIP
   curl -L https://github.com/crazyykhllc-bit/CyberPPT/archive/refs/heads/main.zip -o CyberPPT.zip
   ```

2. Copy to platform directory:
   - Rename project folder to `cyber-ppt`
   - Copy to your platform's skills directory
   - Ensure `SKILL.md` is in the root directory

3. Verify installation:
   ```
   Chat with Agent: Use CyberPPT skill
   ```

## Usage Guide

### Trigger Methods

On all platforms, you can trigger CyberPPT using:

#### Keyword Triggers

- "create PPT"
- "generate presentation"
- "make slides"
- "CyberPPT"
- "consulting-style PPT"

#### Explicit Invocation

```
Use CyberPPT skill to turn this document into a PPT
```

```
Use $cyber-ppt to generate a consulting-style presentation
```

### Workflow

Regardless of platform, CyberPPT follows the same three-stage process:

#### Stage 1: Material Analysis

```
Input: Upload documents (DOCX/PDF/TXT/XLSX)
Output: MBB evidence table, storyline, page-by-page outline
Confirmation: User approves page count, structure, density
```

#### Stage 2: Blueprint Generation

```
Input: User selects visual style (one of 8)
Output: Page-by-page ImageGen blueprints
Confirmation: User approves all page blueprints
```

#### Stage 3: PPT Reconstruction

```
Input: Approved blueprints
Output: Editable PPTX + QA reports
Confirmation: User approves final PPT
```

### Quality Assurance

All platforms share the same quality gate system:

| Gate | What It Checks | If It Fails |
|---|---|---|
| Reference Gate | Stage reference file completeness | Stage cannot start |
| Evidence Gate | Evidence chain traceability | Mark gaps or rework |
| Storyline Gate | Storyline brainstorming and convergence | Cannot enter blueprint stage |
| Density Gate | Page information density | Add content or rearrange |
| Style Gate | Visual style confirmation | Cannot enter blueprint stage |
| Blueprint Gate | Blueprint completeness | Cannot enter reconstruction stage |
| Asset Admission Gate | Image asset necessity | Rebuild natively |
| Editable Layer Gate | Information layer editability | Rework reconstruction |
| Visual Semantics Gate | Visual semantics fidelity | Visual QA failure |
| Curve Trace Gate | Precise curve tracing | Use path/custom geometry |
| Spatial Registration Gate | Spatial anchor alignment | Rework adjustment |
| Container Overflow Gate | Container boundary check | Rework adjustment |
| Typography Gate | Font size hierarchy compliance | Rework adjustment |
| Render QA Gate | Render comparison check | Continue iteration |
| Strict QA Gate | Structured validation | Errors require rework |

## Platform-Specific Features

### OpenCode Features

- ✅ Native YAML configuration support
- ✅ Auto-loads `agents/opencode.yaml`
- ✅ Supports all 16 quality gates
- ✅ Supports ImageGen blueprint generation
- ✅ Supports visual QA inspection

### OpenAI Codex Features

- ✅ Native platform (first supported)
- ✅ Complete feature support
- ✅ Best compatibility guarantee

### Hermes Features

- ✅ Fully compatible
- ✅ Unified workflow
- ✅ Unified quality standards

### OpenClaw Features

- ✅ Fully compatible
- ✅ Unified workflow
- ✅ Unified quality standards

### Anthropic/Claude Features

- ✅ Fully compatible
- ✅ Optimized for long context
- ✅ Supports Claude-specific features

## Adding New Platform Support

### Step 1: Create Configuration File

```bash
cd agents/
cp generic.yaml [new-platform].yaml
```

### Step 2: Edit Configuration

Edit `[new-platform].yaml`:

```yaml
compatibility:
  platforms:
    - [new-platform-name]
```

Adjust `configuration` section according to platform characteristics.

### Step 3: Test and Verify

1. Install to the new platform's skills directory
2. Test with trigger keywords
3. Execute the complete three-stage workflow
4. Verify quality gates work properly

### Step 4: Submit Contribution

To contribute new platform support back to the main repository:

1. Fork the project
2. Create a feature branch
3. Add configuration file and documentation updates
4. Submit a Pull Request

## Troubleshooting

### Common Issues

#### Issue: Agent Cannot Recognize CyberPPT

**Possible Causes:**
- Incorrect installation path
- Wrong folder name
- Missing `SKILL.md` file

**Solutions:**
1. Check if installation path meets platform requirements
2. Confirm folder is named `cyber-ppt`
3. Verify `SKILL.md` exists in root directory
4. Restart Agent or reload skills

#### Issue: Quality Gates Not Working

**Possible Causes:**
- Missing configuration file
- Configuration format error
- Incomplete `quality_gates` list

**Solutions:**
1. Check if `agents/[platform].yaml` exists
2. Verify YAML format is correct
3. Confirm `quality_gates` contains all 16 gates

#### Issue: Output PPTX Format Errors

**Possible Causes:**
- Python environment not installed
- Missing dependencies
- Script execution permission issues

**Solutions:**
1. Confirm Python 3.7+ is installed
2. Install dependencies: `pip install python-pptx pillow`
3. Check `scripts/validate_pptx.py` execution permission

#### Issue: Inconsistent Features Across Platforms

**Possible Causes:**
- Configuration file differences
- Platform-specific limitations

**Solutions:**
1. Compare configurations under `agents/` for different platforms
2. Check platform official documentation for limitations
3. Adjust configuration to adapt to platform characteristics

## Updates and Maintenance

### Updating the Skill

```bash
cd [your-installation-directory]/cyber-ppt
git pull
```

### Version Compatibility

CyberPPT uses Semantic Versioning:

- **Major version**: Incompatible API changes
- **Minor version**: Backward-compatible feature additions
- **Patch version**: Backward-compatible bug fixes

### Migration Guide

When upgrading major versions, please check `CHANGELOG.md` for changes and migration steps.

## Best Practices

### Platform Selection Recommendations

| Use Case | Recommended Platform | Reason |
|---|---|---|
| Daily Use | OpenCode | Best verified support |
| Long Document Processing | Anthropic/Claude | Ultra-long context support |
| Enterprise Environment | OpenAI Codex | Native support, most stable |
| Experimental Features | Hermes/OpenClaw | Flexible configuration |

### Cross-Platform Collaboration

1. **Unified Evidence Source**: All platforms use the same source materials
2. **Shared Blueprints**: Generated blueprints can be shared across platforms
3. **Standardized QA**: Use unified QA inspection scripts
4. **Version Control**: Use Git to manage work outputs

### Performance Optimization

- Use SSD for skills directory storage
- Keep Python environment clean
- Regularly clean cache files
- Use virtual environment to isolate dependencies

## Technical Support

### Getting Help

- **Documentation**: Check the `docs/` directory of this project
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

### Reporting Issues

When submitting an Issue, please include:

1. Platform and version used
2. Complete error messages
3. Steps to reproduce
4. Relevant configuration file content

### Contributing Code

Contributions of new platform support, bug fixes, and feature improvements are welcome. Please follow:

1. Fork the project
2. Create a feature branch
3. Follow code standards
4. Write test cases
5. Submit a Pull Request

## License

MIT License. See [LICENSE](LICENSE) for details.

---

**Version**: v1.0.0  
**Last Updated**: 2026-07-23  
**Maintainer**: CyberPPT Team
