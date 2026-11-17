---
name: md-web
description: Use when the user explicitly asks to publish Markdown online or obtain a public share link through their S3 bucket. 发布 Markdown / 生成公开分享链接 / /md-web. Reads ~/.md-web/config.json. Viewer setup overwrites bucket-root files; optional expire_days manages retention. Local preview uses a local tool.

metadata:
  version: "1.3.12"
  openclaw:
    homepage: https://github.com/rockbenben/aishort-skills/tree/main/skills/md-web
    emoji: "🌐"
    requires:
      bins: ["node"]
    envVars:
      - name: MD_WEB_ACCESS_KEY
        required: false
        description: Bucket access key fallback when access_key is omitted from config.json.
      - name: MD_WEB_SECRET_KEY
        required: false
        description: Bucket secret key fallback when secret_key is omitted from config.json.
    files:
      - upload.js
      - "docsify-server/**"
---

# MD Web - Markdown to Web Page

Upload one raw `.md` file to the user's S3-compatible bucket; a Docsify viewer already in that bucket renders it at a public URL. `{SKILL_DIR}` below is this skill's base directory — always keep it quoted.

## Data and writes

- Publishing writes one Markdown object under the configured bucket's `md-web/` prefix. Re-publishing creates a new link.
- Separate `--setup` uploads `assets/<bundle-hash>/` and replaces root `README.md` / `index.html`, which all document links share. Old assets remain available to cached pages.
- Optional `expire_days` manages one lifecycle rule for `md-web/`; uploads expire after N days, and `0` removes the rule. Other rules are preserved.
- Configuration and the deployment hint live in `~/.md-web/config.json` and `~/.md-web/.deployed`. Requests go to the configured S3 endpoint; publishing checks the active remote viewer. Legacy adjacent config is migrated automatically.

## Ground rules

- **Document publishing.** An explicit request for online publication or a public/shareable Markdown link authorizes uploading that document, including retries. Tell the user the link is public before uploading; resolve unclear sharing scope first. Local preview or text organization stays local.
- **Viewer setup.** Running `--setup` overwrites bucket-root files used by all published documents. Explain the affected paths and obtain authorization for setup, unless the user already authorized it in this task.
- **Retention.** Adding, changing or removing `expire_days` changes the bucket policy. Obtain authorization for the requested retention change, unless it was already included in the user's instruction.
- **Check the public scope.** Review for sensitive material outside the intended sharing scope and redact or clarify it before uploading. Publish raw Markdown; do not convert it to HTML.

## Workflow

### 1. Configuration

Check for `~/.md-web/config.json` (`%USERPROFILE%\.md-web\config.json` on Windows). If it is missing or incomplete, run **First-time configuration** below.

Exception: if it is missing but a legacy `config.json` sits next to `upload.js`, skip the wizard and just upload — the script migrates it (and `.deployed`) to `~/.md-web/` and prints `Config migrated to:`.

### 2. Prepare the file

Use the existing `.md` file, or write the content to a temp file in the **OS temp directory** (`/tmp/` on Linux/macOS; `$TEMP` in Git Bash, `%TEMP%` in cmd).

Use a unique scratch path and remove only the temporary file you created after the upload attempt. Preserve an existing user file.

Viewer limits — write for them:
- Only the `.md` is uploaded: relative images (`![](a.png)`) break. Use absolute `https://` image URLs.
- GFM, tables, `<details>` and inline HTML render; the CSP blocks inline scripts, but HTML can still insert page elements. Review third-party markup before publishing (see **Security & privacy**). **Mermaid and LaTeX/KaTeX are not rendered** (shown as code) — use tables, lists or images instead.
- Start with a `# Title`: it becomes the browser tab title. YAML front matter is stripped automatically.

### 3. Publish

```bash
node "{SKILL_DIR}/upload.js" <local-file> <remote-key>
```

- `<remote-key>`: short lowercase ASCII slug describing the content, e.g. `api-docs`, even for Chinese documents. The script slugifies whatever it gets — a key with no ASCII letters or digits collapses to `doc` — prepends a timestamp, appends a short random suffix so two documents published in the same second cannot land on the same object, forces `.md` and stores it under `md-web/`.
- If stderr contains `SETUP_REQUIRED`, **follow the viewer-setup authorization rule above** — `--setup` rewrites shared bucket-root files — then run setup and retry the same publish command:

  ```bash
  node "{SKILL_DIR}/upload.js" --setup --confirm-shared-writes
  ```

  The required `--confirm-shared-writes` flag records the already obtained setup/retention authorization; never add it merely to bypass a missing-confirmation error. Setup performs the shared writes listed above and applies `expire_days`; both authorization rules still apply. Run it on first use, after a viewer upgrade, after changing `bucket` / `endpoint`, or when the active viewer differs. Existing document URLs stay unchanged. Retention changes also need setup, but publishing does not detect them; changing `public_url` only changes the printed link.
