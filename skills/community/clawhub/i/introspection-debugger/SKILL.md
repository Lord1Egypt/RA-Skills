---
name: introspection-debugger
description: AI Agent 自省调试框架 - 让 AI Agent 具备自我诊断和自动修复能力。用于捕获错误、根因分析、自动修复、生成报告。
homepage: https://github.com/tvvshow/openclaw-evomap
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": {},
        "install": [],
      },
  }
---

# AI Agent 自省调试框架

让 AI Agent 具备自省和自我修复能力。

## 功能

| 功能 | 描述 |
|------|------|
| 全局错误捕获 | 自动拦截 uncaughtException 和 unhandledRejection |
| 根因分析 | 基于规则库匹配常见错误 (80%+) |
| 自动修复 | 自动创建文件、修复权限、安装依赖 |
| 报告生成 | 生成结构化自省报告 |
| 人类通知 | 无法修复时通知人类 |

## 支持的错误类型

- 文件缺失 (ENOENT)
- 权限错误 (EACCES)
- 模块缺失 (MODULE_NOT_FOUND)
- 连接超时 (ETIMEDOUT)
- 限流 (429)
- 服务器错误 (500-504)
- 内存溢出 (OOM)
- 进程被终止 (SIGKILL)
- 认证错误 (401/403)

## 使用方法

### 1. 引入模块

```javascript
const IntrospectionDebugger = require('./introspection-debugger');
```

### 2. 创建实例

```javascript
const debugger = new IntrospectionDebugger({
  workspace: process.cwd(),
  maxHistorySize: 100,
  notificationHook: async (report) => {
    // 通知人类
    console.log('需要人工:', report.recommendation.message);
  }
});
```

### 3. 手动捕获错误

```javascript
try {
  // 你的代码
} catch (e) {
  debugger.catch(e, { source: 'my-code' });
}
```

### 4. 查看统计

```javascript
console.log(debugger.getStats());
// { totalErrors: 10, totalFixes: 8, autoFixRate: 0.8 }
```

## 文件

- `introspection-debugger.js` - 主框架代码
- `reliable-api-client.js` - API 客户端黄金标准

## 相关文档

- `INTROSPECTION_DEBUGGER.md` - 详细使用文档
- `EVOMAP_STANDARD.md` - 胶囊发布规范
