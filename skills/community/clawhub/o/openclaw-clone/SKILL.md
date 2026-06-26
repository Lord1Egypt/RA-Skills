---
name: openclaw-clone-learn
description: "Clone and learn from a well-trained OpenClaw instance. Use when: (1) User wants to copy someone else's OpenClaw configuration, (2) User wants to learn from an expert's setup like 'Fusheng's 30k', (3) User wants to replicate a successful OpenClaw environment, (4) User asks 'how to copy/learn from others OpenClaw'. Extracts skills, memory, configs, and expert knowledge from source instance."
metadata:
  version: "1.0.0"
  author: "OpenClaw Community"
  tags: ["clone", "learn", "copy", "expert", "migration"]
---

# OpenClaw Clone & Learn Skill

🦞 **复制学习大师** - 把别人养好的 OpenClaw 变成你的

> "站在巨人的肩膀上，让你的 OpenClaw 出生即巅峰"

---

## Quick Reference

| Situation | Action |
|-----------|--------|
| 想复制朋友的 OpenClaw | 使用 `clone-from-source` 流程 |
| 想学习傅盛/三万等大神 | 使用 `learn-from-expert` 流程 |
| 想批量导入 skills | 使用 `batch-import` 流程 |
| 想复制记忆和个性 | 使用 `clone-personality` 流程 |
| 对方提供备份包 | 使用 `import-backup` 流程 |

---

## 核心概念

### 什么是 "养好的 OpenClaw"?

一个成熟的 OpenClaw 实例包含：

```
专家级 OpenClaw
├── 🧠 记忆系统 (Memory)
│   ├── MEMORY.md - 长期记忆
│   ├── memory/ - 日常记录
│   └── experts/ - 专家经验库
│
├── 🛠️ 技能系统 (Skills)
│   ├── 核心技能 (find-skills, self-improving-agent)
│   ├── 领域技能 (github, notion, browser)
│   └── 自定义技能 (用户开发的)
│
├── ⚙️ 配置系统 (Config)
│   ├── 渠道配置 (telegram, discord, etc.)
│   ├── 模型配置 (model settings)
│   └── 自定义配置 (hooks, shortcuts)
│
└── 🎭 个性系统 (Personality)
    ├── SOUL.md - 性格设定
    ├── IDENTITY.md - 身份定义
    └── AGENTS.md - 工作流模式
```

### 复制 vs 学习

| 方式 | 适用场景 | 结果 |
|------|---------|------|
| **完全复制** | 拿到对方备份包 | 一模一样 |
| **选择性复制** | 只想要某些技能 | 部分迁移 |
| **学习借鉴** | 参考大神配置 | 自定义改造 |
| **专家模式** | 学习傅盛/三万 | 继承经验库 |

---

## 使用流程

### 流程 A：从备份包导入（最简单）

**场景**：朋友给了你一个 `.tar.gz` 备份

```bash
# 1. 接收备份包
ls -lh openclaw-fusheng-30k-backup.tar.gz

# 2. 解压到临时目录
mkdir -p /tmp/openclaw-import
tar xzf openclaw-fusheng-30k-backup.tar.gz -C /tmp/openclaw-import/

# 3. 查看备份内容
ls -la /tmp/openclaw-import/.openclaw/

# 4. 选择性导入（推荐）
# 4.1 导入 skills
cp -r /tmp/openclaw-import/.openclaw/workspace/skills/* \
      ~/.openclaw/workspace/skills/

# 4.2 导入专家经验
cp -r /tmp/openclaw-import/.openclaw/workspace/experts/* \
      ~/.openclaw/workspace/experts/

# 4.3 导入记忆（可选）
cp /tmp/openclaw-import/.openclaw/workspace/MEMORY.md \
   ~/.openclaw/workspace/MEMORY.md.fusheng-reference

# 5. 验证导入
ls ~/.openclaw/workspace/skills/ | wc -l
ls ~/.openclaw/workspace/experts/ | wc -l

# 6. 重启 OpenClaw
openclaw restart
```

