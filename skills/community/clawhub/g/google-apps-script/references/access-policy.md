# Google Apps Script access policy

An access policy limits which endpoints Google Apps Script connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-apps-script#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Google Apps Script: its 10 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create google-apps-script --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1/projects/{id}/deployments"},
    {"method": "GET", "path": "v1/projects/{id}/deployments/{id}"},
    {"method": "GET", "path": "v1/processes"},
    {"method": "GET", "path": "v1/processes:listScriptProcesses"},
    {"method": "GET", "path": "v1/projects/{id}"},
    {"method": "GET", "path": "v1/projects/{id}/content"},
    {"method": "GET", "path": "v1/projects/{id}/metrics"},
    {"method": "GET", "path": "v1/projects/{id}/versions"},
    {"method": "GET", "path": "v1/projects/{id}/versions/{id}"},
    {"method": "GET", "path": "drive/v3/files"}
  ],
  "deny": []
}
```

## Endpoints

The Google Apps Script endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1/projects/{id}/deployments | read | deployments | Lists the deployments of an Apps Script project. |
| POST | v1/projects/{id}/deployments | write | deployments | Creates a deployment of an Apps Script project. |
| GET | v1/projects/{id}/deployments/{id} | read | deployments | Gets a deployment of an Apps Script project. |
| PUT | v1/projects/{id}/deployments/{id} | write | deployments | Updates a deployment of an Apps Script project. |
| DELETE | v1/projects/{id}/deployments/{id} | write | deployments | Deletes a deployment of an Apps Script project. |
| GET | v1/processes | read | processes | List information about processes made by or on behalf of a user, such as process type and current status. |
| GET | v1/processes:listScriptProcesses | read | processes | List information about a script's executed processes, such as process type and current status. |
| POST | v1/projects | write | projects | Creates a new, empty script project with no script files and a base manifest file. |
| GET | v1/projects/{id} | read | projects | Gets a script project's metadata. |
| GET | v1/projects/{id}/content | read | projects | Gets the content of the script project, including the code source and metadata for each script file. |
| PUT | v1/projects/{id}/content | write | projects | Updates the content of the specified script project. |
| GET | v1/projects/{id}/metrics | read | projects | Get metrics data for scripts, such as number of executions and active users. |
| POST | v1/scripts/{id}:run | write | scripts | script.scripts.run (no description in the discovery document). |
| GET | v1/projects/{id}/versions | read | versions | List the versions of a script project. |
| POST | v1/projects/{id}/versions | write | versions | Creates a new immutable version using the current code, with a unique version number. |
| GET | v1/projects/{id}/versions/{id} | read | versions | Gets a version of a script project. |
| GET | drive/v3/files | read | drive | Lists your Apps Script projects through Drive (needs drive.readonly). |
