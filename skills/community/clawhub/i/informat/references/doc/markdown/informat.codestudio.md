<!-- DOCKEY: cst-2f7b9 -->
# AI Code Studio Development Guide (for the general agent)

AI Code Studio is the Informat platform's **full Vue 3 + Vite frontend project** module. It is far more capable than the website module and is meant for **interactive, component-based frontends with routing/state/charts** (admin panels, data dashboards, business pages, etc.).

This guide teaches you (the general agent) how to build a codestudio app from scratch in a normal conversation using the `_codestudio_*` tools. **All `_xxx` methods are invoked via `node call_informat.js <method> --appId <appId> --file /dev/stdin <<'EOF' {json} EOF`.**

---

## 1. When to use codestudio

- Interactive / component-based frontends with routing, state, or ECharts charts → **use codestudio**.
- Purely static display pages (one or two html files, no interaction) → use the website module (`_website_*`).
- Pick one per requirement; do not mix.

---

## 2. End-to-end flow (follow this order)

```
1. _codestudio_list_modules        list existing modules; reuse if suitable (don't duplicate)
2. _codestudio_create_module       create only if none fits → get moduleId
3. _query_all_table_list           see which tables exist (never fabricate tableId)
4. _query_table_define             get the target table's field definitions
5. _codestudio_create_script       create/update backend script (query/CRUD) → get scriptId
6. _codestudio_create_api          create/update API bound to a script function → frontend uses its path
7. _codestudio_write_file          write Vue files (App.vue / components / views / router)
8. _codestudio_compile             compile, read structured errors; fix & recompile until success
9. _codestudio_preview             get the preview URL for the user
```

> Key: you have **no local filesystem** for the project. Always use `_codestudio_read_file` / `_codestudio_write_file` / `_codestudio_list_files` for project files — do NOT use Read/Write/Edit/Bash on the filesystem.

---

## 3. Create / reuse a module

1. Call `_codestudio_list_modules` first (no params, only appId): returns `[{moduleId, name, remark}]`. If a suitable module already exists, **reuse its moduleId** and skip to step 3.
2. Only if none fits, call `_codestudio_create_module` with `{ "name": "<module name>", "remark": "<optional>" }` → returns a new moduleId. Every subsequent `_codestudio_*` call must carry this moduleId.

---

## 4. Data integration (backend script + API)

### 4.1 Query tables first, never fabricate

- For a business page (orders/students/courses/tasks…), first `_query_all_table_list` to see tables, then `_query_table_define` on relevant tables for field definitions. **Never fabricate tableId / fieldId.**

### 4.2 Create/update script: `_codestudio_create_script`

Params: `{ "moduleId": "<moduleId>", "entityName": "<english entity, e.g. orders>", "content": "<full script>" }`, returns **scriptId** (needed by the API step).

The backend automatically: applies the `ai_{moduleId}_` prefix (→ `ai_{moduleId}_orders.js`), injects an attribution comment on line 1, and files the script into a group directory named after the module. **You don't construct names, create directories, or write the comment.**

- `entityName` is just the entity (`orders`) — no `ai_` prefix, no `.js`, no `_list`/`_create` operation suffix.
- **Idempotent update**: the same `moduleId + entityName` updates the existing `ai_{moduleId}_{entityName}.js` and returns the original scriptId. To fix/extend the same entity, keep the same `entityName`; **do not** create `orders2`, `orders_new`, or `orders_copy`.
- **One entity = one script**: put list/get/create/update/delete for the same table in **one content** via multiple `export function`. Don't create one script per operation (explosion).

**Script content (content) hard rules:**

1. Each exported function takes **a single `context` param** (not params, not `(ctx, params)`).
   - `context` fields: `appId / body / cookies / headers / ip / method / path / query / url`.
   - **`context.body` is a string**; you must `JSON.parse(context.body || '{}')` to get the JSON the frontend sent.