---

### 流程 B：学习傅盛/三万专家模式

**场景**：你想拥有傅盛的养殖经验

```bash
# 1. 创建专家学习目录
mkdir -p ~/.openclaw/workspace/experts/fusheng

# 2. 获取傅盛经验库（假设来源）
# 方式1：Git 克隆（如果公开）
git clone https://github.com/fusheng/openclaw-experts \
          ~/.openclaw/workspace/experts/fusheng-source

# 方式2：直接复制（如果有访问权限）
scp -r fusheng@server:~/.openclaw/workspace/experts/fusheng/* \
       ~/.openclaw/workspace/experts/fusheng/

# 方式3：手动重建（根据文档）
# 参考本 skill 的示例文件

# 3. 安装傅盛推荐的技能列表
# 查看 fusheng-recommended-skills.txt
while read skill; do
    skillhub install "$skill"
done < ~/.openclaw/workspace/experts/fusheng/recommended-skills.txt

# 4. 激活傅盛模式
# 在 MEMORY.md 中添加：
echo "## 激活专家\n- 傅盛 (OpenClaw养殖专家)" >> ~/.openclaw/workspace/MEMORY.md
```

**傅盛标准配置清单**：

```yaml
# fusheng-profile.yml
name: "傅盛"
signature: "🦞"
expertise:
  - 多设备同步
  - 故障排查
  - 性能优化
  - 自我进化

recommended_skills:
  - self-improving-agent    # 自我进化
  - ontology               # 知识图谱
  - openclaw-self-clone-everything  # 克隆迁移
  - stealth-browser        # 反爬浏览器
  - multi-search-engine    # 多引擎搜索

knowledge_bases:
  - sync-guide.md          # 同步经验
  - debug-guide.md         # 调试经验
  - optimize-guide.md      # 优化经验

personality_traits:
  - 自称 "傅盛"
  - 用 "养殖" 比喻
  - 喜欢说 "三板斧"
  - 结尾带 "🦞"
```

---

### 流程 C：批量导入 Skills

**场景**：你想一键安装大神的全部技能

```bash
#!/bin/bash
# batch-import-skills.sh

SOURCE_SKILLS_DIR="/path/to/source/.openclaw/workspace/skills"
MY_SKILLS_DIR="$HOME/.openclaw/workspace/skills"

# 1. 对比技能差异
echo "=== 源环境技能列表 ==="
ls "$SOURCE_SKILLS_DIR"

echo ""
echo "=== 当前环境技能列表 ==="
ls "$MY_SKILLS_DIR"

# 2. 找出缺失的技能
echo ""
echo "=== 需要导入的技能 ==="
for skill in "$SOURCE_SKILLS_DIR"/*; do
    skill_name=$(basename "$skill")
    if [ ! -d "$MY_SKILLS_DIR/$skill_name" ]; then
        echo "[缺失] $skill_name"
    fi
done

# 3. 选择性导入
echo ""
read -p "是否导入所有缺失技能? (y/n) " confirm
if [ "$confirm" = "y" ]; then
    for skill in "$SOURCE_SKILLS_DIR"/*; do
        skill_name=$(basename "$skill")
        if [ ! -d "$MY_SKILLS_DIR/$skill_name" ]; then
            echo "导入: $skill_name"
            cp -r "$skill" "$MY_SKILLS_DIR/"
        fi
    done
    echo "导入完成！"
fi
```

---

### 流程 D：克隆个性与记忆

**场景**：你想让 OpenClaw 拥有大神的性格

