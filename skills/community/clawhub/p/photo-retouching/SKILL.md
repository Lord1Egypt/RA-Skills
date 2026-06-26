---
name: runninghub-comfyui
description: Execute RunningHub ComfyUI workflows via API. Use when you need to run ComfyUI workflows on RunningHub cloud platform, submit tasks, query status, and retrieve results.
---

# RunningHub ComfyUI Workflow Runner

This skill provides tools to execute ComfyUI workflows on the RunningHub cloud platform via API.

## Prerequisites

1. **RunningHub Account** - Register at https://www.runninghub.ai/?inviteCode=kol01-rh124
2. **API Access** - Basic membership or above (free users cannot use API)
3. **API Key** - Get your 32-character API KEY from the API Console
4. **Workflow ID** - The workflow must have been successfully run manually at least once

## Getting API Key

1. Login to RunningHub
2. Click your avatar in the top-right corner
3. Go to "API Console"
4. Copy your API KEY (keep it secure!)

## Getting Workflow ID

1. Open the target workflow page
2. Get the ID from the URL: `https://www.runninghub.ai/#/workflow/WORKFLOW_ID`
3. Example: ID is `1987728214757978114`

## Setup API Key

### Option 1: Save to Config File (Recommended)

```bash
cd /root/.openclaw/workspace/skills/runninghub-comfyui
python3 scripts/runninghub_client.py --save-key YOUR_API_KEY
```

The API key will be saved to `config.json` and automatically loaded for future runs.

### Option 2: Environment Variable

```bash
export RUNNINGHUB_API_KEY=YOUR_API_KEY
```

### Option 3: Command Line (Each Time)

```bash
python3 scripts/runninghub_client.py --api-key YOUR_API_KEY ...
```

## Usage

### Submit Workflow Task (Default Configuration)

For workflows using default configuration:

```bash
cd /root/.openclaw/workspace/skills/runninghub-comfyui

python3 scripts/runninghub_client.py \
  --workflow-id 1987728214757978114 \
  --action submit
```

### Run Workflow with Custom Image (NEW!)

Upload an image and run the workflow with it:

```bash
python3 scripts/runninghub_client.py \
  --workflow-id 1987728214757978114 \
  --action run-with-image \
  --image /path/to/your/image.png \
  --node-id 107 \
  --field-name image
```

**Parameters:**
- `--image`: Path to the local image file
- `--node-id`: The node ID for image input (default: 107)
- `--field-name`: The field name for image input (default: image)

### Query Task Status

```bash
python3 scripts/runninghub_client.py \
  --task-id TASK_ID \
  --action query
```

### Wait for Completion

```bash
python3 scripts/runninghub_client.py \
  --task-id TASK_ID \
  --action wait \
  --poll-interval 5 \
  --max-attempts 60
```

## Python API Usage

```python
from runninghub_client import RunningHubClient, load_config, get_api_key

# Get API key from config
api_key = get_api_key()

# Initialize client
client = RunningHubClient(api_key)

# Upload image and get URL
image_url = client.upload_image("/path/to/image.png")
print(f"Image URL: {image_url}")

# Submit workflow with custom image
result = client.submit_workflow_with_image(
    workflow_id="1987728214757978114",
    node_id="107",
    field_name="image",
    image_url=image_url
)

task_id = result["taskId"]

# Wait for completion
final_result = client.wait_for_completion(task_id)

# Get output URLs
if final_result.get("status") == "SUCCESS":
    for item in final_result.get("results", []):
        print(f"Output: {item.get('url')}")
```

## API Reference

### RunningHubClient Class

#### `__init__(api_key: str)`
Initialize the client with your API KEY.

#### `upload_image(image_path: str) -> Optional[str]`
Upload an image file to RunningHub and get the URL.

**Returns:**
- Image URL on success
- `None` on failure

#### `submit_workflow(workflow_id: str, node_info_list: Optional[list]) -> Dict`
Submit a workflow task for execution.

**Parameters:**
- `workflow_id`: The workflow ID from RunningHub
- `node_info_list`: Node configuration list (optional)

**Important:** Use `fieldValue` (not `value`) in node_info_list:

```python
node_info_list = [
    {
        "nodeId": "107",
        "fieldName": "image",
        "fieldValue": "https://..."  # ✅ Use fieldValue, not value
    }
]
```

**Returns:**
```json
{
  "taskId": "TASK_ID",
  "status": "RUNNING",
  "clientId": "CLIENT_ID"
}
```

#### `submit_workflow_with_image(workflow_id: str, node_id: str, field_name: str, image_url: str) -> Dict`
Submit a workflow with an image input (convenience method).

**Example:**
```python
result = client.submit_workflow_with_image(
    "1987728214757978114",  # workflow_id
    "107",                   # node_id
    "image",                 # field_name
    "https://..."            # image_url
)
```

#### `query_task(task_id: str) -> Dict`
Query the status of a submitted task.

**Returns:**
```json
{
  "status": "RUNNING|SUCCESS|FAILED",
  "results": [
    {"url": "https://...", "filename": "..."}
  ]
}
```

#### `wait_for_completion(task_id: str, poll_interval: int, max_attempts: int) -> Dict`
Wait for a task to complete by polling status.

### Image Upload

**Endpoint:** `POST /openapi/v2/media/upload/binary`

**Headers:**
- `Authorization: Bearer <api_key>`

**Body:**
- Multipart form-data with file field

**Response:**
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "type": "image",
    "download_url": "https://...",
    "fileName": "openapi/...",
    "size": "3490"
  }
}
```

### Submit Workflow with Custom Input

**Endpoint:** `POST /openapi/v2/run/workflow/{workflow_id}`

**Headers:**
- `Authorization: Bearer <api_key>`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "apiKey": "your-api-key",
  "workflowId": "1987728214757978114",
  "addMetadata": true,
  "nodeInfoList": [
    {
      "nodeId": "107",
      "fieldName": "image",
      "fieldValue": "https://..."  // ✅ Use fieldValue, not value
    }
  ],
  "instanceType": "default",
  "usePersonalQueue": "false"
}
```

**Important:** Use `fieldValue` not `value` for node input values!

## Important Notes

1. **Use `fieldValue` not `value`**: When passing node input values via API, always use `fieldValue`:
   ```json
   {"nodeId": "107", "fieldName": "image", "fieldValue": "..."}  // ✅ Correct
   {"nodeId": "107", "fieldName": "image", "value": "..."}       // ❌ Wrong
   ```

2. **Rate Limiting**: Basic members have concurrency limits (usually 1 task at a time)

3. **Error 421**: "API queue limit reached" - Wait for previous tasks to complete

4. **Authentication**: Uses `Authorization: Bearer <api_key>` header

5. **API Endpoints**:
   - Submit: `POST /openapi/v2/run/workflow/{workflow_id}`
   - Query: `POST /openapi/v2/query`
   - Upload: `POST /openapi/v2/media/upload/binary`

## Troubleshooting

### "Invalid node info" (Error 803)
- Check that you're using `fieldValue` not `value`
- Verify the nodeId and fieldName match the workflow configuration
- Use the workflow's `getJsonApiFormat` endpoint to check available nodes

### "API queue limit reached" (Error 421)
- Wait 2-3 minutes and retry
- Check RunningHub web console for running tasks
- Cancel tasks from web console if needed

### "TOKEN_INVALID" (Error 412)
- Verify your API KEY is correct (32 characters)
- Check if your membership is active
- Try regenerating the API KEY from console

### Task stuck in "RUNNING"
- Large workflows may take several minutes
- Check RunningHub web console for actual progress
- Contact support if task runs too long
