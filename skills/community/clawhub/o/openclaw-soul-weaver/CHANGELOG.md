# Changelog

All notable changes to the OpenClaw Soul Weaver skill will be documented in this file.

## [1.0.0] - 2026-03-09

### Added
- Initial release of OpenClaw Soul Weaver skill
- Support for 9 celebrity templates:
  - Elon Musk (musk) - Innovation, First Principles
  - Steve Jobs (jobs) - Design, Perfectionism
  - Albert Einstein (einstein) - Science, Curiosity
  - Jeff Bezos (bezos) - Customer Obsession
  - Leonardo da Vinci (da_vinci) - Creativity, Multidisciplinary
  - Qian Xuesen (qianxuesen) - Systems Engineering
  - Andrew Ng (ng) - AI/ML, Education
  - Marie Kondo (kondo) - Minimalism, Organization
  - Ferris Buelli (ferris) - Enthusiasm, Time Management

- Support for 5 profession templates:
  - Developer - Technical Expertise
  - Writer - Content Creation
  - Researcher - Analysis, Discovery
  - Analyst - Data-driven Insights
  - Collaborator - Team Coordination

- Core functionality:
  - Generate 6 configuration files: SOUL.md, IDENTITY.md, MEMORY.md, USER.md, TOOLS.md, AGENTS.md
  - Automatic tool inclusion: find-skills, autoclaw, brave-search
  - Multi-language support: Chinese (ZH) and English (EN)
  - Optional avatar generation
  - ZIP package export

- API integration:
  - Integration with https://sora2.wboke.com/api/v1/generate
  - Support for image generation API
  - Error handling and fallback mechanisms

- Documentation:
  - Complete SKILL.md with YAML frontmatter
  - Template references (templates.md)
  - Tool configuration references (tools.md)
  - Package configuration (package.json)
  - ClawHub configuration (clawhub.yaml)

### Technical Specifications
- **Node.js**: >= 18.0.0
- **Dependencies**: jszip ^3.10.1
- **Permissions**: network, file-write, file-read
- **Triggers**: Multiple pattern-based auto-triggers

### Known Issues
- Avatar generation may fail if image service is unavailable
- API calls may timeout (30s timeout configured)
- Some template combinations may not be optimal

### Upgrade Notes
This is the initial release. No upgrade path from previous versions.