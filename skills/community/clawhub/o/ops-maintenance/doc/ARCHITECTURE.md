# ops-maintenance 2.0 架构文档

## 🏗️ 架构概览

### 设计原则
- **Clean Architecture**: 领域层独立，依赖方向向内
- **依赖注入**: 所有依赖通过容器管理，易于测试
- **单一职责**: 每个类/模块只做一件事
- **可测试性**: 核心逻辑不依赖外部设施，易于单元测试

### 分层结构

```
src-new/
├── types.ts                    # 统一类型定义（简化版）
├── config/
│   ├── schemas.ts              # 完整类型定义（原版）
│   ├── loader.ts               # ConfigManager - 配置管理
│   ├── validator.ts            # Zod 验证
│   └── ICredentialsProvider.ts # 凭据提供者接口
├── core/
│   ├── entities/               # 领域实体
│   ├── repositories/           # 仓库接口
│   └── usecases/               # 用例层（业务逻辑）
├── infrastructure/
│   ├── ssh/                    # SSH 客户端 & 连接池
│   ├── cache/                  # 缓存实现
│   ├── repositories/           # 仓库实现
│   └── monitoring/             # 监控检查策略
├── presentation/
│   ├── formatters/             # 输出格式化器
│   ├── cli/                    # CLI 命令解析
│   └── LegacyAdapter.ts        # 向后兼容适配器
├── container.ts                # 依赖注入容器
├── legacy.ts                   # 旧版 API 兼容层
├── index.ts                    # 新版应用入口
└── exports.ts                  # 统一导出
```

---

## 🔄 依赖关系

```
    ┌─────────────────┐
    │  presentation   │  CLI / Formatter / LegacyAdapter
    └────────┬────────┘
             │ depends on
    ┌────────▼────────┐
    │    core/usecase │  HealthCheckUseCase, PasswordCheckUseCase
    └────────┬────────┘
             │ depends on
    ┌────────▼────────┐
    │  repositories   │  IServerRepository, ICacheRepository
    └────────┬────────┘
             │ depends on
    ┌────────▼────────┐
    │ infrastructure  │  SSHClient, Cache, ConfigManager
    └─────────────────┘
```

---

## 📦 核心模块说明

### ConfigManager（配置管理）
**职责**: 服务器配置的加载、验证、热重载、CRUD

**特性**:
- 自动加载 `~/.config/ops-maintenance/servers.json`
- 文件监听（macOS/Linux 用 fs.watch，Windows 用轮询）
- 配置变更事件通知
- 运行时增删服务器（`add()`/`remove()`）

**使用**:
```typescript
const cm = new ConfigManager()
await cm.start()
cm.on('change', () => console.log('配置已变更'))
const servers = cm.getAll()
await cm.add({ host: '1.2.3.4', user: 'root', password: 'xxx' })
```

### SSHClient（SSH 客户端）
**职责**: 封装 ssh2 库，提供连接复用、认证、超时控制

**特性**:
- 连接池复用（`connections: Map`）
- keepalive 自动保活
- 命令执行超时控制
- 凭据提供者模式（`ICredentialsProvider`）

**凭据源优先级**:
1. 环境变量 `OPS_CRED_<HOST>` 和 `OPS_KEY_<HOST>`
2. 配置文件（扩展字段，不推荐生产）
3. 默认 SSH 密钥 `~/.ssh/id_rsa` 等

### ConnectionPool（连接池）
**职责**: 管理多服务器连接生命周期

**特性**:
- 最大连接数限制（默认 10）
- 空闲连接自动清理（5 分钟）
- 连接最大存活时间（30 分钟）
- 等待队列机制（并发满时排队）

### Cache（缓存）
**内存缓存**: TTL 自动清理，每分钟扫描过期项  
**文件缓存**: 进程重启后缓存持久化  
**分层缓存**: Memory + File 二级缓存

### HealthChecker（健康检查策略）
**策略模式**: 每个检查项是独立的 `IHealthCheckStrategy`

| 策略 | 优先级 | 关键 | 说明 |
|------|--------|------|------|
| LoadAverageCheck | 1 | ✅ | 1/5/15 分钟负载 |
| MemoryCheck | 2 | ✅ | 内存使用率 |
| DiskCheck | 3 | ✅ | 根分区使用率 |
| ServiceStatusCheck | 4 | ❌ | nginx/docker 等 |

支持自定义策略，通过 `HealthChecker.addStrategy()` 注入。

