---
name: "ovitalmap-parcel-csv"
description: "Parse parcel vertex coordinates from images/text, generate Ovitalmap-compatible CSVs (顶点表 + 边界表), categorize parcels by country-code/provider, and archive into a per-country database. Invoke when user provides parcel coordinates in any format and wants Ovitalmap CSV output."
---

# Ovitalmap Parcel CSV Generator

This skill processes parcel vertex coordinates — from images or text — and produces Ovitalmap-readable CSV files. It also archives every processed parcel into a structured per-country database with provider metadata.

---

## 0) Defaults: Language, Tone, I/O

- **Reply language**: Chinese by default unless the user requests another language.
- **Tone**: non-repetitive, concise, precise, professional.
- **Ambiguity handling**: when inputs are unclear (e.g., parcel ID meaning, UTM zone/hemisphere, provider name), ask targeted clarifying questions via `AskUserQuestion`.
- **CSV headers**: keep original Chinese headers exactly as listed below. Do not translate them.

---

## 0b) Scripting Conventions (MANDATORY)

**Use Python scripts for all data processing, CSV generation, archive management, and QC checks.** Do not process data through LLM reasoning alone — it is unreliable and costly for structured operations.

### Available Scripts

All scripts live in `scripts/` and accept JSON via stdin, returning JSON to stdout.

| Script | Purpose | Key CLI examples |
|--------|---------|------------------|
| **`scripts/utils.py`** | Shared helpers (CSV I/O, boundary comparison, DMS conversion, coordinate validation). Imported by other scripts — not called directly. | `from utils import boundaries_equal, dms_to_decimal` |
| **`scripts/country_locator.py`** | Normalize & validate WGS84 coordinates (lat/lon swap detection, range checks). ALWAYS returns `country_code: null` — the LLM determines the country from spatial knowledge and conversation context. | `echo '[[114.13,22.50],[114.14,22.51]]' \| python3 scripts/country_locator.py` |
| **`scripts/archive_manager.py`** | All archive operations: scan existing codes/max-SEQ/providers, append new parcels, check coordinate duplicates, backup, correct coordinates, extract single-parcel exports from batch files, update cadastre_code. | `echo '{"action":"scan","country_code":"CN","date":"260610"}' \| python3 scripts/archive_manager.py` |
| **`scripts/csv_builder.py`** | Build both Vertices CSV (顶点表) and Boundary CSV (边界表) from structured parcel data. Writes to `ovitalmap_exports/{CC}/`. Can also build single-parcel CSVs for archive hits. | `echo '{"parcels":[{...}],"first_code":"CN-260610-001","count":2,"country_code":"CN"}' \| python3 scripts/csv_builder.py` |
| **`scripts/provider_matcher.py`** | Fuzzy-match a provider name against existing names (exact, whitespace, honorific, substring, pinyin). Returns `ambiguous` flag when multiple candidates match equally. | `echo '{"input_name":"李总","existing_names":["中非李总","张三"]}' \| python3 scripts/provider_matcher.py` |
| **`scripts/parcel_pipeline.py`** | **Main orchestrator.** Runs the full flow in steps. Step 1 = country+provider (read-only), Step 2b = duplicate check → reuse matched codes (read-only), Step 2 = code assignment for new parcels (read-only), Step 3 = CSV build for all + archive for new (writes files). | `echo '{"parcels":[{...}],"date":"260610","resolved_provider_name":"张三"}' \| python3 scripts/parcel_pipeline.py --step 2b` |

### Script principles

- Run scripts via `RunCommand` and read their stdout JSON for results.
- All scripts produce machine-parseable JSON output for the LLM to consume and present to the user.
- **Use `python3`** as the interpreter.
- Do not inline large data transformations in the conversation — delegate to scripts.
- **LLM has the final say.** Scripts are tools, not authorities. If a script's output looks wrong — implausible country, mismatched provider, duplicate not caught, garbled coordinates, unreasonable SEQ jump — the LLM **must** inspect the result, flag anomalies to the user, and override or re-run with corrections when appropriate. Do not silently trust script output.

