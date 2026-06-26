# Mallary Profiles

Profiles are used to group your social media accounts. You can create a profile for each of your businesses, and then connect your social media accounts for each business inside this profile. Your default profile will be used if you don't pass a `profile_id` when making requests.

Mallary profiles group social platform connections, posts, analytics, and brand or AI auto-reply settings. The dashboard has one top-level **Dashboard profile** bar; once a profile is selected there, posts, platforms, analytics, and settings underneath the dashboard belong to that selected profile.

## Default Profile

Every user has a default profile. If a CLI command or API request omits `profile_id`, Mallary uses the user's default profile.

Use a non-default profile when a user manages more than one brand, business, client, or set of social accounts.

## Public Profile IDs

Profiles have random public IDs such as `AbC123xYz90`. Use these public IDs in CLI flags and API payloads, not internal database IDs.

Find the profile ID in either place:

```bash
mallary profiles list
mallary profiles list --json
```

Or copy it from the **Dashboard profile** bar in the Mallary dashboard.

## CLI Commands That Accept Profiles

The CLI can list profiles and target a profile with `--profile-id`:

```bash
mallary profiles list
mallary posts create --message "Launch update" --platform linkedin --profile-id AbC123xYz90
mallary posts list --profile-id AbC123xYz90
mallary analytics list --profile-id AbC123xYz90
mallary settings get --profile-id AbC123xYz90
mallary settings update --file settings.partial.json --profile-id AbC123xYz90
mallary platforms list --profile-id AbC123xYz90
mallary platforms disconnect facebook --profile-id AbC123xYz90
```

In file mode, send `profile_id` in the JSON payload:

```json
{
  "profile_id": "AbC123xYz90",
  "message": "Launch update",
  "platforms": ["facebook", "linkedin"]
}
```

The CLI currently lists and targets profiles. Create and rename profile workflows are handled in the dashboard or by the REST API.

## API Endpoints

Profile-aware API behavior:

- `GET /api/v1/profiles` lists profiles, each profile's connected platforms, and the user's profile/account limit.
- `POST /api/v1/profiles` creates a named non-default profile.
- `POST /api/v1/profiles/{id}` renames a profile.
- `profile_id` can be sent when creating posts, listing posts, listing analytics, listing platforms, disconnecting a platform, and reading or updating settings.
- Omitting `profile_id` selects the default profile.

## Profile-Scoped Behavior

- Platform connections are profile-scoped. Connect accounts in the dashboard after selecting the intended Dashboard profile.
- Posts and grouped post history are profile-scoped.
- Analytics queries are profile-scoped.
- Settings are profile-scoped, including `auto_reply_enabled`, business fields, brand profile text, and AI auto-reply context.
- `--auto-reply-enabled` on a post still depends on the selected profile's saved settings and plan access.

## Limits

`GET /api/v1/profiles` returns `data.limits.max_accounts_per_platform`. The dashboard uses that value to disable **New profile** once the user reaches their allowed profile/account count.

Current backend limit values:

| Plan | Limit |
| --- | ---: |
| Free | 1 |
| Starter | 4 |
| Pro | 10 |
| Business | 50 |

CLI access is paid-plan only, but Free users still have a default profile in the dashboard.
