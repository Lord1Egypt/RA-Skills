# Human-Like Memory v1.1.0 快速测试指南

## 🚀 零配置使用

**重要**: 本技能支持**自动安装依赖**，无需手动执行 `npm install`！

### 正确使用方法

**在 OpenClaw 对话中直接使用命令**（不是在系统控制台）：

```
/remember 我住在杭州，喜欢喝拿铁
/memory stats
```

---

## ⚠️ 重要说明

### 1. 命令输入位置

**❌ 错误**: 在 Linux 终端/控制台输入 `/remember`
```bash
# 这样没用！
/admin$ /remember 测试
```

**✅ 正确**: 在 OpenClaw **聊天对话**中输入
```
你：/remember 我住在杭州，喜欢喝拿铁
AI: ✅ 已记住：杭州居住偏好 (重要性：75)
```

### 2. 依赖自动安装

**v1.1.0 改进**: 技能元数据中包含依赖信息，OpenClaw 会**自动安装**

```json
{
  "openclaw": {
    "requires": {"bins": ["node"]},
    "install": [
      {
        "kind": "node",
        "package": "@xenova/transformers",
        "label": "安装向量化引擎依赖"
      }
    ]
  }
}
```

**安装流程**:
1. 用户执行 `clawhub install human-like-memory-cn`
2. OpenClaw 自动检测依赖
3. **后台自动执行** `npm install @xenova/transformers`
4. 安装完成后技能可用

**无需手动操作！**

---

## 📋 测试方案（在对话中测试）

### 方案 A: 快速功能测试（5 分钟）

**在 OpenClaw 聊天窗口输入以下内容**：

#### 步骤 1: 创建记忆
```
/remember 我住在杭州西湖区，喜欢喝拿铁咖啡
```

**预期回复**:
```
✅ 已创建记忆：杭州居住偏好
   - 重要性：75 分
   - 分类：preference
   - 存储：WARM 记忆
```

#### 步骤 2: 再创建几条
```
/remember 下周三下午 2 点有重要会议，需要准备 Q2 报告
/remember 对芒果过敏，不要推荐含芒果的食物
/remember 正在开发一个电商项目，使用 React 和 Node.js
```

#### 步骤 3: 查看统计
```
/memory stats
```

**预期回复**:
```
📊 记忆统计 (v1.1.0)

总记忆数：4 条
向量化率：100%
平均重要性：71 分

压缩分布:
├─ 原文保留：1 条（25%）- 重要会议
├─ 摘要压缩：2 条（50%）- 居住偏好、电商项目
└─ 关键词：1 条（25%）- 芒果过敏

Token 效率:
├─ 原始大小：~320 tokens
├─ 压缩后：~180 tokens
└─ 节省：44%
```

#### 步骤 4: 测试语义搜索
```
/memory search 咖啡
```

**预期回复**:
```
🔍 搜索结果："咖啡"

1. [相似度 0.89] 喜欢喝拿铁咖啡
   重要性：75 分 | 分类：preference
```

#### 步骤 5: 测试智能问答
```
问：我住在哪里？
```

**预期回复**:
```
📚 根据记忆，你住在杭州西湖区。

💡 相关记忆:
• 喜欢喝拿铁咖啡 [preference]
• 对芒果过敏 [fact]
```

---

### 方案 B: 向量化测试（需要网络，10 分钟）

**前提**: 首次使用会自动下载模型（约 200MB）

#### 测试语义搜索
```
/remember 我喜欢吃重庆火锅，偏好麻辣口味
/remember 上海菜偏甜，我不太喜欢
/remember 川菜很辣，但是很好吃

/memory search 我喜欢吃什么口味的菜？
```

**预期**: 返回火锅/麻辣相关记忆（即使问题中没有 exact match）

---

### 方案 C: 按需注入测试

```
# 先创建一些记忆
/remember 明天下午 2 点有产品评审会议
/remember 我喜欢蓝色，设计时优先用蓝色
/remember 对芒果过敏

# 然后问一个具体问题
问：我明天有什么安排？
```

**预期**: 只注入会议相关记忆，不注入颜色偏好和过敏信息

---

## 🐛 故障排除

### 问题 1: 命令没反应

**可能原因**: 在系统控制台输入，而不是在聊天对话中

**解决方案**: 
- 确保在 OpenClaw **聊天窗口**输入命令
- 命令格式：`/remember [内容]`

### 问题 2: 依赖未安装

**检查方法**:
```
/memory stats
```

如果报错说缺少依赖，手动安装：
```bash
cd /home/admin/openclaw/workspace/skills/human-like-memory
npm install
```

### 问题 3: 向量化失败

**错误**: "fetch failed" 或 "模型下载失败"

**解决方案**:
```bash
# 方案 1: 使用国内镜像
export HF_ENDPOINT=https://hf-mirror.com
cd /home/admin/openclaw/workspace/skills/human-like-memory
npm install

# 方案 2: 临时关闭向量搜索
# 编辑 config.json，添加:
{ "useVectorSearch": false }
```

---

## 📊 测试检查清单

测试完成后，确认以下项目：

- [ ] `/remember` 命令可以创建记忆
- [ ] `/memory stats` 显示统计信息
- [ ] `/memory search` 可以搜索记忆
- [ ] 语义搜索返回相关结果（即使没有 exact match）
- [ ] 记忆按重要性自动压缩
- [ ] 对话中自动注入相关记忆

---

## 💡 常用命令速查

| 命令 | 功能 | 示例 |
|------|------|------|
| `/remember [内容]` | 创建记忆 | `/remember 我喜欢喝拿铁` |
| `/memory stats` | 查看统计 | `/memory stats` |
| `/memory search [关键词]` | 搜索记忆 | `/memory search 咖啡` |
| `/memory review` | 复习记忆 | `/memory review` |
| `/memory compact` | 手动压缩 | `/memory compact` |

---

## 🎯 开始测试

**现在就在聊天对话中输入**:

```
/remember 我住在杭州，喜欢喝拿铁
```

**如果成功**，你会看到记忆创建确认。

**如果失败**，告诉我错误信息，我会帮你解决！

---

*测试版本：v1.1.0 | 更新时间：2026-03-31*
