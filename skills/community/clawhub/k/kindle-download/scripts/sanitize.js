/**
 * 输入验证和清理模块
 * 用于防止 Shell 注入攻击
 * 
 * 安全设计原则：
 * 1. 白名单优先 - 只允许已知安全的字符
 * 2. 深度防御 - 多层过滤，不依赖单一检查
 * 3. 明确失败 - 无效输入返回明确错误，不尝试修复
 */

/**
 * 危险的 Shell 元字符
 * 这些字符在 Shell 中有特殊含义，必须被过滤
 */
const DANGEROUS_SHELL_CHARS = [
    ";",   // 命令分隔符
    "|",   // 管道
    "&",   // 后台执行 / 命令连接
    "$",   // 变量引用
    "`",   // 命令替换（反引号）
    "(",   // 子 shell
    ")",   // 子 shell
    "{",   // 命令组
    "}",   // 命令组
    "<",   // 输入重定向
    ">",   // 输出重定向
    "!",   // 历史扩展
    "\\n", // 换行符
    "\\r", // 回车符
    "\\x00", // 空字节
];

/**
 * 检查字符串是否包含危险的 Shell 元字符
 * @param {string} input - 要检查的字符串
 * @returns {boolean} - 如果包含危险字符返回 true
 */
function containsDangerousChars(input) {
    if (typeof input !== "string") return true;
    
    // 检查危险的 Shell 元字符
    for (const char of DANGEROUS_SHELL_CHARS) {
        if (input.includes(char)) {
            return true;
        }
    }
    
    // 检查控制字符（ASCII 0-31，除了空格、制表符、换行、回车）
    if (/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(input)) {
        return true;
    }
    
    // 检查命令替换模式 $() 和 ``
    if (/\$\([^)]*\)/.test(input) || /\`[^\`]*\`/.test(input)) {
        return true;
    }
    
    // 检查变量扩展 ${...}
    if (/\$\{[^}]*\}/.test(input)) {
        return true;
    }
    
    return false;
}

/**
 * 清理字符串，移除危险的 shell 字符
 * @param {string} input - 原始输入
 * @param {number} maxLength - 最大长度限制
 * @returns {string} - 清理后的字符串
 */
function sanitizeString(input, maxLength = 200) {
    if (typeof input !== "string") {
        return "";
    }
    
    // 限制长度
    let sanitized = input.slice(0, maxLength);
    
    // 移除控制字符（保留基本空格和制表符）
    sanitized = sanitized.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, "");
    
    // 移除危险的 Shell 元字符
    for (const char of DANGEROUS_SHELL_CHARS) {
        sanitized = sanitized.split(char).join("");
    }
    
    // 使用白名单验证：只保留安全字符
    // 允许：中文、英文、数字、空格、基本标点（中文和英文）
    const safeChars = sanitized.match(/[\u4e00-\u9fa5a-zA-Z0-9\s\-_,\\.。·、：:（）()"'"'!?！？]/g);
    if (safeChars) {
        sanitized = safeChars.join("");
    } else {
        sanitized = "";
    }
    
    return sanitized.trim();
}

/**
 * 验证书名格式
 * @param {string} title - 书名
 * @returns {{valid: boolean, sanitized: string, error?: string}}
 */
function validateBookTitle(title) {
    if (!title || typeof title !== "string") {
        return { valid: false, sanitized: "", error: "书名不能为空" };
    }
    
    // 先检查是否包含危险字符
    if (containsDangerousChars(title)) {
        return { valid: false, sanitized: "", error: "书名包含非法字符" };
    }
    
    const sanitized = sanitizeString(title, 100);
    
    if (sanitized.length === 0) {
        return { valid: false, sanitized: "", error: "书名包含非法字符或为空" };
    }
    
    if (sanitized.length < 1) {
        return { valid: false, sanitized: "", error: "书名太短" };
    }
    
    return { valid: true, sanitized };
}

/**
 * 验证作者/出版社名称
 * @param {string} name - 名称
 * @returns {{valid: boolean, sanitized: string, error?: string}}
 */
function validateName(name) {
    if (!name) {
        return { valid: true, sanitized: "" };
    }
    
    if (typeof name !== "string") {
        return { valid: false, sanitized: "", error: "名称格式错误" };
    }
    
    // 先检查是否包含危险字符
    if (containsDangerousChars(name)) {
        return { valid: false, sanitized: "", error: "名称包含非法字符" };
    }
    
    const sanitized = sanitizeString(name, 50);
    
    return { valid: true, sanitized };
}

/**
 * 验证过滤器对象
 * @param {object} filters - 过滤器
 * @returns {{valid: boolean, sanitized: object, errors: string[]}}
 */
function validateFilters(filters) {
    const result = { valid: true, sanitized: {}, errors: [] };
    
    if (!filters || typeof filters !== "object") {
        return result;
    }
    
    // 允许的字段
    const allowedFields = ["author", "publisher", "language"];
    
    for (const [key, value] of Object.entries(filters)) {
        if (!allowedFields.includes(key)) {
            result.errors.push("不允许的字段: " + key);
            continue;
        }
        
        const nameResult = validateName(value);
        if (nameResult.valid && nameResult.sanitized) {
            result.sanitized[key] = nameResult.sanitized;
        } else if (!nameResult.valid) {
            result.errors.push(key + ": " + nameResult.error);
        }
    }
    
    result.valid = result.errors.length === 0;
    return result;
}

/**
 * 验证文件路径安全性
 * @param {string} filePath - 文件路径
 * @returns {{valid: boolean, sanitized: string, error?: string}}
 */
function validateFilePath(filePath) {
    if (!filePath || typeof filePath !== "string") {
        return { valid: false, sanitized: "", error: "文件路径不能为空" };
    }
    
    const path = require("path");
    const os = require("os");
    
    // 标准化路径
    let normalized = path.normalize(filePath);
    
    // 检查路径遍历攻击
    if (normalized.includes("..")) {
        return { valid: false, sanitized: "", error: "路径不能包含 .." };
    }
    
    // 检查绝对路径是否在允许的目录内
    const allowedDirs = [
        os.tmpdir(),
        path.join(os.homedir(), ".config", "kindle-download"),
        path.join(os.tmpdir(), "kindle_downloads")
    ];
    
    const resolved = path.resolve(normalized);
    const isAllowed = allowedDirs.some(dir => {
        const resolvedDir = path.resolve(dir);
        return resolved.startsWith(resolvedDir);
    });
    
    if (!isAllowed) {
        return { valid: false, sanitized: "", error: "文件路径不在允许的目录内" };
    }
    
    // 检查文件扩展名
    const ext = path.extname(normalized).toLowerCase();
    const allowedExts = [".epub", ".pdf", ".mobi", ".azw3"];
    
    if (!allowedExts.includes(ext)) {
        return { valid: false, sanitized: "", error: "不支持的文件类型: " + ext };
    }
    
    return { valid: true, sanitized: resolved };
}

module.exports = {
    sanitizeString,
    validateBookTitle,
    validateName,
    validateFilters,
    validateFilePath,
    containsDangerousChars,
    DANGEROUS_SHELL_CHARS
};
