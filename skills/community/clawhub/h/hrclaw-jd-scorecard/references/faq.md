# FAQ

## What does this skill do?

It turns a JD into a scorecard, or scores a PDF/text resume against that scorecard.

## Does it work with PDF resumes?

Yes, if text can be extracted from the PDF.
If the file is image-only, it should stop with `needs_ocr`.

## Can it output Feishu or DingTalk-friendly text?

Yes.
Use the chat templates when you want a result that can be pasted into team chat.

## What if the JD is vague?

Keep the output conservative and add short assumptions instead of guessing.

## Can it handle more than one role?

Prefer one primary role per scorecard.
Split mixed JDs when the roles are meaningfully different.

## Should it invent missing fields?

No.
Use `null`, `[]`, or a short `assumptions` note when evidence is missing.
