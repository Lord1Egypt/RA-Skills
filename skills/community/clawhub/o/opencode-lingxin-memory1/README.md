# OpenCode 灵芯派记忆技能包

## 功能
为OpenCode AI对话助手提供记忆持久化存储，在灵芯派上保存对话上下文，实现跨会话记忆。

## 特性
- 自动保存对话上下文到本地
- 同步到Gitee实现备份
- 空间占用小（轻量化设计）
- 适用于灵芯派等低内存设备

## 安装

```bash
# 进入技能包目录
cd /home/zmrobo/Project/opencode-memory-skill

# 运行安装脚本
./install.sh
```

## 使用

### 新对话开始时
```bash
# 读取记忆恢复上下文
cat ~/.opencode-memory/README.md
cat ~/.opencode-memory/MEMORY.md
cat ~/.opencode-memory/2026-04-30.md
```

### 对话结束时
```bash
# 同步记忆到Gitee
~/.opencode-memory/sync.sh
```

## 手动命令

```bash
# 查看记忆状态
cd ~/.opencode-memory && git status

# 搜索记忆
grep -r "关键词" ~/.opencode-memory/

# 查看记忆大小
du -sh ~/.opencode-memory/
```

## 配置文件

记忆库位置: `~/.opencode-memory/`

```
~/.opencode-memory/
├── README.md              # 使用说明
├── MEMORY.md             # 长期核心记忆
├── 2026-04-30.md        # 每日记忆
├── INDEX.md              # 索引
├── memory_index.json     # 索引数据
├── project_timeline.json # 时间线
├── sync.sh               # 同步脚本
└── *.md                  # 其他文档
```

## 依赖
- git
- Gitee远程仓库（首次安装时配置）

## 适用系统
- 灵芯派 (SmartPi)
- Debian/Ubuntu ARM设备
- 低内存设备（仅需2GB可用空间）

## License
MIT