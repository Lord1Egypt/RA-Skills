---
name: design-md
version: 0.1.0
description: 在 Markdown 文档里插入脑图或架构图。用户说"画个脑图"、"画架构图"、"插入图表"、"mind map"、"diagram"时触发。
argument-hint: [图表描述，可选]
allowed-tools: Write, Bash, Read
metadata:
  openclaw:
    requires:
      bins:
        - mddoc
        - d2
---

向 Markdown 文档插入图表时，始终遵循以下规则。

## 依赖检查

**开始任何操作前，先检查依赖是否已安装：**

```bash
which mddoc && which d2
```

若 `mddoc` 未安装：

```bash
npm install -g mddoc-cli
```

若 `d2` 未安装：

- macOS：`brew install d2`
- Windows：`winget install terrastruct.d2`
- Linux / 其他：参考 https://d2lang.com/tour/install

两个都就绪后再继续。

## 规则

- 所有图表源文件和 PNG **只放在 `.mddoc/` 目录**（与 Markdown 文件平级）
- 文件名用**英文小写 + 连字符**（`auth-flow`、`module-overview`），不用中文或序号
- **先写源文件，再生成 PNG，再插入 Markdown**，顺序不可颠倒
- Markdown 正文中**永远不要**直接写 D2 或 markmap 代码块
- `.mddoc/` 不存在时先创建

## 脑图（.mmd）

**1. 写源文件** → `.mddoc/<name>.mmd`，格式为 markmap markdown：

```markdown
# 根节点标题

## 一级分支
- 叶节点
- 叶节点

## 一级分支
- 叶节点
  - 二级叶节点
```

**2. 生成 PNG：**

```bash
mddoc mindmap .mddoc/<name>.mmd
```

**3. 插入 Markdown：**

```markdown
![脑图：<描述>](.mddoc/<name>.png)
*源文件：[<name>.mmd](.mddoc/<name>.mmd)*
```

## 架构图（.d2）

**1. 写源文件** → `.mddoc/<name>.d2`，格式为 D2 语言：

```d2
direction: right

client: 客户端 {shape: rectangle}
gateway: API Gateway {shape: rectangle}
db: Database {shape: cylinder}

client -> gateway -> db
```

**2. 生成 PNG：**

```bash
mddoc arch .mddoc/<name>.d2
```

**3. 插入 Markdown：**

```markdown
![架构图：<描述>](.mddoc/<name>.png)
*源文件：[<name>.d2](.mddoc/<name>.d2)*
```

## 批量重新生成

```bash
mddoc build
```

## 反馈与问题

遇到问题或有建议，请到 GitHub 提 issue：
https://github.com/drunkpig/md-of-programer/issues