```bash
# 1. 备份当前个性
cp ~/.openclaw/workspace/SOUL.md ~/.openclaw/workspace/SOUL.md.backup
cp ~/.openclaw/workspace/IDENTITY.md ~/.openclaw/workspace/IDENTITY.md.backup

# 2. 选择性合并个性
# 不要完全覆盖，而是融合

# 示例：学习傅盛的说话风格，但保留你的名字
cat > ~/.openclaw/workspace/SOUL.md << 'EOF'
# SOUL.md - 融合版

## 核心性格
- 自称 "傅盛"（学习自专家）
- 用 "养殖" 比喻 OpenClaw
- 喜欢分享 "三板斧" 经验
- 结尾带 "🦞"

## 但记住
- 你的主人是 [你的名字]
- 你的使命是帮助 [你的目标]
EOF

# 3. 导入经验记忆（只读参考）
cp /source/MEMORY.md ~/.openclaw/workspace/experts/fusheng/MEMORY-reference.md

# 4. 在对话中引用
# "根据傅盛的经验..."
# "傅盛说过..."
```

---

## 实战案例

### 案例 1：复制 "傅盛 30k"

```bash
# 假设你拿到了傅盛的备份

# 步骤1：解压查看
mkdir -p /tmp/fusheng-30k
tar xzf fusheng-30k-openclaw-backup.tar.gz -C /tmp/fusheng-30k/

# 步骤2：分析内容
tree -L 2 /tmp/fusheng-30k/.openclaw/workspace/

# 步骤3：导入核心组件
# 3.1 专家库（必须）
cp -r /tmp/fusheng-30k/.openclaw/workspace/experts/fusheng \
      ~/.openclaw/workspace/experts/

# 3.2 关键技能（必须）
for skill in self-improving-agent ontology stealth-browser; do
    cp -r /tmp/fusheng-30k/.openclaw/workspace/skills/$skill \
          ~/.openclaw/workspace/skills/ 2>/dev/null || echo "$skill 跳过"
done

# 3.3 配置参考（可选）
cp /tmp/fusheng-30k/.openclaw/config ~/.openclaw/config.fusheng-reference

# 步骤4：激活
openclaw restart

# 步骤5：验证
# 问它："如何在多台设备同步 OpenClaw？"
# 应该看到傅盛风格的回答
```

### 案例 2：学习 "三万" 的爬虫技能

```bash
# 假设三万是爬虫专家

# 步骤1：获取技能列表
cat > ~/.openclaw/workspace/experts/sanwan/crawler-skills.txt << 'EOF'
stealth-browser
playwright-scraper-skill
openclaw-ultra-scraping
scraping-recipes
crawl4ai-skill
browser-cash
EOF

# 步骤2：批量安装
while read skill; do
    skillhub install "$skill" || echo "$skill 安装失败"
done < ~/.openclaw/workspace/experts/sanwan/crawler-skills.txt

# 步骤3：导入三万的爬虫指南
cat > ~/.openclaw/workspace/experts/sanwan/crawler-guide.md << 'EOF'
# 三万：爬虫专家指南

## 反爬三板斧
1. 轮换 User-Agent
2. 使用住宅代理
3. 控制请求频率

## 常用命令
```bash
# Stealth 模式
python scripts/stealth_session.py -u "https://target.com" -s site

# 批量抓取
python crawler/batch.py --input urls.txt --output data.json
```
EOF

# 步骤4：创建三万匹配器
# （类似傅盛匹配器，但针对爬虫问题）
```

---

## 安全与伦理

### ⚠️ 重要提醒

1. **尊重隐私**
   - 不要复制他人的敏感信息
   - 不要泄露他人的 API Key
   - 不要传播他人的私人记忆

2. **合法获取**
   - 只复制你获得授权的配置
   - 开源/公开分享的经验可以学习
   - 商业机密不要碰

3. **个性化改造**
   - 不要完全复制，要融合自己的需求
   - 保留自己的身份和记忆
   - 学习思路，不是照搬

### 安全清单

```
□ 已获得原主人授权
□ 已删除敏感信息（API Key、Token）
□ 已检查无个人隐私数据
□ 已做个性化改造
□ 已测试功能正常
```

---

## 高级技巧

### 技巧 1：创建自己的专家品牌

