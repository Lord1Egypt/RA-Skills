---
name: hcp-data-process
description: 从 HCP 仪器结果文件中提取汇总表。适用于用户提供的 HCP 类 Excel 文件，其中第一个 sheet 或原始文本包含 Sample、QC、Standards 等 Group 分段，并希望按样例格式生成新的汇总 sheet。
---

# HCP结果提取 

当 HCP 结果文件遵循 `hcp_dataextract/` 中样例的导出结构时，使用这个 skill。

## 功能说明

- 读取 `.xlsx` 工作簿，以及 UTF-16 制表符分隔的 `.xls` 导出文件。
- 从第一个 sheet 或原始导出文本中解析 `Group:` 分段。
- 提取 `Sample`、`MeanResult` 或 `Meanresult`、`CV%` 或 `CV`。
- 按样例布局生成新的汇总 sheet，起始位置为第 `C` 列、第 `4` 行。
- 仅对生成的汇总 sheet 设置背景色：分组行、表头行、分组后的空白行用浅蓝色，数据行用淡绿色。

## 使用命令

运行内置脚本：

```bash
python scripts/extract_hcp.py <input-path>
```

常用参数：

- `--output-dir <dir>`：将处理结果写入指定目录。
- `--sheet-name <name>`：指定生成的汇总 sheet 名称，默认是 `Sheet1`。
- `--overwrite`：若输出文件已存在则覆盖。

输入路径既可以是单个文件，也可以是目录。若传入目录，脚本会扫描其中的 `.xlsx`、`.xlsm`、`.xls` 文件。

## 输出行为

- 对 `.xlsx` 和 `.xlsm` 文件，脚本会复制原工作簿，替换或创建汇总 sheet，并另存为以 `_extracted.xlsx` 结尾的新文件。
- 对 UTF-16 文本形式的 `.xls` 导出文件，脚本会生成新的 `.xlsx` 工作簿，其中：
  - 第 1 个 sheet：导入后的原始数据
  - 第 2 个 sheet：提取后的汇总表
- 第一个 sheet 的原始数据不设置颜色，只有第二个 sheet 的汇总表会应用背景色。

## 说明

- 解析逻辑基于表头名称而不是固定列号，因此兼容 `MeanResult` / `Meanresult` 以及 `CV%` / `CV`。
- 会忽略空白续行，只提取每个样本的主记录行。
- 只有汇总 sheet 会设置样式，原始数据的第一个 sheet 不做颜色处理。
- 汇总 sheet 的样式与样例保持一致：分组行、表头行、分组后的空白行使用浅蓝色，数据行使用淡绿色。
