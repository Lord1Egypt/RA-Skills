const fs = require('fs');
const path = require('path');

// Default config
const DEFAULT_IGNORE = [
  'node_modules',
  '.git',
  '.openclaw',
  '.DS_Store'
];

/**
 * Recursively find markdown files
 */
function findMarkdownFiles(dir, ignore = DEFAULT_IGNORE) {
  let results = [];
  try {
    const list = fs.readdirSync(dir);
    for (const file of list) {
      if (ignore.includes(file)) continue;
      const filePath = path.join(dir, file);
      let stat;
      try {
        stat = fs.statSync(filePath);
      } catch (e) {
        continue;
      }
      
      if (stat && stat.isDirectory()) {
        results = results.concat(findMarkdownFiles(filePath, ignore));
      } else if (file.endsWith('.md')) {
        results.push(filePath);
      }
    }
  } catch (err) {
    // console.error(`Error reading directory ${dir}:`, err.message);
  }
  return results;
}

/**
 * Check if a file exists
 */
function fileExists(filePath) {
  try {
    return fs.existsSync(filePath);
  } catch (err) {
    return false;
  }
}

/**
 * Validate a single markdown file
 */
function validateFile(filePath, rootDir) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  const errors = [];
  
  // Regex for finding markdown links [text](url)
  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  
  lines.forEach((line, index) => {
    let match;
    while ((match = linkRegex.exec(line)) !== null) {
      const linkText = match[1];
      let linkUrl = match[2];
      
      // Skip external links, anchors, and mailto
      if (linkUrl.startsWith('http') || linkUrl.startsWith('https') || linkUrl.startsWith('mailto:') || linkUrl.startsWith('ftp')) {
        continue;
      }

      // Skip image data URIs
      if (linkUrl.startsWith('data:')) {
        continue;
      }

      // Handle query params or anchors
      linkUrl = linkUrl.split('#')[0].split('?')[0];
      if (!linkUrl) continue; // Was just an anchor
      
      // Resolve path
      let targetPath;
      if (linkUrl.startsWith('/')) {
        // Absolute path from rootDir? Or system root? Usually from project root in docs context
        // Assuming relative to rootDir if starts with /
        targetPath = path.join(rootDir, linkUrl);
      } else {
        // Relative to current file
        targetPath = path.resolve(path.dirname(filePath), linkUrl);
      }
      
      if (!fileExists(targetPath)) {
        errors.push({
          file: filePath,
          line: index + 1,
          link: linkUrl,
          error: `Broken link`
        });
      }
    }
  });

  return errors;
}

/**
 * Main scan function
 */
async function scan(rootDir = '.') {
  const mdFiles = findMarkdownFiles(rootDir);
  const allErrors = [];
  let brokenLinksCount = 0;

  for (const file of mdFiles) {
    const fileErrors = validateFile(file, rootDir);
    if (fileErrors.length > 0) {
      allErrors.push(...fileErrors);
      brokenLinksCount += fileErrors.length;
    }
  }

  return {
    totalFiles: mdFiles.length,
    brokenLinksCount,
    details: allErrors
  };
}

module.exports = {
  scan,
  findMarkdownFiles,
  validateFile
};

// CLI Support if run directly
if (require.main === module) {
  const targetDir = process.argv[2] || '.';
  scan(targetDir).then(report => {
    console.log(JSON.stringify(report, null, 2));
    if (report.brokenLinksCount > 0) process.exit(1);
  }).catch(err => {
    console.error(err);
    process.exit(1);
  });
}
