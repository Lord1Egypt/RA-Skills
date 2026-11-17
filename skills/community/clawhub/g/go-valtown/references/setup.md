# go-valtown: setup and reference

## Contents

- [Requirements](#requirements)
- [Install](#install)
- [Auth](#auth)
- [Operations](#operations)
- [Pagination](#pagination)
- [Union types](#union-types)
- [Enums](#enums)
- [Errors](#errors)

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A Val Town API token, created in the Val Town settings and read from `VALTOWN_API_TOKEN`.

## Install

```bash
go get github.com/psyb0t/go-valtown
```

The package name is `valtown`:

```go
import "github.com/psyb0t/go-valtown"
```

## Auth

Every request carries `Authorization: Bearer <token>`, set with `valtown.WithRequestEditorFn` as the SKILL.md example shows. The base URL is `https://api.val.town`.

## Operations

Each method below also has a plain variant without `WithResponse` that returns `*http.Response`, and the body-taking ones have a `...WithBodyWithResponse` variant that takes a content type and an `io.Reader`. Path parameters come first, then a `*<Op>Params` struct when the operation has query parameters, then the body.

| Method | HTTP |
|---|---|
| `AliasUsernameWithResponse` | `GET /v1/alias/{username}` |
| `MeGetWithResponse` | `GET /v1/me` |
| `UsersGetWithResponse` | `GET /v1/users/{user_id}` |
| `V1blobsListWithResponse` | `GET /v1/blob` |
| `V1blobsGetWithResponse` | `GET /v1/blob/{key}` |
| `V1blobsStoreWithResponse` | `POST /v1/blob/{key}` |
| `V1blobsDeleteWithResponse` | `DELETE /v1/blob/{key}` |
| `SqliteExecuteWithResponse` | `POST /v1/sqlite/execute` |
| `SqliteBatchWithResponse` | `POST /v1/sqlite/batch` |
| `EmailsSendWithResponse` | `POST /v1/email` |
| `TraceListWithResponse` | `GET /v1/telemetry/traces` |
| `LogListWithResponse` | `GET /v1/telemetry/logs` |
| `ValsList2WithResponse` | `GET /v2/vals` |
| `ValsCreate2WithResponse` | `POST /v2/vals` |
| `ValsGet2WithResponse` | `GET /v2/vals/{val_id}` |
| `ProjectsDelete2WithResponse` | `DELETE /v2/vals/{val_id}` |
| `MeVals2WithResponse` | `GET /v2/me/vals` |
| `AliasVal2WithResponse` | `GET /v2/alias/vals/{username}/{val_name}` |
| `BranchesList2WithResponse` | `GET /v2/vals/{val_id}/branches` |
| `BranchesCreate2WithResponse` | `POST /v2/vals/{val_id}/branches` |
| `BranchesGet2WithResponse` | `GET /v2/vals/{val_id}/branches/{branch_id}` |
| `BranchesDelete2WithResponse` | `DELETE /v2/vals/{val_id}/branches/{branch_id}` |
| `BranchesMergeUpstream2WithResponse` | `POST /v2/vals/{val_id}/branches/{branch_id}/merge-upstream` |
| `ValFilesGet2WithResponse` | `GET /v2/vals/{val_id}/files` |
| `FilesCreate2WithResponse` | `POST /v2/vals/{val_id}/files` |
| `FileContentUpdate2WithResponse` | `PUT /v2/vals/{val_id}/files` |
| `FilesDelete2WithResponse` | `DELETE /v2/vals/{val_id}/files` |
| `FilesContentGet2WithResponse` | `GET /v2/vals/{val_id}/files/content` |
| `QueryValFileByIdWithResponse` | `GET /v2/files/{file_id}` |
| `ValEnvironmentVariablesListWithResponse` | `GET /v2/vals/{val_id}/environment_variables/` |
| `ValEnvironmentVariablesCreateWithResponse` | `POST /v2/vals/{val_id}/environment_variables/` |
| `ValEnvironmentVariablesUpdateWithResponse` | `PUT /v2/vals/{val_id}/environment_variables/{key}` |
| `ValEnvironmentVariablesDeleteWithResponse` | `DELETE /v2/vals/{val_id}/environment_variables/{key}` |
| `ValEnvironmentVariableGroupsListWithResponse` | `GET /v2/vals/{val_id}/environment_variable_groups/` |
| `ValEnvironmentVariableGroupsAttachWithResponse` | `PUT /v2/vals/{val_id}/environment_variable_groups/{group_id}` |
| `ValEnvironmentVariableGroupsDetachWithResponse` | `DELETE /v2/vals/{val_id}/environment_variable_groups/{group_id}` |
| `OrgsListWithResponse` | `GET /v2/orgs` |
| `OrgsMembershipsListWithResponse` | `GET /v2/orgs/{org_id}/memberships` |
| `V2blobsListWithResponse` | `GET /v2/blob` |
| `V2blobsGetWithResponse` | `GET /v2/blob/{key}` |
| `V2blobsStoreWithResponse` | `POST /v2/blob/{key}` |
| `V2blobsDeleteWithResponse` | `DELETE /v2/blob/{key}` |
| `EnvironmentVariableGroupsListWithResponse` | `GET /v3/environment-variable-groups/` |
| `EnvironmentVariableGroupsCreateWithResponse` | `POST /v3/environment-variable-groups/` |
| `EnvironmentVariableGroupsRenameWithResponse` | `PUT /v3/environment-variable-groups/{id}` |
| `EnvironmentVariableGroupsDeleteWithResponse` | `DELETE /v3/environment-variable-groups/{id}` |
| `EnvironmentVariableGroupsGetWithResponse` | `GET /v3/environment-variable-groups/{id}/environment-variables` |
| `EnvironmentVariableGroupsCreateVariableWithResponse` | `POST /v3/environment-variable-groups/{id}/environment-variables` |
| `EnvironmentVariableGroupsUpsertVariableWithResponse` | `POST /v3/environment-variable-groups/{id}/environment-variables/{key}` |
| `EnvironmentVariableGroupsVariableDeleteWithResponse` | `DELETE /v3/environment-variable-groups/{id}/environment-variables/{key}` |
| `GetV3ValViewerWithResponse` | `GET /v3/val/viewer` |
| `PostV3ConnectionsSlackTokenWithResponse` | `POST /v3/connections/slack/token` |
| `PostV3ConnectionsGoogleDocsTokenWithResponse` | `POST /v3/connections/google-docs/token` |

## Pagination

List endpoints return `Data` plus `Links` (`valtown.PaginationLinks`, with `Self` and optional `Next` and `Prev` URLs). Page with the params struct. `ValsList2Params` takes `Limit` (required) and a `Cursor` time; other lists such as `MeVals2Params` take `Offset` and `Limit`, both required. Stop when `Links.Next` is nil.

## Union types

Fields that accept more than one shape are structs with `From<Variant>` (set) and `As<Variant>` (read) methods. `SqliteExecuteJSONBody_Statement` is a plain SQL string (`FromSqliteExecuteJSONBodyStatement0`) or a `SqliteExecuteJSONBodyStatement1` with `Sql` and `Args`, where `Args` holds positional (`[]interface{}`) or named (`map[string]interface{}`) arguments.

## Enums

Enum fields have a named type and constants, for example `ValsList2ParamsPrivacyPublic`, `ValsCreate2JSONBodyPrivacyPrivate` or `ValPrivacyUnlisted`. Grep `client.gen.go` for the type name to list the values.

## Errors

| Situation | What you get |
|---|---|
| Network or encoding failure | non-nil `err` |
| HTTP 2xx with JSON | `res.JSON200`, or `res.JSON201` for creates |
| HTTP 4xx/5xx | `err == nil`, the 2xx field nil, the matching `res.JSONxxx` field when the spec declares one, the raw body in `res.Body` |
