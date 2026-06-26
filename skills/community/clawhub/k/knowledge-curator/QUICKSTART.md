# 🚀 Knowledge Curator 快速开始

## 1 分钟上手指南

### 第一步：保存内容

**需要加收藏指令**，单纯发链接不会保存哦：

```
收藏 https://www.bilibili.com/video/BV1xx411c7mD
```

或

```
保存到知识库：https://www.bilibili.com/video/BV1xx411c7mD
```

AI 会自动：
- ✅ 抓取内容
- ✅ 生成摘要
- ✅ 提取知识点
- ✅ 自动分类
- ✅ 保存到知识库

### 第二步：查询内容

使用命令搜索知识库：

```
/kb search Python      # 搜索关键词
/kb list 学习          # 查看分类
/kb stats              # 查看统计
/kb recent             # 最近添加
```

### 第三步：管理内容

```
/kb view <ID>          # 查看详情
/kb delete <ID>        # 删除条目
/kb export             # 导出知识库
```

---

## 完整示例

### 保存 B 站视频

```
你：收藏 https://www.bilibili.com/video/BV1GJ411x7h7

AI: ✅ 已保存到知识库

📁 分类：学习/编程
📝 标题：Python 零基础入门教程
🏷️ 标签：#Python #编程 #教程 #入门
📅 日期：2026-03-15 23:45

💡 关键知识点:
- Python 环境安装与配置
- 基础语法：变量、数据类型
- 控制流程：条件判断、循环
```

**注意**：如果只发链接不带"收藏"指令，AI 不会保存哦～

### 搜索内容

```
你：/kb search Python

AI: 🔍 找到 3 条相关内容：

1️⃣ [学习/编程] Python 零基础入门教程
   📅 2026-03-15 | #Python #编程 #教程

2️⃣ [学习/编程] Python 数据分析实战
   📅 2026-03-14 | #Python #数据分析

3️⃣ [工作/效率] 用 Python 自动化办公
   📅 2026-03-13 | #Python #自动化
```

---

## 支持的平台

| 平台 | 示例链接 | 提取内容 |
|------|----------|----------|
| 📺 B 站 | bilibili.com/video/... | 标题、简介、字幕 |
| 📕 小红书 | xiaohongshu.com/... | 标题、正文、标签 |
| 📖 知乎 | zhihu.com/... | 问题、回答、作者 |
| 📹 YouTube | youtube.com/watch/... | 标题、描述、字幕 |
| 🌐 通用网页 | 任意 URL | 标题、正文、描述 |

---

## 分类体系

内容按主题自动分类到 6 大类别：

- 🖥️ **科技** - AI、编程、数码、互联网
- 🏠 **生活** - 美食、旅行、家居、情感
- 📚 **学习** - 教育、课程、教程、技能
- 🎮 **娱乐** - 影视、音乐、游戏、综艺
- 💼 **工作** - 职场、管理、效率、商业
- 💪 **健康** - 运动、饮食、医疗、养生

---

## 常用命令速查

| 命令 | 功能 | 示例 |
|------|------|------|
| `/kb search <词>` | 搜索 | `/kb search AI` |
| `/kb list [分类]` | 列出 | `/kb list 学习` |
| `/kb view <ID>` | 详情 | `/kb view kb-123` |
| `/kb recent` | 最近 | `/kb recent` |
| `/kb stats` | 统计 | `/kb stats` |
| `/kb delete <ID>` | 删除 | `/kb delete kb-123` |
| `/kb export` | 导出 | `/kb export` |
| `/kb help` | 帮助 | `/kb help` |

---

## 高级用法

### 指定分类保存
```
收藏到工作：https://zhuanlan.zhihu.com/p/xxx
```

### 添加备注
```
收藏这个，备注：明天要看
https://example.com/...
```

### 批量保存
```
批量收藏：
链接 1
链接 2
链接 3
```

---

## 文件结构

```
knowledge-curator/
├── SKILL.md           # 技能定义
├── README.md          # 详细文档
├── QUICKSTART.md      # 本文件
├── scripts/           # 核心脚本
│   ├── main.js        # 主入口
│   ├── fetch.js       # 内容抓取
│   ├── summarize.js   # 内容总结
│   ├── categorize.js  # 自动分类
│   ├── store.js       # 存储管理
│   └── query.js       # 查询检索
└── knowledge-base/    # 知识库
    ├── 科技/
    ├── 生活/
    ├── 学习/
    ├── 娱乐/
    ├── 工作/
    ├── 健康/
    └── index.json     # 索引
```

---

## 测试功能

运行测试验证安装：

```bash
cd skills/knowledge-curator
node scripts/test.js
```

看到 `6 通过 / 0 失败` 即表示安装成功。

---

## 遇到问题？

### 无法抓取内容
- 检查链接是否有效
- 部分平台有反爬限制，稍后重试

### 分类不准确
- 可手动指定：`保存到 [分类]: [链接]`

### 搜索结果为空
- 尝试更换关键词
- 检查是否已保存内容

---

## 开始使用

现在就开始保存你的第一个链接吧！🎉

```
https://...
```

---

**版本**: v1.0.0  
**最后更新**: 2026-03-15
