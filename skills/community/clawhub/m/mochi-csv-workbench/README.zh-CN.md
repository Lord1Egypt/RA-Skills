# CSV清洗分析工作台

[English](README.md)

清洗 CSV/TSV、统计空值和重复行，按指定分组精确汇总金额。

## 功能

读取 UTF-8 CSV/TSV，支持 BOM、引号、逗号和多行单元格。生成列统计、空值与重复行报告，并导出带公式防护的 CSV。小数合计使用精确计算。

默认去除完全重复的行；保留重复交易时使用 `--keep-duplicates`。指定分组列与金额列后，各币种分别汇总，缺失或无效金额另列明细。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
检查这份orders.csv的空值和完全重复行，生成数据质量报告。
```

```text
清洗这份CSV，去除完全重复的行，保留原文件并另存结果。
```

```text
按客户和币种分别汇总amount列，使用精确小数计算，导出汇总CSV。
```

## 高级用法：在终端手动运行

下面是开发者手动运行命令。在安装 OpenClaw 的电脑或服务器终端执行；日常使用直接发送上面的对话示例即可。

先把命令中的占位名称换成实际路径：

- `SKILL_DIRECTORY`：已安装的这个Skill文件夹。
- `INPUT.csv`：要处理的CSV文件。
- `NEW_OUTPUT_DIRECTORY`：新建的结果目录。

```text
node "SKILL_DIRECTORY/scripts/csv.mjs" --input "INPUT.csv" --out "NEW_OUTPUT_DIRECTORY" --group-by "币种" --sum-column "金额" --keep-duplicates
```

把路径和列名替换为文件中的实际值。包内 `samples/currency-input.csv` 包含中文表头的分币种样例。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+ 或 26.1+，以及本地命令和工作目录读写权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-csv-workbench
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-csv-workbench)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-csv-workbench
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-csv-workbench)。下载仓库 ZIP，将 `skills/mochi-csv-workbench` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。

## 补充示例与操作要点

中文示例：“删除明确重复的收款行，用币种列分组、金额列精确汇总，USD和CNY分别列出；空币种、缺失/非数字金额单独报告，不把不同币种相加。”如果没有要求去重，收款场景加`--keep-duplicates`，避免误删完全相同但真实发生的交易。
