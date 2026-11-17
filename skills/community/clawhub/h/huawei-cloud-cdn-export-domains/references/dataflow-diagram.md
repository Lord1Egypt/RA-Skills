# Data Flow Diagram

```mermaid
flowchart TD
    A[agent / user] -->|"python3 scripts/export_cdn_domains.py<br/>--region R --format csv|markdown|json|table<br/>--output O --domain-status online"| B[export_cdn_domains.py]
    B --> G{write-intent guard}
    G -->|mutating intent| X[GuardError → exit 1, no call]
    G -->|read-only| C[build_command: hcloud CDN ListDomains --cli-region=R --page_size=N --page_number=P + filters]
    C --> D[skill-quality-cli run --skill-name huawei-cloud-cdn-export-domains -- hcloud ...]
    D --> E[Huawei Cloud CDN OpenAPI\nGET /v1.0/cdn/domains]
    E -->|JSON domains + total| F{collected >= total?}
    F -->|no| C
    F -->|yes| H[parsed accelerated-domain records]
    C -.->|hcloud binary missing| S[huaweicloudsdkcdn v1 CdnClient.list_domains]
    S --> H
    H --> I{--format}
    I -->|csv (default)| J[render_csv → temp file + atomic rename → .csv]
    I -->|markdown| K[render_markdown → temp file + atomic rename → .md]
    I -->|json| L[render_json → temp file + atomic rename → .json]
    I -->|table| M[render_table → stdout]
    J --> N[(local filesystem export file)]
    K --> N
    L --> N
    S -.->|SDK missing| O[python3 scripts/ensure_env.py → pip install]
```

Parallel semantics:

- **Local-only output** — only the `.csv` / `.md` / `.json` / stdout artifact is
  produced; no CDN write API is ever constructed.
- **Empty region** — a header-only (empty) export file is still written and the
  process exits `0`.