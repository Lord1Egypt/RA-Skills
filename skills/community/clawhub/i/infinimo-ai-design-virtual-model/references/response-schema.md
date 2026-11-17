# Virtual Model — Response Schema

## GET /aigc/image/virtual_model_create

Query params: `base_image_url`, `base_image_type`, optional `bg_image_url`, `prompt`, `face_prompt`, `num`, `aspect_radio`.

Submit returns immediately; poll logs for output.

## GET /aigc/log/list?type=101

| logs[] field | Description |
|--------------|-------------|
| logId | Record id |
| createTime | Timestamp |
| param | Submit params |
| data.type | `image` when ready |
| data.data | Output URL array |

## GET /aigc/log/delete?log_id=

Deletes a log record.
