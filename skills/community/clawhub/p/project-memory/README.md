# Project Memory - 项目记忆管理技能

跨智能体的项目记忆系统，支持项目隔离和共享访问。

## 功能特点

- **项目管理**: 创建、切换、归档、删除项目
- **记忆读写**: 在指定项目下读取和写入记忆
- **跨智能体共享**: 多个智能体可以访问同一项目的记忆
- **搜索功能**: 按关键词搜索项目记忆

## 适用场景

- 产品经理、程序员、营销等多角色协作
- 需要按项目隔离记忆的团队
- 希望在不同智能体间共享上下文的用户

## 安装

```bash
clawhub install project-memory
```

## 使用方法

### 项目管理
```
/project list           # 列出所有项目
/project create <名称>  # 创建新项目
/project use <名称>     # 切换到项目
/project info           # 显示当前项目
/project archive <名称> # 归档项目
/project delete <名称>  # 删除项目
```

### 记忆管理
```
/memory save <标题>     # 保存记忆
/memory search <关键词> # 搜索记忆
/memory list            # 列出记忆
```

## 数据存储

所有项目数据存储在 `~/.openclaw/projects/` 目录下。

## 许可证

MIT License
