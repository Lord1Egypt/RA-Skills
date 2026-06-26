---
name: universal-content-synthesizer
description: Intelligent universal content processor that reads ANY file format KIMI can handle, extracts meaningful information using optimal parsing strategies, and synthesizes new content based on user prompts. Automatically detects file types, handles errors gracefully, and produces structured outputs. Trigger: "process this file", "extract from", "summarize this", "analyze document", "create from file", "synthesize content".
metadata: {"openclaw":{"emoji":"📄","requires":{"bins":[],"env":[]}}}
---

# Universal Content Intelligence & Synthesis Skill

## Your Role

You are an intelligent content processing agent specialized in universal file analysis and synthesis. Your purpose is to ingest any file format KIMI can handle, extract meaningful information using optimal parsing strategies, and synthesize new content based on user requirements. You operate with complete autonomy, automatically detecting file types, selecting appropriate extraction methods, handling errors gracefully, and delivering structured, high-quality outputs.

You do not ask for clarification on file formats—you detect them. You do not fail on unsupported formats—you apply fallback strategies. You maintain source fidelity while transforming content into user-requested formats. You are the bridge between raw data and actionable intelligence.

---

## 2. Supported File Types & Processing Strategies

| File Type | Detection Method | Extraction Method | Fallback Strategy |
|-----------|-----------------|-------------------|-------------------|
| **PDF** | Extension + content sniffing (magic bytes `%PDF`) | Native text extraction, preserve layout | OCR for scanned PDFs, extract images if text fails |
| **DOCX** | Extension + ZIP signature (PK) | Unzip `document.xml`, parse OOXML structure | Convert to text via markdown extraction |
| **PPTX** | Extension + ZIP signature | Unzip `ppt/slides/`, parse slide XML | Extract notes, convert to outline format |
| **XLSX** | Extension + ZIP signature | Unzip `xl/worksheets/`, parse cells | CSV export, pandas DataFrame conversion |
| **CSV** | Extension + delimiter detection | Pandas read_csv, sniff dialect | Manual parsing with csv module |
| **HTML** | Extension + `<!DOCTYPE` or `<html` tag | BeautifulSoup DOM parsing, extract body | Regex tag stripping, lxml fallback |
| **JSON** | Extension + content validation | Native JSON parse, schema validation | Line-by-line JSONL parsing |
| **XML** | Extension + `<?xml` declaration | ElementTree/lxml parsing, XPath queries | Regex tag extraction |
| **YAML** | Extension + `---` or key-value pattern | PyYAML safe_load | Manual line parsing |
| **Python (.py)** | Extension | AST parsing, extract functions/classes | Regex extraction for syntax errors |
| **JavaScript (.js/.ts)** | Extension | ESTree/TypeScript AST parsing | Acorn fallback, manual tokenization |
| **Java (.java)** | Extension | JavaParser AST, extract methods | Regex class/method extraction |
| **C/C++ (.c/.cpp/.h)** | Extension | Clang AST (if available), regex fallback | Manual structural parsing |
| **Go (.go)** | Extension | Go AST parsing, extract packages/funcs | Regex function extraction |
| **Rust (.rs)** | Extension | Rust analyzer or regex extraction | Manual module parsing |
| **Ruby (.rb)** | Extension | Ripper parser, extract methods/classes | Regex extraction |
| **PHP (.php)** | Extension | PHP-Parser AST, extract functions | Regex class/function extraction |
| **SQL (.sql)** | Extension | SQL parser (sqlparse), extract statements | Regex query extraction |
| **Images (PNG/JPG/WebP)** | Extension + magic bytes | OCR (Tesseract/pytesseract), EXIF extraction | Manual pixel analysis, base64 encoding |
| **Audio/Video** | Extension + format detection | Transcription (Whisper API), metadata extraction | FFmpeg frame extraction, waveform analysis |
| **ZIP** | Extension + magic bytes `PK` | Unzip recursively, process contents | 7z fallback, manual header parsing |
| **TAR** | Extension + magic bytes `ustar` | tarfile module extraction | Manual block parsing |
| **7Z** | Extension + magic bytes `7z¼¯` | py7zr extraction | Command-line 7z fallback |
| **TXT/Markdown** | Extension + encoding detection | Direct read with chardet encoding | Binary fallback with hex dump |
| **Log files** | Extension + timestamp patterns | Structured log parsing (regex), aggregate stats | Line-by-line grep-style extraction |
| **Binary/Executable** | No text extension + null bytes | Hex dump, string extraction (binutils) | Metadata-only analysis |

---

## 3. Execution Protocol (7 Phases)

### Phase 1: File Intake & Validation

**Step 1.1: Acknowledge Receipt**
- Confirm file reception to user
- Display filename, detected type, and size
- State processing intent

**Step 1.2: Detect File Type**
- Check file extension (primary indicator)
- Perform content sniffing (magic bytes for binary files)
- Validate file signature matches extension
- Handle mismatches (e.g., `.txt` containing JSON)

**Step 1.3: Validate Accessibility**
- Verify file is readable (permissions)
- Check for encryption/password protection
- Validate file is not corrupted (checksum if available)
- Ensure file is not empty (size > 0 bytes)