### Recommended workflow

The LLM should orchestrate the pipeline **step-by-step** using `parcel_pipeline.py`:

1. **After the user confirms coordinates and provider:** run `--step 1` → get country code, country name, and provider match results.
2. **Before code assignment — duplicate check:** run `--step 2b` → coordinate-based duplicate check against archive. Archive hits **reuse the existing `parcel_code`** (no new code assigned). Non-hits proceed to step 2.
3. **Assign codes for new parcels:** run `--step 2` → sequential codes for genuinely new parcels only.
4. **After the user confirms codes and any archive hits are resolved:** run `--step 3` → CSV generation for **ALL parcels** (batch for new, single-file for hits) + archive append (**new parcels only**).

Alternatively, call individual scripts for targeted operations (e.g., `provider_matcher.py` alone when only checking a provider name).

---

## 1) Inputs and Core Assumptions

- **Input**: one or more images or text blocks that contain parcel vertex coordinates.
- **Coordinate parsing**: auto-detect format:
  - Decimal degrees: `22.50422, 114.13472`
  - DMS: `22°30'15.2"N, 114°08'05.0"E`
  - UTM with zone and hemisphere
  - Other formats on a best-effort basis
- **WGS84 policy**:
  1. Always display the raw recognized coordinates verbatim per parcel.
  2. Always display WGS84 decimal-degree coordinates (convert if needed).
- **Date token (YYMMDD)**:
  - Use user-provided date if given.
  - Else use today's local date.
- **CSV format**: UTF-8, comma-separated, no BOM.

---

## 2) Country and Parcel Codes

### 2.1) Country Code
- **The LLM determines the country.** The `country_locator.py` script only normalizes coordinates; it does NOT perform geocoding. Use your spatial knowledge: match coordinate ranges against the world map, combine with any country names visible in documents, administrative regions mentioned, or the user's stated location.
- **State it, don't ask.** Present your determination (e.g. "根据坐标判断，该地块位于中国 (CN)") and proceed. Do NOT ask "which country?" — the user will correct if wrong.
- Default standard: **ISO 3166-1 alpha-2** (e.g., CN, HK, US, FR).
- **Cross-border parcels**: assign to the country where the majority of the parcel falls. Do not split.

### 2.2) Parcel Code — Always Generated

**Every parcel MUST receive a `parcel_code`.** There is no "no code" fallback.

The code follows one of two formats, with priority given to official registration IDs:

| Priority | Source | Format | Example |
|----------|--------|--------|---------|
| 1 (preferred) | Official registration ID found in **image text or explicitly provided by user** | `{CC}-{OFFICIAL_ID}` | `CN-PE12345`, `AU-EL9876` |
| 2 (default) | Auto-generated sequential code | `{CC}-{YYMMDD}-{SEQ}` | `CN-260609-003`, `HK-260609-001` |

Where `{CC}` is the **ISO 3166-1 alpha-2** country code.

**Official registration ID detection:**
- Scan any user-provided text, image OCR output, chat context, attached documents, or any other input modality for candidate registration / permit / cadastre numbers.
- If a clear mining cadastre / registration / permit number appears, present it to the user for confirmation before adopting it.
- If multiple candidate IDs appear for the same parcel, pick the most specific one and ask the user to confirm.

### 2.3) Uniqueness Check (Mandatory Before Code Assignment)

**Before finalizing any `parcel_code`,** you MUST scan the existing archive to prevent duplicates. This is critical because:
- Users may upload multiple parcels in one session or across separate sessions on the same day.
- A new session must NOT restart SEQ from 001 — it must continue from the last used number.

**Procedure:**

