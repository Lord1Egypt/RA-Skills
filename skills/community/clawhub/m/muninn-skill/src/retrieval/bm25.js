"use strict";
/**
 * BM25 Retrieval Implementation
 *
 * Sparse retrieval using Okapi BM25 ranking function.
 * Complements dense (semantic) search with exact term matching.
 */
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.BM25Scorer = void 0;
exports.bm25Search = bm25Search;
/**
 * Default BM25 parameters
 */
var DEFAULT_K1 = 1.5;
var DEFAULT_B = 0.75;
/**
 * BM25 Scorer class
 */
var BM25Scorer = /** @class */ (function () {
    function BM25Scorer(options) {
        if (options === void 0) { options = {}; }
        var _a, _b, _c;
        this.idf = new Map();
        this.docLengths = new Map();
        this.docTermFreqs = new Map();
        this.k1 = (_a = options.k1) !== null && _a !== void 0 ? _a : DEFAULT_K1;
        this.b = (_b = options.b) !== null && _b !== void 0 ? _b : DEFAULT_B;
        this.avgDocLen = (_c = options.avgDocLen) !== null && _c !== void 0 ? _c : 100; // Default estimate
    }
    /**
     * Index a corpus of documents
     */
    BM25Scorer.prototype.index = function (documents) {
        var docCount = documents.length;
        var termDocFreq = new Map(); // df - document frequency
        // First pass: collect document frequencies
        for (var _i = 0, documents_1 = documents; _i < documents_1.length; _i++) {
            var doc = documents_1[_i];
            var terms = this.tokenize(doc.content);
            var uniqueTerms = new Set(terms);
            this.docLengths.set(doc.id, terms.length);
            // Update average
            if (terms.length > 0) {
                this.avgDocLen = (this.avgDocLen + terms.length) / 2;
            }
            // Count document frequency for each unique term
            for (var _a = 0, uniqueTerms_1 = uniqueTerms; _a < uniqueTerms_1.length; _a++) {
                var term = uniqueTerms_1[_a];
                termDocFreq.set(term, (termDocFreq.get(term) || 0) + 1);
            }
        }
        // Second pass: build term frequency maps
        for (var _b = 0, documents_2 = documents; _b < documents_2.length; _b++) {
            var doc = documents_2[_b];
            var terms = this.tokenize(doc.content);
            var termFreqs = new Map();
            for (var _c = 0, terms_1 = terms; _c < terms_1.length; _c++) {
                var term = terms_1[_c];
                termFreqs.set(term, (termFreqs.get(term) || 0) + 1);
            }
            this.docTermFreqs.set(doc.id, termFreqs);
        }
        // Calculate IDF for each term
        for (var _d = 0, termDocFreq_1 = termDocFreq; _d < termDocFreq_1.length; _d++) {
            var _e = termDocFreq_1[_d], term = _e[0], df = _e[1];
            // IDF using standard BM25 formula
            var idf = Math.log((docCount - df + 0.5) / (df + 0.5) + 1);
            this.idf.set(term, idf);
        }
    };
    /**
     * Tokenize text into terms
     */
    BM25Scorer.prototype.tokenize = function (text) {
        return text
            .toLowerCase()
            .replace(/[^\w\s]/g, ' ')
            .split(/\s+/)
            .filter(function (term) { return term.length > 1; }); // Skip single chars
    };
    /**
     * Calculate BM25 score for a single document
     */
    BM25Scorer.prototype.scoreDocument = function (query, docId) {
        var queryTerms = this.tokenize(query);
        var termFreqs = this.docTermFreqs.get(docId);
        var docLen = this.docLengths.get(docId) || this.avgDocLen;
        if (!termFreqs)
            return 0;
        var score = 0;
        for (var _i = 0, queryTerms_1 = queryTerms; _i < queryTerms_1.length; _i++) {
            var term = queryTerms_1[_i];
            var tf = termFreqs.get(term) || 0;
            var idf = this.idf.get(term) || 0;
            // BM25 scoring formula
            var numerator = tf * (this.k1 + 1);
            var denominator = tf + this.k1 * (1 - this.b + this.b * (docLen / this.avgDocLen));
            score += idf * (numerator / denominator);
        }
        return score;
    };
    /**
     * Search documents using BM25
     */
    BM25Scorer.prototype.search = function (query, documents, k) {
        var _this = this;
        if (k === void 0) { k = 10; }
        // Re-index if needed (for simplicity, re-index each search)
        // In production, you'd want to cache this
        this.index(documents);
        // Score all documents
        var scores = documents.map(function (doc) { return ({
            doc: doc,
            score: _this.scoreDocument(query, doc.id)
        }); });
        // Sort by score descending
        scores.sort(function (a, b) { return b.score - a.score; });
        // Return top k
        return scores.slice(0, k).map(function (s) { return (__assign(__assign({}, s.doc), { _bm25Score: s.score })); });
    };
    return BM25Scorer;
}());
exports.BM25Scorer = BM25Scorer;
/**
 * Simple BM25 search function (convenience wrapper)
 */
function bm25Search(query, documents, options) {
    if (options === void 0) { options = {}; }
    var scorer = new BM25Scorer({
        k1: options.k1,
        b: options.b
    });
    return scorer.search(query, documents, options.k || 10);
}
