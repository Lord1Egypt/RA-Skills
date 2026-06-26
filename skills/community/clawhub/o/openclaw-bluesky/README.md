# OpenClaw-Bluesky

An advanced, security-conscious AT Protocol (Bluesky) orchestration skill designed to enable authenticated, thread-aware interaction with the Bluesky Social network.

## Purpose
This skill provides a standardized way for autonomous agents and tools operating within the OpenClaw environment to interact with the Bluesky social graph. It is designed for:
- **Responsive Automation**: Thread-aware posting, replying, and quoting.
- **Engagement**: Structured likes and reposts.
- **Content Management**: Blob-based media uploads and private content bookmarking.

## Transparency & Security
- **Authentication**: This skill requires an **App Password**. You should never use your primary account password.
- **Data Integrity**: Uses `TextEncoder` to ensure byte-perfect rich-text facets, preventing rendering failures common in naive UTF-16 implementations.
- **Scope**: Designed specifically for AT Protocol write/read operations. It does not scrape unrelated files or system internals.
- **Provisioning**: Requires explicit environment variable configuration to function, ensuring secrets are handled via your secure environment configuration, not hardcoded.

## Getting Started
See the [SKILL.md](./SKILL.md) for full configuration instructions, capability details, and authentication steps.

## Provenance
Developed as part of the OpenClaw AgentSkills initiative. For questions or audit concerns, reach out via [Bluesky](https://bsky.app/profile/jenniferstrategist.bsky.social).
