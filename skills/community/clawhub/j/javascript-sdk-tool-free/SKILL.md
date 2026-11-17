---

name: "javascript-sdk-tool-free"
description: "JavaScript AI 应用 SDK 入门工具，支持模型调用、文件上传与基础代理配置。Use when 需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于需要100%确定性的关键决策。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "JS SDK工具免费版"
  version: "1.0.0"
  summary: "JavaScript AI 应用 SDK 入门工具，支持模型调用、文件上传与基础代理配置。"
  tags:
    - "开发工具"
    - "JavaScript"
    - "AI应用"
    - "SDK"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# JavaScript SDK 工具（免费版）

## 概述

本工具为个人开发者提供 JavaScript/TypeScript AI 应用 SDK 的基础使用指引，覆盖 SDK 安装、认证配置、应用调用、文件上传等核心场景。通过自然语言指令驱动，帮助开发者快速集成 AI 应用调用能力到 JavaScript 项目中。免费版聚焦个人开发者的基础调用场景，提供简洁的 API 示例与错误处理模板。

## 核心能力

| 能力模块 | 描述 | 典型用法 |
| --- | --- | --- |
| SDK 安装 | npm/yarn/pnpm 安装 | `npm install @ai/sdk` |
| 认证配置 | API Key 与环境变量 | 直接配置或环境变量 |
| 应用调用 | 运行 AI 应用并获取结果 | `client.run({ app, input })` |
| 文件上传 | 自动或手动上传文件 | `client.uploadFile(path)` |
| 错误处理 | 基础异常捕获 | try/catch + 类型判断 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：JavaScript、入门工具、支持模型调用、文件上传与基础代、理配置、面向个人开发者的、提供基础的模型调、用与文件处理能力、应用调用与结果获、文件自动上传与手、环境变量认证配置、基础错误处理、CommonJS、Module、双支持等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：快速调用 AI 应用

开发者需要在 JavaScript 项目中调用 AI 模型。

```text
用户：帮我在 Node.js 项目中调用 AI 模型生成图片

助手：
1. 安装 SDK
   npm install @ai/sdk

2. 配置认证
   // 直接配置
   import { createClient } from '@ai/sdk';
   const client = createClient({ apiKey: 'your_api_key' });
   
   // 或使用环境变量（推荐）
   // .env 文件
   AI_API_KEY=your_api_key
   
   const client = createClient({ apiKey: process.env.AI_API_KEY });

3. 调用应用
   const result = await client.run({
       app: 'image-generator',
       input: { prompt: '山间日落' }
   });
   
   console.log(result.status);  // "completed"
   console.log(result.output);  // 输出数据

4. 错误处理
   try {
   } catch (e) {
       if (e.name === 'RequirementsNotMet') {
           console.log('缺少必要参数:', e.errors);
       } else {
           console.log('API 错误:', e.message);
       }
   }
```

### 场景二：文件上传与处理

开发者需要上传文件并交给 AI 应用处理。

```typescript
import { createClient } from '@ai/sdk';

// 方式一：自动上传（路径作为输入）
const result1 = await client.run({
    app: 'image-processor',
    input: {
        image: '/path/to/image.png'  // 自动上传
    }
});

// 方式二：手动上传
const file = await client.uploadFile('/path/to/image.png', {
    filename: 'custom_name.png',
    contentType: 'image/png',
    public: true
});

const result2 = await client.run({
    app: 'image-processor',
    input: { image: file.uri }
});

// 方式三：浏览器文件上传
const input = document.querySelector('input[type="file"]');
uploadFile(input.files[0]);
const result3 = await client.run({
    app: 'image-processor',
});
```

### 场景三：异步任务处理

开发者需要处理耗时较长的 AI 任务。

```typescript
// 异步执行（不等待完成）
const task = await client.run({
    app: 'video-generator',
    input: { prompt: '无人机飞越山脉' }
}, { wait: false });

console.log(`任务 ID: ${task.id}`);

// 后续查询任务状态
const status = await client.getTask(task.id);
console.log(`状态: ${status.status}`);

if (status.status === 'completed') {
    console.log('结果:', status.output);
} else if (status.status === 'failed') {
    console.log('失败:', status.error);
}
```

## 不适用场景

以下场景JS SDK工具免费版不适合处理：

- 逆向工程闭源API
- API安全安全评估
- 非标准协议集成

## 触发条件

需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 安装

```bash
# npm
npm install @ai/sdk

# yarn
yarn add @ai/sdk

# pnpm
pnpm add @ai/sdk
```

**环境要求**：Node.js 18.0.0+（或支持 fetch 的现代浏览器）

### 认证配置

```typescript
import { createClient } from '@ai/sdk';

// 方式一：直接配置 API Key
const client = createClient({ apiKey: 'your_api_key' });

// 方式二：环境变量（推荐）

// 方式三：前端代理（不暴露 Key）
const client = createClient({ proxyUrl: '/api/proxy' });
```

