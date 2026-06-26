const fs = require('fs');
const path = require('path');

function getMemoryFile() {
  return path.join(process.env.HOME || require('os').homedir(), '.openclaw', 'workspace', 'MEMORY.md');
}

function extractDecisions(text) {
  const decisions = [];
  const patterns = [
    /decided to\s+(.+?)(?:\.|$)/gi,
    /agreed (?:on|to)\s+(.+?)(?:\.|$)/gi,
    /will\s+(.+?)(?:\.|$)/gi,
    /built\s+(.+?)(?:\.|$)/gi,
    /created\s+(.+?)(?:\.|$)/gi,
    /installed\s+(.+?)(?:\.|$)/gi,
    /fixed\s+(.+?)(?:\.|$)/gi,
  ];
  
  for (const pattern of patterns) {
    let match;
    const textCopy = text;
    while ((match = pattern.exec(textCopy)) !== null) {
      const content = match[1].trim();
      if (content.length > 10 && content.length < 300) {
        decisions.push(content);
      }
    }
  }
  return [...new Set(decisions)];
}

function syncToMemory(date, decisions) {
  if (!decisions.length) return 0;
  
  const memoryFile = getMemoryFile();
  
  if (!fs.existsSync(memoryFile)) {
    fs.writeFileSync(memoryFile, '# MEMORY.md - Long-Term Memory\n\n_Curated memories._\n\n');
  }
  
  let content;
  try {
    content = fs.readFileSync(memoryFile, 'utf-8');
  } catch {
    content = '# MEMORY.md - Long-Term Memory\n\n';
  }
  
  const header = '## Auto-Captured';
  const entries = decisions.map(d => `- **[${date}]** ${d}`).join('\n');
  
  if (content.includes(header)) {
    const idx = content.indexOf(header);
    content = content.slice(0, idx + header.length) + '\n' + entries + '\n' + content.slice(idx + header.length);
  } else {
    content += `\n${header}\n\n${entries}\n`;
  }
  
  fs.writeFileSync(memoryFile, content);
  return decisions.length;
}

module.exports = { extractDecisions, syncToMemory };
