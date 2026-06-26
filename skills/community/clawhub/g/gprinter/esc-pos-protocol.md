# ESC/POS Protocol Reference — GP-C200V

Complete reference for ESC/POS commands used with the GP-C200V receipt printer.

## Protocol Basics

- **Transport**: Raw TCP on port 9100 (no encryption)
- **Byte order**: Little-endian for multi-byte values
- **Character encoding**: GBK for Chinese text (NOT UTF-8, NOT GB2312)
- **Paper width**: 80mm thermal paper, 384 pixels printable width

## Command Structure

ESC/POS commands use 2-3 byte prefixes followed by data:

```
ESC  = 0x1B  (27)
GS   = 0x1D  (29)
DLE  = 0x10  (16)
LF   = 0x0A  (10)
```

## Printer Control

| Name | Hex | Description |
|------|-----|-------------|
| `ESC @` | `1B 40` | Initialize printer — resets all settings to defaults |
| `ESC ! n` | `1B 21 n` | Character size (see below) |
| `ESC a n` | `1B 61 n` | Text alignment: 0=left, 1=center, 2=right |
| `ESC d n` | `1B 64 n` | Print and feed n lines |
| `ESC J n` | `1B 4A n` | Print and feed n dots (1 ≤ n ≤ 255) |
| `ESC i` | `1B 69` | Full cut (paper) |
| `ESC m` | `1B 6D` | Partial cut (if supported) |
| `LF` | `0A` | Print current line and feed |
| `CR` | `0D` | Carriage return (usually paired with LF) |

### Character Size (ESC ! n)

| Value | Size |
|-------|------|
| `0x00` | Normal (1x1) |
| `0x01` | Double width (2x1) |
| `0x10` | Double height (1x2) |
| `0x11` | Double both (2x2) |

### Text Formatting

| Command | Hex | Description |
|---------|-----|-------------|
| `ESC E n` | `1B 45 n` | Bold: n=0 off, n=1 on |
| `ESC - n` | `1B 2D n` | Underline: n=0 off, n=1 on |
| `ESC { n` | `1B 7B n` | Upside-down: n=0 off, n=1 on |

## Barcode (GS k)

### Setup

| Command | Hex | Description |
|---------|-----|-------------|
| `GS h n` | `1D 68 n` | Barcode height (dots), default 162 |
| `GS w n` | `1D 77 n` | Barcode width, 2-6 (default 3) |

### Print Barcode

```
GS k TYPE LEN DATA
1D 6B TYPE LEN d1 d2 ... dn
```

| TYPE | Hex | Standard | Data Format |
|------|-----|----------|-------------|
| UPC-A | 0x41 | UPC-A | 11-12 digits |
| UPC-E | 0x42 | UPC-E | 6-11 digits |
| EAN13 | 0x43 | EAN-13 | 12-13 digits |
| EAN8 | 0x44 | EAN-8 | 7-8 digits |
| CODE39 | 0x45 | Code 39 | ASCII + `$%*+-./` |
| ITF | 0x46 | Interleaved 2/5 | Even digits only |
| CODABAR | 0x47 | Codabar | `0-9 $+-./:` |
| CODE93 | 0x48 | Code 93 | Full ASCII |
| CODE128 | 0x49 | Code 128 | Full ASCII |

### Example: CODE128 Barcode

```javascript
const data = 'GP-12345';
const cmd = [];
cmd.push(0x1B, 0x40);       // Init
cmd.push(0x1D, 0x68, 80);   // Height: 80 dots
cmd.push(0x1D, 0x77, 3);    // Width: 3
cmd.push(0x1D, 0x6B, 0x49, data.length); // Type + length
for (const c of data) cmd.push(c.charCodeAt(0));
cmd.push(0x0A);             // Print
```

## QR Code (GS ( k)

QR codes require a sequence of 4 sub-commands:

| Step | Command | Hex | Description |
|------|---------|-----|-------------|
| 1 | `GS ( k 3 0 1 E n` | `1D 28 6B 03 00 31 45 n` | Error correction level |
| 2 | `GS ( k 3 0 1 C n` | `1D 28 6B 03 00 31 43 n` | Module size (1-15) |
| 3 | `GS ( k pL pH 1 P 0 d...` | `1D 28 6B pL pH 31 50 30 d...` | Store data |
| 4 | `GS ( k 3 0 1 Q 0` | `1D 28 6B 03 00 31 51 30` | Print QR |

### Error Correction Levels

| n | Level | Recovery |
|---|-------|----------|
| 48 (0x30) | L | 7% |
| 49 (0x31) | M | 15% |
| 50 (0x32) | Q | 25% |
| 51 (0x33) | H | 30% |

### Example: QR Code

