# 学习陪练与错题复习

[English](README.md)

批量导入题库，保存答题与复习进度，统计练习结果，导出不含答案的复习清单。

## 实际功能

批量导入题库，保存答题与复习进度，统计练习结果，导出不含答案的复习清单。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
导入我提供的题库，今天抽五道练习，逐题提问并记录答题结果。
```

```text
找出我之前答错的题，先给提示，等我回答后再解析。
```

```text
根据已保存的练习记录生成复习清单，导出不含答案的版本。
```

## 导出结果

review-plan.md / review-queue.csv

文件保存在当前助手工作区，返回路径和 SHA256；记录与历史导出保留。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+、当前助手工作区的读写权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-study-coach
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-study-coach)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-study-coach
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-study-coach)。下载仓库 ZIP，将 `skills/mochi-study-coach` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
