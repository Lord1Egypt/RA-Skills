---
name: hybrids3
description: Self-hosted lightweight object storage speaking three interfaces at once: the S3 API (boto3 / AWS-SDK compatible, AWS Sig V4), a plain HTTP API (curl-friendly, Bearer auth), and MCP (Streamable HTTP tools for agents). Buckets/objects with SQLite metadata and flat-file storage on disk; buckets are config-defined (no create/delete API), each with a public/private flag, a private key + public key pair, optional TTL expiry, and a max upload size. Auth is per-bucket keys plus a cross-bucket master key; presigned GET/PUT URLs for handing out single-object access. Use when the user wants to put/get/list/delete files in a self-hosted S3-compatible store, generate presigned upload/download links, drive their own boto3-compatible object storage, or connect an agent to object storage over MCP.
homepage: https://github.com/psyb0t/docker-hybrids3
user-invocable: true
permissions:
  - "network: outbound HTTP(S) to the configured HYBRIDS3_URL object-storage endpoint"
  - "object storage: read/write/delete objects (upload, download, list, delete) and generate presigned GET/PUT URLs, scoped to whatever bucket key is provided"
metadata:
  { "openclaw": { "emoji": "🪣", "primaryEnv": "HYBRIDS3_URL", "requires": { "bins": ["docker", "curl"] } } }
---

# hybrids3

Lightweight object storage that speaks three interfaces from one container: the **S3 API** (boto3 / any AWS SDK, AWS Signature V4), a **plain HTTP API** (`curl` + Bearer token), and **MCP** (Streamable HTTP tool definitions for AI agents). Metadata lives in SQLite, object bytes are flat files on disk.

Buckets are **configuration, not state**. They're defined in the server's `config.yaml` and there is no API to create or delete them. Each bucket carries: a `public`/private flag, a private `key` (Bearer token + S3 signing secret), a `public_key` (the `aws_access_key_id` identifier), an optional `ttl` (objects auto-expire after last write), and an optional `max_file_size`. A single cross-bucket `master_key` operates on every bucket and is the only credential that can list all buckets.

Object keys support nested paths (`reports/2024/jan.pdf`). Content type is auto-detected on upload (libmagic sniff + extension fallback). Presigned GET/PUT URLs hand out time-limited single-object access without exposing a key.

For installation, configuration, and container setup, see [references/setup.md](references/setup.md).

## Security & safety

