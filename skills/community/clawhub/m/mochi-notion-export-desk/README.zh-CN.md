# Notion 导出资料整理

[English](README.md)

读取 Notion 的 Markdown 与 CSV 导出包，整理页面索引、数据库行列统计和原文合集，保留来源路径及哈希。

## 能做什么

读取 Notion 的 Markdown 与 CSV 导出包，整理页面索引、数据库行列统计和原文合集，保留来源路径及哈希。

## 用法示例

安装后将下面任意一条发给助手，并提供所需文件或参数。

```text
把这个 Notion 导出包整理成页面索引和 Markdown 合集。
```

```text
看看导出的数据库有多少行、有哪些字段。
```

```text
列出导出包里未处理的附件，核对每个页面的来源哈希。
```

## 运行方式与边界

Python 3.10+，仅标准库。处理当前助手工作区内选定的资料，报告保存到新目录。

读取已导出的 Markdown 与 CSV ZIP，不同步 Notion API，不保证完整备份附件或权限。

## 运行要求

Python 3.10+；标准库

## 安装与开始使用

先[安装并连接 MochiLab Skills 助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，再发送：

```text
安装 mochi-notion-export-desk
```

免费注册即可连接助手并下载本免费 Skill。多 BOT 各自使用自己的 MochiLab 账户。也可在本页领取 ZIP，将包内技能目录放入目标助手工作区的 skills/，安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。

## 补充示例与操作要点

读取 Notion 的 Markdown 与 CSV 导出包，整理页面索引、数据库行列统计和原文合集，保留来源路径及哈希。

- 把这个 Notion 导出包整理成页面索引和 Markdown 合集。

- 看看导出的数据库有多少行、有哪些字段。

- 列出导出包里未处理的附件，核对每个页面的来源哈希。
