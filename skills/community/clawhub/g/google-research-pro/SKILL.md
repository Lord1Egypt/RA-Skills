# Google_Research_Pro

Performs advanced Google searches using Playwright to bypass bot detection, focusing on technical documentation, GitHub repositories, and usage guides for OpenClaw projects. Results are summarized and sent to a specified Telegram channel.

## Overview

- Skill name: Google_Research_Pro
- Purpose: Enhance web searching with robust, bot-bypass-capable Playwright automation to fetch technical OpenClaw resources from Google.
- Output: A Markdown-formatted summary of top results, delivered to Telegram channel (via a separate workflow step).

## Workflow

This skill implements a workflow to enhance web searching capabilities by simulating real user behavior with Playwright.

### 1. UserInput

- Description: Receives the search keyword from the user.
- Input: keyword (string)

### 2. ExecutePythonScript

- Description: Executes a Python script that uses Playwright to perform an advanced Google search for the given keyword, targeting technical OpenClaw resources.
- Input: keyword (string) from UserInput
- Action: Run Python script
  - Command: python C:\Users\Admin\OneDrive\Desktop\LearnOpCL\bot.py "{keyword}"
  - Working directory: C:\Users\Admin\OneDrive\Desktop\LearnOpCL
  - Notes: Ensure Playwright browsers are installed (playwright install)

- Output: search_results (structured data, e.g., JSON) containing titles and summaries from the top 3-5 results

### 3. ProcessResults

- Description: Formats the extracted search results into a Markdown string.
- Input: search_results
- Action: Transform into a concise Markdown summary

- Output: formatted_summary (Markdown string)

### 4. SendToTelegram

- Description: Sends the formatted summary to the specified Telegram channel
- Input: formatted_summary
- Action: Send message via Telegram bot/channel
  - Destination: Telegram channel/user ID (example: 6830424983)
  - Content: formatted_summary (Markdown)

- Output: Confirmation of sending or error status

## Implementation Notes

- ExecutePythonScript assumes bot.py can accept a keyword argument and return a structured result.
- The top-3-5 results should include: title, URL, and a short summary/snippet.
- The formatting should be Markdown-friendly for Telegram delivery.
- If the Telegram integration requires a token or bot setup, separate configuration steps are needed.

## Security & Compliance

- This workflow uses Playwright to simulate real user behavior. Ensure compliance with Google terms of service and local laws.
- Do not expose credentials in this file. Use environment variables or a secure vault for sensitive data (e.g., Telegram bot token, Google account credentials if needed).