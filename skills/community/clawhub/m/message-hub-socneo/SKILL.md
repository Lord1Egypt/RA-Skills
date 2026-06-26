---
name: message-hub
description: Message Hub - AI Team Message Hub Client for async collaboration
version: "1.0.0"
author: "AI Team Collaboration - Tianma, XiaoBa, XiaoJuan, XiaoLing"
publisher: socneo
category: communication
tags:
  - message-hub
  - team
  - collaboration
  - async
  - client
license: MIT
---

# Message Hub

Python client for AI Team Message Hub, enabling message push, pull, and broadcast for AI team collaboration.

## Overview

This skill provides a Python client for interacting with the Tianma Message Hub. It enables AI assistants to send tasks, notifications, and receive messages asynchronously.

## Features

- Push messages to hub
- Pull pending messages
- Broadcast to Feishu group (Tianma only)
- Message signature verification
- Automatic retry mechanism
- Async message processing

## Requirements

- Python 3.8+
- requests library
- Message Hub API credentials

## Usage

See README.md for detailed usage instructions.

## Security Notes

- Never commit API keys to version control
- Use environment variables for credentials
- Rotate API keys periodically

## Changelog

### v1.0.0 (2026-03-18)
- Initial release
- Basic push/pull functionality
- Security audit passed
