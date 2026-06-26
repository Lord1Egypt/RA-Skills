---
name: lifequery
description: "Query your Telegram chat history using a LifeQuery instance. Use when the user wants to search past conversations, find shared links, or ask about specific people/events from their Telegram messages."
---

# LifeQuery Telegram History Skill

Query your Telegram chat history using a [LifeQuery](https://github.com/nikira-studio/lifequery) instance.

## When to Use

Use when the user wants to:
- Search past Telegram conversations
- Find shared links, photos, or files
- Ask about specific people, events, or topics from their Telegram messages
- Retrieve context from old chats

## Configuration

Set these environment variables:

- `LIFEQUERY_BASE_URL`: Base URL of your LifeQuery instance (e.g., `http://localhost:3134/v1` or `http://your-server:80/v1`)
- `LIFEQUERY_API_KEY`: Optional API key if protected

## How it Works

The skill runs a Python script that sends search queries to the LifeQuery `/chat/completions` endpoint and returns semantically relevant answers with citations from the chat history.
