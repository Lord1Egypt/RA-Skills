---
name: mofang-page-builder
description: Build Magicflu/Mofang web-table custom pages from the jsonv2 records API. Use when users ask for Magicflu/Mofang forms, records, lists, create/edit/detail/admin CRUD pages, H5 extension pages, React/Vue/vanilla JS examples, local jsonv2 mock/proxy debugging, or same-origin publishing to Magicflu websites. Works as a standalone skill for Codex/OpenAI, OpenClaw, Claude Code, Trae, and Trae CN.
metadata:
  version: 1.1.0
  author: magicscape
  platforms:
    - Codex
    - OpenAI
    - OpenClaw
    - Claude Code
    - Trae
    - Trae CN
  compatibility:
    node: ">=18"
---

# 魔方网表页面生成

Use this skill to generate and publish Magicflu/Mofang web-table pages. The safe path is:

1. Confirm `spaceId`, `formId`, and page type.
2. Fetch or import the real `fielddef`.
3. Generate page code using only field `name` values from `fielddef.fields[]`.
4. Test with local `mock-jsonv2` or proxy.
5. Set `CONFIG.apiBase` to `''` before same-origin publishing.

## Install Locations

Copy the whole `mofang-page-builder/` folder, not only `SKILL.md`.

| Client | Project install | Global install |
|--------|-----------------|----------------|
| Claude Code | `.claude/skills/mofang-page-builder/` | `~/.claude/skills/mofang-page-builder/` |
| Trae | `.trae/skills/mofang-page-builder/` | `~/.trae/skills/mofang-page-builder/` |
| Trae CN | `.trae/skills/mofang-page-builder/` | `~/.trae-cn/skills/mofang-page-builder/` |

Keep these directories with the skill: `examples/`, `assets/`, `references/`, and `scripts/`.

## Required Workflow

Never guess real form field names from Chinese labels. For real data:

1. Ask for or identify `spaceId` and `formId`.
   - If only a space name is known, resolve it with `/magicflu/service/json/spaces/feed`.
   - To traverse all spaces, use `/magicflu/service/json/spaces/feed?start=0&limit=-1&bq=(created,orderby,desc)`.
   - If only a form label is known, resolve it with `/magicflu/service/s/json/{spaceId}/forms/feed`.
2. Run `scripts/fetch-form-spec.mjs`, or ask the user for an exported fielddef JSON and import it.
3. Use only `fielddef.fields[].name` as API keys, submit keys, and filter field names.
4. Use `fielddef.fields[].label` only for UI text.
5. Test locally before deployment.

Example fields in `examples/` and `assets/mock-data/` are demos only.

## Page Contract

Generated pages must include:

```js
const CONFIG = {
  apiBase: '', // local debug: 'http://127.0.0.1:3847'; same-origin production: ''
  spaceId: 'YOUR_SPACE_ID',
  formId: 'YOUR_FORM_ID',
};

function apiUrl(path) {
  const origin = CONFIG.apiBase ? CONFIG.apiBase.replace(/\/$/, '') : '';
  return `${origin}${path}`;
}
```

Same-origin pages rely on browser Cookie auth. Do not set an `Authorization` header in page code.

## API Summary

Read `references/api-summary.md` when you need endpoint details, bq syntax, response shape, or field value formats.

Core paths:

