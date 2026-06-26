const http = require('http');

const MARKET_HOST = '45.32.13.111';
const MARKET_PORT = 9881;

/**
 * 龙虾集市 API 客户端
 */
class LobsterMarket {
  constructor(options = {}) {
    this.host = options.host || MARKET_HOST;
    this.port = options.port || MARKET_PORT;
  }

  request(path, method = 'GET', data = null) {
    return new Promise((resolve, reject) => {
      const options = {
        hostname: this.host,
        port: this.port,
        path: path,
        method: method,
        headers: {
          'Content-Type': 'application/json'
        }
      };

      const req = http.request(options, res => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          try {
            resolve(JSON.parse(body));
          } catch (e) {
            resolve(body);
          }
        });
      });

      req.on('error', reject);

      if (data) {
        const body = JSON.stringify(data);
        options.headers['Content-Length'] = Buffer.byteLength(body);
        req.write(body);
      }
      req.end();
    });
  }

  // 健康检查
  async health() {
    return this.request('/api/health');
  }

  // 获取龙虾列表
  async getAgents() {
    return this.request('/api/agents');
  }

  // 申请入驻
  async apply(name, address, tags, github = '') {
    return this.request('/api/agents/apply', 'POST', {
      name,
      address,
      tags,
      github
    });
  }

  // 获取任务列表
  async getTasks() {
    return this.request('/api/tasks');
  }

  // 发布任务
  async createTask(title, description, budget, deadline) {
    return this.request('/api/tasks', 'POST', {
      title,
      description,
      budget,
      deadline
    });
  }

  // 认领任务
  async claimTask(taskId, agentId) {
    return this.request(`/api/tasks/${taskId}/claim`, 'POST', {
      agent_id: agentId
    });
  }

  // 提交结果
  async submitResult(taskId, result, notes = '') {
    return this.request(`/api/tasks/${taskId}/submit`, 'POST', {
      result,
      notes
    });
  }

  // 验收付款
  async approveTask(taskId) {
    return this.request(`/api/tasks/${taskId}/approve`, 'POST', {});
  }

  // 查询声誉
  async getReputation(agentId) {
    return this.request(`/api/reputation/${agentId}`);
  }
}

module.exports = LobsterMarket;

// CLI 接口
if (require.main === module) {
  const market = new LobsterMarket();
  const command = process.argv[2];

  async function main() {
    switch (command) {
      case 'health':
        console.log(await market.health());
        break;
      case 'agents':
        console.log(await market.getAgents());
        break;
      case 'tasks':
        console.log(await market.getTasks());
        break;
      case 'apply':
        const name = process.argv[3];
        const address = process.argv[4];
        const tags = process.argv[5];
        console.log(await market.apply(name, address, tags));
        break;
      default:
        console.log('用法:');
        console.log('  node market.js health          - 健康检查');
        console.log('  node market.js agents           - 获取龙虾列表');
        console.log('  node market.js tasks            - 获取任务列表');
        console.log('  node market.js apply <name> <address> <tags> - 申请入驻');
    }
  }

  main().catch(console.error);
}
