---
name: png-lsb-skills
description: PNG图片LSB隐写分析、块信息解析与CRC校验工具，支持提取sRGB/gAMA/pHYs元数据并检测多种LSB隐藏模式；适合CTF比赛场景，当用户需要分析PNG图片结构、验证数据完整性、检测隐写信息或提取图像元数据时使用
dependency:
  python:
    - Pillow>=9.0.0
---

# PNG图片LSB隐写分析技能

## 任务目标
- 本Skill用于：深度分析PNG图片的内部结构与隐写信息
- 能力包含：
  - PNG签名验证
  - 块信息解析(IHDR/IDAT/IEND等所有chunk)
  - CRC校验(验证数据完整性)
  - 元数据提取(sRGB/gAMA/pHYs等)
  - LSB隐写分析(15种模式解码)
- 触发条件：用户上传PNG图片并询问图片结构、隐写信息、数据完整性或元数据时

## 前置准备
- 依赖说明：scripts脚本所需的依赖包及版本
  ```
  Pillow>=9.0.0
  ```

## 操作步骤

### 步骤1：调用脚本分析PNG图片
使用以下命令分析PNG图片：
```bash
python scripts/png_analyzer.py --png <图片路径> [--output <输出JSON路径>]
```

参数说明：
- `--png`：PNG图片路径（必需）
- `--output`：输出JSON文件路径（可选，不指定则直接打印结果）

### 步骤2：查看分析结果
脚本将返回以下信息：

**PNG签名验证**
- 验证文件是否为有效的PNG格式

**块信息解析**
- 遍历所有chunk，提取类型、长度、数据
- 对每个chunk进行CRC校验，标记校验结果

**元数据提取**
- sRGB：色彩空间信息
- gAMA：Gamma值
- pHYs：DPI分辨率信息

**LSB隐写分析**
- 提取前8行的最低有效位(LSB)
- 按15种模式组合并尝试解码为ASCII字符
- 详见 [references/lsb_patterns.md](references/lsb_patterns.md)

### 步骤3：判断隐写信息
根据LSB分析结果判断：
- 如果某个模式的解码结果中出现可读文本，可能存在隐写信息
- 重点关注连续的可打印字符(ASCII 32-126)
- 不同模式对应不同的隐写算法

## 资源索引
- 必要脚本：见 [scripts/png_analyzer.py](scripts/png_analyzer.py)（用途：PNG图片分析，参数：--png图片路径 --output输出路径）
- 领域参考：见 [references/lsb_patterns.md](references/lsb_patterns.md)（何时读取：理解LSB隐写模式与解码方法时）

## 注意事项
- 仅支持PNG格式，其他格式会报错
- LSB分析默认提取前8行，适合常见隐写分析场景
- CRC校验失败可能表示文件损坏或被篡改
- 部分PNG图片可能不包含sRGB/gAMA/pHYs等元数据
- LSB解码结果需要人工判断是否为有意义的信息

## 使用示例

**示例1：分析PNG图片结构**
```bash
python scripts/png_analyzer.py --png ./image.png
```

**示例2：保存分析结果到JSON**
```bash
python scripts/png_analyzer.py --png ./image.png --output ./result.json
```

**示例3：检测隐写信息**
用户上传PNG图片后，调用脚本分析，重点关注LSB分析部分的chars字段，查找可读文本。
