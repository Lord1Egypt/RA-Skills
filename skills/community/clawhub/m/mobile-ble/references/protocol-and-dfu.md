# Protocol design and firmware updates

Load this when designing, implementing or reviewing the byte-level protocol on top of GATT, or a firmware
update (DFU) flow. The firmware specification is authoritative. Everything below marked "example" is a
pattern to compare against, not a format to assume. If the device document does not define a field,
timing or opcode, the agent asks instead of inventing one.

## Example frame layout

```text
Example only. Real layout comes from the firmware document.

 0        1        2        3 .. 3+len-1     3+len   3+len+1
+--------+--------+--------+---------------+--------+--------+
| opcode |  seq   |  len   |   payload     |  crc16 (LE)     |
+--------+--------+--------+---------------+--------+--------+
crc16 = CRC-16/IBM-3740 (CCITT-FALSE) over bytes 0 .. 3+len-1
```

Questions the firmware document must answer before code is written:

| Topic | Question |
|---|---|
| Byte order | Little or big endian for every multi-byte field? |
| Length | What does `len` count? Maximum value? Is a zero-length payload legal? |
| CRC | Which variant (poly, init, reflect, xorout)? Over which bytes? Byte order of the CRC itself? |
| Sequence | Width, wrap-around, per direction or shared, reset on reconnect? |
| Chunking | Is a frame allowed to span several ATT packets? How is the first and last chunk marked? |
| Acknowledgement | ACK per frame, per window, or none? What does a NACK carry? |
| Timing | Response timeout per opcode, inter-packet gap, maximum time to apply a command |
| Errors | Error codes and which ones are retryable |
| Versioning | How the app learns the protocol version and what it does on mismatch |

## Chunking above the MTU

- Payload per ATT packet is `ATT_MTU - 3`. Default ATT_MTU is 23, so the safe minimum is 20 bytes.
- A single attribute value is at most 512 bytes (Core spec, ATT). Anything larger must be framed by the
  application.
- Put a header on each chunk (example: frame id, chunk index, last-chunk flag) or a length prefix on the
  frame so the receiver knows when it is complete.
- Reassembly limits: maximum frame size, maximum chunks, and a timeout after which a partial frame is
  dropped. Without limits a broken or hostile device can exhaust memory.

```kotlin
class Reassembler(private val maxFrame: Int, private val timeout: Duration, private val clock: () -> Long) {
    private var buffer = ByteArrayOutputStream()
    private var expected = -1
    private var startedAt = 0L

    // Example chunk header: [0] = total length low byte, [1] = high byte on the first chunk only.
    fun accept(chunk: ByteArray, first: Boolean): ByteArray? {
        if (first) {
            if (chunk.size < 2) return reset()
            expected = (chunk[0].toInt() and 0xFF) or ((chunk[1].toInt() and 0xFF) shl 8)
            if (expected == 0 || expected > maxFrame) return reset()
            buffer = ByteArrayOutputStream(expected)
            buffer.write(chunk, 2, chunk.size - 2)
            startedAt = clock()
        } else {
            if (expected < 0 || clock() - startedAt > timeout.inWholeMilliseconds) return reset()
            if (buffer.size() + chunk.size > expected) return reset()
            buffer.write(chunk)
        }
        if (buffer.size() < expected) return null
        return buffer.toByteArray().also { reset() }
    }

    private fun reset(): ByteArray? { expected = -1; buffer = ByteArrayOutputStream(); return null }
}
```

## Never trust device input

- Bounds-check every length, count and offset against both the received size and a fixed maximum.
- Mask bytes before arithmetic: `b.toInt() and 0xFF` in Kotlin, `Int(b)` from `UInt8` in Swift,
  `b & 0xFF` in Dart.
- Reject unknown opcodes and versions; count rejects in a metric without logging payloads.
- Strings from the device (names, versions) are untrusted: limit length, validate the charset, and never
  build file paths, SQL or HTML from them.
- Fuzz the parser in unit tests: random bytes, truncated frames, maximum lengths, wrong CRCs.

