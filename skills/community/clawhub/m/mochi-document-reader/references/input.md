# Document Reading and Questions input contract

read/search: file (relative to current workspace), optional limit 1..200. read accepts start line. search requires query (literal normalized match). Supported text suffixes .txt .md .csv .tsv .json .log, UTF-8, up to 2 MiB. Output gives totalLines, matches, truncation and line-numbered text; long lines are flagged and truncated after 2000 characters.

## Added in 1.1.0

New: DOCX main-text support, extract {file}, search-many {files:[],queries:[],limit?}, export {files:[],queries?:[],start?,limit?}. DOCX <=10 MiB and body XML <=2 MiB; text <=2 MiB. At most 10 files, 8 queries, 200 returned lines per section and 2000 characters per line. extract/export require requestId. Citations are extracted lines, not DOCX pages.

## Output files

document.txt / source.json / evidence.md / citations.json

Exports create a new unique directory and return files [{path,bytes,sha256}]. Repeating the same requestId returns the same files; altered or missing saved exports raise an error. CSV output quotes fields and neutralizes spreadsheet formula prefixes. Keep other operations' active lock files in place. All files and records are scoped to the supplied active workspace.
