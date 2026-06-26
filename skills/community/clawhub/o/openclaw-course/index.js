#!/usr/bin/env node

/**
 * OpenClaw Course Search
 * Searchable reference for the OpenClaw Masterclass
 * 
 * Usage:
 *   node index.js search "query"           # Search course content
 *   node index.js list                     # List all modules
 *   node index.js section "module" "title" # Get specific section
 */

const fs = require('fs');
const path = require('path');

const REFERENCES_DIR = path.join(__dirname, 'references');

const MODULES = [
  { file: '01-FOUNDATIONS.md', name: 'Foundations', topics: ['installation', 'setup', 'gateway', 'telegram', 'whatsapp', 'slack', 'docker'] },
  { file: '02-THE-SOUL-ARCHITECTURE.md', name: 'Soul Architecture', topics: ['SOUL.md', 'IDENTITY.md', 'USER.md', 'AGENTS.md', 'HEARTBEAT.md', 'personality'] },
  { file: '03-LOCAL-POWER.md', name: 'Local Power', topics: ['ollama', 'local ai', 'voice', 'whisper', 'comfyui', 'vision', 'codex', 'claude code'] },
  { file: '04-CONTEXT-AND-COSTS.md', name: 'Context & Costs', topics: ['cost', 'pricing', 'optimization', 'tokens', 'context window', 'routing'] },
  { file: '05-VPS-EMPLOYEE.md', name: 'VPS Employee', topics: ['vps', 'server', 'deploy', 'tailscale', 'cron', 'systemd', '24/7'] },
  { file: '06-SECURITY.md', name: 'Security', topics: ['security', 'hardening', 'ssh', 'firewall', 'secrets', 'privacy'] },
  { file: '07-SKILLS-AND-FUTURE.md', name: 'Skills & Future', topics: ['skills', 'custom skill', 'clawhub', 'create skill', 'manifest'] },
  { file: 'README.md', name: 'Overview', topics: ['overview', 'introduction', 'course'] }
];

/**
 * Parse a markdown file into structured sections
 */
