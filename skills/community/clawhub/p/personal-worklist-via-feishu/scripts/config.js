/**
 * 飞书 API 凭证配置
 *
 * APP_ID / APP_SECRET: 自动从 OpenClaw 配置读取
 * APP_TOKEN / TABLE_ID: 用户安装后自行配置（运行 node scripts/set_config.js --app-token XXX --table-id XXX）
 *
 * 凭证说明:
 *   - APP_ID: 飞书应用的 App ID，从 OpenClaw 配置自动读取
 *   - APP_SECRET: 飞书应用的 App Secret，从 OpenClaw 配置自动读取
 *   - APP_TOKEN: 多维表格的唯一标识，从飞书多维表格 URL 中提取
 *   - TABLE_ID: 数据表的 ID，从飞书多维表格 URL 中提取
 *   - 示例 URL: https://xxx.feishu.cn/base/APP_TOKEN?table=TABLE_ID
 */

const fs = require('fs');
const path = require('path');

const CONFIG = {
  // 从 OpenClaw 配置自动读取，或环境变量
  APP_ID: process.env.FEISHU_APP_ID || '',
  APP_SECRET: process.env.FEISHU_APP_SECRET || '',
  // 用户安装后通过 node scripts/set_config.js 配置
  APP_TOKEN: '',
  TABLE_ID: ''
};

// 自动从 OpenClaw 配置读取 APP_ID 和 APP_SECRET
function loadOpenClawConfig() {
  try {
    // 向上查找最多 4 层目录
    let dir = __dirname;
    for (let i = 0; i < 5; i++) {
      const configPath = path.join(dir, 'openclaw.json');
      if (fs.existsSync(configPath)) {
        const data = JSON.parse(fs.readFileSync(configPath, 'utf8'));
        const feishu = data?.channels?.feishu;
        if (feishu?.appId && feishu?.appSecret) {
          CONFIG.APP_ID = feishu.appId;
          CONFIG.APP_SECRET = feishu.appSecret;
          return;
        }
      }
      dir = path.dirname(dir);
    }
  } catch (e) {
    // 忽略，继续使用环境变量
  }
}

// 如果环境变量中有凭证，优先使用
if (process.env.FEISHU_APP_ID) CONFIG.APP_ID = process.env.FEISHU_APP_ID;
if (process.env.FEISHU_APP_SECRET) CONFIG.APP_SECRET = process.env.FEISHU_APP_SECRET;

// 如果环境变量没有，尝试从 OpenClaw 配置读取
if (!CONFIG.APP_ID || !CONFIG.APP_SECRET) {
  loadOpenClawConfig();
}

module.exports = { CONFIG };
