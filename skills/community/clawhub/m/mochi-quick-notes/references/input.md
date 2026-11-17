# Quick Notes and Tasks input contract

add: kind note|task|idea, text, optional tags (max 3), due YYYY-MM-DD. list/search: optional status, kind; search requires query and performs literal normalized substring matching. complete/archive: id. Mutations require requestId. Archived records are retained and can be listed with status archived.

## Added in 1.1.0

New: update {id,text?,tags?,due?:YYYY-MM-DD|null}, reopen {id}, export accepts list filters. Filters: kind, status, exact tag, query, dueFrom,dueTo. Default excludes archived items. update retains history. Writes and exports require requestId.

## Output files

notes.md / notes.csv

Exports create a new unique directory and return files [{path,bytes,sha256}]. Repeating the same requestId returns the same files; altered or missing saved exports raise an error. CSV output quotes fields and neutralizes spreadsheet formula prefixes. Keep other operations' active lock files in place. All files and records are scoped to the supplied active workspace.
