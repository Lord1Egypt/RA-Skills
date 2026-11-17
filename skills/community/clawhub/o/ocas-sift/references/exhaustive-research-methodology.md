# Exhaustive Research Methodology

When tasked with synthesizing or auditing a large collection of files (design systems, skill libraries, reference files):

## Rule: Consume Everything, Don't Sample

**Do NOT** read a few representative files and extrapolate. Read ALL files.

### Procedure
1. **List all files** first (`find`, `ls`, or tree output)
2. **Read every file** — don't stop at a "representative" subset
3. **Extract commonalities** across ALL files
4. **Note outliers** — files that break the pattern are important
5. **Cross-reference** — patterns in 90%+ = commonality; 100% = universal rule

### Anti-Pattern
- "I read a few files from each category" → WRONG
- "Read 5 of 72 brand files" → WRONG
- "Read all 272+ files and found 9 universal sections" → CORRECT

### Web Research Depth

Same principle applies to web research. Getting a page title or result snippet is not reading the page.

- "Found the manual name from manualslib" → WRONG (that's a pointer, not content)
- "Read the first result and summarized it" → Only correct if user asked for summary
- "Fetched 5+ pages, extracted full content, synthesized substance" → CORRECT for "exhaustive" requests

**Self-check before reporting:** Can I answer a detailed question about the source's actual content? If not, fetch more.

### For Very Large Collections (1000+ files)
Use `search_files` with targeted regex to find patterns across the full set without reading every file end-to-end. But always sample from ALL categories/sections.
