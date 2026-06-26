---
name: make-and-model-recogntion
description: Detect the largest vehicle from an image using TrafficEye car-box detection, run make and model recognition for that vehicle, and return all license plates attached to the same road-user payload. Use when the user wants the dominant vehicle, vehicle classification, car box detection, make and model recognition, or the plates associated with the main vehicle in a local image file. You can obtain API key and tokens from https://trafficeye.ai.
metadata:
  openclaw:
    requires:
      env:
        - TRAFFICEYE_API_KEY
      anyBins:
        - python3
        - python
    primaryEnv: TRAFFICEYE_API_KEY
    homepage: https://trafficeye.ai
    os:
      - linux
      - macos
      - windows
---

# TrafficEye Largest Road User Reader

Use this skill when the user wants the largest detected vehicle from an image, along with its make and model classification and every detected license plate belonging to that same road user.

## What This Skill Does

1. Accepts a local image path.
2. Uploads the image to the TrafficEye recognition API.
3. Sends a recognition request that asks for detection, OCR, and MMR with box preference by default.
4. Parses the API response, including responses wrapped as `{ "status": ..., "data": ... }`.
5. Picks the largest detected road user by `box.position` area.
6. Returns a wrapper object containing `roadUser`, `box`, `plates`, `area`, and `source`, preserving the full selected road-user payload.

## Expected Input

- A local image file path.
- If the user supplied an attachment instead of a path, first resolve it to a local file path and then run the helper.

## Default Runtime Assumptions

- The API endpoint defaults to `https://trafficeye.ai/recognition`.
- The default request payload is `{"tasks":["DETECTION","OCR","MMR"],"requestedDetectionTypes":["BOX","PLATE"],"mmrPreference":"BOX"}`.
- The default API-key transport matches the TrafficEye public API example: header mode with header name `apikey`.
- Auth and request fields remain configurable in case your deployment differs.

## Environment Variables

- `TRAFFICEYE_API_KEY`: required unless passed explicitly to the helper.
- `TRAFFICEYE_API_URL`: optional, defaults to `https://trafficeye.ai/recognition`.
- `TRAFFICEYE_API_KEY_MODE`: one of `header`, `bearer`, `form`, `query`. Default: `header`.
- `TRAFFICEYE_API_KEY_NAME`: key name for `header`, `form`, or `query` mode. Default: `apikey`.
- `TRAFFICEYE_FILE_FIELD`: multipart field for the image. Default: `file`.
- `TRAFFICEYE_REQUEST_FIELD`: multipart field for the JSON request. Default: `request`.
- `TRAFFICEYE_REQUEST_JSON`: JSON string to include as the request field. By default this is `{"tasks":["DETECTION","OCR","MMR"],"requestedDetectionTypes":["BOX","PLATE"],"mmrPreference":"BOX"}`.
- `TRAFFICEYE_TIMEOUT_S`: optional timeout in seconds. Default: `30`.

Only `TRAFFICEYE_API_KEY` is required for the default live API flow. The other variables are optional overrides.

## How To Run

Setup your API key:
```bash
export TRAFFICEYE_API_KEY='YOUR_REAL_KEY'
```

Use the road-user helper:

```bash
python3 recognize_road_user.py /absolute/path/to/image.jpg
```

For structured output:

```bash
python3 recognize_road_user.py /absolute/path/to/image.jpg --format json
```

If the deployment expects Bearer auth:

```bash
TRAFFICEYE_API_KEY_MODE=bearer python3 recognize_road_user.py /absolute/path/to/image.jpg
```

If the deployment needs an explicit request payload:

```bash
TRAFFICEYE_REQUEST_JSON='{"tasks":["DETECTION","OCR","MMR"],"requestedDetectionTypes":["BOX","PLATE"],"mmrPreference":"BOX"}' python3 recognize_road_user.py /absolute/path/to/image.jpg --format json
```

Equivalent to the documented public API example:

```bash
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -H "apikey: YOUR_API_KEY_HERE" \
  -F "file=@image.jpg" \
  -F 'request={"tasks":["DETECTION","OCR","MMR"],"requestedDetectionTypes":["BOX","PLATE"],"mmrPreference":"BOX"}' \
  https://trafficeye.ai/recognition
```

## Agent Workflow

1. Verify that the image path exists.
2. Run `python3 recognize_road_user.py <image-path> --format json`.
3. Present the full selected road-user payload to the user, especially `box`, `mmr`, and the complete `plates` array.
4. If the selected road user has no plates, explain that the largest vehicle was found but no plates were attached to that road user.
5. If authentication fails, ask the user which auth mode their deployment expects and retry with the matching environment variables.

## Offline Validation

You can validate the selection logic without calling the API:

```bash
python3 recognize_road_user.py --response-json-file examples/sample_response.json --format json
```

## Output Shape

The helper prints JSON with this top-level structure:

```json
{
  "roadUser": {"box": {}, "plates": [], "mmr": {}},
  "box": {},
  "plates": [],
  "area": 0,
  "source": {
    "combinationIndex": 0,
    "roadUserIndex": 0,
    "path": "combinations[0].roadUsers[0]"
  }
}
```

- `roadUser` is the original selected road-user payload from TrafficEye.
- `box` repeats `roadUser.box` for convenience.
- `plates` repeats `roadUser.plates` for convenience and may be empty.
- `area` is the computed rectangle area used for winner selection.
- `source` identifies where the selected road user came from in the API response.

## Notes

- The helper intentionally chooses the largest boxed vehicle by geometric area, not by detection confidence.
- The response parser first checks `data.combinations[].roadUsers[]`, then `combinations[].roadUsers[]`, then `roadUsers[]`, and finally nested road-user payloads discovered recursively.
- The default request and auth header mirror the public example at `https://www.trafficeye.ai/api`.
- The selected result now includes the original road-user payload from the API so `mmr`, `box`, all `plates`, and their scores are preserved.