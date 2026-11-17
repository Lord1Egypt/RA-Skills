## Browser Behaviour

- Use `kleinanzeigen_browser_status` when diagnosing login, browser launch,
  profile, private/incognito mode, or runtime/browser mismatch issues.
- Report only sanitized effective browser settings, such as browser, binary
  location, private-window mode, and redacted profile configured-state markers.
- If publishing fails during login-state detection or browser interaction, check
  whether `usePrivateWindow` is enabled. Private/incognito windows may interfere
  with expected login or profile persistence.
- Use `kleinanzeigen_browser_check` to test proposed browser settings without
  changing the real miniclaw config.
- Only change browser configuration with `kleinanzeigen_browser_configure` after
  explicit user confirmation. Persist only supported browser choices and
  workspace or system-default profile modes; custom executables and custom
  profile directories must be edited locally outside chat.
