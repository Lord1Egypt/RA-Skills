"use strict";
/**
 * 智能搜索类型定义
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ENGINE_LABELS = exports.ENGINE_QUOTAS = exports.ENGINE_PRIORITIES = void 0;
exports.ENGINE_PRIORITIES = {
    bailian: 1,
    tavily: 2,
    serper: 3,
    exa: 4,
    firecrawl: 5
};
exports.ENGINE_QUOTAS = {
    bailian: 2000,
    tavily: 1000,
    serper: 2500,
    exa: 1000,
    firecrawl: 500
};
exports.ENGINE_LABELS = {
    bailian: '百炼 MCP',
    tavily: 'Tavily',
    serper: 'Serper',
    exa: 'Exa',
    firecrawl: 'Firecrawl'
};
//# sourceMappingURL=types.js.map