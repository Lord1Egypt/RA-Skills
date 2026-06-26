# NFC hardware fallback guide

When the NFC reader or driver stack is missing, keep moving forward by preparing everything that can be verified without touching a tag.

## Design the payload offline
1. Pick the target tag type (Ultralight, Classic, DESFire, etc.) and model its capacity (e.g., Ultralight: 64 bytes, Classic 1K: 16 sectors of 4 blocks).
2. Author the desired NDEF records as a binary blob: use `ndef-tool new --text "My URL" payload.ndef` or manually assemble the TLV sections with `python -c 'print(bytes([...]))'` and capture the hex with `xxd -p payload.ndef`.
3. For sector/block-based tags, map each block to its final content in a table (see the sample template below). Keep the table in the repo or a user note so the writer can reproduce the exact byte offsets once hardware is back.

## Sample Classic layout template
| Sector | Block | Byte range | Purpose | Payload file |
|--------|-------|------------|---------|--------------|
| 0      | 0     | 0-15       | UID + Manufacturer data | `sector0.bin` |
| 0      | 1     | 16-31      | Application data | `sector0-b1.bin` |
| 1      | 0     | 32-47      | NDEF TLV start | `sector1-b0.bin` |
| ...    | ...   | ...        | ... | ... |

## Simulate verification
- Use `xxd payload.mfd` or `od -An -tx1 payload.ul` to show the user the exact bytes that will be written.
- If possible, run `ndef-tool dump payload.ndef` to confirm record types, MIME types, and URIs.

## Document the missing hardware
- Note which device (e.g., `pn532_uart:/dev/ttyACM0`) was expected so re-connection attempts target the right port.
- Flag the plan as "Awaiting NFC reader" in your update so the human in the loop can supply the hardware or run the final command later.