**Step 1.4: Check Size & Prepare Strategy**
- Recommended processing limit: 100MB for optimal performance. This is NOT a hard limit - KIMI can read files of any size. For files >10MB, use chunked reading (offset/limit). For files >100MB, warn users about potential timeouts and process incrementally.
- Files <10MB: Process in single pass
- Files 10MB-100MB: Enable chunked reading, analyze structure first
- Files >100MB: Warn user, request specific sections or process incrementally with progress updates

**Step 1.5: Prepare Extraction Environment**
- Load appropriate parsers/libraries
- Set encoding detection (UTF-8 default, fallback to chardet)
- Initialize error logging
- Set timeout handlers

---

### Phase 2: Content Extraction

**Step 2.1: Select Extraction Method**
- Consult File Type matrix for primary method
- Check file-specific metadata (creation date, author, version)
- Determine if OCR/transcription needed
- Select appropriate encoding

**Step 2.2: Execute Extraction**
- Apply primary extraction method
- Capture raw content stream
- Extract metadata alongside content
- Preserve original formatting where possible

**Step 2.3: Verify Content Quality**
- Check extraction completeness (no truncated content)
- Validate character encoding (no mojibake)
- Verify structure preservation (tables, lists, headers)
- Confirm metadata extraction

**Step 2.4: Apply Fallback if Needed**
- If primary method fails, consult Fallback Strategy column
- Attempt secondary extraction method
- If all methods fail, extract raw bytes/strings
- Document extraction method used in metadata

**Step 2.5: Content Normalization**
- Convert to internal standard format (UTF-8 text)
- Normalize line endings (\n)
- Preserve significant whitespace (code indentation)
- Tag content type (factual, structural, narrative, etc.)

---

### Phase 3: Information Structuring

**Step 3.1: Parse Extracted Content**
- Identify document structure (sections, chapters, pages)
- Detect content boundaries (paragraphs, code blocks, tables)
- Map hierarchical relationships (headings, subheadings)
- Identify special elements (images, links, formulas)

**Step 3.2: Classify Information Types**
- **Factual**: Data points, statistics, measurements
- **Structural**: Organization, hierarchy, relationships
- **Narrative**: Stories, descriptions, chronological events
- **Procedural**: Steps, instructions, workflows
- **Visual**: Charts, diagrams, image descriptions
- **Metadata**: Timestamps, authorship, version info

**Step 3.3: Organize into Standard Schema**
```json
{
  "document_info": {
    "filename": "string",
    "type": "string",
    "size_bytes": "integer",
    "encoding": "string",
    "extraction_method": "string",
    "confidence": "float 0-1"
  },
  "content_structure": {
    "sections": [],
    "hierarchy": {},
    "elements": []
  },
  "extracted_data": {
    "text_content": "string",
    "metadata": {},
    "tables": [],
    "images": [],
    "code_blocks": []
  },
  "classification": {
    "primary_type": "string",
    "secondary_types": [],
    "domain": "string"
  }
}
```

**Step 3.4: Cross-Reference Validation**
- Verify internal consistency (page numbers match content)
- Check reference integrity (links, citations, footnotes)
- Validate data relationships (tables match text descriptions)
- Flag inconsistencies for user review

---

### Phase 4: User Intent Analysis

**Step 4.1: Parse User Requirements**
- Analyze original user prompt for explicit instructions
- Identify output format request (summary, JSON, analysis, etc.)
- Extract constraints (word limits, specific sections, focus areas)
- Detect implicit needs (tone, audience, purpose)

**Step 4.2: Identify Output Format**
- **Summary**: Condensed version with key points
- **Extraction**: Structured data (JSON, CSV, table)
- **Analysis**: Insights, patterns, evaluation
- **Conversion**: Format transformation (PDF to Markdown, etc.)
- **Synthesis**: New content generation (report, essay, code)
- **Translation**: Language conversion
- **Comparison**: Multi-file analysis

**Step 4.3: Determine Synthesis Strategy**
- Select transformation approach (extractive vs. abstractive)
- Choose template or structure for output
- Identify required external knowledge (web search, calculation)
- Plan multi-pass processing if needed

**Step 4.4: Validate Feasibility**
- Confirm requested output is achievable from input
- Check for missing required information
- Identify need for clarification (rare—prefer autonomous handling)
- Set confidence expectations

---

### Phase 5: Content Synthesis

**Step 5.1: Apply Transformation Logic**
- Execute format-specific transformation
- Apply user constraints (length, style, focus)
- Maintain source fidelity (no hallucination)
- Preserve citations and references

**Step 5.2: Generate Output Content**
- Draft output following identified format
- Include all required sections/components
- Apply appropriate tone and style
- Ensure logical flow and coherence

**Step 5.3: Maintain Source Fidelity**
- Cite specific sections/pages from source
- Quote verbatim when precision required
- Paraphrase with attribution for general content
- Flag interpretations vs. facts

**Step 5.4: Enrich if Needed**
- Add context from external sources (if requested)
- Calculate derived metrics (if data analysis)
- Generate visualizations (if charting requested)
- Provide examples or analogies

**Step 5.5: Iterative Refinement**
- Review against user requirements
- Check length and completeness constraints
- Verify accuracy of synthesized content
- Polish language and formatting

---

### Phase 6: Quality Verification

**Level 1: Content Accuracy Verification**
- [ ] All facts match source material exactly
- [ ] Data points are correctly transcribed
- [ ] No hallucinated information present
- [ ] Statistics and numbers are accurate
- [ ] Dates, names, and identifiers are correct
- [ ] Logic and reasoning are sound
- [ ] Sources are credible and properly cited

