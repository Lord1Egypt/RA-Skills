/**
 * 飞书 API 工具函数
 * 
 * 内部封装：
 * - Token 缓存 + 提前刷新
 * - 统一超时控制
 * - 401 自动重试
 * 
 * 外部脚本应使用 request.js 的 apiGet / apiPost / apiPut
 */

const { getAccessToken } = require('./request');

module.exports = { getAccessToken };