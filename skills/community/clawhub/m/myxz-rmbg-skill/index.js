import fs from 'node:fs';
import fsPromises from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import FormData from 'form-data';
import axios from 'axios';
import { initDB, dbOps } from './database.js';
import { utils } from './utils.js';

// 配置常量 - 指向新的 C端通道接口
const API_BASE = 'https://stableai.com.cn/myxz/skill/imagermbg';
const MAX_SIZE = 15 * 1024 * 1024; // 15MB

function fail(error, data = undefined) {
    return {
        success: false,
        message: error,
        error,
        data
    };
}

/**
 * 核心执行器 - 适配新抠图 API
 */
export default async function run(params = {}) {
    let { input, saveDir, backgroundColor } = params;
    const vk = params.config?.vk || params.vk;

    // 1. VK 校验
    const activeVK = vk || process.env.RMBG_VK;
    if (!activeVK) {
        return fail('缺少 API Key (VK)，请在插件配置中输入。');
    }

    if (!input || (typeof input === 'string' && input.trim() === '')) {
        return fail('缺少输入图片，请提供图片路径、目录、URL 或数组。');
    }

    if (!saveDir || saveDir.trim() === '') {
        saveDir = path.join(process.cwd(), 'myxz-result', 'bgremove-v2');
    }

    // 2. 初始化环境
    const absoluteSaveDir = path.resolve(saveDir);
    const dateStr = new Date().toISOString().split('T')[0];
    const batchId = crypto.randomBytes(4).toString('hex');
    const batchDir = path.join(absoluteSaveDir, dateStr, batchId);

    try {
        await fsPromises.mkdir(batchDir, { recursive: true });
    } catch (err) {
        return fail(`无法创建目录: ${err.message}`);
    }

    const db = initDB(absoluteSaveDir);
    await dbOps.cleanup(db);

    // 3. 解析输入源
    const sources = Array.isArray(input)
        ? input
        : String(input).includes(',')
            ? String(input).split(',')
            : [input];

    const tasks = [];

    for (let s of sources) {
        s = String(s).trim();
        if (!s) continue;

        if (s.startsWith('http')) {
            tasks.push({ type: 'url', path: s });
            continue;
        }

        if (!fs.existsSync(s)) continue;

        const stats = await fsPromises.lstat(s);

        if (stats.isDirectory()) {
            const files = await fsPromises.readdir(s);

            for (const f of files) {
                if (utils.isValidFormat(path.extname(f))) {
                    tasks.push({ type: 'file', path: path.join(s, f) });
                }
            }
        } else if (utils.isValidFormat(path.extname(s))) {
            tasks.push({ type: 'file', path: s });
        }
    }

    const totalPicNum = tasks.length;

    if (totalPicNum === 0) {
        return fail('未找到可处理的图片，请检查输入路径、URL 或图片格式。', {
            batchId,
            saveDir: batchDir,
            total: 0,
            results: [],
            failures: []
        });
    }

    const summary = {
        total: totalPicNum,
        details: []
    };

    // 4. 串行处理任务
    for (const task of tasks) {
        let buffer;
        let fileName;
        let tempPath = null;

        try {
            // A. 加载图片数据
            if (task.type === 'url') {
                const dl = await utils.downloadUrl(task.path);
                buffer = dl.buffer;
                fileName = dl.name;
                tempPath = dl.tempPath;
            } else {
                const stats = await fsPromises.stat(task.path);
                if (stats.size > MAX_SIZE) {
                    throw new Error('文件超过15MB限制');
                }

                buffer = await fsPromises.readFile(task.path);
                fileName = path.basename(task.path);
            }

            // B. 缓存检查
            const imageHash = utils.getHash(buffer);
            const normalizedBgColor = backgroundColor || 'transparent';
            const cacheSeed = `${imageHash}:${normalizedBgColor}`;
            const hash = utils.getHash(Buffer.from(cacheSeed));
            const bgSuffix = normalizedBgColor === 'transparent'
                ? 'transparent'
                : normalizedBgColor.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
            const targetName = `${path.basename(fileName, path.extname(fileName))}_no_bg_${bgSuffix}.png`;
            const localSavePath = path.join(batchDir, targetName);

            const record = await dbOps.find(db, { hash });

            if (record && record.status === 'success' && fs.existsSync(record.localPath)) {
                summary.details.push({
                    taskId: record.taskId,
                    input: task.path,
                    status: 'success',
                    cached: true,
                    resultUrl: record.remoteUrl,
                    localPath: record.localPath
                });
                continue;
            }

            // C. 提交任务
            const form = new FormData();
            form.append('file', buffer, { filename: fileName });
            form.append('batchId', batchId);
            form.append('picNum', String(totalPicNum));

            if (backgroundColor) {
                form.append('backgroundColor', backgroundColor);
            }

            const sRes = await axios.post(`${API_BASE}/submittask`, form, {
                headers: {
                    'X-Skill-VK': activeVK,
                    ...form.getHeaders()
                },
                timeout: 30000
            });

            if (sRes.data.code !== 200) {
                throw new Error(sRes.data.message || '任务提交失败');
            }

            // taskId 格式一般为 "orderId###itemId"
            const taskId = sRes.data.data.taskId;

            // D. 轮询结果
            let remoteUrl = null;

            for (let i = 0; i < 60; i++) {
                await utils.sleep(1500);

                const qRes = await axios.post(
                    `${API_BASE}/querytask`,
                    { taskId },
                    {
                        headers: {
                            'X-Skill-VK': activeVK
                        },
                        timeout: 30000
                    }
                );

                const resData = qRes.data;

                if (resData.code !== 200) {
                    throw new Error(`查询出错: ${resData.message}`);
                }

                const taskStatus = resData.data.status;

                if (taskStatus === 200) {
                    remoteUrl = resData.data.resultUrl;
                    break;
                }

                if (taskStatus === 202) {
                    continue;
                }

                throw new Error(resData.data.message || 'AI处理失败');
            }

            if (!remoteUrl) {
                throw new Error('处理超时');
            }

            // E. 下载并保存
            const imgRes = await axios.get(remoteUrl, {
                responseType: 'arraybuffer',
                timeout: 60000
            });

            await fsPromises.writeFile(localSavePath, Buffer.from(imgRes.data));

            // F. 存入数据库
            await dbOps.insert(db, {
                hash,
                taskId,
                status: 'success',
                remoteUrl,
                localPath: localSavePath,
                bgColor: backgroundColor || 'transparent',
                createdAt: Date.now()
            });

            summary.details.push({
                taskId,
                input: task.path,
                status: 'success',
                cached: false,
                resultUrl: remoteUrl,
                localPath: localSavePath
            });
        } catch (err) {
            summary.details.push({
                input: task.path,
                status: 'failed',
                error: err.message
            });
        } finally {
            if (tempPath && fs.existsSync(tempPath)) {
                await fsPromises.rm(tempPath).catch(() => { });
            }
        }
    }

    // 5. 生成统一返回值
    const successList = summary.details.filter(d => d.status === 'success');
    const failList = summary.details.filter(d => d.status === 'failed');

    const success = successList.length > 0;
    const partialSuccess = successList.length > 0 && failList.length > 0;

    return {
        success,
        partialSuccess,
        message: success
            ? `处理完成，成功 ${successList.length} 张，总计 ${summary.total} 张。`
            : `处理失败，成功 0 张，总计 ${summary.total} 张。`,
        error: success ? undefined : '全部图片处理失败',
        data: {
            batchId,
            saveDir: batchDir,
            total: summary.total,
            successCount: successList.length,
            failedCount: failList.length,
            backgroundColor: backgroundColor || 'transparent',
            results: successList.map(d => ({
                input: d.input,
                fileName: path.basename(d.input),
                taskId: d.taskId,
                resultUrl: d.resultUrl,
                localPath: d.localPath,
                cached: Boolean(d.cached)
            })),
            failures: failList.map(d => ({
                input: d.input,
                fileName: path.basename(d.input),
                error: d.error
            }))
        }
    };
}
