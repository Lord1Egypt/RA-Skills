"use strict";
// Micro Memory - Link Network System
Object.defineProperty(exports, "__esModule", { value: true });
exports.LinkManager = void 0;
exports.linkCommand = linkCommand;
exports.graphCommand = graphCommand;
const utils_1 = require("./utils");
class LinkManager {
    data;
    constructor() {
        this.data = (0, utils_1.readJson)(utils_1.LINKS_FILE, { links: [] });
    }
    save() {
        (0, utils_1.writeJson)(utils_1.LINKS_FILE, this.data);
    }
    addLink(from, to) {
        const exists = this.data.links.some(l => (l.from === from && l.to === to) || (l.from === to && l.to === from));
        if (exists) {
            return false;
        }
        this.data.links.push({
            from,
            to,
            strength: 1,
            created: new Date().toISOString(),
        });
        this.save();
        return true;
    }
    getLinksForMemory(id) {
        return this.data.links.filter(l => l.from === id || l.to === id);
    }
    getRelatedMemories(id) {
        const links = this.getLinksForMemory(id);
        return links.map(l => l.from === id ? l.to : l.from);
    }
    removeLinksForMemory(id) {
        this.data.links = this.data.links.filter(l => l.from !== id && l.to !== id);
        this.save();
    }
    buildGraph(memories, centerId) {
        const lines = ['\n🔗 Memory Link Graph\n'];
        if (centerId) {
            const related = this.getRelatedMemories(centerId);
            if (related.length === 0) {
                lines.push(`Memory #${centerId} has no links.`);
                return lines.join('\n');
            }
            lines.push(`Memory #${centerId} is linked to:`);
            for (const id of related) {
                const memory = memories.find(m => m.id === id);
                if (memory) {
                    lines.push(`  → #${id}: ${memory.content.substring(0, 50)}...`);
                }
            }
        }
        else {
            lines.push(`Total links: ${this.data.links.length}\n`);
            const memoryLinkCount = {};
            for (const link of this.data.links) {
                memoryLinkCount[link.from] = (memoryLinkCount[link.from] || 0) + 1;
                memoryLinkCount[link.to] = (memoryLinkCount[link.to] || 0) + 1;
            }
            const sorted = Object.entries(memoryLinkCount)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);
            lines.push('Most connected memories:');
            for (const [id, count] of sorted) {
                const memory = memories.find(m => m.id === parseInt(id));
                if (memory) {
                    lines.push(`  #${id} (${count} links): ${memory.content.substring(0, 40)}...`);
                }
            }
        }
        return lines.join('\n');
    }
    findPath(from, to, maxDepth = 5) {
        const visited = new Set();
        const queue = [{ id: from, path: [from] }];
        while (queue.length > 0) {
            const { id, path } = queue.shift();
            if (id === to) {
                return path;
            }
            if (path.length >= maxDepth) {
                continue;
            }
            visited.add(id);
            const related = this.getRelatedMemories(id);
            for (const nextId of related) {
                if (!visited.has(nextId)) {
                    queue.push({ id: nextId, path: [...path, nextId] });
                }
            }
        }
        return null;
    }
}
exports.LinkManager = LinkManager;
function linkCommand(args, memories) {
    const from = parseInt(args.from);
    const toStr = args.to;
    if (isNaN(from) || !toStr) {
        (0, utils_1.printColored)('Error: from and to are required', 'red');
        return;
    }
    const linkManager = new LinkManager();
    const toIds = toStr.split(',').map(s => parseInt(s.trim()));
    for (const to of toIds) {
        if (isNaN(to))
            continue;
        const fromMemory = memories.find(m => m.id === from);
        const toMemory = memories.find(m => m.id === to);
        if (!fromMemory || !toMemory) {
            (0, utils_1.printColored)(`Memory #${from} or #${to} not found`, 'red');
            continue;
        }
        if (linkManager.addLink(from, to)) {
            (0, utils_1.printColored)(`✓ Linked #${from} → #${to}`, 'green');
        }
        else {
            (0, utils_1.printColored)(`Link between #${from} and #${to} already exists`, 'yellow');
        }
    }
}
function graphCommand(args, memories) {
    const linkManager = new LinkManager();
    const id = args.id ? parseInt(args.id) : undefined;
    console.log(linkManager.buildGraph(memories, id));
}
//# sourceMappingURL=links.js.map