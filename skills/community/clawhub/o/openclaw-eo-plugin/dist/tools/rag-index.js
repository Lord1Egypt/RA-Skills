/**
 * EO RAG Index Tool Handler
 * Bulk index documents into shared knowledge base
 */
import { getSharedRAGSystem } from '../rag/rag-system.js';
import { textResult, errorResult } from '../formatters/index.js';
import * as fs from 'fs';
import * as path from 'path';
export async function handleRAGIndex(params, agentId) {
    const ragSystem = getSharedRAGSystem();
    try {
        switch (params.action) {
            case 'add':
                return handleAdd(ragSystem, params, agentId);
            case 'remove':
                return handleRemove(ragSystem, params, agentId);
            case 'list':
                return handleList(ragSystem);
            case 'stats':
                return handleStats(ragSystem);
            case 'clear':
                return handleClear(ragSystem);
            default:
                return errorResult('Unknown action: ' + params.action);
        }
    }
    catch (err) {
        return errorResult('RAG Index error: ' + (err instanceof Error ? err.message : String(err)));
    }
}
async function handleAdd(ragSystem, params, agentId) {
    const docs = [];
    if (params.content) {
        docs.push({
            content: params.content,
            source: params.source || 'manual',
            layer: params.layer,
            tags: params.tags
        });
    }
    if (params.filePath && fs.existsSync(params.filePath)) {
        const stat = fs.statSync(params.filePath);
        if (stat.isDirectory()) {
            const files = fs.readdirSync(params.filePath);
            for (const file of files) {
                const filePath = path.join(params.filePath, file);
                if (fs.statSync(filePath).isFile()) {
                    const content = fs.readFileSync(filePath, 'utf-8');
                    docs.push({
                        content: content.substring(0, 10000),
                        source: 'file://' + file,
                        layer: params.layer,
                        tags: params.tags || [path.extname(file).slice(1)]
                    });
                }
            }
        }
        else {
            const content = fs.readFileSync(params.filePath, 'utf-8');
            docs.push({
                content: content.substring(0, 10000),
                source: 'file://' + params.filePath,
                layer: params.layer,
                tags: params.tags || [path.extname(params.filePath).slice(1)]
            });
        }
    }
    if (docs.length === 0) {
        return errorResult('No content to index. Provide content or filePath.');
    }
    let indexed = 0;
    for (const doc of docs) {
        await ragSystem.indexChunk({
            layer: doc.layer || 2,
            content: doc.content,
            metadata: {
                source: doc.source,
                acl: params.visibility || 'public',
                tags: doc.tags || []
            }
        }, agentId);
        indexed++;
    }
    const output = '✅ Indexed ' + indexed + ' document(s) to RAG Knowledge Base\n\n' +
        '**Source:** ' + (params.source || params.filePath || 'manual') + '\n' +
        '**Layer:** ' + (params.layer || 2) + '\n' +
        '**Visibility:** ' + (params.visibility || 'public') + '\n' +
        '**Agent:** ' + (agentId || 'global') + '\n\n' +
        '*Data persists across Gateway restarts*';
    return textResult(output);
}
async function handleRemove(ragSystem, params, agentId) {
    if (!params.source) {
        return errorResult('Provide source to remove matching chunks');
    }
    const deleted = await ragSystem.deleteBySource(params.source, agentId || 'global');
    return textResult('✅ Deleted ' + deleted + ' chunk(s) from source "' + params.source + '"');
}
async function handleList(ragSystem) {
    const stats = await ragSystem.getStats();
    const layerNames = ['', 'L1:Expert', 'L2:Pattern', 'L3:Checkpoint', 'L4:ETP', 'L5:Session'];
    const byLayerLines = Object.entries(stats.byLayer).map(([l, c]) => '  ' + (layerNames[parseInt(l)] || l) + ': ' + c).join('\n');
    const byACLLines = Object.entries(stats.byACL).map(([v, c]) => '  ' + v + ': ' + c).join('\n');
    const output = '📚 RAG Knowledge Base\n\n' +
        '**Total Chunks:** ' + stats.totalChunks + '\n' +
        '**Storage:** ' + stats.storagePath + '\n\n' +
        '### By Layer\n' + byLayerLines + '\n\n' +
        '### By Visibility\n' + byACLLines;
    return textResult(output);
}
async function handleStats(ragSystem) {
    const stats = await ragSystem.getStats();
    const layerDist = Object.entries(stats.byLayer).map(([l, c]) => 'L' + l + ': ' + c).join(' | ');
    const visDist = Object.entries(stats.byACL).map(([v, c]) => v + ': ' + c).join(' | ');
    const output = '📊 RAG System Statistics\n\n' +
        '| Metric | Value |\n' +
        '|--------|-------|\n' +
        '| Enabled | ' + (stats.enabled ? '✅' : '❌') + ' |\n' +
        '| Total Chunks | ' + stats.totalChunks + ' |\n' +
        '| Storage Path | ' + stats.storagePath + ' |\n\n' +
        '### Layer Distribution\n' + layerDist + '\n\n' +
        '### Visibility Distribution\n' + visDist + '\n\n' +
        '*All 9 administrators share this knowledge base*';
    return textResult(output);
}
async function handleClear(ragSystem) {
    return textResult('ℹ️ Clear not implemented - manual deletion required');
}
//# sourceMappingURL=rag-index.js.map