- **Public buckets are world-readable.** A bucket with `public: true` serves `GET`/`HEAD`/`LIST` to anyone who can reach the port, with no auth at all. Only store data there that's meant to be openly readable; keep sensitive data in a `public: false` bucket.
- **Bind loopback, not all interfaces.** The container listens on `8080`. Publishing it as `-p 8080:8080` / compose `"8080:8080"` makes it reachable from the network by default. Use `-p 127.0.0.1:8080:8080` (loopback) unless remote access is intentionally required, and for real deployments put the service on an internal Docker network behind a reverse proxy instead of exposing the port directly. See [references/setup.md](references/setup.md#quick-install) and [Behind a Reverse Proxy](references/setup.md#behind-a-reverse-proxy).
- **`DELETE`, presigned `PUT`, and MCP `delete_object` are destructive & irreversible.** There's no undo, no versioning, no recycle bin. A deleted object (or one overwritten via `PUT`) is gone. An agent must NEVER call `DELETE` / `delete_object`, or generate/use a presigned `PUT` that overwrites, unless the user explicitly asked for that exact key to be removed or replaced; confirm the specific bucket + key first, never enumerate-then-bulk-delete, and treat bulk cleanup as requiring explicit per-object user confirmation.
- **Bucket keys, master key, and presigned URLs are bearer credentials.** Whoever holds a bucket's private `key` or the `master_key` (or a live presigned URL) can act as that bucket/master until the credential is rotated or the URL expires. There's no per-caller revocation. Never paste these into shared prompts, logs, or presigned URLs handed to untrusted parties beyond the one object they're meant to grant.
- **This skill is a consumer, not an operator.** It talks to an instance the user already runs; it doesn't provision, harden, or expose the server. Don't use this skill to reconfigure `config.yaml`, change bucket visibility, or alter port bindings on the user's behalf without being explicitly asked.

## When To Use

- Put / get / list / delete files in a self-hosted, S3-compatible object store.
- Drive existing boto3 / AWS-SDK code against your own endpoint (change `endpoint_url` + credentials, nothing else).
- Store artifacts, uploads, reports, backups that services and agents read/write.
- Generate a **presigned PUT URL** so a third party can upload one specific key without your bucket key.
- Generate a **presigned GET URL** so a third party can download one private object for a limited time.
- Connect an AI agent to object storage over **MCP** with structured `upload_object` / `download_object` / `list_objects` / etc. tools.
- Auto-expiring scratch storage: set a bucket `ttl` and objects clean themselves up.

## When NOT To Use

- Creating or deleting buckets at runtime. Buckets live in `config.yaml`; add/remove them there and restart. `PUT /{bucket}` is an S3-compat no-op.
- Multipart / chunked uploads (S3's multipart protocol): not implemented. Upload the whole object in one request.
- Object versioning, ACLs beyond bucket-level public/private, replication, or encryption at rest: none are supported.
- Downloading objects **over 50 MB via MCP**: the MCP `download_object` tool caps at 50 MB. Use the S3 or plain HTTP `GET` for large objects.
- CORS from a browser: no CORS headers are emitted; add them at the reverse-proxy layer.
- Provisioning, configuring, or hardening the server itself. This skill is a **consumer**. It talks to an instance the user already runs and trusts.

## Setup

The container should already be running. Point the skill at it:

```bash
export HYBRIDS3_URL=http://localhost:8080
```

**Verify:** `curl $HYBRIDS3_URL/health` returns `{"status":"ok"}`.

Keys are per-bucket and come from the operator's `config.yaml`. Export the ones you'll use rather than pasting them inline:

```bash
export HYBRIDS3_KEY=<bucket-private-key>          # Bearer token / aws_secret_access_key
export HYBRIDS3_PUBLIC_KEY=<bucket-public-key>    # aws_access_key_id (defaults to bucket name)
# For cross-bucket / list-all-buckets operations, use the master credentials instead:
export HYBRIDS3_MASTER_KEY=<master-key>
export HYBRIDS3_MASTER_PUBLIC_KEY=<master-public-key>   # defaults to "master"
```

If the server runs behind a reverse proxy at a subpath, `HYBRIDS3_URL` includes it (e.g. `http://host/storage`) and every route, health included, lives under that prefix.

For install / `config.yaml` shape / bucket + key definitions / ports / reverse proxy, see [references/setup.md](references/setup.md).

## Three Access Modes

One service, three front doors on the **same port** (`8080`). Pick per client:

| Mode | Endpoint | Auth | Reach for it when… |
|---|---|---|---|
| **S3 API** | root (`/`), signed requests | AWS Sig V4 (`public_key` = access key id, `key` = secret) | You already have boto3 / AWS-SDK code, or want SDK ergonomics (pagination, presign helpers, retries). |
| **Plain HTTP** | `/{bucket}/{key}` etc. | `Authorization: Bearer <key>` | Shell scripts, `curl`, quick one-offs. No SDK, no signing, just a Bearer header (and public-bucket reads need none). |
| **MCP** | `POST /mcp/` | per-connection + per-tool `auth_key` | An AI agent should manipulate storage through typed tool calls instead of raw HTTP. |

They share one SQLite metadata store and one flat-file tree, so an object written over S3 is readable over plain HTTP and MCP, and vice versa.

## S3 API

S3 clients authenticate with **AWS Signature V4**. The bucket's `public_key` is the `aws_access_key_id` (travels in the request in plaintext, in the `Credential=` field); the bucket's private `key` is the `aws_secret_access_key` (used only to compute the HMAC locally, never transmitted). `region_name` is required by SDKs but the value is arbitrary; use `us-east-1`.

```
Authorization: AWS4-HMAC-SHA256 Credential=uploads-id/20240101/us-east-1/s3/aws4_request, SignedHeaders=host;x-amz-date, Signature=<hmac>
```

### boto3

```python
import boto3
from botocore.config import Config

# per-bucket client: access limited to the "uploads" bucket
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:8080",     # HYBRIDS3_URL
    aws_access_key_id="uploads-id",           # bucket public_key
    aws_secret_access_key="uploads-secret",   # bucket key (private)
    region_name="us-east-1",                  # arbitrary but required
    config=Config(signature_version="s3v4"),
)

s3.put_object(Bucket="uploads", Key="file.txt", Body=b"hello")
s3.get_object(Bucket="uploads", Key="file.txt")["Body"].read()
s3.head_object(Bucket="uploads", Key="file.txt")
s3.list_objects_v2(Bucket="uploads", Prefix="images/")
s3.delete_object(Bucket="uploads", Key="file.txt")
s3.list_buckets()                             # bucket key → only "uploads"

# presigned URLs (see MCP / HTTP presign for the same semantics)
get_url = s3.generate_presigned_url(
    "get_object", Params={"Bucket": "permanent", "Key": "doc.pdf"}, ExpiresIn=3600,
)
put_url = s3.generate_presigned_url(
    "put_object", Params={"Bucket": "uploads", "Key": "inbox/report.pdf"}, ExpiresIn=600,
)
```

For cross-bucket access or `list_buckets()` returning **all** buckets, build a second client with the **master** credentials (`aws_access_key_id=master_public_key`, `aws_secret_access_key=master_key`). Don't embed the master key in client-facing code; per-bucket keys scope access to one bucket.

**Destructive & irreversible.** `delete_object` deletes the object with no undo: no versioning, no recycle bin. An agent must NEVER call it unless the user explicitly asked for that exact key to be deleted; confirm the specific bucket + key first, scope it to the current task, and never enumerate-then-bulk-delete. On a shared instance where multiple callers use the same bucket, this can destroy another caller's data, so treat bulk deletes as admin-only and requiring explicit confirmation.

### aws-cli

```bash
aws --endpoint-url "$HYBRIDS3_URL" \
    --region us-east-1 \
    s3api put-object --bucket uploads --key file.txt --body ./file.txt
# credentials via env: AWS_ACCESS_KEY_ID=<public_key> AWS_SECRET_ACCESS_KEY=<key>
```

Supported S3 operations: `put_object`, `get_object`, `head_object`, `delete_object`, `list_objects_v2` (honours `Prefix`), `list_buckets`, `generate_presigned_url` (GET + PUT). Not supported: multipart upload, versioning, ACLs, bucket create/delete (boto3's implicit `create_bucket` maps to a no-op).

## Plain HTTP API

Bearer auth: pass the bucket's private `key` (or the `master_key`) as `Authorization: Bearer <key>`. Public-bucket **reads** (GET/HEAD/LIST) need no auth; **all writes** and **private-bucket reads** require a key.

Requests carrying an AWS Sig V4 `Authorization` header get S3-style XML back; everything else gets JSON. Every response includes `X-Request-Id` (log correlation) and `X-Content-Type-Options: nosniff`. Errors carry `"error"` + `"request_id"` fields.

### Objects

| Method | Path | Auth | Description |
|---|---|---|---|
| `PUT` | `/{bucket}/{key}` | write | Upload object. Returns `ETag` (MD5 of content). Content type auto-detected; override with a `Content-Type` header. |
| `GET` | `/{bucket}/{key}` | read | Download object. Returns `ETag`, `Last-Modified`, `Content-Length`. |
| `HEAD` | `/{bucket}/{key}` | read | Object metadata, no body. |
| `DELETE` | `/{bucket}/{key}` | write | Delete object. Always `204`, even if absent. |
| `GET` | `/{bucket}` | read | List objects. Query: `prefix`, `max-keys`. |
| `POST` | `/presign/{bucket}/{key}` | write | Generate a presigned URL. Query: `method` (`GET` default / `PUT`), `expires` (seconds, 1 to 604800, default 3600). |

**Destructive & irreversible.** `DELETE` removes the object with no undo. An agent must NEVER call it unless the user explicitly asked for that exact key to be deleted; confirm the specific bucket + key first, scope it to the current task, and never enumerate-then-bulk-delete. On a shared bucket used by other callers, this can destroy their data, so treat it as admin-only.

```bash
# upload
curl -X PUT "$HYBRIDS3_URL/uploads/file.txt" \
  -H "Authorization: Bearer $HYBRIDS3_KEY" \
  --data-binary @file.txt

# upload a nested key (parent dirs created automatically)
curl -X PUT "$HYBRIDS3_URL/uploads/reports/2024/january.pdf" \
  -H "Authorization: Bearer $HYBRIDS3_KEY" \
  --data-binary @january.pdf

# download from a public bucket, no auth needed
curl "$HYBRIDS3_URL/uploads/file.txt"

# download from a private bucket
curl "$HYBRIDS3_URL/permanent/doc.pdf" \
  -H "Authorization: Bearer $HYBRIDS3_KEY"

# list objects with a prefix
curl "$HYBRIDS3_URL/uploads?prefix=images/&max-keys=50" \
  -H "Authorization: Bearer $HYBRIDS3_KEY"

# delete
curl -X DELETE "$HYBRIDS3_URL/uploads/file.txt" \
  -H "Authorization: Bearer $HYBRIDS3_KEY"
```

### Buckets

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/health` | none | `{"status":"ok"}` liveness check. |
| `GET` | `/` | master or bucket key | List buckets. The master key lists all, bucket key lists only its own. |
| `HEAD` | `/{bucket}` | read | `200` if bucket exists in config, else `404`. |
| `PUT` | `/{bucket}` | write | S3-compat no-op: `200` if bucket exists in config, `404` if not. Creates nothing. |

```bash
# list all buckets, needs the master key
curl "$HYBRIDS3_URL/" -H "Authorization: Bearer $HYBRIDS3_MASTER_KEY"

# a bucket key lists only its own bucket
curl "$HYBRIDS3_URL/" -H "Authorization: Bearer $HYBRIDS3_KEY"
```

### Presigned URLs (HTTP)

`POST /presign/{bucket}/{key}` requires the bucket key or master key. The result grants exactly one verb on exactly one key. A GET URL can't be used to PUT (the method is baked into the signature).

```bash
# presigned GET on a PRIVATE bucket → signed, expiring URL
curl -X POST "$HYBRIDS3_URL/presign/permanent/doc.pdf?expires=3600" \
  -H "Authorization: Bearer $HYBRIDS3_KEY"
# → {"url":"http://.../permanent/doc.pdf?X-Amz-Algorithm=...&X-Amz-Signature=...","method":"GET","expires":3600}

# presigned GET on a PUBLIC bucket → plain URL, no signature, no expiry (reads are open anyway)
curl -X POST "$HYBRIDS3_URL/presign/uploads/photo.jpg" \
  -H "Authorization: Bearer $HYBRIDS3_KEY"
# → {"url":"http://.../uploads/photo.jpg","method":"GET","expires":null}

# presigned PUT → ALWAYS signed, even for public buckets (anonymous writes are never allowed)
curl -X POST "$HYBRIDS3_URL/presign/uploads/inbox/report.pdf?method=PUT&expires=600" \
  -H "Authorization: Bearer $HYBRIDS3_KEY"

# recipient uploads using only the URL, no Authorization header
curl -X PUT "<presigned-put-url>" --data-binary @report.pdf
```

The bucket's `max_file_size` is enforced server-side during the upload regardless of how it was authenticated (oversized → `413`). Expired or tampered presigned URLs → `403`.

## MCP Endpoint

An MCP server runs at `POST /mcp/` over the **Streamable HTTP** transport. Client config:

```json
{
  "mcpServers": {
    "hybrids3": { "type": "streamable-http", "url": "http://localhost:8080/mcp/" }
  }
}
```

Wire it into Claude Code:

```bash
claude mcp add --transport http hybrids3 "$HYBRIDS3_URL/mcp/"
# with endpoint-level auth:
claude mcp add --transport http hybrids3 "$HYBRIDS3_URL/mcp/" \
  --header "Authorization: Bearer $HYBRIDS3_MASTER_KEY"
```

### Auth (two layers)

**Endpoint-level (optional)**: a token that authenticates the *connection* before any tool runs. Any valid key (master or bucket) is accepted; it does not grant or limit anything inside the tools, which per-tool auth decides. Send it as `Authorization: Bearer <key>`, or (for clients that can't set headers) as `?auth=<key>` on the URL. A token that matches nothing → `401`; **no token → passes through**, and per-tool auth applies. When the server sets `path_prefix`, the token check is skipped entirely.

**Per-tool**: every tool that touches a bucket takes an `auth_key` argument (the bucket's private `key` or the master key), checked independently of the connection token. Public-bucket reads (`download_object`, `list_objects`, `object_info`) accept an empty `auth_key`; all writes and all private-bucket ops require it.

### Tools

| Tool | Args | Auth | Notes |
|---|---|---|---|
| `upload_object` | `bucket`, `key`, `content`, `auth_key`, `content_type=""`, `encoding="utf-8"` | bucket/master key | `encoding="base64"` for binary. Returns `size`, `etag`, `content_type`. |
| `download_object` | `bucket`, `key`, `auth_key=""`, `encoding="utf-8"` | key on private only | `base64` for binary; UTF-8 that won't decode auto-falls back to base64. **Objects > 50 MB rejected, use HTTP.** |
| `delete_object` | `bucket`, `key`, `auth_key` | bucket/master key | Idempotent. |
| `list_objects` | `bucket`, `auth_key=""`, `prefix=""`, `max_keys=100` | key on private only | `max_keys` clamped to 1 to 1000. |
| `list_buckets` | `auth_key` | master or bucket key | Master lists all; bucket key lists only its own. |
| `object_info` | `bucket`, `key`, `auth_key=""` | key on private only | Metadata only (size, content_type, etag, uploaded_at, expires_at). |
| `presign_url` | `bucket`, `key`, `auth_key`, `method="GET"`, `expires=3600`, `base_url=""`, `host=""` | bucket/master key | `method` GET/PUT. Same public-GET-plain / everything-else-signed logic as the HTTP endpoint. `expires` clamped to 1 to 604800. Set `base_url` to the externally-reachable URL so the link is usable. |

**`delete_object` is destructive & irreversible.** It deletes the object with no undo. An agent must NEVER call it unless the user explicitly asked for that exact key to be deleted; confirm the specific bucket + key first, never enumerate-then-bulk-delete. On a shared bucket used by other callers, this can destroy their data, so treat it as admin-only.

All tools return `structuredContent` with a plain-text fallback. Internal error details are masked.

### Raw JSON-RPC

For debugging or non-MCP callers, POST JSON-RPC directly. The server keeps a session per client: send `initialize` first, read the `mcp-session-id` response header, send `notifications/initialized`, then pass `Mcp-Session-Id` on every call. Each request needs the `Accept` header below, and the URL keeps its trailing slash. A call without a session gets `400 Bad Request: Missing session ID`.

```bash
# initialize, capture the session id
SID=$(curl -s -D - -o /dev/null "$HYBRIDS3_URL/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"1"}}}' |
  awk -F': ' 'tolower($1) == "mcp-session-id" { print $2 }' | tr -d '\r')

curl -s "$HYBRIDS3_URL/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'

# tools/list
curl -s "$HYBRIDS3_URL/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'

# tools/call: upload
curl -s "$HYBRIDS3_URL/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SID" \
  -d '{
    "jsonrpc":"2.0","id":3,"method":"tools/call",
    "params":{
      "name":"upload_object",
      "arguments":{"bucket":"uploads","key":"note.txt","content":"hello","auth_key":"'"$HYBRIDS3_KEY"'"}
    }
  }'
```

Responses arrive as server-sent events; the JSON-RPC result is on the `data:` line.

## Authentication (all modes)

| Credential | Config field | Role | Keep secret? |
|---|---|---|---|
| Bucket private key | `key` | Bearer token (HTTP/MCP) **and** `aws_secret_access_key` (S3). Signs/verifies, never transmitted. | **Yes** |
| Bucket public key | `public_key` | `aws_access_key_id` (S3) + `Credential=` in presigned URLs. Identifies, grants nothing. Defaults to bucket name. | No |
| Master key | `master_key` | Cross-bucket god key. Works on every bucket + only credential that lists all buckets. | **Yes** |
| Master public key | `master_public_key` | `aws_access_key_id` paired with the master key (S3). Defaults to `"master"`. | No |

Bucket visibility:

| | GET / HEAD / LIST | PUT | DELETE / presign |
|---|---|---|---|
| `public: true` | no auth | bucket key, master key, or valid presigned PUT | bucket key or master key |
| `public: false` | bucket key, master key, or valid presigned GET | bucket key, master key, or valid presigned PUT | bucket key or master key |

Unauthorized or non-existent bucket access returns `404`, so callers can't tell "doesn't exist" from "no access". The exceptions: `GET /` without a valid key and an invalid or expired presigned GET URL return `403`. All key comparisons are constant-time.

## Typical Workflows

### Upload + fetch over plain HTTP

```bash
export HYBRIDS3_URL=http://localhost:8080
export HYBRIDS3_KEY=<uploads-key>

curl -X PUT "$HYBRIDS3_URL/uploads/report.pdf" \
  -H "Authorization: Bearer $HYBRIDS3_KEY" --data-binary @report.pdf
curl -sO "$HYBRIDS3_URL/uploads/report.pdf"     # public bucket → no auth on read
```

Or via the helper (see [`scripts/hybrids3.sh`](scripts/hybrids3.sh)):

```bash
HYBRIDS3_URL=http://localhost:8080 HYBRIDS3_KEY=<key> \
  scripts/hybrids3.sh put uploads report.pdf ./report.pdf
scripts/hybrids3.sh list uploads reports/
scripts/hybrids3.sh get uploads report.pdf ./out.pdf
scripts/hybrids3.sh delete uploads report.pdf
scripts/hybrids3.sh buckets                     # needs HYBRIDS3_KEY=<master-key>
```

### Hand someone a presigned upload URL

```bash
# you generate it (needs a key); they upload with no credentials
curl -X POST "$HYBRIDS3_URL/presign/uploads/inbox/theirs.zip?method=PUT&expires=600" \
  -H "Authorization: Bearer $HYBRIDS3_KEY" | jq -r .url
# → hand the URL over; recipient: curl -X PUT "<url>" --data-binary @theirs.zip
```

### Drop-in boto3 against your own endpoint

Point any existing boto3 code at `HYBRIDS3_URL`, set the bucket's `public_key`/`key` as the credential pair, `region_name="us-east-1"`, `signature_version="s3v4"`. See [S3 API](#s3-api).

### Agent-driven storage over MCP

Add the server (`claude mcp add --transport http hybrids3 "$HYBRIDS3_URL/mcp/"`), then call `list_buckets` to discover buckets, `upload_object` / `download_object` / `list_objects` to move data. Pass the bucket `key` as `auth_key`; use the master key only when you need cross-bucket reach.

### Auto-expiring scratch storage

If a bucket has a `ttl` set (server config), objects delete themselves that long after their last write; overwriting resets the clock. Nothing to do client-side; just write to the bucket.
