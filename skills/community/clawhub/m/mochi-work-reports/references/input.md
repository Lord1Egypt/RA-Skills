# Daily and Weekly Work Reports input contract

add: date, title, detail, status done|in-progress|blocked, evidence [source references], optional minutes 0..1440. report: from,to inclusive. Output includes selected records, grouped sections, recordedMinutes and recordsWithoutDuration. Add requires requestId.

## Added in 1.1.0

New: update {id,date?,title?,detail?,status?,evidence?,minutes?:0..1440|null}; import-csv {file} uses date,title,detail,status,evidence,minutes?,sourceId? (evidence separated by semicolon); export {from,to}. Conflicting imports under an existing sourceId are rejected. Updates retain prior values; period reports count the current event once. Writes/exports require requestId.

## Output files

work-report.md / work-records.csv

Exports create a new unique directory and return files [{path,bytes,sha256}]. Repeating the same requestId returns the same files; altered or missing saved exports raise an error. CSV output quotes fields and neutralizes spreadsheet formula prefixes. Keep other operations' active lock files in place. All files and records are scoped to the supplied active workspace.
