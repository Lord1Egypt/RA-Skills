# 联系人与跟进工作台

[English](README.md)

导入 CSV/vCard 联系人，按邮箱电话查重、合并记录、记录跟进并导出通讯录。

## 功能

导入 CSV/vCard 联系人，按邮箱电话查重、合并记录、记录跟进并导出通讯录。

在当前助手工作区运行，数据保存在本机。连接邮箱、网盘和日历时使用自己的账户参数。定时提醒通过 OpenClaw 的任务计划运行。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
预览这份contacts.csv的字段映射和重复联系人，确认前先不要导入。
```

```text
按邮箱和电话号码检查重复联系人，列出冲突字段，让我选择如何合并。
```

```text
记录今天与张先生的沟通，下周三跟进；列出本周待跟进联系人并导出CSV。
```

## 运行要求

Python 3.10+; vobject==0.9.9

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-contact-desk
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-contact-desk)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-contact-desk
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-contact-desk)。下载仓库 ZIP，将 `skills/mochi-contact-desk` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
