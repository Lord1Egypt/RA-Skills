const axios = require('axios');

async function main() {
  const nodes = {
    "RTX 3090": "http://192.168.2.236:5000/gpu",
    "RTX 4090": "http://192.168.2.164:5000/gpu"
  };

  const results = [];
  for (const [name, url] of Object.entries(nodes)) {
    try {
      const resp = await axios.get(url, { timeout: 3000 });
      const { used, total } = resp.data;
      const percent = Math.round((used / total) * 1000) / 10;
      
      const barLen = 10;
      const filled = Math.min(Math.floor(percent / 10), barLen);
      const bar = "█".repeat(filled) + "░".repeat(barLen - filled);
      
      const status = percent < 90 ? "🟢" : "🔴";
      results.push(`${status} **${name}** \`[${bar}]\` ${percent}% - 已用: ${used}MB / 总共: ${total}MB`);
    } catch (error) {
      results.push(`⚪️ **${name}** - 节点不在线或 API 未启动`);
    }
  }
  return results.join("\n");
}

module.exports = { main };