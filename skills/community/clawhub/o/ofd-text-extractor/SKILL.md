---
name: ofd-text-extractor
description: >
  本技能用于从 OFD 格式文件中提取文本内容，并保留位置信息。
  触发场景包括：分析 OFD 发票内容、从 OFD 文件中提取特定位置的信息、
  或需要了解 OFD 文件的详细结构时使用。
---

# OFD 文本提取专家

## 功能概述

本技能提供 OFD（Open Fixed-layout Document）格式文件的文本提取能力，输出包含精确位置信息的结构化数据。

**新增功能：**
- ✅ 模板页提取（类似 PDF 中的 Form）
- ✅ 字符级位置计算（每个字符的精确坐标）
- ✅ 支持 DeltaX 字符间距

## 何时使用

当用户需要以下操作时触发本技能：

- 从 OFD 文件中提取文本内容
- 获取文字在 OFD 页面中的位置坐标
- 分析 OFD 文件的内部结构
- 批量提取 OFD 文件的文本信息
- 需要字符级精度的文本位置

## OFD 文件结构

OFD 本质上是 ZIP 压缩包，解压后包含以下核心文件：

| 文件/目录 | 说明 |
|---|---|
| `OFD.xml` | 主入口文件，定义文档基本结构 |
| `Doc_0/Document.xml` | 文档结构定义，包含模板页映射 |
| `Doc_0/Pages/Page_X/Content.xml` | 页面内容，包含文字和位置信息 |
| `Doc_0/Tpls/Tpl_X/Content.xml` | 模板页内容（如发票表头） |
| `Doc_0/Res/` | 资源文件（图片、字体等） |

## 文字位置信息格式

在 `Content.xml` 中，每个 `TextObject` 包含：

```xml
<ofd:TextObject ID="6956" Boundary="28.8287 6.087 28.7 19.8488" Font="6993" Size="3.175">
    <ofd:TextCode X="4.825" Y="11.0658" DeltaX="3.175 3.175 3.175 3.175 3.175">旅客运输服务</ofd:TextCode>
</ofd:TextObject>
```

| 属性 | 说明 |
|---|---|
| `Boundary` | 边界框：X Y Width Height（单位：mm） |
| `X, Y` | 文字起始坐标（单位：mm） |
| `DeltaX` | 字符间距数组，用于计算每个字符的位置 |
| `TextCode` 内容 | 实际文本内容 |

### 字符位置计算

字符位置计算公式：
- 第 0 个字符：X = TextCode.X
- 第 n 个字符：X = TextCode.X + DeltaX[0] + DeltaX[1] + ... + DeltaX[n-1]

示例：`旅客运输服务`
- 旅 @ X=4.825
- 客 @ X=4.825 + 3.175 = 8.0
- 运 @ X=8.0 + 3.175 = 11.175
- ...

## 使用方法

### 快速提取

```powershell
# 基本提取
.\scripts\extract_ofd.ps1 -OfdFile "发票.ofd"

# 提取并显示字符位置
.\scripts\extract_ofd.ps1 -OfdFile "发票.ofd" -ShowCharacters

# 导出到 JSON
.\scripts\extract_ofd.ps1 -OfdFile "发票.ofd" -OutputFile "result.json" -ShowCharacters
```

### 输出格式

```json
{
  "file": "发票.ofd",
  "pages": [
    {
      "pageIndex": 0,
      "pageSize": { "width": 210, "height": 180 },
      "usedTemplates": ["1"],
      "texts": [
        {
          "id": "page_0",
          "objectId": "6956",
          "text": "旅客运输服务",
          "x": 4.825,
          "y": 11.0658,
          "boundary": {
            "x": 28.8287,
            "y": 6.087,
            "width": 28.7,
            "height": 19.8488
          },
          "source": "page",
          "isTemplate": false,
          "characters": [
            { "char": "旅", "x": 4.825, "y": 11.0658, "index": 0 },
            { "char": "客", "x": 8.0, "y": 11.0658, "index": 1 },
            { "char": "运", "x": 11.175, "y": 11.0658, "index": 2 },
            { "char": "输", "x": 14.35, "y": 11.0658, "index": 3 },
            { "char": "服", "x": 17.525, "y": 11.0658, "index": 4 },
            { "char": "务", "x": 20.7, "y": 11.0658, "index": 5 }
          ]
        }
      ]
    }
  ]
}
```

### 字段说明

| 字段 | 说明 |
|---|---|
| `text` | 完整文本内容 |
| `x, y` | 文本起始坐标（mm） |
| `boundary` | 文本对象边界框 |
| `source` | 来源：`page` 或 `template_X` |
| `isTemplate` | 是否来自模板页 |
| `characters` | 字符级位置数组（使用 `-ShowCharacters` 时包含） |

## 模板页支持

OFD 发票通常使用模板页来定义固定的表头（如"出行人"、"出发地"等标签）。

脚本会自动：
1. 解析 `Document.xml` 找到模板页映射
2. 加载 `Tpls/Tpl_X/Content.xml` 中的模板内容
3. 合并页面内容和模板页内容
4. 通过 `isTemplate` 字段区分来源

## 执行脚本

技能使用 `scripts/extract_ofd.py` 脚本进行提取（推荐 Python 版本，跨平台兼容）：

```powershell
# 基本用法
python scripts/extract_ofd.py <ofd文件路径>

# 显示字符位置
python scripts/extract_ofd.py <ofd文件路径> --show-chars

# 导出 JSON
python scripts/extract_ofd.py <ofd文件路径> --output <输出路径> --show-chars
```

参数说明：
- `<ofd文件路径>`: OFD 文件路径（必需）
- `--output <输出路径>`: JSON 输出文件路径（可选）
- `--show-chars`: 显示/包含字符级位置（可选）

## 注意事项

- OFD 是矢量格式，坐标单位为毫米（mm）
- 同一行的文字可能有多个 TextObject，需根据 Y 坐标判断
- 图片和路径对象不会被提取为文本
- 模板页内容通过 `isTemplate: true` 标记
- 字符位置需要 `-ShowCharacters` 参数才会包含在输出中