2. **No `async`/`await`**: all `informat.*` methods return **synchronously**; use the return value directly.
3. **Mandatory error envelope**: wrap each function body in try/catch with a fixed shape:
   - success `{ code: 0, data: <real data> }`
   - failure `{ code: -1, error: e.message || String(e), errorType: e.name || 'Error', stack: e.stack || null }`
   - The frontend SDK treats `code !== 0` as an API error and throws, so "let AI fix" gets the precise cause. **Don't let exceptions bubble raw** (a 500 carries no readable error).
   - **★ The SDK auto-unwraps `data`**: a script `return { code:0, data:{ rows, total } }` means the frontend `await callApi(...)` receives `{ rows, total }` directly — **do not `.data` again** on the frontend.

**informat.table methods (read & write allowed in scripts):**

- Query: `query(tableId,id,setting?)` / `queryById(tableId,id)` / `queryOne(tableKey,query)` / `queryList(tableId,query)` / **`queryListCount(tableId,filter)` (use this to count, NOT count; the second `filter` argument is required; pass `{}` when there is no filter; never call it with only tableId)** / `queryRelationList` / `queryChildrenList` / `getTableInfo` / `getTableFieldInfo`.
- Write: `insert` / `batchInsert` / `update` / `updateList` / `batchUpdate` / `delete` / `batchDelete` / `deleteList` / `addRelation` / `deleteRelation`.
- **❌ Non-existent / invalid calls (runtime error if used)**: `count`→use `queryListCount(tableId, filter)`; `queryListCount(tableId)`→missing required `filter`, write `queryListCount(tableId, {})`; `findOne/findById`→use `queryOne/queryById`; `exists`→use `queryListCount(tableId, filter)>0`; `aggregate/sum/avg/max/min`→fetch then reduce.
- For other namespaces (`informat.user.*` / `informat.http.*` / `informat.file.*`), when unsure of a signature, check the matching doc under `doc/markdown/script/`.

**Script content example (one entity per file, 4 functions together):**

```js
// ai_<moduleId>_orders.js — all operations for the orders entity
export function listOrders(context) {
  try {
    const data = JSON.parse(context.body || '{}');
    const rows = informat.table.queryList('tbl_orders', { filter: data.filter, pageIndex: data.page || 1, pageSize: data.size || 20 });
    const total = informat.table.queryListCount('tbl_orders', data.filter || {});
    return { code: 0, data: { rows, total } };
  } catch (e) {
    return { code: -1, error: e.message || String(e), errorType: e.name || 'Error', stack: e.stack || null };
  }
}
export function createOrder(context) {
  try {
    const data = JSON.parse(context.body || '{}');
    const id = informat.table.insert('tbl_orders', data);
    return { code: 0, data: { id } };
  } catch (e) {
    return { code: -1, error: e.message || String(e), errorType: e.name || 'Error', stack: e.stack || null };
  }
}
export function updateOrder(context) { /* same try/catch + JSON.parse + informat.table.update */ }
export function deleteOrder(context) { /* same try/catch + informat.table.delete */ }
```

### 4.3 Create/update API: `_codestudio_create_api`

**One API per operation**; multiple APIs reuse the same scriptId and differ by scriptFunc. Params:

```json
{ "moduleId": "<moduleId>", "subPath": "orders/list", "name": "Order list",
  "scriptId": "<scriptId from previous step>", "scriptFunc": "listOrders", "method": "POST" }
```

The backend auto-applies the `ai/{moduleId}/` path prefix (→ `ai/{moduleId}/orders/list`) and files the API into a group directory named after the module. **You only provide `subPath` (`entity/operation`) — no full path, no directory, no parentId.** You may create several in parallel (each carries moduleId; the backend files them into the same group without conflict).

- **Idempotent update**: the same `moduleId + subPath` updates the existing API path and returns the original id. To fix/extend the same endpoint, keep the same `subPath`; **do not** create `orders/list2`, `orders/list_new`, or `orders/query` to bypass duplicates.

