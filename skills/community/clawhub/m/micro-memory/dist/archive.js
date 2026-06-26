"use strict";
// Micro Memory - Archive, Compress, Export, Consolidate
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.archiveCommand = archiveCommand;
exports.compressCommand = compressCommand;
exports.consolidateCommand = consolidateCommand;
exports.exportCommand = exportCommand;
const utils_1 = require("./utils");
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
function archiveCommand(args, memories) {
    const days = parseInt(args.older_than) || 30;
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - days);
    const toArchive = [];
    const toKeep = [];
    for (const memory of memories) {
        const memDate = new Date(memory.timestamp.replace(' ', 'T'));
        if (memDate < cutoff && memory.strength.level !== 'permanent') {
            toArchive.push(memory);
        }
        else {
            toKeep.push(memory);
        }
    }
    if (toArchive.length === 0) {
        (0, utils_1.printColored)('No memories to archive', 'yellow');
        return;
    }
    (0, utils_1.ensureDir)(utils_1.ARCHIVE_DIR);
    const archiveFile = path.join(utils_1.ARCHIVE_DIR, `archive_${(0, utils_1.formatTimestamp)().replace(/[: ]/g, '-')}.json`);
    (0, utils_1.writeJson)(archiveFile, { archived: toArchive, date: (0, utils_1.formatTimestamp)() });
    // Update index
    const index = { memories: toKeep, nextId: (0, utils_1.readJson)(utils_1.INDEX_FILE, { memories: [], nextId: 1 }).nextId };
    (0, utils_1.writeJson)(utils_1.INDEX_FILE, index);
    (0, utils_1.printColored)(`✓ Archived ${toArchive.length} memories to ${path.basename(archiveFile)}`, 'green');
    console.log(`  Kept ${toKeep.length} memories active`);
}
function compressCommand(memories) {
    let compressed = 0;
    for (const memory of memories) {
        if (memory.strength.level === 'critical' || memory.strength.score < 10) {
            // Compress: keep only essential info
            memory.content = `[COMPRESSED] ${memory.content.substring(0, 100)}...`;
            memory.strength.score = 5;
            memory.strength.level = 'critical';
            compressed++;
        }
    }
    if (compressed > 0) {
        (0, utils_1.writeJson)(utils_1.INDEX_FILE, { memories, nextId: (0, utils_1.readJson)(utils_1.INDEX_FILE, { memories: [], nextId: 1 }).nextId });
        (0, utils_1.printColored)(`✓ Compressed ${compressed} weak memories`, 'green');
    }
    else {
        (0, utils_1.printColored)('No memories need compression', 'yellow');
    }
}
function consolidateCommand(memories) {
    // Remove duplicates based on content similarity
    const seen = new Set();
    const unique = [];
    let duplicates = 0;
    for (const memory of memories) {
        const key = memory.content.toLowerCase().substring(0, 50);
        if (seen.has(key)) {
            duplicates++;
        }
        else {
            seen.add(key);
            unique.push(memory);
        }
    }
    if (duplicates > 0) {
        (0, utils_1.writeJson)(utils_1.INDEX_FILE, { memories: unique, nextId: (0, utils_1.readJson)(utils_1.INDEX_FILE, { memories: [], nextId: 1 }).nextId });
        (0, utils_1.printColored)(`✓ Removed ${duplicates} duplicate memories`, 'green');
        console.log(`  Kept ${unique.length} unique memories`);
    }
    else {
        (0, utils_1.printColored)('No duplicates found', 'yellow');
    }
}
function exportCommand(args, memories) {
    const format = args.format || 'json';
    const timestamp = (0, utils_1.formatTimestamp)().replace(/[: ]/g, '-');
    if (format === 'json') {
        const exportFile = path.join(process.cwd(), `memory_export_${timestamp}.json`);
        (0, utils_1.writeJson)(exportFile, { memories, exported: (0, utils_1.formatTimestamp)() });
        (0, utils_1.printColored)(`✓ Exported to ${exportFile}`, 'green');
    }
    else if (format === 'csv') {
        const exportFile = path.join(process.cwd(), `memory_export_${timestamp}.csv`);
        const lines = ['id,content,tag,type,importance,timestamp,strength_score,strength_level'];
        for (const memory of memories) {
            const row = [
                memory.id,
                `"${memory.content.replace(/"/g, '""')}"`,
                memory.tag || '',
                memory.type || '',
                memory.importance || '',
                memory.timestamp,
                memory.strength.score,
                memory.strength.level,
            ].join(',');
            lines.push(row);
        }
        fs.writeFileSync(exportFile, lines.join('\n'), 'utf-8');
        (0, utils_1.printColored)(`✓ Exported to ${exportFile}`, 'green');
    }
    else {
        (0, utils_1.printColored)(`Unsupported format: ${format}`, 'red');
    }
}
//# sourceMappingURL=archive.js.map