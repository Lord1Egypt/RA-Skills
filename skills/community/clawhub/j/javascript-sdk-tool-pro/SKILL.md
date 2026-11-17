---

slug: javascript-sdk-tool-pro
name: "javascript-sdk-tool-pro"
version: "1.0.0"
displayName: "JS SDK工具专业版"
summary: "企业级 AI 应用 SDK 方案，支持智能体构建、流式响应、会话管理与服务器代理集成。。面向企业级 AI 应用开发的 JavaScript SDK 专业工具，提供智能体构建与高级调用能力。核"
license: "Proprietary"
edition: "pro"
description: |-
  面向企业级 AI 应用开发的 JavaScript SDK 专业工具，提供智能体构建与高级调用能力。核心能力:
  - 智能体（Agent）构建与多轮对话
  - 流式响应与实时进度更新
  - 会话管理与有状态执行
  - 工具构建器 API（自定义工具/应用工具/代理工具）
  - 服务器代理集成（Next。Use when 需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于需要100%确定性的关键决策。
tags:
  - 开发工具
  - JavaScript
  - AI应用
  - 智能体
  - 企业开发
  - 工具
  - 效率
  - 写作
  - 电商
  - const
  - await
  - update
  - 流式响应
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"

---

> **功能说明**: 本技能涵盖 与有状态执行 等核心能力。


本工具面向企业级 AI 应用开发团队，提供智能体构建、流式响应、会话管理、工具构建器与服务器代理集成的完整方案。在免费版基础应用调用与文件上传能力之上，专业版新增 Agent SDK、流式响应处理、有状态会话、自定义工具构建、多框架代理集成、人工审批工作流等能力。通过丰富的 API 与类型安全支持，帮助团队构建生产级 AI 智能体应用.
**版本兼容性说明**：专业版完全兼容免费版（`javascript-sdk-tool-free`）的所有基础调用、认证配置与文件上传能力，可无缝升级.
## 核心能力
| 能力模块 | 免费版 | 专业版新增 |
|----|---|-----|
| 应用调用 | 基础 run/getTask | 流式响应 + 进度回调 |
| 智能体 | - | Agent 构建 + 多轮对话 |
| 会话管理 | - | 有状态执行 + 会话保持 |
| 工具系统 | - | 工具构建器 API |
| 文件处理 | 基础上传 | 附件处理 + 多格式支持 |
| 代理集成 | 基础代理 | Next.js/Express/Hono/Remix/SvelteKit |
| 审批流程 | - | 人工审批工作流 |
| 类型安全 | 基础类型 | 完整类型定义 + 类型守卫 |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级、SDK、支持智能体构建、会话管理与服务器、面向企业级、应用开发的、JavaScript、专业工具、提供智能体构建与、高级调用能力、核心能力、构建与多轮对话、流式响应与实时进、度更新、会话管理与有状态、自定义工具、应用工具、代理工具、服务器代理集成等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景
### 场景一：构建自定义智能体
团队需要构建一个带有自定义工具的 AI 智能体.
> 详细代码示例已移至 `references/detail.md`

### 场景二：流式响应处理
应用需要实时显示 AI 响应的生成过程.
```typescript
const agent = client.agent({
    core_app: { ref: 'claude-sonnet@latest' },
    system_prompt: '你是一个技术讲解助手。'
});
// ...
// 流式响应
const response = await agent.sendMessage('解释量子计算的基本原理', {
    onMessage: (msg) => {
        // 实时输出内容
        if (msg.content) {
            process.stdout.write(msg.content);
        }
    },
    onToolCall: async (call) => {
        // 工具调用回调
        console.log(`\n[工具调用: ${call.name}]`);
        console.log('参数:', call.args);
// ...
        // 执行工具并返回结果
        const result = await executeTool(call.name, call.args);
        agent.submitToolResult(call.id, result);
    }
});
// ...
console.log('\n\n完整响应:', response.text);
```

