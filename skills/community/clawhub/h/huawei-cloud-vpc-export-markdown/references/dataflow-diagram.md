# Data Flow Diagram

```mermaid
flowchart TD
    A[agent / user] -->|python3 scripts/export_vpc_markdown.py --region R --output O.md| B[export_vpc_markdown.py]
    B --> G{write-intent guard}
    G -->|mutating intent| X[GuardError → exit 1, no call]
    G -->|read-only| C[build_command: hcloud VPC ListVpcs --cli-region=R --limit=N --marker=M]
    C --> D[skill-quality-cli run --skill-name huawei-cloud-vpc-export-markdown -- hcloud ...]
    D --> E[Huawei Cloud VPC OpenAPI\nvpc.R.myhuaweicloud.com\nGET /v1/{project_id}/vpcs]
    E -->|JSON vpcs + page_info.next_marker| F{marker present?}
    F -->|yes| C
    F -->|no| H[parsed VPC records]
    C -.->|hcloud binary missing| S[huaweicloudsdkvpc v2 VpcClient.list_vpcs]
    S --> H
    H --> I{--format}
    I -->|md (default)| J[render_markdown → temp file + atomic rename → .md]
    I -->|table| K[render_table → stdout]
    I -->|json| L[json.dumps → stdout]
    J --> M[(local filesystem .md)]
    S -.->|SDK missing| N[python3 scripts/ensure_env.py → pip install]
```

Parallel semantics:

- **Local-only output** — only the `.md`/stdout artifact is produced; no VPC
  write API is ever constructed.
- **Empty region** — a header-only (empty) Markdown table is still written and
  the process exits `0`.