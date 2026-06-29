---
name: map-reduce-llm
description: Structured Map-Reduce workflow for analyzing large documents with LLMs when the content exceeds the model's context window. Covers intelligent chunking strategies (including Linux split and Windows PowerShell equivalents), prompt templates, hierarchical and agentic variants, and quality control.
version: 1.0.0
tags: [llm, map-reduce, large-files, chunking, summarization, analysis, workflow, long-context]
---

# LLM Map-Reduce for Large Document Analysis

## When to Use
- The target document (or collection of documents) is too large for one context window.
- You need **global understanding** across the entire text (themes, cross-references, overall narrative, contradictions, or high-level insights).
- Common tasks: full-document summarization, theme extraction, key decision logging, comparative analysis, report generation, codebase architecture review.
- Pure RAG retrieval is insufficient because the task requires synthesis and reasoning across many parts of the document.
- You want a scalable, parallelizable, and auditable process that works with models of any context size.

For initial low-level reconnaissance (e.g., identifying structure, extracting specific patterns, or statistics), combine this pattern with traditional scripting tools (grep, awk, Python single-pass processing) as a preparatory step.

## Core Map-Reduce Pattern

1. **Chunk** — Split the document into manageable, semantically coherent pieces.
2. **Map** — Independently process each chunk (summarize, extract facts, answer sub-questions, or perform targeted analysis). These steps can run in parallel.
3. **Reduce** — Aggregate all Map outputs into one coherent final result (comprehensive summary, structured report, answers to questions, or synthesized insights).

### Variants
- **Basic Map-Reduce**: Single round of Map followed by one Reduce.
- **Hierarchical / Iterative Map-Reduce**: Perform Reduce on groups of Map outputs, then reduce the results again until everything fits comfortably in context. Excellent for extremely long documents.
- **LLM×MapReduce** (research-inspired): Add an explicit "Collapse" step that merges related or adjacent Map outputs before the final Reduce. Reduces information loss.
- **Agentic / Sub-Agent Map-Reduce**: The main agent plans and performs the final Reduce. It delegates Map work to isolated sub-agents (each with a clean context containing only its assigned chunk). Sub-agents return only structured results.
- **Map-Reduce + RAG**: Use vector retrieval to select only the most relevant chunks for the Map phase instead of processing every chunk.

## Phase 1: Preparation & Intelligent Chunking

**Avoid naive fixed-size splits** whenever the document has natural structure.

### Recommended Chunking Strategies (ranked)
1. **Structure-aware / Page-level** — Split by headings, chapters, sections, paragraphs, slides, or page breaks. Usually gives the best results.
2. **Recursive Character Splitter** (safe default)
   - Typical chunk size: 800–2000 tokens (tune based on your model and task).
   - Overlap: 100–300 tokens to preserve context across boundaries.
3. **Semantic Chunking** — Use embeddings to locate natural semantic boundaries.
4. **LLM-assisted Chunking** — Ask the model to suggest good split points with justifications.

### Checking File Type and Basic Properties (Important First Step)

Before deciding how to chunk a large file, always inspect its type and basic characteristics.

#### Linux

```bash
# Basic file type detection (strongly recommended to run first)
file big_document.txt
file -i big_document.txt          # Show MIME type + character encoding (e.g. utf-8, iso-8859-1, ascii)

# Brief output
file -b big_document.txt

# File size information
ls -lh big_document.txt           # Human-readable size
du -h big_document.txt
wc -c big_document.txt            # Total bytes
wc -l big_document.txt            # Total lines
wc -w big_document.txt            # Total words

# Peek at the beginning to determine if it is text or binary
head -c 200 big_document.txt | cat -A
```

#### Windows PowerShell

```powershell
# Basic file information
Get-Item "big_document.txt" | Select-Object Name, Length, Extension, LastWriteTime

# Show size in MB
(Get-Item "big_document.txt").Length / 1MB

# Line count (efficient for large files)
(Get-Content "big_document.txt" -ReadCount 0).Count

# Character encoding reference (PowerShell does not have a direct equivalent to file -i)
Get-Content "big_document.txt" -TotalCount 5 -Encoding UTF8   # Try different encodings

# Preview the beginning of the file
Get-Content "big_document.txt" -TotalCount 10

# Peek at raw bytes (to determine if it is a text file)
[System.IO.File]::ReadAllBytes("big_document.txt") | Select-Object -First 100 | Format-Hex
```

**Why this matters**
- Confirm that the file is actually a text file (not a PDF, compressed archive, database dump, etc.).
- Detect the character encoding to avoid garbled text when opening the file later in Python or PowerShell.
- Decide whether to split by lines or by bytes based on the file characteristics.

### Quick Chunking with Command-Line Tools

#### Linux

