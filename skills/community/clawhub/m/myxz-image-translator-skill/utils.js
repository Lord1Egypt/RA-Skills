import crypto from 'node:crypto';
import fsPromises from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import axios from 'axios';

export const utils = {
    getHash: (buffer) => crypto.createHash('md5').update(buffer).digest('hex'),
    isValidFormat: (ext) => ['.jpg', '.jpeg', '.png', '.webp', '.bmp'].includes(ext.toLowerCase()),
    sleep: (ms) => new Promise(res => setTimeout(res, ms)),
    downloadUrl: async (url) => {
        const tempPath = path.join(os.tmpdir(), `trans_${crypto.randomBytes(4).toString('hex')}`);
        const res = await axios({ url, method: 'GET', responseType: 'arraybuffer', timeout: 30000 });
        const buffer = Buffer.from(res.data);
        await fsPromises.writeFile(tempPath, buffer);
        let name = 'web_image.png';
        try { name = path.basename(new URL(url).pathname) || name; } catch (e) { }
        return { buffer, tempPath, name };
    }
};