---
name: Schema Sleuth
description: Infer clean, production-ready schemas from messy sample data. Paste 1-5 examples of any data format — JSON, CSV, API responses, plain text, LLM output — and get back a Pydantic model, Zod schema, TypeScript interface, JSON Schema, and/or Go struct with correct types, nullability, optional fields, and validation rules inferred from the samples. Also detects dates, UUIDs, emails, URLs, enums, and nested objects. Zero external API required — pure inference. Triggers on "infer schema", "generate schema", "generate types", "pydantic from json", "zod from json", "typescript interface from", "what's the schema for", "/schema-sleuth".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - schema
    - pydantic
    - zod
    - typescript
    - json-schema
    - go
    - data-modeling
    - type-inference
    - developer-tools
    - api-integration
---

# Schema Sleuth

Paste raw sample data — any format, any messiness — and get production-ready schemas in every language you need. No manual typing, no guessing nullability, no forgetting nested objects.

**Supports: Pydantic v2, Zod, TypeScript interfaces, JSON Schema Draft 7, Go structs. Zero config.**

---

## Trigger Phrases

- "infer schema", "generate schema", "generate types", "what's the schema for this"
- "pydantic from json", "zod from json", "zod from this", "typescript interface from"
- "generate pydantic model", "generate zod schema", "type this response"
- "model this data", "schema from sample", "parse this data format"
- "/schema-sleuth"

---

## How to Provide Input

```
# Option 1: Paste raw JSON (one example)
/schema-sleuth
{"id": 42, "name": "Alice", "email": "alice@example.com", "role": null}

# Option 2: Multiple examples for better inference
/schema-sleuth
Sample 1: {"id": 1, "status": "active", "score": 98.5}
Sample 2: {"id": 2, "status": "inactive", "score": null}
Sample 3: {"id": 3, "status": "pending", "score": 72.0}

# Option 3: CSV data
/schema-sleuth
user_id,name,email,created_at,is_premium
1,Alice,alice@ex.com,2024-01-15,true
2,Bob,,2024-02-01,false
3,Carol,carol@ex.com,,true

# Option 4: Specify output format
/schema-sleuth --output pydantic,zod
{"id": "uuid-here", "payload": {"action": "click", "timestamp": 1710000000}}

# Option 5: Named schema
/schema-sleuth --name UserEvent
{"user_id": 123, "event": "purchase", "amount": 49.99}
```

---

## Step 1: Normalize the Input

Before inferring types, standardize the input:

1. **Detect format**: Is it JSON, JSON array, NDJSON, CSV, TSV, YAML, or plain key-value text?
2. **Parse all samples**: If multiple samples provided, parse each one separately
3. **Build a field inventory**: For each field seen across ALL samples, track every value observed

```
Field: "score"
  Values seen: 98.5, null, 72.0
  → Type: float | null (nullable float)
  → Not always present: check if all samples have it

Field: "status"
  Values seen: "active", "inactive", "pending"
  → Type: string — but all values are from a fixed set → candidate ENUM
  → Enum candidates: active | inactive | pending
```

---

## Step 2: Infer Types with Pattern Detection

For each field, determine the most specific type:

### Primitive Type Rules

| Observed Values | Inferred Type | Notes |
|----------------|--------------|-------|
| `true` / `false` | `bool` | |
| `42`, `100` (all integers) | `int` | |
| `3.14`, `98.5` (any float) | `float` | Promote if mixed int+float |
| `"hello"` (generic string) | `str` / `string` | |
| `null` anywhere | Mark field as `Optional` / nullable | |
| Field missing in some samples | Mark as `Optional` | |
| Both `null` and missing | `Optional` with default `None` |  |

### Semantic Pattern Detection (look at string values)

| Pattern | Detected Type | Validation |
|---------|--------------|-----------|
| `"2024-01-15"` | `date` | ISO 8601 date |
| `"2024-01-15T10:30:00Z"` | `datetime` | ISO 8601 datetime |
| `1710000000` (10-digit int) | `unix_timestamp` | Note: could be POSIX ts |
| `"alice@example.com"` | `email` | Apply EmailStr / z.string().email() |
| `"https://..."` / `"http://..."` | `url` | Apply AnyUrl / z.string().url() |
| `"550e8400-e29b-41d4-..."` | `uuid` | UUID v4 format |
| Repeated values, ≤ 8 distinct in 5+ samples | `enum` | List all values as literals |
| `"#FF5733"` | `hex_color` | String with pattern |
| All values positive integers | Consider `PositiveInt` | |