| Capability | Method | Path |
|------------|--------|------|
| List all spaces | GET | `/magicflu/service/json/spaces/feed?start=0&limit=-1&bq=(created,orderby,desc)` |
| Find spaces by label | GET | `/magicflu/service/json/spaces/feed?start=0&limit=10&bq=(label,eq,{spaceLabel})` |
| List forms in a space | GET | `/magicflu/service/s/json/{spaceId}/forms/feed?start=0&limit=-1` |
| Find forms by label | GET | `/magicflu/service/s/json/{spaceId}/forms/feed?start=0&limit=10&bq=(label,eq,{formLabel})` |
| Field definition | GET | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}?selector=fielddef&lng=en` |
| List records | GET | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}/records/entry` |
| Create record | POST | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}/records` |
| Update record | PUT | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}/records/entry/{recordId}` |
| Delete record | DELETE | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}/records/entry/{recordId}` |

Use the spaces endpoint when the user gives only a space name. The returned space id is `items[].id`; the display name is `items[].label`. Use the form-list endpoint when the user gives only a `spaceId` or form label. The returned form id is `feed.entry[].id`; the display name is `feed.entry[].content.form.label`; the English form key is `feed.entry[].content.form.name`.

Field rules:

- API payload keys must be `name`, not `label`.
- Omit empty values before submit.
- Never submit `""` for number fields.
- Do not submit system, serial, secondary reference, image, attachment, location, webpage, comment, or external field-group fields.

## Fetch Field Definitions

Account/password:

```bash
BASE_URL="http://appdev.com.magicflu.com:9999" \
MOFANG_USERNAME="你的账号" \
MOFANG_PASSWORD='你的密码' \
node scripts/fetch-form-spec.mjs \
  --spaceId <空间UUID> \
  --formId <表单UUID> \
  --out ./mock-data
```

If only names are known, resolve and fetch in one command:

```bash
BASE_URL="http://appdev.com.magicflu.com:9999" \
MOFANG_USERNAME="你的账号" \
MOFANG_PASSWORD='你的密码' \
node scripts/fetch-form-spec.mjs \
  --spaceLabel "空间名称" \
  --formLabel "表单名称" \
  --out ./mock-data
```

Cookie:

```bash
node scripts/fetch-form-spec.mjs \
  --baseUrl https://你的魔方域名 \
  --spaceId <空间UUID> \
  --formId <表单UUID> \
  --out ./mock-data \
  --cookie "浏览器 Cookie"
```

Offline import:

```bash
node scripts/fetch-form-spec.mjs \
  --spaceId <空间UUID> \
  --formId <表单UUID> \
  --out ./mock-data \
  --import-json ./fielddef-export.json
```

Output: `mock-data/manifest.json`, `mock-data/<formId>/fielddef.json`, `records.seed.json`, `typesnippets.md`, and `api-outline.md`.

## Local Debug

Use the bundled demo data:

```bash
cp -R assets/mock-data ./mock-data
node scripts/mock-jsonv2.mjs --port 3847 --dir ./mock-data
```

Set page config:

```js
CONFIG.apiBase = 'http://127.0.0.1:3847';
```

Proxy to a real environment only when the user explicitly wants real data behavior:

```bash
BASE_URL="http://appdev.com.magicflu.com:9999" \
MOFANG_USERNAME="你的账号" \
MOFANG_PASSWORD='你的密码' \
node scripts/mock-jsonv2.mjs --mode proxy --port 3847
```

Proxy mode forwards supported space, `json`, and `jsonv2` calls to the real environment. `POST`, `PUT`, and `DELETE` will change real records.

## Publish Same-Origin Pages

Before publishing, set page `CONFIG.apiBase` to `''`.

```bash
BASE_URL="http://appdev.com.magicflu.com:9999" \
MOFANG_USERNAME="你的账号" \
MOFANG_PASSWORD='你的密码' \
node scripts/deploy.mjs \
  --spaceId <空间UUID> \
  --label "站点名称" \
  --shortcut custom-page \
  --files index.html
```

The deploy script logs in, creates a website, warms the session, uploads files through `filemanager.jsp`, and prints the final URL:

```text
{BASE_URL}/magicflu/html/sites/userfiles/{spaceId}/{websiteId}/index.html
```

Read `references/design.md`, `references/requirements.md`, and `references/filemanager.js` only when debugging implementation details.

## Examples

| Stack | File | Purpose |
|-------|------|---------|
| Vanilla HTML+JS | `examples/vanilla/list-page.html` | Same-origin list page |
| Vanilla HTML+JS | `examples/vanilla/list-page-with-apibase.html` | List page wired to local mock |
| Vanilla HTML+JS | `examples/vanilla/form-page.html` | Create-record form |
| React | `examples/react/MagicfluList.tsx` | List component |
| Vue | `examples/vue/MagicfluForm.md` | Text-safe create-record form component |

## Validation

Run these from the skill root:

```bash
npm run check:scripts
npm run smoke:fetch-import
npm run smoke:mock
npm run smoke:upload
```
