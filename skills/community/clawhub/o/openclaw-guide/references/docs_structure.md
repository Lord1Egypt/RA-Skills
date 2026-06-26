# OpenClaw Documentation Structure

## Official Documentation Site
- **URL**: https://docs.openclaw.ai
- **Source**: Generated from `/docs` directory in the main repository
- **Primary Authority**: This is the definitive source for all OpenClaw capabilities, configuration, and usage

## Key Documentation Sections

### 1. Getting Started
- Installation guides
- Basic setup and configuration
- First-time user walkthrough

### 2. Core Concepts
- Agent architecture
- Skills system
- Memory and workspace management
- Gateway and node concepts

### 3. Configuration
- `openclaw.config.json` structure
- Channel configuration (Telegram, Discord, etc.)
- Security and permissions
- Model and runtime settings

### 4. Skills Reference
- Built-in skills documentation
- Skill creation guide
- Skill sharing and distribution

### 5. CLI Reference
- All `openclaw` subcommands
- Gateway management
- Agent control commands
- Utility commands

### 6. API and Integration
- WebSocket Gateway API
- REST endpoints
- Third-party integrations

### 7. Troubleshooting
- Common issues and solutions
- Debugging techniques
- Performance optimization

## Source Code Repository Structure

### Main Repository: https://github.com/openclaw/openclaw

#### Key Directories:
- `/docs` - Source for official documentation
- `/packages` - Core packages and modules
- `/scripts` - Development and utility scripts  
- `/examples` - Usage examples and templates
- `/test` - Test suites and fixtures

#### Important Files:
- `package.json` - Dependencies and scripts
- `README.md` - Project overview
- `CONTRIBUTING.md` - Contribution guidelines
- `LICENSE` - License information

## Search Strategy Guidelines

When answering questions about OpenClaw:

1. **Always prioritize official documentation** over any other source
2. **Cross-reference with source code** when documentation is unclear or missing
3. **Check recent commits/issues** for breaking changes or new features
4. **Verify information currency** - OpenClaw evolves rapidly
5. **Provide specific references** to documentation sections or source files

## Common Query Patterns

### Configuration Questions
- Search: `configuration`, `settings`, `openclaw.config.json`
- Check: `/docs/configuration.md`, repository issues tagged "config"

### Capability Questions  
- Search: specific feature names, skill names
- Check: `/docs/skills/`, `/docs/capabilities/`

### Troubleshooting Questions
- Search: error messages, symptoms
- Check: `/docs/troubleshooting.md`, recent GitHub issues

### API/Integration Questions
- Search: `API`, `WebSocket`, `REST`, integration names
- Check: `/docs/api/`, `/packages/gateway/`

This reference file should be loaded when detailed documentation structure knowledge is needed for comprehensive answers.