### Nested Object Detection

```json
{"user": {"id": 1, "name": "Alice"}, "timestamp": "2024-01-01T00:00:00Z"}
```
→ `user` field is a nested object → create a sub-model `User` / `z.object()`

### Array Detection

```json
{"tags": ["python", "api", "backend"], "scores": [98.5, 72.0]}
```
→ `tags`: `list[str]` / `z.array(z.string())`
→ `scores`: `list[float]` / `z.array(z.number())`

---

## Step 3: Generate Schemas

Generate all requested output formats. Default: Pydantic + Zod + TypeScript interface.

### Pydantic v2 (Python)

```python
from pydantic import BaseModel, EmailStr, AnyUrl
from typing import Optional
from datetime import datetime
from enum import Enum
from uuid import UUID

class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    pending = "pending"

class UserEvent(BaseModel):
    id: int
    name: str
    email: Optional[EmailStr] = None
    status: StatusEnum
    score: Optional[float] = None
    created_at: datetime
    is_premium: bool

    model_config = {"str_strip_whitespace": True}
```

**Pydantic rules:**
- Use `Optional[T] = None` for nullable or missing fields
- Use `EmailStr` for email strings (requires `pydantic[email]`)
- Use `AnyUrl` for URL strings
- Use `str(Enum)` for string enums
- Add `model_config` block with common defaults

### Zod (TypeScript/JavaScript)

```typescript
import { z } from "zod";

const StatusEnum = z.enum(["active", "inactive", "pending"]);

export const UserEventSchema = z.object({
  id: z.number().int(),
  name: z.string(),
  email: z.string().email().nullable().optional(),
  status: StatusEnum,
  score: z.number().nullable().optional(),
  created_at: z.string().datetime(),
  is_premium: z.boolean(),
});

export type UserEvent = z.infer<typeof UserEventSchema>;
```

**Zod rules:**
- Chain `.nullable()` when null was observed, `.optional()` when field was absent
- Use `.int()` for integer fields
- Use `.datetime()` for ISO datetime strings
- Always export the inferred type alongside the schema
- Export both schema and type from the same file

### TypeScript Interface (no runtime validation)

```typescript
type Status = "active" | "inactive" | "pending";

interface UserEvent {
  id: number;
  name: string;
  email?: string | null;
  status: Status;
  score?: number | null;
  created_at: string; // ISO 8601 datetime
  is_premium: boolean;
}
```

### JSON Schema Draft 7

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "UserEvent",
  "type": "object",
  "required": ["id", "name", "status", "created_at", "is_premium"],
  "properties": {
    "id": { "type": "integer" },
    "name": { "type": "string" },
    "email": { "type": ["string", "null"], "format": "email" },
    "status": { "type": "string", "enum": ["active", "inactive", "pending"] },
    "score": { "type": ["number", "null"] },
    "created_at": { "type": "string", "format": "date-time" },
    "is_premium": { "type": "boolean" }
  },
  "additionalProperties": false
}
```

### Go Struct

```go
package models

import "time"

type Status string

const (
    StatusActive   Status = "active"
    StatusInactive Status = "inactive"
    StatusPending  Status = "pending"
)

type UserEvent struct {
    ID          int        `json:"id"`
    Name        string     `json:"name"`
    Email       *string    `json:"email,omitempty"`
    Status      Status     `json:"status"`
    Score       *float64   `json:"score,omitempty"`
    CreatedAt   time.Time  `json:"created_at"`
    IsPremium   bool       `json:"is_premium"`
}
```

---

## Step 4: Output Report

Always structure the output as:

```markdown
## Schema Sleuth: [SchemaName]
Input: [N samples] | Detected format: JSON | Fields: 7 | Nullable: 2 | Optional: 1 | Enums: 1

### Field Analysis

