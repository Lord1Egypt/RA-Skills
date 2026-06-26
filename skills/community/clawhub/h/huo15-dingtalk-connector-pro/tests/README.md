# 钉钉 OpenClaw 连接器 — 测试套件

单元测试套件，覆盖钉钉插件的核心模块。所有测试均可离线运行，无需外部服务。

## 📁 目录结构

每个模块对应一个子目录，包含测试文件和测试方案文档：

```
tests/
├── <module>/
│   ├── <module>.test.ts   # 测试用例
│   └── PLAN.md            # 测试方案（目的、用例表、预期输出）
├── index.ts               # 共享 mock 工厂
├── setup.ts               # vitest 全局 setup
└── README.md              # 本文件
```

## 📋 测试模块

| 目录 | 覆盖内容 |
|------|----------|
| `ai-card/` | AI Card 创建、流式更新、投放与回退 |
| `async/` | 异步消息处理 |
| `audio/` | 音频文件处理与转码 |
| `bindings/` | 插件绑定与注册 |
| `card-update/` | 卡片更新操作 |
| `channel/` | 频道管理 |
| `chunk-upload/` | 分片上传 |
| `config/` | 配置 schema 校验 |
| `config-token/` | 配置令牌获取 |
| `core/` | 核心能力聚合（指令归一、消息去重、鉴权、媒体） |
| `deliver-payload/` | 消息投放载荷构建 |
| `directory/` | 通讯录查询、过滤、去重 |
| `docs/` | 文档 CRUD、搜索 |
| `download/` | 文件下载 |
| `file-markers/` | 文件标记处理 |
| `integration/` | 集成测试 |
| `logger/` | 日志工具 |
| `mcp-tools/` | MCP 工具注册与调用 |
| `media/` | 媒体文件处理 |
| `message-extract/` | 消息内容提取 |
| `onboarding/` | 入驻配置 |
| `policy/` | 群组工具策略 |
| `proactive/` | 主动消息发送 |
| `probe/` | 连接探测、缓存、超时 |
| `prompts/` | 提示词构建 |
| `reply-dispatcher/` | 回复分发与命令归一化 |
| `sdk/` | SDK 工具函数 |
| `secret-input/` | 密钥输入 schema |
| `send/` | 消息发送 |
| `send-message/` | 消息发送（高级） |
| `session/` | 会话管理 |
| `socket-manager/` | WebSocket 管理与消息队列 |
| `targets/` | 目标地址解析、格式化、ID 识别 |
| `upload/` | 文件上传 |
| `utils-legacy/` | 历史工具函数 |
| `video/` | 视频文件处理 |

## 🚀 快速开始

```bash
# 安装依赖
npm install

# 运行所有测试
npm test

# 监听模式
npm run test:watch

# 生成覆盖率报告
npm run test:coverage
```

## 📊 测试设计原则

- **纯单元测试**：所有外部依赖（axios、fetch、config 解析）均通过 `vi.mock` 隔离
- **零网络请求**：不依赖钉钉 API、OpenClaw Gateway 或任何外部服务
- **快速执行**：全部测试可在数秒内完成
- **CI/CD 友好**：无需环境变量或特殊配置即可运行

## 📝 编写新测试

1. 在 `tests/` 下创建 `<module>/` 子目录
2. 创建 `<module>.test.ts` 编写测试用例
3. 创建 `PLAN.md` 描述测试方案（目的、用例表、预期输出与潜在错误）
4. 使用 `vi.mock` 隔离外部依赖
5. 如需共享 mock，添加到 `tests/index.ts`
