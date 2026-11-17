# Activity → Expert Dispatch Map · Activity-to-Expert Map

This file is the "routing table" for PM Master's second-layer dispatch: given the **domain, product, and task keywords** of a WBS activity/deliverable,
it determines which **expert role** should produce it. Works together with `references/expert-roles.md` (role definitions and prompts)
and `scripts/dispatch.py` (auto-generates the dispatch plan).

> **Single source of truth = `scripts/role_catalog.py`.** The domain catalogue, keyword maps, and
> specialization naming all live there. `dispatch.py` and `consistency_check.py` import it; this document
> is the human-readable mirror. **The pack is domain-agnostic** — it ships no data-domain bias and applies
> to any tech project (software / cloud / data / AI / security / product / QA / integration / ERP / BI).

## 1. Tech Domains (inferred from contract/SOW extract)

`infer_domain(text)` scans the SOW/contract objective+scope+assumptions and picks the best-matching domain.
When no signal is found, domain = `generic` and roles fall back to cross-cutting / neutral defaults.

| domain key | covers |
|------------|--------|
| `data-platform` | data lake / warehouse / ETL / modeling / governance |
| `software-dev` | application / backend / frontend / microservice / mobile |
| `cloud-infra` | cloud / k8s / terraform / SRE / platform / DevOps / network |
| `ai-ml` | LLM / GenAI / ML / model training / MLOps |
| `cybersecurity` | security / privacy / AppSec / SecOps |
| `product` | product management / ownership / UX |
| `qa` | test engineering / automation / performance |
| `integration` | ESB / middleware / API gateway |
| `erp` | ERP implementation / finance-HR modules |
| `biz-analytics` | BI / reporting / metrics layer |

> `project.domain` may also be set explicitly (e.g. via `init_project.py --domain <domain>`); an explicit
> domain overrides inference. Legacy project domains (`insurance-data-lake` / `payments` / `ecommerce` /
> `fintech-core`) still resolve via a backward-compat map in `role_catalog.py` so existing programs keep
> their specialization labels.

## 2. Activity Type → Role (keyword routing, by domain)

Routing is **two-tier**: (1) if a domain is known, its domain-specific role keywords win; (2) otherwise
cross-cutting keywords apply; (3) ambiguous words fall back to a neutral role (e.g. "model/design" → `solution-architect`).
Representative mappings (full set in `role_catalog.py`):

| Activity / deliverable keywords (EN) | domain | dispatch role role_id |
|------------------------------|--------|------------------|
| modeling / model / schema / ERD / subject-domain | data-platform | `data-architect` |
| migration / ETL / load / data-pipeline | data-platform | `etl-engineer` |
| governance / metadata / lineage / audit | data-platform | `data-governance-lead` |
| desensitization / privacy / PII / encryption / compliance | data-platform / cybersecurity | `data-security-engineer` / `privacy-engineer` |
| architecture-design / module / system-design | software-dev | `software-architect` |
| backend / server-side / API-implementation | software-dev | `backend-engineer` |
| frontend / UI / interface | software-dev | `frontend-engineer` |
| fullstack | software-dev | `fullstack-engineer` |
| mobile / iOS / Android | software-dev | `mobile-engineer` |
| cloud-architecture / landing-zone | cloud-infra | `cloud-architect` |
| reliability / SRE / disaster-recovery | cloud-infra | `sre-engineer` |
| platform-engineering / DevOps / CI-CD | cloud-infra | `platform-engineer` / `devops-engineer` |
| network / VPC / DNS | cloud-infra | `network-engineer` |
| LLM / RAG / fine-tuning | ai-ml | `llm-engineer` |
| model-training / feature-engineering / ML | ai-ml | `ml-engineer` |
| model-deployment / monitoring / MLOps | ai-ml | `mlops-engineer` |
| penetration / zero-trust / hardening | cybersecurity | `security-engineer` |
| application-security / SAST / DAST | cybersecurity | `appsec-engineer` |
| security-operations / SOC / threat-detection | cybersecurity | `secops-engineer` |
| product-planning / roadmap / requirements-management | product | `product-manager` |
| backlog / product-owner | product | `product-owner` |
| user-experience / UX / prototype | product | `ux-designer` |
| test / UAT / quality | qa (or cross-cutting `qa-lead`) | `qa-engineer` |
| automated-testing / test-framework | qa | `test-automation-engineer` |
| performance-testing / load-testing | qa | `performance-engineer` |
| integration / ESB / middleware / connector | integration | `integration-engineer` |
| API-design / gateway | integration | `api-engineer` |
| ERP-implementation / business-process / blueprint | erp | `erp-consultant` |
| ERP-development / custom-development | erp | `erp-developer` |
| report / dashboard / BI | biz-analytics | `bi-engineer` |
| metric / metric-system / marts | biz-analytics | `analytics-engineer` |
| training / enablement / course | cross-cutting | `enablement-lead` |
| infrastructure / installation / environment / deployment | cross-cutting | `infra-engineer` |
| SME / domain-knowledge / source-system | cross-cutting | `domain-sme` |
| test / UAT / quality (generic) | cross-cutting | `qa-lead` |
| requirements / user-story / specification | cross-cutting | `ba` |
| change / CCB | cross-cutting | `change-manager` |
| blueprint / integration / solution (program) | cross-cutting | `solution-architect` |
| charter / RACI / communication / status / risk / scheduling-skeleton | PM-generalist | existing (planner/risk/stakeholder/…) |

