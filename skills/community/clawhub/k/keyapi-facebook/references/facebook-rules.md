# Facebook Rules

Use this file for Facebook platform-level routing boundaries. Use module files for scenario-specific workflows.

## Entity Scope

public profiles, pages, profile IDs, profile posts, Reels, photos, public groups, group IDs, group posts, and future events

## Scenario Module Routing

- Use `facebook-profile-rules.md` for public profile/page resolution and baseline detail.
- Use `facebook-profile-content-rules.md` for profile/page posts, Reels, and photos.
- Use `facebook-group-rules.md` for public group resolution, group detail, group posts, and future events.

## Identifier Discipline

- Keep profile/page IDs and group IDs separate.
- Resolve URLs through the documented resolver before ID-only calls.
- Do not infer private, demographic, or membership data that the API does not return.

## Output Guidance

- For profile/page reports, separate identity facts from posts and media evidence.
- For group reports, separate group metadata, post activity, and future event evidence.
