# GitHub Repo Deep Dive

> 输入任意 GitHub 开源项目，一键生成完整技术架构分析、知识卡片和多平台发布内容。

## 🎯 业务场景

**技术选型调研** — 团队在评估引入某个开源库时，往往需要花 1-2 小时阅读 README、搜索评价、梳理架构。这个工具将这个过程压缩到 **5 分钟自动完成**。

**典型用户画像：**
- 后端/全栈工程师：评估新框架/库是否值得投入
- 技术总监/CTO：快速了解团队正在使用的项目
- 技术博主：批量生成高质量开源项目解读内容
- 开源爱好者：系统化积累对社区项目的理解

## 😣 痛点

| 痛点 | 现状 | 解决后 |
|------|------|--------|
| 读 README 太慢 | 手动浏览，理解效率低 | AI 摘要一键提炼重点 |
| 不知道项目社区反馈 | 到处搜索 Twitter/Reddit | Agent-Reach 自动聚合 |
| 架构分析靠猜 | 看文件结构一头雾水 | 结构化分析输出 |
| 想分享但没有素材 | 手动作图费时费力 | 自动生成知识卡片 |
| 报告难沉淀 | 复制粘贴到各处 | 结构化 Markdown 输出 |

## 🔧 Skill 编排图谱

```
[用户输入 GitHub URL]
        │
        ▼
┌─────────────────────┐
│  ① github           │  获取仓库元数据（描述/语言/Stars/ Fork数）
│  (gh CLI)           │  获取文件结构树、README 内容
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  ② summarize        │  AI 深度摘要 README 和关键文档
│  (summarize CLI)    │  提炼技术亮点、架构模式、使用限制
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  ③ Agent-Reach      │  搜索 Twitter/X Reddit HackerNews 评价
│  (社交媒体搜索)     │  收集真实用户使用反馈、优缺点
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  ④ card-renderer    │  生成小红书风格架构解读卡片
│  (Mac Pro 极客风)   │  封面图 + 详情页，适配多平台发布
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  ⑤ 输出结构化报告   │  Markdown 格式，可同步到 Wiki/Obsidian
│  (最终交付物)       │  含架构分析 + 卡片图 + 社区反馈
└─────────────────────┘
```

## 📦 涉及技能

| # | 技能 | 角色 | 关键操作 |
|---|------|------|---------|
| 1 | `github` | 数据采集 | `gh repo view`, `gh api`, README 读取 |
| 2 | `summarize` | 内容提炼 | `summarize <url>` 生成摘要 |
| 3 | `Agent-Reach` | 舆情分析 | 搜索 Twitter/Reddit 评价 |
| 4 | `card-renderer` | 可视化 | `render_mac_pro_card.py` 生成极客风卡片 |

## 🚀 使用示例

### 场景：评估 `microsoft/TypeScript` 是否值得深入学习

**输入：**
```
分析 https://github.com/microsoft/TypeScript
```

**自动执行流程：**

1. `gh repo view microsoft/TypeScript` → 获取基本信息
   - 语言：TypeScript，Stars: 99k+，描述：JavaScript 超集

2. `gh api repos/microsoft/TypeScript/contents` → 获取文件树
   - 发现 `src/compiler/` 核心目录结构

3. `summarize "https://github.com/microsoft/TypeScript"` → README 摘要
   - 提炼：编译时类型检查、跨平台支持、VS Code 深度集成

4. `Agent-Reach` → 搜索社区评价
   - Twitter: "TypeScript 已经是前端标配"
   - Reddit: "类型系统是最大优势，编译速度是痛点"

5. `card-renderer` → 生成架构卡片
   - 封面：TypeScript 定位 + Star 数
   - 详情：架构模式 + 优缺点 + 适用场景

**输出：** 完整 Markdown 报告 + 知识卡片图片

### 场景：批量对比三个框架

**输入：**
```
对比 Next.js、Remix、 Astro 的架构差异
```

**自动执行：** 依次分析三个仓库，生成并排对比报告

## 📋 输出文档结构

```markdown
# [项目名] 深度技术解读

## 📊 基本信息
- 仓库：owner/repo
- 语言：TypeScript
- Stars：99,000+
- 最新版本：v5.4.0

## 🎯 项目定位
[一句话描述]

## 🏗️ 架构分析
[核心模块解读]

## 📦 技术栈
[关键依赖分析]

## 💬 社区反馈
[优缺点总结]

## ✅ 适用场景
[何时选用 / 不选用]

## 🔗 相关资源
[官方文档/ Playground 链接]
```

## ⚙️ 扩展方向

- **飞书 Wiki 同步**：接入 `feishu-wiki` 将报告自动发布为 Wiki 页面
- **定时监控**：对核心项目设置 Star 变化监控，定时推送更新报告
- **Obsidian 归档**：接入 `obsidian` 自动创建笔记并建立双向链接
- **对比报告生成**：批量分析多个仓库，输出对比矩阵
