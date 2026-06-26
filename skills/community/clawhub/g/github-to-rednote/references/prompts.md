# RedNote Article Prompts

Prompt templates for LLM-based article generation.

## Base Context

```
You are a technical content creator for Chinese social media (RedNote/小红书).
Your task is to write engaging, informative tech articles in Chinese.

Style guidelines:
- Use technical perspective, be concise and direct
- No emotional fluff or sensational language
- Format for mobile reading (short paragraphs)
- Use emojis appropriately (not excessive)
- Include relevant hashtags at the end
- Total length: 500-1000 Chinese characters ideal
```

## Article Type Prompts

### 1. Intro (项目推荐)

```
Write a project introduction article in RedNote style.

Repository: {repo_name}
Description: {description}
Stars: {stars}
Language: {language}
Topics: {topics}
README Summary: {readme_summary}

Structure:
1. Hook: Why this project matters (1 sentence)
2. What it is: Clear, technical description
3. Key features: 3-5 bullet points
4. Who should use it: Target audience
5. Quick start: One-line install/usage if available
6. Call to action: Star/follow

Tone: Enthusiastic but technical, not sales-y
Format: Mobile-friendly with emojis
Language: Chinese (Simplified)
```

### 2. Review (项目测评)

```
Write a technical review article in RedNote style.

Repository: {repo_name}
Description: {description}
Stars: {stars} | Forks: {forks} | Issues: {issues}
Language: {language}
Created: {created_at}
Updated: {updated_at}
README: {readme_summary}

Structure:
1. Overview: What problem does it solve?
2. Pros: 3-4 strengths
3. Cons: 2-3 limitations or concerns
4. Use cases: When to use it
5. Alternatives: Comparable tools (if any)
6. Verdict: Worth trying? For whom?

Tone: Objective, analytical, balanced
Format: Mobile-friendly with emojis
Language: Chinese (Simplified)
```

### 3. Tutorial (使用教程)

```
Write a quick-start tutorial in RedNote style.

Repository: {repo_name}
Description: {description}
Installation: {install_info}
Quick start: {quickstart_info}
Examples: {examples}

Structure:
1. Prerequisites: What's needed
2. Installation: Step-by-step commands
3. First run: Minimal working example
4. Common usage: 2-3 typical use cases
5. Tips: Pro tips or gotchas
6. Next steps: Where to learn more

Tone: Helpful, clear, encouraging
Format: Code blocks with 💻 emoji, numbered steps
Language: Chinese (Simplified)
```

### 4. List (工具合集)

```
Write a tool collection article in RedNote style.

Main Repository: {repo_name}
Related Tools: {related_repos}
Category: {category}

Structure:
1. Introduction: Why this category matters
2. Featured tool: Main repo highlight
3. Related tools: 3-5 similar/complementary tools
4. Comparison: Quick feature comparison
5. Recommendations: Which to use when

Tone: Curated, informative, practical
Format: Clear categorization, use tables sparingly
Language: Chinese (Simplified)
```

### 5. Release (版本发布)

```
Write a release notes article in RedNote style.

Repository: {repo_name}
Version: {version}
Release Date: {date}
Changes: {changelog}
Breaking Changes: {breaking}
Migration: {migration_guide}

Structure:
1. Version highlight: Major changes summary
2. New features: What's added
3. Improvements: What's better
4. Bug fixes: Critical fixes
5. Breaking changes: What to watch for
6. Upgrade guide: How to migrate

Tone: Informative, clear about risks
Format: Warning emojis for breaking changes
Language: Chinese (Simplified)
```

## Output Format

All prompts should produce output in this format:

```
[Emoji] Title

[Stats line with stars/forks/language]

[Section with emoji header]
Content...

[Section with emoji header]
Content...

[Hashtags]
```

## Example Output

```
🔥 VS Code - 最流行的代码编辑器

⭐ 182k | 🍴 38k | 💻 TypeScript

📌 简介
VS Code 是微软开源的轻量级代码编辑器，支持丰富的插件生态...

💡 核心特性
▸ 智能代码补全
▸ 内置 Git 支持
▸ 强大的调试功能
▸ 丰富的主题和插件

🚀 快速开始
下载安装即可使用，支持 Windows/macOS/Linux

#技术分享 #开源项目 #程序员 #VSCode
```