```javascript
const content = 'https://example.com';
const dataBytes = GBK.encode(content);
const len = dataBytes.length + 3;

const cmd = [];
cmd.push(0x1B, 0x40); // Init
// Error correction M
cmd.push(0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x45, 49);
// Module size 6
cmd.push(0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x43, 6);
// Data
cmd.push(0x1D, 0x28, 0x6B, len & 0xFF, (len >> 8) & 0xFF, 0x31, 0x50, 0x30);
cmd.push(...dataBytes);
// Print
cmd.push(0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x51, 0x30);
cmd.push(0x0A);
```

## Bitmap Image (GS v 0)

Prints a raster bitmap image.

```
GS v 0 m xL xH yL yH DATA
1D 76 30 00 xL xH yL yH d1 d2 ... dn
```

| Field | Description |
|-------|-------------|
| m | 0 = normal, 1 = double width, 2 = double height, 3 = both |
| xL | Width in bytes (low byte) |
| xH | Width in bytes (high byte) |
| yL | Height in dots (low byte) |
| yH | Height in dots (high byte) |
| DATA | 1-bit per pixel, MSB first, row-major |

### Image Conversion

```javascript
function imageToBitmap(pixels, width, height, threshold = 128) {
  const bytesPerRow = Math.ceil(width / 8);
  const bitmapData = [];

  for (let y = 0; y < height; y++) {
    for (let byteIndex = 0; byteIndex < bytesPerRow; byteIndex++) {
      let byte = 0;
      for (let bit = 0; bit < 8; bit++) {
        const x = byteIndex * 8 + bit;
        if (x < width) {
          const gray = pixels[y * width + x];
          if (gray < threshold) byte |= (1 << (7 - bit));
        }
      }
      bitmapData.push(byte);
    }
  }
  return { bitmapData, bytesPerRow };
}
```

### Building the Command

```javascript
const { bitmapData, bytesPerRow } = imageToBitmap(grayPixels, 384, 200);
const cmd = [];
cmd.push(0x1B, 0x40); // Init
cmd.push(0x1B, 0x61, 1); // Center
cmd.push(0x1D, 0x76, 0x30, 0x00); // GS v 0 mode=0
cmd.push(bytesPerRow & 0xFF, (bytesPerRow >> 8) & 0xFF);
cmd.push(200 & 0xFF, (200 >> 8) & 0xFF);
cmd.push(...bitmapData);
cmd.push(0x1B, 0x4A, 0xFF); // Feed
cmd.push(0x1B, 0x69);       // Cut
```

## Real-time Status (DLE EOT)

| Command | Hex | Description |
|---------|-----|-------------|
| `DLE EOT 1` | `10 04 01` | Printer status |
| `DLE EOT 2` | `10 04 02` | Offline status |
| `DLE EOT 3` | `10 04 03` | Error status |
| `DLE EOT 4` | `10 04 04` | Paper sensor status |

Note: The printer must support real-time status for these to return data.

## Buzzer (ESC B)

```
ESC B n t
1B 42 n t
```

| Field | Description |
|-------|-------------|
| n | Number of beeps (1-9) |
| t | Beep duration (1-9) |

## Character Encoding

### Chinese Text

**ALWAYS use GBK encoding.** The built-in `encodeToGb2312` mapping is incomplete and will produce garbled output for many CJK characters.

```javascript
// Correct
const bytes = Buffer.from('中文文本', 'gbk');

// Or with GBK library in browser
const bytes = GBK.encode('中文文本');
```

### Full-width Character Detection

CJK characters take 2x the width of ASCII characters:

```javascript
function isFullWidth(char) {
  const code = char.charCodeAt(0);
  return code >= 0x1100 && code <= 0x115F ||  // Hangul Jamo
         code >= 0x2E80 && code <= 0x9FFF ||  // CJK Radicals
         code >= 0xAC00 && code <= 0xD7A3 ||  // Hangul Syllables
         code >= 0xF900 && code <= 0xFAFF ||  // CJK Compat Ideographs
         code >= 0xFE30 && code <= 0xFE6F ||  // CJK Compat Forms
         code >= 0xFF00 && code <= 0xFFEF;    // Half/Fullwidth Forms
}
```

## Paper Feed Before Cut

**Critical**: The GP-C200V cuts immediately on `ESC i`. If text is still at the cutter position, it will cut through the text.

```
ESC J 0xFF  →  Feed 255 dots (~10-11 lines)
ESC i       →  Cut
```

Always feed at least 0x80 (128 dots, ~5 lines) before cutting. Use 0xFF (255 dots) for safety with double-size text.

## Common Gotchas

1. **UTF-8 → Garbled**: Printer expects GBK, not UTF-8
2. **GB2312 → Missing chars**: The mapping table is incomplete; use full GBK
3. **Cut too early**: Feed paper before cutting, or text gets sliced
4. **Empty lines ignored**: Must send explicit `0x0A` for each line break
5. **Barcode data**: Some barcode types require checksum digits (EAN, UPC)
6. **QR max size**: ~1800 bytes of data for mode M (Level 40, Error M)
