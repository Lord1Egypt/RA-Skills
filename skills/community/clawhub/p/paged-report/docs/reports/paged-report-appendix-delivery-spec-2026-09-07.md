# Paged-report Appendix + Delivery Contract

**Status:** PROPOSED / SPEC GATE PENDING
**Date:** 2026-09-07
**Implementation:** Not started
**Release impact:** None; this document does not authorize a release, commit, deployment, or customer publication.

## 1. Purpose

把 Collection 报告复盘中已经验证过、但目前仍由项目代码重复实现的能力，收敛为两个可选、可验收的通用契约：

1. `paged-report` 的可选 `data_appendix`：表格、关系、搜索、分页、导出和附录打印。
2. `artifact-delivery` 的 delivery package：主文件、附件、hash、QA 证据、展示状态和线上验证回执。

核心原则：**项目层保留业务语义和来源判断；共享层只提供通用结构、交互、验证和交付边界。**

## 2. Traceability / source evidence

本规格由以下已存在资料推导，不把历史建议当成已经实现的事实：

- Prior project retrospective (`WORKFLOW-RETROSPECTIVE.md`; local source evidence, not part of the generic package)
  - §10, lines 216–240：`paged-report` 的可选 appendix、搜索语义、打印、状态和 QA 回执建议。
  - §11, lines 242–265：`artifact-delivery` 的 package 注册、附件、密码引用、发布回执和保护等级建议。
  - §12–13, lines 267–294：两个技能的边界、交接清单和实施顺序。
- `README.md`, `## Package boundary`, `## Integration with artifact-delivery`
  - 当前 package 状态仍是 `development / review-pending / migration-blocked`。
  - 当前生成与发布仍是两个独立阶段。
- `docs/reports/paged-report-qa-contract-2026-09-07.md`
  - 当前已有 HTML/PDF/A4/blank/page-policy/overflow 证据契约；logical page 与 physical page 不等同。
  - 当前 `WARN / MANUAL_REVIEW_REQUIRED` 不得被自动升级为 `PASS`。
- `~/.hermes/skills/devops/artifact-delivery/SKILL.md`
  - 当前以单文件注册、dry-run、部署和 URL 验证为主。
  - browser-side password gate 不是服务器鉴权，直链附件不受该 gate 保护。

### Already absorbed / not repeated

以下建议已在当前工作流中部分或全部吸收，本规格不重新定义其语义：

- self-contained HTML、inline CSS、无外部资源；
- structured JSON input 与 unknown-field validation；
- Kimi WebBridge 作为交互/PDF preview 主路线；
- logical/physical page 分离；
- A4、blank page、page policy 和 manual overflow evidence；
- generic release allowlist 与 `development / review-pending` 边界。

本规格要补的是：**把项目内重复的 appendix 和 delivery evidence 变成机器可读、可复用的接口。**

## 3. Goals

- 让没有附录的确认函、报价和进度报告保持现有最小路径，不额外加载大数据模块。
- 让数据审计类报告通过配置声明数据集、列、关系、搜索和导出，而不是通过 `replace('</body>', ...)` 注入项目专用 HTML/JS。
- 让 QA 结果直接写入可追溯 evidence manifest，减少人工转录。
- 让发布包明确主文件、附件、hash、来源快照、展示状态和验证状态。
- 在不保存或传播密码明文的前提下，记录实际保护等级。
- 让所有“已发布”声明都有线上 read-back evidence，而不是仅凭部署命令成功。

## 4. Non-goals / explicit boundaries

本阶段不做：

- 数据库、后端 API、登录系统、RBAC 或服务器端鉴权；
- 第三方店铺平台分类、产品语义批准、业务事实核查或 source-of-truth 决策；
- 自动把任意长内容压缩为一页物理 A4；
- 用 Playwright 替代 Kimi WebBridge 的快速交互/PDF 路线；
- 默认把所有大型数据复制进每一个 HTML 字段；
- Markdown 作为本阶段的发布主格式；
- stable release、tag、push、deploy 或客户发布授权。

## 5. Proposed architecture

```text
project adapter
  ├─ reviewed report content
  ├─ normalized datasets + source snapshot metadata
  ├─ report config
  └─ appendix config (optional)
          │
          ▼
    paged-report
  ├─ main report HTML
  ├─ optional appendix UI
  └─ QA evidence input/output
          │
          ▼
  delivery package manifest
  ├─ primary HTML
  ├─ optional CSV/ZIP/PDF attachments
  ├─ hashes + provenance
  ├─ QA evidence
  └─ publish/verification state
          │
          ▼
    artifact-delivery
  ├─ package registration
  ├─ dry-run
  ├─ deploy
  └─ index/direct URL/read-back verification
```

