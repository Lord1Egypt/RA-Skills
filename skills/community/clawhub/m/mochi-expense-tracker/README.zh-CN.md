# 日常记账与预算

[English](README.md)

导入 CSV 账单、识别重复记录，精确汇总收支与预算，导出账本和报告。

## 实际功能

导入 CSV 账单、识别重复记录，精确汇总收支与预算，导出账本和报告。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
记录今天午饭32元、交通18元，分别归入餐饮和交通。
```

```text
导入这份账单CSV，先检查重复记录，再按月份和类别汇总收支。
```

```text
把本月餐饮预算设为1500元，生成预算使用报告和账本CSV。
```

## 导出结果

ledger.csv / budget-report.md

文件保存在当前助手工作区，返回路径和 SHA256；记录与历史导出保留。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+、当前助手工作区的读写权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-expense-tracker
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-expense-tracker)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-expense-tracker
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-expense-tracker)。下载仓库 ZIP，将 `skills/mochi-expense-tracker` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
