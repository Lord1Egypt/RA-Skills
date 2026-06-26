// Micro Memory - Core Memory Management

import { Memory, MemoryIndex, Stats, CommandArgs } from './types';
import { 
  readJson, writeJson, formatTimestamp, 
  printColored, truncate, fuzzyMatch, fuzzyMatchWithTolerance, regexMatch, 
  multiKeywordMatch, calculateRelevanceScore, parseSearchKeywords, STORE_FILE, INDEX_FILE 
} from './utils';
import { updateStrength, getStrengthEmoji, getDecayWarning } from './strength';
import * as fs from 'fs';

export class MemoryManager {
  private index: MemoryIndex;

  constructor() {
    this.index = readJson<MemoryIndex>(INDEX_FILE, { memories: [], nextId: 1 });
    this.updateAllStrengths();
  }

  private save(): void {
    writeJson(INDEX_FILE, this.index);
    this.syncToMarkdown();
  }

  private updateAllStrengths(): void {
    for (const memory of this.index.memories) {
      memory.strength = updateStrength(memory);
    }
  }

  private syncToMarkdown(): void {
    const lines: string[] = ['# Memory Store\n'];
    for (const memory of this.index.memories) {
      const emoji = getStrengthEmoji(memory.strength.level);
      let line = `${memory.id}. [${memory.timestamp}]`;
      if (memory.tag) line += `[#${memory.tag}]`;
      line += `[${memory.type || 'note'}]`;
      line += `[${emoji}] ${memory.content}`;
      lines.push(line);
    }
    fs.writeFileSync(STORE_FILE, lines.join('\n'), 'utf-8');
  }

  add(args: CommandArgs): void {
    const content = args.content as string;
    if (!content) {
      printColored('Error: content is required', 'red');
      return;
    }

    const id = this.index.nextId;
    const timestamp = formatTimestamp();
    
    const memory: Memory = {
      id,
      content,
      tag: args.tag as string,
      type: (args.type as 'shortterm' | 'longterm') || 'shortterm',
      importance: parseInt(args.importance as string) || 3,
      timestamp,
      strength: {
        level: 'stable',
        score: 50,
        lastReinforced: timestamp,
      },
    };

    if (args.link) {
      memory.links = (args.link as string).split(',').map(s => parseInt(s.trim()));
    }
    if (args.review) {
      memory.review = args.review as string;
    }

    this.index.memories.push(memory);
    this.index.nextId = id + 1;
    this.save();

    printColored(`✓ Added memory #${id}`, 'green');
    console.log(`  Content: ${truncate(content, 60)}`);
    if (memory.tag) console.log(`  Tag: #${memory.tag}`);
  }

  list(args: CommandArgs): void {
    let memories = this.index.memories;

    if (args.tag) {
      memories = memories.filter(m => m.tag === args.tag);
    }
    if (args.type) {
      memories = memories.filter(m => m.type === args.type);
    }

    if (memories.length === 0) {
      printColored('No memories found', 'yellow');
      return;
    }

    console.log(`\nFound ${memories.length} memories:\n`);
    for (const memory of memories) {
      const emoji = getStrengthEmoji(memory.strength.level);
      const strengthInfo = args.show_strength 
        ? ` [${memory.strength.level}:${memory.strength.score}]` 
        : '';
      
      console.log(`${emoji} #${memory.id}${strengthInfo} [${memory.timestamp}]`);
      if (memory.tag) console.log(`   Tag: #${memory.tag}`);
      console.log(`   ${truncate(memory.content, 80)}`);
      
      const warning = getDecayWarning(memory);
      if (warning) printColored(`   ${warning}`, 'yellow');
      console.log();
    }
  }

  search(args: CommandArgs): void {
    const keyword = args.keyword as string || args.content as string;
    if (!keyword) {
      printColored('Error: keyword is required', 'red');
      return;
    }

    const useRegex = args.regex === true;
    const useFuzzy = args.fuzzy === true;
    const keywords = parseSearchKeywords(keyword);
    
    let results = this.index.memories.filter(m => {
      const text = m.content + ' ' + (m.tag || '');
      
      if (useRegex) {
        // 正则模式
        return regexMatch(text, keyword);
      } else if (useFuzzy) {
        // 模糊模式：使用多关键词 AND 匹配
        return multiKeywordMatch(text, keywords);
      } else {
        // 默认模式：原始模糊匹配
        return fuzzyMatch(m.content, keyword) || 
               (m.tag && fuzzyMatch(m.tag, keyword));
      }
    });

    // 按相关性排序
    if (useFuzzy || keywords.length > 1) {
      results = results.sort((a, b) => {
        const scoreA = calculateRelevanceScore(a, keywords);
        const scoreB = calculateRelevanceScore(b, keywords);
        return scoreB - scoreA;
      });
    }

    if (args.tag) {
      results = results.filter(m => m.tag === args.tag);
    }

    const limit = parseInt(args.limit as string) || 10;
    const totalResults = results.length;
    results = results.slice(0, limit);

    if (results.length === 0) {
      printColored(`No memories found for "${keyword}"`, 'yellow');
      return;
    }

    console.log(`\nFound ${totalResults} results for "${keyword}" (showing ${results.length}):\n`);
    for (const memory of results) {
      const emoji = getStrengthEmoji(memory.strength.level);
      console.log(`${emoji} #${memory.id} [${memory.timestamp}]`);
      console.log(`   ${truncate(memory.content, 80)}`);
      if (memory.tag) console.log(`   Tag: #${memory.tag}`);
      console.log();
    }
  }

