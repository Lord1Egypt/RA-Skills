# Security & Privacy

This document describes how the Mobilerun skill handles sensitive data, credentials, and device permissions.

## Data Handling

- **Screenshots and UI tree data** may contain personal information visible on the user's screen (messages, emails, photos, etc.). This data is fetched on-demand for the current task and is not stored, cached, or transmitted beyond the API response.
- All API calls go to `https://api.mobilerun.ai/v1` over HTTPS.
- The skill does not collect analytics, telemetry, or usage data.

## Credentials

- The `MOBILERUN_API_KEY` (prefixed `dr_sk_`) is provided by the host platform (OpenClaw) and used solely for authenticating API requests.
- The key is never displayed, logged, or included in user-facing output.
- Keys can be created, rotated, or revoked at any time from https://cloud.mobilerun.ai/api-keys.

## Device Permissions

The Droidrun Portal app on the user's Android device requires the **Accessibility Service** permission. This is the same system API used by screen readers and assistive technology. It allows the skill to:

- Read the UI element tree (text, buttons, layout)
- Simulate taps, swipes, and text input
- Identify the foreground app

The user grants this permission explicitly during setup and can revoke it at any time in Android Settings.

## APK Installation

The Portal app is distributed as an APK from GitHub Releases (open source: https://github.com/droidrun/droidrun-portal). Because it is installed outside the Play Store, Android shows a standard sideloading warning. This is expected behavior for any app not distributed through the Play Store.

## Input Handling

API endpoint paths in the documentation use placeholders like `{deviceId}`, `{packageName}`, and `{task_id}`. These are UUIDs or Android package name strings returned by the API itself (e.g. from `GET /devices`). They are not user-supplied free text. When constructing curl commands, always use values obtained directly from prior API responses — never interpolate raw user input into URLs or shell commands.

## Scope of Control

The skill can only interact with devices that the user has explicitly connected to their Mobilerun account. It cannot access devices belonging to other users, and all actions require a valid authenticated API key.
