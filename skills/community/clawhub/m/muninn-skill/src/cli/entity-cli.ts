#!/usr/bin/env node
/**
 * Entity List Builder CLI
 * 
 * Usage:
 *   node entity-cli.js scan <db-path>     - Scan memories for entities
 *   node entity-cli.js list               - List all entities
 *   node entity-cli.js merge <from> <to>  - Merge entity A into B
 *   node entity-cli.js export             - Export for review
 */

import Database from 'better-sqlite3';
import { 
  scanMemoriesForEntities, 
  getAllEntities, 
  mergeEntities, 
  exportEntityList,
  findEntity,
  addAlias,
  clearCache,
  CanonicalEntity
} from '../extractors/entity-builder.js';

const args = process.argv.slice(2);
const command = args[0];

async function main() {
  switch (command) {
    case 'scan': {
      const dbPath = args[1];
      if (!dbPath) {
        console.error('Usage: node entity-cli.js scan <db-path>');
        process.exit(1);
      }
      
      console.log('📂 Scanning memories for entities...\n');
      
      const db = new Database(dbPath, { readonly: true });
      const memories = db.prepare(`
        SELECT content, created_at as timestamp 
        FROM memories 
        ORDER BY created_at ASC
      `).all() as Array<{ content: string; timestamp: string }>;
      
      console.log(`Found ${memories.length} memories\n`);
      
      const result = await scanMemoriesForEntities(memories);
      
      console.log('\n✅ Scan complete!');
      console.log(`   Total entities: ${result.total}`);
      console.log(`   New entities: ${result.newEntities}`);
      
      // Show top entities
      const stats = exportEntityList();
      console.log('\n📊 Top mentioned entities:');
      for (const e of stats.statistics.topMentioned.slice(0, 5)) {
        console.log(`   ${e.id}: ${e.name} (${e.type}) - ${e.mentionCount} mentions`);
      }
      
      db.close();
      break;
    }
    
    case 'list': {
      const entities = getAllEntities();
      const type = args[1];
      
      if (type) {
        const filtered = entities.filter(e => e.type === type);
        console.log(`\n📋 ${type.toUpperCase()} entities (${filtered.length}):\n`);
        for (const e of filtered) {
          console.log(`  ${e.id}: ${e.name}`);
          if (e.aliases.length > 1) {
            console.log(`    Aliases: ${e.aliases.slice(1).join(', ')}`);
          }
          console.log(`    Mentions: ${e.mentionCount}`);
        }
      } else {
        console.log(`\n📋 All entities (${entities.length}):\n`);
        
        const byType: Record<string, CanonicalEntity[]> = {};
        for (const e of entities) {
          byType[e.type] = byType[e.type] || [];
          byType[e.type].push(e);
        }
        
        for (const [t, ents] of Object.entries(byType)) {
          console.log(`\n${t.toUpperCase()} (${ents.length}):`);
          for (const e of ents.slice(0, 10)) {
            console.log(`  ${e.id}: ${e.name} (${e.mentionCount})`);
          }
          if (ents.length > 10) {
            console.log(`  ... and ${ents.length - 10} more`);
          }
        }
      }
      break;
    }
    
    case 'merge': {
      const fromId = args[1];
      const toId = args[2];
      
      if (!fromId || !toId) {
        console.error('Usage: node entity-cli.js merge <from-id> <to-id>');
        console.error('Example: node entity-cli.js merge PERSON_002 PERSON_001');
        process.exit(1);
      }
      
      const success = mergeEntities(fromId, toId);
      
      if (success) {
        console.log(`✅ Merged ${fromId} into ${toId}`);
      } else {
        console.error(`❌ Failed to merge. Check IDs.`);
      }
      break;
    }
    
    case 'alias': {
      const entityId = args[1];
      const alias = args[2];
      
      if (!entityId || !alias) {
        console.error('Usage: node entity-cli.js alias <entity-id> <alias>');
        process.exit(1);
      }
      
      const success = addAlias(entityId, alias);
      
      if (success) {
        console.log(`✅ Added alias "${alias}" to ${entityId}`);
      } else {
        console.error(`❌ Failed to add alias.`);
      }
      break;
    }
    
    case 'find': {
      const name = args.slice(1).join(' ');
      
      if (!name) {
        console.error('Usage: node entity-cli.js find <name>');
        process.exit(1);
      }
      
      const entity = findEntity(name);
      
      if (entity) {
        console.log(`\n✅ Found: ${entity.id}`);
        console.log(`   Name: ${entity.name}`);
        console.log(`   Type: ${entity.type}`);
        console.log(`   Aliases: ${entity.aliases.join(', ')}`);
        console.log(`   Mentions: ${entity.mentionCount}`);
      } else {
        console.log(`❌ No entity found for "${name}"`);
      }
      break;
    }
    
    case 'export': {
      const stats = exportEntityList();
      
      console.log('\n📊 Entity Statistics:');
      console.log(`   Total entities: ${stats.statistics.total}`);
      console.log('\n   By type:');
      for (const [type, count] of Object.entries(stats.statistics.byType)) {
        console.log(`     ${type}: ${count}`);
      }
      
      console.log('\n   Top 10 mentioned:');
      for (const e of stats.statistics.topMentioned) {
        console.log(`     ${e.name} (${e.type}): ${e.mentionCount} mentions`);
        if (e.aliases.length > 1) {
          console.log(`       Aliases: ${e.aliases.slice(1).join(', ')}`);
        }
      }
      
      // Export to JSON
      const exportPath = '/tmp/muninn-entities-export.json';
      const fs = await import('fs');
      fs.writeFileSync(exportPath, JSON.stringify(stats, null, 2));
      console.log(`\n📁 Exported to: ${exportPath}`);
      break;
    }
    
    case 'clear': {
      clearCache();
      console.log('✅ Entity cache cleared');
      break;
    }
    
    default:
      console.log(`
Entity List Builder CLI

Commands:
  scan <db-path>       Scan memories for entities
  list [type]          List all entities (or by type)
  merge <from> <to>    Merge entity A into B
  alias <id> <alias>   Add alias to entity
  find <name>          Find entity by name/alias
  export               Export statistics and top entities
  clear                Clear entity cache

Examples:
  node entity-cli.js scan /path/to/memories.db
  node entity-cli.js list person
  node entity-cli.js merge PERSON_002 PERSON_001
  node entity-cli.js alias PERSON_001 "Carrie"
  node entity-cli.js find Caroline
`);
  }
}

main().catch(console.error);