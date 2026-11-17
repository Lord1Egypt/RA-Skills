# Publishing via browser (fallback)

Fallback for accounts without an X developer app; the default path is
PUBLISH-API.md. Uses OpenClaw's managed browser profile, which must already be
logged into X, so it requires a machine with a display server or headless
Chromium. You only ever compose and submit a single post. Nothing else on
x.com.

This mode publishes a single text post only — the media-first package
(media attachment plus the link reply) is API-mode only. If the pending
draft's `format` is `media+reply` or `text+reply`: post only the body, with
the reply's link folded back in at the end of the body text, re-verified
against the length check in DRAFTING.md before typing it. No media is
attached, no reply is posted, and the report to the user says the package
was degraded to a single link-bearing post because `postVia` is `browser`.

1. `browser status` — if the browser isn't ready, report and stop.
2. Open `https://x.com/compose/post` in the managed profile.
3. Take a snapshot. If you see a login form, "Sign in", or the compose box is
   missing: stop, alert the user that the X session expired. Do not log in.
4. Click the post text area and type the approved draft text exactly. Do not
   let autocomplete popups change the text; snapshot again and verify the box
   contains exactly the draft.
5. Click the "Post" button.
6. Wait for the confirmation toast or the compose dialog to close, then open
   the user's own profile page and verify the new post is at the top.
7. Capture the tweet's permalink (click the post's timestamp or copy its
   `/status/<id>` href from the snapshot) and a screenshot for the record.
   Screenshot only the compose dialog or the post itself, never the full
   timeline/notifications (a logged-in session can expose DMs). Store
   screenshots under `postflight-state/` and share them only with the authorized user in
   the approval channel.
8. Return the permalink. If verification fails at step 6-7, tell the user the
   post state is uncertain and include the screenshot; do not post again.
