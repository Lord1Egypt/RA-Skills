# File Reader Skill

Read and display file contents for the user.

## Instructions

When the user asks to read a file, use the read_file tool:

```javascript
const fs = require('fs');

function readFile(path) {
  return fs.readFileSync(path, 'utf8');
}

module.exports = { readFile };
```
