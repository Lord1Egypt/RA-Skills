# Knowledge Curator 使用示例

## 📥 保存内容

### 基础用法

直接发送链接：
```
用户：https://www.bilibili.com/video/BV1GJ411x7h7

AI: ✅ 已保存到知识库

📁 分类：学习/编程
📝 标题：Python 零基础入门教程
🏷️ 标签：#Python #编程 #教程 #入门
📅 日期：2026-03-15 23:45
🔗 链接：https://www.bilibili.com/video/BV1GJ411x7h7

💡 关键知识点:
- Python 环境安装与配置
- 基础语法：变量、数据类型
- 控制流程：条件判断、循环
- 函数定义与调用
```

### 指定分类保存

```
用户：保存到工作：https://zhuanlan.zhihu.com/p/123456

AI: ✅ 已保存到知识库【工作】

📝 标题：职场沟通技巧指南
🏷️ 标签：#职场 #沟通 #技巧 #工作
```

### 添加备注

```
用户：收藏这个，备注：明天要看
https://www.xiaohongshu.com/discovery/item/xxx

AI: ✅ 已保存，已添加备注

📝 备注：明天要看
```

---

## 🔍 查询内容

### 关键词搜索

```
用户：/kb search Python

AI: 🔍 找到 5 条相关内容：

1️⃣ [学习/编程] Python 零基础入门教程
   📅 2026-03-15 | #Python #编程 #教程
   ID: kb-1710518700-a1b2c3d4

2️⃣ [学习/编程] Python 数据分析实战
   📅 2026-03-14 | #Python #数据分析 #实战
   ID: kb-1710432300-e5f6g7h8

3️⃣ [工作/效率] 用 Python 自动化办公
   📅 2026-03-13 | #Python #自动化 #办公
   ID: kb-1710345900-i9j0k1l2

4️⃣ [科技/AI] Python 机器学习入门
   📅 2026-03-12 | #Python #机器学习 #AI
   ID: kb-1710259500-m3n4o5p6

5️⃣ [学习/课程] Python 网课推荐
   📅 2026-03-10 | #Python #网课 #推荐
   ID: kb-1710086700-q7r8s9t0

输入 `/kb view <ID>` 查看详细内容
```

### 按分类查看

```
用户：/kb list 学习

AI: 📚 学习分类 (15 条)

最近添加:
1. [编程] Python 零基础入门教程 (2026-03-15)
2. [编程] JavaScript 进阶指南 (2026-03-14)
3. [课程] 吴恩达机器学习笔记 (2026-03-13)
4. [教程] Git 版本控制教程 (2026-03-12)
5. [技能] 时间管理方法论 (2026-03-11)

... 还有 10 条，使用 `/kb list 学习 --all` 查看全部
```

### 查看条目详情

```
用户：/kb view kb-1710518700-a1b2c3d4

AI: 📖 Python 零基础入门教程

**原始链接**: https://www.bilibili.com/video/BV1GJ411x7h7
**来源平台**: B 站
**收藏日期**: 2026-03-15 23:45
**分类**: 学习/编程
**标签**: #Python #编程 #教程 #入门

## 摘要
本教程适合零基础的 Python 学习者，从环境安装开始讲解，
涵盖基础语法、数据类型、控制流程、函数等核心概念。
通过实例演示帮助初学者快速上手 Python 编程。

## 关键知识点
- Python 环境安装与配置
- 基础语法：变量、数据类型
- 控制流程：条件判断、循环
- 函数定义与调用
- 常用内置函数

## 备注
无

---
*由 Knowledge Curator 自动整理*
```

---

## 📊 管理命令

### 查看统计

```
用户：/kb stats

AI: 📊 知识库统计

📚 总条目数：42
📁 分类分布:
   🖥️ 科技：12 条
   📚 学习：15 条
   💼 工作：8 条
   🏠 生活：4 条
   🎮 娱乐：2 条
   💪 健康：1 条

📅 最近 7 天新增：8 条
🏷️ 热门标签：#Python #AI #教程 #效率 #学习

💾 存储位置：knowledge-base/
📄 索引文件：index.json (已更新)
```

### 删除条目

```
用户：/kb delete kb-1710518700-a1b2c3d4

AI: ⚠️ 确认删除？
标题：Python 零基础入门教程
分类：学习/编程

回复"确认"完成删除，或回复"取消"放弃
```

```
用户：确认

AI: ✅ 已删除条目
📝 Python 零基础入门教程
```

### 导出知识库

