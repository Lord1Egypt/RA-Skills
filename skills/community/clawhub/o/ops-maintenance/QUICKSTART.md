# ops-maintenance v2.0 快速开始

## 安装

```bash
cd /Users/a1234/.openclaw/workspace/skills/ops-maintenance
npm install
```

## 配置

### 1. 创建配置目录
```bash
mkdir -p ~/.config/ops-maintenance
```

### 2. 创建服务器配置文件
```bash
cat > ~/.config/ops-maintenance/servers.json << 'EOF'
{
  "servers": [
    {
      "name": "web-1",
      "host": "192.168.1.100",
      "user": "root",
      "port": 22,
      "keyFile": "~/.ssh/id_rsa",
      "tags": ["production", "web"]
    },
    {
      "name": "db-1",
      "host": "192.168.1.101",
      "user": "root",
      "port": 22,
      "keyFile": "~/.ssh/id_rsa",
      "tags": ["production", "database"]
    }
  ]
}
EOF
```

## 使用

### 本地检查

```typescript
import { checkHealth } from './src/index.ts'

// 健康检查
const health = await checkHealth()
console.log(health)
```

### 远程检查

```typescript
import { checkRemoteHealth } from './src/index.ts'

// 远程健康检查
const result = await checkRemoteHealth({
  host: '192.168.1.100',
  user: 'root',
  keyFile: '~/.ssh/id_rsa'
})
console.log(result)
```

### 文件传输

```typescript
import { uploadFile, downloadFile } from './src/index.ts'

const config = {
  host: '192.168.1.100',
  user: 'root',
  keyFile: '~/.ssh/id_rsa'
}

// 上传文件
await uploadFile(config, './local.txt', '/tmp/remote.txt')

// 下载文件
await downloadFile(config, '/tmp/remote.txt', './downloaded.txt')
```

### 集群管理

```typescript
import { 
  addServer, 
  checkAllServersHealth,
  executeOnAllServers 
} from './src/index.ts'

// 添加服务器
await addServer({
  host: '192.168.1.100',
  user: 'root',
  name: 'web-1',
  tags: ['production', 'web']
})

// 批量健康检查
const results = await checkAllServersHealth(['production'])

// 批量执行命令
const outputs = await executeOnAllServers('uptime', ['production'])
```

## 测试

```bash
npm test
```

## 构建

```bash
npm run build
```

## 开发

```bash
npm run dev
```

## 常见问题

### 1. SSH连接失败
- 检查SSH密钥是否正确
- 检查服务器是否可达
- 检查防火墙设置

### 2. 权限错误
- 确保SSH密钥文件权限为600
- 确保用户有执行权限

### 3. 超时问题
- 增加连接超时时间
- 检查网络延迟

## 更多信息

查看完整文档:
- `README.md` - 项目说明
- `SKILL.md` - Skill文档
- `OPTIMIZATION_REPORT.md` - 优化报告
- `examples/` - 使用示例
