---
name: hxxra
description: A Research Assistant workflow skill with five core commands: search papers, download PDFs, analyze content, generate reports, and save to Zotero. Entry point is a Python script located at scripts/hxxra.py and invoked via stdin/stdout (OpenClaw integration). The search uses crawlers for Google Scholar and arXiv APIs; download uses Python requests or arXiv API; analyze uses an LLM; report generates Markdown summaries from analysis.json files; save uses Zotero API.
---

# hxxra

This skill is a Research Assistant that helps users search, download, analyze, report, and save research papers.

## Recommended Directory Structure

For better organization, it is recommended to create a dedicated workspace for `hxxra` under your OpenClaw working directory:

```
📁 workspace/                              # OpenClaw current working directory
└── 📁 hxxra/
    ├── 📁 searches/                       # Stores all search result JSON files
        ├── 2025-03-07_neural_radiance_fields_arxiv.json
        ├── 2025-03-07_transformer_architectures_scholar.json
        └── ...
    ├── 📁 papers/                           # Stores downloaded PDF files and per-paper analysis results (each as a subfolder)
        ├── papers_report.md                # Generated Markdown report summarizing all analyzed papers
        ├── 2023_Smith_NeRF_Explained/      # Folder named after the PDF (without extension)
          ├── 2023_Smith_NeRF_Explained.pdf
          ├── analysis.json                 # Structured output from LLM analysis
          └── notes.md                      # (Optional) User-added notes
        ├── 2024_Zhang_Transformer_Survey/
          ├── 2024_Zhang_Transformer_Survey.pdf
          ├── analysis.json
          └── ...
        └── ...
    └── 📁 logs/ # Stores execution logs
        └── hxxra_2025-03-07.log
```

This structure keeps all related files organized and easily accessible for review and further processing.

## Core Commands

### 1. **hxxra search** - Search for research papers

**Dependencies**: `pip install scholarly`

**Purpose**: Search for papers using Google Scholar and arXiv APIs

**Academic Note**: To account for the distinct characteristics of each data source, the tool adopts a differentiated sorting strategy—**arXiv results are ordered by submission date in descending order**, prioritizing the timeliness of recent research; **Google Scholar results retain the source's default relevance ranking**, ensuring strong alignment with the query keywords while appropriately weighing influential or classical literature.

**Parameters**:

- `-q, --query <string>` (Required): Search keywords
- `-s, --source <string>` (Optional): Data source: `arxiv` (default), `scholar`
- `-l, --limit <number>` (Optional): Number of results (default: 10)
- `-o, --output <path>` (Optional): JSON output file (default: `{workspace}/hxxra/searches/search_results.json`)

**Input Examples**:

```json
{"command": "search", "query": "neural radiance fields", "source": "arxiv", "limit": 10, "output": "results.json"} | python scripts/hxxra.py
{"command": "search", "query": "transformer architecture", "source": "scholar", "limit": 15} | python scripts/hxxra.py
```

**Output Structure**:

```json
{
  "ok": true,
  "command": "search",
  "query": "<query>",
  "source": "<source>",
  "results": [
    {
      "id": "1",
      "title": "Paper Title",
      "authors": ["Author1", "Author2"],
      "year": "2023",
      "source": "arxiv",
      "abstract": "Abstract text...",
      "url": "https://arxiv.org/abs/xxxx.xxxxx",
      "pdf_url": "https://arxiv.org/pdf/xxxx.xxxxx.pdf",
      "citations": 123
    }
  ],
  "total": 10,
  "output_file": "/path/to/results.json"
}
```

------

### 2. **hxxra download** - Download PDF files

**Purpose**: Download PDFs for specified papers

**Parameters**:

- `-f, --from-file <path>` (Required): JSON file with search results
- `-i, --ids <list>` (Optional): Paper IDs (comma-separated or range)
- `-d, --dir <path>` (Optional): Download directory (default: `{workspace}/hxxra/papers/`)

**Input Examples**:

```json
{"command": "download", "from-file": "results.json", "ids": ["1", "3", "5"], "dir": "./downloads"} | python scripts/hxxra.py
{"command": "download", "from-file": "results.json", "dir": "./downloads"} | python scripts/hxxra.py
```

**Output Structure**:

```json
{
  "ok": true,
  "command": "download",
  "downloaded": [
    {
      "id": "1",
      "title": "Paper Title",
      "status": "success",
      "pdf_path": "{workspace}/hxxra/papers/2023_Smith_NeRF_Explained/2023_Smith_NeRF_Explained.pdf",
      "size_bytes": 1234567,
      "url": "https://arxiv.org/pdf/xxxx.xxxxx.pdf"
    }
  ],
  "failed": [],
  "total": 3,
  "successful": 3,
  "download_dir": "{workspace}/hxxra/papers"
}
```

------

### 3. **hxxra analyze** - Analyze PDF content

**Dependencies**: `pip install pymupdf pdfplumber openai`

