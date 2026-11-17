# Rednote Collect API

Verified from HotBee public bundle:

- Endpoint: `POST https://www.smsz.xyz/prod-api/tool/rednote/xhs_note_content`
- Parameters: `key`, `note_url`
- Transport in the package CLI: query parameters with POST.

Scope limit:

- This verifies note content parsing.
- Rednote account/profile/search endpoints were not found in the public bundle. Do not invent them.

Example:

```bash
npx -y github:shanye1402-hash/hotbee-social-data-skills#v1.1.0 call rednote --dry-run --url "https://www.xiaohongshu.com/explore/xxxx"
```
