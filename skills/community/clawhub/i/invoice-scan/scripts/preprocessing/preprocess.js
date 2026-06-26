/**
 * Document Pre-Processing
 * 
 * Normalises input document quality before sending to AI extraction.
 * Uses Sharp (libvips) for image processing.
 */

const fs = require('fs');
const path = require('path');

let sharp;
try {
  sharp = require('sharp');
} catch (e) {
  sharp = null;
}

/**
 * Pre-process an image file for optimal OCR/AI extraction.
 * Returns a Buffer of the processed image (PNG format).
 * 
 * @param {string|Buffer} input - File path or Buffer
 * @param {object} options
 * @param {boolean} options.deskew - Attempt to straighten rotated scans
 * @param {boolean} options.denoise - Remove noise/artefacts
 * @param {boolean} options.enhanceContrast - Boost contrast for faded text
 * @param {boolean} options.upscale - Upscale low-res images
 * @param {number} options.minDpi - Minimum DPI threshold for upscaling (default: 150)
 * @returns {Promise<{ buffer: Buffer, metadata: object }>}
 */
async function preprocessImage(input, options = {}) {
  const {
    denoise = true,
    enhanceContrast = true,
    upscale = true,
    minDpi = 150,
    sharpen = true,
    normalise = true,
  } = options;

  if (!sharp) {
    // Sharp not available — return raw input
    const buffer = Buffer.isBuffer(input) ? input : fs.readFileSync(input);
    return {
      buffer,
      metadata: { preprocessed: false, reason: 'sharp not installed' },
    };
  }

  let pipeline = sharp(Buffer.isBuffer(input) ? input : fs.readFileSync(input));
  const inputMeta = await pipeline.metadata();
  const steps = [];

  // Auto-rotate based on EXIF
  pipeline = pipeline.rotate();
  steps.push('auto-rotate');

  // Upscale if below minimum DPI (estimate from dimensions)
  if (upscale && inputMeta.width && inputMeta.width < 1500) {
    const scale = Math.ceil(1500 / inputMeta.width);
    if (scale > 1 && scale <= 4) {
      pipeline = pipeline.resize(inputMeta.width * scale, null, {
        kernel: 'lanczos3',
      });
      steps.push(`upscale-${scale}x`);
    }
  }

  // Normalise (auto-stretch levels for contrast)
  if (normalise) {
    pipeline = pipeline.normalise();
    steps.push('normalise');
  }

  // Sharpen (helps OCR on slightly blurry scans)
  if (sharpen) {
    pipeline = pipeline.sharpen({ sigma: 1.0 });
    steps.push('sharpen');
  }

  // Median filter for denoising (light pass)
  if (denoise) {
    pipeline = pipeline.median(3);
    steps.push('denoise');
  }

  // Output as JPEG to keep size under API limits (5MB)
  pipeline = pipeline.jpeg({ quality: 90 });

  const buffer = await pipeline.toBuffer();
  const outputMeta = await sharp(buffer).metadata();

  return {
    buffer,
    metadata: {
      preprocessed: true,
      steps,
      input: {
        format: inputMeta.format,
        width: inputMeta.width,
        height: inputMeta.height,
        channels: inputMeta.channels,
      },
      output: {
        format: outputMeta.format,
        width: outputMeta.width,
        height: outputMeta.height,
        size: buffer.length,
      },
    },
  };
}

/**
 * Determine if a file is an image or PDF.
 * @param {string} filePath
 * @returns {'image'|'pdf'|'unknown'}
 */
function detectFileType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const imageExts = ['.png', '.jpg', '.jpeg', '.tiff', '.tif', '.webp', '.heic', '.svg'];
  if (imageExts.includes(ext)) return 'image';
  if (ext === '.pdf') return 'pdf';
  return 'unknown';
}

module.exports = { preprocessImage, detectFileType };