  delete(args: CommandArgs): void {
    const id = parseInt(args.id as string);
    if (isNaN(id)) {
      printColored('Error: valid id is required', 'red');
      return;
    }

    const index = this.index.memories.findIndex(m => m.id === id);
    if (index === -1) {
      printColored(`Memory #${id} not found`, 'red');
      return;
    }

    this.index.memories.splice(index, 1);
    this.save();
    printColored(`✓ Deleted memory #${id}`, 'green');
  }

  edit(args: CommandArgs): void {
    const id = parseInt(args.id as string);
    const content = args.content as string;
    
    if (isNaN(id) || !content) {
      printColored('Error: id and content are required', 'red');
      return;
    }

    const memory = this.index.memories.find(m => m.id === id);
    if (!memory) {
      printColored(`Memory #${id} not found`, 'red');
      return;
    }

    memory.content = content;
    this.save();
    printColored(`✓ Updated memory #${id}`, 'green');
  }

  reinforce(args: CommandArgs): void {
    const id = parseInt(args.id as string);
    if (isNaN(id)) {
      printColored('Error: valid id is required', 'red');
      return;
    }

    const memory = this.index.memories.find(m => m.id === id);
    if (!memory) {
      printColored(`Memory #${id} not found`, 'red');
      return;
    }

    const boost = parseInt(args.boost as string) || 1;
    const { reinforce } = require('./strength');
    memory.strength = reinforce(memory, boost);
    this.save();

    printColored(`✓ Reinforced memory #${id}`, 'green');
    console.log(`  New strength: ${memory.strength.level} (${memory.strength.score})`);
  }

  strength(args: CommandArgs): void {
    let memories = this.index.memories;
    
    if (args.decaying) {
      memories = memories.filter(m => m.strength.level === 'critical' || m.strength.level === 'weak');
    }

    memories.sort((a, b) => a.strength.score - b.strength.score);

    console.log('\nMemory Strength Report:\n');
    for (const memory of memories.slice(0, 20)) {
      const emoji = getStrengthEmoji(memory.strength.level);
      const bar = '█'.repeat(Math.floor(memory.strength.score / 5)) + 
                  '░'.repeat(20 - Math.floor(memory.strength.score / 5));
      console.log(`${emoji} #${memory.id} [${bar}] ${memory.strength.score}`);
      console.log(`   ${truncate(memory.content, 60)}`);
    }
  }

  stats(): void {
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

  private calculateStats(): Stats {
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

    const byTag: Record<string, number> = {};
    const byType: Record<string, number> = {};
    let totalStrength = 0;

    for (const m of memories) {
      if (m.tag) byTag[m.tag] = (byTag[m.tag] || 0) + 1;
      if (m.type) byType[m.type] = (byType[m.type] || 0) + 1;
      totalStrength += m.strength.score;
    }

    const timestamps = memories.map(m => new Date(m.timestamp.replace(' ', 'T')));
    timestamps.sort((a, b) => a.getTime() - b.getTime());

    return {
      total: memories.length,
      byTag,
      byType,
      avgStrength: totalStrength / memories.length,
      oldest: memories.find(m => m.timestamp === formatTimestamp(timestamps[0]))?.timestamp || '-',
      newest: memories.find(m => m.timestamp === formatTimestamp(timestamps[timestamps.length - 1]))?.timestamp || '-',
    };
  }

  getMemories(): Memory[] {
    return this.index.memories;
  }

  getMemoryById(id: number): Memory | undefined {
    return this.index.memories.find(m => m.id === id);
  }

  updateMemory(memory: Memory): void {
    const index = this.index.memories.findIndex(m => m.id === memory.id);
    if (index !== -1) {
      this.index.memories[index] = memory;
      this.save();
    }
  }
}
