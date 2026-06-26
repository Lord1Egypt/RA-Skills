#!/usr/bin/env node
/**
 * QMD CLI Wrapper - 兼容 OpenClaw 的 QMD 后端调用
 * 模拟官方 QMD CLI 接口，实际使用 BM25 检索
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

function parseArgs(args) {
    const result = { command: null, query: null, limit: 6, json: false, collection: 'memory-root' };
    let i = 0;
    while (i < args.length) {
        const arg = args[i];
        if (arg === 'search' || arg === 'query' || arg === 'vsearch') {
            result.command = arg;
        } else if (arg === '-c' || arg === '--collection') {
            result.collection = args[++i];
        } else if (arg === '-n' || arg === '--limit') {
            result.limit = parseInt(args[++i]);
        } else if (arg === '--json') {
            result.json = true;
        } else if (arg.startsWith('-') === false && result.command) {
            result.query = arg;
        }
        i++;
    }
    return result;
}

function formatResult(doc, idx) {
    const dateMatch = doc.path.match(/memory\/(\d{4}-\d{2}-\d{2})\.md/);
    const date = dateMatch ? dateMatch[1] : null;
    
    return {
        id: `${doc.path}:${idx}`,
        path: doc.path,
        text: doc.content,
        score: doc.score,
        metadata: {
            type: doc.metadata?.type || 'memory',
            date,
            collection: 'memory-root'
        }
    };
}

function main() {
    const args = process.argv.slice(2);
    
    // 处理 help
    if (args.includes('--help') || args.includes('-h')) {
        console.log(`QMD CLI (BM25 Wrapper)
        
Usage: qmd <command> [query] [options]

Commands:
  search, query, vsearch    Search memory files
  update                    Update index (rebuild)
  embed                     Embed documents (no-op for BM25)
  collection                Manage collections

Options:
  -c, --collection <name>   Collection name (default: memory-root)
  -n, --limit <num>         Max results (default: 6)
  --json                    Output as JSON
  --help, -h                Show this help
`);
        process.exit(0);
    }
    
    // 处理 collection 命令
    if (args[0] === 'collection') {
        console.log('[]');
        process.exit(0);
    }
    
    // 处理 update/embed 命令 (no-op)
    if (args[0] === 'update' || args[0] === 'embed') {
        console.log('OK');
        process.exit(0);
    }
    
    const opts = parseArgs(args);
    
    if (!opts.command || !opts.query) {
        console.error('Usage: qmd <search|query> <query-text> [--json] [-n <limit>]');
        process.exit(1);
    }
    
    const workspace = process.env.WORKSPACE || '/Users/ben/.openclaw/workspace';
    const indexPath = path.join(workspace, 'qmd-index', 'bm25-index.json');
    
    if (!fs.existsSync(indexPath)) {
        if (opts.json) {
            console.log(JSON.stringify({ error: 'Index not found', results: [] }));
        } else {
            console.error('Index not found. Run: node qmd-index.js');
        }
        process.exit(1);
    }
    
    const searcher = new BM25Searcher(indexPath);
    const results = searcher.search(opts.query, opts.limit);
    
    const formattedResults = results.map((r, i) => formatResult(r, i));
    
    if (opts.json) {
        console.log(JSON.stringify({
            query: opts.query,
            collection: opts.collection,
            limit: opts.limit,
            total: formattedResults.length,
            results: formattedResults
        }, null, 2));
    } else {
        formattedResults.forEach((r, i) => {
            console.log(`\n[${i + 1}] ${r.path} (score: ${r.score.toFixed(4)})`);
            console.log(r.text.substring(0, 200) + '...');
        });
    }
}

main();
