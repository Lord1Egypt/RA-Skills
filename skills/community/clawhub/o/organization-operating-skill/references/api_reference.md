# API Reference Index

This index file is for navigation only and does not repeat the full details.
When using the skill, jump to the reference that matches the current task instead of loading every API contract at once.

Verified on: `2026-03-30`

## Environment Entry Points

- Default production base: `https://api.zingup.club/biz`
- Test environment: `https://test-api.groupoo.net/biz`
- Local development: `http://localhost:8080/biz`
- If neither `--base-url` nor `--env` is provided, the skill defaults to production.

## Reading Path

- Authentication, tokens, headers, and environment switching:
  read [auth_reference.md](auth_reference.md)
- Organization list, detail, create, update, members, and join flows:
  read [org_reference.md](org_reference.md)
- Post publishing, post share links, and post read limitations:
  read [content_reference.md](content_reference.md)
- Activity drafts, publish, search, signup, and share links:
  read [activity_reference.md](activity_reference.md)
- Capability priority and future gaps:
  read [capability_inventory.md](capability_inventory.md)

## Capability Map

| Capability ID | Reference |
| --- | --- |
| `auth.guest.generate` | [auth_reference.md](auth_reference.md) |
| `auth.agent.third_login` | [auth_reference.md](auth_reference.md) |
| `auth.refresh` | [auth_reference.md](auth_reference.md) |
| `user.profile.get` | [auth_reference.md](auth_reference.md) |
| `user.profile.update` | [auth_reference.md](auth_reference.md) |
| `web.config.get` | [org_reference.md](org_reference.md) |
| `org.list` | [org_reference.md](org_reference.md) |
| `org.detail` | [org_reference.md](org_reference.md) |
| `org.detail.manage` | [org_reference.md](org_reference.md) |
| `org.create` | [org_reference.md](org_reference.md) |
| `org.update` | [org_reference.md](org_reference.md) |
| `org.member.list` | [org_reference.md](org_reference.md) |
| `org.member.page` | [org_reference.md](org_reference.md) |
| `org.join` | [org_reference.md](org_reference.md) |
| `content.post.create` | [content_reference.md](content_reference.md) |
| `activity.save` | [activity_reference.md](activity_reference.md) |
| `activity.publish` | [activity_reference.md](activity_reference.md) |
| `activity.cancel` | [activity_reference.md](activity_reference.md) |
| `activity.delete` | [activity_reference.md](activity_reference.md) |
| `activity.detail` | [activity_reference.md](activity_reference.md) |
| `activity.search` | [activity_reference.md](activity_reference.md) |
| `activity.org.list` | [activity_reference.md](activity_reference.md) |
| `activity.user.sign.list` | [activity_reference.md](activity_reference.md) |
| `activity.sign.list` | [activity_reference.md](activity_reference.md) |
| `activity.signup` | [activity_reference.md](activity_reference.md) |

## Conventions

- Do not read every reference file by default.
- Start with `scripts/org_skill_cli.py --help`, then open only the references needed for the current task.
- Response shapes documented here follow the currently verified backend code and observed runtime behavior.
