# openclaw-macos-contacts（中文说明）

这是一个面向 OpenClaw 的 macOS 原生通讯录技能（Skill），目标是提供**生产级**的联系人读取、查询、创建、更新、删除、去重与合并能力。

## 能力概览

- 使用 SQLite 快速读取联系人数据
- 使用 Swift + `Contacts.framework` 进行原生创建、更新、删除与查询
- 支持重复检测、重复组规划与 merge 去重
- 支持备份、恢复、事务包装与失败回滚

## 设计原则

### 1. 读写分离

- **读路径**：SQLite（快、灵活、适合搜索）
- **写路径**：Swift + `Contacts.framework`（系统原生、稳定、适合生产）
- **兼容路径**：AppleScript / Contacts.app（作为 fallback）

### 2. 不直接写通讯录数据库

不要直接修改 macOS 通讯录 SQLite 主库。所有写操作都应通过系统原生 API 完成。

### 3. 修改前先备份

对于更新、删除、merge 这类写操作，建议统一通过事务包装脚本执行，这样可以先自动备份，失败时自动回滚。

## 关键脚本

- `scripts/contacts_sqlite.py`
  - 读取/搜索/列出联系人
- `scripts/contacts_swift.swift`
  - 原生查询、创建、更新、删除、重复检测
- `scripts/contacts_merge.swift`
  - 重复联系人合并计划与执行
- `scripts/contacts_backup.sh`
  - 备份通讯录数据库
- `scripts/contacts_restore.sh`
  - 恢复备份
- `scripts/contacts_txn.sh`
  - 事务包装：写操作前备份，失败自动回滚
- `scripts/contacts_dedupe.sh`
  - 基于 identifier 的重复清理辅助脚本

## 常见用法

### 搜索联系人

```bash
python3 scripts/contacts_sqlite.py search "张三"
swift scripts/contacts_swift.swift find --query "张三"
```

### 创建联系人

```bash
bash scripts/contacts_txn.sh swift scripts/contacts_swift.swift create \
  --first-name 张 \
  --last-name 三 \
  --phone 15555550123 \
  --email zhangsan@example.com
```

### 更新联系人

```bash
bash scripts/contacts_txn.sh swift scripts/contacts_swift.swift update \
  --identifier "CONTACT_ID" \
  --organization "示例公司" \
  --job-title "产品经理"
```

### 删除联系人

```bash
bash scripts/contacts_txn.sh swift scripts/contacts_swift.swift delete \
  --identifier "CONTACT_ID"
```

### 查看重复联系人并合并

```bash
swift scripts/contacts_merge.swift plan-duplicates
bash scripts/contacts_txn.sh swift scripts/contacts_merge.swift apply-plan \
  --keep KEEP_ID \
  --drop DROP_ID_1 \
  --drop DROP_ID_2
```

## 安全建议

- 不要直接写 SQLite 主库
- 对更新、删除、merge 一律使用事务包装
- 删除与 merge 尽量使用 identifier 精确定位
- 运行时备份状态应保存在 skill 目录之外

## 当前定位

这个 skill 已具备私有/内部生产使用的能力，后续仍可继续增强：

- 批量导入
- 冲突报告
- 更高级字段合并策略
- 更完善的审计日志
