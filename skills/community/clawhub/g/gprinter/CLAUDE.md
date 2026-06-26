# GP-C200V Printer Skill

佳博 (Gainscha) GP-C200V ESC/POS 热敏打印机打印技能。

## Printer Info

| Item | Value |
|------|-------|
| Model | GP-C200V |
| Type | ESC/POS 热敏收据打印机 |
| Paper | 80mm 热敏纸 |
| Connection | WiFi (TCP port 9100) |
| Print Width | 384px (80mm 满宽) |
| Chars/Line | 标准 42 / 双倍 21 |

## Quick Start

### Architecture

```
Node.js script (TCP direct) → WiFi (port 9100) → GP-C200V
```

Print commands are sent directly to the printer via TCP — no HTTP bridge needed.
Use `print-standalone.js` for CLI printing or `print-helper.js` as a reusable library.

### Basic Print (Node.js)

```javascript
// Using print-helper.js
const GPPrinter = require('./print-helper');
const printer = new GPPrinter({ host: '192.168.50.189' });
await printer.connect();
const cmd = printer.buildTextCommand('Hello 世界', { cut: true });
await printer.sendRaw(cmd);
await printer.disconnect();

// Or using print-standalone.js from CLI:
//   node print-standalone.js --text "Hello 世界" --cut
```

```javascript
// Low-level: build raw ESC/POS byte array
const cmd = [];
cmd.push(0x1B, 0x40);             // ESC @ — init
cmd.push(0x1B, 0x61, 1);          // ESC a 1 — center
// ... add text/barcode/QR/image bytes ...
cmd.push(0x1B, 0x4A, 0xFF);       // ESC J 0xFF — feed 255 dots
cmd.push(0x1B, 0x69);             // ESC i — cut

// Send via direct TCP (no server.js needed)
const net = require('net');
const socket = net.connect(9100, '192.168.50.189');
socket.on('connect', () => socket.write(Buffer.from(cmd), () => socket.end()));
```

### Optional: HTTP Bridge (Browser context)

An HTTP bridge (`server.js`) exists in the sibling `h5-usb-serial/` project to enable **browser-based** printing via `fetch()`. This is **not needed** for any Node.js printing — use direct TCP instead. Do NOT start or reference `server.js` from this skill unless specifically working with the browser test page.

## Key Rules

### 1. Always use GBK encoding for Chinese text

Use `iconv-lite` with `'gbk'` encoding — the old `encodeToGb2312` mapping table is incomplete.

```javascript
// CORRECT: Use iconv-lite GBK encoding
const iconv = require('iconv-lite');
const gbkBytes = Array.from(iconv.encode(text, 'gbk'));
for (const b of gbkBytes) cmd.push(b);

// WRONG: Uses incomplete GB2312 mapping (from old h5-usb-serial/lib)
gpESC.createNew().setText(text);  // DON'T — will produce garbled output
```

### 2. Always feed paper before cutting

The GP-C200V cuts immediately on `ESC i`. If the text hasn't fully cleared the cutter position, it will cut through text.

```javascript
// Feed 255 dots (~10-11 lines) before cutting
cmd.push(0x1B, 0x4A, 0xFF);  // ESC J 0xFF
cmd.push(0x1B, 0x69);        // ESC i
```

### 3. Use raw byte arrays, not gpESC objects

The `gpESC.createNew()` pattern uses `setText()` which relies on the broken `encodeToGb2312` mapping. Build command arrays directly:

```javascript
// CORRECT: Direct byte array + iconv-lite GBK
const iconv = require('iconv-lite');
const cmd = [0x1B, 0x40, 0x1B, 0x61, 1];
cmd.push(...Array.from(iconv.encode('中文文本', 'gbk')));
cmd.push(0x0A);
cmd.push(0x1B, 0x4A, 0xFF);
cmd.push(0x1B, 0x69);
```

### 4. Text auto-wrap for long content

