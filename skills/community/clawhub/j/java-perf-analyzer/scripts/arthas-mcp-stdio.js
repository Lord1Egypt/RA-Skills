#!/usr/bin/env node
/**
 * Arthas MCP Server - Stdio mode (本地 wrapper，连接远程 Arthas HTTP API)
 * 用法: mcporter.json 中配置此脚本作为 MCP Server
 */

const readline = require('readline');
const http = require('http');

// 远程 Arthas 配置（通过 SSH 隧道访问）
const ARTHAS_HOST = process.env.ARTHAS_HOST || 'localhost';
const ARTHAS_PORT = process.env.ARTHAS_PORT || 8563;

// 执行 Arthas 命令
function executeArthasCommand(command) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      action: 'exec',
      command: command
    });

    const options = {
      hostname: ARTHAS_HOST,
      port: ARTHAS_PORT,
      path: '/api',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      },
      timeout: 30000
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve(parsed.body?.results?.[0] || parsed.body || parsed);
        } catch (e) {
          resolve({ raw: data });
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Arthas API timeout'));
    });
    req.write(postData);
    req.end();
  });
}

// MCP 工具定义
const tools = [
  {
    name: 'jvm_info',
    description: '获取 JVM 基本信息（内存、GC、线程、类加载）',
    inputSchema: { type: 'object', properties: {} }
  },
  {
    name: 'thread_info',
    description: '查看线程状态，支持 -n 限制数量或指定线程ID',
    inputSchema: {
      type: 'object',
      properties: {
        threadId: { type: 'string', description: '线程ID或"-n N"取最忙N个' }
      }
    }
  },
  {
    name: 'memory_info',
    description: '查看内存详细信息（堆各区、非堆、缓冲池）',
    inputSchema: { type: 'object', properties: {} }
  },
  {
    name: 'class_info',
    description: '搜索类信息',
    inputSchema: {
      type: 'object',
      properties: {
        className: { type: 'string', description: '类名或通配符如 *Service' }
      },
      required: ['className']
    }
  },
  {
    name: 'method_trace',
    description: '追踪方法执行耗时',
    inputSchema: {
      type: 'object',
      properties: {
        classMethod: { type: 'string', description: '格式: Class#method' },
        condition: { type: 'string', description: '条件如 "#cost > 100"' }
      },
      required: ['classMethod']
    }
  },
  {
    name: 'watch_method',
    description: '监控方法参数和返回值',
    inputSchema: {
      type: 'object',
      properties: {
        classMethod: { type: 'string', description: '格式: Class#method' },
        watchExpr: { type: 'string', description: '表达式如 "{params, returnObj, #cost}"' }
      },
      required: ['classMethod']
    }
  },
  {
    name: 'decompile_class',
    description: '反编译类查看源码',
    inputSchema: {
      type: 'object',
      properties: {
        className: { type: 'string', description: '完整类名' }
      },
      required: ['className']
    }
  },
  {
    name: 'stack_trace',
    description: '查看方法调用来源',
    inputSchema: {
      type: 'object',
      properties: {
        classMethod: { type: 'string', description: '格式: Class#method' }
      },
      required: ['classMethod']
    }
  },
  {
    name: 'profiler',
    description: 'CPU/内存火焰图采样',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', enum: ['start', 'stop', 'status'], description: '动作' },
        event: { type: 'string', default: 'cpu', description: '事件类型: cpu/alloc/lock' },
        duration: { type: 'number', default: 30, description: '采样时长（秒）' }
      },
      required: ['action']
    }
  },
  {
    name: 'heapdump',
    description: '生成堆转储文件',
    inputSchema: {
      type: 'object',
      properties: {
        path: { type: 'string', description: '转储文件路径如 /tmp/dump.hprof' }
      },
      required: ['path']
    }
  },
  {
    name: 'arthas_command',
    description: '执行任意 Arthas 命令',
    inputSchema: {
      type: 'object',
      properties: {
        command: { type: 'string', description: '完整 Arthas 命令' }
      },
      required: ['command']
    }
  }
];

// 工具处理
async function handleToolCall(toolName, args) {
  let command = '';

  switch (toolName) {
    case 'jvm_info':
      command = 'jvm';
      break;
    case 'thread_info':
      command = args.threadId ? `thread ${args.threadId}` : 'thread -n 5';
      break;
    case 'memory_info':
      command = 'memory';
      break;
    case 'class_info':
      command = `sc -d ${args.className}`;
      break;
    case 'method_trace':
      command = args.condition
        ? `trace ${args.classMethod} "${args.condition}" -n 5`
        : `trace ${args.classMethod} -n 5`;
      break;
    case 'watch_method':
      const expr = args.watchExpr || '{params, returnObj, #cost}';
      command = `watch ${args.classMethod} "${expr}" -n 5 -x 2`;
      break;
    case 'decompile_class':
      command = `jad ${args.className}`;
      break;
    case 'stack_trace':
      command = `stack ${args.classMethod} -n 5`;
      break;
    case 'profiler':
      if (args.action === 'start') {
        command = `profiler start --event ${args.event || 'cpu'} --duration ${args.duration || 30}`;
      } else if (args.action === 'stop') {
        command = 'profiler stop --format html';
      } else {
        command = 'profiler status';
      }
      break;
    case 'heapdump':
      command = `heapdump ${args.path}`;
      break;
    case 'arthas_command':
      command = args.command;
      break;
    default:
      return { error: `Unknown tool: ${toolName}` };
  }

  try {
    const result = await executeArthasCommand(command);
    return result;
  } catch (error) {
    return { error: error.message };
  }
}

// Stdio MCP 处理
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

rl.on('line', async (line) => {
  try {
    const msg = JSON.parse(line);

    if (msg.method === 'initialize') {
      respond({
        jsonrpc: '2.0',
        id: msg.id,
        result: {
          protocolVersion: '2024-11-05',
          capabilities: { tools: {} },
          serverInfo: { name: 'arthas-mcp-stdio', version: '1.0.0' }
        }
      });
    } else if (msg.method === 'initialized') {
      // Notification, no response
    } else if (msg.method === 'tools/list') {
      respond({
        jsonrpc: '2.0',
        id: msg.id,
        result: { tools }
      });
    } else if (msg.method === 'tools/call') {
      const result = await handleToolCall(msg.params?.name, msg.params?.arguments || {});
      respond({
        jsonrpc: '2.0',
        id: msg.id,
        result: {
          content: [{
            type: 'text',
            text: typeof result === 'string' ? result : JSON.stringify(result, null, 2)
          }]
        }
      });
    } else {
      respond({
        jsonrpc: '2.0',
        id: msg.id,
        error: { code: -32601, message: `Unknown method: ${msg.method}` }
      });
    }
  } catch (e) {
    // Ignore parse errors
  }
});

function respond(msg) {
  process.stdout.write(JSON.stringify(msg) + '\n');
}