1. Scan `ovitalmap_archive/{CC}_parcels.csv` (if it exists) — this is the single source of truth.
2. Extract all existing `parcel_code` values from the archive.
3. For **official registration IDs** (format 1): check that `{CC}-{OFFICIAL_ID}` does NOT already exist. If it does, warn the user and ask for clarification.
4. For **sequential codes** (format 2): find the maximum SEQ already used for today (`{CC}-{YYMMDD}-*`). The new SEQ = max_existing + 1. If none exist for today, SEQ starts at `001`.
5. If the archive file does not exist yet, SEQ starts at `001`.

---

## 3) Output Files Overview

Two CSVs are produced together for the batch:

| # | File | Description |
|---|------|-------------|
| 1 | **Vertices CSV** (顶点表) | Every parcel vertex |
| 2 | **Boundary CSV** (边界表) | Every parcel as a closed polygon |

### 3.1) File Naming & Layout

Store generated CSVs in **country subdirectories** under `ovitalmap_exports/`:

```
ovitalmap_exports/{CC}/
```

Every export filename includes a `YYMMDD_HHMMSS` timestamp to prevent collisions even across re-exports or parallel sessions:

| File | Pattern |
|------|---------|
| Vertices CSV | `{firstCode}_N{count}_{YYMMDD_HHMMSS}.csv` |
| Boundary CSV | `{firstCode}_N{count}_{YYMMDD_HHMMSS}_boundary.csv` |

- `firstCode` = the `parcel_code` of the first parcel in this batch.
- `count` = total number of parcels in this batch.
- `YYMMDD_HHMMSS` = export timestamp at file-write time.

Examples:
- `CN-260609-001_N2_260609_143021.csv` — batch of 2, first is 001.
- `CN-PE12345_N1_260609_143522.csv` — single parcel with an official registration code.

### 3.2) Mandatory User-Facing Delivery Wording

Whenever sending generated CSV files to the user, explicitly identify which file is the **顶点表** and which file is the **边界表**. Do not rely on filenames alone.

**Mandatory file delivery:** After generating CSVs, send/attach the actual CSV files to the user. Do not only mention filenames in text. If the current runtime cannot attach files directly, provide the exact generated file paths or downloadable links and explicitly state that these are the files the user should download/import.

Always include the import instructions below with the delivered files:

```text
CSV 文件已生成并已随消息发送，请按下面方式导入奥维地图：

顶点表（用于导入为“标签”，显示各个边界顶点）：
- 文件：`{vertices_filename}`（已发送/已附上）
- 导入方法：用奥维地图打开顶点表文件，在导入 CSV 时选择“标签”，进入“导入标签”页面后点击右上角“确定”，然后在“导入对象”页面选择“导入”，最后在“导入选项”中选择“确定”。

边界表（用于导入为“轨迹”，显示完整边界线）：
- 文件：`{boundary_filename}`（已发送/已附上）
- 导入方法：用奥维地图打开边界表文件，在导入 CSV 时选择“轨迹”，进入“导入轨迹”页面后点击右上角“确定”，然后在“导入对象”页面选择“导入”，最后在“导入选项”中选择“确定”。
```

For multiple batches or archive-hit exports, repeat this block per pair, or list all 顶点表 files under the 顶点表 section and all 边界表 files under the 边界表 section. The user must never have to infer the import type from `_boundary` or any filename pattern.

---

## 4) Vertices CSV (顶点表)

Headers (exact, in order, **do not translate**):

```
文件夹,名称,经度,纬度,海拔,文本显示风格,图标样式,Comment
```

### Field Rules

| Field | Rule |
|-------|------|
| **文件夹** | `{parcel_code}` — always |
| **名称** | `{parcel_code}_A{vertex-index}`. `vertex-index` starts at **A01** and increases by original vertex order |
| **经度** | WGS84 decimal longitude. Preserve sign and precision. **No rounding.** |
| **纬度** | WGS84 decimal latitude. Preserve sign and precision. **No rounding.** |
| **海拔** | Fill if present in input; else leave **empty** |
| **文本显示风格** | Empty by default |
| **图标样式** | Default `1` |
| **Comment** | `提供者:{provider_name} 归档日期:{archive_date}`. If a `cadastre_code` exists (user-provided official ID or explicit code), append ` 地籍号:{cadastre_code}`. Applies to all parcels uniformly. |

