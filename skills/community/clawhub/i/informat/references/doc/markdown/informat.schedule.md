<!-- DOCKEY: sch-8d5b2 -->
This document is the scheduled task documentation for the Informat low-code platform.

## Overview
A scheduled task is a preset task that executes a preset automation program or script at a specific time. For example, at 10:00 AM every day, query overdue tasks and send reminder emails.

The precision of scheduled tasks is 1 minute, meaning all scheduled tasks will have a delay of +(0 - 60 seconds) when executed.
## ScheduleDefine Definition

A ScheduleDefine corresponds to one scheduled task (Schedule / Job), used to trigger automation or script execution at specified times or intervals. Its definition structure is as follows:

```
{
  // =========================
  // Basic Information
  // =========================

  // Scheduled task name
  name: String,

  // Scheduled task type
  // Options:
  // - "default"  : Standard periodic scheduling
  // - "cron"     : Cron expression scheduling
  type: String,

  // Cron expression (effective when type = "cron")
  cron: String,


  // =========================
  // Invocation Method
  // =========================

  // Invocation type
  // Options:
  // - "script"    : Call script
  invokeType: String,

  // Script ID (when invokeType = "script")
  scriptId: String,        // @Ref(CallScript)

  // Script function name
  scriptFunc: String,


  // =========================
  // Scheduling Rules (non-cron)
  // =========================

  // Scheduling period type
  // Options:
  // - "day"       : Daily
  // - "week"      : Weekly
  // - "dualweek"  : Bi-weekly
  // - "month"     : Monthly
  // - "interval"  : Interval execution
  schedulePeriod: String,

  // List of days of the week for weekly scheduling (1-7, corresponding to Monday through Sunday)
  scheduleWeekList: List<Integer>,

  // List of days of the month for monthly scheduling (1-31)
  scheduleDayList: List<Integer>,

  // First trigger time
  scheduleTriggeredTime: Date,

  // Interval execution time (unit: minutes, only when schedulePeriod = "interval")
  scheduleInterval: int,

  // =========================
  // Execution Control
  // =========================

  // Whether to enable this scheduled task
  isEnable: boolean,



```

[Important Rules]
- All scriptId / scriptFunc referenced in ScheduleDefine must actually exist in the application. It is forbidden to reference scripts or functions that have not yet been created in the ScheduleDefine definition.
- All script functions must be explicitly exported using export function


## Trigger Types
In the Informat AI low-code platform, there are two main types of scheduled tasks:

- Default (periodic trigger): This type of scheduled task automatically triggers at preset periodic time intervals. For example, you can set a task to trigger every hour, every day, or every week.

- Cron expression: This type of scheduled task uses a Cron expression to define complex time scheduling rules. A Cron expression is a string format used to represent a schedule, allowing users to precisely define when a task triggers at specific time points or intervals.

## Examples

Default (periodic trigger):
Trigger a task at 1:00 AM every day.
Trigger a task at 8:00 AM every Monday.

Cron expression:

0 0 1 * * ?: Trigger a task at 1:00 AM every day.
0 0 8 ? * MON: Trigger a task at 8:00 AM every Monday.