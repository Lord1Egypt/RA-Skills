# Benchmark Results · 基准测试结果

## Test Setup

- **Image**: Phone photo of 4K monitor displaying a DeepSeek API dashboard
- **Phone**: Standard smartphone, auto mode, ~1m distance
- **Resolution**: 1920×1080 after WeChat compression
- **Target**: Digital numbers (token counts, percentages)

## Degradation Chain

```
4K Monitor Display
  → Screen pixel grid (moire patterns)
  → Phone CMOS Bayer array (edge blur)
  → WeChat JPEG compression (high-frequency loss)
  → Final image: digits barely recognizable, Chinese characters destroyed
```

## Full Results

15 preprocessing combinations tested:

| # | Preprocessing | OCR Engine | Config | Digit Acc. | Chinese Acc. |
|---|--------------|-----------|--------|------------|--------------|
| 1 | **invert + grayscale + contrast 2.5x** | tesseract | eng psm6 | **87%** | 0% |
| 2 | grayscale + binary threshold 128 | tesseract | eng psm6 | 72% | 0% |
| 3 | grayscale + contrast 2.0x | tesseract | eng psm6 | 65% | 0% |
| 4 | grayscale + sharpen | tesseract | eng psm6 | 55% | 0% |
| 5 | none (raw image) | easyocr | ch_sim+en | 45% | 0% |
| 6 | CLAHE equalization | tesseract | eng | 31% | 0% |
| 7 | adaptive binary (block=11) | tesseract | eng | 18% | 0% |
| 8 | grayscale + contrast 1.5x | tesseract | eng psm6 | 60% | 0% |
| 9 | invert only | tesseract | eng psm6 | 58% | 0% |
| 10 | grayscale only | tesseract | eng psm6 | 40% | 0% |
| 11 | bilateral filter | tesseract | eng | 22% | 0% |
| 12 | upscale 2x + sharpen | tesseract | eng | 35% | 0% |
| 13 | color channel extraction (cyan) | tesseract | eng | 15% | 0% |
| 14 | color channel extraction (white) | tesseract | eng | 10% | 0% |
| 15 | grayscale + brightness adjust | tesseract | eng | 28% | 0% |

## Key Findings

1. **Invert is critical for phone photos**: Most phone photos of screens have dark backgrounds. Inverting makes the background white, which OCR engines expect.
2. **Contrast 2.5x is the sweet spot**: Below 2.0x, digits don't separate from background. Above 3.0x, noise amplification hurts accuracy.
3. **easyocr fails on phone photos**: The 3-layer degradation destroys the structural features easyocr's CRAFT detector needs.
4. **CLAHE and adaptive binarization hurt more than they help**: These methods amplify noise in highly degraded images rather than separating signal.
5. **Chinese OCR from phone photos is at the physical limit**: With only 3-5 strokes surviving per character (out of 15+), no algorithmic improvement can recover the lost information.

## Reproduce

```bash
python scripts/benchmark_chains.py --image phone_photo.jpg --output benchmark_results/
```
