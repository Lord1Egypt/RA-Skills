> **Bilingual — 中英文皆可适配**  This skill ships both Chinese and English content. The Chinese counterpart of this file is `portability.zh.md`.

# Portable Deployment and Integration (Phase 11 · deliverables · vendor narrowing removed)

> Core premise: the ontology specification layer (semantic / logic / decision / action library / departments / industry packs / private customization under `references/` + `experts-template/`) is **vendor-neutral data**.
> The three deployment modes = the same specification + different "runtime shells". Swap the shell and it runs; **the business brain is neither lost nor rewritten**.
> This file explains how to use two scripts to export the specification as a portable bundle and generate integration configs.
> **Important: EdgeClaw / JoyAgent etc. are only "reference implementation examples", not the sole answer; any product satisfying the pattern capability contract in deployment.yaml can be plugged in.**

## 1. Two scripts (purely additive, core untouched)

| Script | Purpose | Reads | Writes |
|---|---|---|---|
| `scripts/export_spec.py` | Specification exporter: packages the source specification + instance into a self-contained bundle | references / instance | `exports/<slug>_ontology_bundle/` + `.zip` |
| `scripts/adapters.py` | Integration config generator: produces "pattern manifests" and "reference implementation / host platform" integration configs from the bundle | bundle / deployment.yaml | `runtime_manifest.yaml` + per-item `*.yaml` manifests |

Neither script depends on core scripts such as `init.py`; they only read existing references / instance and produce purely additive artifacts.

## 2. Exporting the specification (export_spec.py)

```bash
# Full bundle (source specification + instance) — default
python scripts/export_spec.py --bundle all --slug weishu --zip

# Source specification only (vendor-neutral, contains no enterprise instance; easy to distribute as a "blank template")
python scripts/export_spec.py --bundle source

# Digital twin instance only
python scripts/export_spec.py --bundle instance --slug weishu --out exports/
```

Output directory structure (`weishu_ontology_bundle/`):
```
weishu_ontology_bundle/
├── manifest.json          # portable contract (schema version / sync boundary / red lines / portable targets)
├── references/            # full specification copy (including packs/)
├── experts-template/      # department_experts.yaml (department library)
├── instance/              # instance.yaml + company-memory.md (+ experts.yaml if present)
└── (optional) weishu_ontology_bundle.zip
```

Key fields in `manifest.json`:
- `schema_version`: contract version (currently `1.0`)
- `source.department_library_count` / `action_specs_total`: specification scale
- `instance`: company name / pack / resolved departments / private customization (renames / genders / disabled / added)
- `governance.sync_boundary_ref` → `references/deployment.yaml#sync_boundary`
- `portable_to`: `["skill_package","cloud_edge","pure_private"]`

## 3. Integration config (adapters.py) — pattern first, product as example

`adapters.py` produces three kinds of manifests, **prioritizing the vendor-neutral "pattern manifest"; a specific product is only one reference implementation of that pattern**:

```bash
# (1) Vendor-neutral "runtime manifest" (main output, recommended): describes the capability
#     contract of a deployment pattern without binding to any product
python scripts/adapters.py --slug weishu --pattern edge_cloud
python scripts/adapters.py --slug weishu --pattern on_prem

# (2) Reference implementation examples (pick one or both): EdgeClaw / JoyAgent are examples only
python scripts/adapters.py --slug weishu --target edgeclaw
python scripts/adapters.py --slug weishu --target joyagent
python scripts/adapters.py --bundle exports/weishu_ontology_bundle --target both

# (3) Host platform "wrapping scaffold": port the same specification to competitor platforms
#     (answers "is it only for WorkBuddy")
python scripts/adapters.py --slug weishu --target coze
python scripts/adapters.py --slug weishu --target dify
python scripts/adapters.py --slug weishu --target claude
python scripts/adapters.py --slug weishu --target yuanqi
python scripts/adapters.py --slug weishu --target qianfan
python scripts/adapters.py --slug weishu --target workbuddy   # native platform notes
```