function parseMarkdown(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');
  
  const sections = [];
  let currentSection = null;
  let codeBlock = null;
  let lineNumber = 0;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    lineNumber = i + 1;
    
    // Code block handling
    if (line.startsWith('```')) {
      if (codeBlock) {
        // End of code block
        codeBlock.endLine = lineNumber;
        if (currentSection) {
          currentSection.codeBlocks.push(codeBlock);
        }
        codeBlock = null;
      } else {
        // Start of code block
        codeBlock = {
          language: line.slice(3).trim(),
          content: [],
          startLine: lineNumber
        };
      }
      continue;
    }
    
    if (codeBlock) {
      codeBlock.content.push(line);
      continue;
    }
    
    // Section headers (## or ###)
    const headerMatch = line.match(/^(#{2,3})\s+(.+)$/);
    if (headerMatch) {
      if (currentSection) {
        currentSection.endLine = lineNumber - 1;
        sections.push(currentSection);
      }
      currentSection = {
        level: headerMatch[1].length,
        title: headerMatch[2].trim(),
        content: [],
        codeBlocks: [],
        startLine: lineNumber
      };
      continue;
    }
    
    if (currentSection) {
      currentSection.content.push(line);
    }
  }
  
  // Close final section
  if (currentSection) {
    currentSection.endLine = lines.length;
    sections.push(currentSection);
  }
  
  return {
    content,
    lines,
    sections,
    totalLines: lines.length
  };
}

/**
 * Score a match based on relevance
 */
function scoreMatch(queryLower, text, title) {
  let score = 0;
  const textLower = text.toLowerCase();
  const titleLower = title.toLowerCase();
  
  // Title match is weighted heavily
  if (titleLower === queryLower) score += 100;
  else if (titleLower.includes(queryLower)) score += 50;
  
  // Exact match in content
  if (textLower === queryLower) score += 40;
  else if (textLower.includes(queryLower)) score += 20;
  
  // Word boundary matches
  const words = queryLower.split(/\s+/);
  for (const word of words) {
    if (word.length < 3) continue; // Skip short words
    if (titleLower.includes(word)) score += 10;
    if (textLower.includes(word)) score += 5;
  }
  
  return score;
}

/**
 * Extract excerpt around matching content
 */
function getExcerpt(lines, startLine, endLine, contextLines = 3) {
  const start = Math.max(0, startLine - contextLines - 1);
  const end = Math.min(lines.length, endLine + contextLines);
  return lines.slice(start, end).join('\n').trim();
}

/**
 * Search across all course modules
 */
function search(query, options = {}) {
  const queryLower = query.toLowerCase().trim();
  const results = [];
  
  if (!queryLower) {
    return { error: 'Please provide a search query' };
  }
  
  for (const module of MODULES) {
    const filePath = path.join(REFERENCES_DIR, module.file);
    
    if (!fs.existsSync(filePath)) {
      continue;
    }
    
    const parsed = parseMarkdown(filePath);
    
    // Check module-level topics match
    const topicMatch = module.topics.some(t => t.includes(queryLower) || queryLower.includes(t));
    if (topicMatch) {
      results.push({
        module: module.name,
        file: module.file,
        type: 'module',
        title: module.name,
        excerpt: `Module covering: ${module.topics.join(', ')}`,
        line: 1,
        score: 30
      });
    }
    
    // Search sections
    for (const section of parsed.sections) {
      const sectionText = section.content.join('\n');
      const fullText = section.title + '\n' + sectionText;
      const score = scoreMatch(queryLower, fullText, section.title);
      
      if (score > 0) {
        results.push({
          module: module.name,
          file: module.file,
          type: 'section',
          title: section.title,
          excerpt: getExcerpt(parsed.lines, section.startLine, Math.min(section.startLine + 5, section.endLine)),
          line: section.startLine,
          score: score,
          level: section.level
        });
      }
      
      // Search within code blocks
      for (const codeBlock of section.codeBlocks) {
        const codeText = codeBlock.content.join('\n');
        if (codeText.toLowerCase().includes(queryLower)) {
          results.push({
            module: module.name,
            file: module.file,
            type: 'code',
            title: `${section.title} (code example)`,
            excerpt: codeText.slice(0, 300) + (codeText.length > 300 ? '...' : ''),
            line: codeBlock.startLine,
            score: 15,
            language: codeBlock.language
          });
        }
      }
    }
    
    // Full-text search for any remaining matches
    const fullContent = parsed.content.toLowerCase();
    if (fullContent.includes(queryLower) && !results.some(r => r.file === module.file)) {
      // Find the line number
      const lines = parsed.lines;
      let matchLine = 1;
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].toLowerCase().includes(queryLower)) {
          matchLine = i + 1;
          break;
        }
      }
      
      results.push({
        module: module.name,
        file: module.file,
        type: 'content',
        title: `Mention in ${module.name}`,
        excerpt: getExcerpt(parsed.lines, matchLine, matchLine + 3),
        line: matchLine,
        score: 5
      });
    }
  }
  
  // Sort by score descending
  results.sort((a, b) => b.score - a.score);
  
  // Limit results
  const limit = options.limit || 5;
  return {
    query,
    totalResults: results.length,
    results: results.slice(0, limit)
  };
}

/**
 * Get a specific section by module and title
 */
function getSection(moduleFile, sectionTitle) {
  const filePath = path.join(REFERENCES_DIR, moduleFile);
  
  if (!fs.existsSync(filePath)) {
    return { error: `Module not found: ${moduleFile}` };
  }
  
  const parsed = parseMarkdown(filePath);
  const titleLower = sectionTitle.toLowerCase();
  
  for (const section of parsed.sections) {
    if (section.title.toLowerCase().includes(titleLower)) {
      const content = section.content.join('\n');
      let result = `# ${section.title}\n\n${content}`;
      
      // Include code blocks
      for (const codeBlock of section.codeBlocks) {
        const code = codeBlock.content.join('\n');
        result += `\n\n\`\`\`${codeBlock.language}\n${code}\n\`\`\``;
      }
      
      return {
        module: moduleFile,
        title: section.title,
        line: section.startLine,
        content: result
      };
    }
  }
  
  return { error: `Section not found: ${sectionTitle}` };
}

