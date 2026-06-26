# /careful — 危险操作警告模式

> **作用**: 当 AI 即将执行可能造成不可逆影响的操作时，
> 强制暂停并要求用户明确确认。

## 危险操作清单（自动检测）

### 🟥 极度危险（必须阻止，除非用户强制确认）
| 操作 | 风险 | 示例 |
|------|------|------|
| 删除目录 | 数据永久丢失 | `rm -rf`, `shutil.rmtree`, `delete_file(目录)` |
| 清空数据库 | 所有数据丢失 | `DROP TABLE`, `TRUNCATE`, `DELETE *` |
| 覆盖重要配置 | 服务不可恢复 | 覆盖 `.env`, `nginx.conf`, `systemd service` |
| Force push | 覆盖团队提交历史 | `git push --force` |
| 生产环境变更 | 影响真实用户 | 连接生产DB、修改生产配置 |

### 🟠 高风险（警告 + 二次确认）
| 操作 | 风险 | 示例 |
|------|------|------|
| 批量删除文件 | 可能误删 | 删除 >10 个文件 |
| 数据库 schema 变更 | 可能破坏数据 | ALTER TABLE, ADD/DROP COLUMN |
| 密钥轮换 | 可能导致服务中断 | 更新 API Key, 证书 |
| 重启服务 | 服务中断 | `systemctl restart`, `kill process` |
| 安装全局包 | 污染系统环境 | `pip install -g`, `npm -g` |

### 🟡 中等风险（提醒）
| 操作 | 风险 | 示例 |
|------|------|------|
| 修改核心依赖版本 | 可能引入不兼容 | 改 package.json / requirements.txt |
| 修改数据库迁移文件 | 可能无法回滚 | 改 alembic migration |
| 修改认证相关代码 | 可能导致安全问题 | 改 login/auth/jwt 相关 |

## 交互流程

```
AI 检测到危险操作
       ↓
显示警告卡片:
┌─────────────────────────────────────┐
│  ⚠️  CAREFUL MODE                   │
│                                     │
│  操作: rm -rf /opt/data/cache       │
│  风险等级: 🔴 极度危险               │
│  影响: 永久删除所有缓存数据           │
│                                     │
│  [确认执行] [取消] [查看详情]        │
└─────────────────────────────────────┘
       ↓
用户选择:
  - 确认 → 继续执行（记录日志）
  - 取消 → 中止操作
  - 详情 → 显示更多影响分析
```

## 日志记录

所有经过 careful 确认的操作都应记录：
```json
{
  "timestamp": "2026-04-25T11:30:00",
  "operation": "delete_directory",
  "target": "/opt/data/cache",
  "risk_level": "critical",
  "user_confirmed": true,
  "reason": "清理过期缓存"
}
```
