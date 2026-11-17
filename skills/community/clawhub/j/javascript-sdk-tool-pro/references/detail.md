# 详细参考 - javascript-sdk-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (typescript)

```typescript
import {
    tool, appTool, agentTool, webhookTool,
    string, number, integer, boolean,
    enumOf, array, obj, optional
} from '@ai/sdk';

// 1. 参数类型定义
const name = string('用户名');
const age = integer('年龄');
const score = number('分数 0-1');
const active = boolean('是否活跃');
const priority = enumOf(['low', 'medium', 'high'], '优先级');
const tags = array(string('标签'), '标签列表');
const address = obj({
    street: string('街道'),
    city: string('城市'),
    zip: optional(string('邮编'))
}, '地址');

// 2. 客户端工具（在本地代码中执行）
const greet = tool('greet')
    .display('问候用户')
    .describe('根据名字问候用户')
    .param('name', string('要问候的名字'))
    .requireApproval()  // 需要人工审批
    .build();

// 3. 应用工具（调用其他 AI 应用）
const generate = appTool('generate_image', 'image-gen@latest')
    .describe('根据文字生成图片')
    .param('prompt', string('图片描述'))
    .setup({ model: 'schnell' })
    .input({ steps: 20 })
    .requireApproval()
    .build();

// 4. 代理工具（委托给子智能体）
const researcher = agentTool('research', 'researcher@v1')
    .describe('研究指定主题')
    .param('topic', string('研究主题'))
    .build();

// 5. Webhook 工具（调用外部 API）
const notify = webhookTool('slack', 'https://hooks.slack.com/...')
    .describe('发送 Slack 通知')
    .secret('SLACK_SECRET')
    .param('channel', string('频道'))
    .param('message', string('消息内容'))
    .build();

// 6. 内置工具配置
import { internalTools } from '@ai/sdk';

const config = internalTools()
    .plan()                    // 规划能力
    .memory()                  // 记忆能力
    .webSearch(true)           // 网页搜索
    .codeExecution(true)       // 代码执行
    .imageGeneration({
        enabled: true,
        appRef: 'image-gen@latest'
    })
    .build();

const agent = client.agent({
    core_app: { ref: 'claude-sonnet@latest' },
    internal_tools: config
});
```

## 代码示例 (typescript)

```typescript
const agent = client.agent({
    core_app: { ref: 'claude-sonnet@latest' },
    tools: [dangerousTool],
    system_prompt: '你是一个系统管理助手。'
});

const response = await agent.sendMessage('删除所有临时文件', {
    onToolCall: async (call) => {
        // 检查是否需要审批
        if (call.requiresApproval) {
            // 向用户展示工具调用详情
            const approved = await promptUser(
                `是否允许执行 "${call.name}"？\n参数: ${JSON.stringify(call.args, null, 2)}`
            );

            if (approved) {
                // 执行工具
                const result = await executeTool(call.name, call.args);
                agent.submitToolResult(call.id, result);
            } else {
                // 拒绝执行
                agent.submitToolResult(call.id, { error: '用户拒绝执行' });
            }
        } else {
            // 不需要审批的直接执行
            const result = await executeTool(call.name, call.args);
            agent.submitToolResult(call.id, result);
        }
    }
});

// 用户审批交互函数
async function promptUser(message: string): Promise<boolean> {
    return new Promise((resolve) => {
        // 实际应用中可以连接 UI 组件
        const readline = require('readline').createInterface({
            input: process.stdin,
            output: process.stdout
        });
        readline.question(`${message} (y/n): `, (answer) => {
            readline.close();
            resolve(answer.toLowerCase() === 'y');
        });
    });
}
```

## 代码示例 (typescript)

```typescript
import { createClient, tool, appTool, string, number } from '@ai/sdk';

const client = createClient({ apiKey: process.env.AI_API_KEY });

// 1. 定义自定义工具
const calculator = tool('calculate')
    .describe('执行数学计算')
    .param('expression', string('数学表达式'))
    .build();

// 2. 定义应用工具（调用其他 AI 应用）
const imageGenerator = appTool('generate_image', 'image-gen@latest')
    .describe('根据文字生成图片')
    .param('prompt', string('图片描述'))
    .setup({ model: 'schnell' })
    .build();

// 3. 创建智能体
const agent = client.agent({
    core_app: { ref: 'claude-sonnet@latest' },
    system_prompt: '你是一个有用的助手，可以计算数学问题和生成图片。',
    tools: [calculator, imageGenerator],
    temperature: 0.7,
    max_tokens: 4096
});

// 4. 多轮对话
const response1 = await agent.sendMessage('25 乘以 4 是多少？');
console.log(response1.text);

const response2 = await agent.sendMessage('帮我把这个数字生成一张图片');
console.log(response2.text);

// 5. 重置对话
agent.reset();

// 6. 获取聊天历史
const chat = await agent.getChat();
console.log('历史记录:', chat.messages);
```

## 代码示例 (typescript)

```typescript
// ============ Next.js 代理（App Router）============
// app/api/proxy/route.ts
import { createRouteHandler } from '@ai/sdk/proxy/nextjs';

const route = createRouteHandler({
    apiKey: process.env.AI_API_KEY
});

export const POST = route.POST;

// ============ Express 代理 ============
import express from 'express';
import { createProxyMiddleware } from '@ai/sdk/proxy/express';

const app = express();
app.use('/api/proxy', createProxyMiddleware({
    apiKey: process.env.AI_API_KEY
}));

app.listen(3000);

// ============ Hono 代理 ============
import { Hono } from 'hono';
import { createHonoProxy } from '@ai/sdk/proxy/hono';

const app = new Hono();
app.use('/api/proxy', createHonoProxy({
    apiKey: process.env.AI_API_KEY
}));

// ============ 前端客户端配置 ============
import { createClient } from '@ai/sdk';

const client = createClient({
    proxyUrl: '/api/proxy'
    // 前端不需要 apiKey
});
```

## 代码示例 (typescript)

```typescript
import type {
    TaskDTO,
    ChatDTO,
    ChatMessageDTO,
    AgentTool,
    TaskStatusCompleted,
    TaskStatusFailed,
    TaskStatusRunning
} from '@ai/sdk';

// 类型守卫
function isCompleted(task: TaskDTO): task is TaskStatusCompleted {
    return task.status === 'completed';
}

function isFailed(task: TaskDTO): task is TaskStatusFailed {
    return task.status === 'failed';
}

// 使用类型安全的处理
async function processTask(taskId: string) {
    const task = await client.getTask(taskId);

    if (isCompleted(task)) {
        // task.output 类型安全
        console.log('完成:', task.output);
    } else if (isFailed(task)) {
        // task.error 类型安全
        console.log('失败:', task.error);
    } else {
        // TaskStatusRunning
        console.log('运行中...');
    }
}
```

