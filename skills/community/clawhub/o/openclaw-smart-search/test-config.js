// 测试配置脚本
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 读取主密钥
const masterKey = process.env.OPENCLAW_MASTER_KEY || fs.readFileSync('.env', 'utf-8').match(/OPENCLAW_MASTER_KEY=(.+)/)[1];
console.log('✅ 主密钥长度:', masterKey.length);

// 生成盐值
const salt = crypto.randomBytes(16).toString('hex');
console.log('✅ 盐值已生成:', salt);

// 创建配置
const config = {
  version: '2.0',
  salt: salt,
  encryptedKeys: {},
  metadata: {
    owner: 'test',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
};

// 保存配置
const configPath = path.join(process.env.HOME, '.openclaw/secrets/smart-search.json.enc');
fs.writeFileSync(configPath, JSON.stringify(config, null, 2), { mode: 0o600 });
console.log('✅ 配置文件已创建:', configPath);

// 验证权限
const stats = fs.statSync(configPath);
console.log('✅ 文件权限:', (stats.mode & 0o777).toString(8));

console.log('');
console.log('配置完成！现在可以运行 npm run setup 配置 API Keys');
