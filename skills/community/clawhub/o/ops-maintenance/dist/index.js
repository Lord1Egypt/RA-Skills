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
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.initLegacyAdapter = exports.LegacyAdapter = exports.OpsMaintenanceApp = exports.Container = exports.ServerStatus = exports.Server = void 0;
// 重新导出旧版兼容 API（保持向后兼容）
__exportStar(require("./legacy"), exports);
var schemas_1 = require("./config/schemas");
Object.defineProperty(exports, "Server", { enumerable: true, get: function () { return schemas_1.Server; } });
Object.defineProperty(exports, "ServerStatus", { enumerable: true, get: function () { return schemas_1.ServerStatus; } });
var container_1 = require("./container");
Object.defineProperty(exports, "Container", { enumerable: true, get: function () { return container_1.Container; } });
var index_1 = require("./index");
Object.defineProperty(exports, "OpsMaintenanceApp", { enumerable: true, get: function () { return index_1.OpsMaintenanceApp; } });
var LegacyAdapter_1 = require("./presentation/LegacyAdapter");
Object.defineProperty(exports, "LegacyAdapter", { enumerable: true, get: function () { return LegacyAdapter_1.LegacyAdapter; } });
Object.defineProperty(exports, "initLegacyAdapter", { enumerable: true, get: function () { return LegacyAdapter_1.initLegacyAdapter; } });
//# sourceMappingURL=index.js.map