```typescript
// 流式应用调用（进度更新）
const stream = await client.run({
    app: 'video-generator',
    input: { prompt: '海浪日落' }
}, { stream: true });
// ...
for await (const update of stream) {
    console.log(`状态: ${update.status}`);
// ...
    if (update.logs?.length) {
        const lastLog = update.logs[update.logs.length - 1];
        console.log('日志:', lastLog);
    }
// ...
    if (update.status === 'completed') {
        console.log('输出:', update.output);
    }
}
```

### 场景三：有状态会话管理
应用需要在多次调用间保持会话状态.
```typescript
// 1. 创建新会话
const result1 = await client.run({
    app: 'my-app',
    input: { action: 'init', user_id: 'user123' },
    session: 'new',
    session_timeout: 300  // 5 分钟空闲超时
});
// ...
const sessionId = result1.session_id;
console.log('会话 ID:', sessionId);
// ...
// 2. 在同一会话中继续
const result2 = await client.run({
    app: 'my-app',
    input: { action: 'process', data: '...' },
    session: sessionId  // 复用会话
});
// ...
// 3. 会话保持工作器热度，避免冷启动
const result3 = await client.run({
    app: 'my-app',
    input: { action: 'query', question: '...' },
    session: sessionId
});
// ...
// 4. 会话超时后自动清理
// session_timeout 控制空闲超时时间（1-3600 秒）
```

## 不适用场景

以下场景JS SDK工具专业版不适合处理：

- 需要100%确定性的关键决策
- 医疗诊断
- 法律判决

## 触发条件

需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于非本工具能力范围的需求.
## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 工具构建器 API

### 人工审批工作流

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例
### 服务器代理集成

### 文件附件处理
```typescript
import { readFileSync } from 'fs';
// ...
// 1. 从文件路径发送（Node.js）
const response1 = await agent.sendMessage('分析这张图片', {
    files: [readFileSync('image.png')]
});
// ...
// 2. 从 base64 发送
const response2 = await agent.sendMessage('分析这个文件', {
    files: ['data:image/png;base64,iVBORw0KGgo...']
});
// ...
// 3. 从浏览器 File 对象发送
const input = document.querySelector('input[type="file"]');
const response3 = await agent.sendMessage('描述这张图片', {
    files: [input.files[0]]
});
// ...
// 4. 多文件发送
const response4 = await agent.sendMessage('比较这两张图片', {
    files: [file1, file2]
});
```

### 技能（Skills）配置
```typescript
    core_app: { ref: 'claude-sonnet@latest' },
    skills: [
        {
            name: 'code-review',
            description: '代码审查指南',
            content: `# 代码审查规范
1. 检查安全性
2. 检查性能
3. 检查可读性`
        },
        {
            name: 'api-docs',
            description: 'API 文档',
            url: 'https://example.com/docs/api.md'
        }
    ]
});
// ...
// 智能体会自动参考技能内容进行回答
sendMessage('帮我审查这段代码');
```

### 完整类型定义

## 优选实践
1. **前端用代理模式**：永远不要在前端暴露 API Key

2. **流式响应用 SSE**：提升用户体验
   ```typescript
   agent.sendMessage(msg, { onMessage: (m) => update(m) });
   ```

3. **会话保持用 session**：避免重复初始化

4. **危险操作加审批**：`requireApproval()` 确保安全

5. **工具职责单一**：每个工具只做一件事

6. **system_prompt 要明确**：清晰的角色定义提升输出质量

7. **使用类型定义**：充分利用 TypeScript 类型安全

8. **错误处理要完整**：覆盖网络、API、工具执行错误

## 常见问题
### Q1：如何在 React 中使用？
```typescript
// React Hook 封装
import { useState, useCallback } from 'react';
import { createClient } from '@ai/sdk';
// ...
const client = createClient({ proxyUrl: '/api/proxy' });
// ...
function useAgent() {
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
// ...
    const send = useCallback(async (text: string) => {
        setLoading(true);
        try {
                core_app: { ref: 'claude-sonnet@latest' }
            });
// ...
                onMessage: (msg) => {
                    if (msg.content) {
                        setMessages(prev => [...prev, {
                            role: 'assistant',
                            content: msg.content
                        }]);
                    }
                }
            });
        } finally {
            setLoading(false);
        }
    }, []);
// ...
    return { messages, send, loading };
}
```