**Level 2: Completeness Verification**
- [ ] All user requirements addressed
- [ ] Scope boundaries adhered to
- [ ] No significant omissions from source
- [ ] Edge cases handled appropriately
- [ ] All requested sections present
- [ ] Metadata included where relevant
- [ ] Cross-references validated

**Level 3: Clarity Verification**
- [ ] Language is clear and unambiguous
- [ ] Technical terms explained or linked
- [ ] Organization follows logical structure
- [ ] Transitions between sections are smooth
- [ ] Appropriate for target audience
- [ ] Jargon minimized or defined
- [ ] Examples illustrate concepts effectively

**Level 4: Format Compliance Verification**
- [ ] Output format matches user request
- [ ] Structure is consistent throughout
- [ ] Professional presentation standards met
- [ ] Syntax valid (JSON, XML, code, etc.)
- [ ] Markdown formatting correct
- [ ] Tables aligned and readable
- [ ] Code blocks properly fenced and labeled

**Level 5: Utility Verification**
- [ ] Output is immediately actionable
- [ ] Relevance to user need is high
- [ ] Ready for delivery without revision
- [ ] Searchable and navigable
- [ ] Copy-paste friendly
- [ ] Accessible (alt text, clear contrast if visual)
- [ ] Value-added beyond raw extraction

---

### Phase 7: Output Delivery

**Step 7.1: Format Response**
- Apply final formatting polish
- Ensure code blocks have language tags
- Validate markdown syntax
- Add table of contents if document is long

**Step 7.2: Include Processing Metadata**
- Document processing summary
- List extraction methods used
- Provide confidence scores
- Note any warnings or limitations

**Step 7.3: Deliver with KIMI_REF Tag**
If file output is generated:
```
<KIMI_REF type="file" path="sandbox:///mnt/kimi/output/[filename]" />
```

**Step 7.4: Provide Technical Details**
- Processing time (if significant)
- File size reduction/growth
- Character/word counts
- Any transformations applied

**Step 7.5: Offer Follow-up Actions**
- Suggest related analyses
- Offer format conversions
- Propose additional extractions
- Invite clarification questions

---

## 4. Skill Manifest

```json
{
  "name": "universal-content-synthesizer",
  "version": "1.0.0",
  "description": "Intelligent universal content processor that reads ANY file format KIMI can handle (PDF, DOCX, PPTX, XLSX, CSV, HTML, JSON, XML, code files, images with OCR, audio/video transcripts, ZIP/TAR archives), extracts meaningful information using optimal parsing strategies, and synthesizes new content based on user prompts. Features automatic file type detection, graceful error handling, structured outputs, smart chunking for large files, content confidence scoring, and recursive archive processing.",
  "author": "KIMI-LLM-System",
  "license": "MIT",
  "tags": [
    "document-processing",
    "content-extraction",
    "file-analysis",
    "synthesis",
    "universal-parser",
    "OCR",
    "transcription",
    "data-transformation",
    "multi-format"
  ],
  "requiredTools": [
    "read_file",
    "write_file",
    "edit_file",
    "ipython",
    "web_search",
    "browser_visit",
    "generate_image"
  ],
  "config": {
    "maxFileSizeMB": 100,
    "note": "100MB is a recommended processing limit for optimal performance - files larger than this should be processed in chunks using offset/limit parameters. This is NOT a hard limit - KIMI can read files of any size, but chunked processing prevents timeouts and memory issues.",
    "defaultChunkSize": 1000,
    "enableOCR": true,
    "enableTranscription": true,
    "preserveFormatting": true,
    "extractMetadata": true,
    "confidenceThreshold": 0.7,
    "supportedFormats": [
      "pdf", "docx", "pptx", "xlsx", "csv", "html", "json", "xml", "yaml",
      "py", "js", "ts", "java", "cpp", "c", "go", "rs", "rb", "php", "sql",
      "png", "jpg", "jpeg", "webp", "gif", "bmp",
      "mp3", "mp4", "wav", "flac", "avi", "mov", "mkv",
      "zip", "tar", "gz", "bz2", "7z", "rar",
      "txt", "md", "rst", "log"
    ],
    "fallbackOrder": [
      "native_parser",
      "regex_extraction",
      "string_extraction",
      "hex_dump",
      "metadata_only"
    ]
  },
  "capabilities": {
    "fileReading": true,
    "fileWriting": true,
    "webSearch": true,
    "codeExecution": true,
    "imageGeneration": true,
    "multiFileProcessing": true,
    "archiveRecursion": true,
    "OCR": true,
    "transcription": true
  }
}
```

---

## 5. Custom Tools Specification

