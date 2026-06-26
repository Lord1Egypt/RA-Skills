"use strict";
// Micro Memory - Core Memory Management
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
exports.MemoryManager = void 0;
const utils_1 = require("./utils");
const strength_1 = require("./strength");
const fs = __importStar(require("fs"));
class MemoryManager {
    index;
    constructor() {
        this.index = (0, utils_1.readJson)(utils_1.INDEX_FILE, { memories: [], nextId: 1 });
        this.updateAllStrengths();
    }
    save() {
        (0, utils_1.writeJson)(utils_1.INDEX_FILE, this.index);
        this.syncToMarkdown();
    }
    updateAllStrengths() {
        for (const memory of this.index.memories) {
            memory.strength = (0, strength_1.updateStrength)(memory);
        }
    }
    // 模糊匹配（容错版）
    fuzzyMatchWithTolerance(text, pattern, tolerance) {
        if (!text || !pattern)
            return false;
        text = text.toLowerCase();
        pattern = pattern.toLowerCase();
        // 如果完全包含，直接返回 true
        if (text.includes(pattern))
            return true;
        // 如果 pattern 很短，直接检查包含
        if (pattern.length <= 3)
            return text.includes(pattern);
        // 计算 Levenshtein 距离
        const distance = this.levenshteinDistance(text, pattern);
        // 如果距离在容错范围内，返回 true
        return distance <= tolerance;
    }
    // Levenshtein 距离算法
    levenshteinDistance(s1, s2) {
        const m = s1.length, n = s2.length;
        if (m < n)
            return this.levenshteinDistance(s2, s1);
        if (n === 0)
            return m;
        let prev = new Array(n + 1);
        let curr = new Array(n + 1);
        for (let j = 0; j <= n; j++)
            prev[j] = j;
        for (let i = 1; i <= m; i++) {
            curr[0] = i;
            for (let j = 1; j <= n; j++) {
                const cost = s1[i - 1] === s2[j - 1] ? 0 : 1;
                curr[j] = Math.min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost);
            }
            [prev, curr] = [curr, prev];
        }
        return prev[n];
    }
    syncToMarkdown() {
        const lines = ['# Memory Store\n'];
        for (const memory of this.index.memories) {
            const emoji = (0, strength_1.getStrengthEmoji)(memory.strength.level);
            let line = `${memory.id}. [${memory.timestamp}]`;
            if (memory.tag)
                line += `[#${memory.tag}]`;
            line += `[${memory.type || 'note'}]`;
            line += `[${emoji}] ${memory.content}`;
            lines.push(line);
        }
        fs.writeFileSync(utils_1.STORE_FILE, lines.join('\n'), 'utf-8');
    }
    add(args) {
        const content = args.content;
        if (!content) {
            (0, utils_1.printColored)('Error: content is required', 'red');
            return;
        }
        const id = this.index.nextId;
        const timestamp = (0, utils_1.formatTimestamp)();
        const memory = {
            id,
            content,
            tag: args.tag,
            type: args.type || 'shortterm',
            importance: parseInt(args.importance) || 3,
            timestamp,
            strength: {
                level: 'stable',
                score: 50,
                lastReinforced: timestamp,
            },
        };
        if (args.link) {
            memory.links = args.link.split(',').map(s => parseInt(s.trim()));
        }
        if (args.review) {
            memory.review = args.review;
        }
        this.index.memories.push(memory);
        this.index.nextId = id + 1;
        this.save();
        (0, utils_1.printColored)(`✓ Added memory #${id}`, 'green');
        console.log(`  Content: ${(0, utils_1.truncate)(content, 60)}`);
        if (memory.tag)
            console.log(`  Tag: #${memory.tag}`);
    }
    list(args) {
        let memories = this.index.memories;
        if (args.tag) {
            memories = memories.filter(m => m.tag === args.tag);
        }
        if (args.type) {
            memories = memories.filter(m => m.type === args.type);
        }
        if (memories.length === 0) {
            (0, utils_1.printColored)('No memories found', 'yellow');
            return;
        }
        console.log(`\nFound ${memories.length} memories:\n`);
        for (const memory of memories) {
            const emoji = (0, strength_1.getStrengthEmoji)(memory.strength.level);
            const strengthInfo = args.show_strength
                ? ` [${memory.strength.level}:${memory.strength.score}]`
                : '';
            console.log(`${emoji} #${memory.id}${strengthInfo} [${memory.timestamp}]`);
            if (memory.tag)
                console.log(`   Tag: #${memory.tag}`);
            console.log(`   ${(0, utils_1.truncate)(memory.content, 80)}`);
            const warning = (0, strength_1.getDecayWarning)(memory);
            if (warning)
                (0, utils_1.printColored)(`   ${warning}`, 'yellow');
            console.log();
        }
    }
    search(args) {
        const keyword = args.keyword;
        if (!keyword) {
            (0, utils_1.printColored)('Error: keyword is required', 'red');
            return;
        }
        let results = [];
        // 正则搜索模式
        if (args.regex) {
            try {
                const regex = new RegExp(keyword, 'i');
                results = this.index.memories.filter(m => regex.test(m.content) ||
                    (m.tag && regex.test(m.tag)));
            } catch (e) {
                (0, utils_1.printColored)('Error: invalid regex pattern', 'red');
                return;
            }
        }
        // 模糊搜索模式（简化版：支持字符缺失容错）
        else if (args.fuzzy) {
            const keywords = keyword.toLowerCase().split(/\s+/);
            results = this.index.memories.filter(m => {
                const content = m.content.toLowerCase();
                const tag = m.tag ? m.tag.toLowerCase() : '';
                // 每个关键词至少模糊匹配（允许1-2个字符缺失）
                return keywords.every(kw => {
                    return this.fuzzyMatchWithTolerance(content, kw, 2) ||
                           this.fuzzyMatchWithTolerance(tag, kw, 2);
                });
            });
        }
        // 默认：多关键词搜索
        else {
            const keywords = keyword.toLowerCase().split(/\s+/);
            results = this.index.memories.filter(m => {
                const content = m.content.toLowerCase();
                const tag = m.tag ? m.tag.toLowerCase() : '';
                // 所有关键词都必须在内容或标签中出现
                return keywords.every(kw => content.includes(kw) || tag.includes(kw));
            });
        }
        if (args.tag) {
            results = results.filter(m => m.tag === args.tag);
        }
        const limit = parseInt(args.limit) || 10;
        results = results.slice(0, limit);
        if (results.length === 0) {
            (0, utils_1.printColored)(`No memories found for "${keyword}"`, 'yellow');
            return;
        }
        const searchMode = args.regex ? ' (regex)' : args.fuzzy ? ' (fuzzy)' : '';
        console.log(`\nFound ${results.length} results for "${keyword}"${searchMode}:\n`);
        for (const memory of results) {
            const emoji = (0, strength_1.getStrengthEmoji)(memory.strength.level);
            console.log(`${emoji} #${memory.id} [${memory.timestamp}]`);
            console.log(`   ${(0, utils_1.truncate)(memory.content, 80)}`);
            if (memory.tag)
                console.log(`   Tag: #${memory.tag}`);
            console.log();
        }
    }
    delete(args) {
        const id = parseInt(args.id);
        if (isNaN(id)) {
            (0, utils_1.printColored)('Error: valid id is required', 'red');
            return;
        }
        const index = this.index.memories.findIndex(m => m.id === id);
        if (index === -1) {
            (0, utils_1.printColored)(`Memory #${id} not found`, 'red');
            return;
        }
        this.index.memories.splice(index, 1);
        this.save();
        (0, utils_1.printColored)(`✓ Deleted memory #${id}`, 'green');
    }
    edit(args) {
        const id = parseInt(args.id);
        const content = args.content;
        if (isNaN(id) || !content) {
            (0, utils_1.printColored)('Error: id and content are required', 'red');
            return;
        }
        const memory = this.index.memories.find(m => m.id === id);
        if (!memory) {
            (0, utils_1.printColored)(`Memory #${id} not found`, 'red');
            return;
        }
        memory.content = content;
        this.save();
        (0, utils_1.printColored)(`✓ Updated memory #${id}`, 'green');
    }
    reinforce(args) {
        const id = parseInt(args.id);
        if (isNaN(id)) {
            (0, utils_1.printColored)('Error: valid id is required', 'red');
            return;
        }
        const memory = this.index.memories.find(m => m.id === id);
        if (!memory) {
            (0, utils_1.printColored)(`Memory #${id} not found`, 'red');
            return;
        }
        const boost = parseInt(args.boost) || 1;
        const { reinforce } = require('./strength');
        memory.strength = reinforce(memory, boost);
        this.save();
        (0, utils_1.printColored)(`✓ Reinforced memory #${id}`, 'green');
        console.log(`  New strength: ${memory.strength.level} (${memory.strength.score})`);
    }
    strength(args) {
        let memories = this.index.memories;
        if (args.decaying) {
            memories = memories.filter(m => m.strength.level === 'critical' || m.strength.level === 'weak');
        }
        memories.sort((a, b) => a.strength.score - b.strength.score);
        console.log('\nMemory Strength Report:\n');
        for (const memory of memories.slice(0, 20)) {
            const emoji = (0, strength_1.getStrengthEmoji)(memory.strength.level);
            const bar = '█'.repeat(Math.floor(memory.strength.score / 5)) +
                '░'.repeat(20 - Math.floor(memory.strength.score / 5));
            console.log(`${emoji} #${memory.id} [${bar}] ${memory.strength.score}`);
            console.log(`   ${(0, utils_1.truncate)(memory.content, 60)}`);
        }
    }
    stats() {
        const stats = this.calculateStats();
        console.log('\n📊 Memory Statistics\n');
        console.log(`Total memories: ${stats.total}`);
        console.log(`Average strength: ${stats.avgStrength.toFixed(1)}`);
        console.log(`Oldest: ${stats.oldest}`);
        console.log(`Newest: ${stats.newest}`);
        console.log('\nBy Tag:');
        for (const [tag, count] of Object.entries(stats.byTag)) {
            console.log(`  #${tag}: ${count}`);
        }
        console.log('\nBy Type:');
        for (const [type, count] of Object.entries(stats.byType)) {
            console.log(`  ${type}: ${count}`);
        }
    }
    calculateStats() {
        const memories = this.index.memories;
        if (memories.length === 0) {
            return {
                total: 0,
                byTag: {},
                byType: {},
                avgStrength: 0,
                oldest: '-',
                newest: '-',
            };
        }
        const byTag = {};
        const byType = {};
        let totalStrength = 0;
        for (const m of memories) {
            if (m.tag)
                byTag[m.tag] = (byTag[m.tag] || 0) + 1;
            if (m.type)
                byType[m.type] = (byType[m.type] || 0) + 1;
            totalStrength += m.strength.score;
        }
        const timestamps = memories.map(m => new Date(m.timestamp.replace(' ', 'T')));
        timestamps.sort((a, b) => a.getTime() - b.getTime());
        return {
            total: memories.length,
            byTag,
            byType,
            avgStrength: totalStrength / memories.length,
            oldest: memories.find(m => m.timestamp === (0, utils_1.formatTimestamp)(timestamps[0]))?.timestamp || '-',
            newest: memories.find(m => m.timestamp === (0, utils_1.formatTimestamp)(timestamps[timestamps.length - 1]))?.timestamp || '-',
        };
    }
    getMemories() {
        return this.index.memories;
    }
    getMemoryById(id) {
        return this.index.memories.find(m => m.id === id);
    }
    updateMemory(memory) {
        const index = this.index.memories.findIndex(m => m.id === memory.id);
        if (index !== -1) {
            this.index.memories[index] = memory;
            this.save();
        }
    }
}
exports.MemoryManager = MemoryManager;
//# sourceMappingURL=memory.js.map