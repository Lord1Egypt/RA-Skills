# KB Framework Roadmap

**Version:** 1.2.0  
**Last Updated:** 2026-04-27

---

## Overview

This document outlines the strategic direction and planned enhancements for the KB Framework. Items are organized by priority and estimated complexity.

---

## Current Priorities

### Critical

| Feature | Description | Status |
|---------|-------------|--------|
| **Complete Code Review** | Full 10-phase review (context, functions, architecture, connections, optimizations, hardcoded paths, performance, security, tests, documentation) | ✅ Done |
| **Bug Fixes Round 1-3** | 33 bugs found and fixed, 3 false positives identified | ✅ Done |
| **Meta-Review Workflow** | Review + self-validation tested (20% false positive rate) | ✅ Done |
| **Performance Optimizations** | fetchall() → fetchmany(1000), COUNT queries, ChromaDB batching | ✅ Done |
| **Security Improvements** | Exception handling, SQL injection protection, path traversal | ✅ Done |
| **Documentation Sync** | README.md, SKILL.md, CHANGELOG.md updated to 1.2.0 | ✅ Done |
| **Hybrid Search Module** | Re-integration of combined keyword + semantic search capabilities | ✅ Done |
| **ChromaDB Warmup** | Model preloading to eliminate cold-start latency | ✅ Done |
| **Delta Indexing** | Incremental re-indexing based on file modification timestamps | ✅ Done |
| **SearchCommand CLI** | Unified search command with filters (semantic/keyword/fts5) | ✅ Done |
| **FTS5 Integration** | SQLite Full-Text Search for keyword fallback | ✅ Done |
| **Reranker Module** | Cross-encoder reranking for search results | ✅ Done |
| **ChromaPlugin** | ChromaDB collection management and persistence | ✅ Done |

### High

| Feature | Description | Status |
|---------|-------------|--------|
| OCR Engine Configuration | Flexible OCR backend selection (Tesseract default, EasyOCR optional) | Planned |
| **ChromaDB Warmup** | Model preloading to eliminate cold-start latency | ✅ Done |
| **Delta Indexing** | Incremental re-indexing based on file modification timestamps | ✅ Done |
| **SearchCommand CLI** | Unified search command with filters (semantic/keyword/fts5) | ✅ Done |
| **FTS5 Integration** | SQLite Full-Text Search for keyword fallback | ✅ Done |
| **Reranker Module** | Cross-encoder reranking for search results | ✅ Done |
| **ChromaPlugin** | ChromaDB collection management and persistence | ✅ Done |

### Medium

| Feature | Description | Status |
|---------|-------------|--------|
| Backup/Restore CLI | Native commands for database and vector store management | Planned |
| Test Coverage | Comprehensive test suite alignment with current schema | In Progress |
| Auto-Updater Validation | Production testing of the update mechanism | Planned |
| **Gemma LLM Integration** | Optional local LLM support for query enhancement (Google Gemma 4B) | Proposed |

### Future

| Feature | Description | Status |
|---------|-------------|--------|
| Web Interface | Browser-based search and status dashboard | Backlog |
| Plugin Architecture | Extensible hook system for custom indexers | Backlog |
| Full i18n Support | Complete internationalization framework | Backlog |

---

## Completed (Recent)

| Feature | Date | Description |
|---------|------|-------------|
| KB Migration | 2024-04-13 | Migration from legacy structure; 868 files indexed |
| Auto-Updater Fix | 2024-04-13 | Repository configuration corrected |
| Documentation Update | 2024-04-13 | Installation guides and structure diagrams |
| Database Integrity | 2024-04-13 | Foreign key constraints enabled; orphaned records removed |
| Code Standardization | 2024-04-13 | All docstrings and comments migrated to English |

---

## Design Principles

**Offline-First:** All operations function without external network dependencies, cloud services, or API keys.

---

*This roadmap is reviewed weekly. For contribution guidelines, see CONTRIBUTING.md.*
