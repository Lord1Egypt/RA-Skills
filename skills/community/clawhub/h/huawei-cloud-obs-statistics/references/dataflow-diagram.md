# Data Flow Diagram

## Architecture Overview

```mermaid
graph LR
    subgraph Agent
        A[AI Agent]
    end
    subgraph Execution
        A -->|"1. hcloud OBS ls (buckets)"| B[KooCLI OBS / obsutil]
        A -->|"2. hcloud OBS ls obs://bucket/prefix (objects)"| B
        A -->|"3. collect_obs_stats.py"| P[Python script]
        A -->|"4. huaweicloudsdkobs (fallback)"| C[Python SDK]
    end
    B --> D["Huawei Cloud OBS API<br/>GET / (ListBuckets)<br/>GET /?prefix=&marker= (ListObjects)"]
    C --> D
    P --> B
    P --> C
    D --> E[(OBS Buckets / Objects)]
    E --> B
    E --> C
    B -->|"obs:// lines + sizes"| P
    C -->|"list_buckets / list_objects"| P
    P -->|"aggregate: buckets / objects / size / storage-class / region"| A
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant A as Agent
    participant P as collect_obs_stats.py
    participant C as hcloud CLI (obsutil)
    participant S as Python SDK
    participant O as OBS Service

    U->>A: Statistics for bucket X (prefix P)?
    A->>P: --bucket X --prefix P
    P->>C: hcloud OBS ls -limit=N -e=obs.<region>...
    C->>O: GET / (ListBuckets)
    O-->>C: buckets
    C-->>P: obs://bucket lines
    loop each bucket
        P->>C: hcloud OBS ls obs://X/P/ -limit=N -e=...
        C->>O: GET /?prefix=P (ListObjects)
        O-->>C: objects (key, size, storage class)
        C-->>P: object lines
    end
    P->>P: aggregate locally
    P-->>A: table | json | md
    A-->>U: bucket count / object count / capacity / distributions

    alt hcloud unavailable
        A->>P: --executor sdk
        P->>S: ObsClient.list_buckets / list_objects
        S->>O: GET / and GET /?prefix=&marker=
        O-->>S: buckets / objects
        S-->>P: aggregated inputs
        P-->>A: table | json | md
    end
```