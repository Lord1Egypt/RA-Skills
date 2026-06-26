# API Setup

## Access model

Meta Ads access is account-specific.
Each agent that uses this skill should have its own token, account ID, and permissions.

## Typical credentials

- `META_ADS_API_KEY` or equivalent bearer token
- account ID in `act_<id>` format when calling the Graph API

## Permissions

Common permissions include:
- `ads_read` for reporting and insights
- `ads_management` for live changes
- lead access permissions for form lead retrieval where applicable

## Credential handling

Do not store tokens in tracked files or workspace notes.
Use the approved secure credential workflow for the environment and expose tokens to the runtime through approved environment injection only.

## Connection basics

Before doing meaningful work, confirm:
- token is present
- token has the right scopes
- correct ad account is selected
- expected endpoints respond without permission errors

## Important notes

- Meta Graph API versions change over time. Keep examples current when updating the skill.
- Read access and write access are not the same thing.
- Some insights or lead endpoints may fail without the right combination of ad account, page, app, or business permissions.
