# Action contract

project.upsert: id,name,due optional YYYY-MM-DD. task.upsert: id,project,title,status todo|doing|done|cancelled,owner,due,dependencies existing same-project IDs,estimateHours0..10000,milestone optional. Cycles and completing before dependencies are rejected. task.remove:id refuses removal while depended on. list/report: project optional, today optional YYYY-MM-DD. report creates HTML/JSON/CSV and deadlines.ics (all-day deadlines, not notification schedules). State persists locally; operations are not messages to other people.

Reports remain local. Use the current model to interpret results; the executable tool performs the documented data operations.
