# Node.js 版本兼容矩阵

## 驱动支持

| Node.js 版本 | kb 包版本 | 状态 |
|-------------|----------|------|
| 8.x | kb@1.x | 维护中 |
| 10.x | kb@1.x | 维护中 |
| 12.x | kb@2.x | 推荐 |
| 14.x | kb@2.x | 推荐 |
| 16.x | kb@3.x | 推荐 |
| 18.x | kb@3.x | 推荐 |
| 20.x | kb@3.x | 推荐 |

## 安装

```bash
# 基础安装
npm install kb

# 指定版本
npm install kb@3
```

## 连接示例

```javascript
// Node.js 12+ 推荐写法
const { Client, Pool } = require('kb');

// 单连接
const client = new Client({
  host: 'localhost',
  port: 54321,
  database: 'test',
  user: 'SYSTEM',
  password: '123456'
});

await client.connect();
const result = await client.query('SELECT version()');
console.log(result.rows[0]);
await client.end();

// 连接池
const pool = new Pool({
  host: 'localhost',
  port: 54321,
  database: 'test',
  user: 'SYSTEM',
  password: '123456',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});

const result = await pool.query('SELECT version()');
pool.end();
```

## TypeScript 支持

```typescript
import { Client, Pool } from 'kb';

const client = new Client({
  host: 'localhost',
  port: 54321,
  database: 'test',
  user: 'SYSTEM',
  password: '123456'
});
```

## 注意事项

1. Node.js 8.x 即将停止支持，建议升级至 12+
2. 使用连接池管理高并发场景
3. 异步/回调模式根据 kb 包版本选择
4. SSL/TLS 连接需配置额外参数
