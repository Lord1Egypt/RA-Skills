# Reminders and Scheduled Tasks input contract

prepare: name, message, timezone (IANA), schedule {kind: at|cron|every, value}, delivery {agentId,channel,accountId,to}. at requires a future ISO timestamp with an offset; cron accepts five numeric fields. Returns a validated plan and CLI argument array. record: plan, receipt {jobId,enabled,nextRunAtMs,timezone,schedule,delivery}; normalize fields from the actual scheduler read-back. update-receipt: jobId, state enabled|disabled|removed, confirmedByScheduler true after verification. list reads saved receipts. Every mutation requires requestId.

## Added in 1.1.0

New actions: audit {jobs:[{jobId,enabled,nextRunAtMs,delivery}]}; record-delivery {jobId,receipt:{source:"native-scheduler",confirmedByScheduler:true,runId,state,finishedAt,evidence,delivery}}; export-calendar {jobId,durationMinutes?}. The native tool must supply audit/run receipts. Calendar copies support one-shot or simple daily/weekly/monthly fixed-time cron. Writes and exports require requestId.

## Output files

reminder.ics / receipt.md

Exports create a new unique directory and return files [{path,bytes,sha256}]. Repeating the same requestId returns the same files; altered or missing saved exports raise an error. CSV output quotes fields and neutralizes spreadsheet formula prefixes. Keep other operations' active lock files in place. All files and records are scoped to the supplied active workspace.
