# OpenCode 灵芯派记忆技能包

## 版本
v1.0.0

## 功能
为OpenCode AI助手提供记忆持久化，跨会话保存上下文

## 包含文件
- install.sh - 安装脚本
- README.md - 使用说明
- MEMORY.md - 长期核心记忆模板
- INDEX.md - 索引
- 2026-04-30.md - 今日记忆模板
- memory_index.json - 索引数据
- sync.sh - 同步脚本

## 安装
```bash
./install.sh
```

## 使用
```bash
# 同步
~/.opencode-memory/sync.sh

# 查看
cat ~/.opencode-memory/MEMORY.md
```