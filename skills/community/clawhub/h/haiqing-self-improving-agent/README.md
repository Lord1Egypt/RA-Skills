# Self-Improving Agent v2

AI自我改进与记忆系统 - 让AI从错误中学习，越用越聪明。

**灵感来源**: Hermes Agent 的"做-学-改"循环

## 核心功能

- 🔄 **三层学习机制**: 被动捕获 → 主动检查 → 主动生成Skill
- 🧠 **记忆系统**: 错误、纠正、最佳实践全部记录
- 🎯 **主动生成**: 复杂任务成功后主动提议生成可复用Skill
- 🔍 **执行前检查**: 运行命令前自动检查相关记忆

## 安装

```bash
# 克隆到 OpenClaw skills 目录
# 或直接使用 skills-related 目录

# 创建必要目录
mkdir -p ~/.openclaw/memory/self-improving
mkdir -p ~/.openclaw/skills-generated
```

## 使用方法

### 记录错误
```bash
python3 log_error.py --command "npm install xxx" --error "permission denied" --fix "use sudo"
```

### 记录用户纠正
```bash
python3 log_correction.py --topic "代码风格" --wrong "双引号" --correct "单引号"
```

### 主动生成Skill
```bash
python3 generate_skill.py \
  --name "my-tool" \
  --trigger "相关任务描述" \
  --desc "工具功能描述" \
  --files "path/to/file.py"
```

### 执行前检查
```bash
python3 check_memory.py --command "npm install"
```

## 文件结构

```
~/.openclaw/memory/self-improving/
├── errors.jsonl
├── corrections.jsonl
├── best_practices.jsonl
├── skills_registry.json
└── index.json

~/.openclaw/skills-generated/
└── [生成的Skill]
```

## 与Hermes的差距

| 功能 | Hermes | 我们的 |
|------|--------|--------|
| 自动固化 | ✅ 全自动 | ⚠️ 需用户确认 |
| 模式识别 | ✅ 自动泛化 | ⚠️ 需触发条件 |
| 技能质量 | 高 | 中（需人工review） |

**我们的优势**: 用户可控、透明、不冲动做不可逆操作。

## License

MIT-0 - Free to use, modify, and redistribute. No attribution required.
