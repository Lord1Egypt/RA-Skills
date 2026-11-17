# 研究筆記

## pob-cli

來源：https://github.com/qpooqp777/pob-cli 。目前 master commit 為 e96f2fc。工具面向 PoE1 PC Build，可讀取 PoB XML，並提供 `pob analyze`、`pob calc`、`pob tree`、`pob skills`、`pob items`、`pob compare`、`pob price`、`pob share --dry-run`、`pob optimize-tree` 與 `pob optimize-tree-matrix` 等命令。`pob calc` 會呼叫 Path of Building Community Fork 的 LuaJIT headless 核心，不能用 Python 簡化公式取代；精確計算需要 Python 3.11+、LuaJIT 與本機 PoB 原始碼。

`pob calc BUILD --pob-root POB_ROOT --skill SKILL --format json` 可輸出官方 PoB scalar，包括 Life、Energy Shield、Armour、Evasion、元素／混沌抗性、TotalDPS、TotalDoTDPS、TotalEHP、MaximumHitTaken 等。分析時必須明確指定主技能，避免把位移或防禦技能當成 DPS 技能。`pob skills --details` 可取得技能組、socket group、gem metadata 與 support relationship；`pob tree --all` 可列出完整天賦節點；`pob items` 可列出原始裝備與詞綴；`pob share --dry-run` 可產生角色分享 code 而不公開上傳。

流派 DB 的自動生成 XML 目前可能出現主技能載入問題；不能把自動生成的 XML 計算結果宣稱為可靠，除非先用 `pob calc` 成功驗證。技能應把角色 code 產生與官方 PoB 計算驗證分開，並保留 warnings。

## PoE Ninja

首頁目前重新導向至 https://poe.ninja/poe1/builds/，頁面主要內容由前端動態載入；不能依賴靜態 HTML。PoE Ninja 可依聯盟、職業、技能、物品、連線技能、被動技能、Keystone、Anoint、武器配置等條件篩選 Build。技能實作應優先使用可配置的 JSON／資料傾印或可確認的公開端點，若端點不存在則要求使用者提供 PoE Ninja 匯出的 JSON、角色頁或 PoB code，而不要盲目刮取動態頁面。

## 輸出原則

每個階段都要輸出：stage、level_range、main_skill、skill_links、passive_plan、equipment_targets、pob_metrics、assumptions、warnings。任何數值若沒有成功通過 PoB headless 計算，必須標註為估計或未驗證。交易價格屬市場快照，SSF 不得直接視為可取得性。

## 3.29 verification update

- GGG's official 3.29.0 patch-note page identifies the expansion and challenge league as **Path of Exile: Curse of the Allflame**, with Standard, Hardcore, and Solo Self-Found variants.
  Source: https://www.pathofexile.com/forum/view-thread/3985332
- The public PoE Ninja PoE1 builds page exposes navigation to Builds, Statistics, Data dumps, and Docs & FAQ, but its main build content is client-rendered and should not be treated as static HTML data.
  Source: https://poe.ninja/poe1/builds

### Operational consequence

Use `Curse of the Allflame` as the human-readable 3.29 example, but verify the exact league identifier before querying. Record retrieval timestamp, filters, sample size, and whether the snapshot is historical or current.

Do not hard-code a single "best" build from search snippets or video titles. Generate a 3.29 recommendation from an explicit Ninja data snapshot, then filter by league, class/ascendancy, main skill, level, cost, and defensive requirements, and verify with Path of Building Community through `pob-cli` when valid XML and PoB root are available.

## 3.29 API connection test and CLI verification

### PoE Ninja build endpoint

The previously documented URL shape

```text
https://poe.ninja/api/data/builds?overview=<league>&type=exp
```

was probed on 2026-08-18 with `allflame`, `Allflame`, `CurseOfTheAllflame`, and `Curse of the Allflame`. All four requests returned HTTP 404. Therefore this endpoint shape is **unverified / unavailable for the current public service**, not a working 3.29 API. The pipeline must not silently retry it as authoritative. Prefer a user-provided JSON export, a permitted data dump, a confirmed endpoint from PoE Ninja documentation, or a public PoB XML/character source. Preserve the failed URL, HTTP status, and timestamp in report warnings.

The official PoE Ninja data page documents raw economy dumps rather than build snapshots. Its download pattern is:

```text
https://poe.ninja/poe1/api/data/dumps/dump?name=<league-name>
```

The page states that ZIP files contain semicolon-separated CSV data points. This is useful for price snapshots, but does not prove that a full passive-tree/build JSON is available through the same route. Source: https://poe.ninja/poe1/data

### Verified `pob-cli` commands

The checked-out `qpooqp777/pob-cli` documentation confirms:

```bash
pob skills build.xml
pob tree build.xml
pob items build.xml
pob calc build.xml --pob-root "$POB_ROOT" --skill "MAIN SKILL" --format json > baseline.json
pob analyze build.xml --pob-root "$POB_ROOT" --skill "MAIN SKILL" --format json > analysis.json
pob compare current.xml candidate.xml
pob price "Divine Orb" --league allflame
pob share build.xml --dry-run > share-code.txt
```

`pob calc` and JSON/Markdown `pob analyze` can call the Path of Building Community Fork Headless Lua core when the XML, LuaJIT runtime, and `POB_ROOT` are valid. Use `--timeout 300` for complex builds. Run `pob skills` before calculation to resolve the exact active-skill name. Use `pob compare` for basic defence comparison, and calculate both XML files separately when comparing DPS, TotalEHP, MaximumHitTaken, or configuration-dependent output.

`pob share BUILD.xml` uploads a public `pobb.in` URL. `pob share --dry-run` only emits the compressed URL-safe code and must be the default in automated tests. Keep code generation separate from public upload.

### Test fixture policy

A Ninja 404 response or missing PoB XML is a valid negative test, but cannot produce an actually verified build. A provisional 3.29 starter fixture may be generated from a local JSON snapshot and hand-authored stage plan; it must carry `source.status=provisional` and warnings. It must not claim official PoB metrics until `pob calc` succeeds.

Sources:

- https://poe.ninja/poe1/data
- https://github.com/qpooqp777/pob-cli/blob/master/CLI_USAGE.md
- https://github.com/qpooqp777/pob-cli/blob/master/POB_CLI_VALIDATION.md

## pobb.in Python upload verification

The checked-out pobb.in source confirms that the public upload route is `POST https://pobb.in/pob/`. It accepts the URL-safe Base64 representation of a **zlib-wrapped Deflate stream**, not a raw Deflate stream. Its server decodes Base64, passes the bytes through a `ZlibDecoder`, then parses the resulting PoB XML. Therefore the existing Python `zlib.compress(xml)` approach is correct at the compression layer; switching to raw `wbits=-15` is incorrect for this service.

The same source shows the newer internal JSON endpoint `POST /api/internal/paste/`, whose `content` field is raw PoB XML rather than a share code. The direct `/pob/` endpoint returns HTTP 400 when decompression or PoB XML schema validation fails. A successful local `pob calc` is not sufficient proof that the XML satisfies pobb.in's stricter serialized PoB schema. Source: https://github.com/Dav1dde/pasteofexile

Operational consequence: retain `zlib.compress` in `pob-cli`, and repair the generated XML schema before retrying the three public uploads. Do not report a pobb.in URL for an HTTP 400 response.
