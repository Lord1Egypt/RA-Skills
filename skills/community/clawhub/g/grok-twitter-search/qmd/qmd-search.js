#!/usr/bin/env node
/**
 * QMD - 记忆检索 (BM25 全文检索)
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

function searchMemories(query, limit = 5) {
    const workspace = process.env.WORKSPACE || '/Users/ben/.openclaw/workspace';
    const indexPath = path.join(workspace, 'qmd-index', 'bm25-index.json');

    if (!fs.existsSync(indexPath)) {
        console.log(JSON.stringify({
            error: '索引不存在',
            message: '请先运行 qmd-index.js 创建索引',
            results: []
        }));
        return;
    }

    const searcher = new BM25Searcher(indexPath);
    const results = searcher.search(query, limit);

    const formattedResults = results.map((r, i) => ({
        rank: i + 1,
        path: r.path,
        content: r.content,
        score: r.score,
        metadata: r.metadata
    }));

    console.log(JSON.stringify({
        query,
        limit,
        totalFound: formattedResults.length,
        results: formattedResults
    }, null, 2));
}

// 命令行参数
const args = process.argv.slice(2);
if (args.length === 0) {
    console.log(JSON.stringify({ error: '请提供查询文本', usage: 'qmd-search.js <查询文本> [limit]' }));
    process.exit(1);
}

const query = args[0];
const limit = parseInt(args[1]) || 5;
searchMemories(query, limit);
