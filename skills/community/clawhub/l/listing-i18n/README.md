# listing-i18n

一个运行在 OpenClaw 上的电商 Listing 本地化 skill，用于把中文产品资料整理成 Amazon / Shopify 多语言输出。

它不是独立翻译程序。实际工作方式是：

- OpenClaw 的 LLM 负责翻译和本地化改写
- 本仓库脚本负责模板生成、输入检查、输出落盘、结果校验

## 当前能力

- 生成标准输入模板
- 检查 Excel / CSV 输入结构
- 按约定 JSON 生成最终 Excel
- 校验 Amazon / Shopify 输出限制

## 文件说明

- `SKILL.md`
  OpenClaw skill 主说明
- `generate_template.py`
  生成输入模板
- `inspect_input.py`
  检查输入文件并给出字段映射建议
- `build_output.py`
  根据 `translations.json` 生成最终 workbook
- `validate.py`
  校验输出 workbook
- `product_template.xlsx`
  预生成模板
- `translations.example.json`
  更贴近 OpenClaw 对话产物的示例输入，可直接喂给 `build_output.py`

## 基本用法

### 1. 生成模板

```bash
python3 generate_template.py
```

### 2. 检查输入文件

```bash
python3 inspect_input.py products.xlsx
python3 inspect_input.py products.xlsx --sheet Products
python3 inspect_input.py products.csv
```

### 3. 生成输出文件

```bash
cp translations.example.json translations.json
python3 build_output.py translations.json products_listing_i18n.xlsx
```

### 4. 校验输出文件

```bash
python3 validate.py products_listing_i18n.xlsx
```

## 依赖

- Python 3
- openpyxl

安装：

```bash
python3 -m pip install openpyxl
```
