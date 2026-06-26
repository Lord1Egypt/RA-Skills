# OpenClaw 部署记录规范（详细版）

## 目录结构

```
memory/services/           ← 所有服务记录的根目录
├── registry.md            ← 索引，所有服务的快速概览表
└── {name}.md             ← 单个服务详细记录
```

## registry.md 格式

### 要求
- 顶部写"更新时间"
- 按**类型**和**状态**两个维度分类
- 每行一个服务，格式：`| 名称 | 端口/地址 | 状态 | 用途 |`
- 状态标识：✓ running / ⏸ paused / ✗ stopped / 🔴 removed

### 分类优先级
1. **Docker / 容器**
2. **本地服务**（Python/Node 等直接运行）
3. **远程 / 云服务**（第三方 SaaS、官方服务）
4. **Skill / 扩展**

## {name}.md 格式

### 必须字段
- 基本信息（类型、状态、日期、用途）
- 访问信息（URL、端口、凭证位置）
- 技术细节（依赖、数据存储）
- 部署命令

### 可选字段
- 变更历史
- 备份策略
- 相关文档链接

### 禁止写入
- 凭证明文（token、password、secret key）
- 实际文件内容（配置只写路径）
- 个人隐私信息

## 命名规范

- 文件名：`kebab-case`，如 `wewe-rss.md`、`openclaw-gateway.md`
- 服务名：英文或中文均可，与文件名对应

## 状态值定义

| 状态 | 含义 |
|------|------|
| running | 正常运行中 |
| stopped | 已停止但未卸载 |
| paused | 暂停（可恢复） |
| removed | 已删除/取消部署（保留记录） |

## 凭证脱敏规则

❌ 禁止：
- `token = ghp_xxx`
- `password = "123456"`
- `api_key = "sk-xxx"`

✅ 正确：
- `token` 环境变量，配置在 `.env` 文件
- `AUTH_CODE` 启动参数，见 docker-compose.yml
- 凭证路径：`~/.config/xxx/credentials.json`（字段名不暴露）

## 示例模板

详见 SKILL.md 正文中的 `## 详细记录格式`。
