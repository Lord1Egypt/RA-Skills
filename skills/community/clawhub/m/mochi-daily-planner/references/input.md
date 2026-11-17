# Daily Planner and Review input contract

plan: date, availableMinutes 1..1440, tasks [{title,minutes 1..1440,priority 1..3}]. show: date. complete: date, taskId. rollover: from, to (later date), availableMinutes if target day is new. Rollover marks original open tasks deferred and copies them once. Mutations require requestId.

## Added in 1.1.0

New: add-task {date,title,minutes,priority}; revise {date,taskId,title?,minutes?,priority?}; schedule/export {date,start:"09:00",breakMinutes?:0..120,availableMinutes?:1..1440}. Priority 1 first; schedule is a local plan, not a calendar job. Exports and edits require requestId.

## Output files

daily-plan.md / time-blocks.csv

Exports create a new unique directory and return files [{path,bytes,sha256}]. Repeating the same requestId returns the same files; altered or missing saved exports raise an error. CSV output quotes fields and neutralizes spreadsheet formula prefixes. Keep other operations' active lock files in place. All files and records are scoped to the supplied active workspace.
