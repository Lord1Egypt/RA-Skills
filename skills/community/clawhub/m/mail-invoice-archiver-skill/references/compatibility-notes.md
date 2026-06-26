# Compatibility Notes

## 2026-04 Attachment format preference lesson

A real-world invoice mail may include the same invoice in several attachment forms at once, for example:

- OFD
- PDF
- ZIP
- sometimes image attachments

For user-facing archive output, OFD is often the least convenient option because many users do not routinely open, print, or inspect OFD files. In this workflow, canonical file selection should prefer formats the user can open immediately.

Recommended priority for canonical saved artifacts:

1. image (`png` / `jpg` / `jpeg`)
2. `pdf`
3. `xml`
4. `ofd`
5. `zip`

Practical rule:

- If PDF or image exists for the same invoice, do not save OFD as the default canonical artifact.
- Keep OFD or ZIP only as fallback or supplemental material when no more accessible format exists.
- This preference is about user-facing archive convenience, not about extraction confidence alone.

## Real-World Findings

- 126 mailbox IMAP worked with a Keychain-stored authorization code.
- Direct `imap.126.com` TLS handshakes were unreliable in the tested terminal environment.
- `appleimap.126.com` succeeded and allowed a real login with the 126 account.
- After login, selecting `INBOX` failed with `Unsafe Login` unless the client sent a realistic IMAP `ID` first.
- Using an Apple Mail style client `ID` allowed `SELECT INBOX` and normal mailbox reads.
- During the live test, the mailbox sent a new-device login alert, which confirms the login path was real.
- The runtime now implements `system` auth with macOS Keychain on macOS and Windows Credential Manager on Windows.
- The Windows Credential Manager path is implemented and covered by unit tests, but it was not live-tested in this macOS session.
- 163 is implemented as a sibling provider to 126 because the Netease help flow and IMAP guidance are the same family, but 163 was not live-tested in this workspace.
- Gmail is implemented as a separate provider with `imap.gmail.com` and an app-password secret model. That is the phase-one path for personal Gmail accounts; some Google Workspace tenants may still require OAuth or admin-side IMAP controls.

## Pitfalls

- Do not assume `imap.126.com` is the best production host for every environment.
- Do not assume macOS Keychain is the only acceptable secret store. The runtime now supports `system`, `env`, `config`, and `prompt` modes, and `system` now covers Windows Credential Manager too.
- Do not assume all providers use the same secret type. 126 and 163 use authorization codes; Gmail requires an app password in the current runtime.
- Do not assume all Gmail accounts behave the same. Personal Gmail can use app passwords, while some Google Workspace environments may still block this path without admin changes or OAuth.
- Do not assume every provider needs the same IMAP handshake. The Apple Mail style `ID` is intentionally scoped to the Netease providers.
- Do not rely on file names for invoice identity. Re-sent messages and alternate formats can represent the same invoice.
- Do not assume OCR is always available. The runtime falls back to XML, PDF text, subject, and body extraction when OCR tools are missing.
- Do not auto-merge invoices when the invoice number matches but the amount differs; flag them as conflicts.
- Do not treat chat delivery as SMTP. The runtime only prepares the zip and summary; the agent layer must attach the zip in the current chat.
- Do not assume PDF text extraction preserves visual order. In real invoice PDFs, `价税合计（大写）` and `（小写）` labels may be separated from the actual amounts by many unrelated lines after text extraction.
- Do not grab the first `¥` amount in a PDF invoice region. In the tested restaurant invoices, the first `¥` was the tax base amount, the second was tax amount, and the last was the final invoice total.
- Do not treat buyer and seller labels as a simple nearest-neighbor regex problem. In tested PDFs, `名称： 名称：` collapsed into one line, and the actual buyer/seller values appeared several lines later in fixed positional order.
- Do not let month summary logic depend only on current-month rows with `status='saved'`. A current-month artifact may be marked `duplicate` against an older canonical row from a previous run, and the summary still needs to count that business key for the current month.

## 2026-04 Repair Notes

During live repair on 2026-04 invoice data, the following issues were reproduced and fixed:

1. Homebrew Python 3.14 loaded `pyexpat` against `/usr/lib/libexpat.1.dylib`, which broke XML parsing. The working recovery path was: repoint the library, then re-sign the touched Python artifacts so macOS would load them again.
2. PDF vendor extraction initially captured the buyer (`广东天习律师事务所`) instead of the seller. The reliable fix was to switch from plain regex matching to layout-aware extraction that understands the buyer/seller block after `名称： 名称：`.
3. PDF amount extraction initially captured tax-base amounts such as `232.08` and `198.11` because the generic fallback matched the first `¥` in a reordered text block. The fix was to add a dedicated PDF total extractor that inspects the invoice total area first.
4. Month report totals became unstable when current-month rows were duplicates of older canonical rows created in previous runs. The fix was to summarize by current-month `business_key`, selecting the best representative row from the current month instead of requiring a current-month `saved` row.
5. One invoice family required an explicit business rule choice for total amount interpretation. When the user confirms a reporting rule such as using `价税合计 = 900.00`, persist that interpretation consistently in extraction and reporting.
