"use strict";
/**
 * Cross-Encoder Reranking
 *
 * Uses a cross-encoder model to rerank retrieval results
 * for better precision. Cross-encoders jointly encode query+document,
 * providing more accurate relevance scores than separate encoding.
 */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.rerankWithCrossEncoder = rerankWithCrossEncoder;
exports.lightweightRerank = lightweightRerank;
exports.setRerankerModel = setRerankerModel;
var transformers_1 = require("@xenova/transformers");
// Skip model download warnings
transformers_1.env.allowLocalModels = false;
transformers_1.env.useBrowserCache = true;
// Singleton reranker instance
var rerankerInstance = null;
var rerankerModel = 'cross-encoder/ms-marco-MiniLM-L-6-v2';
/**
 * Get or initialize the reranker
 */
function getReranker() {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (!!rerankerInstance) return [3 /*break*/, 2];
                    console.log('🔄 Loading cross-encoder reranker...');
                    return [4 /*yield*/, (0, transformers_1.pipeline)('feature-extraction', rerankerModel, {
                            quantized: true,
                        })];
                case 1:
                    rerankerInstance = _a.sent();
                    console.log('✅ Cross-encoder reranker loaded');
                    _a.label = 2;
                case 2: return [2 /*return*/, rerankerInstance];
            }
        });
    });
}
/**
 * Rerank documents using cross-encoder
 *
 * @param query - Search query
 * @param documents - Documents to rerank
 * @param topK - Number of top results to return
 * @returns Reranked documents with scores
 */
function rerankWithCrossEncoder(query_1, documents_1) {
    return __awaiter(this, arguments, void 0, function (query, documents, topK) {
        var reranker, pairs, outputs_1, scored, error_1;
        if (topK === void 0) { topK = 10; }
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (documents.length === 0)
                        return [2 /*return*/, []];
                    if (documents.length === 1) {
                        return [2 /*return*/, [{ doc: documents[0], score: 1.0 }]];
                    }
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 4, , 5]);
                    return [4 /*yield*/, getReranker()];
                case 2:
                    reranker = _a.sent();
                    pairs = documents.map(function (doc) { return "[CLS] ".concat(query, " [SEP] ").concat(doc.content, " [SEP]"); });
                    return [4 /*yield*/, reranker(pairs, {
                            pooling: 'mean',
                            normalize: true,
                        })];
                case 3:
                    outputs_1 = _a.sent();
                    scored = documents.map(function (doc, i) {
                        var _a;
                        return ({
                            doc: doc,
                            score: typeof outputs_1[i] === 'number' ? outputs_1[i] : ((_a = outputs_1[i].data) === null || _a === void 0 ? void 0 : _a[0]) || 0
                        });
                    });
                    scored.sort(function (a, b) { return b.score - a.score; });
                    return [2 /*return*/, scored.slice(0, topK)];
                case 4:
                    error_1 = _a.sent();
                    console.warn('Cross-encoder reranking failed:', error_1);
                    // Fallback: return original order with uniform scores
                    return [2 /*return*/, documents.map(function (doc) { return ({ doc: doc, score: 1.0 }); })];
                case 5: return [2 /*return*/];
            }
        });
    });
}
/**
 * Lightweight reranking using simpler method
 * Useful when cross-encoder is too slow
 */
function lightweightRerank(query, documents, topK) {
    if (topK === void 0) { topK = 10; }
    var queryTerms = new Set(query.toLowerCase().split(/\s+/).filter(function (t) { return t.length > 2; }));
    var scored = documents.map(function (doc) {
        var contentTerms = doc.content.toLowerCase().split(/\s+/);
        var matches = 0;
        var positionBonus = 0;
        for (var i = 0; i < contentTerms.length; i++) {
            if (queryTerms.has(contentTerms[i])) {
                matches++;
                // Earlier matches get higher bonus
                positionBonus += 1 / (i + 1);
            }
        }
        var termScore = matches / Math.max(queryTerms.size, 1);
        var positionScore = positionBonus / Math.max(queryTerms.size, 1);
        return {
            doc: doc,
            score: termScore * 0.7 + positionScore * 0.3
        };
    });
    scored.sort(function (a, b) { return b.score - a.score; });
    return scored.slice(0, topK);
}
/**
 * Set custom reranker model
 */
function setRerankerModel(model) {
    rerankerModel = model;
    // Reset instance to load new model
    rerankerInstance = null;
}