`paged-report` 不决定哪些产品属于哪个 Collection；`artifact-delivery` 不改写报告结论。

## 6. Feature A — optional `data_appendix`

### 6.1 Activation and top-level shape

没有 `data_appendix` 时，生成结果不包含附录 UI、附录 JavaScript 或附录数据块。

建议的配置形状：

```json
{
  "data_appendix": {
    "title": "Data appendix",
    "datasets": [
      {
        "id": "collections",
        "label": "Collections",
        "primary_key": "collection_id",
        "source": {
          "snapshot_at": "2026-09-07T08:33:24Z",
          "record_count": 3
        },
        "columns": [
          {
            "field": "collection_id",
            "label": "Collection ID",
            "type": "text",
            "visible": false,
            "searchable": false,
            "export": true
          },
          {
            "field": "name",
            "label": "Name",
            "type": "text",
            "visible": true,
            "searchable": true,
            "export": true
          }
        ],
        "records": [
          {"collection_id": "c-001", "name": "Example Collection"}
        ]
      }
    ],
    "relations": [
      {
        "id": "collection-products",
        "from_dataset": "collections",
        "from_field": "collection_id",
        "to_dataset": "products",
        "to_field": "collection_id",
        "label": "Products"
      }
    ],
    "search": {
      "default_scope": "name",
      "scopes": ["name", "all_fields"],
      "show_matched_fields": true
    },
    "pagination": {
      "default_page_size": 25,
      "page_sizes": [25, 50, 100]
    },
    "exports": {
      "filtered_csv": true,
      "dataset_csv": true
    },
    "print": {
      "mode": "all_filtered_rows"
    }
  }
}
```

The exact field names remain **proposed** until the Spec Gate. The contract must not silently accept unknown appendix fields.

### 6.2 Required semantics

- `datasets[].id` and `primary_key` are unique within the appendix.
- Every configured column declares its source field, display label, type, visibility, searchability, and exportability.
- Hidden identity fields may be exported and used for relations but are not visible by default.
- Relations use explicit keys; title matching is not a relation mechanism.
- The UI must distinguish:
  - total records in the selected dataset;
  - records matching the current filter/search;
  - the object being counted (dataset records, not pages or visible columns).
- Search scope must be visible to the user. When `show_matched_fields=true`, a result must identify the configured field(s) that matched.
- Screen pagination changes visible rows only; it must not change the filtered dataset used by CSV export.
- “Print all filtered rows” must temporarily render all filtered rows, print the requested range, and restore the previous screen state.
- Empty results must show an explicit no-match state and must not be confused with an empty dataset.
- The appendix must use vanilla, self-contained JavaScript generated by the package; no CDN, external stylesheet, or runtime backend is introduced.

### 6.3 Data size and self-containment

- `embedded` data is the default and preserves one-file HTML delivery.
- Records must not be duplicated merely to support relations; relation views resolve by declared keys.
- A future `bundle` mode may keep large datasets as attachments, but it is outside the first implementation unless a measured fixture demonstrates that embedded HTML is operationally unsuitable.
- The implementation must record HTML byte size and record counts in QA evidence. “Opened on the developer machine” is not a performance gate.

## 7. Feature B — QA evidence manifest

The current QA CLI remains the source of deterministic checks. The next interface adds an explicit output path, for example:

```bash
python3 qa/paged_report_qa.py report.html \
  --pdf /tmp/report.pdf \
  --expected-logical-pages 3 \
  --expected-physical-pages 3 \
  --output qa/report-evidence.json \
  --pretty
```

Proposed evidence shape:

```json
{
  "schema_version": 1,
  "artifact": {
    "html": {"path": "report.html", "bytes": 0, "sha256": "..."},
    "pdf": {"path": "report.pdf", "bytes": 0, "sha256": "..."}
  },
  "content": {
    "logical_pages": 3,
    "data_appendix": {
      "enabled": true,
      "datasets": 2,
      "records": 3,
      "html_bytes": 0
    }
  },
  "checks": {
    "html": "PASS",
    "a4": "PASS",
    "blank_pages": "PASS",
    "page_policy": {"status": "PASS", "verdict": "EXACT_PASS"},
    "overflow": {
      "status": "WARN",
      "verdict": "MANUAL_REVIEW_REQUIRED",
      "evidence": null
    }
  },
  "browser_review": {
    "adapter": "kimi-webbridge",
    "status": "PENDING",
    "reviewed_at": null,
    "screenshots": []
  },
  "overall": "WARN"
}
```