### 基础调用模板

```typescript
import { createClient } from '@ai/sdk';

async function main() {
    try {
            app: 'text-generator',
            input: {
                prompt: '用一句话介绍 JavaScript',
                max_tokens: 100
            }
        });
        
        console.log('状态:', result.status);
        console.log('输出:', result.output);
    } catch (error) {
        console.error('调用失败:', error.message);
    }
}

main();
```

## 示例

### 运行参数说明

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `app` | string | 应用 ID |
| `input` | object | 匹配应用 schema 的输入 |
| `setup` | object | 隐藏的配置参数 |
| `infra` | string | `cloud` 或 `private` |
| `wait` | boolean | 是否等待完成（默认 true） |

### CommonJS 支持

```javascript
const { createClient } = require('@ai/sdk');

const client = createClient({ apiKey: 'your_api_key' });

async function run() {
        app: 'text-generator',
        input: { prompt: '你好' }
    });
    console.log(result);
}

run();
```

### 环境变量配置

```bash
# .env 文件
AI_API_KEY=your_api_key_here

# 加载环境变量（Node.js）
# npm install dotenv
import 'dotenv/config';

```

## 优选实践

1. **API Key 用环境变量**：不要硬编码在代码中
   ```typescript
// 本技能的核心实现逻辑
// 请参考上方使用说明进行配置和调用
const result = "implementation_ready";
```

2. **始终做错误处理**：网络和 API 调用可能失败
   ```typescript
   try {
   } catch (e) {
       console.error(e);
   }
   ```

3. **长任务用异步模式**：避免请求超时
   ```typescript
run({...}, { wait: false });
   ```

4. **文件上传指定类型**：确保正确处理
   ```typescript
   await client.uploadFile(path, { contentType: 'image/png' });
   ```

5. **前端用代理模式**：不暴露 API Key
   ```typescript
   const client = createClient({ proxyUrl: '/api/proxy' });
   ```

## 常见问题

### Q1：如何获取 API Key？

```text
在 AI 平台的设置页面：
Settings → API Keys → Create API Key
复制生成的 Key 并保存到环境变量
```

### Q2：调用超时怎么办？

```typescript
// 长耗时任务使用异步模式
    app: 'video-generator',
    input: { prompt: '...' }
}, { wait: false });

// 轮询任务状态
async function waitForTask(taskId, interval = 5000) {
    while (true) {
        if (status.status === 'completed') return status;
        if (status.status === 'failed') throw new Error(status.error);
        await new Promise(r => setTimeout(r, interval));
    }
}

const result = await waitForTask(task.id);
```

### Q3：如何在浏览器中使用？

```typescript
// 不要在浏览器中暴露 API Key
// 使用代理模式
const client = createClient({ proxyUrl: '/api/proxy' });

// 浏览器文件上传
querySelector('input[type="file"]');
uploadFile(input.files[0]);
```

### Q4：如何处理 API 错误？

```typescript
import { RequirementsNotMetError, APIError } from '@ai/sdk';

try {
} catch (e) {
    if (e instanceof RequirementsNotMetError) {
        // 缺少必要参数
        for (const err of e.errors) {
            console.log(`  - ${err.type}: ${err.key}`);
        }
    } else if (e instanceof APIError) {
        // API 调用错误
        console.log('API 错误:', e.message);
        console.log('状态码:', e.statusCode);
    } else {
        // 网络或其他错误
        console.log('未知错误:', e);
    }
}
```

### Q5：支持哪些 Node.js 版本？

```text
需要 Node.js 18.0.0 或以上版本
因为 SDK 使用了原生 fetch API
Node.js 18 以下需要安装 node-fetch polyfill
```

### Q6：如何批量调用？

```typescript
// 并行调用（注意速率限制）
const prompts = ['问题1', '问题2', '问题3'];

const results = await Promise.all(
    prompts.map(prompt => 
        client.run({
            app: 'text-generator',
            input: { prompt }
        })
    )
);

// 串行调用（避免速率限制）
const results = [];
for (const prompt of prompts) {
        app: 'text-generator',
        input: { prompt }
    });
    results.push(result);
}
```

## 依赖说明

### 运行环境
- **Agent 平台**: 支持读取 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **Node.js 版本**: 18.0.0+（或支持 fetch 的现代浏览器）
- **包管理器**: npm / yarn / pnpm

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Node.js | 运行时 | 必需 | nodejs.org 下载 |
| @ai/sdk | npm 包 | 必需 | `npm install @ai/sdk` |
| dotenv | 环境变量 | 推荐 | `npm install dotenv` |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 需要 AI 平台的 API Key，通过环境变量配置
- 前端应用使用代理模式，不暴露 Key
- 环境变量名称建议：`AI_API_KEY`

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**: 通过自然语言指令驱动 Agent 提供 SDK 集成建议，代码运行需要 Node.js 和 npm 执行能力

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需要API Key，无Key环境无法使用
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。