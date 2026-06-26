# Auto Memory 用户使用指南

## 快速开始

### 1. 安装检查依赖

```bash
# 确保 jq 已安装
which jq || brew install jq
```

### 2. 初始化记忆目录

```bash
cd ~/.openclaw/workspace/skills/auto-memory/scripts
chmod +x memory_cli.sh
./memory_cli.sh config show  # 初始化配置
```

### 3. 设定 boss 基本信息

```bash
./memory_cli.sh capture --type boss_info --importance 10 "老板叫XX，是XX公司的XX职位"
```

---

## 日常使用

### 自动记忆（推荐）

在对话中，AI 会自动分析并调用：
```bash
./memory_cli.sh auto_analyze "对话内容"
```

### 手动记忆

```bash
# 自动判断类别
./memory_cli.sh capture "boss 喜欢川菜"

# 指定类别
./memory_cli.sh capture --type boss_preference "boss 喜欢川菜，讨厌粤菜"

# 指定重要度
./memory_cli.sh capture --type boss_decision --importance 9 "团建去贵州"
```

### 搜索记忆

```bash
# 关键词搜索
./memory_cli.sh search "boss 喜欢"

# 查看最近记忆
./memory_cli.sh recent 10

# 记忆统计
./memory_cli.sh stats
```

---

## 用户自定义配置

### 添加自定义记忆类别

```bash
./memory_cli.sh config add_type "投资记录" "boss 的投资持仓和盈亏"
```

### 设置触发规则

```bash
# 格式：关键词:类别:重要度
./memory_cli.sh config set_trigger "川菜:boss_preference:8"
./memory_cli.sh config set_trigger "贵州:boss_decision:9"
```

### 调整记忆层级

```bash
# 把某类记忆放到永久层
./memory_cli.sh config set_tier work_context permanent
```

---

## 记忆冲突处理

当新记忆与旧记忆矛盾时：

1. AI 检测到冲突
2. 自动将旧记忆备份到 `conflict/` 目录
3. 以 boss 最新说的为准更新记忆
4. 输出提示告知 boss

```
[CONFLICT DETECTED]
旧记忆：boss 喜欢川菜
新记忆：boss 现在说想吃粤菜
已自动更新为新记忆，旧记忆已备份
```

---

## 导出与备份

```bash
# 导出所有记忆
./memory_cli.sh export --format markdown

# 导入备份
./memory_cli.sh import --file backup.json
```

---

## 触发规则说明

| 触发词 | 记忆类别 | 默认重要度 |
|--------|---------|-----------|
| "记住..." | auto_detect | 10 |
| "决定/定下来" | boss_decision | 9 |
| "喜欢/不喜欢" | boss_preference | 8 |
| "我叫/我是" | boss_info | 9 |
| "完成了/搞定了" | work_context | 7 |
| "学会了/学到" | learning | 8 |
| 数字/日期/金额 | work_context | 6 |
| 情绪/状态描述 | work_context | 5 |

---

## 三层记忆分层

| 层级 | 存放内容 | 清理规则 |
|------|---------|---------|
| L1 permanent | boss决策/偏好/重要信息 | 永久不删 |
| L2 current | 当前项目/任务/上下文 | 30天后审阅 |
| L3 temporary | 临时上下文/一次性信息 | 7天后自动清理 |

---

## AI 集成使用

在 AGENTS.md 中加入：

```markdown
## 记忆加载
每次新会话开始：
1. 读 MEMORY.md（核心长期记忆）
2. 读 memory/YYYY-MM-DD.md（今日日志）
3. 搜索 auto-memory 索引：./memory_cli.sh recent 10

## 记忆自动触发
每次重要对话后调用：
./memory_cli.sh auto_analyze "对话内容"
```

---

## 注意事项

1. 重要信息用 `--importance 9` 或 `10`
2. 临时信息不要设太高重要度，避免污染永久层
3. 定期运行 `./memory_cli.sh dedup` 清理重复记忆
4. 冲突时以 boss 最新说的为准，自动更新

有问题随时问！