/**
 * List all available modules
 */
function listModules() {
  return MODULES.map(m => ({
    name: m.name,
    file: m.file,
    topics: m.topics
  }));
}

/**
 * Format search results for display
 */
function formatResults(searchResult) {
  if (searchResult.error) {
    return `Error: ${searchResult.error}`;
  }
  
  if (searchResult.results.length === 0) {
    return `No results found for "${searchResult.query}".\n\nTry searching for:\n- Installation: "install OpenClaw"\n- Configuration: "SOUL.md"\n- Local AI: "Ollama setup"\n- VPS: "VPS deployment"\n- Skills: "create skill"`;
  }
  
  let output = `Found ${searchResult.totalResults} result${searchResult.totalResults !== 1 ? 's' : ''} for "${searchResult.query}":\n`;
  output += '=' .repeat(60) + '\n\n';
  
  for (let i = 0; i < searchResult.results.length; i++) {
    const r = searchResult.results[i];
    output += `[${i + 1}] **${r.title}**\n`;
    output += `    Module: ${r.module} | Source: ${r.file}:${r.line}\n`;
    
    if (r.type === 'code' && r.language) {
      output += `    Language: ${r.language}\n`;
    }
    
    output += '\n';
    
    // Format excerpt
    const excerpt = r.excerpt.split('\n').map(line => '    ' + line).join('\n');
    output += excerpt + '\n\n';
    
    if (i < searchResult.results.length - 1) {
      output += '-'.repeat(40) + '\n\n';
    }
  }
  
  output += '\n' + '='.repeat(60) + '\n';
  output += `Showing top ${searchResult.results.length} of ${searchResult.totalResults} results.\n`;
  output += `Use \`node index.js section "file.md" "Section Title"\` to get full section.`;
  
  return output;
}

// CLI handling
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command || command === 'help' || command === '--help' || command === '-h') {
    console.log(`
OpenClaw Course Search
Searchable reference for the OpenClaw Masterclass

Usage:
  node index.js search "query"            Search course content
  node index.js list                      List all modules  
  node index.js section "file" "title"    Get specific section
  node index.js help                      Show this help

Examples:
  node index.js search "install OpenClaw"
  node index.js search "SOUL.md example"
  node index.js search "VPS setup"
  node index.js search "cost optimization"
  node index.js section "02-THE-SOUL-ARCHITECTURE.md" "SOUL.md Structure"
`);
    return;
  }
  
  if (command === 'list') {
    const modules = listModules();
    console.log('OpenClaw Masterclass Modules:\n');
    for (const m of modules) {
      console.log(`${m.file.replace('.md', '')}`);
      console.log(`  Name: ${m.name}`);
      console.log(`  Topics: ${m.topics.slice(0, 5).join(', ')}${m.topics.length > 5 ? '...' : ''}`);
      console.log();
    }
    return;
  }
  
  if (command === 'search') {
    const query = args.slice(1).join(' ');
    const result = search(query, { limit: 5 });
    console.log(formatResults(result));
    return;
  }
  
  if (command === 'section') {
    const file = args[1];
    const title = args.slice(2).join(' ');
    const result = getSection(file, title);
    
    if (result.error) {
      console.log(`Error: ${result.error}`);
      return;
    }
    
    console.log(result.content);
    console.log(`\n---\nSource: ${result.module}, line ${result.line}`);
    return;
  }
  
  console.log(`Unknown command: ${command}`);
  console.log('Use "node index.js help" for usage information.');
}

// Export for use as module
module.exports = {
  search,
  getSection,
  listModules,
  formatResults,
  parseMarkdown
};

// Run CLI if executed directly
if (require.main === module) {
  main();
}