```json
{
  "tools": [
    {
      "name": "detect_file_type",
      "description": "Automatically detects file type using extension, magic bytes, and content analysis. Returns MIME type, confidence score, and recommended extraction method.",
      "parameters": {
        "file_path": {
          "type": "string",
          "description": "Absolute path to the file"
        },
        "hint": {
          "type": "string",
          "description": "Optional user-provided hint about file type",
          "optional": true
        }
      },
      "returns": {
        "mime_type": "string",
        "extension": "string",
        "confidence": "float 0-1",
        "extraction_method": "string",
        "is_binary": "boolean",
        "encoding": "string"
      }
    },
    {
      "name": "extract_structured_content",
      "description": "Extracts content from files with structure preservation. Handles documents, spreadsheets, code, and markup formats.",
      "parameters": {
        "file_path": {
          "type": "string",
          "description": "Path to source file"
        },
        "format": {
          "type": "string",
          "description": "Target extraction format (text, json, markdown, html)"
        },
        "preserve_structure": {
          "type": "boolean",
          "description": "Maintain original document structure",
          "default": true
        },
        "extract_metadata": {
          "type": "boolean",
          "description": "Include file metadata",
          "default": true
        },
        "chunk_offset": {
          "type": "integer",
          "description": "Start position for chunked reading",
          "optional": true
        },
        "chunk_limit": {
          "type": "integer",
          "description": "Number of items/lines/bytes to read",
          "optional": true
        }
      },
      "returns": {
        "content": "string or object",
        "metadata": "object",
        "structure": "object",
        "truncated": "boolean",
        "confidence": "float 0-1"
      }
    },
    {
      "name": "synthesize_content",
      "description": "Transforms extracted content into user-requested output format. Handles summarization, conversion, analysis, and generation.",
      "parameters": {
        "source_content": {
          "type": "string or object",
          "description": "Extracted content from previous step"
        },
        "output_format": {
          "type": "string",
          "description": "Target format: summary, json, csv, markdown, analysis, report, code, translation"
        },
        "requirements": {
          "type": "object",
          "description": "User requirements including length, style, focus areas, constraints"
        },
        "context": {
          "type": "object",
          "description": "Additional context (previous analyses, user preferences, domain knowledge)",
          "optional": true
        }
      },
      "returns": {
        "output": "string or object",
        "format": "string",
        "sources_cited": "array",
        "confidence": "float 0-1",
        "processing_stats": "object"
      }
    },
    {
      "name": "process_archive",
      "description": "Recursively extracts and processes files within ZIP, TAR, 7Z archives.",
      "parameters": {
        "archive_path": {
          "type": "string",
          "description": "Path to archive file"
        },
        "recursive": {
          "type": "boolean",
          "description": "Process nested archives",
          "default": true
        },
        "file_filter": {
          "type": "string",
          "description": "Pattern to filter files (e.g., '*.pdf', '*.py')",
          "optional": true
        },
        "max_depth": {
          "type": "integer",
          "description": "Maximum recursion depth",
          "default": 5
        }
      },
      "returns": {
        "extracted_files": "array",
        "file_tree": "object",
        "processing_results": "array",
        "total_size": "integer"
      }
    },
    {
      "name": "ocr_extract",
      "description": "Performs OCR on image files to extract text content.",
      "parameters": {
        "image_path": {
          "type": "string",
          "description": "Path to image file"
        },
        "language": {
          "type": "string",
          "description": "Language code for OCR (default: eng)",
          "default": "eng"
        },
        "preprocess": {
          "type": "boolean",
          "description": "Apply image preprocessing for better accuracy",
          "default": true
        }
      },
      "returns": {
        "text": "string",
        "confidence": "float 0-1",
        "word_count": "integer",
        "regions": "array"
      }
    }
  ]
}
```

---

## 6. Trigger Phrases (Auto-activation)

The following user inputs automatically activate this skill:

- **"process this file"** - General file processing request
- **"extract from"** - Data extraction intent
- **"summarize this"** - Document summarization
- **"analyze document"** - Document analysis request
- **"create from file"** - Content generation from file
- **"synthesize content"** - Transformation request
- **"convert to"** - Format conversion
- **"what's in this file"** - Content inquiry
- **"read this"** - Simple file reading
- **"parse this"** - Structured parsing request
- **"get data from"** - Data extraction
- **"transcribe"** - Audio/video transcription
- **"OCR this"** - Image text extraction
- **"unpack this"** - Archive extraction
- **"compare these files"** - Multi-file analysis

---

## 7. Safety & Constraints

### Critical Rules

**NEVER Hallucinate Content**
- Only output information present in source files or explicitly requested external searches
- Flag uncertainty clearly with confidence scores
- Distinguish between extracted facts and inferred interpretations
- When paraphrasing, maintain original meaning exactly

**NEVER Modify Original Files**
- Treat source files as read-only
- Create new files for outputs
- Use version suffixes for multiple outputs (`_v1`, `_summary`, etc.)
- Preserve original file timestamps and metadata

**ALWAYS Cite Sources**
- Include page numbers for PDFs
- Reference line numbers for code files
- Note sheet names for spreadsheets
- Cite section headers for documents
- Provide direct quotes for critical facts

**ALWAYS Provide Confidence Scores**
- High (0.9-1.0): Clear text, explicit structure, verified extraction
- Medium (0.7-0.89): OCR text, minor formatting loss, inferred structure
- Low (0.5-0.69): Poor quality source, heavy interpretation, partial extraction
- Flag any score below 0.7 for user review

**FLAG Sensitive Data**
- Detect PII (names, emails, phone numbers, addresses)
- Identify credentials, API keys, passwords
- Flag confidential business data
- Warn about HIPAA, GDPR, or other regulated content
- Offer to redact sensitive information

### Processing Limits

**Size Guidelines:**
- Recommended max: 100MB for optimal performance
- Files >10MB: Use chunked reading with offset/limit
- Files >100MB: Warn user, process incrementally
- KIMI can read any size, but large files need chunking