80mm paper fits 42 characters (standard) or 21 characters (double size) per line. Long lines should wrap automatically:

```javascript
const CHARS_PER_LINE = { normal: 42, double: 21 };
function isFullWidth(char) {
  const code = char.charCodeAt(0);
  return code >= 0x1100 && code <= 0x115F || code >= 0x2E80 && code <= 0x9FFF ||
         code >= 0xAC00 && code <= 0xD7A3 || code >= 0xF900 && code <= 0xFAFF ||
         code >= 0xFE30 && code <= 0xFE6F || code >= 0xFF00 && code <= 0xFFEF;
}
function wrapLine(line, maxChars) {
  const result = []; let current = ''; let width = 0;
  for (const char of line) {
    const charWidth = isFullWidth(char) ? 2 : 1;
    if (width + charWidth > maxChars && current.length > 0) {
      result.push(current); current = ''; width = 0;
    }
    current += char; width += charWidth;
  }
  if (current.length > 0) result.push(current);
  return result.length > 0 ? result : [line];
}
```

## File Structure

```
gprinter/
├── CLAUDE.md              # Skill main doc (this file)
├── SKILL.md               # Usage quick reference
├── esc-pos-protocol.md    # ESC/POS protocol reference
├── print-helper.js        # Reusable Node.js print library
├── print-standalone.js    # CLI print tool
├── package.json           # Dependencies (iconv-lite for GBK)
└── package-lock.json
```

## Common ESC/POS Commands

| Command | Bytes | Description |
|---------|-------|-------------|
| `ESC @` | `1B 40` | Initialize printer |
| `ESC a n` | `1B 61 n` | Alignment: 0=left, 1=center, 2=right |
| `ESC ! n` | `1B 21 n` | Character size: 0=normal, 0x11=2x2 |
| `ESC d n` | `1B 64 n` | Feed n lines |
| `ESC J n` | `1B 4A n` | Feed n dots (max 255) |
| `ESC i` | `1B 69` | Full cut |
| `LF` | `0A` | Print and line feed |
| `GS h n` | `1D 68 n` | Barcode height |
| `GS w n` | `1D 77 n` | Barcode width |
| `GS k 73 n d...` | `1D 6B 49 n d...` | CODE128 barcode |
| `GS ( k ...` | `1D 28 6B ...` | QR code commands |
| `GS v 0 m xL xH yL yH d...` | `1D 76 30 00 xL xH yL yH d...` | Raster bitmap |

## Image Printing

```
1. Resize image to targetWidth (384 = 80mm full width)
2. Convert to grayscale → binary threshold
3. Build bitmap: row-major, 8 pixels per byte, MSB first
4. Send via GS v 0 command
```

Full image printing implementation is in `gp-c200v.html` → `printImage()`.

## Barcode Types (ESC/POS)

| Type Code | Standard |
|-----------|----------|
| 65 (0x41) | UPC-A |
| 66 (0x42) | UPC-E |
| 67 (0x43) | EAN13 |
| 68 (0x44) | EAN8 |
| 69 (0x45) | CODE39 |
| 70 (0x46) | ITF |
| 71 (0x47) | CODABAR |
| 72 (0x48) | CODE93 |
| 73 (0x49) | CODE128 |

## QR Code Commands

```
Set error correction: 1D 28 6B 03 00 31 45 n
  n=48(L) 49(M) 50(Q) 51(H)

Set module size:      1D 28 6B 03 00 31 43 n
  n=1..15

Store data:           1D 28 6B pL pH 31 50 30 d1...dn
  pL/pH = data_length + 3 (little-endian)

Print QR:             1D 28 6B 03 00 31 51 30
```

## Error Codes

| Error | Meaning |
|-------|---------|
| ECONNREFUSED | Printer IP/port incorrect |
| ETIMEDOUT | Network unreachable |
| ECONNRESET | Connection dropped |
| EPIPE | Broken pipe (printer disconnected) |