### Indexing conventions
- `vertex-index` resets from **01 per parcel** (A01, A02, …).
- Preserve original vertex order. If ordering is unclear, ask the user about **clockwise reordering**.

---

## 5) Boundary CSV (边界表)

Headers (exact, in order, **do not translate**):

```
文件夹,名称,经纬度[经度+纬度],线条宽度,线条颜色,线条不透明度,闭合,线型,轨迹风格,Comment
```

### Field Rules

| Field | Rule |
|-------|------|
| **文件夹** | Same as Vertices CSV |
| **名称** | `{parcel_code}` — the bare parcel code, no `_A01` vertex suffix. The boundary represents the whole polygon. |
| **经纬度[经度+纬度]** | Concatenate as `lon,lat;lon,lat;…` (no spaces) following Vertices order. Close the polygon by repeating the first vertex at the end if the input does not already close it. |
| **线条宽度** | Default `3` |
| **线条颜色** | Default `0X00FF0000` |
| **线条不透明度** | Default `50` |
| **闭合** | Default `1` |
| **线型** | Default `0` |
| **轨迹风格** | Default `1` |
| **Comment** | `提供者:{provider_name} 归档日期:{archive_date}`. If a `cadastre_code` exists (user-provided official ID or explicit code), append ` 地籍号:{cadastre_code}`. Applies to all parcels uniformly. |

---

## 6) Quality Checks and Special Cases

1. **Range checks**: longitude ∈ [-180, 180], latitude ∈ [-90, 90]. Flag any violations explicitly.
2. **Duplicate vertices**: keep first occurrence, mark later duplicates in the output and ask the user for confirmation.
3. **Cross-border parcels**: use the country where the majority area falls (§2.1). Do not split.
4. **Missing altitude**: leave the field empty; never infer or guess.
5. **Naming collisions**: if 文件夹 + 名称 duplicates occur, report the collision to the user.
6. **Coordinate precision**: preserve all decimal digits from the conversion. Do not round.
7. **Existing-parcel duplicate detection (MANDATORY before archiving)**: Before writing a new parcel to the archive, check whether a parcel with the **same set of vertex coordinates** already exists in the archive using `archive_manager.py check_duplicate`. Comparison rules:
   - The same vertices in **any** cyclic permutation or reversal (different starting point, clockwise vs counterclockwise) are considered equal.
   - If a match is found, **do NOT generate new CSVs or re-archive**. Instead, follow the **archive-hit workflow** (§6.8).
8. **Archive-hit workflow**: When `check_duplicate` finds a coordinate match in the archive, follow this procedure:
   a. Report the match to the user with the existing `parcel_code` and provider.
   b. **Reuse the existing `parcel_code`** — do NOT assign a new code.
   c. **Provide the existing archived document to the user** — regenerate single-parcel CSV files (`{parcel_code}_N1_{timestamp}.csv` + `_boundary.csv`) in `ovitalmap_exports/{CC}/` with full Comment metadata (provider, archive date, cadastre code if available). Never return other parcels' data alongside the archive-hit parcel.
   d. **Cadastre code update**: If the existing parcel only has a generic date-based code (e.g., `CN-260609-001`) and the user is now providing an official registration ID, update the `cadastre_code` field in the archive (both per-country and master) with the new official ID. Use `archive_manager.py update_cadastre` for this. The regenerated CSV will then include `地籍号:{official_id}` in the Comment.
   e. **Do not re-archive** the parcel.
   f. If the user explicitly says it is a **different parcel** despite identical coordinates, archive normally with a note in `provider_notes`: `"Coordinates identical to {existing_code}; user confirmed it is a different parcel."`.
