#!/usr/bin/env node
/**
 * QMD - 本地记忆索引系统 (BM25 全文检索)
 * 无需向量模型，纯本地全文检索
 */

const fs = require('fs');
const path = require('path');

// 简单的 BM25 实现
class BM25 {
    constructor(k1 = 1.5, b = 0.75) {
        this.k1 = k1;
        this.b = b;
        this.documents = [];
        this.avgDocLength = 0;
        this.termFreqs = [];
        this.docLengths = [];
        this.idf = new Map();
    }

    tokenize(text) {
        return text.toLowerCase()
            .replace(/[^\w\s\u4e00-\u9fff]/g, ' ')
            .split(/\s+/)
            .filter(w => w.length > 1);
    }

    index(documents) {
        this.documents = documents;
        this.termFreqs = [];
        this.docLengths = [];
        const df = new Map();

        documents.forEach((doc, idx) => {
            const tokens = this.tokenize(doc.content);
            this.docLengths.push(tokens.length);
            const tf = new Map();
            tokens.forEach(term => {
                tf.set(term, (tf.get(term) || 0) + 1);
                if (!df.has(term)) df.set(term, new Set());
                df.get(term).add(idx);
            });
            this.termFreqs.push(tf);
        });

        this.avgDocLength = this.docLengths.reduce((a, b) => a + b, 0) / documents.length;

        // 计算 IDF
        const N = documents.length;
        df.forEach((docSet, term) => {
            this.idf.set(term, Math.log((N - df.get(term).size + 0.5) / (df.get(term).size + 0.5) + 1));
        });

        return this;
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

        // 返回 top-k
        return scores
            .map((score, idx) => ({ ...this.documents[idx], score }))
            .filter(r => r.score > 0)
            .sort((a, b) => b.score - a.score)
            .slice(0, limit);
    }
}

async function buildIndex() {
    const workspace = process.env.WORKSPACE || '/Users/ben/.openclaw/workspace';
    const memoryDir = path.join(workspace, 'memory');
    const qmdDir = path.join(workspace, 'qmd-index');

    console.log('📂 工作目录:', workspace);
    console.log('📂 记忆目录:', memoryDir);
    console.log('📂 QMD 索引目录:', qmdDir);

    // 确保目录存在
    if (!fs.existsSync(qmdDir)) {
        fs.mkdirSync(qmdDir, { recursive: true });
    }

    // 收集所有记忆片段
    const documents = [];

    // 读取 MEMORY.md
    const memoryFile = path.join(workspace, 'MEMORY.md');
    if (fs.existsSync(memoryFile)) {
        const content = fs.readFileSync(memoryFile, 'utf-8');
        const chunks = chunkText(content, 500);
        chunks.forEach((chunk, i) => {
            documents.push({
                id: `memory-main-${i}`,
                path: 'MEMORY.md',
                content: chunk,
                metadata: { type: 'long-term', chunk: i }
            });
        });
        console.log(`✅ MEMORY.md: ${chunks.length} 个片段`);
    }

    // 读取 memory/*.md
    if (fs.existsSync(memoryDir)) {
        const files = fs.readdirSync(memoryDir).filter(f => f.endsWith('.md'));
        for (const file of files) {
            const filePath = path.join(memoryDir, file);
            const content = fs.readFileSync(filePath, 'utf-8');
            const chunks = chunkText(content, 500);
            chunks.forEach((chunk, i) => {
                documents.push({
                    id: `memory-daily-${file}-${i}`,
                    path: `memory/${file}`,
                    content: chunk,
                    metadata: { type: 'daily', file, chunk: i }
                });
            });
            console.log(`✅ ${file}: ${chunks.length} 个片段`);
        }
    }

    if (documents.length === 0) {
        console.log('⚠️  没有找到记忆文件');
        return;
    }

    // 构建 BM25 索引
    console.log(`\n🔄 正在索引 ${documents.length} 个片段...`);
    const bm25 = new BM25();
    bm25.index(documents);

    // 保存索引
    const indexData = {
        documents,
        avgDocLength: bm25.avgDocLength,
        idf: Object.fromEntries(bm25.idf),
        termFreqs: bm25.termFreqs.map(tf => Object.fromEntries(tf)),
        docLengths: bm25.docLengths
    };

    const indexPath = path.join(qmdDir, 'bm25-index.json');
    fs.writeFileSync(indexPath, JSON.stringify(indexData, null, 2));
    console.log(`✅ 索引保存成功：${indexPath}`);
    console.log(`📊 索引大小：${(fs.statSync(indexPath).size / 1024).toFixed(2)} KB`);
}

function chunkText(text, maxChunkSize) {
    const paragraphs = text.split(/\n\n+/);
    const chunks = [];
    let currentChunk = '';

    for (const para of paragraphs) {
        if (currentChunk.length + para.length > maxChunkSize && currentChunk) {
            chunks.push(currentChunk.trim());
            currentChunk = para;
        } else {
            currentChunk += '\n\n' + para;
        }
    }
    if (currentChunk.trim()) {
        chunks.push(currentChunk.trim());
    }

    return chunks.filter(c => c.length > 20);
}

buildIndex().catch(console.error);
