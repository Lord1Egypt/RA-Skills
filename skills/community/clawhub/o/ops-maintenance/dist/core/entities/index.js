"use strict";
/**
 * 领域实体导出
 * 从 config 层重新导出核心实体
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ServerStatus = exports.Server = void 0;
var schemas_1 = require("../../config/schemas");
Object.defineProperty(exports, "Server", { enumerable: true, get: function () { return schemas_1.Server; } });
Object.defineProperty(exports, "ServerStatus", { enumerable: true, get: function () { return schemas_1.ServerStatus; } });
//# sourceMappingURL=index.js.map