### ThresholdChecker（阈值检查）
**环境感知**: production/staging/development 不同阈值

ThresholdConfig:
```typescript
{
  diskWarning: 80, diskCritical: 90,
  memoryWarning: 80, memoryCritical: 90,
  swapWarning: 70, swapCritical: 90,
  loadWarningMultiplier: 1.0, loadCriticalMultiplier: 2.0
}
```

### UseCases（用例层）
**单一职责**:
- `HealthCheckUseCase` - 协调检查所有服务器
- `PasswordCheckUseCase` - 密码过期检查
- `DiskCheckUseCase` - 磁盘使用分析

**输入/输出**:
```typescript
interface HealthCheckInput {
  tags?: string[]
  servers?: Server[]
  force?: boolean
  services?: string[]
}
```

### LegacyAdapter（向后兼容）
**目标**: 旧版 `index.ts` 导出的所有函数保持不变

旧版代码无需修改即可使用新架构：
```typescript
// 旧代码
const { loadServers, checkAllServersHealth } = require('./dist/index')
// 底层实际调用 LegacyAdapter
```

---

## 🔐 凭据管理

### 环境变量（推荐）

```bash
# 密码认证（格式：user:password 或仅 password）
export OPS_CRED_10_119_120_143="salt:Giten!#202501Tab*&"
export OPS_CRED_10_111_66_177="salt:another_password"

# 密钥认证（私钥文件路径）
export OPS_KEY_10_119_120_143="/home/user/.ssh/id_rsa"
```

### 配置文件格式

`~/.config/ops-maintenance/servers.json`:
```json
[
  {
    "host": "10.119.120.143",
    "port": 22,
    "user": "salt",
    "name": "DM裸金属服务器",
    "tags": ["DB", "production"]
  }
]
```
密码/密钥**不存储**在配置文件中，通过环境变量注入。

---

## 🎯 使用示例

### 新架构（推荐）

```typescript
import { Container, Server, HealthCheckUseCase } from 'ops-maintenance'

// 初始化容器
const container = await initContainer({
  configPath: '/path/to/servers.json',
  environment: 'production',
  cacheTTL: 30
})

// 创建用例
const healthUseCase = container.createHealthCheckUseCase()

// 执行检查
const report = await healthUseCase.execute({
  tags: ['production'],
  force: false
})

console.log(`健康: ${report.healthy}, 警告: ${report.warning}, 离线: ${report.offline}`)
```

### 旧版 API（向后兼容）

```typescript
// 与旧版完全相同的调用方式
const { loadServers, checkAllServersHealth } = require('ops-maintenance')

const servers = await loadServers()
const results = await checkAllServersHealth(['production'])
```

---

## 🧪 测试策略

### 单元测试（Jest）
- ConfigManager 解析配置
- ThresholdChecker 阈值判断
- SSHClient 连接逻辑（Mock ssh2）

### 集成测试
- 使用 Docker 模拟真实服务器
- 端到端完整流程

### 覆盖率目标
- 核心模块 ≥80%
- 使用 `npm run test:coverage`

---

## 📈 性能优化

| 优化项 | 当前 | 目标 | 收益 |
|--------|------|------|------|
| SSH 连接复用 | ❌ | ✅ | 减少 70% 握手开销 |
| 结果缓存 | ❌ | ✅ 30s TTL | 减少 50% SSH 调用 |
| 并发控制 | Promise.all | 信号量 | 避免压垮服务器 |
| 配置热加载 | ❌ | ✅ | 无需重启更新配置 |

---

## 🚀 迁移指南

### 从 v1.x 迁移到 v2.0

**无需修改代码**，v2.0 完全向后兼容。

如需使用新 API：
```typescript
// v1.x
const { checkAllServersHealth } = require('ops-maintenance')

// v2.0（新 API）
import { Container, HealthCheckUseCase } from 'ops-maintenance'
const container = await initContainer()
const useCase = container.createHealthCheckUseCase()
const report = await useCase.execute({ tags: ['production'] })
```

---

## 📝 待办事项

- [ ] Phase 2: 完成所有 UseCases 实现（日志、性能、端口、进程）
- [ ] Phase 2: 编写单元测试（≥80% 覆盖率）
- [ ] Phase 2: 告警系统（Webhook、邮件）
- [ ] Phase 3: 性能压测（50+ 服务器）
- [ ] Phase 3: 文档完善（API 文档、示例）
- [ ] Phase 3: 发布 v2.0.0

---

**维护者**: Claude Code  
**最后更新**: 2026-04-09