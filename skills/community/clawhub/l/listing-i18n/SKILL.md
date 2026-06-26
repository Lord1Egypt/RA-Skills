---
name: listing-i18n
description: 在 OpenClaw 中把中文产品 Excel 或 CSV 本地化为 Amazon 和 Shopify 的多语言 Listing。适用于翻译产品、跨境电商 Listing 本地化、Amazon listing、Shopify listing、localize products 等场景。
version: 0.2.0
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      bins: ["python3"]
---

# Listing I18n

这个 skill 运行在 OpenClaw 上：

- 翻译和本地化改写由 OpenClaw 当前会话中的 LLM 完成
- 模板生成、输入检查、Excel 输出、结果校验由本地 Python 脚本完成

不要把这个 skill 当成独立翻译程序。它是“LLM 工作流 + 本地辅助脚本”的组合。

## 可用脚本

- `python3 generate_template.py [output.xlsx]`
  生成输入模板
- `python3 inspect_input.py <input.xlsx|csv> [--sheet SheetName]`
  检查输入文件结构，列出字段和样例数据
- `python3 build_output.py <translations.json> [output.xlsx]`
  按约定 JSON 结构生成最终 Excel
- `python3 validate.py <output.xlsx>`
  校验输出文件是否满足平台限制

## 工作流

### 1. 用户没有产品文件

运行：

```bash
python3 generate_template.py
```

告诉用户填写 `Products` sheet 第 3 行起的数据，再继续。

### 2. 用户提供了产品文件

先运行：

```bash
python3 inspect_input.py <input_file>
```

基于脚本输出完成三件事：

1. 告诉用户检测到的列名和前 3 行样例
2. 确认以下字段映射
3. 如果缺少必填字段，要求用户补齐

必填字段：

- `product_id`
- `brand`
- `product_name`
- `category`
- `specs`
- `selling_points`
- `keywords_cn`
- `package_includes`

可选字段：

- `custom_attributes`
- `images_note`

### 3. 确认平台和目标市场

如果用户没有特别说明：

- 平台默认 `Both`
- 目标市场默认 `en_US`

支持的目标市场：

- `en_US`
- `en_UK`
- `de_DE`
- `ja_JP`
- `es_ES`
- `fr_FR`
- `it_IT`

### 4. 由 LLM 执行逐产品翻译

对每个产品、每个目标市场、每个平台分别生成内容。

#### Amazon

- `title`
  最长 200 chars，建议不超过 150
- `bullet_point_1` 到 `bullet_point_5`
  共 5 条，每条建议 150-250 chars
- `description`
  建议 150-300 词
- `backend_keywords`
  最长 249 bytes，小写、空格分隔、不含品牌名

#### Shopify

- `title`
  最长 100 chars
- `description_html`
  建议 100-400 词，只用基础 HTML 标签
- `seo_title`
  最长 70 chars
- `seo_description`
  最长 320 chars
- `tags`
  8-15 个，逗号分隔，小写
- `product_type`
  英文品类路径，用 `>` 分隔

翻译要求：

- 不是直译，要做目标市场本地化
- Amazon 偏搜索导向，Shopify 偏品牌叙事
- 避免绝对化营销词，如 `best`、`#1`、`guaranteed`
- `custom_attributes` 的 key 保持英文，value 翻译成目标语言
- 美国站优先使用美式计量单位；英国、德国、日本按本地习惯表达

### 5. 生成输出文件

先把翻译结果组织成 JSON，再运行：

```bash
python3 build_output.py <translations.json> [output.xlsx]
```

输出 workbook 需包含：

- `Amazon_<lang>` sheet
- `Shopify_<lang>` sheet
- `Source_CN` sheet

Amazon sheet 列顺序必须是：

```text
product_id
brand
title
bullet_point_1
bullet_point_2
bullet_point_3
bullet_point_4
bullet_point_5
description
backend_keywords
custom_attributes
source_product_name
```

Shopify sheet 列顺序必须是：

```text
product_id
brand
title
description_html
seo_title
seo_description
tags
product_type
custom_attributes
source_product_name
```

### 6. 校验并汇报

生成 Excel 后运行：

```bash
python3 validate.py <output.xlsx>
```

向用户汇报：

- 处理了多少个产品
- 生成了哪些平台和语言版本
- 输出文件路径
- 校验结果中有哪些 `error` 和 `warning`

## `translations.json` 结构

`build_output.py` 读取如下结构。仓库里还提供了可直接参考的 [translations.example.json](/Users/zcq/beansmile/haixia/i18n-listing-skill-code/translations.example.json)：

```json
{
  "sheets": [
    {
      "name": "Amazon_en_US",
      "headers": [
        "product_id",
        "brand",
        "title",
        "bullet_point_1",
        "bullet_point_2",
        "bullet_point_3",
        "bullet_point_4",
        "bullet_point_5",
        "description",
        "backend_keywords",
        "custom_attributes",
        "source_product_name"
      ],
      "rows": [
        [
          "SP-001",
          "SoundPulse",
          "SoundPulse Noise Cancelling Earbuds",
          "【NOISE CANCELLATION】...",
          "【HI-RES AUDIO】...",
          "【ALL-DAY COMFORT】...",
          "【SWEAT RESISTANCE】...",
          "【IN THE BOX】...",
          "Long description...",
          "wireless earbuds bluetooth earbuds sports earbuds",
          "color:black | connectivity:bluetooth 5.3",
          "SP-Pro 主动降噪真无线蓝牙耳机"
        ]
      ]
    },
    {
      "name": "Source_CN",
      "headers": ["product_id", "brand", "product_name"],
      "rows": [["SP-001", "SoundPulse", "SP-Pro 主动降噪真无线蓝牙耳机"]]
    }
  ]
}
```

## 注意

- 依赖：`python3` 和 `openpyxl`
- 建议每批不超过 20 个产品
- 日语和德语输出建议母语者最终复核
