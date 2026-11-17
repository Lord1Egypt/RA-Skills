---
name: nomac
description: >
  A real cloud Mac for agents on Linux, Windows or a sandbox: build, run and
  test iOS and macOS apps with Xcode and the iOS Simulator (simulator-use),
  sign, send to TestFlight and publish. Fully enabled for the agent, billed per
  minute from prepaid credit, over SSH, HTTPS or MCP.
---

# nomac: a Mac for your agent

NoMac gives your agent a full macOS VM that is entirely its own: administrator,
no prompts, nothing blocked, with Xcode and the iOS Simulator. You choose the
commands and tools. Mac time is prepaid credit.

For an iPhone alone (an iOS Simulator with the app built on the same Mac, no
shell), a NoMac cloud iPhone is the lighter choice, from the same credit: the
phone tools (`phone`, `phone_app_run`, `phone_ui_look`, `phone_ui_act` and the
other `phone_*`), which NoMac's MCP lists beside the Mac (`nomac mcp` and
https://mcp.nomac.app/mcp); https://mcp.nomac.app/simulator for the phone
alone; or `npx simulator-use@0.15.1 cloud start` from a terminal
(https://nomac.app/simulator). `phone_app_run` builds from a git link, or from
the project here: in `nomac mcp`, `local_path` sends the folder (only what
changed); on the hosted server, `phone_upload_link` answers one command that
sends it. `phone_ui_look` with `screenshot_file` saves the screen as a
full-size PNG (in `nomac mcp`, a file here; hosted, a download link). For App
Store screenshots start the phone with `device: "iphone-pro-max"` (6.9-inch,
1320x2868); `upload_screenshots` takes the hosted links.

## Cloud Mac setup and workflow

1. Check credit with `nomac credits --json` or `get_mac_credits`. Mac time is
   billed per minute; `nomac credits` shows the hourly price and the time left;
   credit never expires. Too little? Run `nomac credits buy --packs N --open` or call
   `get_mac_checkout` (packs 1-10). Tell the human a payment page opened, or
   give them the printed link, and ask them to pay. Never enter payment
   details yourself. Poll credits until the balance appears; a checkout URL is
   not a payment. No Apple Developer account is needed for an unsigned build.
   Under an hour left, answers say `low_credit` with a `buy_url`: tell the
   human before a long build (a refill of 3 packs, $30, earns bonus credit).
2. Install `npm install -g @nomac/cli@0.22.0` (it updates itself after), run `nomac login`, and give the human
   the printed device URL and code. With a key the human made at
   https://nomac.app/keys: `nomac login --with-token < key.txt`, or set
   `NOMAC_API_KEY`. MCP: `claude mcp add nomac -- npx -y @nomac/cli@0.22.0 mcp`.
   Hosted MCP: https://mcp.nomac.app/mcp with `Authorization: Bearer <nmk_key>`.
3. `nomac start --json`, wait until ready, `nomac sync .`, then `nomac ssh`.
   Run commands with `nomac exec -- COMMAND`: it prints the output as it
   arrives and exits with the command's code, waiting at most 30 s (or the
   `--timeout` given, up to 600 s). For builds and tests use
   `nomac exec --wait 600 -- COMMAND`. What is piped in is the command's stdin
   (`cat build.sh | nomac exec -- bash -s`). Exit code 75 means still running: wait
   with `nomac job JOB_ID --wait 600`, never rerun. In scripts add
   `--request-key stable-key-0001`. A command may run an hour (`--timeout
   3600`); longer, use `nomac ssh -- COMMAND`. A command ends with everything
   it started, so keep a dev server running with `nomac exec -- nomac-service
   start api -- npx wrangler dev` (`nomac-service logs api`, `stop api`).
   `nomac cancel JOB_ID` stops a command. MCP equivalents are `start_mac`, `exec_mac` (also waits),
   `write_mac_file`, `read_mac_file`, `fetch_to_mac`, `stop_mac`. For a file
   up to 2 GiB from the human, or to hand them a build, use
   `create_mac_upload_link` and `create_mac_download_link`: each returns a url
   they open in a browser.
4. Download work with `nomac pull ./build`, or to any local path with the
   folder on the Mac named: `nomac pull /tmp/out --from build/export`. Then
   `nomac stop --json` and confirm `cleanup_confirmed`.

