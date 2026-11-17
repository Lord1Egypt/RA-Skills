# LINE OA Chat: UI selector notes

Why the send flow targets what it targets. The implementation is
`scripts/send_line_oa_chat.py` — the only one. This file explains the reasoning
behind its selectors so they can be repaired when LINE changes the UI, and does
not restate the algorithm.

## Choosing the page

Select the page whose URL begins with `https://chat.line.biz/`, and require
exactly one such page. More than one is ambiguous — two tabs can hold two
different conversations, and picking either is a guess about where a message
lands. Zero means the session is not authenticated or the browser is elsewhere.

## Searching for a recipient

The chat-list search is the sidebar input labelled `搜尋`.

**Match the placeholder exactly.** Playwright's placeholder matching is
substring-based by default, and LINE has an unrelated `輸入搜尋內容` field that a
loose match also hits. `get_by_placeholder("搜尋", exact=True)` selects the chat
list search and nothing else.

## Selecting the result

Take the anchor that contains the matching `<mark>`, not a text match on the
recipient name.

Two distinct reasons:

- **Name collisions reach the wrong element.** `get_by_text(recipient,
  exact=True)` can match the signed-in account menu rather than the chat result
  when the names coincide. The account menu is not a conversation.
- **A hidden label is not a missing result.** On a narrow layout the sidebar
  hides the chat label, so the matching text has no bounding box — but its
  containing chat-list `<a>` is still present and clickable. Treating the hidden
  label as "not found" turns a responsive layout into a false negative. Locate
  the anchor from the `<mark>` instead.

## Confirming the conversation loaded

Check that the message composer is visible and prior conversation content is
present before typing. A click that has been dispatched is not a conversation
that has rendered.

## The composer

The composer lives inside a custom element. `page.locator("textarea-ex")
.locator("textarea")` pierces the shadow DOM to the real editable element.

A placeholder-based lookup matches both the `textarea-ex` host and its internal
`textarea`, and filling the host does not fill the field. Chain the locators so
the target is unambiguous.

Submit with `input[type="submit"][value="傳送"]`.

## Verifying the send

A successful click is not evidence that a message was sent. Two conditions
together are:

1. the composer cleared, and
2. the exact text appears in the active transcript.

Prefer checking the recent transcript tail over a page-wide text match. A
page-wide match can be satisfied by an identical message sent earlier, which
would confirm a send that did not happen.

**If verification fails, do not retry.** LINE may have accepted the message
already; a retry risks sending twice. Inspect the browser first.