> The matching engine lives in `role_catalog.py` (`infer_role`). `dispatch.py` and `consistency_check.py`
> share it (single source of truth). To add a domain or role, edit `role_catalog.py` only.

## 3. Granularity Standard — preventing "SOW-level coarse-grained WBS"

An experienced team's WBS is not 10 SOW packages but **hundreds of leaf work packages**. Decision rules:

- **Leaf work package (leaf)**: `estimate` (person-days) ≤ `granularity_threshold` (default **10 person-days**;
  can be overridden via `control.granularity_threshold` in `project.yaml`).
- Any package with `estimate > threshold` is treated as a **summary package**, and its domain expert must be dispatched to further decompose it into
  leaf packages beneath it, **until all leaves ≤ threshold**.
- Required fields for a leaf package: `id` / `name` / `deliverable` / `role` (producing role) / `owner` / `estimate`
  / `acceptance` (DoD) / `dependsOn` / `domain`.
- **ID convention**: leaf packages decomposed by an expert inherit the parent package prefix, e.g. under `SOW1` there are `SOW1.1`, `SOW1.2`…;
  levels are separated by `.` to keep dependencies pointable.

## 4. Dispatch Flow (executed by the master controller, see orchestration.md §3.2)

```
1. Draft WBS (SOW-level summary packages, tagged with domain)
2. Tag each package's role (if absent, infer via §2 keywords, write to wbs[].role / wbs[].domain)
3. For each summary package (estimate > threshold) dispatch the corresponding expert sub-Agent:
   - Use that role's system_prompt from expert-roles.md (substituting DOMAIN/PRODUCT)
   - brief: decompose "<package name>" into leaf packages (≤ threshold person-days), write back to project.yaml.wbs (ID prefix <package ID>.x)
4. Expert writes back leaf packages → master re-renders wbs.md → runs consistency_check (new gate validates role tags + granularity)
5. If not passed, return to the corresponding expert to keep decomposing, until all leaves ≤ threshold and all domain activities have role tags
```

## 5. Consistency Gate Integration (consistency_check.py)

- **Domain activity missing a `role` tag → fatal by default (exit 1 blocks delivery)**; under `--strict`, other warnings are also escalated to fatal.
- Domain activities with `estimate > granularity_threshold` that are not decomposed → **fatal by default**; non-domain activities exceeding the threshold are only warnings (generic granularity hint).
- Program-level `summary` rollup packages (SOW/P0 parent packages) are skipped; the component-layer leaf packages carry them instead.

These two gates keep "coarse-grained SOW-level WBS not decomposed by experts / self-decomposed by master" out the door—you must go through `dispatch.py` → domain expert sub-Agent decomposition,
otherwise `consistency_check.py` will rule it fatal before delivery and it cannot be released (see SKILL.md Step 2.5 / §6).
