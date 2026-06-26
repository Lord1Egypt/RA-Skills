---
name: p-e
version: 1.0.0
description: |
  极速图片提取工具。发送模板图片+多张实际图片，秒懂格式，一步到位生成 Excel 表格。无需确认，直接输出。
  触发方式：/p-e、/pe、「图片提取」「提取Excel」「picture extract」
  Picture Extract: send template + data images, instantly generate Excel with embedded images.
metadata:
  openclaw:
    emoji: "📊"
    os: ["darwin", "linux"]
    requires:
      bins: ["python3"]
    user-invocable: true
---

# P-E: 图片批量提取 → Excel 表格

## 概述

从相同格式的图片中提取数据，自动生成带嵌入图片的 Excel 表格。零交互，一步完成。

## 触发条件

当用户发送以下内容时触发：
- 模板图片 + 多张实际数据图片
- 说「图片提取」「提取Excel」「picture extract」
- 使用 `/p-e` 或 `/pe`

## 工作流程

### 第 0 步：依赖检查（仅首次）

用 `exec` 工具运行：

```bash
python3 -c "import openpyxl; import PIL" 2>/dev/null || pip3 install --user openpyxl Pillow
```

如果失败，告知用户运行：`bash ~/.agents/skills/p-e/scripts/setup.sh`

### 第 1 步：分析模板图片

用你的视觉能力分析用户发送的第一张（模板）图片：
1. 识别所有字段的位置和格式
2. 理解数据的排版规律
3. 推断字段名称和数据类型
4. 建立字段-位置的映射关系

### 第 2 步：提取所有图片数据

逐张分析实际数据图片，提取每张图片中的结构化数据。

同时，将用户发送的每张图片保存到临时目录，用于后续嵌入 Excel：

```bash
# 用 exec 工具创建临时目录
mkdir -p /tmp/p-e-images
```

如果图片已经在本地文件系统上（用户给了路径），直接使用该路径。
如果图片是通过聊天发送的，用 `write` 工具将图片保存到 `/tmp/p-e-images/`。

### 第 3 步：生成 JSON 数据文件

将提取的数据组织为 JSON 格式，用 `write` 工具写入临时文件：

```json
{
  "fields": ["编号", "产品描述", "装箱数", "单价", "尺寸", "图片"],
  "data": [
    {
      "编号": "3-4",
      "产品描述": "手掌最后的晚餐",
      "装箱数": 24,
      "单价": 25,
      "尺寸": "17×24",
      "图片": "/tmp/p-e-images/img1.jpg"
    }
  ]
}
```

**重要规则：**
- 最后一个字段必须命名为「图片」「image」或「图」
- 图片字段的值必须是图片文件的绝对路径
- 数字类型（价格、数量）使用数字而非字符串
- 无法识别的字段标记为 `[待确认]`

用 `write` 工具将 JSON 写入 `/tmp/p-e-data.json`。

### 第 4 步：运行 Excel 生成脚本

用 `exec` 工具运行：

```bash
python3 ~/.agents/skills/p-e/scripts/generate_excel.py \
  --json /tmp/p-e-data.json \
  --output ~/Desktop/product_list.xlsx
```

如果用户指定了输出路径，使用用户指定的路径。默认输出到桌面。

### 第 5 步：清理临时文件

```bash
rm -f /tmp/p-e-data.json
```

保留 `/tmp/p-e-images/` 中的图片（Excel 生成后不再需要，但用户可能想保留）。

### 第 6 步：报告结果

输出格式：

```
✓ 已识别 N 张图片

✓ 已生成 product_list.xlsx

数据统计：
- N 行数据
- M 列字段（字段1|字段2|...|图片）
- 所有图片自动嵌入到最后一列
- 完毕！
```

## Excel 输出规格

| 属性 | 值 |
|------|-----|
| 文件名 | `product_list.xlsx`（默认） |
| 表头样式 | 蓝色背景 (#4472C4)，白色粗体字 |
| 数据列宽 | 15 |
| 图片列宽 | 55 |
| 行高 | 190 |
| 图片尺寸 | 320×240px，原图直接嵌入不压缩 |
| 边框 | 所有单元格细边框 |

## 异常处理

| 情况 | 处理方式 |
|------|---------|
| 字段不清晰或缺失 | 标记为 `[待确认]` |
| 一张图有多条数据 | 自动拆分为多行 |
| 信息缺失 | 该单元格留空 |
| 图片文件不存在 | 显示 `[File not found]` |
| Python 依赖缺失 | 自动安装或提示运行 setup.sh |

## 使用示例

用户发送：
```
【模板】
[鞋子信息表照片]

【实际数据】
[鞋1] [鞋2] [鞋3] [鞋4]
```

或者指定文件夹：
```
/path/to/images 帮我把这些图片整理出表格
```