Rules:

- Hashes are calculated from the exact local artifact under review.
- `WARN` remains `WARN`; the tool never infers visual `PASS` from static checks.
- Browser evidence is external evidence and must remain distinguishable from deterministic CLI checks.
- No secrets, passwords, tokens, cookies, or connection strings are written to the manifest.
- The evidence file is suitable for inclusion in a delivery package, but its inclusion is explicit rather than automatic.

## 8. Feature C — delivery package manifest

`artifact-delivery` should accept one package manifest instead of requiring callers to register loosely related files one at a time.

Proposed shape:

```json
{
  "schema_version": 1,
  "package_id": "example-report-20260907",
  "display_state": "review",
  "primary": {
    "path": "report.html",
    "filename": "example-report-20260907.html",
    "sha256": "...",
    "bytes": 0
  },
  "attachments": [
    {
      "path": "data.zip",
      "filename": "example-report-20260907-data.zip",
      "media_type": "application/zip",
      "sha256": "...",
      "bytes": 0
    }
  ],
  "source": {
    "generated_at": "2026-09-07T08:33:24Z",
    "data_snapshot_at": "2026-09-07T03:05:03Z",
    "source_refs": [
      {"path": "report-content.json", "sha256": "..."}
    ]
  },
  "qa": {
    "evidence_path": "qa/report-evidence.json",
    "status": "WARN",
    "manual_review_required": true
  },
  "publish": {
    "target": "artifacts-pi",
    "access_level": "browser-gate",
    "password_ref": "existing-approved-entry",
    "deployment_status": "NOT_STARTED",
    "verification_status": "NOT_STARTED"
  }
}
```

Rules:

- `primary` is required; every attachment referenced by the manifest must exist before registration.
- `filename` is a basename and must be unique within the package namespace.
- Hash and byte counts are computed from the exact files being registered.
- `password_ref` is an identifier only. Password values never enter the manifest, CLI arguments in logged output, QA evidence, or release notes.
- `access_level` must describe the actual mechanism: `public`, `browser-gate`, or `server-authenticated`. `browser-gate` must carry the existing warning that direct non-HTML URLs may bypass it.
- `display_state` is one of `preview`, `review`, or `published`.
- `published` is valid only after deployment and direct URL/index/read-back verification are recorded.
- A failed verification must be represented as `DEPLOYED_VERIFICATION_INCOMPLETE`, not as a clean publish success.
- Stable-link replacement and new-artifact publication are distinct operations and must be recorded separately.

## 9. State transitions

```text
preview
  └─ owner review approved → review
       └─ deploy + primary/attachment/index/read-back PASS → published
```

- Generation may produce `preview` only.
- User/owner approval is required before a package is treated as `review`-ready for publication.
- The tooling may not self-promote an artifact to `published` based only on a successful deploy command.
- `published` does not mean source facts are correct; business/source approval remains a project-layer gate.

## 10. EARS acceptance criteria

### Appendix

1. **WHEN** a report has no `data_appendix` **THE** renderer **SHALL** produce the existing main report without appendix markup, appendix data, or appendix scripts.
2. **WHEN** a valid `data_appendix` is supplied **THE** renderer **SHALL** render every declared dataset and configured visible column without project-specific HTML injection.
3. **WHEN** an appendix contains an unknown field, duplicate dataset ID, invalid primary key, invalid relation endpoint, or unsupported column type **THE** generator **SHALL** fail before writing the output HTML with a contract error.
4. **WHEN** search scope is `name` or `all_fields` **THE** appendix **SHALL** expose the active scope and, when configured, the matched field name(s).
5. **WHEN** a filtered dataset is exported **THE** export **SHALL** contain all matching records, not only the current screen page or visible columns.
6. **WHEN** “print all filtered rows” is selected **THE** appendix **SHALL** expose all matching records to the print container and restore the prior screen state after printing.
7. **WHEN** the appendix is enabled **THE** generated HTML **SHALL** remain self-contained and contain no CDN, external stylesheet, or network data dependency.
8. **WHEN** the appendix fixture contains N records **THE** QA evidence **SHALL** report N as the dataset record count and record the generated HTML byte size.

