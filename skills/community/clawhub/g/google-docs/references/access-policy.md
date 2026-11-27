# Google Docs access policy

An access policy limits which endpoints Google Docs connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-docs#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Google Docs: its 2 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create google-docs --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1/documents/{id}"},
    {"method": "GET", "path": "drive/v3/files"}
  ],
  "deny": []
}
```

## Endpoints

The Google Docs endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | v1/documents | write | documents | Creates a blank document using the title given in the request. |
| GET | v1/documents/{id} | read | documents | Gets the latest version of the specified document. |
| POST | v1/documents/{id}:batchUpdate | write | documents | Applies one or more updates to the document. |
| GET | drive/v3/files | read | drive | Lists your documents through Drive: all of them with drive.readonly, or only those created or opened through Maton with drive.file. |
