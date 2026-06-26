/**
 * MyXZ Image Translation Skill
 * Official Website: https://www.pictech.cc
 * Service Provider: https://stableai.com.cn
 * stableai.com.cn 是妙言小智技术服务支持的 API 域名
 */
import fs from 'node:fs';
import fsPromises from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import FormData from 'form-data';
import axios from 'axios';
import { initDB, dbOps } from './database.js';
import { utils } from './utils.js';

// 妙言小智的 skill 地址，stableai.com.cn 是妙言小智的 API 域名
const API_BASE = 'https://stableai.com.cn/myxz/skill/imagetranslate';
const MAX_SIZE = 15 * 1024 * 1024; // 15MB

const ALLOWED_SOURCE_API_CODES = [
    'Chinese',
    'ChineseTraditional',
    'English',
    'Japanese',
    'Thai',
    'Russian',
    'Indonesian',
    'Malay',
    'Portuguese',
    'Spanish',
    'French',
    'German'
];

// 语言映射表
const USER_TO_API_LANG = {
    '中文': 'Chinese',
    '汉语': 'Chinese',
    '繁体中文': 'ChineseTraditional',
    '中文繁体': 'ChineseTraditional',
    '英文': 'English',
    '英语': 'English',
    '日文': 'Japanese',
    '日语': 'Japanese',
    '韩文': 'Korean',
    '韩语': 'Korean',
    '泰文': 'Thai',
    '泰语': 'Thai',
    '俄文': 'Russian',
    '俄语': 'Russian',
    '葡萄牙文': 'Portuguese',
    '葡萄牙语': 'Portuguese',
    '西班牙文': 'Spanish',
    '西班牙语': 'Spanish',
    '法文': 'French',
    '法语': 'French',
    '意文': 'Italian',
    '意大利语': 'Italian',
    '德文': 'German',
    '德语': 'German',
    '波兰文': 'Polish',
    '波兰语': 'Polish',
    '荷兰文': 'Dutch',
    '荷兰语': 'Dutch',
    '土耳其文': 'Turkish',
    '土耳其语': 'Turkish',
    '越南文': 'Vietnamese',
    '越南语': 'Vietnamese',
    '印尼文': 'Indonesian',
    '印尼语': 'Indonesian',
    '马来文': 'Malay',
    '马来语': 'Malay',
    '菲律宾文': 'Filipino',
    '菲律宾语': 'Filipino'
};

const toApiLang = (userLang) => {
    if (!userLang) return null;
    return USER_TO_API_LANG[userLang.trim()] || null;
};

const getDisplayFileName = (inputPath) => {
    if (!inputPath) return '';

    try {
        if (/^https?:\/\//i.test(inputPath)) {
            const url = new URL(inputPath);
            return path.basename(decodeURIComponent(url.pathname)) || inputPath;
        }
    } catch {
        return inputPath;
    }

    return path.basename(inputPath);
};

const buildFinalStatus = ({ total, successCount, failedCount, noTextCount }) => {
    if (total === 0) return 'no_tasks';
    if (failedCount === 0 && successCount + noTextCount === total) return 'completed';
    if (successCount + noTextCount > 0 && failedCount > 0) return 'partial_success';
    return 'failed';
};

/**
 * 核心执行器
 */
