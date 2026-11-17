---
name: release-handoff
description: >-
  Finish an iOS release after the build is uploaded. When a build has been
  uploaded to App Store Connect by any tool (fastlane, asc, Xcode, Xcode
  Cloud, CI) and the user wants it shipped: attach the build to the version,
  clear export compliance, run the readiness sweep, fix what blocks, and
  submit for review through MetaRun. Also the way back after App Review
  rejects a version: read the verdict, fix, resubmit. Trigger phrases: "ship
  it", "submit the build", "finish the release", "send 2.4 to review", "the
  build is up", "Apple rejected it", "resubmit".
metadata:
  openclaw:
    homepage: https://metarun.dev/agents
    primaryEnv: METARUN_TOKEN
    envVars:
      - name: METARUN_TOKEN
        required: false
        description: MetaRun personal access token (Settings, MCP). Not needed after `npx metarun login`, which stores it in ~/.metarun/config.json.
    requires:
      anyBins:
        - npx
---

# Release handoff: from uploaded build to submitted release

You are completing a release through MetaRun. The build side (compile, sign,
upload) is already done by whatever tool the project uses; your job is
everything after. Only two things still need App Store Connect in a browser,
and each is named where it comes up: App Privacy and App Review's messages.

## Ground rules (read once, apply always)

- **Transport.** Use MetaRun's tools via the MCP server (`metarun` tools in
  your tool list) if connected. Otherwise use the CLI: `npx metarun run
  <tool> '<json>'`. Same tools, same behavior. If neither is set up, run
  `npx metarun login` (needs a token from metarun.dev Settings -> MCP).
- **Schemas are live, never guessed.** Before calling a tool with arguments
  you have not used in this session, fetch its input schema:
  `npx metarun tools <tool-name> --json` (or read it from the MCP listing).
  Do not invent parameter names from memory.
- **Every write is a preview/apply pair.** The preview returns a diff and a
  `confirmToken`; the apply requires that token and fails if the store
  changed in between (then: re-preview, show the user, re-apply). Never
  skip showing the user what a preview returned before applying it.
- **Resolve ids, never guess them.** Version ids come from
  `apple_list_versions`, build ids from `apple_list_builds`, review
  submission ids from `apple_list_review_submissions`. A bundle id the user
  gives you ("com.example.app") is the only id you may take on faith.

## The mission

### 1. Locate the app and the editable version

- `apple_list_apps` -> find the app by bundle id or name.
- `apple_list_versions` -> the newest versions carry state. You need the one
  editable version (states like PREPARE_FOR_SUBMISSION). Apple allows only
  ONE editable version at a time.
- REJECTED or METADATA_REJECTED (or the user says Apple rejected it)? That
  version is still the editable one: do not create another. Work through 1b
  before anything else. (DEVELOPER_REJECTED is not a verdict: the team
  withdrew the version itself.)
- No editable version? Create one: `apple_preview_create_version` ->
  confirm with the user -> `apple_apply_create_version`. Wrong version
  number on an existing draft? Renumber with `apple_preview_set_version_string`
  (never delete-and-recreate; Apple permits one draft).

### 1b. If App Review rejected it

- `apple_list_review_submissions` -> the app's submissions, newest first,
  with who sent each. The rejected one reads Unresolved Issues; pass
  `states: ["UNRESOLVED_ISSUES"]` to list only those.
