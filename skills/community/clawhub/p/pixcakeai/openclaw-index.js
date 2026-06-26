const sharp = require("sharp");

module.exports = {
  async handleRequest(event) {
    const data = event.data || {};
    const img = data.image || data.file;
    const txt = data.watermark_text || data.text;
    
    if (!img) {
      return { statusCode: 400, body: "No image provided" };
    }
    
    // Get buffer from input
    let buf = typeof img === "string" ? Buffer.from(img.split(",").pop(), "base64") : img.data ? Buffer.from(img.data, "base64") : img;
    
    // Step 1: Resize to 9:16 aspect ratio
    const meta = await sharp(buf).metadata();
    const targetWidth = meta.width;
    const targetHeight = Math.floor(meta.width * (16 / 9));
    
    // Crop or extend to 9:16
    if (meta.height > targetHeight) {
      // Center crop
      buf = await sharp(buf)
        .extract({
          left: 0,
          top: Math.floor((meta.height - targetHeight) / 2),
          width: targetWidth,
          height: targetHeight
        })
        .toBuffer();
    } else if (meta.height < targetHeight) {
      // Extend with black bars
      buf = await sharp(buf)
        .extend({
          top: Math.floor((targetHeight - meta.height) / 2),
          bottom: Math.ceil((targetHeight - meta.height) / 2),
          background: { r: 0, g: 0, b: 0, alpha: 1 }
        })
        .toBuffer();
    }
    
    // Step 2: Apply enhancements (CCD effect)
    buf = await sharp(buf)
      .sharpen({ sigma: 1.2, m1: 0, m2: 0.8 })
      .modulate({ brightness: 1.08, saturation: 1.15 })
      .blur(0.3)
      .sharpen({ sigma: 0.8, m1: 0, m2: 0.5 })
      .modulate({ brightness: 1.05, saturation: 1.12 })
      .gamma(1.02)
      .toBuffer();
    
    // Step 3: Add watermark if text exists
    if (txt) {
      const m = await sharp(buf).metadata();
      const h = Math.floor(m.height * 0.12);
      const fs = Math.floor(h * 0.55);
      const safe = String(txt).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
      
      const svg = `<svg width="${m.width}" height="${h}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#000" fill-opacity="0.4"/><text x="50%" y="52%" font-family="Arial" font-size="${fs}" font-weight="600" fill="#fff" fill-opacity="0.85" text-anchor="middle">${safe}</text></svg>`;
      
      buf = await sharp(buf)
        .composite([{ input: Buffer.from(svg), top: m.height - h, left: 0 }])
        .toBuffer();
    }
    
    // Step 4: Final output
    const out = await sharp(buf).jpeg({ quality: 95, progressive: true }).toBuffer();
    
    return { statusCode: 200, body: out.toString("base64"), isBase64Encoded: true, headers: { "Content-Type": "image/jpeg" } };
  }
};
