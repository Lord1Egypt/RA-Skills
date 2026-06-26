# REST API

## Authorization {#authorization}
You can only access the REST API via https. In order to access the REST API you need to use an Access Token. You can generate an Access Token by going to your Organization's Account page.
In the API Tokens section click on Generate Token.
Give your token a name and click the button to create your new token. A new window will appear showing you your new access token.
Make sure you note that down because you will not be able to see the token once you close this window. This token is meant to be kept secret so do not share it with anyone other than your team (for example do not post this on forums).
From your Account page you can also Revoke all the tokens you have generated or a specific one. You can also edit the name of a token.
When you make calls to the API you must set the 'Authorization' header in your HTTP request to this value:
```none
Bearer [access_token]
```
Replace `[access_token]` with an Access Token you generated in your Account page.
For example:
```none
curl -H "Authorization: Bearer nesgdxhiqe7hylfilr6ss1rds0gq1uj8" https://playcanvas.com/api/...
```
## Parameters {#parameters}
Various routes accept a number of parameters. For GET requests if the parameter is not part of the URL, you can pass it as an HTTP query string parameter. For POST, PUT and DELETE requests parameters not included in the URL should be encoded as JSON with a Content-Type of 'application/json'.
There are several common parameters that are used in each endpoint:
### project_id {#project_id}
This can be found in the URL on the project overview page.
### scenes {#scenes}
When opening a scene in the Editor, the scene id is in the URL.
### branch_id {#branch_id}
This is found in the [version control](/user-manual/editor/version-control/) panel and can be selected and copied.
## Response Format {#response-format}
Our REST API is following some generic guidelines when it comes to the response format of each API call.
### GET resource {#get-resource}
If you are trying to GET a single resource the response will be a JSON object with the resource you requested.
### GET multiple resources {#get-multiple-resources}
If you are trying to GET multiple resources like for example listing the Apps of a Project you will get a JSON object with this format:
```none
{
    "result": [
        resource_1,
        resource_2,
        ...,
        resource_N
    ],
    "pagination": {
        "limit": number,
        "skip": number,
        "total": number
    }
}
```
As you can notice the response in this case also contains pagination data. To control the pagination of the response you can pass the following URL parameters:
| Name    | Description                                                                                                                      |
| ------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `limit` | The maximum number of items to include in the response.                                                                          |
| `skip`  | The number of items to skip from the original result set.                                                                        |
| `sort`  | The name of the field to use to sort the result set. See the documentation of each request to see which values are allowed here. |
| `order` | If you want results in ascending order pass 1 otherwise pass -1 for descending order.                                            |
So for example to get 32 items after the first 16 items you would send this request:
```none
https://playcanvas.com/api/items?limit=32&amp;skip=16
```
### Errors {#errors}
When an error is raised you will get a JSON object with this format:
```json
{
    "error": "This is the error message"
}
```
Also the status code of the response will be the appropriate HTTP error code.
## Rate Limiting {#rate-limiting}
Calls to the REST API have a rate limit. Check your actual limits by querying [this endpoint](https://playcanvas.com/api/ratelimits). There are different rate limits depending on the request:
| Rate Limit Type | Description               | Limit for free accounts | Limit for personal/org accounts |
| --------------- | ------------------------- | ----------------------- | ------------------------------- |
| Normal          | The normal rate limit     | 120 requests/minute     | 240 requests/minute             |
| Strict          | The strict rate limit     | 5 requests/minute       | 10 requests/minute              |
| Assets          | The assets rate limit     | 60 requests/minute      | 120 requests/minute             |
The response will contain the following headers to help you regulate how often you call the API:
| Name                    | Description                                                                                                             |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `X-RateLimit-Limit`     | The number of requests allowed in a minute.                                                                             |
| `X-RateLimit-Remaining` | The remaining number of requests that you are allowed to make this minute.                                              |
| `X-RateLimit-Reset`     | The time at which the current rate limit window resets in [UTC epoch seconds](https://en.wikipedia.org/wiki/Unix_time). |
If you exceed the rate limit you will get a `429 Too Many Requests` status code. You will have to wait for the current window to reset in order to continue making requests.
## Download App
`POST https://playcanvas.com/api/apps/download`
Starts app export job (static or npm format). Poll [job by id](/user-manual/api/job-get) until complete.
**Required:** `project_id` (number), `name` (string), `scenes` (number[] — first = initial scene).
**Optional:** `branch_id`, `description`, `version`, `release_notes`, `scripts_concatenate`, `scripts_minify` (default true), `scripts_sourcemaps`, `optimize_scene_format`, `format` (`static`|`npm`), `engine_version`.
Response `201`: job with `status` (running|complete|error), `id`, `data`. Strict rate limit.
Errors: 401, 403, 404, 429.
## Get App
`GET https://playcanvas.com/api/apps/:id`
Returns: `id`, `project_id`, `owner_id`, `name`, `description`, `version`, `release_notes`, `thumbnails` (s/m/l/xl), `size`, `views`, `completed_at`, `created_at`, `modified_at`, `url`.
Normal rate limit. Errors: 401, 403, 404, 429.
## Get Primary App
`GET https://playcanvas.com/api/projects/:projectId/app`
Same response as Get App. Normal rate limit.
Errors: 401, 403, 404 (project/no primary/app), 429.
## List Project Apps
`GET https://playcanvas.com/api/projects/:projectId/apps`
Returns `result` array + `pagination`. Normal rate limit.
Errors: 401, 403, 404, 429.
## Assets
Base URL: `https://playcanvas.com/api`
## Create Asset
`POST /api/assets`
**Required:** `project_id` (number), `name` (string), `type` (string — asset type).
**Optional:** `folder_id`, `preload`, `data`, `tags`, `source_asset_id`, `region` (default: "eu-west-1").
Response `201`: asset object with `id`, `name`, `type`, `tags`, `preload`, `file`, `data`, `region`, `created_at`, `modified_at`.
Strict rate limit. Errors: 401, 403, 404, 429.
## Get Asset
`GET /api/assets/:id`
Returns full asset details including `id`, `name`, `type`, `tags`, `preload`, `file`, `data`, `source_asset_id`, `created_at`, `modified_at`.
Normal rate limit. Errors: 401, 403, 404, 429.
## List Assets
`GET /api/projects/:projectId/assets`
Query params: `type` (filter), `folder_id`, `search`, `tags`, `limit`, `skip`, `sort`, `order`.
Returns `result` array + `pagination`. Normal rate limit.
## Update Asset
`PUT /api/assets/:id`
Updatable fields: `name`, `tags`, `preload`, `data`, `folder_id`.
Normal rate limit. Errors: 401, 403, 404, 429.
## Delete Asset
`DELETE /api/assets/:id`
**Query params:** `force` (boolean) — required if asset has references.
Normal rate limit. Errors: 401, 403, 404, 409 (has references), 429.
## Upload Asset File
`POST /api/assets/:id/files`
Upload or replace the file for an existing asset. Multipart form: `file` field.
Subsequent calls replace the previous file. Strict rate limit (1 request per asset per 30s).
Errors: 401, 403, 404, 429, 503 (retry later).
## Version Control
### Create Branch
`POST /api/projects/:projectId/branches`
**Required:** `name` (string), `sourceCheckpointId` (number). **Optional:** `description`.
Response `201`: branch with `id`, `name`, `checkpoint_id`, `created_at`. Strict rate limit.
### List Branches
`GET /api/projects/:projectId/branches`
Returns array of branches with `id`, `name`, `checkpoint_id`, `latest_checkpoint_id`, `favorite`, `status` (open|closed), `created_at`, `closed_at`. Normal rate limit.
### Create Checkpoint
`POST /api/projects/:projectId/checkpoints`
**Required:** `name` (string), `branchId` (string). **Optional:** `description`.
Response `201`: checkpoint with `id`, `name`, `description`, `branch_id`, `created_at`. Strict rate limit.
### Get Checkpoint
`GET /api/checkpoints/:id`
Returns checkpoint details with `id`, `name`, `description`, `branch_id`, `created_at`. Normal rate limit.
### List Checkpoints
`GET /api/projects/:projectId/checkpoints`
Query: `branchId` (required). Returns array of checkpoints. Normal rate limit.
### Merge Branches
`POST /api/projects/:projectId/merge`
**Required:** `sourceBranchId` (string), `targetBranchId` (string). **Optional:** `deleteSourceBranch` (boolean), `force` (boolean — resolve all conflicts using source).
Response `200`: `job_id` — poll via [job-get](/user-manual/api/job-get). Strict rate limit.
## Export Project
`POST /api/projects/:projectId/export`
**Optional:** `branch_id`, `scenes`, `format` (`static`|`npm`).
Starts export job. Poll via job-get. Response `201`. Strict rate limit.
## Job Status
`GET /api/jobs/:id`
Returns job: `status` (running|complete|error), `messages`, `data`, `created_at`, `modified_at`.
Normal rate limit.
## Splat Publish
`POST /api/projects/:projectId/splats/publish`
**Required:** `name`, `asset_id` (gsplat asset). **Optional:** `description`.
Publishes a Gaussian Splat. Response `201`. Strict rate limit.