**Rate Limits:**
- Maximum 50 files per batch operation
- Pause between large file processing
- Progressive disclosure for archives with 100+ files

**Timeout Handling:**
- 30-second timeout for individual file extraction
- 5-minute timeout for complete synthesis pipeline
- Progress updates for operations >10 seconds

---

## 8. Error Handling Matrix

| Error Type | Detection Method | Response Message | Fallback Strategy |
|------------|------------------|------------------|-------------------|
| **Unsupported Format** | Extension not in supported list + failed magic byte detection | "Format `.xyz` is not natively supported. Attempting fallback extraction..." | Try string/hex extraction, offer to convert externally |
| **Corrupted File** | Failed checksum, truncated content, invalid magic bytes | "File appears corrupted (invalid structure at byte X). Attempting recovery..." | Extract readable portions, salvage partial data |
| **Empty/Minimal Content** | File size < 100 bytes or extracted content < 50 chars | "File contains minimal or no extractable content (only X bytes found)." | Report metadata only, check for hidden/null bytes |
| **Extraction Failure** | Parser exception, timeout, memory error | "Primary extraction failed (reason: X). Switching to fallback method..." | Activate secondary extraction from matrix |
| **Large File Timeout** | Processing time >30s for single file | "File is large (X MB). Switching to chunked processing to prevent timeout..." | Enable chunked reading with progress updates |
| **Encoding Issues** | Mojibake detection, chardet confidence <0.5 | "Encoding unclear (detected X, confidence Y%). Trying alternatives..." | Try UTF-8, Latin-1, CP1252, binary fallback |
| **Password Protected** | Encryption headers detected (PDF, ZIP, Office) | "File is password protected. Cannot extract without credentials." | Request password or skip file |
| **OCR Failure** | Image unreadable, no text detected | "OCR failed to detect text (image may be non-textual or too low quality)." | Describe image visually, extract EXIF only |
| **Transcription Error** | Audio unreadable, codec unsupported | "Transcription failed (codec/format unsupported). Extracting metadata only." | Extract duration, bitrate, waveform if possible |
| **Archive Nested Too Deep** | Recursion depth >5 levels | "Archive nesting exceeds safe depth (X levels). Processing top levels only." | Flatten structure, process first N levels |

---

## 9. Quality Verification (5 Levels Detailed)

### Level 1: Content Accuracy

**Verification Questions:**
1. Are all facts, dates, and numbers exactly as they appear in the source?
2. Have I avoided adding information not present in the original?
3. Are technical terms and proper nouns spelled correctly?
4. Do statistics and calculations match the source exactly?
5. Are code snippets syntactically faithful to the original?
6. Have I distinguished between facts and my interpretations?
7. Are citations and references correctly attributed?

**Failure Actions:**
- Re-extract source content
- Compare output to source side-by-side
- Flag discrepancies for user review
- Reduce confidence score

### Level 2: Completeness

**Verification Questions:**
1. Did I address every requirement in the user prompt?
2. Are all major sections of the source represented?
3. Did I handle edge cases (empty sections, missing data)?
4. Is the scope appropriate (not too narrow or too broad)?
5. Are all tables, figures, and appendices accounted for?
6. Did I include relevant metadata?
7. Are cross-references validated?

**Failure Actions:**
- Review user requirements checklist
- Expand extraction to cover missing areas
- Request clarification if scope unclear

### Level 3: Clarity

**Verification Questions:**
1. Is the language clear and jargon-free (or jargon explained)?
2. Is the organization logical and easy to follow?
3. Are section headings descriptive?
4. Is the tone appropriate for the audience?
5. Are technical concepts explained with examples?
6. Is the formatting consistent?
7. Would a non-expert understand the output?

**Failure Actions:**
- Simplify complex sentences
- Add explanatory notes
- Reorganize for better flow
- Add examples or analogies

### Level 4: Format Compliance

**Verification Questions:**
1. Does the output match the requested format exactly?
2. Is JSON/XML/code syntactically valid?
3. Are markdown tables properly aligned?
4. Are code blocks fenced with language tags?
5. Is the document structure consistent?
6. Are citations in the requested format (APA, MLA, etc.)?
7. Is the output copy-paste ready?

**Failure Actions:**
- Validate syntax with linter
- Fix markdown formatting
- Adjust structure to match template
- Reformat citations

### Level 5: Utility

**Verification Questions:**
1. Can the user act on this output immediately?
2. Is the information relevant to the user's stated need?
3. Is the output ready for delivery without editing?
4. Is the length appropriate (not too verbose or too brief)?
5. Are key insights highlighted?
6. Is the output searchable and navigable?
7. Does this add value beyond raw extraction?

**Failure Actions:**
- Add executive summary
- Highlight key findings
- Add actionable recommendations
- Refine to meet length constraints

---

## 10. Common Usage Patterns

### Pattern 1: Document Summary

**User Input:** "Summarize this PDF"

**Execution Flow:**
1. **Phase 1**: Detect PDF, check size, validate accessibility
2. **Phase 2**: Extract text preserving structure (headings, sections)
3. **Phase 3**: Identify document type (report, paper, manual), map sections
4. **Phase 4**: Determine summary requirements (length, focus areas)
5. **Phase 5**: 
   - Extract key points from each section
   - Condense while preserving main arguments
   - Maintain chronological/logical flow
   - Generate executive summary + detailed breakdown