9. **Batch with mixed hits**: If the user provides multiple parcels and some hit the archive while others are new:
   - Archive-hit parcels → **reuse existing `parcel_code`**, regenerate single-parcel CSVs with Comment metadata, update cadastre_code if applicable.
   - New parcels → assign codes, generate batch CSVs, and archive normally.
   - The two groups are processed independently. Present results separately to the user.

---

## 7) Archiving and Categorization (Database)

**After generating the CSVs for a parcel**, you MUST archive the parcel into the workspace database.

### 7.1) Archive Location

All archives live flat in `ovitalmap_archive/` at the workspace root. One file per country:

```
ovitalmap_archive/{CC}_parcels.csv
```

If the file does not exist yet, create it with headers.

### 7.2) Archive CSV Headers

```
parcel_code,provider_name,archive_date,boundary_coords,provider_notes,cadastre_code
```

### 7.3) Field Rules for Archiving

| Field | Rule |
|-------|------|
| **parcel_code** | Assigned per §2.2–2.3. Always populated. |
| **provider_name** | The name of the person/organization who provided this parcel. **MUST ask the user** for at least a name. If the user mentions a series of similar names, confirm with them before archiving. If they mention none of the names you suggest, treat it as a new provider. |
| **archive_date** | Date of archiving in YYYY-MM-DD format |
| **boundary_coords** | Full boundary string in the format `lon,lat;lon,lat;…` (same as Boundary CSV 经纬度 field). This is the canonical coordinate storage. |
| **provider_notes** | Any additional notes about the provider or context; empty by default |
| **cadastre_code** | Populate with **any official registration / cadastre / permit ID** from government documents, regardless of whether it is used as the `parcel_code`. This includes: mining cadastre numbers, land registration IDs, permit numbers, or any government-issued parcel identifier — from images, OCR, documents, or explicit user input. When `parcel_code` uses format 1 (`{CC}-{OFFICIAL_ID}`), the `{OFFICIAL_ID}` portion MUST also be stored here. Leave empty only when no official ID exists. The pipeline's `step2_assign_codes()` ensures this automatically when `official_id` is present. |

### 7.4) Provider Name Workflow

1. **At Step 1** (before any code assignment or file writing), ask the user: **"Who provided this parcel? (请提供此地块的提供者姓名)"**
2. After the user provides a name, **immediately scan all existing providers** from both:
   - `ovitalmap_archive/{CC}_parcels.csv` (per-country archive)
   - `ovitalmap_archive/master.csv` (cross-country archive)
3. **Proactive fuzzy deduplication** — compare the user-supplied name against every existing provider via `provider_matcher.py`. Accept the provider only when `exact_match` is found or after explicit user confirmation. The script returns:
   - `exact_match`: the name if an exact match exists.
   - `candidates`: list of `{name, reason, score}` sorted by score.
   - `ambiguous`: `true` when there are **multiple candidates with equal scores** (i.e., the script cannot determine a definitive match — the LLM MUST ask the user).

   Match types recognized by the script:
   - **Exact match** (score 100): identical string after case-insensitive normalization and whitespace/punctuation removal (e.g., `"Zhang San"` ≈ `"Zhang-San"` ≈ `"ZhangSan"`). The script's `_normalize()` function handles this before comparison.
   - **Chinese ↔ Pinyin match** (score 90): one is Chinese characters and the other is the corresponding pinyin (e.g., `"张三"` ≈ `"zhangsan"`).
   - **Cross-language pinyin** (score 85): one name has Chinese with its pinyin matching the other's normalized form.
   - **Substring overlap** (score 80): one name is fully contained within another, checked both with and without honorific stripping (e.g., `"李总"` ⊂ `"中非李总"`).
   - **Honorific variation** (score 75): names differ only by a common Chinese honorific or prefix (e.g., `"李总"` ≈ `"李"` after stripping `"总"`).

