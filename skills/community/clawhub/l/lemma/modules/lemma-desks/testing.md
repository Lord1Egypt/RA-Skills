# Desk Testing Guide

Use this guide when you need to test a React desk locally or inside a remote Lemma workspace.

## Goal

Verify all of the following before upload:

- the desk loads with the correct API, auth, and pod env values
- injected-token auth works through `localStorage["lemma_token"]`
- the UI looks correct in a real browser
- important operator actions succeed
- console and network behavior are understood
- the final bundle uploads and the desk becomes `READY`



This keeps the desk on the latest published SDK while still importing from `lemma-sdk`.

## Runtime Env

The desk needs:

```bash
VITE_LEMMA_API_URL=<api-url>
VITE_LEMMA_AUTH_URL=<auth-url>
VITE_LEMMA_POD_ID=<pod-id>
```

Remote workspace example:

```bash
VITE_LEMMA_API_URL=${LEMMA_BASE_URL}
VITE_LEMMA_AUTH_URL=${LEMMA_AUTH_URL}
VITE_LEMMA_POD_ID=${LEMMA_POD_ID}
LEMMA_DESK_DEV_PORT=5173
```

## Start The Desk

Local or workspace:

```bash
npm run dev
npm run preview:url
```

Use the agent-local URL inside the container:

```text
http://127.0.0.1:5173/
```

In a remote workspace, also capture the public preview URL from `npm run preview:url`.

## Playwright CLI Setup

The workspace image already includes `playwright-cli`, Chromium, and the wrapper path described in `lemma-workspace` skill.

Open the desk:

```bash
playwright-cli open http://127.0.0.1:5173/ --browser=chromium
playwright-cli snapshot
```

If the wrapper script is available, prefer that wrapper over a global install.

## Injected Token Auth

Use token-mode browser auth only through local storage.

Set the token:

```bash
playwright-cli localstorage-set lemma_token "$LEMMA_TOKEN"
playwright-cli reload
playwright-cli snapshot
```

Equivalent manual browser snippet:

```js
localStorage.setItem("lemma_token", "<access-token>");
window.location.reload();
```

Do not put testing tokens in query params, source files, or screenshots shared outside the workspace.

## First Checks After Reload

Always inspect these first:

1. page snapshot
2. screenshot
3. console output
4. network requests

Useful commands:

```bash
playwright-cli snapshot
playwright-cli screenshot
playwright-cli console
playwright-cli network
```

## What To Verify

Visual checks:

- the app renders the expected desk, not the auth wall
- headers, empty states, cards, and forms are laid out correctly
- no obvious broken spacing, overlapping elements, or clipped content

Auth checks:

- `/users/me` succeeds after token injection
- repeated 401s mean the token is missing, expired, or not being read
- if the browser stays on the sign-in screen, inspect `/users/me` first before debugging the React app

Form checks:

- fill the primary operator form
- click the main action button
- confirm a success banner or updated UI state
- re-snapshot after the write

Workflow checks:

- click at least one workflow launcher
- confirm a run id appears and the state changes to something like `WAITING`, `RUNNING`, or `COMPLETED`

## Recommended Smoke Flow

This is the shortest high-value desk smoke path:

1. open the desk
2. snapshot the unauthenticated page
3. inject `lemma_token`
4. reload and snapshot again
5. take a screenshot of the authenticated UI
6. fill and submit one direct-write form
7. verify a success banner and refreshed list state
8. click one workflow launcher
9. verify a run id and status appears
10. check console and network before upload

## Remote Workspace Notes

- Use the workspace image's built-in `playwright-cli`.
- `workspace_server/Dockerfile` already installs Chromium and wires the `playwright-cli` wrapper.
- If you want the user to watch the browser live, follow `lemma-workspace` and expose the preview or noVNC URL.
- Inside the workspace container, keep using `http://127.0.0.1:<port>`.
- For user-visible previews, use the public workspace port URL from `npm run preview:url`.

## Failure Patterns To Recognize

Auth wall with 401s:

- missing or expired `lemma_token`
- wrong API or auth URL
- token injected before the wrong page or wrong origin

Auth wall with CORS/network failures:

- wrong tested origin for the backend
- missing same-origin proxy when the backend only allows specific origins
- use the public workspace URL if that is the allowed origin

Desk loads but actions fail:

- wrong `VITE_LEMMA_POD_ID`
- missing backend resources in the pod
- workflow or function names do not match the provisioned names

## Upload Verification

Before upload:

```bash
npm run build
npm run bundle
lemma desk bundle-upload <desk-name> --pod-id <pod-id> --source-dir . --html-file ./bundle.html
lemma desk get <desk-name> --pod-id <pod-id>
```

Success looks like:

- bundle upload returns success
- desk status becomes `READY`

