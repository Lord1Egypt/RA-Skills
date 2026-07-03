# Knowledge Engineering — 快速入门

> 3 分钟上手，30 分钟精通。不需要读完完整文档。

## 一分钟开始

打开对话框说：

```
把 C:\docs\redis-guide.md 切片
```

Agent 会自动完成分析、拆分、生成、校验四步，你只需等待（10片以内约2分钟）然后验收结果。

---

## 四种常用操作

| 你要做什么 | 怎么说 |
|:---|:---|:---|
| 切片一个文档 | `把 C:\docs\xxx.md 切片` |
| 指定输出位置 | `把 C:\docs\xxx.md 切片，输出到 D:\kb\` |
| 先看计划不生成 | `先看 C:\docs\xxx.md 的切片计划` |
| 大文档中断后继续 | 重新说原指令，Agent 自动跳过已有切片 |

---

## 验收三件事

切片完成后 Agent 会给你：

| 输出 | 在哪 | 干什么用 |
|:---|:---|:---|
| 切片文件 | `输出目录/源文件名/api/` `config/` `guide/` `concepts/` | 直接导入 RAG 知识库 |
| 检索报告 | R@1/R@5/MRR 评分 | 看哪些片检索不到，需要优化 |
| 审计报告 | 死链/缺失/异常检测 | 确认没有遗漏 |

---

## 看懂切片文件

打开任意一个 `.md`，结构固定为五段 + YAML 头：

```
─── YAML 头部（元数据：分类、标签、检索关键词）───
## 概念定义    ← 一句话说清"是什么"
## 使用场景    ← "什么时候用它"
## 核心内容    ← "怎么用"（代码/步骤/配置）
## 注意事项    ← "有什么坑"
## 相关链接    ← "还看什么"
```

---

## 切片效果示例

**输入**（源文件片段）：
```markdown
## HTTP Server

`http.createServer()` 创建一个 HTTP 服务器并监听指定端口。
该方法接受一个回调函数 `(req, res)`，每次请求时触发。

const http = require('http');
const server = http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Hello World');
});
server.listen(3000, () => console.log('Server running on port 3000'));
```

**输出**（一个切片文件）：
```markdown
---
title: "核心模块 > HTTP > 创建 HTTP 服务器"
source_id: "nodejs-reference"
category: "api"
index: 001
tags: ["http", "Node.js", "createServer"]
embedding_hint: "http.createServer 创建 HTTP 服务器，接受回调函数处理请求响应，通过 server.listen 监听 3000 端口"
qa_pairs:
  - q: "Node.js http.createServer 怎么创建 HTTP 服务器？"
    a: "调用 http.createServer(callback) 创建服务器实例，再调用 server.listen(port) 监听端口。回调接收 req 和 res 参数。"
    type: "how-to"
---

## 概念定义
`http.createServer()` 是 Node.js 核心模块 `http` 的方法，用于创建 HTTP 服务器实例。

## 使用场景
需要搭建 Web 服务器、API 端点或处理 HTTP 请求时使用。

## 核心内容
const http = require('http');
const server = http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Hello World');
});
server.listen(3000, () => console.log('Server running on port 3000'));

## 注意事项
> [!WARNING] 回调函数中的 res.end() 必须调用，否则请求会挂起直到超时。

## 相关链接
依赖：`concepts_001-Node.js事件循环.md`
```

---

## 常见问题速查

**Q: 切片分类错了怎么办？**
A: 说 `把 api_005 改成 config 分类`

**Q: 检索评分低怎么办？**
A: 说 `retrieval 死了，重新切片并优化 embedding_hint`

**Q: 文档很大（> 10 万字）？**
A: Agent 自动分批。你也可以先拆成几个小文件分别切片。

**Q: 生成到一半中断了？**
A: 重新说一次原指令，Agent 自动跳过已生成的切片继续。

---

## 下一步

- 想了解全部能力 → 看 [README.md](README.md) 使用说明
- 想知道怎么自定义规则 → 看 [SKILL.md](SKILL.md) §9
- 遇到问题 → 看 [SKILL.md](SKILL.md) §12 反模式与 FAQ
