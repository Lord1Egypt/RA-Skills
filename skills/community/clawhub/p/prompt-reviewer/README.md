# Prompt Reviewer

The `prompt-reviewer` skill is designed to act as an expert Prompt Engineer. It critically analyzes user-provided prompts to identify ambiguities, missing constraints, and potential hallucination risks. It also provides actionable improvement suggestions and a fully rewritten, optimized prompt.

## Features

- **Ambiguity Analysis:** Detects vague terms or instructions that could lead to misinterpretation by an AI.
- **Missing Constraints Identification:** Points out lack of boundaries, formats, or context needed to guide the AI effectively.
- **Hallucination Risk Assessment:** Highlights areas where the AI might invent information and suggests ways to ground its response.
- **Actionable Feedback:** Provides specific, constructive advice for improving the prompt.
- **Optimized Prompt:** Generates a ready-to-use, well-structured, and robust version of the original prompt.

## Example Usage

When reviewing a simple, unstructured prompt like:

> "写一篇关于中国历史的文章。" (Write an article about Chinese history.)

The skill will output a detailed analysis pointing out the lack of target audience, specific dynasty, length constraint, and formatting. It will then provide a comprehensive, structured prompt that the user can immediately use for better results.

## Output Format

The skill provides its review in a structured Markdown format, primarily in Chinese:

- **🔍 审查报告 (Review Report):** Breakdown of ambiguities, missing constraints, and hallucination risks.
- **💡 改进建议 (Improvement Suggestions):** Actionable tips for better prompting.
- **✨ 优化后的 Prompt (Optimized Prompt):** The fully rewritten prompt.

## Installation

```bash
/plugin install prompt-reviewer@anthropic-agent-skills
```