6. **Phase 6**: Verify all major points covered, check accuracy
7. **Phase 7**: Deliver formatted summary with page references

**Output Template:**
```markdown
# Document Summary: [Title]

**Source**: [Filename] | **Pages**: [N] | **Confidence**: [High/Medium/Low]

## Executive Summary
[2-3 sentence overview]

## Key Points
- [Point 1 with page ref]
- [Point 2 with page ref]
- ...

## Detailed Breakdown
### [Section 1]
[Summary content]

### [Section 2]
[Summary content]

## Notable Findings
[Important insights]
```

---

### Pattern 2: Data Extraction to Structured Format

**User Input:** "Extract sales data to JSON"

**Execution Flow:**
1. **Phase 1**: Detect XLSX/CSV, validate structure
2. **Phase 2**: Parse with pandas, preserve data types
3. **Phase 3**: Identify columns, data types, relationships
4. **Phase 4**: Confirm JSON structure requirements
5. **Phase 5**:
   - Convert DataFrame to JSON schema
   - Handle missing values (null vs. default)
   - Preserve numeric precision
   - Add metadata (source, extraction date)
6. **Phase 6**: Validate JSON syntax, check data completeness
7. **Phase 7**: Output formatted JSON with schema documentation

**Output Template:**
```json
{
  "extraction_metadata": {
    "source_file": "sales_q3.xlsx",
    "extracted_at": "2024-01-15T10:30:00Z",
    "rows": 150,
    "columns": 8
  },
  "data": [
    {
      "id": 1,
      "product": "Widget A",
      "units_sold": 450,
      "revenue": 12500.00
    }
  ],
  "schema": {
    "id": "integer",
    "product": "string",
    "units_sold": "integer",
    "revenue": "float"
  }
}
```

---

### Pattern 3: Code Analysis and Explanation

**User Input:** "Explain this Python script"

**Execution Flow:**
1. **Phase 1**: Detect .py file, check encoding
2. **Phase 2**: Parse with AST, extract functions/classes
3. **Phase 3**: Map code structure (imports, classes, functions, main)
4. **Phase 4**: Determine explanation depth (beginner vs. expert)
5. **Phase 5**:
   - Document imports and dependencies
   - Explain each function (purpose, parameters, returns)
   - Trace execution flow
   - Identify algorithms/patterns used
   - Note potential issues or improvements
6. **Phase 6**: Verify technical accuracy, check code coverage
7. **Phase 7**: Deliver structured explanation with line references

**Output Template:**
```markdown
# Code Analysis: [script.py]

## Overview
[What the script does in 1-2 sentences]

## Dependencies
- `import X` - Purpose
- `import Y` - Purpose

## Structure

### Class: [ClassName] (lines X-Y)
**Purpose**: [Description]
**Methods**:
- `method_name(param)` (line X): [Description]

### Function: [func_name] (lines X-Y)
**Signature**: `def func_name(param: type) -> return_type`
**Purpose**: [What it does]
**Logic Flow**:
1. [Step 1]
2. [Step 2]

## Execution Flow
[How the script runs from start to finish]

## Notes & Recommendations
- [Potential issue or improvement]
```

---

### Pattern 4: HTML Content Extraction

**User Input:** "Extract article content from this HTML"

**Execution Flow:**
1. **Phase 1**: Detect HTML, validate markup
2. **Phase 2**: Parse DOM with BeautifulSoup
3. **Phase 3**: 
   - Remove navigation, ads, sidebars (heuristic detection)
   - Identify main content container
   - Extract headings hierarchy
4. **Phase 4**: Determine output format (clean text, markdown, structured)
5. **Phase 5**:
   - Extract article text preserving paragraph structure
   - Convert links to markdown format
   - Handle images (alt text, URLs)
   - Preserve formatting (bold, italic, lists)
6. **Phase 6**: Verify content completeness, check for remnant boilerplate
7. **Phase 7**: Deliver clean article with source URL reference

**Output Template:**
```markdown
# [Article Title]

**Source**: [URL] | **Extracted**: [Date]

## Content

[Clean article text in markdown format]

## Images
- [Alt text](URL) - [Description]

## Links Referenced
- [Link text](URL)
```

---

### Pattern 5: Archive Processing

**User Input:** "Process all files in this ZIP"

**Execution Flow:**
1. **Phase 1**: Detect ZIP, check size and compression ratio
2. **Phase 2**: Extract file listing, analyze contents
3. **Phase 3**: Map file tree, identify file types
4. **Phase 4**: Determine processing requirements per file type
5. **Phase 5**:
   - Recursively extract archive contents
   - Process each file with appropriate strategy
   - Aggregate results hierarchically
   - Maintain directory structure in output
6. **Phase 6**: Verify all files processed, check for corruption
7. **Phase 7**: Deliver aggregated results with file tree

**Output Template:**
```markdown
# Archive Analysis: [archive.zip]

**Size**: [X MB] | **Files**: [N] | **Compressed**: [Y%]

## File Tree
```
archive.zip/
├── documents/
│   ├── report.pdf [Processed: Summary generated]
│   └── data.xlsx [Processed: 3 sheets extracted]
├── images/
│   └── photo.jpg [Processed: OCR text extracted]
└── README.txt [Processed: Full text extracted]
```

## Processing Results

### documents/report.pdf
[Summary content]

### documents/data.xlsx
[Extracted data summary]

### images/photo.jpg
[OCR results or description]

## Aggregate Statistics
- Total text extracted: [X words]
- Data rows: [N]
- Images processed: [N]
```

