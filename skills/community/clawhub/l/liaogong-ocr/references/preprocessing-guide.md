# Preprocessing Guide · 预处理指南

## When to Use Which Chain

### Phone Photos of Screens → `optimal_phone`
- **Problem**: Phone photos of screens suffer triple degradation (screen pixel grid → moire patterns, CMOS Bayer array → edge blur, JPEG compression → high-frequency loss)
- **Solution**: invert colors → grayscale → contrast enhance 2.5x → tesseract eng psm6
- **Result**: 87% digit accuracy. Chinese characters remain unreadable (physical limit of phone camera + compression).

### Clean Documents → No Preprocessing
- If the image is a clean scan/screenshot with white background and dark text, use tesseract directly with `--psm 3`.

### Chinese Posters / Complex Layouts → easyocr (No Preprocessing)
- easyocr's CRAFT text detector + CRNN recognizer handles complex layouts, curved text, and artistic fonts natively. Preprocessing often reduces accuracy for these cases.

### Multi-Chain Cross-Validation
- For critical data (e.g., financial numbers), run 3+ chains and take the consensus result. If `optimal_phone`, `grayscale_binary`, and `contrast_enhance` all produce the same number, reliability is significantly higher.

## Chain Reference

| Chain Name | Steps | Best For | Digit Acc. |
|-----------|-------|----------|------------|
| `optimal_phone` | invert → grayscale → contrast 2.5x | Phone photos of screens | 87% |
| `grayscale_binary` | grayscale → threshold 128 | High-contrast documents | 72% |
| `contrast_enhance` | grayscale → enhance 2.0x | Low-contrast text | 65% |
| `sharpen` | grayscale → sharpen filter | Blurry text | 55% |
| `clahe` | CLAHE equalization | Uneven lighting | 31% |
| `adaptive_binary` | adaptive threshold | Mixed lighting | 18% |

## Known Limitations

- **Phone photo Chinese OCR**: Chinese characters with 15+ strokes are reduced to 3-5 strokes after phone camera + compression. Use screenshots instead of photos for Chinese text.
- **easyocr is CPU-bound**: Without GPU, easyocr processes ~5-30 seconds per image. Use tesseract for speed-critical tasks.
- **Handwritten text**: Neither engine is optimized for handwriting. Consider PaddleOCR or TrOCR for handwriting.
