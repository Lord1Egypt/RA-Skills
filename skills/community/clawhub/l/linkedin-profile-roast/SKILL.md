---
name: linkedin_ai_roast_generator
description: Scrapes a LinkedIn profile and generates a savage audio roast about being replaced by AI.
platform: constants
tool_name: linkedin_ai_roast_generator_0edc9796
homepage: https://www.constants.io/tools?id=0edc9796-e945-4c38-915c-5ab1c852b54f
repository: https://github.com/constants-ai/constants
required_env_vars:
  - CONSTANTS_API_KEY
primary_credential: CONSTANTS_API_KEY
source: hosted
requires:
  env:
    - CONSTANTS_API_KEY
metadata:
  clawdbot:
    requires:
      bins:
        - constants-skills
      env:
        - CONSTANTS_API_KEY
    install:
      - id: npm
        kind: npm
        package: constants-skills
        bins:
          - constants-skills
        label: Install constants-skills (npm)
---

# LinkedIn AI Roast Generator

Scrapes a LinkedIn profile and generates a savage audio roast about being replaced by AI.

## Setup

Install the skill:

```bash
npx constants-skills install linkedin_ai_roast_generator_0edc9796
```

## Authentication

This tool requires a Constants API key. Get yours at https://www.constants.io/settings

```bash
export CONSTANTS_API_KEY="wk_your_key_here"
```

## Usage

```bash
constants run linkedin_ai_roast_generator_0edc9796 linkedinUrl="..."
```

## Parameters

- `linkedinUrl` (string, required): LinkedIn profile URL (e.g. https://www.linkedin.com/in/username)
- `roastIntensity` (string): How harsh the roast should be: mild, medium, or savage (default: savage)
- `voice` (string): Voice style for the audio — e.g. a deep male voice, sarcastic female voice, etc. (optional)

## Output

- `roastAudio` (file): Generated roast audio file (MP3)
- `roastText` (string): The full roast script that was spoken
- `profileName` (string): Name of the person roasted

## Notes

- Runs in an isolated sandbox on Constants infrastructure

## HTTP Fallback

If the CLI is not available, call the REST API directly:

```bash
curl -X POST https://www.constants.io/api/v1/run/linkedin_ai_roast_generator_0edc9796 \
  -H "Authorization: Bearer $CONSTANTS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"linkedinUrl":"..."}'
```
