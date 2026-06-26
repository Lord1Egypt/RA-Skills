---
name: github-to-rednote
description: Convert GitHub repositories into RedNote (小红书) style technical articles. Use when user wants to generate tech promotion content from GitHub repos - including project intros, reviews, tutorials, tool lists, or release notes. Supports 5 article templates with emoji formatting and hashtag tags.
---

# GitHub to RedNote

Convert GitHub repositories into RedNote-style technical articles.

## Overview

This skill transforms GitHub repository information into engaging RedNote (小红书) formatted articles suitable for Chinese tech community promotion.

**Supported Article Types:**
1. **Intro** - Project recommendation/overview
2. **Review** - Technical review and evaluation
3. **Tutorial** - Usage guide and tutorial
4. **List** - Tool collection/list
5. **Release** - Version release notes

## Quick Start

```bash
# Basic usage - generate intro article
python3 scripts/generate_article.py <github-url>

# Specify article type
python3 scripts/generate_article.py <github-url> --type review

# Save to file
python3 scripts/generate_article.py <github-url> --output article.md
```

## Workflow

1. **Parse URL** - Extract owner/repo from GitHub URL
2. **Fetch Data** - Get repo info, README, languages via GitHub API
3. **Generate Content** - Use LLM to create RedNote-style article
4. **Format Output** - Apply emoji formatting and hashtags

## Article Types

### 1. Intro (项目推荐)
Project introduction and recommendation
- Focus: What it does, key features, why use it
- Style: Enthusiastic but technical

### 2. Review (项目测评)
Technical review and evaluation
- Focus: Pros/cons, use cases, comparison
- Style: Objective analysis

### 3. Tutorial (使用教程)
Usage guide
- Focus: Installation, quick start, examples
- Style: Step-by-step instructions

### 4. List (工具合集)
Tool collection
- Focus: Multiple related tools, categorized
- Style: Curated list with brief descriptions

### 5. Release (版本发布)
Version release notes
- Focus: New features, changes, migration
- Style: Changelog format

## Output Format

RedNote style includes:
- Emoji decorations (🔥💡⚡️🚀)
- Section dividers
- Topic hashtags (#技术分享 #开源项目 #程序员)
- Concise paragraphs (适合手机阅读)

## Resources

### scripts/
- `generate_article.py` - Main script for article generation
- `github_api.py` - GitHub API wrapper
- `formatters.py` - RedNote formatting utilities

### references/
- `prompts.md` - LLM prompt templates for each article type
- `rednote-style.md` - RedNote formatting guidelines

### assets/
- Templates and example outputs
