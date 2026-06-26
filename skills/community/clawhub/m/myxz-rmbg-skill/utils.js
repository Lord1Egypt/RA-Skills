import crypto from 'node:crypto';
import fsPromises from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import axios from 'axios';

export const utils = {
    /**
     * 计算 Buffer 的 MD5 指纹
     */
    getHash: (buffer) => crypto.createHash('md5').update(buffer).digest('hex'),

    /**
     * 校验图片格式 (支持大写)
     */
    isValidFormat: (ext) => {
        if (!ext) return false;
        return ['.jpg', '.jpeg', '.png', '.webp'].includes(ext.toLowerCase());
    },

    /**
     * 下载 URL 图片到系统临时目录
     * 采用原生 fsPromises 替代 fs-extra
     */
    downloadUrl: async (url) => {
        // 生成唯一的临时文件路径
        const tempFileName = `rmbg_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
        const tempPath = path.join(os.tmpdir(), tempFileName);

        // 下载图片
        const response = await axios({
            url,
            method: 'GET',
            responseType: 'arraybuffer',
            timeout: 30000 // 增加超时到 30 秒提高稳定性
        });

        const buffer = Buffer.from(response.data);

        // 使用原生 fsPromises 写入文件
        await fsPromises.writeFile(tempPath, buffer);

        // 尝试从 URL 提取文件名
        let fileName = 'web_image.png';
        try {
            const urlObj = new URL(url);
            const baseName = path.basename(urlObj.pathname);
            if (baseName && baseName.includes('.')) {
                fileName = baseName;
            }
        } catch (e) {
            // URL 解析失败则使用默认名
        }

        return { buffer, tempPath, name: fileName };
    },

    /**
     * 基于 Promise 的延迟函数
     */
    sleep: (ms) => new Promise(res => setTimeout(res, ms))
};