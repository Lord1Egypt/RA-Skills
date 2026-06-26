# ClawHub API Fallback | ClawHub 备用发布

> 当 `clawhub publish` 返回 502 错误时，可通过 Node.js 直接调用 ClawHub API 发布。

## 使用方法

将占位符替换为实际值后执行：

- `<skill-name>` → SKILL.md 的 `name`
- `<displayName>` → SKILL.md 的 `displayName`
- 版本号、changelog → 本次发布对应值
- `folder` → skill 仓库的本地绝对路径

```bash
node -e "
const fs = require('fs');
const path = require('path');
const os = require('os');
const configPath = path.join(process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming'), 'clawhub', 'config.json');
const TOKEN = JSON.parse(fs.readFileSync(configPath, 'utf8')).token;

const folder = '/path/to/<skill-name>';
const files = [];
function walk(dir, prefix='') {
  for (const f of fs.readdirSync(dir, {withFileTypes: true})) {
    const full = path.join(dir, f.name);
    const rel = prefix ? prefix + '/' + f.name : f.name;
    if (f.name === '.git' || f.name === 'node_modules' || f.name === '.claude-plugin') continue;
    if (f.isDirectory()) walk(full, rel);
    else if (rel.split('.').pop().match(/^(md|json|yaml|yml|js|ts|py|sh|txt|toml|css|html|svg|xml|csv|env|ini|cfg)$/)) {
      files.push({ relPath: rel, bytes: fs.readFileSync(full) });
    }
  }
}
walk(folder);

const form = new FormData();
form.set('payload', JSON.stringify({
  slug: '<skill-name>',
  displayName: '<displayName>',
  version: '1.2.0',
  changelog: 'description of changes',
  acceptLicenseTerms: true,
  tags: ['latest']
}));
for (const f of files) form.append('files', new Blob([f.bytes], {type: 'text/plain'}), f.relPath);

fetch('https://clawhub.ai/api/v1/skills', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/json' },
  body: form
}).then(async r => {
  const data = await r.json();
  console.log(r.ok ? 'OK ' + data.versionId : JSON.stringify(data));
});
"
```

## 说明

- 脚本读取 ClawHub 配置中的 token 鉴权（Windows: `%APPDATA%\clawhub\config.json`，其他: `~/.config/clawhub/config.json`）
- 仅上传文本类文件（按扩展名白名单过滤），跳过 `.git`、`node_modules` 和 `.claude-plugin`
- `tags: ['latest']` 标记为最新版本
- `acceptLicenseTerms: true` 必须保留
