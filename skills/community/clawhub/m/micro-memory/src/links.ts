// Micro Memory - Link Network System

import { Link, LinksData, Memory } from './types';
import { readJson, writeJson, LINKS_FILE, printColored } from './utils';

export class LinkManager {
  private data: LinksData;

  constructor() {
    this.data = readJson<LinksData>(LINKS_FILE, { links: [] });
  }

  private save(): void {
    writeJson(LINKS_FILE, this.data);
  }

  addLink(from: number, to: number): boolean {
    const exists = this.data.links.some(l => 
      (l.from === from && l.to === to) || (l.from === to && l.to === from)
    );
    
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

  getLinksForMemory(id: number): Link[] {
    return this.data.links.filter(l => l.from === id || l.to === id);
  }

  getRelatedMemories(id: number): number[] {
    const links = this.getLinksForMemory(id);
    return links.map(l => l.from === id ? l.to : l.from);
  }

  removeLinksForMemory(id: number): void {
    this.data.links = this.data.links.filter(l => l.from !== id && l.to !== id);
    this.save();
  }

  buildGraph(memories: Memory[], centerId?: number): string {
    const lines: string[] = ['\n🔗 Memory Link Graph\n'];
    
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
    } else {
      lines.push(`Total links: ${this.data.links.length}\n`);
      
      const memoryLinkCount: Record<number, number> = {};
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

  findPath(from: number, to: number, maxDepth: number = 5): number[] | null {
    const visited = new Set<number>();
    const queue: { id: number; path: number[] }[] = [{ id: from, path: [from] }];
    
    while (queue.length > 0) {
      const { id, path } = queue.shift()!;
      
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

export function linkCommand(args: Record<string, string | boolean>, memories: Memory[]): void {
  const from = parseInt(args.from as string);
  const toStr = args.to as string;
  
  if (isNaN(from) || !toStr) {
    printColored('Error: from and to are required', 'red');
    return;
  }

  const linkManager = new LinkManager();
  const toIds = toStr.split(',').map(s => parseInt(s.trim()));
  
  for (const to of toIds) {
    if (isNaN(to)) continue;
    
    const fromMemory = memories.find(m => m.id === from);
    const toMemory = memories.find(m => m.id === to);
    
    if (!fromMemory || !toMemory) {
      printColored(`Memory #${from} or #${to} not found`, 'red');
      continue;
    }

    if (linkManager.addLink(from, to)) {
      printColored(`✓ Linked #${from} → #${to}`, 'green');
    } else {
      printColored(`Link between #${from} and #${to} already exists`, 'yellow');
    }
  }
}

export function graphCommand(args: Record<string, string | boolean>, memories: Memory[]): void {
  const linkManager = new LinkManager();
  const id = args.id ? parseInt(args.id as string) : undefined;
  console.log(linkManager.buildGraph(memories, id));
}
