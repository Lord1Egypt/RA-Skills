# JSON — Encoding, Decoding, and the Silent Failures

## Always Pass Flags

```php
$data = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
$body = json_encode($payload, JSON_THROW_ON_ERROR | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
```

- `json_decode` returns `null` both for the valid input `"null"` and for a parse error. Without `JSON_THROW_ON_ERROR` (`php >=7.3`) you cannot distinguish them, and the alternative is `json_last_error() !== JSON_ERROR_NONE` on the line immediately after every call.
- `json_encode` returns `false` on failure — malformed UTF-8, `NAN`/`INF`, or a resource in the structure. Truthiness checks read that `false` as an empty body and clients receive a 200 with nothing in it.
- `JSON_THROW_ON_ERROR` raises `JsonException`, which is catchable and carries the reason (`errors.md`).

## Decoding

- Second argument `true` gives associative arrays; omitted, objects become `stdClass`. Pick one convention per codebase — mixing them produces `$row['id']` on an object and a fatal error at runtime.
- Depth defaults to 512 and counts nesting levels; exceeding it is `JSON_ERROR_DEPTH`, which without the throw flag looks exactly like invalid JSON.
- Big integers: any number above `PHP_INT_MAX` becomes a float and loses digits, which silently corrupts 64-bit IDs and Twitter-style snowflakes. `JSON_BIGINT_AS_STRING` keeps them as strings.
- Duplicate keys in the input: the last one wins, silently. If that matters for security (a signed payload with two `role` keys), validate the raw text before decoding.
- `json_validate($raw)` (`php >=8.3`) checks validity WITHOUT building the structure — the right tool for rejecting a 50 MB body before allocating it.
- Decoding does not validate your schema. Decode, then check the shape (array shapes in `static-analysis.md`, or a validator library); a missing key is `null` and travels a long way before failing.

## Encoding

| Flag | Effect | When |
|---|---|---|
| `JSON_THROW_ON_ERROR` | `JsonException` instead of `false` | Always |
| `JSON_UNESCAPED_SLASHES` | `/` stays `/` instead of `\/` | Always — the escaping is legacy and only bloats the payload |
| `JSON_UNESCAPED_UNICODE` | Emits UTF-8 instead of `\uXXXX` | Always for UTF-8 responses; smaller and readable |
| `JSON_PRESERVE_ZERO_FRACTION` | `1.0` stays `1.0` instead of becoming `1` | When the consumer distinguishes int from float |
| `JSON_PRETTY_PRINT` | Indented | Logs and files, never a hot API response |
| `JSON_HEX_TAG\|HEX_AMP\|HEX_APOS\|HEX_QUOT` | Escapes `<>&'"` | Embedding JSON inside an HTML `<script>` block (`security.md`) |
| `JSON_INVALID_UTF8_SUBSTITUTE` | Replaces bad bytes instead of failing | A last resort; find the encoding bug instead (`strings.md`) |
| `JSON_PARTIAL_OUTPUT_ON_ERROR` | Emits a truncated structure | Never in an API — it produces valid JSON with missing data |

- List vs object: a PHP array encodes as `[...]` only when its keys are `0..n-1` in order. `array_filter` leaves gaps, so a filtered list becomes `{"1":…,"3":…}` and the client's `.map()` throws. `array_values()` after every filter (`arrays.md`).
- Empty array is `[]`, and there is no way to make it `{}` except casting to an object or using `JSON_FORCE_OBJECT` (which affects the whole structure). An API field that is sometimes `[]` and sometimes `{}` is this bug.
- Objects: only PUBLIC properties are encoded. Implement `JsonSerializable::jsonSerialize()` to control the output explicitly — it is the only way to get private state, computed fields, or a stable field order.
- Backed enums encode to their scalar value automatically; a pure enum throws unless it implements `JsonSerializable` (`oop.md`).
- `DateTimeImmutable` encodes as an object with `date`, `timezone_type`, and `timezone` keys, which no consumer wants. Format it explicitly: `$d->format(DATE_ATOM)` inside `jsonSerialize()` (`datetime.md`).
- Floats are emitted using `serialize_precision`. At `-1` (the modern default) you get the shortest round-trip representation; at `17` you get `0.30000000000000004` in your API responses (`php-ini.md`, `types.md`).

## Large Payloads

- `json_decode` builds the entire structure in memory; a 200 MB document needs several times that. A streaming pull parser (the JSON Machine family) walks it with constant memory.
- Newline-delimited JSON (one object per line) is the pragmatic export format: `fgets` plus `json_decode` per line streams in both directions with no special library (`files.md`).
- Encoding a large collection: write to `php://output` incrementally — open the array bracket, encode each element, join with commas — rather than building one giant string (`http.md`).

## API Boundary Checklist

- Request: read from `php://input`, not `$_POST` (`http.md`); `json_validate` or decode with the throw flag; validate the shape; convert to typed objects once.
- Response: `Content-Type: application/json; charset=utf-8`; encode with the throw flag; `array_values()` on every list; explicit `jsonSerialize` on every object that leaves the process.
- Errors: a consistent error envelope with a machine-readable code, and never a raw exception message — those leak paths, SQL, and versions (`security.md`).

## Related

- Which array shapes encode as lists: `arrays.md`
- Encoding validity and mojibake: `strings.md`
- Sending and receiving the payloads: `http.md`