### QA evidence

9. **WHEN** the QA CLI is run with `--output PATH` **THE** CLI **SHALL** write a valid JSON evidence manifest at PATH and still print a concise result to stdout.
10. **WHEN** a supplied PDF is not A4, contains a deterministic blank page, or violates an explicit page-count policy **THE** CLI **SHALL** return exit code 1.
11. **WHEN** static checks pass but visual overflow has not been externally reviewed **THE** evidence **SHALL** remain `WARN / MANUAL_REVIEW_REQUIRED`.
12. **WHEN** an evidence manifest is generated **THE** manifest **SHALL** include exact artifact hash/byte metadata and SHALL NOT include secrets.

### Delivery package

13. **WHEN** a package manifest references a missing primary or attachment **THE** registrar **SHALL** fail before mutating the delivery inventory.
14. **WHEN** a package is registered **THE** registrar **SHALL** verify unique basenames, hash/byte metadata, and primary/attachment membership.
15. **WHEN** a package uses `password_ref` **THE** logs and machine-readable receipt **SHALL** expose only the reference or enabled/disabled state, never the password value.
16. **WHEN** deployment completes but any required URL/read-back check fails **THE** receipt **SHALL** report deployment success with verification incomplete, not `published`.
17. **WHEN** a package is marked `published` **THE** receipt **SHALL** include primary URL, attachment URL(s), index verification, verification timestamp, and the exact artifact hashes checked.
18. **WHEN** a package replaces a stable filename **THE** receipt **SHALL** preserve before/after artifact identity and explicitly label the operation as stable-link replacement.

## 11. Fixture-first implementation plan

No implementation is authorized by this document. After Spec Gate approval, use sanitized fixtures in this order:

1. **Appendix-small fixture:** 2 datasets, explicit keys, 1 relation, 3 records, one no-match search, one all-fields match, 25-row page size.
2. **Appendix-export fixture:** more than one screen page, hidden identity field, filtered CSV and all-record CSV assertions.
3. **Appendix-print fixture:** enough rows to exercise print expansion and restoration without relying on physical A4 equality.
4. **Delivery-package fixture:** one primary HTML, one ZIP attachment, one QA evidence file, deterministic hashes, no password value.
5. **Failure fixtures:** missing attachment, duplicate filename, invalid relation, stale hash, failed direct URL, deployment verification incomplete.

Each fixture must remain generic and contain no customer brand names, store-platform identifiers, customer password, token, local absolute path, or private source data.

## 12. Proposed implementation sequence

### Phase A — evidence output (lower coupling)

- Add `--output` to `qa/paged_report_qa.py`.
- Add tests for exact JSON shape, hash/bytes, WARN preservation, and secret exclusion.
- Keep current stdout contract backward compatible.

### Phase B — appendix contract and renderer

- Add schema/runtime validation for `data_appendix`.
- Add a small vanilla-JS appendix renderer with explicit dataset/column/relation/search/export contracts.
- Keep appendix opt-in and leave existing reports byte-stable where no appendix is configured.
- Add deterministic HTML/interaction tests; use Kimi WebBridge for real-browser spot checks.

### Phase C — delivery package

- Define package manifest validation in `artifact-delivery`.
- Support package registration, dry-run, attachment checks, redacted receipts, and stable-link/new-artifact distinction.
- Verify index, primary URL, attachment URLs, and selected existing artifacts.

### Phase D — performance and optional bundle mode

- Only after a measured large fixture exceeds the agreed operational threshold, evaluate attachment-backed or lazy data loading.
- Do not add a database or frontend framework as a response to one 30MB report.

## 13. Spec Gate decisions required before implementation

1. Approve the exact `data_appendix` field names and whether records are supplied inline or through a separate input file.
2. Approve whether `data_appendix` is implemented inside `paged-report` or as a separately versioned optional module.
3. Approve the delivery manifest owner: `artifact-delivery` repository/skill versus a shared contract consumed by both projects.
4. Approve the allowed `access_level` values and wording for browser-side password gates.
5. Approve the minimum evidence retention policy for screenshots and browser session identifiers.

Until these decisions are approved, this document is a proposal and must not be represented as an implemented feature or stable release.
