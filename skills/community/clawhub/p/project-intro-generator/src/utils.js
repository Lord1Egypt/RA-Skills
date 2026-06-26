const fs = require('fs');
const path = require('path');

async function pathExists(targetPath) {
  try {
    await fs.promises.access(targetPath, fs.constants.F_OK);
    return true;
  } catch (_) {
    return false;
  }
}

async function readTextFile(targetPath) {
  const exists = await pathExists(targetPath);
  if (!exists) return null;
  return fs.promises.readFile(targetPath, 'utf8');
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${(bytes / Math.pow(k, i)).toFixed(1)} ${sizes[i]}`;
}

function isTextFile(ext) {
  const textExts = new Set([
    '.js', '.ts', '.tsx', '.jsx', '.json', '.md', '.txt', '.yaml', '.yml',
    '.py', '.go', '.java', '.rs', '.rb', '.php', '.c', '.cpp', '.cc',
    '.h', '.hpp', '.m', '.swift', '.kt', '.kts', '.sh', '.bat', '.ps1',
    '.css', '.scss', '.less', '.html'
  ]);
  return textExts.has(ext.toLowerCase());
}

function detectLanguage(ext) {
  const map = {
    '.js': 'JavaScript',
    '.mjs': 'JavaScript',
    '.cjs': 'JavaScript',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript + React',
    '.jsx': 'JavaScript + React',
    '.py': 'Python',
    '.go': 'Go',
    '.rb': 'Ruby',
    '.rs': 'Rust',
    '.php': 'PHP',
    '.java': 'Java',
    '.cs': 'C#',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.c': 'C',
    '.h': 'C/C++ Header',
    '.hpp': 'C++ Header',
    '.m': 'Objective-C',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.kts': 'Kotlin Script',
    '.dart': 'Dart',
    '.scala': 'Scala',
    '.lua': 'Lua',
    '.sh': 'Shell',
    '.bash': 'Shell',
    '.zsh': 'Shell',
    '.ps1': 'PowerShell',
    '.html': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.less': 'Less',
    '.sql': 'SQL',
    '.md': 'Markdown',
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML'
  };
  return map[ext.toLowerCase()] || null;
}

module.exports = {
  pathExists,
  readTextFile,
  formatBytes,
  isTextFile,
  detectLanguage
};
