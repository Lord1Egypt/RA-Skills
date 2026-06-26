/**
 * 养老金计算器 MCP Server
 * 为 LLM 提供调用接口
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} = require('@modelcontextprotocol/sdk/types.js');

// 数据文件路径 - 使用相对路径，确保 Skill 在任何位置都能运行
const DATA_DIR = path.join(__dirname, 'data');
const DATA_FILE = path.join(DATA_DIR, 'user-data.json');
const STATUS_FILE = path.join(DATA_DIR, 'status.json');

// 确保数据目录存在
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
  console.error('Created data directory:', DATA_DIR);
}

console.error('Data file path:', DATA_FILE);
console.error('Status file path:', STATUS_FILE);

// 导入计算模块
const PensionCalculator = require('./js/pensionCalculator.js');
const PensionDataModel = require('./js/pensionData.js');

// Web 服务器实例
let webServer = null;
let serverPort = 8082;

/**
 * 启动 Web 服务器
 */
function startWebServer() {
  return new Promise((resolve, reject) => {
    if (webServer) {
      resolve({ url: `http://localhost:${serverPort}`, alreadyRunning: true });
      return;
    }

    webServer = http.createServer((req, res) => {
      // 设置 CORS
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
      res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

      if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
      }

      // API: 保存数据
      if (req.url === '/api/save-data' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
          try {
            const data = JSON.parse(body);
            fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
            
            // 更新状态文件
            fs.writeFileSync(STATUS_FILE, JSON.stringify({
              status: 'completed',
              lastModified: new Date().toISOString()
            }));
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ success: true }));
          } catch (error) {
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: error.message }));
          }
        });
        return;
      }

      // API: 获取数据
      if (req.url === '/api/get-data' && req.method === 'GET') {
        try {
          if (fs.existsSync(DATA_FILE)) {
            const data = fs.readFileSync(DATA_FILE, 'utf8');
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(data);
          } else {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'No data found' }));
          }
        } catch (error) {
          res.writeHead(500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: error.message }));
        }
        return;
      }

      // API: 获取状态
      if (req.url === '/api/status' && req.method === 'GET') {
        try {
          if (fs.existsSync(STATUS_FILE)) {
            const status = fs.readFileSync(STATUS_FILE, 'utf8');
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(status);
          } else {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'waiting' }));
          }
        } catch (error) {
          res.writeHead(500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: error.message }));
        }
        return;
      }

      // 静态文件服务
      const filePath = req.url === '/' ? '/index.html' : req.url;
      const fullPath = path.join(__dirname, filePath);
      
      try {
        if (fs.existsSync(fullPath) && fs.statSync(fullPath).isFile()) {
          const ext = path.extname(fullPath);
          const contentType = {
            '.html': 'text/html',
            '.js': 'application/javascript',
            '.css': 'text/css',
            '.json': 'application/json'
          }[ext] || 'text/plain';
          
          const content = fs.readFileSync(fullPath);
          res.writeHead(200, { 'Content-Type': contentType });
          res.end(content);
        } else {
          res.writeHead(404);
          res.end('Not found');
        }
      } catch (error) {
        res.writeHead(500);
        res.end('Server error');
      }
    });

    webServer.listen(serverPort, () => {
      console.error(`Web server running at http://localhost:${serverPort}`);
      resolve({ url: `http://localhost:${serverPort}`, alreadyRunning: false });
    });

    webServer.on('error', (err) => {
      if (err.code === 'EADDRINUSE') {
        // 端口被占用，尝试其他端口
        serverPort++;
        webServer.listen(serverPort);
      } else {
        reject(err);
      }
    });
  });
}

/**
 * 读取用户数据
 */
function readUserData() {
  try {
    console.error('Reading data from:', DATA_FILE);
    console.error('File exists:', fs.existsSync(DATA_FILE));
    
    if (fs.existsSync(DATA_FILE)) {
      const data = fs.readFileSync(DATA_FILE, 'utf8');
      console.error('Data file content length:', data.length);
      const parsed = JSON.parse(data);
      console.error('Successfully parsed data');
      return parsed;
    } else {
      console.error('Data file not found');
    }
  } catch (e) {
    console.error('Error reading user data:', e);
  }
  return null;
}

/**
 * 生成分析报告
 */