```bash
# 1. Split by number of lines (fastest and most common)
split -l 1000 -d --additional-suffix=.txt big_document.txt chunk_

# Result: chunk_00.txt, chunk_01.txt, chunk_02.txt ... (1000 lines each)

# 2. Split by approximate byte size
split -b 500K -d big_document.txt chunk_

# 3. Split using a pattern (more semantic, e.g. before every heading)
csplit -z -f section_ -b "%03d.txt" document.txt '/^## /' '{*}'

# Useful reconnaissance commands
wc -l big_document.txt
head -n 100 big_document.txt
tail -n 50 big_document.txt
```

#### Windows PowerShell

PowerShell does not have a built-in `split` command. The following scripts can be used to split large text files.

**Simple version (easier to read):**

```powershell
# Split by number of lines (1000 lines per chunk)
$inputFile = "big_document.txt"
$linesPerChunk = 1000
$baseName = "chunk"
$chunkIndex = 0
$currentChunk = @()

Get-Content $inputFile | ForEach-Object {
    $currentChunk += $_
    if ($currentChunk.Count -eq $linesPerChunk) {
        $currentChunk | Set-Content ("{0}_{1:D3}.txt" -f $baseName, $chunkIndex)
        $currentChunk = @()
        $chunkIndex++
    }
}

# Write any remaining lines
if ($currentChunk.Count -gt 0) {
    $currentChunk | Set-Content ("{0}_{1:D3}.txt" -f $baseName, $chunkIndex)
}
```

**More efficient version for very large files (uses StreamReader):**

```powershell
$inputFile = "big_document.txt"
$linesPerChunk = 1000
$reader = [System.IO.StreamReader]::new($inputFile)
$chunkIndex = 0
$lineCount = 0
$writer = $null

try {
    while (-not $reader.EndOfStream) {
        if ($lineCount % $linesPerChunk -eq 0) {
            if ($writer) { $writer.Dispose() }
            $writer = [System.IO.StreamWriter]::new("chunk_{0:D3}.txt" -f $chunkIndex)
            $chunkIndex++
        }
        $writer.WriteLine($reader.ReadLine())
        $lineCount++
    }
} finally {
    if ($writer) { $writer.Dispose() }
    $reader.Dispose()
}
```

**Recommendations**
- The Linux `split` command is very fast and simple, making it ideal for extremely large files.
- For PowerShell, the StreamReader/StreamWriter version is recommended for large files to avoid excessive memory usage.
- After splitting, it is often useful to run a follow-up Python or PowerShell script over the chunks to add overlap or perform light semantic cleaning.

Store all chunks and metadata in a dedicated run folder.

## Phase 2: Map Phase (Independent Processing)

Each chunk is processed in isolation with a narrowly scoped prompt.

### Recommended Map Prompt Template

```
You are an expert analyst. Carefully read the following document chunk.

CHUNK {chunk_id} of {total_chunks}
SOURCE METADATA: {optional_heading_or_location}

TASK:
{specific_map_task}

  Example tasks:
  - "Create a dense bullet-point summary of the main facts, decisions, arguments, and data points. Include speaker names and approximate timestamps if present."
  - "Extract all action items, owners, and deadlines mentioned."
  - "List key technical decisions and the rationale provided."

OUTPUT REQUIREMENTS (strict):
- Output ONLY in the requested format below.
- Every point must be self-contained.
- Reference the chunk ID where relevant.
- Do not add any text outside the required format.

DOCUMENT CHUNK:
{chunk_text}
```

### Map Phase Execution Options
- **Sequential**: Simple loop over chunks.
- **Parallel / Batched** (strongly recommended for large documents): Process multiple chunks simultaneously using whatever parallel mechanism your environment supports (sub-agents, thread pools, batch API calls, or distributed workers).
- Group related chunks together when there are clear dependencies.

**Critical best practice**: Force Map outputs to be highly structured (consistent bullet format, JSON, or key-value pairs). This makes the subsequent Reduce step dramatically more reliable and reduces hallucinations.

Save every Map result with its chunk ID for later reference.

## Phase 3: Reduce Phase (Synthesis)

This is where the model gains a global view by reading the distilled Map outputs.

### Recommended Reduce Prompt Template

```
You are a senior analyst synthesizing a very large document.

You have been given independent analysis results (Map outputs) from {total_chunks} chunks that together cover the entire source material.

OVERALL OBJECTIVE: {overall_goal_or_question}

INSTRUCTIONS:
1. Carefully review every Map output.
2. Produce a single coherent synthesis.
3. Explicitly call out connections, patterns, contradictions, or themes that appear across multiple chunks.
4. Clearly state when information is missing or conflicting.
5. Follow the exact output format requested.

MAP OUTPUTS:
{all_map_outputs_formatted_with_chunk_ids}

REQUIRED FINAL OUTPUT FORMAT:
{desired_final_structure}

  Example structure:
  - Executive Summary (200-400 words)
  - Key Themes and Insights (bulleted, with cross-chunk references)
  - Detailed Findings (organized by topic)
  - Open Questions and Limitations
  - Traceability: For each major claim, note the chunk IDs that support it
```

