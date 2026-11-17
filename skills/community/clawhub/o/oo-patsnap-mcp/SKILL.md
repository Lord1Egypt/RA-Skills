---
name: oo-patsnap-mcp
description: "Patsnap MCP (open.patsnap.com). Use this skill for ANY Patsnap MCP request — reading, creating, and updating data. Whenever a task involves Patsnap MCP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Patsnap MCP"
  author: "OOMOL"
  version: "1.0.3"
  services: ["patsnap_mcp"]
  icon: "https://static.oomol.com/logo/third-party/patsnap_mcp.svg"
---

# Patsnap MCP

Operate **Patsnap MCP** through your OOMOL-connected account. This skill calls the `patsnap_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Patsnap MCP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "patsnap_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "patsnap_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `abstract_image` — Retrieves Valuation Patent Abstract Image data so users can review the key information and continue with downstream analysis.
- `abstract_translated` — Retrieves Patent Abstract Translated data so users can review the key information and continue with downstream analysis.
- `award_data` — Retrieves Patent Awards to review honors, awards, and external recognition for a company or patent.
- `bibliography` — Retrieves detailed Bibliography for verification, full-text review, and deeper analysis.
- `claim_translated` — Retrieves detailed Translated Claims for verification, full-text review, and deeper analysis.
- `claims` — Retrieves detailed Claims for verification, full-text review, and deeper analysis.
- `customs_data` — Retrieves Customs Recordation to assess status changes, patent stability, and potential legal risk.
- `description` — Retrieves detailed Description for verification, full-text review, and deeper analysis.
- `description_translated` — Retrieves detailed Translated Description for verification, full-text review, and deeper analysis.
- `design_create_image_upload_url` — Returns a temporary PUT upload URL. Upload the image binary to this URL using HTTP PUT, then pass the returned image URL to design_submit_workflow. This tool only creates the upload URL and does not accept image binaries or large base64 payloads. [write]
- `design_get_stage_result` — Get execution result of a specific stage — returns the full business data (result_data) of a stage, which may be large. To get final results, typically use stage='feature_comparison' or 'generate_report'
- `design_get_task_status` — Query workflow task status — returns lightweight task overview and per-stage summaries (status/duration/retry count/error message) without large result_data, suitable for high-frequency polling
- `design_submit_workflow` — Submit FTO workflow task — triggers the full pipeline (lineart conversion → search → rerank → RRF fusion → feature comparison → report generation) in one shot. Returns a task_id for polling via design_get_task_status and fetching results via design_get_stage_result [write]
- `family` — Retrieves Patent Family to review family relationships, jurisdictional coverage, and family breadth.
- `forward_citation` — Retrieves Valuation Patent Forward Citation data so users can review the key information and continue with downstream analysis.
- `fulltext_image` — Retrieves detailed Full-text Images for verification, full-text review, and deeper analysis.
- `get_patent_legal_status` — Retrieves Simple Legal Status to assess status changes, patent stability, and potential legal risk.
- `landscape_applicant_rank` — Analyzes Applicant Ranking to show activity changes, leading entities, and directional signals.
- `landscape_applicant_technology_analysis` — Retrieves Applicant Technology Analysis data so users can review the key information and continue with downstream analysis.
- `landscape_applicant_trend` — Analyzes Leading Applicant Filing Trend to show activity changes, leading entities, and directional signals.
- `landscape_cooperation_applicant_analysis` — Retrieves Cooperation Applicant Analysis data so users can review the key information and continue with downstream analysis.
- `landscape_detail` — Retrieves detailed Patent Details for verification, full-text review, and deeper analysis.
- `landscape_detail_aggregation` — Retrieves detailed Patent Detail Aggregation for verification, full-text review, and deeper analysis.
- `landscape_detail_text` — Retrieves detailed Patent Detail Text for verification, full-text review, and deeper analysis.
- `landscape_domain_map` — Analyzes Domain Map to show structure, distribution, hotspots, and the overall landscape.
- `landscape_famn_rank` — Analyzes Patent Family Ranking to show activity changes, leading entities, and directional signals.
- `landscape_get_patent_pdf` — Retrieves Patent PDF data so users can review the key information and continue with downstream analysis.
- `landscape_get_rec_office_year` — Analyzes Receiving Office Statistics By Year to show activity changes, leading entities, and directional signals.
- `landscape_info` — Retrieves detailed Patent Field Details for verification, full-text review, and deeper analysis.
- `landscape_list` — Retrieves a Patent List for batch review, filtering, and further processing.
- `landscape_map_3d` — Analyzes 3D Map Analysis to show structure, distribution, hotspots, and the overall landscape.
- `landscape_rec_office` — Analyzes Receiving Office Statistics to show activity changes, leading entities, and directional signals.
- `landscape_refered_rank` — Analyzes Citation Count Ranking to show activity changes, leading entities, and directional signals.
- `landscape_search_patents_facet` — Searches Patent Search Facets based on input criteria and returns matching results for screening, comparison, and follow-up analysis.
- `landscape_search_patents_statistics` — Analyzes Patent Statistics to show activity changes, leading entities, and directional signals.
- `landscape_search_patents_v3` — Searches Patent Search based on input criteria and returns matching results for screening, comparison, and follow-up analysis.
- `landscape_search_patents_with_detail` — Searches Patent Search With Details based on input criteria and returns matching results for screening, comparison, and follow-up analysis.
- `landscape_tech_applicant_dist` — Analyzes Key Technology Branch Applicant Distribution to show structure, distribution, hotspots, and the overall landscape.
- `landscape_technology_constitute` — Analyzes Technology Composition to show structure, distribution, hotspots, and the overall landscape.
- `landscape_technology_life_cycle` — Analyzes Technology Life Cycle to show structure, distribution, hotspots, and the overall landscape.
- `landscape_trend` — Analyzes Patent Trend to show activity changes, leading entities, and directional signals.
- `legal_data` — Retrieves detailed Legal Details for verification, full-text review, and deeper analysis.
- `license_data` — Retrieves Valuation Patent License Data data so users can review the key information and continue with downstream analysis.
- `list_tools` — Discover current tools and live input schemas for one Patsnap MCP service. Defaults to core_patents.
- `pdf` — Retrieves detailed Full-text PDF for verification, full-text review, and deeper analysis.
- `pledge_data` — Retrieves Valuation Patent Pledge Data data so users can review the key information and continue with downstream analysis.
- `reexamination_invalidation` — Retrieves Reexamination And Invalidation to assess status changes, patent stability, and potential legal risk.
- `search_patents` — Searches Patent Search By Query based on input criteria and returns matching results for screening, comparison, and follow-up analysis.
- `transfer_data` — Retrieves Valuation Patent Transfer Data data so users can review the key information and continue with downstream analysis.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Patsnap MCP state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Patsnap MCP is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/patsnap_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Patsnap MCP homepage: https://open.patsnap.com/marketplace/mcp-servers
- API documentation: https://open.patsnap.com/devportal/guides/mcp-quickstart
