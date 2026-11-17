# Speech To Text API

Verified from HotBee public bundle:

- Endpoint: `POST https://www.smsz.xyz/prod-api/tool/speech/speechToText`
- Parameters: `key`, and one of:
  - `file_url`
  - `video_url`
- Transport in the package CLI: query parameters with POST.

Example:

```bash
npx -y github:shanye1402-hash/hotbee-social-data-skills#v1.1.0 call transcript --dry-run --file-url "https://example.com/audio.mp3"
```
