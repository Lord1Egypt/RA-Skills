# HAR capture checklist

## Goal
Capture one clean, successful manual run of the exact site action you want to replay.

## Before capture
- Confirm the user is already logged in normally.
- Confirm the manual action works at least once.
- Open a fresh browser tab if practical.
- Open DevTools -> Network.
- Turn **Preserve log** on.
- Turn **Disable cache** on.
- Clear old network entries.
- If the site is noisy, filter by `fetch`, `xhr`, `graphql`, `upload`, `media`, or the target domain.

## During capture
- Perform only the target action.
- Avoid unrelated navigation.
- Wait for visible success.
- If the action has several stages, wait until the last one finishes.

## Export
- Export the HAR immediately after the successful run.
- Keep the original HAR untouched.
- If analysis needs experimentation, work from a copy.

## What good capture looks like
You should be able to see the full chain, for example:
- upload init
- upload append/chunk send
- finalize
- poll/status
- final mutation/create request
- optional readback/confirmation request

## What to avoid
- huge mixed logs from many tabs
- captures where the action failed
- captures taken before login was complete
- HAR files missing the final successful request
