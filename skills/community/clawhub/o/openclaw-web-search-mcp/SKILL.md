# Web Search and Research MCP

This MCP provides comprehensive web browsing, search, and research capabilities for AI agents, including PDF extraction, YouTube transcripts, summarization, and semantic search.

## Overview

This MCP implements a full suite of tools for AI agents to interact with the web:
- Google search integration
- Web page content extraction
- Link extraction from pages
- PDF text extraction
- YouTube video transcript retrieval
- Text summarization
- Text embedding and semantic search
- Automated research workflows

## Features

- **Search**: Perform Google searches and get structured results
- **Page Extraction**: Extract clean text content from web pages
- **Link Extraction**: Get all links from a webpage
- **PDF Processing**: Extract text from PDF documents
- **YouTube Transcripts**: Retrieve transcripts from YouTube videos
- **Summarization**: Generate concise summaries of text content
- **Embeddings**: Store and search text using semantic embeddings
- **Research**: Automated multi-step research workflows

## Tools

- `search` - Google search with results
- `open_page` - Extract text from web pages
- `extract_links` - Get links from pages
- `extract_pdf` - Extract text from PDFs
- `youtube_transcript` - Get YouTube video transcripts
- `summarize` - Summarize text content
- `embed` - Store text embeddings
- `semantic_search` - Search stored embeddings
- `research` - Conduct automated research

## Installation

```bash
npm install
```

## Usage

Run the MCP server:
```bash
node index.js <tool_name> <json_input>
```

Example:
```bash
node index.js search '{"query":"artificial intelligence"}'
```

## Dependencies

- axios: HTTP requests
- cheerio: HTML parsing
- natural: Text processing
- pdf-parse: PDF text extraction
- youtube-transcript: YouTube transcript API