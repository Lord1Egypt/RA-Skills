# OFD 文件结构详解

## 概述

OFD（Open Fixed-layout Document）是中国的电子文档格式标准，类似于 PDF。它是一种基于 XML 的矢量文档格式。

## 文件结构

OFD 文件本质上是 ZIP 压缩包，包含以下核心文件：

```
example.ofd/
├── OFD.xml                    # 主入口文件
├── Doc_0/
│   ├── Document.xml           # 文档结构定义
│   ├── DocumentRes.xml        # 文档资源索引
│   ├── PublicRes.xml          # 公共资源
│   ├── Pages/
│   │   └── Page_0/
│   │       └── Content.xml    # 页面内容（包含文字和图形）
│   ├── Res/
│   │   ├── image_*.png        # 图片资源
│   │   └── font_*.ttf         # 字体资源
│   ├── Tpls/                  # 模板
│   └── Tags/                  # 标签（结构化信息）
└── ...
```

## 核心 XML 文件说明

### 1. OFD.xml（主入口）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ofd:OFD xmlns:ofd="http://www.ofdspec.org/2016">
    <ofd:DocBody>
        <ofd:DocInfo>...</ofd:DocInfo>
        <ofd:DocRoot>Doc_0/Document.xml</ofd:DocRoot>
    </ofd:DocBody>
</ofd:OFD>
```

### 2. Content.xml（页面内容）

页面内容是文本提取的主要来源。结构如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ofd:Page xmlns:ofd="http://www.ofdspec.org/2016">
    <ofd:Area>
        <ofd:PhysicalBox>0 0 210 180</ofd:PhysicalBox>
        <!-- 页面尺寸：宽度210mm, 高度180mm -->
    </ofd:Area>
    <ofd:Content>
        <ofd:Layer ID="1">
            <!-- 文本对象 -->
            <ofd:TextObject ID="100" Boundary="10 10 50 5" Font="Font1" Size="3.5">
                <ofd:TextCode X="0" Y="3">Hello World</ofd:TextCode>
            </ofd:TextObject>

            <!-- 图片对象 -->
            <ofd:ImageObject ID="101" CTM="..." ResourceID="img1"/>

            <!-- 路径对象 -->
            <ofd:PathObject ID="102" Boundary="...">...</ofd:PathObject>
        </ofd:Layer>
    </ofd:Content>
</ofd:Page>
```

## 文字位置信息

### TextObject 属性

| 属性 | 说明 | 示例 |
|---|---|---|
| `ID` | 对象唯一标识 | `100` |
| `Boundary` | 边界框 (X, Y, Width, Height) | `"10 10 50 5"` |
| `Font` | 字体资源ID | `"6993"` |
| `Size` | 字体大小 (pt) | `"3.175"` |

### TextCode 属性

| 属性 | 说明 | 示例 |
|---|---|---|
| `X` | 文字起始X坐标 | `"0"` |
| `Y` | 文字Y坐标（基线位置） | `"3"` |
| `DeltaX` | 字符间距数组 | `"3.175 3.175..."` |

### 坐标系统

- **单位**：毫米（mm）
- **原点**：页面左下角
- **Y轴向上**：OFD 坐标系统 Y 轴向上增长

```
(0, 页面高度)
     ↑
     |    ┌─────────────┐
     |    │   Page      │
     |    │             │
     |    │  Text here  │  ← Y 从底部计算
     |    │             │
     |    └─────────────┘
     └──────────────────→ (页面宽度, 0)
```

## 文本提取注意事项

1. **多行文本**：同一行文字可能被拆分成多个 TextObject，需根据 Y 坐标分组

2. **字体映射**：字体名称在 Res 目录中定义，需要通过 ResourceID 查找

3. **文字方向**：默认从左到右，部分语言可能不同

4. **图片OCR**：图片对象需要通过 OCR 提取文本，不在本技能范围内

5. **矢量图形**：PathObject 通常是边框或装饰，不是文本

## 扩展参考

- OFD 规范文档：http://www.ofdspec.org/
- 国家标准：GB/T 33190-2016
