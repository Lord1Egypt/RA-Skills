"use strict";
/**
 * 统一导出文件
 * 明确区分类型导出和值导出
 */
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
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.initLegacyAdapter = exports.getLegacyAdapter = exports.LegacyAdapter = exports.main = exports.AppConfig = exports.OpsMaintenanceApp = exports.initContainer = exports.getContainer = exports.Container = exports.CLI = exports.CommandParser = exports.JsonFormatter = exports.MarkdownFormatter = exports.DiskCheckUseCase = exports.PasswordCheckUseCase = exports.HealthCheckUseCase = exports.EnvironmentCredentialsProvider = exports.ConfigManagerCredentialsProvider = exports.createServerRepository = exports.ServerFileRepository = exports.ENV_THRESHOLDS = exports.DEFAULT_THRESHOLDS = exports.ThresholdChecker = exports.checkServices = exports.ServiceStatusCheck = exports.DiskCheck = exports.MemoryCheck = exports.LoadAverageCheck = exports.HealthChecker = exports.ConnectionPool = exports.SSHClient = exports.CacheFactory = exports.TieredCache = exports.FileCache = exports.MemoryCache = exports.ConfigValidationError = exports.ServerStatus = exports.Server = void 0;
// 值和类型导出（类和枚举）
var schemas_1 = require("./config/schemas");
Object.defineProperty(exports, "Server", { enumerable: true, get: function () { return schemas_1.Server; } });
Object.defineProperty(exports, "ServerStatus", { enumerable: true, get: function () { return schemas_1.ServerStatus; } });
// 接口（需要值导入，因为包含静态方法）
var validator_1 = require("./config/validator");
Object.defineProperty(exports, "ConfigValidationError", { enumerable: true, get: function () { return validator_1.ConfigValidationError; } });
// 实用工具类
var CacheRepository_1 = require("./infrastructure/cache/CacheRepository");
Object.defineProperty(exports, "MemoryCache", { enumerable: true, get: function () { return CacheRepository_1.MemoryCache; } });
Object.defineProperty(exports, "FileCache", { enumerable: true, get: function () { return CacheRepository_1.FileCache; } });
Object.defineProperty(exports, "TieredCache", { enumerable: true, get: function () { return CacheRepository_1.TieredCache; } });
Object.defineProperty(exports, "CacheFactory", { enumerable: true, get: function () { return CacheRepository_1.CacheFactory; } });
var SSHClient_1 = require("./infrastructure/ssh/SSHClient");
Object.defineProperty(exports, "SSHClient", { enumerable: true, get: function () { return SSHClient_1.SSHClient; } });
var ConnectionPool_1 = require("./infrastructure/ssh/ConnectionPool");
Object.defineProperty(exports, "ConnectionPool", { enumerable: true, get: function () { return ConnectionPool_1.ConnectionPool; } });
var HealthChecker_1 = require("./infrastructure/monitoring/HealthChecker");
Object.defineProperty(exports, "HealthChecker", { enumerable: true, get: function () { return HealthChecker_1.HealthChecker; } });
Object.defineProperty(exports, "LoadAverageCheck", { enumerable: true, get: function () { return HealthChecker_1.LoadAverageCheck; } });
Object.defineProperty(exports, "MemoryCheck", { enumerable: true, get: function () { return HealthChecker_1.MemoryCheck; } });
Object.defineProperty(exports, "DiskCheck", { enumerable: true, get: function () { return HealthChecker_1.DiskCheck; } });
Object.defineProperty(exports, "ServiceStatusCheck", { enumerable: true, get: function () { return HealthChecker_1.ServiceStatusCheck; } });
Object.defineProperty(exports, "checkServices", { enumerable: true, get: function () { return HealthChecker_1.checkServices; } });
var ThresholdChecker_1 = require("./infrastructure/monitoring/ThresholdChecker");
Object.defineProperty(exports, "ThresholdChecker", { enumerable: true, get: function () { return ThresholdChecker_1.ThresholdChecker; } });
Object.defineProperty(exports, "DEFAULT_THRESHOLDS", { enumerable: true, get: function () { return ThresholdChecker_1.DEFAULT_THRESHOLDS; } });
Object.defineProperty(exports, "ENV_THRESHOLDS", { enumerable: true, get: function () { return ThresholdChecker_1.ENV_THRESHOLDS; } });
var ServerFileRepository_1 = require("./infrastructure/repositories/ServerFileRepository");
Object.defineProperty(exports, "ServerFileRepository", { enumerable: true, get: function () { return ServerFileRepository_1.ServerFileRepository; } });
Object.defineProperty(exports, "createServerRepository", { enumerable: true, get: function () { return ServerFileRepository_1.createServerRepository; } });
var CredentialsRepository_1 = require("./infrastructure/repositories/CredentialsRepository");
Object.defineProperty(exports, "ConfigManagerCredentialsProvider", { enumerable: true, get: function () { return CredentialsRepository_1.ConfigManagerCredentialsProvider; } });
Object.defineProperty(exports, "EnvironmentCredentialsProvider", { enumerable: true, get: function () { return CredentialsRepository_1.EnvironmentCredentialsProvider; } });
// UseCases
var HealthCheckUseCase_1 = require("./core/usecases/HealthCheckUseCase");
Object.defineProperty(exports, "HealthCheckUseCase", { enumerable: true, get: function () { return HealthCheckUseCase_1.HealthCheckUseCase; } });
var PasswordCheckUseCase_1 = require("./core/usecases/PasswordCheckUseCase");
Object.defineProperty(exports, "PasswordCheckUseCase", { enumerable: true, get: function () { return PasswordCheckUseCase_1.PasswordCheckUseCase; } });
var DiskCheckUseCase_1 = require("./core/usecases/DiskCheckUseCase");
Object.defineProperty(exports, "DiskCheckUseCase", { enumerable: true, get: function () { return DiskCheckUseCase_1.DiskCheckUseCase; } });
// Presentation
var MarkdownFormatter_1 = require("./presentation/formatters/MarkdownFormatter");
Object.defineProperty(exports, "MarkdownFormatter", { enumerable: true, get: function () { return MarkdownFormatter_1.MarkdownFormatter; } });
var JsonFormatter_1 = require("./presentation/formatters/JsonFormatter");
Object.defineProperty(exports, "JsonFormatter", { enumerable: true, get: function () { return JsonFormatter_1.JsonFormatter; } });
var CommandDispatcher_1 = require("./presentation/cli/CommandDispatcher");
Object.defineProperty(exports, "CommandParser", { enumerable: true, get: function () { return CommandDispatcher_1.CommandParser; } });
var CLI_1 = require("./presentation/cli/CLI");
Object.defineProperty(exports, "CLI", { enumerable: true, get: function () { return CLI_1.CLI; } });
// Container
var container_1 = require("./container");
Object.defineProperty(exports, "Container", { enumerable: true, get: function () { return container_1.Container; } });
Object.defineProperty(exports, "getContainer", { enumerable: true, get: function () { return container_1.getContainer; } });
Object.defineProperty(exports, "initContainer", { enumerable: true, get: function () { return container_1.initContainer; } });
// App
var index_1 = require("./index");
Object.defineProperty(exports, "OpsMaintenanceApp", { enumerable: true, get: function () { return index_1.OpsMaintenanceApp; } });
Object.defineProperty(exports, "AppConfig", { enumerable: true, get: function () { return index_1.AppConfig; } });
Object.defineProperty(exports, "main", { enumerable: true, get: function () { return index_1.main; } });
// Legacy
var LegacyAdapter_1 = require("./presentation/LegacyAdapter");
Object.defineProperty(exports, "LegacyAdapter", { enumerable: true, get: function () { return LegacyAdapter_1.LegacyAdapter; } });
Object.defineProperty(exports, "getLegacyAdapter", { enumerable: true, get: function () { return LegacyAdapter_1.getLegacyAdapter; } });
Object.defineProperty(exports, "initLegacyAdapter", { enumerable: true, get: function () { return LegacyAdapter_1.initLegacyAdapter; } });
// 向后兼容（旧版 API）
__exportStar(require("./legacy"), exports);
//# sourceMappingURL=exports.js.map