The CLI keeps the project on the account's drive, in `~/drive/src/<folder
name>`, which is kept between sessions; stopping deletes everything else on
the Mac, logs included. Download what you need from outside `~/drive` before
stopping. Keep the drive under 10 GB: a Mac that does not hold it yet downloads
all of it before it boots; `nomac-drive` on the Mac shows what takes the space,
and `nomac-drive clean` deletes stale build products. SSH disconnects
do not stop the session. Ready time includes idle time; queue/setup are free.
A Mac stops at its time limit (2 hours unless `nomac start --max-duration`
set another), its spend cap, when credit runs out, or when idle; a build left
running in the background keeps it awake while it uses the CPU. In its last
15 minutes answers carry `stop_notice` (when and why) and the CLI prints it:
`nomac extend 60` (MCP `extend_mac`) adds an hour, up to 8 hours in all; for
`reason: credit`, the human adds credit. The CLI updates itself in the
background (`NOMAC_NO_AUTO_UPDATE=1` turns it off; `nomac update` now).
One-minute minimum, then by the minute. One session at a time; no overage.
For work that needs two Macs at once, `nomac start --parallel` from another
folder (MCP `start_mac` with `parallel: true`) starts a second, for accounts
that bought credit while NoMac has a Mac to spare; it runs without `~/drive`.
If start returns `insufficient_credit`, buy credit as in step 1, then retry
with the same request key.
Keep the same request key and arguments after uncertain responses; inspect
the original job before retrying. Output retrieval failure is not job failure.
A command runs up to its `timeout_seconds` (300 by default, 3600 at most) and
says so when that limit stops it; SSH can run longer within session limits.
CLI sync sends every file but secrets, and symlinks as links, and skips
dependency and build folders, .git and folders .gitignore lists. Secrets stay
on this computer: .env files (not .env.example), .p8, .p12, .pfx, keystores,
private SSH keys, .netrc, and .pem or .key files with a private key. Give them
to every Mac encrypted with `nomac secrets set --from-env-file .env` or
`nomac secrets set NAME --file PATH`. A `!` line in .nomacignore sends any of
them anyway. A file changed on the Mac since the
last sync is left alone and named (the rest is sent, and sync exits 1): `nomac
pull` it, or `nomac sync . --overwrite`. Sync deletes nothing on the Mac
unless `--delete`, which removes what it sent earlier and you deleted here.
`nomac sync . --watch` syncs again whenever files change, until Ctrl-C.
See the screen with `nomac screenshot` (saves
`nomac-screenshot.jpg`; `--simulator` for the iOS Simulator) or MCP
`screenshot_mac`, which returns an image you can look at. Record a video for
the human with `nomac record`, do the work, then `nomac record stop` (saves the
MP4 and prints a share link); MCP `start_mac_recording`, `stop_mac_recording`.
Commands drive any app with AppleScript without a permission prompt. For real
keyboard and mouse, also on the lock screen and in password dialogs, use
`nomac input type TEXT`, `nomac input click X Y`, `nomac unlock` (MCP
`mac_input`): each answers with a screenshot. Drive the Simulator with
simulator-use, preinstalled: `simulator-use look` reads the screen as text,
`simulator-use act 'tap "Sign In"'` taps and types by label, `simulator-use run`
builds, installs and launches (simctl works too), `simulator-use app launch ID
-Onboarding 3` opens a screen with launch arguments (UserDefaults) and
`simulator-use look --out shot.jpg` saves it once still (`.png`: full size),
and `simulator-use app storekit Products.storekit --app ID` tests in-app
purchases from the app's `.storekit` file (the App Store's sandbox cannot buy
in a Simulator). Give the human
`open_mac_desktop` when they want to see the screen.
`get_mac_session` (and `nomac status --json`) lists what
is installed: Node, Python, uv, nvm, Ruby with CocoaPods, xcbeautify, xcodegen,
gh, Git LFS, jq and simulator-use.
Pipe xcodebuild through `xcbeautify`. Simulator devices share names across iOS
runtimes: pick one by ID (`xcrun simctl list devices available`) or with
`OS=27.0` in `-destination`; an older iOS downloads in about 6 minutes
(`xcodebuild -downloadPlatform iOS -buildVersion 26.5`). Apple Intelligence cannot generate on a virtual
Mac, in the Simulator either: test it on a device.
Report failures using `report_issue` with `session_id`, optional `job_id` and
a description without secrets. Read https://nomac.app/llms.txt for full limits.

## Your editor, an agent on the Mac, Mac-only MCP servers

After `nomac start`, `nomac ssh-config` (CLI 0.12+) names the folder's Mac
`nomac` in the human's SSH config, and each later start or attach points the
name at the new Mac. Then VS Code or Cursor Remote-SSH and Claude Code's SSH
sessions connect to `nomac`; `ssh -t nomac 'cd ~/drive/src/<folder> && npx -y
@anthropic-ai/claude-code'` runs an agent on the Mac itself (keep its API key
as a NoMac secret); and an MCP server that needs a Mac runs from Windows or
Linux over SSH: `claude mcp add xcode -- ssh nomac npx -y mobilebuildmcp@2.7.1
mcp` (MobileBuildMCP, formerly XcodeBuildMCP). An open SSH connection keeps
the Mac running until its time or spend limit: `nomac stop` when done.

