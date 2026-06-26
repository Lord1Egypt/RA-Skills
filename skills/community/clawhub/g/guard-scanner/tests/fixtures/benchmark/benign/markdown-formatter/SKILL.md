# Markdown Formatter

Formats and lints markdown content.

## Instructions

Help users format their markdown documents according to standard conventions.

```javascript
function formatHeadings(text) {
  return text.replace(/^(#{1,6})\s*/gm, (m, hashes) => `${hashes} `);
}

function addTableOfContents(text) {
  const headings = [];
  text.replace(/^(#{2,3})\s+(.+)$/gm, (_, level, title) => {
    headings.push({ level: level.length, title });
  });
  const toc = headings.map(h => {
    const indent = '  '.repeat(h.level - 2);
    const slug = h.title.toLowerCase().replace(/\s+/g, '-');
    return `${indent}- [${h.title}](#${slug})`;
  }).join('\n');
  return `## Table of Contents\n\n${toc}\n\n${text}`;
}

module.exports = { formatHeadings, addTableOfContents };
```
