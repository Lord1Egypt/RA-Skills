# Troubleshooting

## `obclip` Is Not Recognized

Cause:
- The npm package is not installed globally.
- The shell has not picked up the global npm bin path yet.

Fix:
- Run `npm install -g @harris7/obclip`
- Open a new shell and retry
- Or use `npx @harris7/obclip ...`
- Or use `node .\dist\cli.cjs ...` inside the source repo

## Saved Note Is Incomplete

Cause:
- The page was still hydrating when extraction ran.
- The site mounted content after initial load.

Fix:
1. Add `--settle-ms 3000` or `--settle-ms 5000`
2. If still incomplete, add `--wait-selector "<css>"`
3. Use a content selector such as `article`, `main`, or a stable post container

## Page Shows Login Or Signup Shell

Cause:
- The browser session has no login state.

Fix:
1. Use `--browser-profile "<dir>"`
2. Use `--headful` the first time if manual login is needed
3. Reuse the same dedicated profile on later runs

Delay alone does not solve authentication problems.

## Browser Path Fails

Cause:
- `--browser-executable` points to a missing file or a non-Chromium browser path.

Fix:
- Verify the file exists
- Quote the full Windows path
- Retry with the known good Chromium path

## Profile Directory Is Busy

Cause:
- Another browser process is already using the same profile directory.

Fix:
- Close the other browser process
- Or use a different dedicated profile directory

## Output Directory Behaves Like A File Path

Cause:
- `--output` points to a non-existent path without a trailing slash

Fix:
- Use an existing directory
- Or make directory intent explicit: `--output "D:\data\Clippings\"`

## Chromium Prompts For Network Access

Cause:
- The OS or security software is asking whether the browser binary may access the network

Fix:
- Allow the browser once in the OS dialog
- Prefer a fixed Chromium executable path instead of relying on temporary bundled browser locations
