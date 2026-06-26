const http = require('http');

const secret = 'ff62c2da-1504-446b-986f-f13ba034e8a5';
const port = 61222;

function request(path, method = 'GET', body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: '127.0.0.1',
      port: port,
      path: path,
      method: method,
      headers: {
        'Authorization': `Bearer ${secret}`,
        'Content-Type': 'application/json'
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch(e) {
          resolve(data);
        }
      });
    });

    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function run(command) {
  const args = command.toLowerCase();
  
  // 状态查询
  if (args.includes('状态') || args.includes('status') || args.includes('查看')) {
    try {
      const configs = await request('/configs');
      const proxies = await request('/proxies');
      return `=== Clash 状态 ===\n🟢 运行中\n代理端口: ${configs['mixed-port']}\nGLOBAL: ${proxies.proxies.GLOBAL.now}\n自动选择: ${proxies.proxies['自动选择'].now}`;
    } catch(e) {
      return '❌ Clash 未运行或 API 不可用';
    }
  }
  
  // 开启代理
  if (args.includes('开启') || args.includes('启动') || args.includes('开') || 
      args.includes('on') || args.includes('打开') || args.includes('代理开启')) {
    try {
      await request('/proxies/GLOBAL', 'PUT', { name: '自动选择' });
      return '✅ 已开启代理（自动选择）';
    } catch(e) {
      return '❌ 开启失败: ' + e.message;
    }
  }
  
  // 关闭代理
  if (args.includes('关闭') || args.includes('停止') || args.includes('关') || 
      args.includes('off') || args.includes('代理关闭')) {
    try {
      await request('/proxies/GLOBAL', 'PUT', { name: 'DIRECT' });
      return '✅ 已关闭代理（DIRECT）';
    } catch(e) {
      return '❌ 关闭失败: ' + e.message;
    }
  }
  
  // 切换节点
  if (args.includes('切换') || args.includes('换') || args.includes('节点')) {
    try {
      await request('/proxies/GLOBAL', 'PUT', { name: '自动选择' });
      return '✅ 已切换到自动选择';
    } catch(e) {
      return '❌ 切换失败: ' + e.message;
    }
  }
  
  // 获取节点列表
  if (args.includes('节点') || args.includes('list') || args.includes('列表')) {
    try {
      const proxies = await request('/proxies');
      const list = proxies.proxies['自动选择'].all.slice(0, 10).join('\n');
      return `=== 可用节点 ===\n${list}\n...`;
    } catch(e) {
      return '❌ 获取失败: ' + e.message;
    }
  }
  
  return `📖 Clash Controller 用法:
- 开启代理 / 启动 Clash
- 关闭代理 / 停止 Clash  
- 状态 / 查看代理
- 切换节点 / 节点列表`;
}

module.exports = { run };