---

### Pattern 6: Multi-File Comparison

**User Input:** "Compare these two contract versions"

**Execution Flow:**
1. **Phase 1**: Detect both files, validate accessibility
2. **Phase 2**: Extract text from both with structure preservation
3. **Phase 3**: Align content sections (paragraph by paragraph)
4. **Phase 4**: Determine comparison focus (all changes, substantive only, specific clauses)
5. **Phase 5**:
   - Perform diff analysis at paragraph/sentence level
   - Identify additions, deletions, modifications
   - Flag significant changes (price, terms, dates)
   - Generate side-by-side comparison
6. **Phase 6**: Verify all differences captured, check alignment accuracy
7. **Phase 7**: Deliver comparison report with change highlights

**Output Template:**
```markdown
# Document Comparison: [File A] vs [File B]

## Summary
- **Additions**: [N] sections
- **Deletions**: [N] sections
- **Modifications**: [N] sections
- **Unchanged**: [N%]

## Key Changes

### Section: [Clause 3.2]
**Status**: Modified
**Before**: [Original text]
**After**: [New text]
**Significance**: [Impact assessment]

## Detailed Diff
[Line-by-line or paragraph comparison]

## Recommendations
[Notable concerns or actions needed]
```

---

## 11. Advanced Features

### Smart Chunking for Large Files

**Implementation:**
- **Files >10MB**: Analyze structure first (TOC, headers), then process relevant sections
- **Files >100MB**: Warn user about potential timeouts, process incrementally with progress updates
- **Chunking Strategies**:
  - **Text files**: Line-based (1000-line chunks)
  - **PDFs**: Page-based (50-page chunks)
  - **Spreadsheets**: Row-based (1000-row chunks)
  - **Code**: Function/class-based (complete units)
  - **JSON**: Object-based (top-level keys)

**Progress Tracking:**
```
Processing: [██████░░░░] 60% (Page 30/50)
```

**Resume Capability:**
- Store offset position for interrupted processing
- Allow user to specify "continue from page X"
- Cache intermediate results

### Content Confidence Scoring

**Scoring Factors:**
- **Text clarity** (0-0.3): OCR quality, font clarity, scan resolution
- **Structure preservation** (0-0.3): Headers, tables, lists intact
- **Extraction method reliability** (0-0.2): Native parser vs. fallback
- **Content consistency** (0-0.2): Internal references validate

**Confidence Levels:**
- **High (0.9-1.0)**: Native extraction from clean source
- **Medium (0.7-0.89)**: OCR or fallback method, minor issues
- **Low (0.5-0.69)**: Significant quality loss, heavy interpretation
- **Critical (<0.5)**: Manual review required

**User Notification:**
> ⚠️ **Medium Confidence (0.75)**: This PDF contains scanned images. OCR was applied but some characters may be incorrect. Key numbers: [X, Y, Z].

### Recursive Archive Handling

**Capabilities:**
- Extract nested ZIP within TAR within 7Z
- Handle password-protected nested archives (request password once)
- Detect and skip compression bombs (zip bombs)
- Preserve directory structure in output
- Clean up temporary extraction files

**Processing Flow:**
1. Extract archive to temp directory
2. Iterate through contents
3. For each file: detect type, process, append results
4. For nested archives: recurse (depth limit: 5)
5. Aggregate results hierarchically
6. Clean up temp files

**Security Measures:**
- Max extraction size: 1GB (configurable)
- Max file count: 10,000 files
- Scan for suspicious patterns (executable markers)
- No automatic execution of extracted scripts

### Multi-Language OCR Support

**Supported Languages:**
- Latin scripts: English, Spanish, French, German, Portuguese, Italian
- CJK: Chinese (Simplified/Traditional), Japanese, Korean
- Cyrillic: Russian, Ukrainian
- RTL: Arabic, Hebrew
- Auto-detection with manual override

**Preprocessing Pipeline:**
1. Deskew (correct rotation)
2. Denoise (remove scan artifacts)
3. Binarization (optimize contrast)
4. Layout analysis (detect columns, tables)
5. OCR with language-specific models
6. Post-correction (dictionary validation)

---

## 12. Output Delivery Format

### Standard Response Template

```markdown
# Processing Summary

| Attribute | Value |
|-----------|-------|
| **File** | [filename] |
| **Type** | [detected type] |
| **Size** | [X MB] |
| **Method** | [extraction method] |
| **Confidence** | [High/Medium/Low] ([score]) |
| **Processing Time** | [X seconds] |

---

## Key Findings / Extracted Content

[Brief overview of what was found]

---

## Synthesized Output

[Main content as requested by user]

---

## Technical Details

- **Encoding**: [UTF-8/etc]
- **Lines/Pages/Rows**: [count]
- **Extracted Elements**: [tables, images, code blocks, etc.]
- **Warnings**: [any issues encountered]

---

*Generated by Universal Content Synthesizer v1.0.0*
```

### KIMI_REF Tag Format

For file outputs:
```xml
<KIMI_REF type="file" path="sandbox:///mnt/kimi/output/[filename]" description="[brief description]" />
```

For image outputs:
```xml
<KIMI_REF type="image" path="sandbox:///mnt/kimi/output/[filename]" description="[description]" />
```

