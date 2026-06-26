# Import & Export

Use `COPY FROM` for bulk import and `COPY TO` for export. Never substitute looped `MERGE` for bulk operations.

Staging directory: `~/openclaw/db/ocas-weave/staging/` (auto-created on first use).

## COPY FROM

Basic:
```cypher
COPY Person FROM '~/openclaw/db/ocas-weave/staging/contacts.csv' (header=true)
```

Partial columns (CSV has fewer columns than table):
```cypher
COPY Person(id, name, email, source_type, source_ref, confidence, record_time)
FROM '~/openclaw/db/ocas-weave/staging/partial.csv' (header=true)
```

With error skipping:
```cypher
COPY Person FROM '~/openclaw/db/ocas-weave/staging/contacts.csv' (header=true, ignore_errors=true)
```

After ignore_errors, always check then clear:
```cypher
CALL show_warnings() RETURN *;
CALL clear_warnings();
```

Row count verification:
```cypher
MATCH (p:Person) RETURN count(p) AS before;
-- run COPY FROM --
MATCH (p:Person) RETURN count(p) AS after;
```

Relationship import:
```cypher
COPY Knows FROM '~/openclaw/db/ocas-weave/staging/knows.csv' (from='Person', to='Person', header=true)
```

CSV must contain `from` and `to` columns with Person `id` values.

## COPY TO

Query results to CSV:
```cypher
COPY (MATCH (p:Person) RETURN p.id, p.name, p.email, p.location_city)
TO '~/openclaw/db/ocas-weave/staging/export_people.csv'
```

To JSON:
```cypher
COPY (MATCH (p:Person) RETURN p.*) TO '~/openclaw/db/ocas-weave/staging/export_people.json'
```

## Pre-import CSV prep (Python)

Run before every `COPY FROM` on external data. Adds missing required columns.

```python
import csv, uuid
from datetime import datetime, timezone
from pathlib import Path

STAGING = Path("~/openclaw/db/ocas-weave/staging").expanduser()

def prep_import_csv(input_path, output_filename, source_ref):
    now = datetime.now(timezone.utc).isoformat()
    STAGING.mkdir(parents=True, exist_ok=True)
    output_path = STAGING / output_filename
    required = {
        "source_type": "imported",
        "source_ref": source_ref,
        "confidence": "0.8",
        "record_time": now
    }
    with open(input_path) as fin, open(output_path, "w", newline="") as fout:
        reader = csv.DictReader(fin)
        extra = [f for f in required if f not in (reader.fieldnames or [])]
        writer = csv.DictWriter(fout, fieldnames=list(reader.fieldnames or []) + extra)
        writer.writeheader()
        for row in reader:
            if not row.get("id"):
                row["id"] = str(uuid.uuid4())
            for k, v in required.items():
                row.setdefault(k, v)
            writer.writerow(row)
    return output_path
```

## Connector export helpers

Modified since last sync (Google outbound):
```cypher
COPY (
  MATCH (p:Person)
  WHERE p.record_time > $last_sync_at AND p.google_resource_name IS NOT NULL
  RETURN p.id, p.name, p.name_given, p.name_family,
         p.email, p.phone, p.org, p.occupation, p.google_resource_name
) TO '~/openclaw/db/ocas-weave/staging/outbound_google.csv'
```

Modified since last sync (Clay outbound):
```cypher
COPY (
  MATCH (p:Person)
  WHERE p.record_time > $last_sync_at AND p.confidence >= 0.7 AND p.clay_id IS NOT NULL
  RETURN p.id, p.name, p.email, p.org, p.occupation, p.location_city, p.clay_id
) TO '~/openclaw/db/ocas-weave/staging/outbound_clay.csv'
```
