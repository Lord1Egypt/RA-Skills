<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-21 | Updated: 2026-04-21 -->

# professor-wangqi

## Purpose
Main skill implementation for Professor Wang Qi's TCM Constitution Academic Assistant. Provides PDF parsing, knowledge card extraction, vector indexing, and RAG-powered Q&A with traceable citations.

## Key Files
| File | Description |
|------|-------------|
| `SKILL.md` | Skill definition with trigger conditions, workflow, and response format |
| `README.md` | Detailed documentation with quickstart guide and architecture |
| `QUICKSTART.md` | Quick start guide for setup and usage |
| `requirements.txt` | Python dependencies for this skill |
| `test_index.py` | Test script for vector index functionality |
| `test_retrieval.py` | Test script for retrieval accuracy |
| `temp_pdf_text.txt` | Temporary PDF text extraction output |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `scripts/` | Python scripts for PDF processing, indexing, and Q&A (see `scripts/AGENTS.md`) |
| `data/` | Source PDFs and extracted knowledge cards (see `data/AGENTS.md`) |
| `references/` | Schema definitions and ontology (see `references/AGENTS.md`) |
| `evals/` | Evaluation test cases (see `evals/AGENTS.md`) |
| `chroma_db/` | ChromaDB vector database storage |
| `assets/` | Asset files (reserved for future use) |

## For AI Agents

### Working In This Directory
- This is the main skill package - changes here affect the core functionality
- Always test with `python scripts/ask.py --interactive` after modifications
- The skill follows a RAG architecture: PDF → Knowledge Card → Vector Index → Q&A

### Testing Requirements
- Run `python test_index.py` to verify vector index
- Run `python test_retrieval.py` to test retrieval accuracy
- Use evaluation cases in `evals/evals.json` for comprehensive testing

### Common Patterns
- Knowledge cards use JSON format defined in `references/knowledge-card-schema.md`
- Evidence levels: `[论文]` > `[诊疗经验]` > `[知识归纳]` > `[模型推断]`
- Nine constitution types: 平和质, 气虚质, 阳虚质, 阴虚质, 痰湿质, 湿热质, 血瘀质, 气郁质, 特禀质

### Workflow
1. Place PDFs in `data/01-体质与疾病文章-SCI/` or `data/03-王琦老师诊疗经验/`
2. Run `python scripts/extract_knowledge_cards.py` to generate knowledge cards
3. Run `python scripts/build_local_index.py` to build vector index
4. Run `python scripts/ask.py` for Q&A

## Dependencies

### Internal
- `../.env` - Environment configuration (API keys, model settings)
- `references/knowledge-card-schema.md` - Knowledge card structure definition
- `references/ontology.md` - TCM terminology normalization

### External
- `openai` - OpenAI-compatible API for LLM and embeddings
- `chromadb` - Local vector database
- `pymupdf` / `pdfplumber` - PDF text extraction
- `jieba` - Chinese word segmentation

<!-- MANUAL: -->
