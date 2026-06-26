# 模型 / 联网搜索 / Embeddings 核验清单

> 这个文件专门处理高变能力问题，尤其适用于：
> - 这个平台现在有哪些模型？
> - 哪些模型支持联网搜索？
> - 有没有 embeddings？
> - 某能力到底是模型级、接口级还是工具级？

## 适用问题

以下问题优先使用本清单：

- “XX 平台现在支持联网搜索吗？”
- “XX 平台哪些模型支持 embedding？”
- “新模型是不是也支持 search？”
- “这个能力是模型支持，还是接口/工具支持？”

## 推荐核验顺序

### 第一步：先确认这是哪一层能力
先区分用户问的是：

1. **平台级能力**
   - 平台是否提供 embeddings API
   - 平台是否提供 search / tools / MCP / Responses
2. **接口级能力**
   - 某能力挂在哪个 endpoint / guide / tool 体系下
3. **模型级能力**
   - 具体哪些模型支持该能力

不要一上来就把“平台支持”说成“所有模型都支持”。

### 第二步：查这 5 类入口
按优先级核验：

1. 模型列表 / 模型概览
2. API reference
3. Guide / 功能说明页
4. tools / search / MCP / Responses 相关页
5. changelog / release notes / 公告

### 第三步：按能力类型分别查

#### 查“模型”
优先找：
- list models
- models overview
- models intro
- model list

#### 查“联网搜索”
优先找：
- web search
- search
- tool use
- official tools
- MCP
- Responses
- 浏览器 / 网页抓取 / web fetch 类能力说明

#### 查“embeddings”
优先找：
- embeddings
- create embeddings
- vector
- rerank（有时会和 embedding 能力相邻出现）

## 回答模板

### 情况 A：有明确页面证据
可以回答：
- 平台是否提供该能力
- 能力更像模型级、接口级还是工具级
- 如有明确模型名，再补模型名

### 情况 B：只确认到平台/接口级，没确认到具体模型级
要这样说：
- “当前官方文档能确认平台提供该能力，但我还没看到明确写到哪些具体模型支持，建议以模型页或控制台为准。”

### 情况 C：没查到明确证据
要这样说：
- “我查了当前公开文档，暂时没看到明确的 embeddings/search 入口，不能据此断言不支持。”

## 常见错误

- 把“平台支持”说成“所有模型支持”
- 把“工具层联网搜索”说成“模型原生联网”
- 没看到 embedding 文档就直接说“没有 embedding”
- 忽略 changelog / release notes

## 与其他文件的关系

- 平台入口先看：`references/index.md`
- 高变规则先看：`references/live-check-policy.md`
- 平台横向比较看：`references/capability-matrix.md`
