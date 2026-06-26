# 🧠 焦距记忆系统 (Memory Focal System)

**智能记忆管理，Token 优化 40-60%**

---

## 快速开始

### 1. 安装

技能包已预装在：
```
~/.openclaw/workspace/skills/memory-focal-system/
```

### 2. 初始化

```bash
cd ~/.openclaw/workspace/memory-focal
python3 scripts/cli.py init
```

### 3. 配置

编辑配置文件：
```bash
nano ~/.openclaw/workspace/skills/memory-focal-system/config.json
```

默认配置已优化好，无需修改。

### 4. 测试

```bash
cd ~/.openclaw/workspace/skills/memory-focal-system
python3 memory_manager.py
```

---

## 核心功能

### 消息自动分类
- simple：简单对话，不加载记忆（节省 100% Token）
- task：任务执行，仅加载相关文件（节省 60-75%）
- memory：情感/偏好，加载完整记忆
- new_info：新信息，加载并写入记忆

### 分层记忆加载
- 热存储：最近 7 天，自动加载
- 温存储：7-30 天，按需加载
- 冷存储：30 天+，归档保存

### 自动记忆写入
- 检测新信息
- 自动写入
- 自动生成标签

---

## 配置说明

```json
{
  "enabled": true,              // 是否启用
  "auto_classify": true,        // 自动分类
  "auto_write": true,           // 自动写入
  "load_user": true,            // 加载 USER.md
  "load_memory": true,          // 加载 MEMORY.md
  "load_focal_active": true,    // 加载热存储
  "token_limit": 8000           // Token 上限
}
```

---

## CLI 命令

```bash
cd ~/.openclaw/workspace/memory-focal

# 添加记忆
python3 scripts/cli.py add "少爷偏好早上 8 点起床" --type preference --tags 作息，偏好

# 搜索记忆
python3 scripts/cli.py search "作息"

# 查看统计
python3 scripts/cli.py stats

# 查看高优先级记忆
python3 scripts/cli.py top 5

# 分类测试
python3 scripts/cli.py classify "在吗"

# 生成标签
python3 scripts/cli.py tag "少爷明天考试"

# 预览归档计划
python3 scripts/cli.py cleanup
```

---

## Token 优化效果

| 场景 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| 简单对话 | 8000 tokens | 0 tokens | 100% |
| 任务执行 | 8000 tokens | 2000-3000 tokens | 60-75% |
| 情感/偏好 | 8000 tokens | 8000 tokens | 0% |
| 新信息 | 8000 tokens | 8000 tokens | 0% |

**综合节省：40-60%**

---

## 文件结构

```
memory-focal-system/
├── SKILL.md              # 技能说明
├── README.md             # 本文档
├── _meta.json            # 元数据
├── config.json           # 配置
├── memory_manager.py     # 核心管理模块
└── classifier.py         # 消息分类器
```

---

## 故障排除

### 分类不准确
编辑 `classifier.py`，调整关键词列表

### 记忆写入失败
```bash
chmod +x ~/.openclaw/workspace/memory-focal/scripts/cli.py
```

### Token 超限
降低 `config.json` 中的 `token_limit`

---

## 作者

**Beta (贝塔)** - 少爷翟常喆的专属女秘书

---

## 许可证

MIT License