function generateReport(data) {
  const pensionData = PensionDataModel.create(data);
  const results = PensionCalculator.calculate(pensionData);
  const { summary, details } = results;
  
  let lifestyleText = '开支缩减';
  let lifestyleEmoji = '⚠️';
  if (summary.replacementRate >= 70) {
    lifestyleText = '开支宽裕';
    lifestyleEmoji = '✅';
  } else if (summary.replacementRate >= 55) {
    lifestyleText = '平衡';
    lifestyleEmoji = '✓';
  }
  
  const suggestions = [];
  if (summary.replacementRate < 55) {
    suggestions.push('• 退休后收入显著下降，建议增加养老储蓄或个人养老金投入');
    suggestions.push('• 考虑延迟退休以增加缴费年限');
    suggestions.push('• 提高个人养老金年存入金额');
  } else if (summary.replacementRate < 70) {
    suggestions.push('• 退休收入基本充足，可适当优化投资组合');
    suggestions.push('• 保持当前的储蓄计划');
  } else {
    suggestions.push('• 退休收入充足，可以维持较好的生活品质');
    suggestions.push('• 可考虑适当提高当前生活品质');
    suggestions.push('• 多余资金可用于稳健投资或子女教育');
  }
  
  return {
    summary: `📊 养老金分析报告
═══════════════════════════════════

💰 退休收入总览
每月可领取：${summary.totalMonthly.toLocaleString()} 元
相当于现在：${summary.currentValue.toLocaleString()} 元
替代率：${summary.replacementRate}%

📈 详细构成
1️⃣ 基本养老金：${Math.round(details.basicPension.monthly).toLocaleString()} 元/月
   ├─ 个人账户：${Math.round(details.basicPension.personalMonthly).toLocaleString()} 元/月
   └─ 统筹账户：${Math.round(details.basicPension.poolMonthly).toLocaleString()} 元/月

2️⃣ 企业年金：${Math.round(details.enterprisePension.monthly).toLocaleString()} 元/月

3️⃣ 个人养老金：${Math.round(details.personalPension.monthly).toLocaleString()} 元/月
   └─ 退休时账户：${Math.round(details.personalPension.totalBalance).toLocaleString()} 元

4️⃣ 养老储蓄：${Math.round(details.savingsPension.monthly).toLocaleString()} 元/月
   └─ 退休时累计：${Math.round(details.savingsPension.totalBalance).toLocaleString()} 元

5️⃣ 未来计划：${Math.round(details.futurePension.monthly).toLocaleString()} 元/月
   └─ 退休时累计：${Math.round(details.futurePension.totalBalance).toLocaleString()} 元

🎯 退休生活水平评估
状态：${lifestyleEmoji} ${lifestyleText}

═══════════════════════════════════

💡 建议：
${suggestions.join('\n')}

═══════════════════════════════════

需要调整哪些数据吗？您可以说：
• "修改退休年龄为60岁"
• "增加企业年金到10万"
• "重新打开网页修改"
• "保存报告"`,
    data: results
  };
}

/**
 * 更新参数
 */
function updateParameter(param, value) {
  const data = readUserData() || PensionDataModel.create();
  
  // 解析参数路径，如 "profile.currentAge"
  const keys = param.split('.');
  let target = data;
  for (let i = 0; i < keys.length - 1; i++) {
    target = target[keys[i]];
  }
  target[keys[keys.length - 1]] = value;
  
  // 保存更新后的数据
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
  
  // 重新计算
  return generateReport(data);
}

