# Video Generation — Response Schema

## GET /aigc/ec_media/video/create/dic

`models`, `ratios`, `sizes`, `lengths` — each item `{ id, title }`; length `id` is seconds.

## POST /aigc/ec_media/video/point_calculate

Request: `create_mode`, `model`, `ratio`, `size`, optional `length`, `prompt`.  
Response `data`: numeric credit estimate.

## POST /aigc/ec_media/video/create

Required: `prompt`, `create_mode`, `model`, `ratio`, `size`. Optional: `length`, `attaches`.

## GET /aigc/ec_media/video/create/logs

`items[].url` = output video; `items[].param` = submit params.

## WebSocket

`{"type":"video_result_refresh"}` → re-fetch logs.