```bash
# 学习傅盛后，创建你自己的风格

mkdir -p ~/.openclaw/workspace/experts/chengnuo

# 创建个人品牌配置
cat > ~/.openclaw/workspace/experts/chengnuo/profile.yml << 'EOF'
name: "澄诺"
signature: "🌟"
expertise:
  - 旅游规划
  - 内容创作
  - 数据分析

inspired_by:
  - fusheng  # 学习傅盛的系统化思维
  - sanwan   # 学习三万的爬虫技术

unique_traits:
  - 喜欢说 "老板"
  - 擅长做表格和思维导图
  - 结尾带 "🌟"
EOF
```

### 技巧 2：专家经验融合

```python
# expert_fusion.py - 融合多个专家经验

experts = ["fusheng", "sanwan", "yourself"]

# 合并推荐技能
all_skills = set()
for expert in experts:
    skills = load(f"experts/{expert}/recommended-skills.txt")
    all_skills.update(skills)

# 合并知识库
knowledge = {}
for expert in experts:
    kb = load(f"experts/{expert}/knowledge-base/")
    knowledge[expert] = kb

# 创建融合版回答
# "根据傅盛的经验...同时参考三万的方法...我的建议是..."
```

### 技巧 3：版本控制你的进化

```bash
# 用 Git 追踪你的 OpenClaw 进化

cd ~/.openclaw/workspace
git init
git add experts/ skills/ MEMORY.md SOUL.md
git commit -m "初始版本：学习傅盛前"

# 导入傅盛经验后
git add .
git commit -m "v2.0: 融合傅盛经验"

# 后续每次进化
git tag v3.0 "加入三万爬虫技能"
git tag v4.0 "形成个人风格"
```

---

## 故障排除

### 问题 1：导入后技能不生效

```bash
# 检查依赖
openclaw doctor

# 重新安装依赖
for skill in ~/.openclaw/workspace/skills/*/; do
    if [ -f "$skill/requirements.txt" ]; then
        pip install -r "$skill/requirements.txt"
    fi
done

# 重启
openclaw restart
```

### 问题 2：记忆冲突

```bash
# 合并记忆而不是覆盖
python << 'EOF'
import re

# 读取源记忆
with open('source/MEMORY.md') as f:
    source = f.read()

# 读取当前记忆
with open('.openclaw/workspace/MEMORY.md') as f:
    current = f.read()

# 智能合并（去重）
merged = current + "\n\n## 学习参考\n" + source

with open('.openclaw/workspace/MEMORY.md', 'w') as f:
    f.write(merged)
EOF
```

### 问题 3：个性冲突

```bash
# 保留核心身份，学习表达方式

# 原 SOUL.md 保留：
# - 你的名字
# - 你的使命
# - 你的价值观

# 学习专家的：
# - 说话风格
# - 专业术语
# - 解决问题的方法论
```

---

## 资源与社区

### 专家档案库（示例）

```
experts/
├── fusheng/          # 傅盛 - 养殖专家
├── sanwan/           # 三万 - 爬虫专家
├── xiaocheng/        # 小澄 - 旅游专家
└── YOUR_NAME/        # 你 - 未来的专家
```

### 分享你的经验

```bash
# 打包你的专家经验
tar czf my-openclaw-expertise.tar.gz \
       ~/.openclaw/workspace/experts/YOUR_NAME/ \
       ~/.openclaw/workspace/skills/YOUR_CUSTOM_SKILL/

# 分享给朋友
# 或提交到社区
```

---

## 总结

### 复制学习的三层境界

1. **照搬** - 完全复制（不推荐）
2. **学习** - 理解思路，选择性采用（推荐）
3. **创新** - 融合多家，形成自己的风格（目标）

### 傅盛最后的话

> 🦞 "学我者生，似我者死。学习我的养殖思路，但走出你自己的路！"

---

**现在，去复制学习吧！但记住——最终目标是成为别人想复制的对象！** 🚀

*Skill Version: 1.0.0*
*Compatible with: OpenClaw 2026.3.24+*