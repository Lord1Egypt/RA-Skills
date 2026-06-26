# API Reference

## Purpose

The skill talks to a restricted OpenNebula control plane API that exposes a narrow VM lifecycle surface for disposable environments.

## Endpoints

- `GET /health`
- `GET /vms`
- `POST /vms`
- `DELETE /vms/<vm_id_or_name>`

Prefer readable VM and template names over numeric identifiers whenever possible.

## Create VM

Request body:

```json
{
  "template_name": "curated-ubuntu-24-04-for-nebula-claw-developer",
  "name": "test-nebula-api-2026-04-10"
}
```

Optional OpenNebula credential override for testing:

```json
{
  "template_name": "curated-ubuntu-24-04-for-nebula-claw-developer",
  "name": "test-nebula-api-2026-04-10",
  "one_user": "restrictedapi",
  "one_password": "change-me"
}
```

## Delete VM

Delete by name when possible:

```text
DELETE /vms/test-nebula-api-2026-04-10
```

## Expected environment inputs

The skill expects an API base URL to be available to the helper script, typically through the `NEBULA_CLAW_DEVELOPER_API_BASE` environment variable.

Example:

```bash
NEBULA_CLAW_DEVELOPER_API_BASE=http://10.1.1.130:8080 ./scripts/vm_api.sh health
```

Do not hardcode one deployment-specific endpoint into the published skill unless the installation explicitly targets one environment.

## Current example environment

- restricted API user: `restrictedapi`
- curated template: `curated-ubuntu-24-04-for-nebula-claw-developer`
- example network: `vm`

The API can also expose a configured curated template catalog via `GET /templates` and in the `templates` field of `GET /health` and `GET /vms`.

## Curl examples

Health:

```bash
curl "$NEBULA_CLAW_DEVELOPER_API_BASE/health"
```

List:

```bash
curl "$NEBULA_CLAW_DEVELOPER_API_BASE/vms"
```

Create:

```bash
curl -X POST "$NEBULA_CLAW_DEVELOPER_API_BASE/vms" \
  -H "Content-Type: application/json" \
  -d '{"template_name":"curated-ubuntu-24-04-for-nebula-claw-developer","name":"test-nebula-api-2026-04-10"}'
```

Delete:

```bash
curl -X DELETE "$NEBULA_CLAW_DEVELOPER_API_BASE/vms/test-nebula-api-2026-04-10"
```

## Notes

- If the configured OpenNebula user is `oneadmin`, the API omits `--user`.
- If the configured OpenNebula user is not `oneadmin`, the API adds `--user` and `--password`.
- `GET /vms` should include guest IP when OpenNebula reports it via VM NIC data.
- The config should contain a curated `templates` list, each with `name` and `description`, and `POST /vms` should only allow those templates when the list is configured.
- The current delete path maps to a hard terminate action in OpenNebula.
