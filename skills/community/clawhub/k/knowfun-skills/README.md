# Knowfun Skills - Multi-Platform AI Integration

English | [简体中文](README_CN.md)

Multi-platform AI coding assistant integration for Knowfun.io API. Generate educational content, posters, games, and films using Claude Code, Cursor, Cline, or OpenClaw.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Claude%20Code%20%7C%20Cursor%20%7C%20Cline%20%7C%20OpenClaw-orange.svg)](PLATFORM_COMPARISON.md)
[![npm](https://img.shields.io/badge/npm-knowfun--skills-red.svg)](https://www.npmjs.com/package/knowfun-skills)
[![ClawHub](https://img.shields.io/badge/ClawHub-knowfun--skills-blue.svg)](https://clawhub.ai/duguyixiaono1/knowfun-skills)
[![Security: Verified](https://img.shields.io/badge/Security-Verified-success.svg)](SECURITY.md)
[![Code Safety](https://img.shields.io/badge/Code%20Safety-Transparent-brightgreen.svg)](CLAWHUB_VERIFICATION.md)

## What is Knowfun.io?

Knowfun.io is an AI-powered platform that transforms text and documents into engaging educational content:
- 📚 **Courses**: Interactive presentations with narration
- 🎨 **Posters**: Visual infographics and marketing materials
- 🎮 **Games**: Interactive learning experiences
- 🎬 **Films**: Educational videos and documentaries

## Security & Compliance

This is an **official, verified integration** for the Knowfun.io API:

- ✅ **Fully Open Source** - MIT licensed, all code is transparent
- ✅ **No Arbitrary Code Execution** - Scripts are hardcoded, not user-controlled
- ✅ **Official API Only** - Only calls https://api.knowfun.io endpoints
- ✅ **Industry Standard Security** - API keys via environment variables
- ✅ **No Sensitive Data Exposure** - Credentials never logged or exposed

**Note for Security Scanners**: Automated tools may flag bash script usage. This is a false positive - see [SECURITY.md](SECURITY.md) for detailed security analysis and [CLAWHUB_VERIFICATION.md](CLAWHUB_VERIFICATION.md) for verification steps.

## Features

### Platform Support
- 🎯 **Claude Code** - Native `/knowfun` skill commands
- 🎯 **Cursor** - CLI tool + rules integration
- 🎯 **Cline** - CLI tool + JSON config
- 🎯 **OpenClaw** - CLI tool + skill definition

### Capabilities
- ✅ Create content generation tasks via natural language
- ✅ Monitor task status and progress
- ✅ Retrieve generated content
- ✅ Manage credits and API usage
- ✅ Get configuration options and schemas
- ✅ Multi-language support (English + 简体中文)

## Quick Start

Choose your platform:

- **Claude Code**: See [Claude Code Installation](INSTALLATION.md#claude-code-installation)
- **Cursor**: See [Cursor Installation](INSTALLATION.md#cursor-installation)
- **Cline**: See [Cline Installation](INSTALLATION.md#cline-installation)
- **OpenClaw**: See [OpenClaw Installation](integrations/openclaw/README.md)

Or follow the [5-Minute Quickstart Guide](QUICKSTART.md)

## Setup

1. **Get an API Key**
   - Visit https://www.knowfun.io/api-platform
   - Click "Create API Key"
   - Copy the key (starts with `kf_`)

2. **Configure Environment**
   ```bash
   # Temporary (current session)
   export KNOWFUN_API_KEY="kf_your_api_key_here"

   # Permanent (add to shell profile)
   echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc
   source ~/.zshrc
   ```

## Usage

### Claude Code

```bash
# Use native slash commands
/knowfun create course "Introduction to Python"
/knowfun create poster "Climate Change Facts"
/knowfun status <taskId>
/knowfun credits
```

### Cursor / Cline / OpenClaw

```bash
# Use CLI tool directly
knowfun create course "Introduction to Python"
knowfun create poster "Climate Change Facts"
knowfun status <taskId>
knowfun credits

# Or ask your AI assistant
"Use knowfun to create a course about Python"
```

### All Commands

- `create <type> <content>` - Generate content (course/poster/game/film)
- `status <taskId>` - Check task status
- `detail <taskId>` - Get detailed results
- `list [limit]` - List recent tasks
- `credits` - Check credit balance
- `schema` - Get configuration options

### Examples

#### Example 1: Create a Course from Text

```bash
/knowfun create course "Machine Learning Basics: ML is a subset of AI that enables computers to learn from data without explicit programming."
```

#### Example 2: Create a Course from URL

```bash
/knowfun create course https://example.com/document.pdf
```

#### Example 3: Check Status and Get Results

```bash
# Create task and note the task ID
/knowfun create course "Introduction to Quantum Computing"

# Wait a few minutes, then check status
/knowfun status c3199fb3-350b-4981-858d-09b949bfae88

# Get detailed results when completed
/knowfun detail c3199fb3-350b-4981-858d-09b949bfae88
```

## Documentation

- **[SKILL.md](SKILL.md)**: Main skill instructions and configuration
- **[api-reference.md](api-reference.md)**: Complete API documentation
- **[examples.md](examples.md)**: Comprehensive usage examples

## Configuration Options

### Course Generation
- Content style: detailed, concise, conversational
- Languages: en, zh, and more
- Voice types and TTS styles
- Custom requirements

### Poster Generation
- Usage types: infographic, businessReports, marketing, illustration
- Styles: handDrawn, photorealistic, anime, sciFi, custom
- Aspect ratios: 1:1, 16:9, 9:16, 4:3, 3:4

### Game Generation
- Game types: story, interactive, explore, mission, roleplay, simulation, puzzle, arcade, card, word, timeline, custom
- Custom prompts
- Image uploads

### Film Generation
- Film styles: story, documentary, tutorial, concept_explainer, narration, case_study, animation, cinematic, promotional, custom
- Aspect ratios: 16:9, 9:16, 1:1
- Custom visual styles

## API Endpoints

- **Base URL**: `https://api.knowfun.io`
- **Create Task**: `POST /api/openapi/v1/tasks`
- **Get Status**: `GET /api/openapi/v1/tasks/:taskId`
- **Get Details**: `GET /api/openapi/v1/tasks/:taskId/detail`
- **List Tasks**: `GET /api/openapi/v1/tasks`
- **Credits Balance**: `GET /api/openapi/v1/credits/balance`
- **Credits Pricing**: `GET /api/openapi/v1/credits/pricing`
- **Usage Stats**: `GET /api/openapi/usage`
- **Schema**: `GET /api/openapi/v1/schema`

## Credit System

Each task type costs credits:
- **Course**: 100 credits (default)
- **Poster**: 100 credits (default)
- **Game**: 100 credits (default)
- **Film**: 100 credits (default)

Check your balance: `/knowfun credits` or `knowfun credits`

**Get more credits**: Visit https://www.knowfun.io/api-platform to manage your account

## Rate Limits

- Default: 60 requests/minute
- Default: 1000 requests/day
- Configurable per API key

## Error Handling

Common errors and solutions:

| Error Code | Status | Solution |
|------------|--------|----------|
| INVALID_API_KEY | 401 | Check your API key |
| API_KEY_EXPIRED | 401 | Regenerate API key |
| INSUFFICIENT_CREDITS | 402 | Top up credits |
| RATE_LIMIT_EXCEEDED | 429 | Wait and retry |
| TASK_TYPE_NOT_ALLOWED | 403 | Check API key permissions |

## Advanced Usage

### Using Callbacks

For long-running tasks, set up a callback URL:

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "unique-id",
    "taskType": "course",
    "material": {"text": "Content here"},
    "callbackUrl": "https://your-server.com/callback"
  }'
```

### Batch Processing

Process multiple items:

```bash
# Create a list of tasks
for topic in "Python" "JavaScript" "CSS"; do
  /knowfun create course "Learn $topic Basics"
  sleep 2
done
```

### Using with curl

For advanced configurations, use curl directly:

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "course-001",
    "taskType": "course",
    "material": {
      "text": "Your content here",
      "type": "text"
    },
    "config": {
      "course": {
        "contentStyle": "detailed",
        "contentLanguage": "en",
        "explainLanguage": "en"
      }
    }
  }'
```

## Troubleshooting

### API Key Not Found

```bash
# Check if set
echo $KNOWFUN_API_KEY

# Set temporarily
export KNOWFUN_API_KEY="kf_your_key"

# Or set permanently
echo 'export KNOWFUN_API_KEY="kf_your_key"' >> ~/.zshrc
```

### Task Taking Too Long

- Course generation: typically 2-5 minutes
- Poster generation: typically 1-3 minutes
- Game generation: typically 3-7 minutes
- Film generation: typically 5-10 minutes

If a task is stuck for >15 minutes, contact support.

### Credit Issues

```bash
# Check balance
/knowfun credits

# Check pricing
curl -s https://api.knowfun.io/api/openapi/v1/credits/pricing \
  -H "Authorization: Bearer $KNOWFUN_API_KEY"
```

## Support

- **Web Portal**: https://www.knowfun.io
- **API Platform**: https://www.knowfun.io/api-platform
- **Documentation**: See [api-reference.md](api-reference.md)
- **Examples**: See [examples.md](examples.md)
- **Issues**: Report bugs and request features on [GitHub Issues](../../issues)

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) before submitting pull requests.

- 🐛 [Report bugs](../../issues/new?template=bug_report.md)
- 💡 [Request features](../../issues/new?template=feature_request.md)
- 📝 [Improve documentation](CONTRIBUTING.md#documentation-contributions)
- 🔧 [Submit code](CONTRIBUTING.md#code-contributions)

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to abide by its terms.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Knowfun.io

## Version

- **Version**: 1.0.13
- **Last Updated**: 2026-03-09
- **Compatible with**: Claude Code, Cursor, Cline, OpenClaw

---

