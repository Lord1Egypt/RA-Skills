# 分层记忆系统集成指南

## 概述

本指南说明如何在日常工作中使用分层记忆系统，以及如何集成到现有工作流。

## 快速开始

### 1. 查看当前状态

```bash
cd ~/clawd/skills/layered-memory
node index.js stats
```

### 2. 搜索记忆（推荐使用 L1）

```bash
# 搜索关键词
node index.js search "API" l1

# 搜索项目相关
node index.js search "桌面小组件" l1

# 搜索日期相关
node index.js search "2026-02-19" l1
```

### 3. 读取特定记忆

```bash
# 读取主记忆的概览
node index.js read ~/clawd/MEMORY.md l1

# 读取今天的工作日志
node index.js read ~/clawd/memory/daily/2026-02-20.md l1
```

## 工作流集成

### 场景 1: 创建新的工作日志

```bash
# 1. 创建新文件
DATE=$(date +%Y-%m-%d)
touch ~/clawd/memory/daily/$DATE.md

# 2. 编辑内容
vim ~/clawd/memory/daily/$DATE.md

# 3. 自动生成分层
~/clawd/scripts/memory-hook.sh ~/clawd/memory/daily/$DATE.md
```

### 场景 2: 更新现有记忆

```bash
# 1. 编辑文件
vim ~/clawd/MEMORY.md

# 2. 重新生成分层
node ~/clawd/scripts/generate-layers-simple.js ~/clawd/MEMORY.md
```

### 场景 3: 批量维护

```bash
# 检查并生成所有缺失的分层文件
cd ~/clawd/skills/layered-memory
node index.js maintain
```

## 在对话中使用

### 方式 1: 直接调用 skill

```
我: 搜索关于 API Toolkit 的记忆

你: [调用 layered-memory skill]
node index.js search "API Toolkit" l1
```

### 方式 2: 使用脚本

```
我: 读取今天的工作日志概览

你: [使用 memory-reader]
node ~/clawd/scripts/memory-reader.js read ~/clawd/memory/daily/2026-02-20.md l1
```

### 方式 3: 手动读取

```
我: 给我看看 MEMORY.md 的概览

你: [读取 L1 文件]
cat ~/clawd/.MEMORY.overview.md
```

## Token 优化策略

### 默认策略（推荐）

1. **首次查询**: 使用 L1
   - 了解内容概况
   - 判断是否相关
   - 节省 88% tokens

2. **确认相关**: 使用 L2
   - 获取详细信息
   - 精确引用
   - 仅在必要时使用

3. **批量筛选**: 使用 L0
   - 快速过滤大量文件
   - 节省 99% tokens
   - 适合初步筛选

### 实际案例

**案例 1: 查找某个项目的信息**

```bash
# Step 1: 用 L0 快速筛选相关文件
for file in ~/clawd/memory/daily/*.md; do
  l0=$(cat "${file%.*}.abstract.md" 2>/dev/null)
  if echo "$l0" | grep -q "桌面小组件"; then
    echo "找到: $file"
  fi
done

# Step 2: 用 L1 了解详情
node index.js read <找到的文件> l1

# Step 3: 如需详细信息，读 L2
node index.js read <找到的文件> l2
```

**案例 2: 回顾最近工作**

```bash
# 用 L1 快速浏览最近 7 天的工作
for i in {0..6}; do
  date=$(date -v-${i}d +%Y-%m-%d)
  file=~/clawd/memory/daily/$date.md
  if [ -f "$file" ]; then
    echo "=== $date ==="
    node index.js read "$file" l1
    echo ""
  fi
done
```

## 自动化建议

### 1. 添加到 Git 钩子

```bash
# .git/hooks/post-commit
#!/bin/bash
# 提交后自动生成分层

changed_files=$(git diff-tree --no-commit-id --name-only -r HEAD | grep '\.md$')

for file in $changed_files; do
  if [[ $file == memory/* ]] || [[ $file == MEMORY.md ]]; then
    ~/clawd/scripts/memory-hook.sh "$file"
  fi
done
```

### 2. 添加到定时任务

```bash
# 每天凌晨 1 点自动维护
crontab -e

# 添加:
0 1 * * * cd ~/clawd/skills/layered-memory && node index.js maintain
```

### 3. 添加到 shell 别名

```bash
# ~/.zshrc 或 ~/.bashrc
alias mem-search='node ~/clawd/skills/layered-memory/index.js search'
alias mem-read='node ~/clawd/skills/layered-memory/index.js read'
alias mem-stats='node ~/clawd/skills/layered-memory/index.js stats'
alias mem-maintain='node ~/clawd/skills/layered-memory/index.js maintain'

# 使用:
mem-search "API" l1
mem-read ~/clawd/MEMORY.md l1
mem-stats
```

## 性能监控

### 查看 Token 节省效果

```bash
# 查看统计
node index.js stats

# 输出示例:
# 总文件数: 10
# L0 覆盖: 10/10
# L1 覆盖: 10/10
# Token 统计:
#   L0: 39 词 (节省 99%)
#   L1: 760 词 (节省 88%)
#   L2: 6384 词
```

### 计算实际节省

```bash
# 假设每天 10 次记忆查询
# 每次使用 L1 代替 L2 节省 ~1400 tokens
# 每天节省: 10 * 1400 = 14,000 tokens
# 每月节省: 14,000 * 30 = 420,000 tokens
```

## 故障排除

### 问题 1: 分层文件不存在

```bash
# 解决方案: 运行维护
node index.js maintain
```

### 问题 2: 搜索结果不准确

```bash
# 尝试不同层级
node index.js search "关键词" l0  # 更宽泛
node index.js search "关键词" l1  # 平衡
node index.js search "关键词" l2  # 更精确
```

### 问题 3: 分层内容过时

```bash
# 重新生成所有分层
node index.js generate --all
```

## 最佳实践

1. **默认使用 L1** - 88% 节省率，信息足够
2. **批量筛选用 L0** - 99% 节省率，快速过滤
3. **确认需要才用 L2** - 完整信息，按需加载
4. **定期维护** - 每周运行一次 `maintain`
5. **新文件即生成** - 使用 `memory-hook.sh`

## 进阶技巧

### 1. 组合搜索

```bash
# 先用 L0 快速筛选，再用 L1 详细查看
results=$(node index.js search "API" l0)
# 从结果中选择相关文件
node index.js read <选中的文件> l1
```

### 2. 时间范围查询

```bash
# 查询最近 7 天的工作
find ~/clawd/memory/daily -name "2026-02-*.md" -mtime -7 | while read file; do
  node index.js read "$file" l1
done
```

### 3. 关键词高亮

```bash
# 搜索并高亮关键词
node index.js search "API" l1 | grep --color=auto "API"
```

## 总结

分层记忆系统通过 L0/L1/L2 三层结构，在保持信息完整性的同时大幅减少 Token 消耗。

**核心优势:**
- 节省 88-99% tokens
- 保持信息完整性
- 灵活的层级选择
- 自动化维护

**推荐使用:**
- 日常查询用 L1
- 批量筛选用 L0
- 深度阅读用 L2

开始使用分层记忆，享受 Token 节省的好处！🎉