- `apple_get_review_submission` (the bundle id plus that submission's id) ->
  every item with Apple's verdict, the build attached to the version now
  (after a fix, not necessarily the one Apple reviewed), `nextSteps`, and
  `appStoreConnectUrl`.
- **App Review's message is not in the API.** The reason, the cited
  guideline, the review device and OS, attachments, and replies live only in
  App Store Connect, exactly like App Privacy. Say so plainly, give the user
  `appStoreConnectUrl`, and ask them to paste the message. Never guess a
  reason or cite a guideline you have not been shown.
- Then map the message to a fix:
  - Listing text: `apple_preview_set_version_localization` (description,
    keywords, What's New) or `apple_preview_set_app_info_localization`
    (name, subtitle, privacy URL).
  - The app itself: a new build, attached through steps 2-3.
    METADATA_REJECTED means the build was not the problem; do not ask for
    one.
  - Reviewer notes or the demo account: `apple_preview_set_review_detail`.
  - Screenshots, or another rejected item (a product, an in-app event):
    find its tool with `npx metarun tools <filter>`.
  - An answer, not a change (App Review misread a feature or asked a
    question): offer to draft the reply for the user to paste into App
    Store Connect.
- Then continue from step 4; step 6 covers resubmitting.

### 2. Find the processed build

- `apple_list_builds` -> newest first, with processing state and encryption
  flags. The build you want must be state PROCESSED/VALID. If it is still
  processing, tell the user and wait or check back; do not attach an
  unprocessed build.
- If `usesNonExemptEncryption` is unset, the build sits on "Missing
  Compliance" and cannot ship: run `apple_preview_declare_build_encryption`
  (most apps using only HTTPS/standard crypto answer both questionnaire
  flags false = exempt), confirm, `apple_apply_declare_build_encryption`.
  This one is not revertible; say so when you show the preview.

### 3. Attach the build to the version

- `apple_preview_set_version_build` with the version id and build id ->
  show the diff -> `apple_apply_set_version_build` with the confirmToken.

### 4. Run the readiness sweep

- `apple_preview_submit_for_review` is the sweep: it blocks with a
  per-language checklist of everything Apple still requires. Read the result
  as a work list, not an error.
- `apple_get_listing_coverage` is the same work list as a per-language
  filled/empty map (`submissionBlockers`, plus `gaps` for the optional
  fields). Cheaper to re-read while you close gaps, and it is what confirms
  the fixes actually landed before you re-run the submit preview.
- Common blockers and their fixes:
  - Missing What's New (updates only): `apple_preview_set_version_localization`
    per language. On a FIRST release Apple has no What's New field at all;
    do not try to set it.
  - Missing privacy policy URL: `apple_preview_set_app_info_localization`.
  - Missing description/keywords/support URL per language:
    `apple_preview_set_version_localization`.
  - Another submission already waiting for or in review: withdraw it with
    `apple_preview_cancel_review_submission` (confirm with the user first;
    it withdraws a live submission) or wait for its verdict.
    `apple_list_review_submissions` shows which one it is.
- Screenshots that exist only as local files (simulator captures, a locally
  composed set): `studio_create_upload` returns a signed upload URL and a
  `curl` line; PUT the file with it, then `studio_finalize_upload` returns an
  https `imageUrl` for `apple_preview_upload_screenshot`. Never base64 a file
  into a tool argument.
- A brand-new app has no availability until it is set up: if
  `apple_get_availability` says `configured: false`, set it up with
  `apple_preview_set_territory_availability` (confirm the storefronts with
  the user). Its `saleBlockers` name storefronts Apple still will not sell
  in, such as a missing EU trader status.
- First submission only: the sweep will carry an App Privacy warning. App
  Privacy has NO App Store Connect API; it is entered once by hand in the
  browser. Do not hunt for a tool that writes it. What you can do is build
  the answers: read the app's `PrivacyInfo.xcprivacy` and every SDK's (Swift
  packages under DerivedData/<project>/SourcePackages/checkouts, CocoaPods
  under Pods) and pass them to `apple_build_privacy_answers`, which returns
  the exact data types, linked/tracking answers and purposes to enter, plus
  the inconsistencies App Review rejects. Hand the user that list and the
  App Privacy link it returns.
- Also by hand only, when they apply: EU trader status (App Information >
  App Store Regulations and Permits) and whether an iPhone/iPad app is
  offered on Apple silicon Macs and Vision Pro (Pricing and Availability).

### 5. Release options (ask, do not assume)

If the user has not said how it should release, ask once: automatic on
approval, manual, or phased. Set via `apple_preview_set_release_options` /
`apple_apply_set_release_options`. After approval, `apple_apply_manual_release`
releases a manually-held version and `apple_apply_phased_release` manages a
staged rollout.

### 6. Submit

- Re-run `apple_preview_submit_for_review` until it returns clean (warnings
  may remain; blocks may not). If it still blocks on a language you already
  fixed, `apple_get_listing_coverage` says whether the write actually landed.
- Resubmitting a rejected version is the same pair. The preview resubmits
  the submission Apple left in Unresolved Issues, since the version already
  belongs to it, and names the rejection in its warnings with the App Store
  Connect link. Make sure the user has seen it.
- Show the user exactly what will be submitted.
- `apple_apply_submit_for_review` requires the confirmToken AND
  `acknowledge: true`. The acknowledge flag is the user's explicit yes to an
  outward action: never set it without their clear go-ahead in this
  conversation.

### 7. Close the loop

`apple_list_review_submissions` shows the submission's new status (Waiting
for Review once Apple has it). Report what was submitted and remind the
user: every change you applied is in MetaRun's change history, attributed
and revertible (except the noted exceptions), and review-state changes will
show on the Releases deck.

## Beyond this mission

MetaRun's surface is much larger than this workflow: pricing across 175
territories, metadata and translation, screenshot rendering and publishing,
ASO and answer-engine visibility, reviews, TestFlight. Discover it live with
`npx metarun tools <filter>` (for example `tools pricing`, `tools aso`);
never assume a capability is missing before searching for it.