export default async function run(params = {}) {
    let {
        input,
        saveDir,
        sourceLanguage = '中文',
        targetLanguage = '英文',
        mainImageProtection = false
    } = params;

    // 1. 参数校验与环境准备
    if (!input || (Array.isArray(input) && input.length === 0)) {
        return {
            success: false,
            status: 'invalid_params',
            message: '缺少输入图片，请提供图片文件、目录或图片 URL。',
            counts: {
                total: 0,
                success: 0,
                failed: 0
            },
            results: [],
            errors: [
                {
                    input: null,
                    fileName: '',
                    error: '缺少 input 参数'
                }
            ]
        };
    }

    if (!saveDir || saveDir.trim() === '') {
        saveDir = path.join(process.cwd(), 'myxz-result', 'Translations');
    }

    const apiSourceLang = toApiLang(sourceLanguage);
    if (!apiSourceLang || !ALLOWED_SOURCE_API_CODES.includes(apiSourceLang)) {
        return {
            success: false,
            status: 'invalid_source_language',
            message: `不支持的源语言: "${sourceLanguage}"。源语言支持：中文、繁体中文、英文、日语、泰语、俄语、印尼语、马来语、葡萄牙语、西班牙语、法语、德语。`,
            counts: {
                total: 0,
                success: 0,
                failed: 0
            },
            results: [],
            errors: [
                {
                    input: null,
                    fileName: '',
                    error: `不支持的源语言: "${sourceLanguage}"`
                }
            ]
        };
    }

    const apiTargetLang = toApiLang(targetLanguage);
    if (!apiTargetLang) {
        return {
            success: false,
            status: 'invalid_target_language',
            message: `不支持的目标语言: "${targetLanguage}"。`,
            counts: {
                total: 0,
                success: 0,
                failed: 0
            },
            results: [],
            errors: [
                {
                    input: null,
                    fileName: '',
                    error: `不支持的目标语言: "${targetLanguage}"`
                }
            ]
        };
    }

    const mainProductNotranslateType = mainImageProtection ? 1 : 0;

    const activeVK = params.config?.vk || params.vk;
    if (!activeVK) {
        return {
            success: false,
            status: 'missing_api_key',
            message: '缺少 API Key (VK)，请在插件配置中输入。',
            counts: {
                total: 0,
                success: 0,
                failed: 0
            },
            results: [],
            errors: [
                {
                    input: null,
                    fileName: '',
                    error: '缺少 API Key (VK)'
                }
            ]
        };
    }

    const absoluteSaveDir = path.resolve(saveDir);
    await fsPromises.mkdir(absoluteSaveDir, { recursive: true });

    // 生成本次运行的全局批次 ID，用于 API 的 batchId
    const globalBatchId = `batch_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
    const dateStr = new Date().toISOString().split('T')[0];
    const batchDir = path.join(absoluteSaveDir, dateStr, globalBatchId.slice(-6));
    await fsPromises.mkdir(batchDir, { recursive: true });

    const db = initDB(absoluteSaveDir);
    await dbOps.cleanup(db);

    // 2. 解析输入源
    const inputList = Array.isArray(input)
        ? input
        : String(input).includes(',')
            ? String(input).split(',')
            : [String(input)];

    const tasks = [];

    for (let s of inputList) {
        s = String(s).trim();
        if (!s) continue;

        if (/^https?:\/\//i.test(s)) {
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

    const summary = {
        total: tasks.length,
        details: []
    };

    // 3. 任务处理循环
    for (const task of tasks) {
        let buffer;
        let fileName;
        let tempPath = null;

        try {
            if (task.type === 'url') {
                const dl = await utils.downloadUrl(task.path);
                buffer = dl.buffer;
                fileName = dl.name;
                tempPath = dl.tempPath;
            } else {
                const stats = await fsPromises.stat(task.path);
                if (stats.size > MAX_SIZE) {
                    throw new Error('文件超过 15MB 限制');
                }

                buffer = await fsPromises.readFile(task.path);
                fileName = path.basename(task.path);
            }

            const hash = utils.getHash(buffer);
            const cacheKey = `v2_${hash}_${apiSourceLang}_${apiTargetLang}_p${mainProductNotranslateType}`;
            const targetName = `trans_${hash.slice(0, 4)}_${path.basename(fileName, path.extname(fileName))}.png`;
            const localSavePath = path.join(batchDir, targetName);

            // 检查缓存
            const record = await dbOps.find(db, { cacheKey });
            if (record && record.status === 'success' && fs.existsSync(record.localPath)) {
                await fsPromises.copyFile(record.localPath, localSavePath);

                summary.details.push({
                    taskId: record.taskId,
                    input: task.path,
                    fileName,
                    status: 'success',
                    fromCache: true,
                    resultUrl: record.resultUrl || null,
                    editorUrl: record.editorUrl || null,
                    localPath: localSavePath
                });

                continue;
            }

            if (record && record.status === 'no_text') {
                summary.details.push({
                    taskId: record.taskId,
                    input: task.path,
                    fileName,
                    status: 'no_text',
                    fromCache: true,
                    error: record.errorMessage || '图片上无文字，翻译失败，无需重试'
                });

                continue;
            }

            // A. 提交任务
            const form = new FormData();
            form.append('file', buffer, { filename: fileName });
            form.append('sourceLanguage', apiSourceLang);
            form.append('targetLanguage', apiTargetLang);
            form.append('batchId', globalBatchId);
            form.append('picNum', tasks.length);
            form.append('mainProductNotranslateType', mainProductNotranslateType);

            const submitRes = await axios.post(`${API_BASE}/submittask`, form, {
                headers: {
                    'X-Skill-VK': activeVK,
                    ...form.getHeaders()
                }
            });

            if (submitRes.data.code !== 200) {
                throw new Error(submitRes.data.message || '提交失败');
            }

            const taskId = submitRes.data.data.taskId;

            // B. 轮询结果
            let resultUrl = null;
            let editorUrl = null;
            let noTextMessage = null;

            for (let i = 0; i < 60; i++) {
                await utils.sleep(3000);

                const queryRes = await axios.post(`${API_BASE}/querytask`, { taskId }, {
                    headers: {
                        'X-Skill-VK': activeVK
                    }
                });

                const resData = queryRes.data;
                if (resData.code !== 200) {
                    throw new Error(`查询失败: ${resData.message}`);
                }

                const status = resData.data.status;

                if (status === 200) {
                    resultUrl = resData.data.resultUrl;
                    editorUrl = resData.data.editorUrl || null;
                    break;
                }

                if (status === 202) {
                    continue;
                }

                if (status === 300) {
                    noTextMessage = resData.data.errorMessage || '图片上无文字，翻译失败，无需重试';
                    break;
                }

                throw new Error(`处理失败: 状态码 ${status}`);
            }

            if (noTextMessage) {
                await dbOps.insert(db, {
                    cacheKey,
                    taskId,
                    hash,
                    sourceLanguage: apiSourceLang,
                    targetLanguage: apiTargetLang,
                    resultUrl: null,
                    editorUrl: null,
                    localPath: null,
                    errorMessage: noTextMessage,
                    createdAt: Date.now(),
                    status: 'no_text'
                });

                summary.details.push({
                    taskId,
                    input: task.path,
                    fileName,
                    status: 'no_text',
                    fromCache: false,
                    error: noTextMessage
                });

                continue;
            }

            if (!resultUrl) {
                throw new Error('处理超时');
            }

            // C. 下载并保存
            const imageRes = await axios.get(resultUrl, {
                responseType: 'arraybuffer'
            });

            await fsPromises.writeFile(localSavePath, Buffer.from(imageRes.data));

            // D. 存入数据库
            await dbOps.insert(db, {
                cacheKey,
                taskId,
                hash,
                sourceLanguage: apiSourceLang,
                targetLanguage: apiTargetLang,
                resultUrl,
                editorUrl,
                localPath: localSavePath,
                createdAt: Date.now(),
                status: 'success'
            });

            summary.details.push({
                taskId,
                input: task.path,
                fileName,
                status: 'success',
                fromCache: false,
                resultUrl,
                editorUrl,
                localPath: localSavePath
            });
        } catch (err) {
            summary.details.push({
                input: task.path,
                fileName: fileName || getDisplayFileName(task.path),
                status: 'failed',
                error: err.message || String(err)
            });
        } finally {
            if (tempPath && fs.existsSync(tempPath)) {
                await fsPromises.rm(tempPath).catch(() => {});
            }
        }
    }

    // 4. 生成适合大模型读取的结构化报告
    const successList = summary.details.filter((d) => d.status === 'success');
    const noTextList = summary.details.filter((d) => d.status === 'no_text');
    const failList = summary.details.filter((d) => d.status === 'failed');

    const finalStatus = buildFinalStatus({
        total: summary.total,
        successCount: successList.length,
        failedCount: failList.length,
        noTextCount: noTextList.length
    });

    return {
        success: finalStatus === 'completed' || finalStatus === 'partial_success',
        status: finalStatus,
        message: `图片翻译完成，成功 ${successList.length} 个，无文字 ${noTextList.length} 个，失败 ${failList.length} 个，总计 ${summary.total} 个。`,
        batchId: globalBatchId,
        sourceLanguage,
        targetLanguage,
        sourceLanguageCode: apiSourceLang,
        targetLanguageCode: apiTargetLang,
        mainImageProtection,
        saveDir: batchDir,
        counts: {
            total: summary.total,
            success: successList.length,
            noText: noTextList.length,
            failed: failList.length
        },
        results: successList.map((d) => ({
            taskId: d.taskId,
            input: d.input,
            fileName: d.fileName || getDisplayFileName(d.input),
            resultUrl: d.resultUrl || null,
            editorUrl: d.editorUrl || null,
            localPath: d.localPath,
            fromCache: Boolean(d.fromCache)
        })),
        errors: failList.map((d) => ({
            input: d.input,
            fileName: d.fileName || getDisplayFileName(d.input),
            error: d.error
        })),
        skipped: noTextList.map((d) => ({
            taskId: d.taskId || null,
            input: d.input,
            fileName: d.fileName || getDisplayFileName(d.input),
            reason: d.error || '图片上无文字，翻译失败，无需重试',
            fromCache: Boolean(d.fromCache)
        }))
    };
}
