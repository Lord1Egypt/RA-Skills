---
name: memora-knowledge-graph
description: >
  Memora — Personal AI Knowledge Base with interactive knowledge graph visualization.
  A self-hosted system for managing, retrieving, and querying your personal knowledge assets
  using vector search, hybrid retrieval, and LLM-driven intelligent Q&A.
  Features document upload/processing, semantic search, AI chat sessions, web scraping,
  and Obsidian-style knowledge graph visualization with force-directed layout.
  Use when: user wants to build a personal knowledge base, manage documents, perform semantic search,
  have AI-powered conversations about their knowledge, visualize document/entity relationships,
  or integrate knowledge management into their OpenClaw workflow.
metadata:
  version: 2.0.7
  author: zzlzzlzzl15
  license: MIT
  openclaw:
    requires:
      env:
        - KB_API_BASE
---

# Memora - Personal AI Knowledge Base

**Memora** is a self-hosted personal AI knowledge base system that provides an integrated experience from knowledge capture to intelligent Q&A. Built on vector retrieval, hybrid search, and LLM-driven intelligent organization, it helps you efficiently manage, retrieve, and utilize your personal knowledge assets.

## Version History

### v2.0.7 (Current)
- 🐳 **Docker Build Optimization**: Use Aliyun mirror sources for Debian packages, disable proxy during build
- 🔧 **Deployment Config**: Hardcoded database credentials in docker-compose, added HF_HUB_OFFLINE setting
- 🔒 **Data Consistency**: All v2.0.6 improvements included (Neo4j-MySQL sync, entity ID fix, sync API)

### v2.0.6
- 🔒 **Data Consistency Guarantee**: Real-time Neo4j-MySQL synchronization with automatic orphan node cleanup
  - Added `_ensure_consistency_with_mysql()` for pre-query validation
  - Integrated into all graph query methods (`get_document_graph`, `get_entity_graph`, `get_full_graph`, `get_stats`)
- 🗑️ **Enhanced Deletion Logic**: Improved `delete_document_graph()` with detailed logging and orphan entity cleanup
- 🆔 **Entity ID Fix**: Auto-generated UUIDs for all Entity nodes, resolving "0 nodes displayed" issue
- 🔄 **New Sync API**: `POST /api/v1/documents/knowledge-graph/sync` for manual consistency checks
- 📊 **Document Node Attributes**: Added `document_id` property for frontend-backend compatibility

### v2.0.5
- 📝 **Complete SKILL.md Rewrite**: Updated OpenClaw skill definition with full product overview
- 🎨 **Knowledge Graph v2.0**: Preview + Fullscreen Modal architecture
- 🖱️ **Enhanced Interactions**: Zoom, pan, drag, hover details
-  **Centered Layout**: Force-directed algorithm with origin-centered positioning
- 🔄 **Smart Caching**: Preview data cached, modal uses larger dataset
-  **Dual Views**: Document graph + Entity graph
-  **Package Updates**: Fixed package.json version mismatch

### v2.0.4
- 📝 **Complete Product Documentation**: Comprehensive README with full product overview
- 🎨 **Knowledge Graph v2.0**: Preview + Fullscreen Modal architecture
- 🖱️ **Enhanced Interactions**: Zoom, pan, drag, hover details
- 🎯 **Centered Layout**: Force-directed algorithm with origin-centered positioning
- 🔄 **Smart Caching**: Preview data cached, modal uses larger dataset
-  **Dual Views**: Document graph + Entity graph

### v2.0.0
- Initial release with knowledge graph visualization
- Force-directed layout with interactive controls
- Obsidian-inspired visual design

## Core Features

### 🔐 Privacy & Local Deployment
- **Fully Private**: Data stored locally, no third-party uploads
- **Offline Ready**: Works without internet connection
- **Single User Mode**: No authentication required, ready to use out of the box

###  Intelligent Semantic Retrieval
- **Hybrid Search**: Dense vectors + BM42 sparse vectors dual-engine retrieval
- **Relevance Reranking**: Optional Rerank model for secondary sorting
- **Fallback Mechanism**: Automatic fallback to backup strategies
- **Semantic Understanding**: Vector similarity-based, not keyword matching

### 📄 Multi-Format Document Processing
- **Supported Formats**: PDF, Word (.docx/.doc), Plain Text (.txt), Markdown (.md)
- **Smart Chunking**: LangChain recursive character splitter with Chinese/English support
- **Vector Storage**: Dense + sparse vectors stored in Qdrant
- **Metadata Management**: Tags and custom metadata for organization

