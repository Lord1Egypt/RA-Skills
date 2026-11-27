# Google Forms access policy

An access policy limits which endpoints Google Forms connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-forms#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Google Forms: its 5 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create google-forms --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1/forms/{id}"},
    {"method": "GET", "path": "v1/forms/{id}/responses"},
    {"method": "GET", "path": "v1/forms/{id}/responses/{id}"},
    {"method": "GET", "path": "v1/forms/{id}/watches"},
    {"method": "GET", "path": "drive/v3/files"}
  ],
  "deny": []
}
```

## Endpoints

The Google Forms endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | v1/forms | write | forms | Create a new form using the title given in the provided form message in the request. |
| GET | v1/forms/{id} | read | forms | Get a form. |
| POST | v1/forms/{id}:batchUpdate | write | forms | Change the form with a batch of updates. |
| POST | v1/forms/{id}:setPublishSettings | write | forms | Updates the publish settings of a form. |
| GET | v1/forms/{id}/responses | read | responses | List a form's responses. |
| GET | v1/forms/{id}/responses/{id} | read | responses | Get one response from the form. |
| GET | v1/forms/{id}/watches | read | watches | Return a list of the watches owned by the invoking project. |
| POST | v1/forms/{id}/watches | write | watches | Create a new watch. |
| DELETE | v1/forms/{id}/watches/{id} | write | watches | Delete a watch. |
| POST | v1/forms/{id}/watches/{id}:renew | write | watches | Renew an existing watch for seven days. |
| GET | drive/v3/files | read | drive | Lists your forms through Drive (needs drive.readonly). |
