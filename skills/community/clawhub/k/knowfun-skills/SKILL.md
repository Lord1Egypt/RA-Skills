---
name: knowfun
description: Generate educational content using Knowfun.io API - create courses, posters, games, and films with AI. Use when user wants to generate educational content, visual materials, or interactive experiences.
argument-hint: "<command> [args]"
disable-model-invocation: false
user-invocable: true
allowed-tools: "Bash(curl *), Read, Write"
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "bins": ["knowfun"], "env": ["KNOWFUN_API_KEY"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": ".",
              "bins": ["knowfun"],
              "label": "Build knowfun skills (npm)",
            },
          ],
      },
  }
---

# Knowfun.io API Skill

This skill helps you interact with the Knowfun.io OpenAPI to generate educational content, posters, games, and films.

## Prerequisites

Before using this skill, you need:
1. A Knowfun.io API Key (get it from https://www.knowfun.io/api-platform)
2. Sufficient credits in your account

## Configuration

Set your API key as an environment variable:
```bash
export KNOWFUN_API_KEY="kf_your_api_key_here"
```

Or the skill will prompt you for it when needed.

## Available Commands

When invoked, this skill supports the following operations:

### 1. Create a Task

Generate content by creating a task. Supports four types: `course`, `poster`, `game`, `film`.

**Basic Example:**
```bash
/knowfun create course "Introduction to Machine Learning"
/knowfun create poster "Climate Change Facts"
/knowfun create game "Learn Python Basics"
/knowfun create film "History of the Internet"
```

**With URL:**
```bash
/knowfun create course https://example.com/document.pdf
```

### 2. Check Task Status

Check the status of a task by its ID:
```bash
/knowfun status <taskId>
```

### 3. Get Task Details

Get detailed information about a completed task:
```bash
/knowfun detail <taskId>
```

### 4. List Tasks

List recent tasks:
```bash
/knowfun list
```

### 5. Check Credits

Check your credit balance:
```bash
/knowfun credits
```

### 6. Get Schema

Get available configuration options for each task type:
```bash
/knowfun schema
```

## Task Configuration

Each task type has specific configuration options. See [api-reference.md](api-reference.md) for complete details.

### Course Configuration
- **contentStyle**: detailed, concise, conversational
- **contentLanguage**: zh, en, etc.
- **explainLanguage**: zh, en, etc.
- **voiceType**: standard voice options
- **ttsStyle**: classroom, professional, etc.

### Poster Configuration
- **usage**: infographic (default), businessReports, marketing, illustration
- **style**: handDrawn (default), photorealistic, anime, sciFi, custom
- **aspectRatio**: 1:1, 16:9, 9:16, etc.
- **posterTitle**: Custom title for the poster

### Game Configuration
- **gameType**: story, interactive (default), explore, mission, roleplay, simulation, puzzle, arcade, card, word, timeline, custom
- **customPrompt**: Custom game description

### Film Configuration
- **filmStyle**: narration (default), story, documentary, tutorial, concept_explainer, case_study, animation, cinematic, promotional, custom
- **aspectRatio**: 16:9 (default), 9:16, 1:1
- **visualStyle**: Custom visual style description

## How This Skill Works

1. **Extract API Key**: First checks if KNOWFUN_API_KEY environment variable is set
2. **Parse Command**: Interprets the command (create, status, list, credits, schema)
3. **Make API Request**: Uses curl to interact with the Knowfun.io API
4. **Format Response**: Presents results in a readable format
5. **Handle Errors**: Provides helpful error messages and troubleshooting tips

## API Endpoints

The skill uses the following base URL:
- Production: `https://api.knowfun.io`

## Examples

See [examples.md](examples.md) for comprehensive usage examples.

## Error Handling

Common errors and solutions:

- **401 Unauthorized**: Check your API key is correct and not expired
- **402 Insufficient Credits**: Top up your account at https://knowfun.io
- **429 Rate Limit**: Wait a moment and try again
- **400 Bad Request**: Check your input parameters

## Reference Documentation

For complete API documentation, see [api-reference.md](api-reference.md).

## Implementation Details

When this skill is invoked, Claude will:

1. Verify the API key is available
2. Parse the command and arguments from `$ARGUMENTS`
3. Construct appropriate curl commands to call the Knowfun.io API
4. Handle authentication headers
5. Parse JSON responses
6. Format results for display
7. Provide actionable next steps

The skill uses `curl` for API requests and `jq` for JSON parsing when available.
