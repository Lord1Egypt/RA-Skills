const QRCode = require('qrcode-reader');
const fs = require('fs');
const { createCanvas, loadImage } = require('canvas');

// Get image path from command line argument
const imagePath = process.argv[2];

if (!imagePath) {
  console.error('❌ Usage: node scan-qr.js <image-path>');
  process.exit(1);
}

(async () => {
  try {
    // Read image
    const image = await loadImage(imagePath);

    // Create canvas
    const canvas = createCanvas(image.width, image.height);
    const ctx = canvas.getContext('2d');

    // Draw image to canvas
    ctx.drawImage(image, 0, 0);

    // Get image data
    const imageData = ctx.getImageData(0, 0, image.width, image.height);

    // Use qrcode-reader to recognize QR code
    const qr = new QRCode();

    qr.callback = function(err, value) {
      if (err) {
        console.error('❌ 错误:', err.message);
        process.exit(1);
      } else if (value) {
        console.log('✅ 识别成功:', value.result);
      } else {
        console.error('❌ 未能识别二维码');
        process.exit(1);
      }
    };

    qr.decode(imageData);

  } catch (err) {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  }
})();
