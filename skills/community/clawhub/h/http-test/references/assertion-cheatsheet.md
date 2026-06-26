# Assertion Cheatsheet

Use this file as a fast lookup table. Keep the main skill flow short and use these snippets when writing or editing assertions.

## Status Code

```http
# expect.status = 200
```

Use this for transport-level success or failure expectations.

## Text Marker Exists

```http
# expect.contains = login_required
```

Use this for HTML, plain-text, or mixed responses where a marker matters more than JSON structure.

## Text Marker Must Not Exist

```http
# expect.not_contains = stacktrace
```

Use this for guarding against obvious error markers or debug output.

## JSON Field Equals

```http
# expect.json_path = data.status
# expect.equals = enabled
```

Use this when one business field decides pass or fail.

## JSON Path Exists

```http
# expect.exists = data.items[0].id
```

Use this when the precise value is not stable but the field must exist.

## JSON Path Is Absent

```http
# expect.absent = data.deprecatedField
```

Use this when a field should not be returned anymore.

## errno Equals

```http
# expect.errno = 0
```

Use this for APIs that expose an `errno` style field.

## errno Must Not Equal

```http
# expect.errno_not = 0
```

Use this when only a non-success errno matters.

## List Contains Value

```http
# expect.list_contains = data.items[].code:TARGET_CODE
```

Use this when the response is a list or a projected list field.

## List Must Not Contain Value

```http
# expect.list_not_contains = data.items[].code:REMOVED_CODE
```

Use this when absence is the business requirement.

## Save Raw Response

```http
# expect.save = tmp/case-1.response.json
```

Use this for debugging or when the user explicitly asks to preserve the raw payload.

## Print Key Fields

```http
# output.fields = code,message,data.id,data.status
```

Use this to surface a small set of diagnostic fields in the report.

## Common Mistakes

- `expect.json_path` requires valid JSON. Use `expect.contains` for non-JSON responses.
- `expect.equals` should be paired with `expect.json_path`.
- `expect.list_contains` and `expect.list_not_contains` use the format `<json path>:<expected value>`.
- Prefer a small set of stable business assertions. Full-response matching is usually too brittle.