4. **Handle matches with mandatory user confirmation for non-exact matches:**
   - **Exact match** (score 100 / reason `exact`): automatically reuse the existing `provider_name` spelling. No user confirmation needed.
   - **Single candidate** (score ≥ 80, single candidate, not ambiguous): ask the user explicitly:
     > **"检测到提供者 '{input_name}' 与已有记录 '{existing_name}' 高度相似。是否为同一个人？"**
     - If the user confirms **same person** → reuse the existing `provider_name` spelling.
     - If the user says **different person** → treat as a new provider.
     - If the user is unsure → keep the new name but add a note in `provider_notes`: `Possible duplicate of '{existing_name}'.`
   - **Low-confidence candidate** (score 50-79, single candidate, not ambiguous): ask the user but note the lower confidence:
     > **"检测到提供者 '{input_name}' 与已有记录 '{existing_name}' 可能相似（置信度较低）。是否为同一个人？"**
     - Same confirmation flow as above.
   - **Multiple candidates / ambiguous** (e.g., user says `"李总"`, archive has `"中非李总"` and `"三一李总"`): **MUST list ALL candidates and ask the user to specify.** Do not guess:
     > **"'{input_name}' 在已有记录中匹配到多位提供者：① {candidate1}  ② {candidate2}。请问对应的是哪一位？或都不是(新建)？"**
     - If the user picks one → reuse that existing `provider_name`.
     - If the user says none of them → treat as a new provider.
   - **No match / score < 50**: automatically add as a new provider. No confirmation needed.

5. If the user declines to provide a name, use `"Unknown"` and note it.
6. **Do not proceed to code assignment until provider name is confirmed.**

---

## 8) Master Spreadsheet

After archiving to `ovitalmap_archive/{CC}_parcels.csv`, **also append the same row(s)** to a single consolidated file:

```
ovitalmap_archive/master.csv
```

This is a **single spreadsheet containing every parcel from every country** — the complete cross-country view.

**Headers** (one extra column vs per-country `parcels.csv`):

```
CC,parcel_code,provider_name,archive_date,boundary_coords,provider_notes,cadastre_code
```

Append every newly archived parcel row here immediately after writing to the per-country file. If `master.csv` does not exist, create it with headers.

---

## 9) Interaction Flow

### Guard Rule

**Do NOT write or modify any file until user confirms BOTH coordinates AND provider name.** Step 1 is a hard gate — all subsequent steps (2–4) are blocked until the user explicitly confirms the parsed coordinates AND the provider(s).

When invoked, follow this sequence:

### 1. Parse, Verify & Confirm Provider
- Show raw coordinates and WGS84 conversion per parcel.
- **Ask for the provider name(s)** (§7.4). Identify each parcel's provider.
- Display ⚠️ **"请核实以下识别和转换后的坐标是否与原始数据一致，并确认提供者姓名"**.
→ **STOP HERE. Wait for user to confirm or correct coordinates AND provider.** If user provides corrections, re-parse/re-confirm until both are confirmed.

### 2b. Duplicate Check (MANDATORY — runs before code assignment)
- **Determine country** from coordinates using your spatial knowledge, plus any country names in documents or user context. State it and move on.
- Run `parcel_pipeline.py --step 2b` for each parcel.
- **Archive-hit parcels**: reuse the **existing `parcel_code`** from the archive (no new code). Detect any official registration IDs from image text or user input; if the matched parcel has a generic date-code and no `cadastre_code` yet, update it via `archive_manager.py update_cadastre`. Display: `"检测到地块坐标与已有记录 {matched_code} 一致，沿用归档编码。"`.
- **New parcels**: proceed to step 2.

### 2. Assign Codes (only for new parcels, only after step 2b)
- **Official registration IDs take priority**: if any parcel has a confirmed official registration / cadastre ID (from documents, OCR, or explicit user input), use format 1: `{CC}-{OFFICIAL_ID}` as the `parcel_code`. The `{OFFICIAL_ID}` is also stored as `cadastre_code`.
- For parcels **without** an official ID: run `parcel_pipeline.py --step 2` to get format 2 sequential codes `{CC}-{YYMMDD}-{SEQ}`.
- Display all assigned codes. The user will correct if wrong.