### Reduce Strategies
- **Single-pass Reduce**: When all Map outputs fit in context.
- **Hierarchical Reduce**: When there are too many Map results, first reduce them in groups (by section, topic, or randomly), then perform a final Reduce on the group-level summaries.
- **Iterative Refine**: Generate an initial Reduce, then feed it back along with selected original Map outputs for improvement.

## Phase 4: Quality Control & Iteration

After the Reduce step:
- Spot-check important claims by returning to the original chunks (or source document).
- If the synthesis feels weak, disconnected, or hallucinates links between chunks, improve the structure of Map outputs or insert a Collapse step.
- Consider running a focused second Map-Reduce pass on areas that need deeper analysis.

## Advanced Patterns

### 1. LLM×MapReduce Style
Map → structured Collapse (merge semantically related outputs) → Reduce. This intermediate step helps preserve relationships that would otherwise be lost.

### 2. Agentic / Sub-Agent Version (Most Powerful for Very Large Documents)
- Main agent handles planning, chunk selection strategy, and the final Reduce.
- Each Map task is delegated to a separate sub-agent that receives only its chunk + the Map prompt.
- Sub-agents return **only** the structured output (never the raw chunk text).
- This approach effectively gives you "unlimited" context because the main agent's context never contains the full document.

### 3. Map-Reduce Combined with Tools
During the Map phase, give agents access to additional tools (search within chunk, code execution, external lookup) so they can enrich the per-chunk analysis.

## Recommended General Workflow

1. Perform lightweight reconnaissance on the raw document (structure, format, length).
2. Choose a chunking strategy and persist chunks + metadata in a dedicated directory.
3. Design and test the Map prompt on a few sample chunks. Iterate until outputs are consistent and structured.
4. Execute the Map phase (parallel where possible).
5. Design the Reduce prompt with explicit instructions for cross-chunk reasoning.
6. Run Reduce (hierarchically if needed).
7. Validate key points against source chunks.
8. Produce final structured report + an index that links every conclusion back to source chunks.

Always keep intermediate artifacts (chunks, Map outputs, partial Reduces). This makes the process debuggable, resumable, and auditable.

## Prompt Engineering Best Practices
- Be extremely strict about output format in the Map prompt — this is usually the highest-leverage change.
- Tell each Map call its position (`chunk X of Y`) so the model can calibrate the scope of its output.
- In the Reduce prompt, explicitly ask the model to look for cross-chunk patterns and to flag uncertainty.
- Provide few-shot examples in both Map and Reduce prompts when the desired output format is complex.

## Common Pitfalls and Mitigations

| Pitfall                              | Mitigation |
|--------------------------------------|----------|
| Important ideas cut at chunk boundaries | Use overlap + structure-aware chunking |
| Map outputs are too long or inconsistent | Enforce strict length limits and exact formats (bullets or JSON) |
| Reduce step ignores some chunks      | Number chunks clearly and instruct the model to consider every Map output |
| Fabricated cross-chunk connections   | Require the Reduce output to cite specific chunk IDs for every claim |
| High token cost                      | Use a cheaper/faster model for the Map phase; reserve the strongest model for Reduce |
| Loss of important nuance             | Keep original chunks easily accessible so the final report can support drill-down |

## Typical Use Cases
- Summarizing long meeting transcripts, earnings calls, or interviews.
- Extracting insights and decisions from lengthy research papers, books, or technical reports.
- Analyzing large codebases for architectural patterns, debt, or design decisions (chunk by module or file).
- Synthesizing findings across a collection of related documents.
- Turning massive log files or benchmark outputs into high-level conclusions (after initial scripting-based filtering).

## Output Deliverables
Always produce at minimum:
1. A final structured report or answer set (Markdown or JSON).
2. An index or manifest that lists every chunk and its corresponding Map output.
3. Traceability information (ideally embedded in the final report) so readers can verify claims against the original source.

This pattern is training-free, works with any LLM, scales to documents of essentially arbitrary length (especially when using the sub-agent variant), and produces auditable results.

---

## Quick Start Checklist
- [ ] Document structure and length understood via reconnaissance
- [ ] Chunking strategy selected and chunks + metadata persisted
- [ ] Map prompt tested and producing consistent structured output on samples
- [ ] Reduce prompt written with clear cross-chunk reasoning instructions
- [ ] All intermediate results saved for auditability
- [ ] Final output includes traceability back to source chunks

This workflow is effective whenever you need to perform deep analysis or synthesis on text that does not fit in a single LLM context window.
