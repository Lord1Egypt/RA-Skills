# When a run goes wrong

## A task stays queued

Keep polling that task with `beatra.tasks.get`. The checklist is already usable. The note waits on the read.

## The create response never came back

Retry the identical payload and the same `client_request_id`. If the task id disappeared, list tasks and match the frozen request first.

## The price on the card looks wrong

Read `beatra.models.list` or `beatra.social.tools.get` again and show the number it just returned.

## The repair drifted off the file

Stop. Deliver the original file and the note. A second repair is a new card and a new id, still an edit of the original, not a new picture from text.