| Field | Observed Types | Inferred Type | Nullable | Optional | Notes |
|-------|---------------|--------------|----------|----------|-------|
| `id` | int | `int` | No | No | |
| `name` | str | `str` | No | No | |
| `email` | str, null | `Optional[EmailStr]` | Yes | Yes | Email pattern detected |
| `status` | str (3 values) | `StatusEnum` | No | No | Enum: active/inactive/pending |
| `score` | float, null | `Optional[float]` | Yes | Yes | |
| `created_at` | str | `datetime` | No | No | ISO 8601 datetime |
| `is_premium` | bool | `bool` | No | No | |

### Confidence Notes

- `score`: seen as null in 1/3 samples — marked Optional. If it's always present but can be null, remove `Optional`.
- `email`: missing in 1 CSV row — marked Optional. Confirm if email is truly optional in your domain.
- `status` enum: only 3 values seen in 3 samples — may not be exhaustive. Add `| str` to the type if other values are possible.

### Generated Schemas

[Pydantic v2 code block]
[Zod code block]
[TypeScript interface code block]
[JSON Schema code block — if requested]
[Go struct code block — if requested]
```

---

## Quick Mode

For a single JSON object, just paste it and get back types immediately:

```
Input: {"user_id": 123, "action": "click", "ts": 1710000000}

Quick Schema:
- user_id: int (required)
- action: str (required) — consider enum if values are limited
- ts: int — looks like Unix timestamp (10 digits), consider datetime

Pydantic: UserEvent(user_id: int, action: str, ts: int)
Zod: z.object({ user_id: z.number().int(), action: z.string(), ts: z.number().int() })
TS: { user_id: number; action: string; ts: number }
```

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Field has `null` in every sample | Type is `None` / `null` → flag as "always null, probably placeholder" |
| Empty string `""` in some samples | Distinguish from null — may need `str \| None` + validator |
| Integers and floats mixed | Always promote to `float` |
| Integers that look like booleans (0/1) | Flag: "could be bool or int — confirm intent" |
| Very long strings (> 500 chars) | Flag as "possibly free text / markdown / HTML, consider Text type" |
| Array with mixed types `[1, "a", null]` | `list[int \| str \| None]` / `z.array(z.union([z.number(), z.string(), z.null()]))` |
| Deeply nested objects | Recursively generate sub-models/sub-schemas |
| Date vs datetime ambiguity | If no time component seen, use `date`; if any has time, use `datetime` |
| Large integers (> 2^53) | Flag: "may exceed JavaScript Number precision — use BigInt or string" |
| UUID-like strings | Detect v4 pattern, use `UUID` type or `z.string().uuid()` |

---

## Parser Generation (Optional)

If user says "also write the parser", generate extraction code:

### Python parser

```python
import json
from pathlib import Path

def parse_user_events(data: str | dict | list) -> list[UserEvent]:
    """Parse raw JSON string, dict, or list into UserEvent objects."""
    if isinstance(data, str):
        raw = json.loads(data)
    else:
        raw = data

    if isinstance(raw, list):
        return [UserEvent.model_validate(item) for item in raw]
    return [UserEvent.model_validate(raw)]

# Usage:
events = parse_user_events(api_response_text)
```

### TypeScript parser

```typescript
export function parseUserEvents(raw: unknown): UserEvent[] {
  const input = Array.isArray(raw) ? raw : [raw];
  return input.map((item) => UserEventSchema.parse(item));
}

// With error details:
export function safeParseUserEvents(raw: unknown): {
  data: UserEvent[] | null;
  errors: string[] | null;
} {
  try {
    return { data: parseUserEvents(raw), errors: null };
  } catch (e) {
    return { data: null, errors: [String(e)] };
  }
}
```

---

## Why This Doesn't Already Exist

Tools like `quicktype` do JSON → types, but require a CLI install and produce verbose output that often needs manual cleanup. This skill:

1. **Handles multiple samples** — sees `score: null` in sample 2 and correctly marks it Optional; `quicktype` with one sample misses nullability
2. **Detects semantic types** — `"alice@example.com"` → `EmailStr`, not just `str`
3. **Infers enums from repeated values** — 3 samples with only `"active"/"inactive"/"pending"` → Literal enum, not generic string
4. **Multi-language in one pass** — Pydantic + Zod + TS interface simultaneously
5. **Explains its reasoning** — confidence table shows exactly which fields need human review
6. **Zero install** — no `npm install quicktype`, no CLI, works from any data paste

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