### 3. Build CSVs (for ALL parcels)
Build **both** Vertices CSV (§4) and Boundary CSV (§5) for every parcel:
- **New parcels**: batch CSV (e.g., `{firstCode}_N{count}_{timestamp}.csv` + `_boundary.csv`).
- **Archive-hit parcels**: individual single-parcel CSVs (e.g., `{matchedCode}_N1_260609_143021.csv` + `_boundary.csv`) regenerated with updated Comment metadata.

Run quality checks (§6), send/attach the actual generated CSV files to the user, then use the mandatory delivery wording from §3.2:

> CSV 文件已生成并已随消息发送，请按下面方式导入奥维地图：
>
> 顶点表（用于导入为“标签”，显示各个边界顶点）：
> - 文件：`{firstCode}_N{count}_{timestamp}.csv`（已发送/已附上）
> - 导入方法：用奥维地图打开顶点表文件，在导入 CSV 时选择“标签”，进入“导入标签”页面后点击右上角“确定”，然后在“导入对象”页面选择“导入”，最后在“导入选项”中选择“确定”。
>
> 边界表（用于导入为“轨迹”，显示完整边界线）：
> - 文件：`{firstCode}_N{count}_{timestamp}_boundary.csv`（已发送/已附上）
> - 导入方法：用奥维地图打开边界表文件，在导入 CSV 时选择“轨迹”，进入“导入轨迹”页面后点击右上角“确定”，然后在“导入对象”页面选择“导入”，最后在“导入选项”中选择“确定”。
>
> 已有地块单独导出时，也必须先发送/附上对应文件，再按同样格式说明，并替换为对应的单地块文件名：
> - 顶点表文件：`{matchedCode}_N1_{timestamp}.csv`
> - 边界表文件：`{matchedCode}_N1_{timestamp}_boundary.csv`

### 4. Archive (only for new parcels)
- Append to `ovitalmap_archive/{CC}_parcels.csv` and `ovitalmap_archive/master.csv`.
- Summarize: provider, codes, date.

### 5. Wrap Up
Note any assumptions, edge cases, or corrections. Separately list archive-hit exports and any cadastre_code updates.

---

## 9b) Post-Archive Coordinate Correction

Users may correct a parcel's coordinates after it has been archived. When this happens:

### Procedure

1. **Identify the parcel** by its `parcel_code` in `ovitalmap_archive/{CC}_parcels.csv` and `ovitalmap_archive/master.csv`.

2. **Backup before modifying** — copy the current archive files to a backup:

   ```
   ovitalmap_backups/{CC}_parcels_{YYMMDD_HHMM}.csv
   ovitalmap_backups/master_{YYMMDD_HHMM}.csv
   ```

   Create `ovitalmap_backups/` if it does not exist.

3. **Update the row** in the per-country archive and master spreadsheet:
   - Replace `boundary_coords` with the corrected boundary string.
   - Update `archive_date` to the current date (marking the correction date).
   - Append a note to `provider_notes`: `"[{date}] Coordinates corrected. Original backup: {backup_file}"`.

4. **Regenerate the export CSVs** for the corrected parcel in `ovitalmap_exports/{CC}/`.

5. **Summarize** what was changed, where backups are, and ask the user to verify.

---

## 10) Example Output Snippet

