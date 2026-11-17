<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# API Architecture & Contracts

**Document Status:** {Draft / Review / Approved}
**Version:** {n.n}
**Date:** {YYYY-MM-DD}
**Author:** {Role}

---

## 1. API Style

**Chosen:** {REST / GraphQL / gRPC / Hybrid}
**Rationale:** {Why — ADR-{nnn}}

---

## 2. URL Structure & Naming

| Pattern | Convention | Example |
|---------|-----------|---------|
| Base URL | {pattern} | {example} |
| Collection | {pattern} | {example} |
| Single resource | {pattern} | {example} |
| Nested resource | {pattern} | {example} |
| Actions | {pattern} | {example} |

---

## 3. HTTP Methods & Status Codes

| Method | Semantics | Idempotent? | Success Code |
|--------|-----------|:-----------:|:------------:|
| GET | {semantics} | Yes | 200 |
| POST | {semantics} | No | 201 |
| PUT | {semantics} | Yes | 200 |
| PATCH | {semantics} | Yes | 200 |
| DELETE | {semantics} | Yes | 204 |

---

## 4. Response Format

### Success

```json
{
  "data": { },
  "meta": { }
}
```

### Error

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Description",
    "details": []
  }
}
```

---

## 5. Pagination

**Strategy:** {Offset / Cursor / Keyset}

| Parameter | Default | Maximum |
|-----------|:-------:|:-------:|
| pageSize | {n} | {n} |

---

## 6. Filtering & Sorting

| Concern | Convention | Example |
|---------|-----------|---------|
| Filter | {approach} | {example} |
| Sort | {approach} | {example} |
| Search | {approach} | {example} |

---

## 7. Versioning

**Strategy:** {URL path / Header}
**Format:** {pattern}
**Breaking change policy:** {rule}

---

## 8. Authentication & Rate Limiting

| Consumer | Auth Method | Rate Limit |
|----------|:----------:|:----------:|
| {consumer type} | {method} | {limit/window} |

---

## 9. Documentation

| Aspect | Approach |
|--------|----------|
| Spec format | {OpenAPI 3.x} |
| Interactive docs | {Swagger UI / Redoc} |
| Generation | {Auto / Manual / Hybrid} |

---

*API Architecture v{version} | {date} | Status: {status}*
