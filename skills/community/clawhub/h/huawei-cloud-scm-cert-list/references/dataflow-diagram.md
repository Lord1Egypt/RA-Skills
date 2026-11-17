# Data Flow Diagram

```mermaid
flowchart TD
    A["Agent / operator"] --> B["scripts/list_scm_certs.py"]
    B --> C{"Write intent?<br/>--action / --content"}
    C -- yes --> Z1["Reject (exit 1)<br/>no cloud call"]
    C -- no --> D{"hcloud on PATH?"}
    D -- yes --> E["hcloud SCM ListCertificates<br/>--cli-region --limit --offset<br/>[--content --expired_days_since]"]
    E -- ok --> H["JSON body<br/>certificates + total_count"]
    E -- "transient / missing" --> F["huaweicloudsdkscm<br/>ScmClient.list_certificates"]
    D -- no --> F
    F -- ok --> H
    E -- "403 / credentials / [USE_ERROR]" --> Z2["Actionable error (exit 1)<br/>no fallback"]
    F -- error --> Z2
    H --> I{"short page or<br/>offset >= total_count?"}
    I -- no --> E
    I -- yes --> J["normalize: id / name / domain / type /<br/>status / expire_time / days_left / source"]
    J --> K{"--expiring N?"}
    K -- yes --> L["keep days_left <= N"]
    K -- no --> M["keep all"]
    L --> N{"output mode"}
    M --> N
    N -- default --> O["证书名称 | 绑定域名 | 到期时间"]
    N -- --table --> P["8 columns<br/>ID/名称/域名/类型/状态/到期/剩余天数/region"]
    N -- --json --> Q["raw merged response"]
```

## Notes

- The loop between `E`/`F` and `I` is the offset+limit pagination; `--max-pages`
  is the safety cap.
- `403`, credential and `[USE_ERROR]` failures deliberately **do not** fall back
  to the SDK: a permission problem must never be reported as an empty list.
- `source` is derived from `status` (UPLOAD → 上传托管, SCM lifecycle statuses →
  SCM签发, otherwise `-`); no field is invented beyond what the API returns.