###  AI-Powered Q&A
- **Two Interaction Modes**:
  - **Knowledge Query**: Precise Q&A based on retrieved results
  - **Knowledge Organization**: LLM automatically organizes and summarizes knowledge
- **Streaming Output**: Real-time content generation
- **Session Management**: Multi-turn conversations with history
- **Source Attribution**: Answers include source document links

### 🕸️ Knowledge Graph Visualization
- **Force-Directed Layout**: Automatic node positioning forming natural network structure
- **Dual View Display**: Document relationship graph + Entity relationship graph
- **Interactive Operations**:
  - Mouse wheel zoom (centered on cursor)
  - Drag blank area to pan canvas
  - Drag nodes to reposition
  - Hover to show details
- **Obsidian Style Design**: Black nodes, white background, subtle connections

### 🌐 Web Scraping & Integration
- **Built-in Crawler**: httpx + BeautifulSoup, no external dependencies
- **OpenClaw Integration**: Available as AI Agent Skill with zero-dependency client
- **RESTful API**: Easy integration with other systems

## Quick Start

### Installation via clawhub

```bash
openclaw skills install memora-knowledge-graph@2.0.4
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/zzlzzlzzl15/Memora.git
cd Memora/personal_knowledge_base

# Run installation script
./install.sh
```

### Docker Compose Deployment (Recommended)

```bash
# Clone repository
git clone https://github.com/zzlzzlzzl15/Memora.git
cd Memora/personal_knowledge_base

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# Start services
docker-compose up -d

# Access application
# Open http://localhost:8080 in browser
```

## Configuration

Set the `KB_API_BASE` environment variable to point to your Memora backend:

```bash
export KB_API_BASE=http://127.0.0.1:8080
```

Or create a `.env` file:
```
KB_API_BASE=http://127.0.0.1:8080
```

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `KB_API_BASE` | Memora backend URL | `http://127.0.0.1:8080` |
| `DEEPSEEK_API_KEY` | DeepSeek API Key (for LLM) | `sk-xxx` |
| `DASHSCOPE_API_KEY` | DashScope API Key (for embeddings) | `sk-xxx` |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `USE_RERANK` | Enable reranking | `false` |
| `RERANK_API_KEY` | Qwen3-Rerank API Key | - |
| `RETRIEVAL_TOP_K` | Initial retrieval candidates | `20` |
| `QDRANT_DENSE_DEFAULT_THRESHOLD` | Dense vector similarity threshold | `0.7` |

## Usage Examples

### Upload Documents

1. Click **"Upload Document"** button in left sidebar
2. Select file (PDF, DOCX, TXT, MD supported)
3. Fill in title and tags (optional)
4. Click **"Upload"** - system automatically parses, chunks, and vectorizes

### Ask Questions

1. Enter question in right-side chat interface
2. Choose interaction mode:
   - **Knowledge Query**: Get precise answers based on retrieval
   - **Knowledge Organization**: Let AI organize and summarize related knowledge
3. View answer with cited source documents

### Browse Knowledge Graph

1. Click **"Knowledge Graph"** button in top navigation
2. View two preview cards:
   - **Document Relationship Graph**: Shows connections between documents
   - **Entity Relationship Graph**: Shows extracted entities and relationships
3. Click any card to enter fullscreen modal for interactive exploration:
   - Scroll to zoom
   - Drag to pan
   - Drag nodes to reposition
   - Hover for details

### Manage Documents

- **View List**: See all documents in left sidebar
- **Search**: Use quick search function
- **Recycle Bin**: View and manage deleted documents (recoverable within 30 days)
- **Permanent Delete**: Permanently remove documents and vector data

## Technical Architecture

