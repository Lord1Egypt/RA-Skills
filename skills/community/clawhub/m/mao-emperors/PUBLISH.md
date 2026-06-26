# 帝王会议 Skill - ClawHub 发布指南

## 📦 发布前检查清单

### 1. 文件完整性

确保以下文件存在且内容正确：

```
mao-emperors/
├── SKILL.md          ✅ 核心技能文档 (9.4KB)
├── README.md         ✅ 发布说明 (6.4KB)
├── skill.json        ✅ 元数据配置 (3.2KB)
├── EXAMPLES.md       ✅ 使用示例 (6.7KB)
└── agents/
    ├── MAO.md        ✅ 毛主席 Agent
    ├── QIN_SHIHUANG.md ✅ 秦始皇 Agent
    ├── HAN_WUDI.md   ✅ 汉武帝 Agent
    ├── TANG_TAIZONG.md ✅ 唐太宗 Agent
    └── ZHU_YUANZHANG.md ✅ 朱元璋 Agent
```

### 2. skill.json 检查

确保包含以下必填字段：
- ✅ `name`: "mao-emperors"
- ✅ `version`: "1.0.0" (semver 格式)
- ✅ `description`: 技能描述
- ✅ `author`: "水星魔女"
- ✅ `license`: "MIT"
- ✅ `tags`: 标签数组
- ✅ `triggers`: 触发词数组
- ✅ `agents`: Agent 列表

### 3. 内容质量检查

- ✅ SKILL.md 包含完整的使用说明
- ✅ README.md 包含安装和使用示例
- ✅ 至少有 2 个使用示例
- ✅ Agent 角色定义清晰
- ✅ 输出格式明确

---

## 🚀 发布步骤

### 步骤 1：登录 ClawHub

```bash
clawhub login
```

这会打开浏览器，使用 GitHub 账号登录。

### 步骤 2：发布技能

```bash
cd /Users/lts/.openclaw/workspace/skills
clawhub publish mao-emperors
```

### 步骤 3：填写发布信息

根据提示填写：
- **Slug:** `mao-emperors` (自动生成)
- **Display Name:** 帝王会议 - 毛选思想 Multi-Agent 系统
- **Version:** 1.0.0
- **Tags:** multi-agent,strategy,decision-making,chinese-history
- **Changelog:** 初始版本发布 - 5 位帝王 Agent，毛选思想集成

### 步骤 4：验证发布

访问 ClawHub 查看技能页面：
```
https://clawhub.com/mao-emperors
```

---

## 📝 发布后操作

### 1. 分享技能

**社交媒体：**
```
🎉 我在 ClawHub 发布了新技能「帝王会议」！

基于毛泽东选集核心思想的 Multi-Agent 决策系统，
毛主席指挥秦始皇、汉武帝、唐太宗、朱元璋为你分析战略、组织、决策问题。

🔗 https://clawhub.com/mao-emperors

#OpenClaw #MultiAgent #AI #毛选 #决策支持
```

**技术社区：**
- V2EX
- 知乎
- 掘金
- OpenClaw Discord

### 2. 收集反馈

创建 GitHub Issue 收集：
- Bug 报告
- 功能建议
- 使用案例分享

### 3. 持续迭代

**v1.1.0 计划：**
- [ ] 增加更多帝王（宋太祖、明成祖等）
- [ ] 支持自定义 Agent 配置
- [ ] 添加更多使用场景示例
- [ ] 优化输出格式

---

## ⚠️ 注意事项

### ClawHub 发布规范

1. **技能名称**
   - 唯一性（不能与现有技能重名）
   - 使用小写字母和连字符
   - 长度不超过 50 字符

2. **版本管理**
   - 遵循 semver 规范（major.minor.patch）
   - 每次发布必须递增版本号
   - breaking change 必须升级 major 版本

3. **内容规范**
   - 不得包含敏感政治内容
   - 不得包含虚假信息
   - 不得侵犯他人知识产权

4. **许可证**
   - 必须明确开源许可证
   - 推荐使用 MIT/Apache-2.0
   - 如有第三方依赖，需遵守其许可证

---

## 🐛 常见问题

### Q1: 发布失败 "Not logged in"

**解决：**
```bash
clawhub login
# 重新登录后再发布
```

### Q2: 发布失败 "Skill name already exists"

**解决：**
- 检查是否已经发布过
- 如果是自己的技能，使用新版本号重新发布
- 如果是他人的技能，修改技能名称

### Q3: 发布失败 "Invalid skill.json"

**解决：**
```bash
# 验证 JSON 格式
cat skill.json | python3 -m json.tool

# 检查必填字段
# name, version, description, author 必须存在
```

### Q4: 技能审核不通过

**可能原因：**
- 内容包含敏感信息
- 缺少必要文档
- 许可证不明确

**解决：**
- 根据审核反馈修改
- 重新发布新版本

---

## 📊 发布统计

发布后可以在 ClawHub 查看：
- 下载量
- 安装量
- 评分
- 评论

---

## 📞 支持

如有问题，联系：
- ClawHub 文档：https://clawhub.com/docs
- OpenClaw Discord: https://discord.gg/clawd
- 作者邮箱：threethreeliu@163.com

---

**祝发布顺利！** 🎉
