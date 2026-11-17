# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/compute/ecs/huawei-cloud-ecs-show
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `show_server_via_sdk` mock (no real SDK
  import, no network), plus live regression tests that construct the real
  `ShowServerRequest` and a real `ServerDetail` when `huaweicloudsdkecs` is
  installed (skipped otherwise).
- Cases cover: write-intent guard (including "data values are not scanned",
  including the `--md-file` export path), instance-ID validation (empty /
  whitespace), command construction (`--server_id` is the real ShowServer
  parameter), JSON extraction (nested / flat / absent server), failure
  classification (missing AK/SK / 403 / 404 / generic / `[USE_ERROR]` with rc=0),
  the single-call show path, SDK fallback (success / unavailable), SDK field
  remapping, SDK object serialization safety, detail rendering, Markdown export
  (`render_markdown` / `write_markdown`: key fields, private+public IPs, region
  line, missing fields, `|` escaping, extra-fields section, overwrite /
  invalid-path errors), and all main() output / error paths.

## Live verification (when credentials exist)

The skill's entry point is the script; each command below exercises the
KooCLI path (or the SDK fallback) end-to-end:

```bash
python3 scripts/show_ecs.py --instance-id <real_server_id>
python3 scripts/show_ecs.py --instance-id <real_server_id> --json
python3 scripts/show_ecs.py --instance-id <real_server_id> --region cn-south-1
python3 scripts/show_ecs.py --instance-id <real_server_id> --md-file ./ecs-detail.md
```

Without `--md-file` the script prints to stdout only and writes no file. To
check JSON validity, pipe the `--json` output to `python3 -m json.tool`
manually; to check the Markdown export, open the written `.md` file (it contains
a key-fields table plus an "其他字段" table for any extra response fields).

For reference, the raw KooCLI invocations the script wraps internally
(illustrative — require KooCLI installed):

```text
hcloud configure list
hcloud ECS ShowServer --cli-region=cn-north-4 --server_id=<real_server_id>
```

## REST path provenance

`GET /v1/{project_id}/cloudservers/{server_id}` comes from the official
`huaweicloudsdkecs` v2 client `_show_server_http_info` `resource_path` metadata
(the same path the SDK fallback invokes through `EcsClient.show_server`). No
endpoint was inferred from naming patterns.

- `ShowServerRequest` exposes a single operation parameter, `server_id` —
  this is why the KooCLI argv uses `--server_id=<id>` (project_id is resolved
  from the credential profile / passed to `BasicCredentials` on the SDK path).
- The response model `ShowServerResponse` exposes `server` (`ServerDetail`) —
  `extract_server()` unwraps the `server` object and also tolerates a flat
  server object (defense in depth).
- The SDK `to_dict()` emits Python attribute names (`access_i_pv4`,
  `os_ext_a_zavailability_zone`); `sdk_server_to_dict()` remaps them to the
  OpenAPI wire names (`accessIPv4`, `OS-EXT-AZ:availability_zone`) via
  `ServerDetail.attribute_map` so the CLI and SDK paths produce the same shape.
- A 404 / "server not found" response is surfaced as `NotFoundError`
  (`未找到该 ECS 实例`), not a generic API error.

## IAM action provenance

`ecs:cloudServers:get` is the ECS detail action (documented under ECS
《权限及授权项说明》); it is the read-only counterpart of the mutating
`ecs:cloudServers:create` / `delete` / `start` / `stop` actions. The
least-privilege policy JSON lives in `references/iam-policies.md`.