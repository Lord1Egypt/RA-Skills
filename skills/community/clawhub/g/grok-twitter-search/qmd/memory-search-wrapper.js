#!/usr/bin/env node
/**
 * QMD Memory Search - OpenClaw memory_search 工具的直接替代品
 * 输出格式兼容 OpenClaw 的 memory_search 期望格式
 */

const fs = require('fs');
const path = require('path');

class BM25Searcher {
    constructor(indexPath) {
        const data = JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
        this.documents = data.documents;
        this.avgDocLength = data.avgDocLength;
        this.idf = new Map(Object.entries(data.idf));
        this.termFreqs = data.termFreqs.map(tf => new Map(Object.entries(tf)));
        this.docLengths = data.docLengths;
        this.k1 = 1.5;
        this.b = 0.75;
    }

    tokenize(text) {
        return text.toLowerCase()
            .replace(/[^\w\s\u4e00-\u9fff]/g, ' ')
            .split(/\s+/)
            .filter(w => w.length > 1);
    }

    search(query, limit = 5) {
        const queryTokens = this.tokenize(query);
        const scores = new Array(this.documents.length).fill(0);

        queryTokens.forEach(term => {
            const idf = this.idf.get(term) || 0;
            if (idf === 0) return;

            this.termFreqs.forEach((tf, docIdx) => {
                const freq = tf.get(term) || 0;
                if (freq === 0) return;

                const docLen = this.docLengths[docIdx];
                const score = idf * (freq * (this.k1 + 1)) /
                    (freq + this.k1 * (1 - this.b + this.b * docLen / this.avgDocLength));
                scores[docIdx] += score;
            });
        });

        return scores
            .map((score, idx) => ({ ...this.documents[idx], score }))
            .filter(r => r.score > 0)
            .sort((a, b) => b.score - a.score)
            .slice(0, limit);
    }
}

function formatMemorySnippet(doc) {
    return {
        path: doc.path,
        content: doc.content,
        score: doc.score,
        type: doc.metadata?.type || 'unknown'
    };
}

function searchMemories(query, limit = 5, minScore = 0) {
    const workspace = process.env.WORKSPACE || '/Users/ben/.openclaw/workspace';
    const indexPath = path.join(workspace, 'qmd-index', 'bm25-index.json');

    // 如果索引不存在，返回空结果
    if (!fs.existsSync(indexPath)) {
        return {
            query,
            disabled: false,
            message: 'QMD 索引不存在，请先运行 qmd-index.js 创建索引',
            results: []
        };
    }

    const searcher = new BM25Searcher(indexPath);
    const results = searcher.search(query, limit);

    // 过滤低于最小分数的结果
    const filteredResults = results.filter(r => r.score >= minScore);

    // 格式化为 OpenClaw memory_search 兼容格式
    const snippets = filteredResults.map(doc => {
        const lines = doc.content.split('\n');
        return {
            path: doc.path,
            lines: lines.length,
            content: doc.content,
            score: doc.score,
            type: doc.metadata?.type || 'unknown'
        };
    });

    return {
        query,
        limit,
        minScore,
        totalFound: snippets.length,
        disabled: false,
        results: snippets
    };
}

// 从环境变量或命令行获取参数
const query = process.env.QMD_QUERY || process.argv[2];
const limit = parseInt(process.env.QMD_LIMIT || process.argv[3]) || 5;
const minScore = parseFloat(process.env.QMD_MINSCORE || process.argv[4]) || 0;

if (!query) {
    console.log(JSON.stringify({
        error: '请提供查询文本',
        usage: 'memory-search-wrapper.js <query> [limit] [minScore]',
        envUsage: 'QMD_QUERY="xxx" QMD_LIMIT=5 node memory-search-wrapper.js'
    }));
    process.exit(1);
}

const result = searchMemories(query, limit, minScore);
console.log(JSON.stringify(result, null, 2));