### 4.4 Attribution rules (the most common failure mode)

- **Only call scripts/APIs you created or updated via `_codestudio_create_script` / `_codestudio_create_api` with this module's moduleId prefix.**
- **Never reuse other existing scripts/APIs** (user-handwritten, or other codestudio modules' `ai_*` resources) — their params/returns/semantics almost certainly won't match; the frontend will 404 or get mismatched fields.
- ❌ Don't call `_query_informat_script_list` / `_api_query_define_list` to "see if one exists". If you need API X, just create `ai_{moduleId}_xxx` + `ai/{moduleId}/xxx`.
- The frontend `callApi(path)` path must start with `ai/{moduleId}/`, otherwise it's wrong.

---

## 4.5 Cross-app data (this site reading multiple apps)

The codestudio site you build **is not necessarily a dashboard** — it may be a full-featured business site whose data just happens to be spread across multiple Informat apps. When it needs data from **multiple apps** (e.g. "orders from the work-order app + students from the teaching app"), note the platform has **no cross-app table query** (`informat.table.*` only reads tables of the app the script lives in). So create a set of `ai_` script+API in **each source app**, and have this site's frontend call each across apps:

1. `_company_app_list` to find each source app's appId (the user names the apps; match them).
2. **For each source app**, create script + API (routed to that app):
   - Script: `_codestudio_create_script --appId <sourceAppId>`, params `{ "moduleId":"<this module's id>", "entityName":"...", "content":"...", "ownerAppId":"<this module's app appId>" }`. The script lives in and reads the source app's tables; attribution still belongs to this module.
   - API: `_codestudio_create_api --appId <sourceAppId>`, params `{ "moduleId":"<this module's id>", "subPath":"...", "name":"...", "scriptId":"...", "scriptFunc":"...", "ownerAppId":"<this module's app appId>" }`.
   - For **this module's own app** data, as before: `--appId` = this app, do **NOT** pass `ownerAppId`.
3. Frontend calls:
   - Own app: `await callApi('ai/<moduleId>/...', body)` (unchanged).
   - **Cross-app: `await callApi('ai/<moduleId>/...', body, { appId: '<sourceAppId>' })`** — the 3rd arg `{appId}` routes the SDK to the source app; or use `callAppApi('<sourceAppId>', 'ai/<moduleId>/...', body)`.
4. **Permission (hard constraint)**: you must be a designer of **every** source app. If `_codestudio_create_*` returns `is not app designer`, **do not retry** — tell the user "you need designer rights on app X; ask its admin to add you as a designer".
5. **Publishing (always remind the user)**: cross-app `ai_` scripts/APIs live in the source apps as drafts. They work automatically during this site's **preview**; but after this site is **published**, each source app must be **published separately**, otherwise cross-app calls 404 in production. At the end, state clearly: "this site uses data from apps A and B — remember to publish A and B as well, or these data won't load after going live."

## 5. Frontend Vue (write with `_codestudio_write_file`)

One `_codestudio_write_file` per file, params `{ "moduleId": "<moduleId>", "path": "<relative path>", "content": "<full file>" }`.

### 5.1 File-write boundary

- **✅ You may write**: `App.vue`, `components/*.vue`, `views/*.vue`, `router/index.js`, `styles/*.css`, and other business files.
- **❌ Never write**: `index.html` / `vite.config.js` / `vite.config.ts` / `main.js` / `main.ts` / `tsconfig.json` / `vite-env.d.ts` / `package.json` (boilerplate, fixed; adding deps to package.json gets stripped server-side), `__informat_sdk__.js` / `__informat_sdk__.ts` / `node_modules/` / `dist/` (system-generated).
- Use relative paths (`App.vue`, `components/Foo.vue`), never absolute.

### 5.2 Stack (preinstalled, use directly)

- Vue 3 `<script setup>` / `<script setup lang="ts">` + Element Plus (globally registered, write `<el-button>` directly) + vue-router (createWebHashHistory) + echarts.
- If the project is configured for TypeScript, prefer `.ts` for business scripts and routes, and use `<script setup lang="ts">` in Vue components.
- Icons: `import { Plus } from '@element-plus/icons-vue'` + `<el-icon><Plus/></el-icon>`.
- Feedback: `import { ElMessage, ElMessageBox } from 'element-plus'`.
- Platform API: `window.__informat__.callApi(path, body)`, call after onMounted; try/catch with `ElMessage.error`.
- **npm whitelist**: only import whitelisted packages (vue/vue-router/pinia/element-plus/@element-plus/icons-vue/echarts/vue-echarts/dayjs/lodash-es/axios/typescript). Importing anything else fails the build; don't add deps to package.json.

### 5.3 Calling APIs (SDK already unwraps data)

```js
// script return { code:0, data:{ rows, total } } → frontend receives { rows, total }
const res = await callApi('ai/<moduleId>/orders/list', { page: 1, size: 20 });
rows.value = res.rows;     // ✅ NOT res.data.rows!
total.value = res.total;   // ✅
// create: script return { code:0, data:{ id } }
const r = await callApi('ai/<moduleId>/orders/create', form);
ElMessage.success('Created id=' + r.id);   // ✅ NOT r.data.id!
```
- ❌ Most common bug: `res.data.rows` / `res.data.id` — `res.data` is undefined and throws.
- On error (script `code!==0` or non-2xx) the SDK throws; just catch it. There's no "succeeded but check code" path.

### 5.4 Style & file rules

- Each `.vue` uses `<style scoped>`; call `defineProps/defineEmits` at most once each, merging all fields.
- **Global styles must be imported explicitly**: after writing `styles/xxx.css`, in the **same turn** add `@import './styles/xxx.css';` to App.vue's top `<style>` (or `import './styles/xxx.css';` at the top of `<script setup>`), otherwise styles don't apply.
- Routing: add routes to the routes array in `router/index.js`.

---

## 6. Compile + fix loop

After writing files, call `_codestudio_compile` with `{ "moduleId": "<moduleId>" }`. It returns **synchronously**:

```json
{ "success": true/false, "errorMessage": "...", "stderr": "<build errors>", "illegalDeps": [...], "durationMs": 123 }
```

- `success: false` → read `stderr` (vite errors like `Could not resolve './xxx'`, syntax errors, non-whitelisted imports), locate the file, `_codestudio_read_file` to inspect → `_codestudio_write_file` to fix → `_codestudio_compile` again, until `success: true`.
- `illegalDeps` non-empty → you imported a non-whitelisted package; switch to a whitelisted approach or tell the user.
- **You must compile to success before considering it done.** Don't stop right after writing files.

---

## 7. Preview

After a successful compile, call `_codestudio_preview` with `{ "moduleId": "<moduleId>" }` → returns `{ previewUrl, moduleId }`. Give previewUrl to the user (the conversation renders an "Open preview" card).

---

## 8. Mock data policy (strict)

- ✅ Only when `_query_all_table_list` finds **no** semantically related table may you write 5-10 mock rows in a frontend ref, and you must tell the user "the app has no XX table; create it and I'll wire real data".
- ❌ Table exists but empty (query returns empty) → **no mock**; use the real API and show a normal "no data" empty state.
- ❌ User says "build an order page" and you skip table queries and write `const orders = ref([{...}])` — the worst kind of shortcut, treated as failure.

---

## 9. Security constraints

- In conversation, only `_codestudio_create_script` (create script) and `_codestudio_create_api` (create API) may write to the platform. **Never** call methods that modify "table schema / table records / users / permissions / roles / app config" (`_save_table_*` / `_drop_*` / `_xxx_record_insert/update/delete`, etc.) — those should happen via UI interaction in the generated app (calling `informat.table.insert/update/delete` inside a script is fine; that's runtime behavior).
- Read methods (`_query_*` / `_get_*` / `_list_*`) may be called freely.
