// Micro Memory - Archive, Compress, Export, Consolidate

import { Memory, MemoryIndex } from './types';
import { 
  readJson, writeJson, formatTimestamp, 
  printColored, ensureDir, INDEX_FILE, ARCHIVE_DIR 
} from './utils';
import * as fs from 'fs';
import * as path from 'path';

export function archiveCommand(args: Record<string, string | boolean>, memories: Memory[]): void {
  const days = parseInt(args.older_than as string) || 30;
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);

  const toArchive: Memory[] = [];
  const toKeep: Memory[] = [];

  for (const memory of memories) {
    const memDate = new Date(memory.timestamp.replace(' ', 'T'));
    if (memDate < cutoff && memory.strength.level !== 'permanent') {
      toArchive.push(memory);
    } else {
      toKeep.push(memory);
    }
  }

  if (toArchive.length === 0) {
    printColored('No memories to archive', 'yellow');
    return;
  }

  ensureDir(ARCHIVE_DIR);
  const archiveFile = path.join(ARCHIVE_DIR, `archive_${formatTimestamp().replace(/[: ]/g, '-')}.json`);
  writeJson(archiveFile, { archived: toArchive, date: formatTimestamp() });

  // Update index
  const index: MemoryIndex = { memories: toKeep, nextId: readJson<MemoryIndex>(INDEX_FILE, { memories: [], nextId: 1 }).nextId };
  writeJson(INDEX_FILE, index);

  printColored(`✓ Archived ${toArchive.length} memories to ${path.basename(archiveFile)}`, 'green');
  console.log(`  Kept ${toKeep.length} memories active`);
}

export function compressCommand(memories: Memory[]): void {
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
    writeJson(INDEX_FILE, { memories, nextId: readJson<MemoryIndex>(INDEX_FILE, { memories: [], nextId: 1 }).nextId });
    printColored(`✓ Compressed ${compressed} weak memories`, 'green');
  } else {
    printColored('No memories need compression', 'yellow');
  }
}

export function consolidateCommand(memories: Memory[]): void {
  // Remove duplicates based on content similarity
  const seen = new Set<string>();
  const unique: Memory[] = [];
  let duplicates = 0;

  for (const memory of memories) {
    const key = memory.content.toLowerCase().substring(0, 50);
    if (seen.has(key)) {
      duplicates++;
    } else {
      seen.add(key);
      unique.push(memory);
    }
  }

  if (duplicates > 0) {
    writeJson(INDEX_FILE, { memories: unique, nextId: readJson<MemoryIndex>(INDEX_FILE, { memories: [], nextId: 1 }).nextId });
    printColored(`✓ Removed ${duplicates} duplicate memories`, 'green');
    console.log(`  Kept ${unique.length} unique memories`);
  } else {
    printColored('No duplicates found', 'yellow');
  }
}

export function exportCommand(args: Record<string, string | boolean>, memories: Memory[]): void {
  const format = (args.format as string) || 'json';
  const timestamp = formatTimestamp().replace(/[: ]/g, '-');

  if (format === 'json') {
    const exportFile = path.join(process.cwd(), `memory_export_${timestamp}.json`);
    writeJson(exportFile, { memories, exported: formatTimestamp() });
    printColored(`✓ Exported to ${exportFile}`, 'green');
  } else if (format === 'csv') {
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
    printColored(`✓ Exported to ${exportFile}`, 'green');
  } else {
    printColored(`Unsupported format: ${format}`, 'red');
  }
}
