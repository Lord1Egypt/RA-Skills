"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.FirecrawlEngine = exports.ExaEngine = exports.SerperEngine = exports.TavilyEngine = exports.BailianEngine = void 0;
exports.getEngine = getEngine;
exports.getAllEngines = getAllEngines;
const bailian_1 = require("./bailian");
Object.defineProperty(exports, "BailianEngine", { enumerable: true, get: function () { return bailian_1.BailianEngine; } });
const tavily_1 = require("./tavily");
Object.defineProperty(exports, "TavilyEngine", { enumerable: true, get: function () { return tavily_1.TavilyEngine; } });
const serper_1 = require("./serper");
Object.defineProperty(exports, "SerperEngine", { enumerable: true, get: function () { return serper_1.SerperEngine; } });
const exa_1 = require("./exa");
Object.defineProperty(exports, "ExaEngine", { enumerable: true, get: function () { return exa_1.ExaEngine; } });
const firecrawl_1 = require("./firecrawl");
Object.defineProperty(exports, "FirecrawlEngine", { enumerable: true, get: function () { return firecrawl_1.FirecrawlEngine; } });
function getEngine(name) {
    switch (name) {
        case 'bailian':
            return new bailian_1.BailianEngine();
        case 'tavily':
            return new tavily_1.TavilyEngine();
        case 'serper':
            return new serper_1.SerperEngine();
        case 'exa':
            return new exa_1.ExaEngine();
        case 'firecrawl':
            return new firecrawl_1.FirecrawlEngine();
        default:
            throw new Error(`Unknown engine: ${name}`);
    }
}
function getAllEngines() {
    return [
        new bailian_1.BailianEngine(),
        new tavily_1.TavilyEngine(),
        new serper_1.SerperEngine(),
        new exa_1.ExaEngine(),
        new firecrawl_1.FirecrawlEngine()
    ];
}
//# sourceMappingURL=index.js.map