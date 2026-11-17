# Logging and Local Storage

Read this file only when the user asks to save, read, edit, summarize, or delete records.

## Default Behavior

- Do not persist data by default; complete the calculation or summary in the current conversation.
- “I ate …” supplies information but does not automatically authorize a file write.
- Before long-term tracking, show the proposed fields and exact path, then wait for confirmation.

Confirmation example:

```text
I can save date, meal, food, stated or estimated portion, calorie/nutrient estimates,
and optional meal feedback as local plaintext JSON under <current workspace>/nutrition-data/.
Programs and backups with access to that location may be able to read it. Save there?
```

## Minimal Schema

Save only requested fields:

```json
{
  "date": "YYYY-MM-DD",
  "meals": [
    {
      "id": "stable-id",
      "type": "breakfast|lunch|dinner|snack|other",
      "items": [
        {
          "name": "food name",
          "amount": "user supplied or explicitly estimated portion",
          "calories_estimate": 0
        }
      ],
      "feeling": null
    }
  ],
  "water_ml": null
}
```

Do not save a name, exact birth date, contact information, diagnosis, medication, menstrual dates, or other unnecessary sensitive data by default.

## Edit, Summarize, and Delete

- Before editing, identify the matched date, meal, and item; ask when ambiguous.
- In summaries, disclose missing dates and estimated entries. Do not treat missing data as zero intake.
- Immediately before deletion, repeat the exact target and get confirmation. Prefer one item or one day over a directory-wide deletion.
- Do not silently overwrite an existing file. Use a safe write strategy that preserves the original on failure.
