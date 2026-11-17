# Haven Media — video use terms

The `video` and `video_sound` endpoints are served under upstream
model licences whose use restrictions pass through to you. **Paying for one of
those requests is the act of accepting them** — there is nothing to sign and
nothing to send back, so they are published where you can read them first:

- in the free catalog: `GET /x402/api/v1/catalog | jq .terms`
- in the 402 quote body, and in the quote's `PAYMENT-REQUIRED` header under
  `accepts[0].extra` (`termsUrl`, `termsAcceptance`, `useRestrictions`) — so
  an automated client sees them without parsing prose
- in `agents.txt`

The full, controlling text is at `terms.url`. The summary includes, among
others: no unlawful use, nothing involving minors, no impersonation or
deepfakes of real people without consent, **no using the output to train,
improve, or fine-tune any model**, and — the two that bind you onward:

- **Disclose that the output is machine-generated wherever you publish it.**
  Delivered MP4s normally carry an AI-generated disclosure inside the file
  (`moov/udta/meta/ilst/©cmt`, readable with
  `ffprobe -show_entries format_tags=comment`). **Do not strip it.** The
  response tells you whether this specific file has it:
  `X-Ai-Disclosure-Embedded: true|false`, alongside `X-Ai-Generated` and
  `X-Use-Terms`. When it is `false` the container couldn't be rewritten
  safely — the disclosure obligation still applies, you just have to carry it
  yourself.
- **If you redistribute the output, pass these restrictions on as enforceable
  terms and give your recipients the same notice.**

The music and image kinds are not covered by this block and their quotes
carry no `terms`. Don't infer coverage from this list either way — each
quote states it: a covered kind's quote carries `terms`, an uncovered one's
does not.
