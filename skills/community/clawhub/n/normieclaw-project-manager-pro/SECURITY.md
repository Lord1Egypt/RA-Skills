# Project Manager Pro — Security Considerations

## Data Storage

Project Manager Pro stores tasks and project data as JSON files in your OpenClaw workspace directory (`~/.openclaw/workspace/pm-pro/`). This is local file storage on whatever machine runs your OpenClaw agent.

**No data is sent to NormieClaw servers.** The tool operates entirely through your agent's existing infrastructure.

However, be aware:

- **Your AI agent processes task data.** Task content is sent to your configured LLM provider (Anthropic, OpenAI, etc.) as part of normal agent conversations. This is inherent to how AI agents work — the agent needs to read your tasks to manage them.
- **Cross-tool tasks include context.** If you enable cross-tool integration, task notes may contain information from other tools (expense amounts, meal plans, workout details). This data flows through the same LLM provider.
- **Export files are unencrypted.** Markdown, CSV, and JSON exports are plain text files. Handle them according to your own security practices.
- **No encryption at rest.** Task JSON files are stored as plain text. If your machine's disk is not encrypted, your task data is not encrypted.

## What We Don't Control

- **Your LLM provider's data policies.** How your AI provider (Anthropic, OpenAI, Google, etc.) handles the conversation data that includes your tasks is governed by their terms of service, not ours.
- **Your machine's security posture.** Disk encryption, access controls, backup security, and network security are your responsibility.
- **Your OpenClaw configuration.** How your agent is configured, which channels it operates on, and who has access to those channels affects who can see your task data.

## Recommendations

1. **Use disk encryption** on the machine running your OpenClaw agent (FileVault on macOS, LUKS on Linux, BitLocker on Windows).
2. **Review your LLM provider's data policy** if your tasks contain sensitive information.
3. **Be mindful of channel visibility.** If your agent operates in shared channels (Discord servers, group chats), task responses will be visible to other participants.
4. **Secure exported files.** If you export tasks to CSV/markdown, store or transmit those files with appropriate care.
5. **Back up your data.** The `pm-pro/` directory contains all your task data. Include it in your backup strategy.

## No Telemetry

Project Manager Pro does not phone home, collect analytics, or transmit usage data. The scripts and skill file operate entirely within your local environment and agent context.

## Reporting Issues

If you discover a security concern with Project Manager Pro, contact us at [normieclaw.ai](https://normieclaw.ai).
