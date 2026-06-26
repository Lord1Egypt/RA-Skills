# Image Compress - Technical Reference

## Format Specifications

### Input Formats

| Format | Extension(s) | Alpha Channel | Notes |
|--------|-------------|---------------|-------|
| JPEG | `.jpg`, `.jpeg` | No | Lossy, EXIF support |
| PNG | `.png` | Yes | Lossless, transparency |
| WebP | `.webp` | Yes | Google format, lossy/lossless |
| GIF | `.gif` | Yes | Limited to 256 colors |
| BMP | `.bmp` | No | Uncompressed bitmap |
| HEIC/HEIF | `.heic`, `.heif` | Yes | Apple format, requires system support |

### Output Formats

| Format | Quality Range | Alpha Support | Best For |
|--------|--------------|---------------|----------|
| JPEG | 1-100 | No | Photos, web images |
| PNG | 1-9 (compression) | Yes | Screenshots, graphics with text |
| WebP | 1-100 | Yes | Modern web, best compression |
| AVIF | 1-100 | Yes | Next-gen format, smallest size |

## Sharp API Reference

### Basic Usage

```javascript
import sharp from 'sharp';

// Resize and compress
await sharp(inputPath)
  .resize({ width: 1920, fit: 'inside' })
  .jpeg({ quality: 85 })
  .toFile(outputPath);
```

### Format-Specific Options

#### JPEG

```javascript
.jpeg({
  quality: 85,           // 1-100
  progressive: false,    // Progressive JPEG
  mozjpeg: false         // Use mozjpeg encoder
})
```

#### PNG

```javascript
.png({
  compressionLevel: 6,   // 0-9
  adaptiveFiltering: true,
  palette: false
})
```

#### WebP

```javascript
.webp({
  quality: 80,           // 1-100
  alphaQuality: 100,     // Alpha channel quality
  lossless: false,
  nearLossless: false
})
```

#### AVIF

```javascript
.avif({
  quality: 50,           // 1-100
  alphaQuality: 100,
  lossless: false,
  speed: 4               // 0-10 (slower=better)
})
```

### Handling Transparency

When converting PNG with alpha to JPEG:

```javascript
// White background
sharp(input).flatten({
  background: { r: 255, g: 255, b: 255, alpha: 1 }
});

// Custom color
sharp(input).flatten({
  background: { r: 0, g: 0, b: 0, alpha: 1 }  // Black
});
```

## Performance Benchmarks

### Compression Speed (M4 Mac)

| Image Size | Format | Time (ms) |
|------------|--------|-----------|
| 1 MP | JPEG | ~50ms |
| 1 MP | PNG | ~80ms |
| 1 MP | WebP | ~100ms |
| 1 MP | AVIF | ~200ms |
| 12 MP | JPEG | ~300ms |
| 12 MP | PNG | ~500ms |

### Compression Ratios (85% quality)

| Source | JPEG | WebP | AVIF |
|--------|------|------|------|
| Photo (JPG) | 100% | 70% | 50% |
| Screenshot (PNG) | 80% | 60% | 45% |
| Graphics (PNG) | 90% | 65% | 50% |

## Error Codes

| Error | Cause | Solution |
|-------|-------|----------|
| `VIPS__ERROR_NO_MEMORY` | Out of memory | Reduce image size or close other apps |
| `VIPS__ERROR_TEMPORARY` | Temp directory full | Clean up `/tmp` or set TMPDIR |
| `Input buffer has corrupt header` | Corrupt file | Verify file integrity |
| `Unsupported input format` | Unknown format | Check file extension and content |

## Platform-Specific Notes

### macOS

- HEIC support built-in (Apple Silicon)
- Default temp: `/tmp`

### Windows

- Requires VC++ Redistributable
- Long path support may need registry fix

### Linux

- Install dependencies: `sudo apt-get install libvips-dev`
- May need `libimagequant-dev` for PNG

## Configuration Schema

```json
{
  "outputDir": "~/Downloads/compressed-images",
  "defaultQuality": 0.85,
  "defaultFormat": "original",
  "preserveMetadata": false,
  "maxWidth": null,
  "maxHeight": null,
  "backgroundColor": "#FFFFFF"
}
```