// 创建 MCP Server
const server = new Server(
  {
    name: 'pension-calculator',
    version: '1.2.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 注册工具列表
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'start_web_ui',
        description: '启动养老金计算器Web界面，让用户在浏览器中填写数据',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'generate_report',
        description: '读取用户填写的数据并生成养老金分析报告。可以从文件读取数据，也可以直接传入数据对象。',
        inputSchema: {
          type: 'object',
          properties: {
            data: {
              type: 'object',
              description: '可选。直接传入养老金数据对象，如果不传则从文件读取。',
              properties: {
                profile: {
                  type: 'object',
                  properties: {
                    currentAge: { type: 'number' },
                    retirementAge: { type: 'number' }
                  }
                },
                socialSecurity: {
                  type: 'object',
                  properties: {
                    paidMonths: { type: 'number' },
                    currentBalance: { type: 'number' },
                    monthlyBase: { type: 'number' },
                    avgWage: { type: 'number' }
                  }
                },
                personalPension: {
                  type: 'object',
                  properties: {
                    balance: { type: 'number' },
                    annualDeposit: { type: 'number' },
                    returnRate: { type: 'number' }
                  }
                },
                savings: {
                  type: 'object',
                  properties: {
                    amount: { type: 'number' },
                    returnRate: { type: 'number' }
                  }
                }
              }
            }
          },
          required: []
        }
      },
      {
        name: 'update_parameter',
        description: '修改养老金计算的特定参数并重新生成报告',
        inputSchema: {
          type: 'object',
          properties: {
            param: {
              type: 'string',
              description: '参数路径，如 "profile.retirementAge", "socialSecurity.currentBalance"'
            },
            value: {
              type: 'number',
              description: '新的数值'
            }
          },
          required: ['param', 'value']
        }
      },
      {
        name: 'check_status',
        description: '检查用户是否已完成Web界面的数据填写',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      }
    ]
  };
});

// 注册工具处理器
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  try {
    switch (name) {
      case 'start_web_ui': {
        const result = await startWebServer();
        return {
          content: [
            {
              type: 'text',
              text: result.alreadyRunning 
                ? `养老金计算器已在运行：${result.url}\n\n请在浏览器中打开上方链接，填写您的养老金信息。\n填写完成后，请告诉我"已完成"，我将为您生成分析报告。`
                : `🚀 养老金计算器已启动！\n\n请访问：${result.url}\n\n请在浏览器中填写您的养老金信息，包括：\n• 基本信息（年龄、退休年龄）\n• 社保信息（已缴月数、账户余额、缴费基数）\n• 企业年金（如有）\n• 个人养老金\n• 养老储蓄\n\n填写完成后，点击"保存数据"按钮，然后告诉我"已完成"，我将为您生成详细的养老金分析报告。`
            }
          ]
        };
      }
      
      case 'generate_report': {
        // 优先使用传入的数据，如果没有则尝试读取文件
        let data = args.data || null;
        
        if (!data) {
          data = readUserData();
        }
        
        if (!data) {
          return {
            content: [
              {
                type: 'text',
                text: '❌ 未找到用户数据。\n\n请使用以下方式之一提供数据：\n\n方式1：调用 start_web_ui 启动网页界面填写数据\n方式2：在调用 generate_report 时传入 data 参数\n方式3：直接告诉我您的养老金信息，例如：\n"我已填写完成，当前35岁，63岁退休，社保已缴301个月，余额38.4万..."'
              }
            ]
          };
        }
        
        // 如果传入了数据，先保存到文件
        if (args.data) {
          fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
          fs.writeFileSync(STATUS_FILE, JSON.stringify({
            status: 'completed',
            lastModified: new Date().toISOString()
          }));
        }
        
        const report = generateReport(data);
        return {
          content: [
            {
              type: 'text',
              text: report.summary
            }
          ]
        };
      }
      
      case 'update_parameter': {
        const { param, value } = args;
        const report = updateParameter(param, value);
        return {
          content: [
            {
              type: 'text',
              text: `✅ 已更新 ${param} 为 ${value}\n\n${report.summary}`
            }
          ]
        };
      }
      
      case 'check_status': {
        try {
          if (fs.existsSync(STATUS_FILE)) {
            const status = JSON.parse(fs.readFileSync(STATUS_FILE, 'utf8'));
            if (status.status === 'completed') {
              return {
                content: [
                  {
                    type: 'text',
                    text: '✅ 用户已完成数据填写，可以生成报告了。\n\n请调用 generate_report 生成养老金分析报告。'
                  }
                ]
              };
            }
          }
          return {
            content: [
              {
                type: 'text',
                text: '⏳ 用户尚未完成数据填写。\n\n请等待用户在Web界面填写完成并点击"保存数据"按钮。'
              }
            ]
          };
        } catch (e) {
          return {
            content: [
              {
                type: 'text',
                text: '⏳ 等待用户填写数据中...'
              }
            ]
          };
        }
      }
      
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `❌ 错误：${error.message}`
        }
      ],
      isError: true
    };
  }
});

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Pension Calculator MCP Server running on stdio');
}

main().catch(console.error);