```swift
// Safe reads from Data without traps
extension Data {
    func u8(at i: Int) -> UInt8? { indices.contains(startIndex + i) ? self[startIndex + i] : nil }
    func u16le(at i: Int) -> UInt16? {
        guard let lo = u8(at: i), let hi = u8(at: i + 1) else { return nil }
        return UInt16(lo) | (UInt16(hi) << 8)
    }
}
```

Note: `Data` slices keep the parent's indices. Always offset from `startIndex`, as above.

## CRC implementations

CRC detects accidental corruption. It does not detect a deliberate change: anyone can recompute it.
Use a signature (firmware images) or a MAC or AEAD (commands, data) for authenticity.

Verify any implementation with the standard check input `"123456789"` (ASCII):

| Variant | Parameters | Check value |
|---|---|---|
| CRC-16/IBM-3740 (CCITT-FALSE) | poly 0x1021, init 0xFFFF, no reflection, xorout 0 | `0x29B1` |
| CRC-16/XMODEM | poly 0x1021, init 0x0000, no reflection, xorout 0 | `0x31C3` |
| CRC-16/KERMIT | poly 0x1021, init 0x0000, reflected, xorout 0 | `0x2189` |
| CRC-16/MODBUS | poly 0x8005, init 0xFFFF, reflected, xorout 0 | `0x4B37` |
| CRC-32 (ISO-HDLC, zlib) | poly 0x04C11DB7, init 0xFFFFFFFF, reflected, xorout 0xFFFFFFFF | `0xCBF43926` |

Kotlin, CRC-16/IBM-3740:

```kotlin
fun crc16Ccitt(data: ByteArray, from: Int = 0, to: Int = data.size): Int {
    var crc = 0xFFFF
    for (i in from until to) {
        crc = crc xor ((data[i].toInt() and 0xFF) shl 8)
        repeat(8) { crc = if (crc and 0x8000 != 0) (crc shl 1) xor 0x1021 else crc shl 1 }
        crc = crc and 0xFFFF
    }
    return crc
}

// CRC-32: use the JDK
fun crc32(data: ByteArray): Long = java.util.zip.CRC32().apply { update(data) }.value

@Test fun crcCheckValues() {
    val input = "123456789".toByteArray(Charsets.US_ASCII)
    assertEquals(0x29B1, crc16Ccitt(input))
    assertEquals(0xCBF43926L, crc32(input))
}
```

Swift:

```swift
func crc16Ccitt(_ data: some Sequence<UInt8>) -> UInt16 {
    var crc: UInt16 = 0xFFFF
    for byte in data {
        crc ^= UInt16(byte) << 8
        for _ in 0..<8 { crc = (crc & 0x8000) != 0 ? (crc << 1) ^ 0x1021 : crc << 1 }
    }
    return crc
}
// XCTAssertEqual(crc16Ccitt(Array("123456789".utf8)), 0x29B1)
```

Dart:

```dart
int crc16Ccitt(List<int> data) {
  var crc = 0xFFFF;
  for (final b in data) {
    crc ^= (b & 0xFF) << 8;
    for (var i = 0; i < 8; i++) {
      crc = (crc & 0x8000) != 0 ? ((crc << 1) ^ 0x1021) & 0xFFFF : (crc << 1) & 0xFFFF;
    }
  }
  return crc;
}
// expect(crc16Ccitt(ascii.encode('123456789')), 0x29B1);
```

## Sequence numbers, timeouts and retries

- Each command carries a sequence number; the response echoes it. Drop responses whose number does not
  match the outstanding command.
- Duplicates (same number twice) are acknowledged again but not applied again. Commands that change state
  should be idempotent or carry the sequence number so the device can deduplicate.
- Wrap-around: compare with modular arithmetic, never with `<` on raw values.
- Per-operation policy, written down with the firmware team:

| Operation | Example timeout | Retries | On final failure |
|---|---|---|---|
| Read device info | 5 s | 2 | Disconnect, reconnect |
| Command with ACK | 3 s | 3, same sequence number | Report error to user |
| DFU chunk | 2 s | 5, resend from last confirmed offset | Pause, resume later |
| Service discovery | 20 s | 1 | Close, reconnect |

