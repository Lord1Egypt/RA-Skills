"use strict";
/**
 * 输入验证工具
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.validateDigitalHumanId = validateDigitalHumanId;
exports.validateUserId = validateUserId;
exports.validateMessage = validateMessage;
exports.validateContentType = validateContentType;
exports.validateWebSocketUrl = validateWebSocketUrl;
exports.validateMediaUrl = validateMediaUrl;
exports.validateDuration = validateDuration;
exports.sanitizeString = sanitizeString;
const constants_1 = require("./constants");
/**
 * 验证数字人ID
 */
function validateDigitalHumanId(id) {
    if (!id || typeof id !== 'string') {
        return { valid: false, error: 'Digital human ID is required' };
    }
    if (id.length < constants_1.VALIDATION_CONFIG.DIGITAL_HUMAN_ID_MIN) {
        return { valid: false, error: 'Digital human ID is too short' };
    }
    if (id.length > constants_1.VALIDATION_CONFIG.DIGITAL_HUMAN_ID_MAX) {
        return { valid: false, error: 'Digital human ID is too long' };
    }
    return { valid: true };
}
/**
 * 验证用户ID
 */
function validateUserId(id) {
    if (!id || typeof id !== 'string') {
        return { valid: false, error: 'User ID is required' };
    }
    if (id.length < constants_1.VALIDATION_CONFIG.USER_ID_MIN) {
        return { valid: false, error: 'User ID is too short' };
    }
    if (id.length > constants_1.VALIDATION_CONFIG.USER_ID_MAX) {
        return { valid: false, error: 'User ID is too long' };
    }
    return { valid: true };
}
/**
 * 验证消息内容
 */
function validateMessage(content) {
    if (!content || typeof content !== 'string') {
        return { valid: false, error: 'Message content is required' };
    }
    if (content.trim().length === 0) {
        return { valid: false, error: 'Message cannot be empty' };
    }
    return { valid: true };
}
/**
 * 验证内容类型
 */
function validateContentType(type) {
    const validTypes = Object.values(constants_1.CONTENT_TYPES);
    if (!validTypes.includes(type)) {
        return {
            valid: false,
            error: `Invalid content type. Must be one of: ${validTypes.join(', ')}`
        };
    }
    return { valid: true };
}
/**
 * 验证 WebSocket URL
 */
function validateWebSocketUrl(url) {
    if (!url || typeof url !== 'string') {
        return { valid: false, error: 'WebSocket URL is required' };
    }
    try {
        const parsed = new URL(url);
        if (parsed.protocol !== 'ws:' && parsed.protocol !== 'wss:') {
            return { valid: false, error: 'URL must use ws:// or wss:// protocol' };
        }
        return { valid: true };
    }
    catch {
        return { valid: false, error: 'Invalid URL format' };
    }
}
/**
 * 验证媒体 URL
 */
function validateMediaUrl(url) {
    if (!url || typeof url !== 'string') {
        return { valid: false, error: 'Media URL is required' };
    }
    try {
        new URL(url);
        return { valid: true };
    }
    catch {
        return { valid: false, error: 'Invalid media URL format' };
    }
}
/**
 * 验证语音时长
 */
function validateDuration(duration) {
    if (typeof duration !== 'number' || isNaN(duration)) {
        return { valid: false, error: 'Duration must be a number' };
    }
    if (duration <= 0) {
        return { valid: false, error: 'Duration must be greater than 0' };
    }
    if (duration > 300) { // 最大5分钟
        return { valid: false, error: 'Duration cannot exceed 300 seconds (5 minutes)' };
    }
    return { valid: true };
}
/**
 * 清理字符串（防止 XSS）
 */
function sanitizeString(input) {
    if (!input || typeof input !== 'string') {
        return '';
    }
    return input
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;')
        .replace(/\//g, '&#x2F;');
}
//# sourceMappingURL=validator.js.map