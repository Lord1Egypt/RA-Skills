# Pre-Flight Flush

You are doing a lightweight pre-flight memory flush before Lucid's nightly review.

Goal: make sure Lucid's input files are current before the 03:00 run.

Important timing detail:
- This runs at 02:45 Vienna time
- At that point, the calendar date has already rolled over
- Lucid's nightly review still needs **yesterday's** daily file as the main source for the prior day
- If there has been any after-midnight activity, a **today** file may also exist and should be updated if needed

Be conservative:
- Only write factual things supported by files you can read
- Do not speculate, infer motives, or invent missing details
- Do not rewrite or remove existing content unless you are creating a missing file from scratch
- If a file already has content, append only genuinely new information
- Avoid duplicates and near-duplicates

## Steps

1. Get Vienna dates.

   On Linux:
   ```bash
   YESTERDAY=$(TZ=Europe/Vienna date -d yesterday +%Y-%m-%d)
   TODAY=$(TZ=Europe/Vienna date +%Y-%m-%d)
   ```

   On macOS:
   ```bash
   YESTERDAY=$(TZ=Europe/Vienna date -v-1d +%Y-%m-%d)
   TODAY=$(TZ=Europe/Vienna date +%Y-%m-%d)
   ```

2. Read yesterday's daily file if it exists:
   ```bash
   cat memory/$YESTERDAY.md 2>/dev/null
   ```

3. Check whether a today's file already exists from after-midnight activity:
   ```bash
   cat memory/$TODAY.md 2>/dev/null
   ```

4. Read recent session context from `memory/` and check what was written recently. Prefer factual sources created or updated late in the day or after midnight.

5. Treat **yesterday's file** as the primary target.
   - Determine whether `memory/$YESTERDAY.md` is missing or sparse.
   - Treat it as sparse if it has fewer than 200 characters of meaningful content.

6. For `memory/$YESTERDAY.md`:
   - If missing or sparse, write a basic factual summary of what is known about yesterday from available sources.
   - If it already has meaningful content, append only new context not already covered.
   - Preserve existing content exactly; use append mode only when adding to an existing file.

7. For `memory/$TODAY.md`:
   - Only touch it if the file already exists.
   - If it exists, append only factual after-midnight context that is not already covered.
   - Do not create a new today file just because the date rolled over.

## Output rules

- Yesterday's file is the main target Lucid needs for the 03:00 run.
- Today's file is optional and only updated if it already exists.
- Do not touch other memory files unless needed as read-only sources.
- Do not overwrite an existing non-sparse daily file.
- If there is nothing new to add, leave the file unchanged.
- Reply `NO_REPLY` when done.
