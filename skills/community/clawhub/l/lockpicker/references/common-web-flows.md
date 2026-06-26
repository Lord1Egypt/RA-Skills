# Common web flows

## Image upload
Often simpler than video.
Common differences:
- no async processing poll, or poll may 404 harmlessly
- file size limits matter more immediately
- media category may differ from video
- image may need local downscaling or recompression

## Video upload
Often needs:
- media duration
- async finalize
- repeated status polling
- larger timeout budget

## GraphQL mutation
Watch for:
- query id in path
- same query id repeated in JSON body
- variables object nesting
- client headers that must match the browser session

## Queue workflow
Once single-item success exists:
- create manifest rows
- schedule one item at a time
- persist returned ids
- pause between groups

## Confirmation pattern
Best success signals:
- returned object id
- permalink in response
- scheduled item visible to the user
- queue row updated locally
