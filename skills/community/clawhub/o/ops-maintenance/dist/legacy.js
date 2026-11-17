"use strict";
/**
 * 向后兼容导出层
 * 提供与旧版 ops-maintenance 完全相同的导出函数
 *
 * 旧版模块使用方式：
 *   const { loadServers, addServer, checkAllServersHealth, ... } = require('./dist/index')
 *
 * 新版通过此适配器透明地使用新架构
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.loadServers = loadServers;
exports.loadServerState = loadServerState;
exports.saveServerState = saveServerState;
exports.calculateServerChecksums = calculateServerChecksums;
exports.detectNewServers = detectNewServers;
exports.addServer = addServer;
exports.removeServer = removeServer;
exports.getServersByTag = getServersByTag;
exports.checkAllServersHealth = checkAllServersHealth;
exports.executeOnAllServers = executeOnAllServers;
exports.batchAddServers = batchAddServers;
exports.importServersFromText = importServersFromText;
exports.checkAllServersPasswordExpiration = checkAllServersPasswordExpiration;
exports.checkAllServersPasswordExpirationReport = checkAllServersPasswordExpirationReport;
exports.getClusterSummary = getClusterSummary;
exports.runRemoteCommand = runRemoteCommand;
exports.runCommand = runCommand;
exports.checkRemoteHealth = checkRemoteHealth;
exports.checkRemotePort = checkRemotePort;
exports.checkRemoteProcess = checkRemoteProcess;
exports.checkRemoteDisk = checkRemoteDisk;
exports.checkRemotePerformance = checkRemotePerformance;
exports.checkRemoteLogs = checkRemoteLogs;
exports.executeOp = executeOp;
exports.executeRemoteOp = executeRemoteOp;
exports.getContainer = getContainer;
exports.initContainer = initContainer;
exports.createApp = createApp;
const LegacyAdapter_1 = require("./presentation/LegacyAdapter");
// 创建全局适配器实例
let adapter = null;
// 延迟初始化适配器
async function getAdapter() {
    if (!adapter) {
        adapter = new LegacyAdapter_1.LegacyAdapter();
        await adapter.init();
    }
    return adapter;
}
/**
 * 加载服务器列表
 * @deprecated 建议使用 Container + Repository 模式
 */
async function loadServers() {
    const a = await getAdapter();
    return a.loadServers();
}
/**
 * 加载服务器状态追踪
 * @deprecated 内部使用
 */
async function loadServerState() {
    // 简化实现，返回 null
    return null;
}
/**
 * 保存服务器状态追踪
 * @deprecated 内部使用
 */
async function saveServerState(state) {
    // 简化实现，不做操作
}
/**
 * 计算服务器列表的校验和数组
 * @deprecated 内部使用
 */
function calculateServerChecksums(servers) {
    return servers.map(s => `${s.host}:${s.port || 22}:${s.user || 'root'}`).sort();
}
/**
 * 检测新增服务器
 * @deprecated 内部使用
 */
async function detectNewServers() {
    const a = await getAdapter();
    return a.detectNewServers();
}
/**
 * 添加服务器
 * @deprecated 建议使用 ServerRepository.add()
 */
async function addServer(config) {
    const a = await getAdapter();
    return a.addServer(config);
}
/**
 * 移除服务器
 * @deprecated 建议使用 ServerRepository.remove()
 */
async function removeServer(host) {
    const a = await getAdapter();
    return a.removeServer(host);
}
/**
 * 按标签筛选服务器
 * @deprecated 建议使用 ServerRepository.findByTags()
 */
async function getServersByTag(tag) {
    const a = await getAdapter();
    return a.getServersByTag(tag);
}
/**
 * 批量检查所有服务器健康状态
 */
async function checkAllServersHealth(tags, serverList) {
    const a = await getAdapter();
    return a.checkAllServersHealth(tags, serverList);
}
/**
 * 批量执行命令到所有服务器
 */
async function executeOnAllServers(command, tags) {
    const a = await getAdapter();
    return a.executeOnAllServers(command, tags);
}
/**
 * 批量添加服务器
 */
async function batchAddServers(servers) {
    const a = await getAdapter();
    return a.batchAddServers(servers);
}
/**
 * 从文本批量导入服务器
 */
async function importServersFromText(text) {
    const a = await getAdapter();
    return a.importServersFromText(text);
}
/**
 * 批量检查所有服务器密码过期状态
 */
async function checkAllServersPasswordExpiration(tags) {
    const a = await getAdapter();
    return a.checkAllServersPasswordExpiration(tags);
}
/**
 * 生成密码过期检查报告
 */
async function checkAllServersPasswordExpirationReport(tags) {
    const a = await getAdapter();
    return a.checkAllServersPasswordExpirationReport(tags);
}
/**
 * 获取集群摘要
 */
async function getClusterSummary() {
    const a = await getAdapter();
    return a.getClusterSummary();
}
/**
 * 远程命令执行
 */
async function runRemoteCommand(config, command) {
    const a = await getAdapter();
    return a.runRemoteCommand(config, command);
}
/**
 * 本地命令执行
 */
async function runCommand(cmd, timeout) {
    const a = await getAdapter();
    return a.runCommand(cmd, timeout);
}
/**
 * 远程服务器健康检查
 */
async function checkRemoteHealth(config, services) {
    const a = await getAdapter();
    return a.checkRemoteHealth(config, services);
}
/**
 * 远程服务器端口检查
 * @deprecated 未完全实现
 */
async function checkRemotePort(config, port) {
    return `端口检查功能尚未完全实现`;
}
/**
 * 远程服务器进程检查
 * @deprecated 未完全实现
 */
async function checkRemoteProcess(config, name) {
    return `进程检查功能尚未完全实现`;
}
/**
 * 远程服务器磁盘检查
 */
async function checkRemoteDisk(config) {
    const a = await getAdapter();
    // 使用 DiskCheckUseCase 实现
    // 简化：返回占位符
    return `磁盘检查: ${config.host}`;
}
/**
 * 远程服务器性能检查
 * @deprecated 未完全实现
 */
async function checkRemotePerformance(config) {
    return `性能检查功能尚未完全实现`;
}
/**
 * 远程服务器日志检查
 * @deprecated 未完全实现
 */
async function checkRemoteLogs(config, pattern, lines) {
    return `日志检查功能尚未完全实现`;
}
/**
 * 本地运维操作
 */
async function executeOp(action, arg) {
    const a = await getAdapter();
    return a.executeOp(action, arg);
}
/**
 * 远程运维操作
 */
async function executeRemoteOp(action, config, arg) {
    const a = await getAdapter();
    return a.executeRemoteOp(action, config, arg);
}
// ============ 新增：高级 API（新架构）============
/**
 * 获取容器实例（新 API）
 */
function getContainer() {
    return require('./container').getContainer();
}
/**
 * 初始化容器（新 API）
 */
async function initContainer(options) {
    return require('./container').initContainer(options);
}
/**
 * 创建 OpsMaintenanceApp（新 API）
 */
function createApp(config) {
    return new (require('./index').OpsMaintenanceApp)(config);
}
//# sourceMappingURL=legacy.js.map