### Q2：如何处理工具执行错误？
```typescript
sendMessage('执行任务', {
    onToolCall: async (call) => {
        try {
        } catch (error) {
            // 工具执行失败也返回结果
                error: `工具执行失败: ${error.message}`
            });
        }
    }
});
```

### Q3：如何实现多智能体协作？
```typescript
import { agentTool } from '@ai/sdk';
// ...
// 主智能体可以委托给子智能体
const researcher = agentTool('research', 'research-agent@v1')
    .describe('研究指定主题')
    .param('topic', string('研究主题'))
    .build();
// ...
const writer = agentTool('write', 'writer-agent@v1')
    .describe('根据研究结果撰写文章')
    .param('research_data', string('研究数据'))
    .build();
// ...
const coordinator = client.agent({
    core_app: { ref: 'claude-sonnet@latest' },
    system_prompt: '你是协调者，负责分配任务给研究者和撰写者。',
    tools: [researcher, writer]
});
// ...
const response = await coordinator.sendMessage(
    '研究量子计算并写一篇科普文章'
);
```

### Q4：如何控制会话超时？
```typescript
// 创建会话时指定超时（秒）
const result = await client.run({
    app: 'my-app',
    input: { action: 'init' },
    session: 'new',
    session_timeout: 600  // 10 分钟
});
// ...
// 范围: 1-3600 秒
// 超时后会话自动清理
```

### 已知限制
```typescript
// 简单的速率限制器
class RateLimiter {
    private queue: Array<() => void> = [];
    private running = 0;
    constructor(private maxConcurrent: number = 5) {}
// ...
    async execute<T>(fn: () => Promise<T>): Promise<T> {
        if (this.running >= this.maxConcurrent) {
            await new Promise<void>(resolve => this.queue.push(resolve));
        }
        this.running++;
        try {
            return await fn();
        } finally {
            this.running--;
            if (this.queue.length > 0) {
                this.queue.shift()!();
            }
        }
    }
}
// ...
const limiter = new RateLimiter(5);
// ...
// 使用
const result = await limiter.execute(() =>
    client.run({ app: 'my-app', input: {...} })
);
```

### Q6：支持哪些框架的代理？
| 框架 | 支持 | 配置方式 |
|:-----|:-----|:-----|
| Next.js (App Router) | 完整支持 | `createRouteHandler` |
| Next.js (Pages Router) | 完整支持 | 中间件配置 |
| Express | 完整支持 | `createProxyMiddleware` |
| Hono | 完整支持 | `createHonoProxy` |
| Remix | 完整支持 | Action 函数 |
| SvelteKit | 完整支持 | Endpoint 配置 |

## 依赖说明
### 运行环境
- **Agent 平台**: 支持读取 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **Node.js 版本**: 18.0.0+（或支持 fetch 的现代浏览器）
- **包管理器**: npm / yarn / pnpm

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Node.js | 运行时 | 必需 | nodejs.org 下载 |
| @ai/sdk | npm 包 | 必需 | `npm install @ai/sdk` |
| Next.js | 框架 | 可选 | `npm install next` |
| Express | 框架 | 可选 | `npm install express` |
| Hono | 框架 | 可选 | `npm install hono` |
| TypeScript | 类型系统 | 推荐 | `npm install -D typescript` |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 需要 AI 平台的 API Key，通过环境变量配置
- 前端应用必须使用代理模式，不暴露 Key
- 服务器代理通过环境变量读取 Key
- Webhook 工具需要配置对应平台的密钥

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**: 通过自然语言指令驱动 Agent 提供 SDK 集成建议，专业版功能依赖 Node.js、框架环境和命令行执行能力

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "JS SDK工具专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "javascript sdk pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。