- `SETUP_CONFLICT` means a concurrent setup changed the entry point or the provider did not return an ETag. Inspect the active viewer before retrying; do not automatically overwrite it. Setup requires S3 conditional object writes (`If-Match` / `If-None-Match`); unsupported providers fail without an unconditional fallback. An upgrade from the old flat-asset layout requires one explicit setup; old flat assets and version directories are not deleted.
- `Warning: lifecycle —` means retention was not confirmed even if viewer setup succeeded. Follow the detail: a permission error may require lifecycle access or a provider-dashboard change; unsupported XML, a rule conflict or concurrent edit requires inspecting the actual policy. Do not treat every warning as a reason to broaden credentials.
- Lifecycle administration has no atomic per-rule update: serialize it with other administrators. Setup re-reads before replacing the policy and warns on a detected edit, unsupported/incomplete XML, or a conflicting rule ID. Policy writes are not automatically retried; a warning does not mean the requested retention took effect. A narrow race remains between the final read and write.

### 4. Reply

- **Success:** the last stdout line is the URL. Reply with the document name and clickable link, plus any material setup or retention warning. Avoid repeating the full document unless requested. Example: `api-docs` — https://pub-xxxx.r2.dev/index.html#/md-web/20260305-091500-api-docs-4f2a
- **Failure** (non-zero exit, `UPLOAD_FAILED` / `CONFIG_MISSING` / `CONFIG_INVALID` / `Missing config fields`): report the error in one line with the likely fix (table below), then deliver the content in chat.

| Error contains | Likely cause |
|---|---|
| `SignatureDoesNotMatch`, `InvalidAccessKeyId` | Wrong keys, or wrong `region` (`auto` for R2; the real region for AWS) |
| `AccessDenied` on upload | Token lacks Object Read & Write, or is scoped to another bucket |
| `NoSuchBucket` | Typo in `bucket`, or endpoint of another account |
| `ENOTFOUND`, `CONFIG_INVALID` | `endpoint` must be a bare hostname; `public_url` must be an HTTP(S) URL; prefer HTTPS for public sharing |
| `Missing config fields` | `config.json` is incomplete — fill in the fields it lists, or set `MD_WEB_ACCESS_KEY` / `MD_WEB_SECRET_KEY` for the two keys |
| Link opens the "Looking for a document?" page | Document expired (`expire_days`) or `public_url` points to another bucket |

## First-time configuration

1. Explain that the skill needs an S3-compatible bucket with public read access. Setup guide: [README.md](README.md) ([中文](README.zh.md)) — Cloudflare R2 step by step, plus AWS S3, B2, Spaces, Wasabi, COS endpoints.
2. Collect the required fields:
   - `access_key`, `secret_key` — credentials for object read/write access (R2 token label: **Object Read & Write**); bucket lifecycle administration is separate below.
   - `endpoint` — hostname without `https://`, e.g. `ACCOUNT_ID.r2.cloudflarestorage.com`
   - `bucket`
   - `public_url` — custom domain if bound (recommended; `r2.dev` URLs are rate-limited), else `https://pub-XXXX.r2.dev`

   Secrets should not travel through chat if avoidable: offer that the user writes `config.json` themselves, or omits the two keys and exports `MD_WEB_ACCESS_KEY` / `MD_WEB_SECRET_KEY` instead (the file wins when both are set).
3. Optional: `region` (default `auto`; AWS needs the real region, e.g. `us-east-1`) and `expire_days` (auto-delete uploads after N days; `0` removes the rule). **Omit `expire_days` unless the user asks for auto-expiry**. Lifecycle administration needs provider-specific bucket permissions: R2 uses [Admin Read & Write](https://developers.cloudflare.com/r2/api/tokens/#permissions), while AWS uses [lifecycle IAM permissions](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketLifecycleConfiguration.html), not an R2 token label. The script only edits its own `md-web/` rule and preserves other rules.
4. Write `~/.md-web/config.json` (create the directory; on macOS/Linux create the directory with mode `0700` and the file with mode `0600` before writing secrets; the script also checks owner-only file access; it never asks for root and never needs elevated privileges):

```json
{
  "access_key": "...",
  "secret_key": "...",
  "endpoint": "ACCOUNT_ID.r2.cloudflarestorage.com",
  "bucket": "md-web",
  "region": "auto",
  "public_url": "https://pub-XXXX.r2.dev"
}
```

5. Run `--setup`, then publish (step 3), using the authorization rules above for each action.

## Security & privacy

Credentials are plaintext in `~/.md-web/config.json` unless supplied through the environment. Migration creates the destination with mode `0600` before writing credentials and tightens its dedicated directory to `0700` on macOS/Linux. Permission failures stop the command. Windows chmod does not enforce ACLs: use a private user directory or environment credentials. Keep credentials out of version control and shared output; a dedicated bucket limits the impact of setup and administration.

The viewer accepts inline HTML. Its CSP blocks inline scripts and the route guard loads same-origin documents under `md-web/`, but neither sanitizes page elements. Review unfamiliar markup and treat published pages as untrusted content. Document language is preserved.
