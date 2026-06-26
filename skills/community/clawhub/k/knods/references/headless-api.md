# Knods Headless Flow Execution API

Use this mode when the task is not an interactive canvas chat turn, but a programmatic flow execution:

1. `GET /api/v1/knods` to discover flows
2. `GET /api/v1/knods/:flowId` to inspect inputs
3. `POST /api/v1/knods/:flowId/run` to start
4. `GET /api/v1/runs/:runId` until status is terminal
5. Read `outputs` or `error`

Auth:

- Base URL: `https://<instance>/api/v1`
- Header: `Authorization: Bearer knods_...`
- Required scopes: `knods:read`, `knods:run`

Input schema:

- `inputs` is an array
- every item requires:
  - `nodeId`
  - `content`
  - `type`
- valid `type` values:
  - `text`
  - `image`
  - `video`
  - `audio`

Run statuses:

- `pending`
- `running`
- `completed`
- `failed`
- `cancelled`

Polling guidance:

- initial delay: about 1 second
- interval: 2-3s for text/image, 5-10s for video
- timeout: 5 minutes max
- on `429`, back off and retry

Limitations:

- no webhooks
- no credit balance endpoint for API keys
- no streaming outputs
- rate limit is IP-based

Packaged client:

```bash
python3 {baseDir}/scripts/knods_headless.py list
python3 {baseDir}/scripts/knods_headless.py get --flow-id <id>
python3 {baseDir}/scripts/knods_headless.py run --flow-id <id> --inputs-json '[...]'
python3 {baseDir}/scripts/knods_headless.py wait --run-id <id>
python3 {baseDir}/scripts/knods_headless.py run-wait --flow-id <id> --inputs-json '[...]'
python3 {baseDir}/scripts/knods_headless.py cancel --run-id <id>
```

Environment:

- `KNODS_API_BASE_URL`
- `KNODS_API_KEY`

If `KNODS_API_BASE_URL` is missing, the client can derive it from `KNODS_BASE_URL` by using the same origin and appending `/api/v1`.
