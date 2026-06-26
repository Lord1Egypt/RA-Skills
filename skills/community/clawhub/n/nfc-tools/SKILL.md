---
name: nfc-tools
description: NFC tag discovery, inspection, and cautious write workflows using libnfc/nfc-utils; trigger when the user asks to read tags, inspect NDEF payloads, write or update NFC data, or automate tag batches with a PN532/ACR122 reader.
---

# NFC tools

## Quick start
1. Validate that `libnfc`/`nfc-utils` is installed, the reader is powered, and the OS has udev rules or similar permissions (see README).
2. Run `scripts/check-nfc.sh` to confirm the CLI tools are on `PATH` and `nfc-list --help` responds before touching any hardware.
3. When the workspace reports hardware missing, follow the offline planning steps in `references/fallback.md`.

## UID privacy
- Redact tag UIDs and identifiers in user-visible prose and logs by default (e.g., replace with `<REDACTED UID>` or `[UID REDACTED]`) so sensitive tag metadata does not leak.
- Reveal the full UID only when the operation explicitly requires it (debugging, pairing details, or an explicit user request), and note the operational reason for unmasking if it is stored.

## Discovery
- Run `nfc-list` or `nfc-poll` to enumerate connected readers and capture `UID`, `Manufacturer`, and `Firmware` strings; use `nfc-list --verbose` only when you need to inspect driver options.
- Keep tags awake by issuing `nfc-poll` once per interaction window; capture signal strength (`RSSI`) and technology (`ISO14443A/B`, `MIFARE Classic`, etc.) before further commands.
- Use `nfc-taginfo -v` or `nfc-taginfo -t` to surface `NDEF`/`MIFARE` block layout, sector keys, and tag capacity without modifying the tag.

## Reading a tag
1. Choose the reader connection string from `nfc-list` output (e.g., `pn532_uart:/dev/ttyACM0`) and set `LIBNFC_DEVICE` if multiple readers exist.
2. Use `nfc-ndefcat --list` for NDEF tags, `nfc-mfultralight r 0 64 dump.ul` for Ultralight blocks, or `nfc-mfclassic r a dump.mfd` for MIFARE Classic sectors (supply the correct key file or default key bundle).
3. Always export a binary/hex dump before proposing edits so the user can refer to the exact pre-write state; include the dump path in your reasoning and mention its layout when answering the request.

## Writing a tag (safety-critical)
1. Confirm the tag UID, target reader, and exact block(s)/records that will be overwritten. Ask the user to reply with `CONFIRM NFC WRITE` (uppercase and exact) before initiating any write.
2. Create a validated payload file (e.g., `payload.ndef`, `payload.ul`, `payload.mfd`) and, when feasible, preview it with `ndef-tool dump payload.ndef` or `xxd` to avoid surprises.
3. For Ultralight tags, write with `nfc-mfultralight w 0 payload.ul`; for MIFARE Classic, use `nfc-mfclassic w a payload.mfd` followed by `nfc-mfclassic c a payload.mfd` if only certain blocks change. When writing NDEF content, prefer to generate the final TLV blob with `ndef-tool` (libndef) or an equivalent helper before feeding it to a writer command so the record size/CRC stay intact.
4. After writing, re-run the appropriate read command (`nfc-ndefcat`, `nfc-mfultralight`, or `nfc-mfclassic`) to verify the payload matches the desired file before declaring success.
5. Never invent tag writes; each request must include the explicit confirmation in step 1 before running a destructive command.


## Erasing, formatting, or resetting a tag (safety-critical)
1. When an operation will erase, reformat, or reset the tag (e.g., `ndef-tool format`, `nfc-mfclassic wipe`, sector reformat, or block resets), document the desired empty or reinitialized state and the commands that will enforce it.
2. Ask the user to reply with `CONFIRM NFC FORMAT` (uppercase and exact) before running any such command; treat this as a second gate in addition to `CONFIRM NFC WRITE` and do not proceed without both confirmations if the workflow also rewrites the tag.
3. Execute the confirmed erase/format command with the validated payload or zeroing steps and monitor the CLI output for success flags or errors.
4. Re-run the appropriate read command (`nfc-ndefcat`, `nfc-mfultralight`, `nfc-mfclassic`, or `nfc-taginfo`) to prove the tag is blank or reset as requested before reporting completion.

## When hardware is missing
- Refer to `references/fallback.md` to plan tag contents, preview binary dumps, and surface manual conversion steps (e.g., building `ndef-tool` data from templates) so a human can run the write once the NFC reader becomes available.
- Document the missing hardware state, mention which reader/device was expected, and set expectations for when the physical NFC reader can be reconnected.

## Resources
- `scripts/check-nfc.sh`: sanity-check script that validates the presence of `nfc-list`, `nfc-poll`, and `nfc-taginfo` before any workflow.
- `references/fallback.md`: offline planning guide for tag payload design when hardware or drivers are unavailable.