**Purpose**: Analyze paper content using LLM

**Parameters**:

- `-p, --pdf <path>` (Optional*): Single PDF file to analyze
- `-d, --directory <path>` (Optional*): Directory with multiple PDFs
- `-o, --output <path>` (Optional): Output directory. If not specified, analysis results will be saved in the same subfolder as the PDF (default: `{workspace}/hxxra/papers/{paper_title}/analysis.json`)

** Note: Either `--pdf` or `--directory` must be provided, but not both*

**Input Examples**:

```json
{"command": "analyze", "pdf": "paper.pdf", "output": "./analysis/"} | python scripts/hxxra.py
{"command": "analyze", "directory": "hxxra/papers/"} | python scripts/hxxra.py
```

**Output Structure**:

```json
{
  "ok": true,
  "command": "analyze",
  "analyzed": [
    {
      "id": "paper_1",
      "original_file": "paper.pdf",
      "analysis_file": "{workspace}/hxxra/papers/2023_Smith_NeRF_Explained/analysis.json",
      "metadata": {
        "title": "Paper Title",
        "authors": ["Author1", "Author2"],
        "year": "2023",
        "abstract": "Abstract text..."
      },
      "analysis": {
        "background": "Problem background...",
        "methodology": "Proposed method...",
        "results": "Experimental results...",
        "conclusions": "Conclusions..."
      },
      "status": "success"
    }
  ],
  "summary": {
    "total": 1,
    "successful": 1,
    "failed": 0
  }
}
```

------

### 4. **hxxra report** - Generate Markdown report

**Purpose**: Generate a comprehensive Markdown report from all `analysis.json` files in a directory

**Parameters**:

- `-d, --directory <path>` (Required): Directory containing paper folders with `analysis.json` files
- `-o, --output <path>` (Optional): Output Markdown file path (default: `{directory}/report.md`)
- `-t, --title <string>` (Optional): Report title (default: "Research Papers Report")
- `-s, --sort <string>` (Optional): Sort by: `year` (default, descending), `title`, or `author`

**Input Examples**:

```json
{"command": "report", "directory": "hxxra/papers/", "output": "hxxra/papers/report.md", "title": "My Research Papers", "sort": "year"} | python scripts/hxxra.py
{"command": "report", "directory": "hxxra/papers/"} | python scripts/hxxra.py
```

**Output Structure**:

```json
{
  "ok": true,
  "command": "report",
  "total_papers": 10,
  "output_file": "/path/to/hxxra/papers/report.md"
}
```

**Generated Markdown Format**:

The generated report includes:
- **Header**: Title, generation date, total papers, data source
- **Keywords Table**: Top 15 most frequent keywords across all papers
- **Overview Table**: Quick summary of all papers (title, author, year, keywords)
- **Detailed Content**: For each paper:
  - Title, authors, year, keywords, code link (if available)
  - Abstract
  - Research background
  - Methodology
  - Main results
  - Conclusions
  - Limitations
  - Impact
  - Source folder path

**Note**: The report command recursively scans all subdirectories for `analysis.json` files and only includes papers with `status: "success"`.

------

### 5. **hxxra save** - Save to Zotero

**Purpose**: Save papers to Zotero collection

**Parameters**:

- `-f, --from-file <path>` (Required): JSON file with search results (e.g., `hxxra/searches/search_results.json`)
- `-i, --ids <list>` (Optional): Paper IDs to save
- `-c, --collection <string>` (Required): Zotero collection name

**Input Examples**:

```json
{"command": "save", "from-file": "hxxra/searches/search_results.json", "ids": ["1", "2", "3"], "collection": "AI Research"} | python scripts/hxxra.py
{"command": "save", "from-file": "hxxra/searches/search_results.json", "collection": "My Collection"} | python scripts/hxxra.py
```

**Output Structure**:

```json
{
  "ok": true,
  "command": "save",
  "collection": "AI Research",
  "saved_items": [
    {
      "id": "1",
      "title": "Paper Title",
      "zotero_key": "ABCD1234",
      "url": "https://www.zotero.org/items/ABCD1234",
      "status": "success"
    }
  ],
  "failed_items": [],
  "total": 3,
  "successful": 3,
  "zotero_collection": "ABCD5678"
}
```

------

## Workflow Examples

### Complete Workflow

```bash
# 1. Search for papers
{"command": "search", "query": "graph neural networks", "source": "arxiv", "limit": 10, "output": "hxxra/searches/gnn_arxiv.json"} | python scripts/hxxra.py

# 2. Download papers
{"command": "download", "from-file": "hxxra/searches/gnn_arxiv.json", "dir": "hxxra/papers"} | python scripts/hxxra.py

# 3. Analyze downloaded papers
{"command": "analyze", "directory": "hxxra/papers/"} | python scripts/hxxra.py

# 4. Generate comprehensive report
{"command": "report", "directory": "hxxra/papers/", "output": "hxxra/papers/report.md", "sort": "year"} | python scripts/hxxra.py

# 5. Save to Zotero
{"command": "save", "from-file": "hxxra/searches/gnn_arxiv.json", "collection": "GNN Papers"} | python scripts/hxxra.py
```