```
⚠️ 请核实以下识别和转换后的坐标是否与原始数据一致，并确认提供者姓名

原始坐标:
• 地块 1: 22°30'15.2"N, 114°08'05.0"E; 22°30'14.8"N, 114°08'08.3"E; …
• 地块 2: 22.50422, 114.13472; 22.50418, 114.13480; …

WGS84:
• 地块 1: 114.13472, 22.50422; 114.13564, 22.50411; …
• 地块 2: 114.13472, 22.50422; 114.13500, 22.50416; …

请提供此地块的提供者姓名？

确认坐标无误并确认提供者后继续处理？(如有修正请提供)

→ 用户确认坐标 + 提供者: 中非李总

所属国家: 中国 (CN)

正在检查重复…
  ✓ 地块 1: 无重复
  ✓ 地块 2: 无重复

正在扫描 CN 存档…
  现有编码: CN-260609-001, CN-260609-002

检测到地块 2 的官方登记号 PE12345 → 采用格式 1 编码

  → 地块 1 → CN-260609-003（无官方编号，顺序编码）
  → 地块 2 → CN-PE12345（官方登记号）

最终编码:
• 地块 1: CN-260609-003（新增）
• 地块 2: CN-PE12345（新增，cadastre_code: PE12345）

CSV 文件已生成并已随消息发送，请按下面方式导入奥维地图：

顶点表（用于导入为“标签”，显示各个边界顶点）：
• 文件：CN-260609-003_N2_260609_143021.csv（已发送/已附上）
• 导入方法：用奥维地图打开顶点表文件，在导入 CSV 时选择“标签”，进入“导入标签”页面后点击右上角“确定”，然后在“导入对象”页面选择“导入”，最后在“导入选项”中选择“确定”。

边界表（用于导入为“轨迹”，显示完整边界线）：
• 文件：CN-260609-003_N2_260609_143021_boundary.csv（已发送/已附上）
• 导入方法：用奥维地图打开边界表文件，在导入 CSV 时选择“轨迹”，进入“导入轨迹”页面后点击右上角“确定”，然后在“导入对象”页面选择“导入”，最后在“导入选项”中选择“确定”。

--- 归档 ---

归档完成:
• 地块编号: CN-260609-003, CN-PE12345
• 提供者: 中非李总
• 归档日期: 2026-06-09
```

### Example: Archive Hit

```
→ 用户确认坐标 + 提供者: 王五

所属国家: 中国 (CN)

正在检查重复…
  ⚠️ 地块 1: 检测到坐标与已有记录 CN-260609-001 (提供者: 张三) 一致
     → 沿用归档编码: CN-260609-001
     → 该地块未被重新归档。

CSV 文件已生成并已随消息发送，请按下面方式导入奥维地图：

顶点表（用于导入为“标签”，显示各个边界顶点）：
• 文件：CN-260609-001_N1_260609_143522.csv（已发送/已附上）
• 导入方法：用奥维地图打开顶点表文件，在导入 CSV 时选择“标签”，进入“导入标签”页面后点击右上角“确定”，然后在“导入对象”页面选择“导入”，最后在“导入选项”中选择“确定”。

边界表（用于导入为“轨迹”，显示完整边界线）：
• 文件：CN-260609-001_N1_260609_143522_boundary.csv（已发送/已附上）
• 导入方法：用奥维地图打开边界表文件，在导入 CSV 时选择“轨迹”，进入“导入轨迹”页面后点击右上角“确定”，然后在“导入对象”页面选择“导入”，最后在“导入选项”中选择“确定”。
  (Comment: 提供者:张三 归档日期:2026-06-02)

--- 归档 ---
无新增记录。已有地块 CN-260609-001 未被重复归档。
```

---

## 11) File Structure

```
skill folder/
├── SKILL.md                       # Skill instructions
├── skill-card.md                  # ClawHub listing card
└── scripts/                       # Python utility scripts (§0b)

runtime workspace root/
├── ovitalmap_exports/             # Generated CSVs (by country subdir)
│   ├── CN/
│   │   └── CN-260609-001_N2_260609_143021.csv
│   ├── HK/
│   │   └── HK-260609-001_N1_260609_143522.csv
│   └── …
├── ovitalmap_archive/             # Persistent database (flat)
│   ├── master.csv                 # All parcels, all countries
│   ├── CN_parcels.csv
│   ├── HK_parcels.csv
│   └── …
├── ovitalmap_backups/             # Pre-correction snapshots (§9b)
│   ├── CN_parcels_260609_1430.csv
│   └── master_260609_1430.csv
```
