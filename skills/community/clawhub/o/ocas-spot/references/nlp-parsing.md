# NLP Parameter Extraction

Extract structured parameters from natural language before calling any command:

| Input pattern | Extracted value |
|---|---|
| "for 2", "party of 4", "table for two" | `party_size` |
| "this Saturday", "next weekend", "March 9" | specific date(s) |
| "in May", "next month", "next 30 days" | `date_range` |
| "Saturdays in May", "weekends in June" | date list (Sat/Sun of that month) |
| "dinner", "prime time", "evening" | `time_window: 18:00-22:00` |
| "lunch" | `time_window: 11:30-14:00` |
| "6-9pm", "7:30 to 9" | explicit `time_window` |
| "monitor", "watch", "alert me when", "notify me" | → `spot.watch.add` |
| "book me", "reserve" | → `spot.book` (after check) |
| "check", "is there availability", "any tables" | → `spot.check` |

When `time_window` is extracted, filter returned times to that window before presenting results. Resolve ambiguous date language ("next Saturday") against today's date before calling any script.