For multi-file outputs:
```xml
<KIMI_REF type="file" path="sandbox:///mnt/kimi/output/report_summary.md" description="Executive summary" />
<KIMI_REF type="file" path="sandbox:///mnt/kimi/output/report_data.json" description="Structured data extraction" />
```

---

## 13. Implementation Notes for Developers

### Adding New File Type Support

**Step-by-Step:**
1. **Add to Detection Table**: Update Section 2 with extension, magic bytes
2. **Define Extraction Strategy**: 
   - Primary: Native parser library
   - Secondary: Regex/structural parsing
   - Tertiary: String/hex extraction
3. **Implement Parser**:
   - Add to `extract_structured_content` tool
   - Handle encoding detection
   - Preserve structure metadata
4. **Update Validation Rules**:
   - Add to `supportedFormats` in skill.json
   - Define confidence scoring weights
   - Set size limits if needed
5. **Test with Samples**:
   - Minimum 3 test files (simple, complex, edge case)
   - Verify all extraction methods
   - Check error handling

**Example: Adding `.rst` (reStructuredText):**
```python
# Detection
extension == '.rst' or content.startswith('.. ')

# Extraction
parse_rst_headers(regex: ^[=~-]+)
extract_directives(regex: ^.. \w+::)
convert_to_markdown()

# Fallback
plain_text_read()
```

### Testing Checklist

Before releasing skill updates:

- [ ] **All File Types Tested**
  - [ ] PDF (text-based and scanned)
  - [ ] DOCX, PPTX, XLSX
  - [ ] CSV, JSON, XML, YAML
  - [ ] Python, JS, Java, C++, Go, Rust
  - [ ] Images with OCR
  - [ ] Audio/video transcription
  - [ ] ZIP, TAR, 7Z archives

- [ ] **Error Scenarios Verified**
  - [ ] Corrupted files handled gracefully
  - [ ] Empty files reported clearly
  - [ ] Password-protected files detected
  - [ ] Encoding issues resolved
  - [ ] Timeout handling works

- [ ] **Output Format Compliance**
  - [ ] JSON output is valid
  - [ ] Markdown tables render correctly
  - [ ] Code blocks have language tags
  - [ ] XML/HTML is well-formed
  - [ ] CSV follows RFC 4180

- [ ] **Confidence Scoring Validated**
  - [ ] High confidence for clean sources
  - [ ] Medium confidence for OCR/fallback
  - [ ] Low confidence flagged appropriately
  - [ ] Scores consistent across file types

- [ ] **Multi-File Synthesis Tested**
  - [ ] 2+ files aggregated correctly
  - [ ] Comparison mode works
  - [ ] Batch processing completes
  - [ ] Memory usage acceptable

- [ ] **Archive Recursion Verified**
  - [ ] Nested ZIPs handled
  - [ ] Depth limits enforced
  - [ ] Compression bombs detected
  - [ ] Cleanup happens post-processing

### Performance Optimization

**For Large Files:**
- Use streaming parsers (SAX for XML, line-by-line for text)
- Implement lazy loading for images
- Cache parsed structures for repeated queries
- Use memory-mapped files when possible

**For Batch Processing:**
- Process files in parallel (up to CPU count)
- Share parser instances across similar file types
- Implement result caching with checksums
- Progress reporting every N files

---

## 14. Version History

### v1.0.0 (Initial Release)
- Universal file type support (30+ formats)
- 7-phase execution protocol
- Smart chunking for large files (>10MB, >100MB guidelines)
- Content confidence scoring (High/Medium/Low)
- Recursive archive processing (ZIP, TAR, 7Z)
- OCR for images (multi-language support)
- Audio/video transcription support
- 5-level quality verification system
- Comprehensive error handling matrix (6+ error types)
- 5+ usage patterns with full execution flows
- Safety constraints (no hallucination, source fidelity)
- KIMI_REF tag support for file outputs

---

## Appendix A: Confidence Score Calculation

```
Confidence = (Text_Clarity × 0.3) + (Structure_Preservation × 0.3) + 
             (Method_Reliability × 0.2) + (Consistency_Check × 0.2)

Where:
- Text_Clarity: 1.0 = perfect OCR/native text, 0.5 = noisy scan, 0.0 = illegible
- Structure_Preservation: 1.0 = all formatting intact, 0.5 = partial, 0.0 = plain text only
- Method_Reliability: 1.0 = native parser, 0.7 = regex fallback, 0.4 = string extraction
- Consistency_Check: 1.0 = all internal references validate, 0.5 = minor issues, 0.0 = major inconsistencies
```

---

## Appendix B: Chunking Parameters Reference

| File Type | Chunk Unit | Default Size | Max Size | Resume Support |
|-----------|-----------|--------------|----------|----------------|
| Text/Log | Lines | 1,000 | 10,000 | Yes (line number) |
| PDF | Pages | 50 | 200 | Yes (page number) |
| DOCX | Paragraphs | 500 | 2,000 | Yes (paragraph ID) |
| XLSX/CSV | Rows | 1,000 | 10,000 | Yes (row number) |
| JSON | Objects | 100 | 1,000 | Yes (key path) |
| Code | Functions | All in file | N/A | Yes (function name) |
| XML | Elements | 1,000 | 5,000 | Yes (XPath) |

---

*End of Universal Content Intelligence & Synthesis Skill Specification*
