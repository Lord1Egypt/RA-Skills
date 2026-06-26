---
name: password-manager
description: |
  本地密码管理器，用于存储、查询、修改和删除账号密码。当用户要求记住密码、查询密码、修改密码、删除密码时使用。
  存储文件：~/.openclaw/workspace/passwords.json
  特性：密码加密存储、支持多账号、记录创建/修改时间、支持备注/URL、支持姓名、全字段搜索
  触发词：记住xxx密码、查一下xxx、修改xxx密码、删除xxx密码、我的密码、搜索xxx
---

# Password Manager

本地密码管理器，支持密码加密、多账号存储、时间记录、备注信息、姓名、全字段搜索。

## 存储位置

- `~/.openclaw/workspace/passwords.json` - 加密后的密码数据
- `~/.openclaw/workspace/.password_key` - 加密密钥（600权限）

## 功能特性

- 🔐 **密码加密**：使用 Fernet 对称加密，密钥存储在本地文件
- 👥 **多账号**：支持同一服务存储多个账号
- 📅 **时间记录**：记录密码创建时间和最后修改时间
- 📝 **备注支持**：支持存储 URL 或备注信息
- 👤 **姓名支持**：支持存储中文名（可选）
- 🔍 **全字段搜索**：支持按服务名、账号、姓名、备注搜索
- ✏️ **修改密码**：支持更新已有密码
- 📤 **导入/导出**：支持 CSV 批量导入导出
- 🏷️ **标签分类**：支持给密码加标签，方便筛选
- ⚡ **原子写入**：防止并发覆盖

## 存储字段

| 字段 | 必填 | 说明 |
|------|------|------|
| username | ✅ | 账号/用户名 |
| password | ✅ | 加密后的密码 |
| name | 可选 | 中文姓名 |
| note | 可选 | 备注/URL |
| tags | 可选 | 标签数组，如 ["VPN", "服务器"] |
| created_at | ✅ | 创建时间 |
| updated_at | ✅ | 最后修改时间 |

## 使用方式

### 记住密码

```
python3 scripts/password_manager.py add <服务名> <账号> <密码> [备注] [姓名] [标签]
```

示例：
```bash
# 基本用法
python3 scripts/password_manager.py add GitHub user1@email.com 123456

# 带备注
python3 scripts/password_manager.py add 首都之窗VPN wangteng wangteng@123 https://example.com

# 带备注、姓名和标签
python3 scripts/password_manager.py add 腾讯云 admin pass123 "" "" "云服务,生产环境,重要"
```

### 查询密码

```
# 查询某服务的所有账号
python3 scripts/password_manager.py get <服务名>

# 查询指定账号
python3 scripts/password_manager.py get <服务名> <账号>
```

### 搜索密码（全字段）

支持精确搜索和模糊搜索：

```
# 精确搜索（默认）
python3 scripts/password_manager.py search <关键词>

# 模糊搜索（支持输错字，比如输入 "wy" 能搜到 "wangyi"）
python3 scripts/password_manager.py search <关键词> --fuzzy
```

示例：
```bash
# 搜索包含 "wangyi" 的所有记录
python3 scripts/password_manager.py search wangyi

# 搜索包含 "李" 的姓名
python3 scripts/password_manager.py search 李

# 搜索备注中包含 "dify" 的记录
python3 scripts/password_manager.py search dify
```

### 修改密码

```
python3 scripts/password_manager.py update <服务名> <账号> <新密码>
```

示例：
```bash
python3 scripts/password_manager.py update GitHub user1@email.com newpass123
```

### 删除密码

```
# 删除指定账号
python3 scripts/password_manager.py delete <服务名> <账号>

# 删除整个服务
python3 scripts/password_manager.py delete <服务名>
```

### 列出所有密码

```
# 列出所有
python3 scripts/password_manager.py list

# 按标签筛选
python3 scripts/password_manager.py list --tag VPN

# 查看所有标签
python3 scripts/password_manager.py tags
```

### 导出密码

导出所有密码为 CSV 文件：
```
python3 scripts/password_manager.py export
```
生成文件：`passwords_export_YYYYMMDD_HHMMSS.csv`

### 导入密码

从 CSV 文件导入密码：
```
python3 scripts/password_manager.py import <CSV文件>
```

CSV 格式要求：
```csv
服务,账号,密码,姓名,备注,标签,创建时间,更新时间
GitHub,user1@email.com,123456,,,云服务,,
测试服务,test,testpass,测试用户,备注,VPN;服务器,2024-01-01,2024-01-01
```

> **注意**：导入时会追加到现有数据，不会覆盖
> 标签用逗号分隔，如 `VPN,服务器`

## 命令行示例

```bash
# 添加密码
python3 scripts/password_manager.py add GitHub user1@email.com 123456

# 添加密码（带备注、姓名和标签）
python3 scripts/password_manager.py add 腾讯云 admin pass123 "" "" "云服务,生产环境,重要"

# 查询所有账号
python3 scripts/password_manager.py get <服务名>

# 查询指定账号（可复制密码）
python3 scripts/password_manager.py get <服务名> <账号> --copy

# 搜索（精确匹配）
python3 scripts/password_manager.py search wangyi

# 模糊搜索（支持输错字）
python3 scripts/password_manager.py search wy --fuzzy

# 列出所有密码
python3 scripts/password_manager.py list

# 按标签筛选
python3 scripts/password_manager.py list --tag VPN

# 查看所有标签
python3 scripts/password_manager.py tags

# 批量添加标签（给某服务所有账号加标签）
python3 scripts/password_manager.py add-tag <服务名> <标签>

# 批量添加标签（给搜索结果加标签）
python3 scripts/password_manager.py add-tag --search <关键词> <标签>

# 移除标签
python3 scripts/password_manager.py remove-tag <服务名> <账号> <标签>

# 批量删除（搜索结果）
python3 scripts/password_manager.py delete --search <关键词>

# 批量删除（按标签）
python3 scripts/password_manager.py delete --tag <标签>

# 批量删除（无标签的记录）
python3 scripts/password_manager.py delete --empty-tags

# 修改密码
python3 scripts/password_manager.py update GitHub user1@email.com newpass123

# 删除指定账号
python3 scripts/password_manager.py delete GitHub user1@email.com

# 导出为 CSV
python3 scripts/password_manager.py export

# 从 CSV 导入
python3 scripts/password_manager.py import passwords.csv
```

## 数据格式

passwords.json 格式：
```json
{
  "服务名": [
    {
      "username": "账号",
      "password": "加密后的密码",
      "name": "中文姓名（可选）",
      "note": "备注/URL（可选）",
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-02T12:00:00"
    }
  ]
}
```

## 依赖

```bash
pip install cryptography
```

- `cryptography`：用于密码加密（必需）

## 测试说明

开发新功能时，使用独立的测试数据：
```bash
# 1. 创建测试数据
python3 scripts/password_manager.py add "测试服务" "testuser" "testpass123"

# 2. 测试功能
python3 scripts/password_manager.py get "测试服务"
python3 scripts/password_manager.py update "测试服务" "testuser" "newpass"
python3 scripts/password_manager.py search test

# 3. 测试完成后删除
python3 scripts/password_manager.py delete "测试服务"
```
