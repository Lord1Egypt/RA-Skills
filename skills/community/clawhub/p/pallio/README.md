# Pallio AI — OpenClaw Skill

Chat with AI personas powered by curated knowledge bases. Pallio personas use RAG (Retrieval-Augmented Generation) to answer questions from uploaded documents with citations.

## Setup

1. Set your persona ID:
   ```
   export PALLIO_PERSONA_ID=your_persona_id_here
   ```

2. Find public persona IDs at [pallioai.com/community](https://pallioai.com/community)

## What It Does

- Initializes a chat session with a Pallio AI persona
- Sends questions and receives RAG-powered answers with document citations
- Maintains conversation context across messages

## Limitations

- **3 free messages per session** — after that, a signup prompt is shown
- **Widget-grade responses** — uses a lightweight pipeline (dense search only, 300 token max, flash-lite model)
- **Rate limited** — 30 session inits/hour, 10 messages/hour per IP

## Full API Access

For unlimited messages, hybrid search, full-length responses, and programmatic access:

1. Sign up at [pallioai.com](https://pallioai.com)
2. Subscribe to Professional tier or higher
3. Generate an API key in Settings → Developer API
4. Install the [Pallio MCP Server](https://www.npmjs.com/package/@pallio/mcp-server) for full tool integration

## Links

- [Pallio AI](https://pallioai.com)
- [Community Personas](https://pallioai.com/community)
- [API Documentation](https://pallioai.com/api-docs)
