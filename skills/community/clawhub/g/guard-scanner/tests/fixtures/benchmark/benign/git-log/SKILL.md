# Git Log Viewer

Display git log information in a formatted way.

```javascript
const { execSync } = require('child_process');

function getRecentCommits(n = 10) {
  const output = execSync(`git log --oneline -n ${n}`, { encoding: 'utf8' });
  return output.trim().split('\n').map(line => {
    const [hash, ...msg] = line.split(' ');
    return { hash, message: msg.join(' ') };
  });
}

module.exports = { getRecentCommits };
```
