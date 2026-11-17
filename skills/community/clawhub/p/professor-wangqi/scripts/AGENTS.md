<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-21 | Updated: 2026-04-21 -->

# scripts

## Purpose
Python scripts for PDF processing, knowledge card extraction, vector index building, and interactive Q&A. This is the processing pipeline that transforms raw PDFs into a queryable knowledge base.

## Key Files
| File | Description |
|------|-------------|
| `extract_knowledge_cards.py` | Parse PDFs and extract structured knowledge cards following the schema |
| `build_local_index.py` | Build ChromaDB vector index from knowledge cards with local embeddings |
| `build_vector_index.py` | Generic vector index builder supporting chroma/milvus/weaviate backends |
| `ask.py` | Interactive Q&A script with RAG retrieval and citation generation |
| `upload_to_openai.py` | Upload knowledge cards to OpenAI vector store (for cloud deployment) |

## For AI Agents

### Working In This Directory
- These scripts form the core processing pipeline
- Test changes by running the full pipeline: extract → build → ask
- Environment variables are loaded from `../../.env`

### Script Usage

#### extract_knowledge_cards.py
```bash
# Extract from SCI papers
python extract_knowledge_cards.py --input ../data/01-体质与疾病文章-SCI/ --output ../data/cards/papers/ --type paper

# Extract from clinical experience articles
python extract_knowledge_cards.py --input ../data/03-王琦老师诊疗经验/ --output ../data/cards/experiences/ --type experience
```

#### build_local_index.py
```bash
python build_local_index.py --cards ../data/cards/ --collection wangqi_knowledge --persist-dir ../chroma_db
```

#### ask.py
```bash
# Single question
python ask.py "痰湿质与肥胖有什么关系？"

# Interactive mode
python ask.py --interactive
```

### Testing Requirements
- Verify PDF extraction produces valid JSON knowledge cards
- Test vector index with sample queries
- Ensure Q&A returns properly cited responses

### Common Patterns
- All scripts use `python-dotenv` to load environment from project root
- Embedding model: configured via `EMBEDDING_MODEL` env var
- Chat model: configured via `MODEL_NAME` env var
- LocalEmbeddingFunction class provides OpenAI-compatible embedding interface

## Dependencies

### Internal
- `../references/knowledge-card-schema.md` - Schema for extracted cards
- `../references/ontology.md` - Terminology for normalization
- `../data/cards/` - Output directory for knowledge cards
- `../chroma_db/` - Vector database storage

### External
- `fitz` (PyMuPDF) or `pdfplumber` - PDF parsing
- `chromadb` - Vector database
- `openai` - LLM and embedding API client
- `jieba` - Chinese word segmentation
- `python-dotenv` - Environment loading

<!-- MANUAL: -->