```
用户：/kb export

AI: 📥 选择导出格式：
1. Markdown - 适合阅读
2. JSON - 适合备份
3. CSV - 适合导入其他工具

回复数字选择，或回复"取消"
```

```
用户：1

AI: ✅ 已导出为 Markdown
📄 文件：knowledge-export-20260315.md
📊 包含：42 条条目
💾 位置：C:\Users\ma\.openclaw\workspace\skills\knowledge-curator\exports\
```

---

## 🎯 高级用法

### 批量保存

```
用户：批量保存以下链接：
https://www.bilibili.com/video/BV1xx411c7mD
https://www.bilibili.com/video/BV1yy411c7mD
https://www.bilibili.com/video/BV1zz411c7mD

AI: 🔄 开始批量处理 (3 条)...

✅ [1/3] Python 入门教程 → 学习/编程
✅ [2/3] JavaScript 进阶 → 学习/编程
✅ [3/3] React 实战项目 → 学习/编程

📊 完成：成功 3 条，失败 0 条
```

### 语义搜索

```
用户：/kb search 如何学习编程

AI: 🔍 语义搜索 "如何学习编程"

找到 7 条相关内容：

1️⃣ [学习/编程] 编程学习路线图
   🎯 匹配：学习路线、编程入门

2️⃣ [学习/教程] 零基础学编程指南
   🎯 匹配：零基础、学习指南

3️⃣ [学习/课程] 编程网课推荐
   🎯 匹配：课程、学习资源

...
```

### 定期整理

```
用户：/kb cleanup

AI: 🧹 知识库整理报告

📋 检查结果:
- 重复条目：0 条
- 无效链接：2 条
- 未分类条目：1 条

🔧 建议操作:
1. 删除 2 条无效链接
2. 为 1 条未分类条目指定分类

回复"执行"应用建议，或回复"查看"查看详情
```

---

## 💡 使用技巧

### 1. 添加个人笔记
```
用户：保存这个，笔记：这个技巧很实用，下次项目可以用
https://zhuanlan.zhihu.com/p/xxx
```

### 2. 跨平台收藏
```
用户：小红书那个美妆教程也保存一下
https://xiaohongshu.com/discovery/item/xxx

AI: ✅ 已识别小红书链接，保存到【生活/美妆】
```

### 3. 视频内容处理
```
用户：https://www.youtube.com/watch?v=xxx

AI: ✅ 已保存视频内容

📹 视频：AI 技术详解
⏱️ 时长：15:32
📝 已提取字幕并生成摘要
🏷️ 标签：#AI #技术 #YouTube #视频
```

### 4. 快速回顾
```
用户：/kb recent

AI: 📅 最近添加 (7 天内)

1. [学习] Python 入门教程 (今天)
2. [工作] 效率工具推荐 (昨天)
3. [科技] AI 新闻汇总 (2 天前)
4. [生活] 美食探店 (3 天前)
...
```

---

## ⚙️ 配置示例

在 `scripts/config.js` 中自定义：

```javascript
module.exports = {
  // 知识库路径
  knowledgeBasePath: './knowledge-base',
  
  // 索引文件
  indexPath: './knowledge-base/index.json',
  
  // 分类列表
  categories: ['科技', '生活', '学习', '娱乐', '工作', '健康'],
  
  // 摘要最大长度
  summaryMaxLength: 500,
  
  // 去重阈值 (0-1)
  duplicateThreshold: 0.85,
  
  // 请求延迟 (ms)
  requestDelay: 1000,
  
  // 启用语义搜索
  enableSemanticSearch: true,
  
  // 导出目录
  exportPath: './exports'
};
```

---

## 📝 输出格式示例

保存后的 Markdown 文件内容：

```markdown
# Python 零基础入门教程

**原始链接**: [https://www.bilibili.com/video/BV1GJ411x7h7](https://www.bilibili.com/video/BV1GJ411x7h7)
**来源平台**: B 站
**收藏日期**: 2026-03-15 23:45
**分类**: 学习
**标签**: #Python #编程 #教程 #入门

## 摘要
本教程适合零基础的 Python 学习者，从环境安装开始讲解，
涵盖基础语法、数据类型、控制流程、函数等核心概念。
通过实例演示帮助初学者快速上手 Python 编程。

## 关键知识点
- Python 环境安装与配置
- 基础语法：变量、数据类型
- 控制流程：条件判断、循环
- 函数定义与调用
- 常用内置函数

## 原文内容
[视频简介和字幕内容...]

## 备注
无

---
*由 Knowledge Curator 自动整理*
```

---

**最后更新**: 2026-03-15  
**版本**: v1.0.0
