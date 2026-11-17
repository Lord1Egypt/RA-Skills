# Sharing HTML Artifacts

Use Pagedrop when the user asks for a hosted preview, shareable link, cross-device review, or annotation feedback for a finished HTML artifact. Pagedrop serves a GitHub Gist through `pagedrop.ai`; it is an optional delivery path, not a replacement for local validation or the local file.

## Guardrails

- Validate the local artifact before publishing it.
- Publish only after the user asks for a hosted/shareable link or explicitly confirms third-party sharing.
- Never publish credentials, secrets, tokens, private customer data, personal data, or internal-only material. Review source excerpts, comments, metadata, embedded data, and hidden UI before sharing.
- Treat secret Gists as unlisted, not private. Anyone with the Pagedrop or Gist URL can view the content.
- Keep the local `.html` file as the canonical artifact.
- Do not claim an expiry. A Pagedrop URL persists until its backing Gist is deleted.

## Prerequisite

Pagedrop uses the authenticated GitHub CLI to create and update Gists:

```bash
gh auth status
```

If `gh` is missing or unauthenticated, return the local artifact and report that hosted sharing needs an authenticated GitHub CLI.

## Publish

From the skill directory, run the bundled publisher:

```bash
node scripts/pagedrop-publish.mjs /absolute/path/to/artifact.html
```

The publisher:

1. Validates the HTML file and GitHub CLI authentication.
2. Creates a secret Gist with `#pagedrop` in its description.
3. Prints the default `https://pagedrop.ai/g/USER/GIST_ID` URL.

Use `--description "Quarterly review"` to set the Gist description. The publisher appends `#pagedrop` when it is missing.

## Routes

- `/g/USER/GIST_ID` is the default route. It serves the latest Gist revision and injects Pagedrop's revision and annotation UI.
- `/g/USER/GIST_ID/SHA` pins a specific Gist revision. Use it when reviewers must see immutable content.
- `/h/USER/GIST_ID` is the large-file fallback when `/g/` returns `503` or cannot inject the page. Publish with `--route h`; the HTML must already include this before `</body>`:

```html
<script src="https://pagedrop.ai/pagedrop.js"></script>
```

- `/s/TOKEN` is a controlled share link created from the Share button while signed in to Pagedrop. It can control annotation and revision visibility.

Creating `/s/` links through `POST https://pagedrop.ai/api/share` requires a Pagedrop-authenticated session. A GitHub CLI token is not a Pagedrop API token. Do not call that API from an unattended agent unless the user explicitly provides an approved Pagedrop authentication mechanism.

Do not invent custom domains, password protection, or TTL controls; those belonged to a different service.

## Iterate

Update the existing Gist instead of creating a new drop:

```bash
gh gist view GIST_ID --files
gh gist edit GIST_ID -f GIST_FILENAME /absolute/path/to/artifact.html
```

GitHub preserves the revision history. The latest `/g/` route may cache for about five minutes; revision-pinned routes are immutable.

## Verify And Return

Open the returned URL in a real browser when possible. Confirm the title, primary content, and one meaningful interaction. For `/g/`, also confirm the Pagedrop revision or annotation UI appears. For `/h/`, confirm the bootstrap script loads that UI.

Return:

- the `pagedrop.ai` URL
- the Gist URL or ID
- the route used and whether it is revision-pinned
- the local artifact path
- any hosted-preview verification gap

Service references: `https://pagedrop.ai` and `https://github.com/Martian-Engineering/pagedrop`.
