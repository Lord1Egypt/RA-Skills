# Extraction schema

All fields shown are required. No extra command, URL-action or integration fields are accepted.

```json
{
  "schemaVersion": 1,
  "sourceSha256": "COPY_THE_ACTUAL_HASH_FROM_PREPARE",
  "language": "en",
  "title": "Project review",
  "summary": [],
  "decisions": [],
  "actions": [],
  "openQuestions": []
}
```

`language` is `en` or `zh-CN`. A summary, decision or open question item has:

```json
{"text":"A supported paraphrase.","quote":"Exact source excerpt.","evidence":["L0001"]}
```

An action has:

```json
{"task":"Send the draft","owner":"Maya","due":"2026-10-23","quote":"Maya will send the draft on 2026-10-23.","evidence":["L0002"]}
```

The examples describe a schema, not claims about the user's meeting. Each real quote must occur verbatim in the cited source lines. For multiple lines use consecutive IDs in source order; the quote may include the exact newline. Refer to at most12 lines per item. No line-ID duplication or fabricated quotation is accepted.

Use explicit JSON `null` for an unstated owner/date, not strings such as "unknown", an empty string or an assumed date. A real owner and ISO date must appear literally in the action's quote. This is necessary but not sufficient: the model must review the meaning before export.

Maximums: title160 characters, task/text800, quote2000;50 actions and30 items in each other array. Arrays may be empty. Do not insert output-format Markdown around the JSON. The file goes to the `draftFile` returned by prepare and must not overwrite the template/evidence.