```
┌─────────────────────────────────────────┐
│           Web Browser                    │
│     (Frontend UI - HTML/CSS/JS)         │
└──────────────┬──────────────────────────┘
               │ HTTP / WebSocket
┌──────────────▼──────────────────────────┐
│         Memora Backend                   │
│       (FastAPI / Python)                │
──────────┬──────────────┬───────────────┤
│ Document │  Retrieval   │ AI Services   │
│Processing│   Engine     │               │
├──────────┼──────────────┼───────────────┤
│• PDF     │• Dense Vector│• Embedding    │
│  Parser  │  Search      │  (DashScope/  │
│• DOCX    │• Sparse Vector│  Local ST)   │
│  Parse   │  (BM42)      │• LLM Chat     │
│• Text    │• Hybrid Search│  (DeepSeek/  │
│  Split   │• Fallback     │  OpenAI Comp)│
│• Metadata│  Logic       │• Rerank       │
│• Upload  │              │  (Qwen3)      │
│  API     │              │• Stream       │
│          │              │  Response     │
└────┬─────┴──────┬───────┴───────┬───────┘
     │            │               │
┌────▼────┐ ┌────▼──────┐ ┌──────▼──────┐
│ MySQL   │ │  Qdrant   │ │ External    │
│(Metadata)│ │(Vector DB)│ │ APIs        │
│         │ │           │ │             │
│• Docs   │ │• Dense    │ │• DashScope  │
│• Users  │ │  Vectors  │ │• DeepSeek   │
│• Sessions│ │• Sparse   │ │• OpenAI     │
│• History │ │  (BM42)   │ │ Compatible  │
└─────────┘ └───────────┘ └─────────────┘
```

### Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| **Backend Framework** | FastAPI (Python 3.11+) | High-performance async web framework |
| **Vector Database** | Qdrant | Hybrid retrieval with dense + sparse vectors |
| **Relational Database** | MySQL 8.0 | Document metadata, users, sessions |
| **Embedding Model** | DashScope text-embedding-v4 / Sentence-Transformers | Cloud API or local models |
| **LLM Service** | DeepSeek / OpenAI Compatible | Streaming output, multi-turn chat |
| **Rerank Model** | Qwen3-Rerank (optional) | Improves retrieval relevance |
| **Document Parsing** | PyPDF2, docx2txt, LangChain | Multi-format processing |
| **Web Scraping** | httpx + BeautifulSoup | Built-in crawler, no dependencies |
| **Containerization** | Docker + Docker Compose | One-click deployment |

## Troubleshooting

### Issue: Preview cards not showing
**Solution**: Check browser console for errors. Ensure `initKnowledgeGraph()` is called after DOM ready.

### Issue: Nodes not centered
**Solution**: Hard refresh page (Cmd+Shift+R). Clear browser cache if needed.

### Issue: Cannot drag/zoom in modal
**Solution**: Verify `setInteractive(true)` is called for fullscreen visualizer. Check console logs.

### Issue: Service won't start
**Solution**: 
```bash
# Check logs
docker-compose logs -f app

# Clean and restart
docker-compose down -v
docker-compose up -d
```

### Issue: Document upload fails
**Solution**:
- Check file format (PDF, DOCX, TXT, MD only)
- Check file size (default limit: 10MB)
- Review application logs: `docker-compose logs -f app`

### Issue: No retrieval results
**Solution**:
- Confirm documents are uploaded and vectorized
- Try different query terms
- Lower `QDRANT_DENSE_DEFAULT_THRESHOLD` value

### Issue: LLM call fails
**Solution**:
```bash
# Check API key configuration
cat .env | grep API_KEY

# Test API connectivity
curl -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  https://api.deepseek.com/v1/chat/completions \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"test"}]}'
```

## Performance Tips

1. **Limit Node Count**: Use smaller limits for previews (50-80 nodes)
2. **Cache Data**: Reuse fetched data instead of reloading
3. **Debounce Resize**: Add debounce to window resize handler
4. **Reduce Iterations**: Lower `iterations` in `initForceLayout()` for faster load (default: 150)
5. **Optimize Rendering**: Skip rendering during rapid mouse movements

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

Requires:
- Canvas 2D API
- CSS backdrop-filter
- ES6+ JavaScript features

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Submit a pull request

## Support

For issues and questions:
- GitHub Issues: https://github.com/zzlzzlzzl15/Memora/issues
- Email: support@memora.dev
- Documentation: https://github.com/zzlzzlzzl15/Memora/blob/main/personal_knowledge_base/README.md

## Acknowledgments

- Inspired by [Obsidian](https://obsidian.md/) graph view
- Built for [Memora](https://github.com/zzlzzlzzl15/Memora) personal knowledge base
- Uses force-directed layout algorithm similar to D3.js force simulation
- References [RAG-Anything](https://github.com/RAG-Anything/RAG-Anything) for multimodal RAG architecture

---

**Made with ❤️ by zzlzzlzzl15**

*Memora - Your Personal AI Knowledge Base*