### 3.1 Vendor-neutral runtime manifest (runtime_manifest.yaml, main output)
- `pattern: edge_cloud | on_prem`; `required_runtime_capabilities` (the capabilities the runtime must satisfy for that pattern, see deployment.yaml `patterns`)
- `reference_products`: lists selectable reference implementations for the pattern (edge-cloud: EdgeClaw Box / Huawei & Lenovo edge all-in-one / cloud vendors' edge gateways / self-built; fully private: JoyAgent / Dify / CrewAI / n8n / Coze private / Zhipu · Tongyi · Wenxin private / Qianfan · Bailian)
- `ontology.source: ./references` (zero rewriting of the specification); `invariants`: the three-mode red lines run through explicitly

### 3.2 Reference implementation examples (edgeclaw_manifest.yaml / joyagent_manifest.yaml)
Explicitly labelled "reference implementation examples", not the sole answer:
- **Mode B cloud collaboration (example: ModelBest EdgeClaw Box)** — `edgeclaw_manifest.yaml`:
  - `runtime: cloud_edge`; references deployment.yaml's `sync_boundary` (sensitive stays on the edge `edge_local`: PII / contracts / finance / internal docs; external brain to the cloud `cloud_sync`: monitoring signals / public intelligence / heavy reasoning)
  - `agents_split`: automatically splits edge vs cloud by data sensitivity (sensitive departments `lead/admin/hr/finance/legal` stay on the edge; outward-facing departments go to the cloud)
  - `ontology.source: ./references` (fed directly to the edge subset + cloud external brain with zero rewriting)
- **Mode C fully private (example: JD JoyAgent-JDGenie)** — `joyagent_manifest.yaml` + `joyagent.docker-compose.yml` (deployment template hint):
  - `runtime: pure_private`; `model.air_gapped: true`; defaults to `deepseek-r1:local` (switchable to qwen / glm / domestic-tech base)
  - `ontology.source: ./references` (fed directly, zero rewriting)
  - `integration.erp_mes_writeback: true` (Action layer write-back to ERP / MES / OA)
  - The docker-compose template is explicitly labelled a "hint / placeholder"; images and volumes must be completed per JoyAgent's official deployment guide

### 3.3 Host platform "wrapping scaffolds" (host_<platform>_manifest.yaml) — answers "is it only for WorkBuddy"
- **Today**: the skill "shell" is WorkBuddy format, so it runs directly on WorkBuddy; Coze / Dify / Claude / Yuanqi / Qianfan use different formats and cannot load it directly.
- **But the specification is vendor-neutral**: run `adapters.py --target <platform>` to generate that platform's "wrapping scaffold", wrapping the same `references/` into the target platform's loadable skill / plugin format, **with zero rewriting of the specification**.
- The scaffold is honestly labelled a `porting scaffold`: it explains the wrapping idea ("use references as a knowledge base + a principal bot calling action_specs"); real integration with that platform's SDK / API is a later, independent phase.
- Each platform's `packaging_hint` is already defined in deployment.yaml `host_platforms` and in `HOST_PLATFORMS` in adapters.py.

## 4. End-to-end flow (Weishu as the example)

```
Install skill (WorkBuddy) ──init.py──> Weishu digital twin (instance.yaml)
        │
        ├─ export_spec.py --bundle all --slug weishu --zip
        │     └─> exports/weishu_ontology_bundle/  (specification + instance, self-contained)
        │
        └─ adapters.py --bundle exports/weishu_ontology_bundle --pattern edge_cloud   (vendor-neutral pattern manifest)
              ├─> runtime_manifest.yaml            (main output: pattern capability contract)
              ├─> edgeclaw_manifest.yaml           (reference implementation example: ModelBest EdgeClaw)
              ├─> joyagent_manifest.yaml           (reference implementation example: JD JoyAgent)
              └─> host_coze_manifest.yaml etc.      (host platform wrapping scaffolds, optional)
```

With one command chain, the business brain (the specification) is never rewritten — only the shell is swapped between Modes A/B/C, or ported to a different host platform.

## 5. Red lines (must be observed)

- Both scripts are **read-only** against references / instance and **never modify** the department template, the action library, `decision` / `semantic` / `logic` / `init.py` or other core files.
- The three-mode red lines sink down to the specification layer (the PII / contract / invoice constraints in `decision.yaml`) and apply equally to forms B and C.
- Integration manifests only "reference" the specification (`./references`, `./instance`) with **zero rewriting** — this is the foundation of "fully self-consistent integration".
- EdgeClaw / JoyAgent etc. are only reference implementation examples; actually feeding the bundle into a concrete runtime still requires integrating with that product's SDK / API (a later, independent phase). This file and the scripts have completed the "portable specification + integration config" layer.
