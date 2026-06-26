# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2026-03-11

### 🔧 Hotfix - Critical Bug Fixes

#### Fixed
- **API Error Handling**: Improved exception handling in routes to distinguish between validation errors (400), not found (404), and server errors (500)
- **L1 Memory Protection**: Added LRU eviction and memory limit enforcement to prevent unbounded memory growth
  - Max size: 100MB
  - Max entries: 10,000
  - Automatic TTL-based and LRU-based eviction
- **L3 Race Condition**: Added file locking mechanism to prevent data corruption during concurrent writes
  - Per-file asyncio locks
  - Write retry with exponential backoff

#### Security
- Added input validation for API endpoints
- Added logging for all error conditions

## [1.0.0] - 2026-03-11

### ✨ Initial Release

#### Features
- **Four-tier memory architecture**: L1 (Hot) → L2 (Warm) → L3 (Cold) → L4 (Archive)
- **Persona generation engine**: Create and evolve AI agent personalities
- **Event detection**: Automatic importance scoring and categorization
- **Vector search**: Semantic memory retrieval using FAISS
- **Daily/weekly persistence**: Automated memory archival
- **RESTful API**: Full-featured FastAPI backend

#### Components
- L1 Hot Storage: In-memory cache with TTL
- L2 Warm Storage: SQLite with structured queries
- L3 Cold Storage: Markdown files for human readability
- L4 Archive: FAISS vector index with compression
- Persona Service: Personality generation and evolution
- Embedding Service: Multilingual sentence embeddings

---

**Version Format**: Based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