### Single Command Examples

```bash
# Search with scholar
{"command": "search", "query": "reinforcement learning", "source": "scholar", "limit": 15} | python scripts/hxxra.py

# Download specific papers
{"command": "download", "from-file": "hxxra/searches/search_results.json", "ids": ["2", "4", "6"], "dir": "hxxra/papers"} | python scripts/hxxra.py

# Analyze single PDF in detail
{"command": "analyze", "pdf": "hxxra/papers/2024_Zhang_Transformer_Survey/2024_Zhang_Transformer_Survey.pdf"} | python scripts/hxxra.py

# Generate report sorted by title
{"command": "report", "directory": "hxxra/papers/", "sort": "title", "output": "hxxra/papers/report_by_title.md"} | python scripts/hxxra.py

# Save with custom notes
{"command": "save", "from-file": "hxxra/searches/search_results.json", "ids": ["1"], "collection": "To Read"} | python scripts/hxxra.py
```

## Configuration Requirements

### API Credentials(config.json)

1. **arXiv API**: No key required for basic access

2. **Google Scholar**: May require authentication for large queries

3. **Zotero API**: Required credentials:

   ```json
   {
     "api_key": "YOUR_ZOTERO_API_KEY", # Create at https://www.zotero.org/settings/keys/new
     "user_id": "YOUR_ZOTERO_USER_ID", # Found on the same page (numeric, not username)
     "library_type": "user"  # or "group"
   }
   ```

4. **LLM API**: OpenAI or compatible API key for analysis

## Notes

- All commands are executed via stdin/stdout JSON communication
- Error handling returns `{"ok": false, "error": "Error message"}`
- Large operations support progress reporting via intermediate messages
- Configuration is loaded from `config.json` or environment variables
- Concurrent operations have configurable limits to avoid rate limiting

## Error Handling

Each command returns standard error format:

```json
{
  "ok": false,
  "command": "<command>",
  "error": "Error description",
  "error_code": "ERROR_TYPE",
  "suggestion": "How to fix it"
}
```

## Development Status

### Current Version: v1.2.0 (2026/3/8)

### Version History

**v1.2.0 · 2026/3/8**

- Added `report` command to generate comprehensive Markdown reports from all `analysis.json` files
- Report includes keyword statistics, overview table, and detailed content for each paper
- Supports sorting by year (default), title, or author
- Generates clean, readable Markdown format with tables, headers, and structured content
- Updated documentation to include the new report command in workflows and examples

**v1.1.1 · 2026/3/7**

- Added `sanitize_filename()` function to unify filename and folder name handling for downloaded papers.
- Modified `handle_download` function to use the new sanitization function for author names and titles.
- Improved filename safety: now only allows letters, numbers, and underscores; multiple consecutive underscores are merged; length limited to 50 characters.

**v1.1.0 · 2026/3/7**

- Added a recommended directory structure for optimal organization of search results, papers, analysis, and logs.
- Updated all examples and default output locations to align with the new `{workspace}/hxxra/` folder layout.
- Clarified file storage practices: each downloaded paper now has its own subfolder containing the PDF and analysis files.
- Improved documentation for command parameters and outputs to reflect the directory structure changes.
- Enhanced clarity of workflow steps, making it easier to manage, locate, and share research outputs.
- Fixed ids data handling: improved ID matching logic to support both string and numeric ID comparisons in download and save commands.
- Fixed analyze output parameter: output directory is now only created when explicitly specified, otherwise analysis results are saved in the same subfolder as the PDF.
- Fixed Zotero API "400 Bad Request" error: changed data format from object to array (`[item_data]`) to comply with Zotero API requirements

**v1.0.2 · 2026/3/6**

- Modified hxxra.py script to add fix_proxy_env() function call, resolving the issue where ALL_PROXY and all_proxy are reset to socks://127.0.0.1:7897/ in new OpenClaw sessions, causing search failures

**v1.0.1 · 2026/3/6**

- Added academic note clarifying that arXiv search results are sorted by most recent submission date, while Google Scholar results use the source's default relevance ranking
- No changes to command structure, parameters, or output formats

**v1.0.0 · 2026/2/9**

Initial release of hxxra – a research assistant tool for searching, downloading, analyzing, and saving research papers.

- Introduces four core JSON-based commands: search, download, analyze, save
- Supports searching papers via Google Scholar and arXiv, with flexible parameters and output structure
- Enables PDF downloads using search results, with fine-grained ID selection and status reporting
- Integrates LLM-driven PDF content analysis, providing structured output for one or many papers
- Allows saving papers to Zotero collections, requiring user API credentials
- Features robust parameter validation, error handling, and documentation with usage examples