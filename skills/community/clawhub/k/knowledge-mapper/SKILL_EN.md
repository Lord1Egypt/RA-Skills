---
version: "1.0.2"
---

# Knowledge Graph Builder

A CLI tool for document knowledge extraction and visualization.

## Description

Knowledge Graph Builder transforms your documents into structured knowledge graphs. It parses Markdown and text files, extracts entities and relationships, and exports visualizations in multiple formats—perfect for research, note-taking, and knowledge management.

## Features

- 📄 **Document Parsing**: Support for Markdown and TXT formats
- 🔍 **Entity Recognition**: Rule-based and keyword-driven entity extraction
- 🔗 **Relationship Discovery**: Co-occurrence based relationship extraction
- 📊 **Knowledge Visualization**: Export to text, JSON, or GraphViz DOT format
- 🔎 **Knowledge Query**: Search entities and documents

## Installation

```bash
# Add to PATH
ln -s ~/.openclaw/workspace/skills/knowledge-mapper/knowledge-graph ~/.local/bin/knowledge-graph
```

## Usage

### Add Documents

```bash
# Add a Markdown document
knowledge-graph add ~/documents/article.md

# Add a text file
knowledge-graph add ~/notes/ideas.txt
```

### View Documents

```bash
knowledge-graph documents
```

### View Entities

```bash
# List all entities (default: 50)
knowledge-graph entities

# List more entities
knowledge-graph entities --limit 100

# Filter by type
knowledge-graph entities --type TECH
```

### Entity Types

| Type | Description |
|------|-------------|
| `PERSON` | People and names |
| `ORG` | Organizations and companies |
| `TECH` | Technologies and programming languages |
| `CONCEPT` | Concepts and terminology |
| `TERM` | High-frequency terms |
| `UNKNOWN` | Uncategorized entities |

### View Relationships

```bash
# List all relationships (default: 30)
knowledge-graph relations

# List more relationships
knowledge-graph relations --limit 50
```

### Export Knowledge Graph

```bash
# Text format (default)
knowledge-graph export

# JSON format
knowledge-graph export --format json

# GraphViz DOT format (for visualization)
knowledge-graph export --format dot > graph.dot
dot -Tpng graph.dot -o graph.png
```

### Search Knowledge Base

```bash
# Search by keyword
knowledge-graph search "artificial intelligence"

# Search for an entity
knowledge-graph search "Python"
```

### View Statistics

```bash
knowledge-graph stats
```

## Examples

### Complete Workflow

```bash
# 1. Add documents to the knowledge base
knowledge-graph add ~/docs/project-notes.md
knowledge-graph add ~/docs/research-paper.md
knowledge-graph add ~/docs/tech-stack.md

# 2. View extracted entities
knowledge-graph entities --limit 20

# 3. View discovered relationships
knowledge-graph relations

# 4. Export for visualization
knowledge-graph export --format dot > my-knowledge.dot

# 5. Generate image (requires GraphViz)
dot -Tpng my-knowledge.dot -o my-knowledge.png
```

### Research Project Analysis

```bash
# Add multiple research documents
knowledge-graph add ~/research/paper-1.md
knowledge-graph add ~/research/paper-2.md
knowledge-graph add ~/research/notes.txt

# Extract entities and relationships
knowledge-graph entities --limit 100 > entities.txt
knowledge-graph relations --limit 50 > relations.txt

# Export as JSON for further processing
knowledge-graph export --format json > knowledge.json

# Generate visual knowledge map
knowledge-graph export --format dot > research-graph.dot
dot -Tsvg research-graph.dot -o research-graph.svg
```

## Data Storage

Data is stored in `~/.openclaw/data/knowledge-graph/`:
- `knowledge_graph.db` - SQLite database

## Technical Details

- **Language**: Python 3.8+
- **Database**: SQLite
- **CLI Framework**: argparse
- **Entity Extraction**: Regular expressions and rule-based patterns
- **Relationship Discovery**: Co-occurrence analysis

## Requirements

- Python 3.8 or higher
- SQLite3
- GraphViz (optional, for visualization)

## Roadmap

- [ ] Support for additional formats (PDF, Word)
- [ ] NLP model integration for precise entity recognition
- [ ] Relationship inference and completion
- [ ] Interactive knowledge graph visualization
- [ ] Entity linking and disambiguation

## License

MIT License