# Provider notes

Fixed request rules for this skill:

- endpoint create: `POST /v1/video/create`
- endpoint status: `GET /v1/video/status`
- model: `Seedance-Pro-1.5`
- duration: `12`
- resolution: `720p`
- ratio from orientation:
  - portrait -> `9:16`
  - landscape -> `16:9`
- `provider_specific.generate_audio` must always be `true`
- polling interval: `30` seconds
- return plain text to caller, not JSON for Feishu delivery
