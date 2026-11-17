# Excel 业务分析工作台

[English](README.md)

合并 XLSX/CSV，按映射清洗、去重、核对销售退款和费用，生成分币种月报、对账表与来源明细。

## 功能

合并 XLSX/CSV，按映射清洗、去重、核对销售退款和费用，生成分币种月报、对账表与来源明细。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
合并我上传的三个月销售表，先核对列名和币种，列出重复及异常行。
```

```text
把销售和退款记录对应起来，按币种比较本月与上月净额，导出Excel。
```

```text
按我提供的字段映射清洗这些CSV，生成汇总表，并保留来源文件和行号。
```

输出 Excel、异常清单、来源行号和可复用映射。原表保留，币种分别汇总。公式检查会列出公式单元格；公式计算使用用户已有的表格应用。

## 运行要求

Python 3.10+, openpyxl 3.1+

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-sheet-studio
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-sheet-studio)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-sheet-studio
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-sheet-studio)。下载仓库 ZIP，将 `skills/mochi-sheet-studio` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