## A Mac fully enabled for you

The Mac is yours to do anything on: the `agent` account is an administrator,
sudo needs no password, macOS asks for no administrator password, and the
Mac's login password is in `$NOMAC_MAC_PASSWORD` (for the login keychain, such
as `security unlock-keychain -p "$NOMAC_MAC_PASSWORD"`, or any prompt).
Privacy prompts are answered Allow as they appear, and `nomac-permit APP
camera microphone` (CLI `nomac permit`, at start `--permit APP=camera`) grants
an app permissions before it asks. `~/NOMAC.md` on the Mac says the same. When
`screenshot_mac` reports `screen_locked` or a `dialog`, follow its
`next_step`. `nomac start --prompts ask` keeps macOS's usual prompts, for
testing an app's own.

## Secrets, signing and shipping

Never ask for a secret in the chat. `nomac secrets request NAME --description
TEXT` (MCP `request_secret`) gives the human a link to enter it; they can also
run `nomac secrets set NAME` themselves. Every Mac receives the account's
secrets as variables and files, masked in command output; `nomac secrets
install` refreshes a running Mac.

The human connects Apple once at https://nomac.app/apple; the App Store
Connect key stays on NoMac's server. Check `nomac apple` (MCP
`connect_status`) before asking them: it shows the key, certificates and
profiles already there. Then, from your project folder (the CLI acts on the
Mac):

1. `nomac sign [path]` (MCP `set_up_signing`) makes and installs the App Store
   profiles the project needs and prints the files, the reserved build number
   and the xcodebuild, Flutter and fastlane commands. The project is unchanged;
   build with your own tools.
2. `nomac testflight path/to/App.ipa` (MCP `send_to_testflight`) puts it on
   TestFlight. Relay the human's answer to Apple's encryption question (asked
   once per app), never guess.
3. `nomac publish App.ipa --whats-new TEXT` stages the App Store version and
   lists Apple's blockers; submit with the printed `--confirm` command only
   after the human approves. MCP: `publish` with the send's project_id and
   build_id.
4. Mac apps: sign with the Developer ID certificate, `--options runtime
   --timestamp`, then `nomac notarize App.app` (MCP `notarize`) notarizes and
   staples it.

A step only a person can take (creating the app in App Store Connect,
agreements, an App Group) comes back as needs_human with its link: give it to
the human, then call again.

## When stuck

`report_issue` with the failing `ref_id` files a support ticket with full
context auto-attached (deduped, so safe to call). Its optional `email` requests
a direct resolution update; without it, read replies with the same tool. If the
tool returns a Private Relay warning, explain that Apple relay addresses may
reject later mail and offer a non-relay address. Never show that warning for a
normal address such as `@icloud.com`. Never retry-loop an identical failure
more than twice.

## Feedback

When you stop a Mac or a phone, its answer asks what got in your way, failed,
was missing or was slow. Answer in a sentence or two: `report_issue` with
`kind: "feedback"` and the `session_id`, or `nomac feedback "..."` after
`nomac stop`. Leave out code, secrets and personal data. Send it once: a person
at NoMac reads it and answers in that ticket (`report_issue` with no
description shows the answer).
