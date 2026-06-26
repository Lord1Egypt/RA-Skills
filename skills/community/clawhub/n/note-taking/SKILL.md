---
name: note-taking
description: 笔记创建与管理的规范指南。当需要创建新笔记、管理笔记目录时使用此 skill。包含：笔记层级结构、语言规范、命名规则、通用模板。
repository: https://github.com/tino-chen/openclaw-skills/tree/main/note-taking
clawhub: https://clawhub.com/skills/note-taking
guide: https://tino-chen.github.io/notes/workflows/auto-note-system.html
---

# 笔记管理系统规范

本文档定义了一个通用的笔记创建、管理规范框架。每次创建或修改笔记时，遵循此规范。

---

## 一、笔记层级结构

### 一级文件夹（导航）

- 文件夹名：kebab-case
- 对应导航名称：Title Case
- **文件夹名与导航名称的对应关系**：kebab-case → Title Case
- 每个一级文件夹下必须有 `index.md`

### 二级文件夹（分组）

- 文件夹名：kebab-case
- 对应分组名称：Title Case
- **文件夹名与分组名称的对应关系**：kebab-case → Title Case

### 笔记文档

- 位置：二级文件夹下
- 命名：**kebab-case**（如 `xxx-yyy.md`）
- **文档内的一级标题 (H1) = 该分组下笔记索引名称**（中文，完全一致）

### index.md 索引目录

- 位置：每个一级文件夹根目录
- 作用：介绍这个分类下有什么内容，给读者一个全局视图
- 内容：分组介绍（如 Network 分组包含哪些笔记）
- **不要放快速链接**

---

## 二、语言规范

| 元素 | 语言 |
|------|------|
| 导航（一级文件夹名） | 英文 |
| 分组（二级文件夹名） | 英文 |
| 笔记内容 | 中文 |

---

## 三、文档类型

| 类型 | 说明 |
|------|------|
| **knowledge** | 知识：概念解析、原理说明、调研报告 |
| **guide** | 教程：步骤指南 |
| **experience** | 经验：最佳实践、踩坑记录、项目复盘 |

---

## 四、通用笔记模板

```yaml
---
type: 类型
title: 标题
tags: [标签1, 标签2]
---

# 标题

... 正文内容 ...

## 参考资料

- [标题1](链接1)
- [标题2](链接2)
```

### 要求

1. **元数据（必须）**
   - `type`: guide | knowledge | experience
   - `title`: 笔记标题
   - `tags`: 标签数组

2. **H1 标题（必须）**
   - 中文，与索引名称一致

3. **参考资料（必须）**
   - 放在文档最后
   - 无序列表格式
   - 包含标题和链接

---

## 五、命名规范

| 元素 | 风格 | 示例 |
|------|------|------|
| 一级文件夹 | kebab-case | `xxx/` |
| 二级文件夹 | kebab-case | `xxx-yyy/` |
| 笔记文档 | kebab-case | `xxx-yyy-zzz.md` |
| 导航名称 | Title Case | "Xxx" |
| 分组名称 | Title Case | "Xxx Yyy" |
| 文档 H1 标题 | 中文，与索引名一致 | `# 标题` |

---

## 六、目录结构示例

```
notes/
├── xxx/                              # 导航: Xxx
│   ├── index.md                      # 分组介绍
│   ├── xxx-yyy/                     # 分组: Xxx Yyy
│   │   └── aaa-bbb.md              # H1: Aaa Bbb
│   └── xxx-zzz/                     # 分组: Xxx Zzz
│       └── ccc-ddd.md               # H1: Ccc Ddd
├── yyy/                              # 导航: Yyy
│   ├── index.md
│   └── ...
└── ...
```

---

## 七、笔记标题长度

**建议**：H1 标题控制在 **30 字符以内**，避免侧边栏换行显示不美观。

---

## 八、侧边栏配置

**重要**：只有当目录下有实际笔记时，才配置侧边栏。空目录不配置侧边栏。

### 配置规则

1. **侧边栏路径与文件夹路径一致**
   - 一级导航对应一个侧边栏配置
   - 二级分组对应一个侧边栏分组

### 示例

```typescript
sidebar: {
  '/tool/': [
    {
      text: 'Network',
      collapsed: false,
      items: [
        { text: 'Tailscale - 如何远程连接 Mac Mini ?', link: '/tool/network/tailscale-remote-connect' },
      ]
    }
  ]
}
```

### 操作流程

1. 添加新笔记后，在 config.ts 中找到对应的 sidebar
2. 在对应的分组下添加新的 item
3. **text 必须与笔记 H1 标题完全一致**

---

## 九、index.md 分组介绍

每个一级导航目录下的 index.md 应该包含**分组介绍**，说明该导航下有哪些分组。

### 示例

```markdown
# Tool

本分类下包含各类工具的使用指南。

## Network

网络相关工具的使用指南和教程。
```

### 注意

- 初始时 index.md 可以为空（`# `），等有分组后再添加
- **先创建分组目录和笔记，再更新 index.md**

---

## 十、检查清单

创建/修改笔记时 checklist：

- [ ] 一级文件夹名 = 导航名（英文，kebab-case）
- [ ] 二级文件夹名 = 分组名（英文，kebab-case）
- [ ] 文档名 = kebab-case
- [ ] 导航名称 = Title Case
- [ ] 分组名称 = Title Case
- [ ] 文档 H1 标题 = 笔记索引名（中文）
- [ ] **H1 标题控制在 30 字符以内**
- [ ] **更新一级目录下的 index.md，添加分组介绍**
- [ ] frontmatter 包含 type, title, tags
- [ ] 内容使用中文
- [ ] 最后一部分是"参考资料"
- [ ] 有笔记的目录才配置 sidebar，空目录不配置
- [ ] 侧边栏 text 与 H1 标题完全一致
- [ ] 提交到 GitHub

---

## 十一、操作流程

### 创建新笔记

1. 确定所属导航（一级文件夹）和分组（二级文件夹）
2. 如果目录不存在，创建它们（kebab-case）
3. 创建笔记文档（kebab-case.md）
4. 按照通用模板填写内容，**H1 标题控制在 30 字符以内**
5. **更新一级文件夹下的 index.md，添加分组介绍**
6. **更新 .vitepress/config.ts 中的 sidebar 配置**
   - text 必须与笔记 H1 标题完全一致
7. 提交到 GitHub
