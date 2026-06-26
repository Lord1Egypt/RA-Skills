# GitHub Collaborative Development System - 依赖清单

## 核心依赖

### 生产依赖 (dependencies)

| 包名 | 版本 | 用途 | 许可证 |
|------|------|------|--------|
| better-sqlite3 | ^11.7.0 | 高性能 SQLite 数据库驱动 | Apache-2.0 |
| commander | ^14.0.0 | CLI 命令解析 | MIT |
| dotenv | ^17.0.0 | 环境变量加载 | BSD-2-Clause |
| uuid | ^11.0.5 | UUID 生成 | MIT |

### 开发依赖 (devDependencies)

| 包名 | 版本 | 用途 | 许可证 |
|------|------|------|--------|
| node | >=16.0.0 | JavaScript 运行时 | Node.js |
| npm | >=8.0.0 | 包管理器 | Artistic-2.0 |

## 依赖关系图

```
github-collab
├── better-sqlite3 (数据库核心)
│   └── sqlite3 (底层绑定)
├── commander (CLI 框架)
├── dotenv (配置管理)
├── uuid (ID 生成)
└── node (运行时环境)
```

## 许可证兼容性

所有依赖均使用兼容 MIT 的开源许可证：
- ✅ Apache-2.0 (better-sqlite3)
- ✅ MIT (commander, uuid)
- ✅ BSD-2-Clause (dotenv)
- ✅ Node.js (node)

## 安全漏洞检查

### 已知问题
- ⚠️ **glob 旧版本**: 如依赖 glob，需升级到最新版本（存在已知安全漏洞）

### 检查命令
```bash
# 检查安全漏洞
npm audit

# 修复已知漏洞
npm audit fix

# 查看详细依赖树
npm ls
```

## 依赖更新记录

### v1.1.0 (2026-03-24)
- ✅ 添加 better-sqlite3 ^11.7.0
- ✅ 添加 commander ^14.0.0
- ✅ 添加 dotenv ^17.0.0
- ✅ 添加 uuid ^11.0.5

### 依赖版本锁定
- 使用 `package-lock.json` 锁定依赖版本
- CI/CD 部署时强制使用锁定版本

## 依赖最小化策略

### 原则
1. **按需引入**: 只引入必要的依赖
2. **版本锁定**: 使用精确版本号，避免自动升级
3. **定期审查**: 每月检查依赖更新和安全漏洞
4. **许可证合规**: 确保所有依赖许可证兼容 MIT

### 检查清单
- [ ] 所有依赖都有明确用途
- [ ] 无重复功能依赖
- [ ] 依赖版本在维护周期内
- [ ] 无已知安全漏洞
- [ ] 许可证兼容项目要求

## 第三方依赖风险

### 高风险依赖
- ❌ 无（当前版本）

### 中风险依赖
- ⚠️ better-sqlite3: 需要 native 编译，部分平台可能有问题

### 低风险依赖
- ✅ commander, dotenv, uuid: 纯 JavaScript，稳定可靠

## 依赖维护计划

### 每月检查
1. 运行 `npm audit` 检查安全漏洞
2. 检查依赖更新通知
3. 评估升级风险

### 每季度更新
1. 更新次要版本（minor updates）
2. 测试兼容性
3. 更新依赖文档

### 每年大版本
1. 评估大版本升级（major updates）
2. 进行完整回归测试
3. 更新技术文档

---

**最后更新**: 2026-03-24  
**维护者**: wljmmx  
**版本**: v1.1.0
