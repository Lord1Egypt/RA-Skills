import fs from 'fs';
import path from 'path';
import { getApiKey, httpsRequest, API_HOST, log, colors, success, error } from '../utils.js';

export async function generateQrCode(entityId, options = {}) {
  const apiKey = getApiKey(options?.apiKey);

  const entityType = options.entityType || 'Tongji';
  const entityPrefix = entityType.toLowerCase();

  const data = JSON.stringify({
    entityId: entityId,
    entityType: entityType,
    app: options.app || 'qingtongji'
  });

  try {
    const response = await httpsRequest(
      {
        hostname: API_HOST,
        port: 443,
        path: '/api/openapi/creator/qrcode',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`,
          'Content-Length': Buffer.byteLength(data)
        }
      },
      data
    );

    if (response.success && response.data && response.data.qrcodeBase64) {
      const qrcodeBase64 = response.data.qrcodeBase64;

      const qrcodeDir = options.output ? path.dirname(options.output) : './qrcodes';
      const imageFormat = qrcodeBase64.match(/^data:image\/([a-z]+);base64,/)?.[1] || 'png';
      const qrcodePath =
        options.output || path.join(qrcodeDir, `${entityPrefix}_${entityId}.${imageFormat}`);

      if (!fs.existsSync(qrcodeDir)) {
        fs.mkdirSync(qrcodeDir, { recursive: true });
      }

      const base64Data = qrcodeBase64.replace(/^data:image\/[a-z]+;base64,/, '');
      fs.writeFileSync(qrcodePath, base64Data, 'base64');

      success('二维码已保存:', qrcodePath);
      return qrcodePath;
    } else {
      throw new Error('生成二维码失败');
    }
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}

export async function generateToupiaoQrCode(toupiaoId, options = {}) {
  const apiKey = getApiKey(options?.apiKey);

  const data = JSON.stringify({
    entityId: toupiaoId,
    entityType: 'Toupiao',
    app: options.app || 'qingtongji'
  });

  try {
    const response = await httpsRequest(
      {
        hostname: API_HOST,
        port: 443,
        path: '/api/openapi/creator/qrcode',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`,
          'Content-Length': Buffer.byteLength(data)
        }
      },
      data
    );

    if (response.success && response.data && response.data.qrcodeBase64) {
      const qrcodeBase64 = response.data.qrcodeBase64;

      const qrcodeDir = options.output ? path.dirname(options.output) : './qrcodes';
      const qrcodePath = options.output || path.join(qrcodeDir, `toupiao_${toupiaoId}.png`);

      if (!fs.existsSync(qrcodeDir)) {
        fs.mkdirSync(qrcodeDir, { recursive: true });
      }

      const base64Data = qrcodeBase64.replace(/^data:image\/[a-z]+;base64/, '');
      fs.writeFileSync(qrcodePath, base64Data, 'base64');

      success('二维码已保存:', qrcodePath);
      return qrcodePath;
    } else {
      throw new Error('生成二维码失败');
    }
  } catch (err) {
    error(err.message);
    process.exit(1);
  }
}
