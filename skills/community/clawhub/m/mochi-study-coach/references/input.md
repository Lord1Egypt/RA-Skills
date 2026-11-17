# Study Coach and Mistake Review input contract

add: topic, question, answer, source, date. due: date, optional topic; answer and review history are omitted from due output. show: id. grade: id, date, grade 0..3, response, feedback. A low grade resets the interval; successful reviews extend it. Mutations require requestId.

## Added in 1.1.0

New: import-csv {file,date?} uses topic,question,answer,source,date? headers. stats {date,topic?}; export {date,topic?,includeAnswers?:false}. Duplicates match topic/question/source; conflicting answers are rejected. Stats count review attempts through the selected date; due dates reflect the current deck. Answers are hidden from due and exports unless explicitly requested. Writes/exports require requestId.

## Output files

review-plan.md / review-queue.csv

Exports create a new unique directory and return files [{path,bytes,sha256}]. Repeating the same requestId returns the same files; altered or missing saved exports raise an error. CSV output quotes fields and neutralizes spreadsheet formula prefixes. Keep other operations' active lock files in place. All files and records are scoped to the supplied active workspace.
