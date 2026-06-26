"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.getLibrary = getLibrary;
exports.findPreset = findPreset;
exports.addPreset = addPreset;
exports.removePreset = removePreset;
exports.parsePulsesContent = parsePulsesContent;
exports.loadPulsesFile = loadPulsesFile;
exports.exportLibrary = exportLibrary;
exports.autoLoadFromDir = autoLoadFromDir;
/**
 * 波形库管理 + .pulses / JSON5 文件解析
 *
 * 支持格式:
 * 1. Coyote-Game-Hub pulse.json5: [{ id, name, pulseData: string[] }]
 * 2. 单个波形 JSON: { id?, name, pulseData: string[] }
 * 3. 纯 pulseData 数组: ["0A0A0A0A64646464", ...]
 */
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
// ─── 内存波形库 ───
const library = new Map();
/** 获取整个波形库 */
function getLibrary() {
    return Array.from(library.values());
}
/** 按 id 或 name 查找波形 */
function findPreset(idOrName) {
    const lower = idOrName.toLowerCase();
    // 先精确 id 匹配
    if (library.has(lower))
        return library.get(lower);
    // 再 name 模糊匹配
    for (const p of library.values()) {
        if (p.name.toLowerCase() === lower)
            return p;
        if (p.name.toLowerCase().includes(lower))
            return p;
    }
    return undefined;
}
/** 添加单个波形到库 */
function addPreset(preset) {
    library.set(preset.id.toLowerCase(), preset);
}
/** 删除波形 */
function removePreset(id) {
    return library.delete(id.toLowerCase());
}
// ─── 验证 ───
/** 验证单条 hex 是否为合法的 8 字节 (16 hex chars) */
function isValidHex(hex) {
    return /^[0-9A-Fa-f]{16}$/.test(hex);
}
/** 验证 pulseData 数组 */
function validatePulseData(data) {
    if (!Array.isArray(data) || data.length === 0)
        return false;
    return data.every((item) => typeof item === 'string' && isValidHex(item));
}
// ─── 简易 JSON5 解析（去除注释 + 允许尾逗号 + 无引号 key）───
function stripJson5(text) {
    // 去掉单行 // 注释和多行 /* */ 注释（简单处理，不处理字符串内的情况）
    let result = text.replace(/\/\/.*$/gm, '');
    result = result.replace(/\/\*[\s\S]*?\*\//g, '');
    // 尾逗号
    result = result.replace(/,\s*([\]}])/g, '$1');
    // 无引号 key → 加引号
    result = result.replace(/([{,]\s*)([a-zA-Z_$][\w$]*)\s*:/g, '$1"$2":');
    // 单引号 → 双引号（简单处理）
    result = result.replace(/'/g, '"');
    return result;
}
function parseJson5(text) {
    return JSON.parse(stripJson5(text));
}
// ─── 解析入口 ───
function generateId() {
    return Math.random().toString(16).slice(2, 10);
}
/**
 * 解析 .pulses / .json5 / .json 文件内容
 * @returns 解析出的波形列表
 */
function parsePulsesContent(content, fileName) {
    const parsed = parseJson5(content);
    const results = [];
    // 格式 1: 数组
    if (Array.isArray(parsed)) {
        // 可能是 [{ id, name, pulseData }] 或纯 ["hex", "hex"]
        if (parsed.length > 0 && typeof parsed[0] === 'string') {
            // 纯 pulseData 数组
            if (!validatePulseData(parsed)) {
                throw new Error('Invalid pulseData: hex strings must be exactly 16 hex characters');
            }
            results.push({
                id: generateId(),
                name: fileName ? path.basename(fileName, path.extname(fileName)) : 'Imported Waveform',
                pulseData: parsed,
            });
        }
        else {
            // 对象数组
            for (const item of parsed) {
                if (item && typeof item === 'object' && 'pulseData' in item) {
                    const obj = item;
                    if (!validatePulseData(obj.pulseData)) {
                        console.warn(`[PulseLib] Skipping invalid pulseData for "${obj.name || 'unknown'}"`);
                        continue;
                    }
                    results.push({
                        id: (typeof obj.id === 'string' ? obj.id : generateId()),
                        name: (typeof obj.name === 'string' ? obj.name : `Waveform ${results.length + 1}`),
                        pulseData: obj.pulseData,
                    });
                }
            }
        }
    }
    else if (parsed && typeof parsed === 'object') {
        // 格式 2: 单个 { id?, name, pulseData }
        const obj = parsed;
        if ('pulseData' in obj && validatePulseData(obj.pulseData)) {
            results.push({
                id: (typeof obj.id === 'string' ? obj.id : generateId()),
                name: (typeof obj.name === 'string' ? obj.name : fileName || 'Imported Waveform'),
                pulseData: obj.pulseData,
            });
        }
        else {
            throw new Error('Invalid pulse file: missing or invalid pulseData field');
        }
    }
    else {
        throw new Error('Invalid pulse file format: expected array or object');
    }
    if (results.length === 0) {
        throw new Error('No valid waveforms found in file');
    }
    return results;
}
/**
 * 从文件路径加载波形并添加到库
 */
function loadPulsesFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const presets = parsePulsesContent(content, path.basename(filePath));
    for (const p of presets) {
        addPreset(p);
    }
    return presets;
}
/**
 * 将当前库导出为 JSON5 格式字符串
 */
function exportLibrary() {
    const items = getLibrary();
    return JSON.stringify(items, null, 2);
}
/**
 * 从 data 目录自动加载所有 .pulses / .json5 / .json 文件
 */
function autoLoadFromDir(dirPath) {
    if (!fs.existsSync(dirPath))
        return 0;
    let count = 0;
    const files = fs.readdirSync(dirPath);
    for (const file of files) {
        if (/\.(pulses|json5?|pulse)$/i.test(file)) {
            try {
                const presets = loadPulsesFile(path.join(dirPath, file));
                count += presets.length;
                console.log(`[PulseLib] Loaded ${presets.length} waveform(s) from ${file}`);
            }
            catch (e) {
                console.warn(`[PulseLib] Failed to load ${file}: ${e.message}`);
            }
        }
    }
    return count;
}
//# sourceMappingURL=pulselib.js.map