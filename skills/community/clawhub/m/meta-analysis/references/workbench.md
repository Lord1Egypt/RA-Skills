# Workbench — published app & local launch

> Extracted from SKILL.md §2.5. Last sync: v2.17.1.

## 2.5 Workbench — the HTML interactive frontend for full-flow

> **Positioning:** `adapters/workbench/` holds the full workbench frontend (`workbench.html`, three-column layout) + backend (`server.py`) + launcher (`launch_workbench.py`).
> **Trigger:** the user mentions "工作台" / "workbench" / "meta 全流程" etc.

**Published application (WorkBuddy Sites):** The workbench is published as a WorkBuddy online app. **When re-publishing, always reuse the existing `appId` to keep the share link stable — never create a new app.**

> 🔴 **Registered exception to the ct-base iron rule** (2026-09-16, user-decided): every other skill publishes to
> `https://<skill-name>.app.workbuddy.host/`, but this skill's link is the **simplified** `https://meta.app.workbuddy.host/`
> (`domainPrefix = meta`, not the skill name). User's words: "但名称是简化的，**这个是特例**". This is the **only**
> whitelisted exception — see ct-base `references/workbench_ui.md` §13.0.1.

| Item | Value |
|---|---|
| Share link | `https://meta.app.workbuddy.host/` (same-host alias: `https://meta.app.workbuddy.link/`) |
| domainPrefix | `meta` — **simplified, whitelisted exception** (iron rule would say `meta-analysis`) |
| appId | `wbapp_hNZl928SI6wByvJt2COtcC` |
| sandboxId | `a3c70e48be8f45019845b76383334bfc` |
| Owner workspace | `2026-09-17-09-54-01` — holds `.wbapp_hNZl928SI6wByvJt2COtcC.genie` |
| Metadata record | `adapters/workbench/app.config.json` (ct-base §16.12.1; excluded from the published package) |
| Runtime | Python (`pip install -r requirements.txt` + `python main.py`) |
| Deploy directory | `meta-workbench-app/` (staging payload: `main.py` + `adapters/` + `scripts/` + `requirements.txt`) |
| Publish toolchain | `adapters/workbench/publish-kit/` — `build_publish.py` (rebuilds the payload), `install_genie.py` (mints/installs `.wbapp_<appId>.genie` + the `applications.yaml` entry so re-publishing keeps the same share link), `check_py311.py`, `smoke_e2e.py`. **Infrastructure, not a deploy source** — excluded from every outbound artifact. |
| ⛔ Deleted 2026-09-22 | `publish/` · `publish-backup/` · `publish-backup.rar` · `publish-preclean-20260917/` — frozen historical snapshots of the skill tree (~72 MB, untracked, **zero code references**). They predated `topic_translate.py` / `evidence_upload.py` / `reasons_en`, so they *looked* deployable but would have shipped the old version. Removed after the 2026-09-22 consistency audit (P2-12). Rebuild the payload any time with `python adapters/workbench/publish-kit/build_publish.py`. |

> ⚠️ **appId 认领地**: the deploy tool only accepts an `appId` whose `.wbapp_<id>.genie` marker exists in the **current**
> workspace. This app is registered in **`2026-09-17-09-54-01`** (verified 2026-09-22: `.wbapp_hNZl928SI6wByvJt2COtcC.genie`
> lives there). The previously documented workspace `2026-09-14-14-30-18` **no longer exists** — re-publishing from any
> workspace without the marker is rejected and would force `createNewApp` → a **suffixed** domain (e.g. `meta-02857`),
> which is a deviation, not an option. If the marker workspace changes again, locate it with:
> `ls -d ~/WorkBuddy/*/ | xargs -I{} sh -c 'ls {}/.wbapp_hNZl928SI6wByvJt2COtcC.genie 2>/dev/null'`

```bash
# Re-publish (update existing app — link unchanged)
# Must run from workspace 2026-09-17-09-54-01 (where the .wbapp_*.genie marker lives)
# workbuddy_sites_deploy with appId=wbapp_hNZl928SI6wByvJt2COtcC, domainPrefix=meta
```

```bash
# Launch the workbench locally (default 127.0.0.1:8765, auto-opens the browser)
python adapters/workbench/launch_workbench.py

# Or start the backend manually
cd adapters/workbench && coze/.venv/Scripts/python.exe -m uvicorn server:app --host 127.0.0.1 --port 8765
```

After launch, open the workbench in the preview panel with `present_files(["http://127.0.0.1:8765"])`.

## Workbench capabilities added 2026-09-22 (web ⇄ agent parity)

| Capability | Web | Agent / CLI context |
|---|---|---|
| 研究主题中→英自动翻译（喂 Europe PMC） | ✅ 选题速览 & C1 自动翻译并展示检索式（`adapters/topic_translate.py`，缓存 + 多端点降级） | same engine; agent may pass `topic_en` explicitly |
| 选题可行性速览文案 | 「先帮我选题」；探针失败显示「暂不可达 + 原因 + ↻ 重试」 | `flow_menu.py ... probe` |
| 演示模式（无 B 信封直接跑 C） | ✅ 三级兜底（粘贴 → 上传 → 内置示例）；页面有常驻「⚠ 演示数据」角标 | `block_b.demo_b_env()` |
| C1 上传作者自备文献 | ✅「初稿证据来源」面板（xlsx/csv/tsv / RIS / BibTeX / txt / zip / pdf） | `adapters/evidence_upload.py collect_uploads(paths)` |
| 软停「跳过本步确认」 | ✅ (2026-09-22 恢复显示) | ✅ CLI 菜单 `skipped` |
| 节点可修订字段 | 由 `await.editable_payload`（= `fullflow.EDITABLE_KEYS`）自动渲染；无专用面板的键给通用编辑框 | CLI 修订项同样由 `EDITABLE_KEYS` 派生 |

**Single source of truth for "what is editable at stage X"** = `adapters/fullflow.EDITABLE_KEYS`.
Both the web (`editable_payload` → generic panel) and the CLI menu derive from it — do **not** add a second list.
The workbench backend reuses the fullflow HITL state machine (red-line checks preserved verbatim); the frontend shows real-time progress and human-gate interactions across direction judgment → retrieval → screening → extraction → computation.
