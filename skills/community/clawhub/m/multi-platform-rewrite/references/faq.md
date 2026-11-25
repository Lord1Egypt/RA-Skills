# When a run goes wrong

## A task stays queued

Keep polling that task with `beatra.tasks.get`. Versions that already finished stay deliverable.

## The create response never came back

Retry the identical payload and the same `client_request_id`. If the task id disappeared, list tasks and match the frozen request first.

## The price on the card looks wrong

Read `beatra.models.list` or `beatra.social.tools.get` again and show the number it just returned.

## One cover lost the claim

One `beatra.images.edit` on that cover restores the exact claim and keeps the ratio. Own card, own id. The other platforms stay as they are.
