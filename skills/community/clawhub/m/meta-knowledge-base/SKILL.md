---
name: meta-knowledge-base
description: AI-powered knowledge base builder that automatically captures, organizes, and retrieves information. Learns from conversations, documents, and interactions to build a personalized knowledge graph. Enables semantic search and intelligent Q&A.
tags:
  - meta
  - knowledge
  - knowledge-base
  - rag
  - embedding
  - vector-search
version: 1.0.0
author: chenq
---

# Meta Knowledge Base

Self-building knowledge management system that learns and grows automatically.

## Features

### 1. Auto-Capture
- **Conversation Learning**: Extract key information from chats
- **Document Parsing**: Extract from PDFs, docs, emails
- **Web Scraping**: Learn from visited pages
- **File Watch**: Monitor folders for new content

### 2. Knowledge Organization
- **Auto-Tagging**: Automatic topic categorization
- **Entity Extraction**: People, companies, concepts
- **Relationship Mapping**: Connect related ideas
- **Version History**: Track knowledge evolution

### 3. Semantic Search
- **Vector Embeddings**: Semantic similarity search
- **Hybrid Search**: Combine keyword + semantic
- **Filtering**: Filter by date, tags, source
- **Ranking**: Relevance-based results

### 4. Intelligent Q&A
- **RAG Pipeline**: Retrieve + Generate answers
- **Context-Aware**: Understand conversation context
- **Citing Sources**: Reference original knowledge
- **Confidence Scoring**: Show answer confidence

### 5. Continuous Learning
- **User Feedback**: Learn from corrections
- **Implicit Learning**: Learn from interactions
- **Knowledge Updates**: Keep information fresh
- **Gap Identification**: Find missing knowledge

## Installation

```bash
pip install numpy faiss-cpu sentence-transformers
```

## Usage

### Initialize Knowledge Base

```python
from meta_knowledge import KnowledgeBase

kb = KnowledgeBase(
    name="my_knowledge",
    embedding_model="paraphrase-multilingual-MiniLM-L12-v2"
)
```

### Add Knowledge

```python
# From text
kb.add(
    content="Python is a high-level programming language...",
    tags=["programming", "python"],
    metadata={"source": "user", "date": "2026-03-22"}
)

# From document
kb.add_from_file("document.pdf", tags=["research"])

# From URL
kb.add_from_url("https://example.com/article", tags=["news"])
```

### Search

```python
# Semantic search
results = kb.search(
    query="What is machine learning?",
    top_k=5
)

for r in results:
    print(f"{r.score:.2f} | {r.content[:100]}...")
```

### Q&A

```python
# Ask questions
answer = kb.ask(
    question="What do I know about AI?",
    include_sources=True
)

print(answer['answer'])
print("Sources:", answer['sources'])
```

### Knowledge Graph

```python
# Get entity relationships
graph = kb.get_knowledge_graph()

# Find related concepts
related = kb.find_related("Python", depth=2)
```

## API Reference

### Adding Knowledge
| Method | Description |
|--------|-------------|
| `add(content, ...)` | Add single piece of knowledge |
| `add_batch(contents)` | Add multiple items |
| `add_from_file(path)` | Parse and add file |
| `add_from_url(url)` | Fetch and add web content |
| `add_from_email(email)` | Parse email content |

### Searching
| Method | Description |
|--------|-------------|
| `search(query, top_k)` | Semantic search |
| `hybrid_search(query, ...)` | Keyword + semantic |
| `filter_search(query, filters)` | Search with filters |
| `find_similar(content)` | Find similar items |

### Q&A
| Method | Description |
|--------|-------------|
| `ask(question, ...)` | Get answer with RAG |
| `get_context(question)` | Get relevant context |
| `generate_summary(topic)` | Generate topic summary |

### Management
| Method | Description |
|--------|-------------|
| `get_knowledge_graph()` | Get entity relationships |
| `list_tags()` | List all tags |
| `export(format)` | Export knowledge |
| `import_(data)` | Import knowledge |

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Sources   │────▶│  Ingestion  │────▶│   Storage    │
│ - Chat      │     │ - Parser    │     │ - Vector DB  │
│ - Docs      │     │ - Embedder  │     │ - Graph DB   │
│ - Web       │     │ - Indexer   │     │ - Document   │
└─────────────┘     └─────────────┘     └─────────────┘
                                           │
                    ┌──────────────────────┘
                    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Query     │────▶│   Retrieve  │────▶│   Generate  │
│ - Search    │     │ - Vector    │     │ - LLM       │
│ - Ask       │     │ - Graph     │     │ - Cite      │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Embedding Models

| Model | Dimensions | Languages | Use Case |
|-------|------------|-----------|----------|
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | 50+ | General |
| bge-small-zh-v1.5 | 512 | Chinese | Chinese |
| text-embedding-ada-002 | 1536 | EN | Production |

## Use Cases

- **Personal Assistant**: Remember everything
- **Team Wiki**: Shared knowledge base
- **Customer Support**: Q&A automation
- **Research**: Paper search & summarization
- **Codebase**: Documentation search

## Best Practices

1. **Regular Updates**: Keep knowledge fresh
2. **Quality over Quantity**: Clean data matters
3. **Use Tags**: Organize for better retrieval
4. **User Feedback**: Improve with corrections
5. **Backup**: Export regularly

## Integration

### With OpenClaw

```python
# Auto-capture from conversations
@hookimpl
def after_message(message, response):
    kb.add(
        content=f"User asked about: {extract_topics(message)}",
        tags=["conversation", extract_topics(message)]
    )
```

### With Skills

```python
# Use knowledge in skills
def my_skill(query):
    context = kb.search(query, top_k=3)
    return generate_response(query, context)
```

## Future Capabilities

- Multi-modal knowledge (images, audio)
- Real-time sync across devices
- Collaborative knowledge base
- Automatic knowledge validation
