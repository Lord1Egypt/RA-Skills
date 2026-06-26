---
name: github-code-analyzer
description: Clone and analyze GitHub project code quality using DeepSeek AI
---
# GitHub Code Analyzer

A skill for analyzing GitHub repository code quality, bugs, and security issues using DeepSeek AI.

## Features

- Clone any public GitHub repository
- Analyze project structure
- Identify code bugs and security vulnerabilities
- Provide improvement suggestions
- Support multiple AI models

## Usage

```
analyze https://github.com/owner/repo
analyze https://github.com/owner/repo --model deepseek
```

## Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| repo | string | GitHub repository URL | required |
| model | string | AI model to use (deepseek, deepseek-coder) | deepseek |

## Examples

```bash
# Analyze a repository
analyze https://github.com/Openwrt-Passwall/openwrt-passwall

# Use specific model
analyze https://github.com/facebook/react --model deepseek-coder
```

## Supported Models

- `deepseek` - General purpose analysis
- `deepseek-coder` - Optimized for code analysis

## Output

The analyzer provides:
1. Project structure overview
2. Code quality assessment
3. Bug and security issue identification
4. Improvement suggestions

## Technical Details

- Uses git clone with --depth 1 for fast cloning
- Samples code files from multiple languages
- Integrates with DeepSeek API for AI analysis
- Falls back to structure-only analysis if API fails

## License

MIT
