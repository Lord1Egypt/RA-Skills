# OurGroceries skill — release notes

## 1.0.0 (2026-04-27)

### Summary for OpenClaw agent (handoff)

**Credentials:** Do not store real usernames/passwords in repo files. OpenClaw should inject `OURGROCERIES_EMAIL` and `OURGROCERIES_PASSWORD` at runtime (vault, host env, etc.). An optional gitignored `env` file may exist for local dev only; `scripts/load_skill_env.py` uses `setdefault` and must not override OpenClaw-provided vars.

---

#### Goal

Align the skill with the **current OurGroceries web API** (especially **auto-categorize** and **list overview**), without depending on the stale PyPI **`ourgroceries`** package.

#### What was implemented

1. **Vendored HTTP client** at `lib/ourgroceries/`  
   - Forked from [py-our-groceries](https://github.com/ljmerza/py-our-groceries), then patched.  
   - **Do not `pip install ourgroceries`** for this skill; scripts prepend `lib/` on `sys.path`.

2. **API / behavior fixes (vendored `__init__.py`)**  
   - **`getLists`** (replaces legacy `getOverview`); payload must include **`knownLists`** (use **`[]`** for a full refresh).  
   - **`get_item_category(item_name, note='', guess=True)`** → POST **`getItemCategory`** (matches the web app).  
   - **`add_item_to_list(..., auto_category=True)`** → calls **`getItemCategory`**, then **`insertItem`** with returned **`categoryId`** (plus fields aligned with the browser). Fallback: omit `categoryId` if the guess returns nothing.  
   - **`login()`** returns **`True`** on success.  
   - **`_post`**: parse JSON with **`content_type=None`**; **`raise_for_status()`** on HTTP errors.

3. **Scripts** (`scripts/add_item.py`, `get_list.py`, `remove_item.py`, `test_connection.py`)  
   - Import the **vendored** client from `lib/`.  
   - **`get_my_lists` response**: use **`lists`**, with fallback to **`shoppingLists`**.  
   - **`remove_item.py`**: normalize **`get_list_items`** to dict rows; use **`item['id']` / `item['name']`**.

4. **Optional local `env` file**  
   - **`scripts/load_skill_env.py`** loads skill-root **`env`** with **`setdefault`** only.  
   - **`env`**, **`.env`**, **`.env.local`** are **gitignored**.

5. **Deps**  
   - **`requirements.txt`**: **`aiohttp`** only. **`.venv/`** gitignored.

6. **Dev / debugging**  
   - **`scripts/devtools_network_monitor.js`**: browser console snippet to log POST JSON to `/your-lists`.

7. **Docs**  
   - **`SKILL.md`** — human setup and examples.  
   - **`AGENTS.md`** (skill + workspace `AGENTS.md`) — agent implementation notes (`knownLists`, `lists`, etc.).

#### Removed

- Ad-hoc test scripts (`test_auto_category_unit.py`, `smoke_live_auto_category.py`, `simple_test.py`).

#### How to run

- Ensure **`OURGROCERIES_EMAIL`** and **`OURGROCERIES_PASSWORD`** are set in the process environment (OpenClaw).  
- `pip install -r requirements.txt` (venv recommended).  
- Example: `python3 scripts/add_item.py "item name" -l "List name"` (`add_item.py` uses auto-categorize).

#### Testing

- Human decides whether to test as-is after credentials are wired. Quick checks: `scripts/test_connection.py`, then `add_item.py` against a real list name.
