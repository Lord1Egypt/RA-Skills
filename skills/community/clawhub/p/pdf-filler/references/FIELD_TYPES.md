# Field type value contract

The `fill` script accepts a flat JSON object `{ "FieldName": value }`. The expected JSON value depends on the field's `type` from `extract.py` output.

## text

A string. Newlines (`\n`) are preserved when the field's `multiline` flag is true.

```json
{ "Full Name": "Ada Lovelace", "Notes": "line one\nline two" }
```

If `max_length` is set on the field, longer strings may be silently truncated by some backends.

## checkbox

A boolean (`true`/`false`) or any of the truthy strings `"true" | "1" | "yes" | "on" | "x" | "checked"`. Falsy strings or `false` set the field to its `Off` state.

```json
{ "I agree to terms": true, "Subscribe": "yes", "Optional": false }
```

The export value (e.g. `Yes`, `On`, `1`) is detected automatically from the field's appearance dictionary.

## radio

A string equal to one of the values listed in the field's `options` array. Use the exact export name reported by `extract.py`.

```json
{ "Salutation": "Mr", "Newsletter Frequency": "Weekly" }
```

## choice (dropdown / listbox)

A string equal to one of the entries in the field's `options` array. For multi-select listboxes, pass a single string for the first selected entry; multi-value support varies by backend.

```json
{ "Country": "Germany" }
```

## signature

Not auto-filled. The skill reports signature fields in the schema with `type: signature` but ignores them at fill time.

## pushbutton

Action triggers, not data fields. Skipped at fill time.

## unknown

Field type couldn't be classified. The orchestrator tries text-style filling and reports the field in `failed` if that doesn't take.
