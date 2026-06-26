# MDShare Agent Install Examples

Use this reference when wiring the packaged skill into OpenClaw or another skill-based agent runtime.

## Packaged file

Use the packaged artifact:

```text
D:\project\mdshare\dist\mdshare-agent.skill
```

## Example 1: Install into a skill-based runtime

Typical pattern:

1. Import or install `mdshare-agent.skill` into the runtime's skill directory.
2. Enable the skill.
3. Let the runtime load `SKILL.md` and bundled `references/`.

If the runtime expects an unpacked folder instead of a `.skill` file, use:

```text
D:\project\mdshare\skills\mdshare-agent
```

## Example 2: Trigger phrases

These user requests should trigger the skill:

- “帮我把这段 markdown 生成临时链接”
- “share this markdown note”
- “read this MDShare link”
- “update this temporary share”
- “delete this MDShare document”

## Example 3: Agent tool call shape

If the agent can call HTTP directly, the skill should guide it toward requests like:

```http
POST https://share.yekyos.com/api/shares
Content-Type: application/json
```

```json
{
  "markdownContent": "# Hello\n\nFrom agent",
  "expiresInHours": 168,
  "password": "",
  "burnMode": "OFF",
  "editableMode": "READ_ONLY"
}
```

## Example 4: Returned output style

Recommended agent reply after creating a share:

```text
分享已创建。
公开访问：https://share.yekyos.com/s/{slug}
管理链接：https://share.yekyos.com/e/{slug}#manage={ownerToken}
```

Only include the edit link when edit mode is enabled.

## Example 5: Safe behavior

When integrating this skill into a general-purpose agent:

- Do not expose manage or edit links unless the user asks for them or needs them.
- Do not auto-confirm burn-after-read access without user intent.
- Do not create a share when the task is only local Markdown formatting or preview.
