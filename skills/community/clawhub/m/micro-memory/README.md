# Micro Memory V3.0 - 完整整合版

智能记忆系统，整合 V2.0-V3.0 所有功能特性。

## 版本历史

| 版本 | 功能 |
|------|------|
| V2.0 | 基础 CRUD、批量命令 |
| V2.1 | 压缩、归档、导出功能 |
| V3.0 | 强度系统、关联网络、复习系统、健康报告 |

## 安装

```bash
cd skills/micro-memory
install.bat
```

## 快速开始

```bash
# 查看帮助
memory help

# 添加记忆
memory add '会议在下午 3 点' --tag work --type shortterm

# 列出记忆
memory list

# 搜索记忆
memory search '会议'

# 强化记忆
memory reinforce --id=5 --boost=1.5

# 查看健康报告
memory health

# 添加关联
memory link --from=1 --to=2,3

# 查看关联图
memory graph --id=1
```

## 完整命令

### 基础命令 (V2.0)
| 命令 | 说明 |
|------|------|
| `memory add` | 添加记忆 |
| `memory list` | 列出记忆 |
| `memory search` | 搜索记忆 |
| `memory delete` | 删除记忆 |
| `memory edit` | 编辑记忆 |
| `memory undo` | 撤销操作 |

### 批量操作 (V2.1)
| 命令 | 说明 |
|------|------|
| `memory compress` | 压缩记忆（移除测试数据） |
| `memory archive` | 归档旧记忆 |
| `memory export` | 导出为 JSON/CSV |

### 强度系统 (V3.0)
| 命令 | 说明 |
|------|------|
| `memory reinforce` | 强化记忆（提升强度分数） |
| `memory strength` | 查看强度报告 |

### 关联网络 (V3.0)
| 命令 | 说明 |
|------|------|
| `memory link` | 添加记忆关联 |
| `memory graph` | 查看关联图 |
| `memory analyze` | 分析关联网络 |

### 复习系统 (V3.0)
| 命令 | 说明 |
|------|------|
| `memory review` | 查看复习状态 |
| `memory consolidate` | 整理记忆系统 |

### 其他
| 命令 | 说明 |
|------|------|
| `memory health` | 健康报告 |
| `memory stats` | 统计信息 |
| `memory help` | 帮助信息 |

## 强度系统

记忆强度分为 4 个等级：
- **Strong (强)**: 分数 >= 80，长期稳定
- **Stable (稳定)**: 分数 50-79，正常状态
- **Decaying (衰退)**: 分数 30-49，需要强化
- **Weak (弱)**: 分数 < 30，即将遗忘

使用 `memory reinforce --id=N --boost=1.5` 强化记忆。

## 数据存储

```
store/
├── store.md          # 记忆内容（Markdown 格式）
├── index.json        # 记忆索引（JSON 格式）
├── reviews.json      # 复习状态
├── links.json        # 关联数据
├── .last_operation.json  # 最后操作（用于 undo）
└── archive/          # 归档目录
```

## 数据格式兼容

V3.0 完全兼容 V2.0-V2.1 的旧数据格式：
- 自动检测并升级旧记忆
- 保留原有标签和类型
- 为旧记忆添加强度字段

## 版本

V3.0 Integrated - 2026 年 3 月 20 日