Values in this table are examples. Use the timings from the firmware document.

## Security of the link

- Pairing: LE Secure Connections (Bluetooth 4.2+, P-256 ECDH). Only Numeric Comparison, Passkey Entry and
  Out of Band give protection against man-in-the-middle during pairing. Just Works protects against
  passive eavesdropping only (with LE Secure Connections) and offers no MITM protection.
- If the product cannot use an authenticated pairing method, protect the application layer: a
  per-device key provisioned at the factory or during onboarding, authenticated encryption (for example
  AES-GCM) with a counter or nonce that never repeats, and replay protection on the device.
- Never ship a shared key in the app binary. Store per-device secrets in the Android Keystore or iOS Keychain.
- Characteristics that change device state require an encrypted link (permission level on the device side).
- Logs: opcode, length, sequence number and status only. No keys, tokens, passwords, raw payloads, or
  unredacted MAC addresses and serial numbers in production logs or analytics.

## Firmware update (DFU) safety

Goal: no sequence of user actions, radio drops or battery events leaves the device unbootable.

Device side (confirm with the firmware team; the app cannot compensate for missing pieces):
- Bootloader verifies the image signature with a public key in protected storage before it boots it.
- Dual-bank or swap-based update; the current image stays bootable until the new one is confirmed.
- Rollback if the new image does not confirm itself after boot (watchdog or test-boot flag).
- Anti-rollback: version counter so older, vulnerable images are rejected.
- Resume: device reports the last confirmed offset so the app can continue after a drop.

App side:
1. Download over HTTPS from your backend; verify the hash or signature metadata of the download.
2. Check compatibility: hardware revision, current version, bootloader version, minimum app version.
3. Preconditions: phone battery or charging, device battery above the firmware team's threshold,
   Bluetooth on, user consent, screen-on or foreground service for the transfer on Android.
4. Request high connection priority (Android) and the largest MTU; chunk from the negotiated size.
5. Send chunks with flow control and per-chunk ACK or windowed ACK; persist the confirmed offset.
6. On disconnect: back off, reconnect, query the offset, resume. Never restart from zero without asking
   the device.
7. After the device reboots: reconnect, rediscover services (the GATT table may change), read the version,
   and confirm success only when it matches the release.
8. Report progress and errors to the user in plain words. Do not let the user start a second update in
   parallel.

```kotlin
sealed interface DfuState {
    data object Checking : DfuState
    data class Blocked(val reason: BlockReason) : DfuState      // low battery, incompatible, no consent
    data class Transferring(val sent: Long, val total: Long) : DfuState
    data class Paused(val confirmedOffset: Long) : DfuState
    data object Validating : DfuState
    data object Rebooting : DfuState
    data class Done(val version: String) : DfuState
    data class Failed(val error: DfuError, val deviceBootable: Boolean) : DfuState
}
```

Vendor DFU libraries (for example the SoC vendor's DFU or SMP/MCUmgr client) implement the transfer. The
safety properties above still have to be checked in the device design; a library cannot add signature
verification to a bootloader that lacks it.

## Protocol checklist

- [ ] Firmware protocol document identified, with version, and every field traced to it
- [ ] Byte order, length semantics, maximum lengths and CRC variant written down
- [ ] Frames larger than `MTU - 3` chunked with a defined first and last marker or length prefix
- [ ] Reassembly has a maximum size, a chunk limit and a timeout
- [ ] Every length and offset bounds-checked; parser fuzzed
- [ ] CRC verified with the standard check value in a unit test
- [ ] Sequence numbers match responses to requests; duplicates not applied twice; wrap-around handled
- [ ] Timeout and retry policy per operation agreed with the firmware team
- [ ] Authenticity: signatures for firmware, MAC or AEAD for sensitive commands; CRC not used as security
- [ ] Pairing method and link security level documented; no shared keys in the app
- [ ] DFU: signed images verified by the bootloader, dual bank or rollback, anti-rollback, resume, battery check
- [ ] Logs contain no keys, payloads or unredacted identifiers
