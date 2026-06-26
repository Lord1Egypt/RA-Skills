# PDF数据提取Skill

这是一个用于从PDF文件中提取商品标签数据的OpenClaw技能。

## 功能特点
- ✅ 智能识别PDF中的数据块
- ✅ 处理跨行商品名称
- ✅ 精确匹配商品编码和名称
- ✅ 输出为Excel格式
- ✅ 数据验证和统计

## 快速开始

### 1. 安装依赖
```bash
pip install pdfplumber pandas openpyxl
```

### 2. 准备PDF文件
将PDF文件放在工作目录中，命名为`Lisa-3.pdf`

### 3. 运行提取
```bash
python scripts/extract_exact.py
```

### 4. 查看结果
提取结果将保存为`Lisa-3_精确提取.xlsx`

## 文件说明

### 核心文件
- `SKILL.md` - 技能描述和指令
- `scripts/extract_exact.py` - 主提取脚本
- `references/完整标签数据.png` - 参考数据结构

### 输出文件
- `Lisa-3_精确提取.xlsx` - 提取结果

## 配置

### 修改PDF路径
编辑`scripts/extract_exact.py`：
```python
pdf_path = "./你的PDF文件.pdf"
```

### 修改输出路径
```python
output_path = "./输出文件.xlsx"
```

## 自定义

### 添加新的商品名称
在`get_exact_names`函数中添加新的名称列表：
```python
if block_idx == 1:
    names = [
        "商品名称1",
        "商品名称2",
        # ...
    ]
```

### 调整提取逻辑
修改`extract_exact_data`函数中的正则表达式和数据块识别逻辑。

## 示例数据

### 输入PDF结构
```
行1: CODIGO：1002-03 CODIGO：2013-08 ...
行2: ANILLOS B150 STD BARRA DE POSAPIES ...
行3: CON GOMAS NEW HORSE/EK BASE AUXILIAR ...
行4: P9 260305005 P9 260305005 ...
行5: 500 100 400 ...
```

### 输出Excel结构
| 商品编码 | 商品名称 | 商品批次 | 商品数量 |
|----------|----------|----------|----------|
| 1002-03 | ANILLOS B150 STD | P9 260305005 | 500 |
| 2013-08 | BARRA DE POSAPIES CON GOMAS NEW HORSE/EK | P9 260305005 | 100 |

## 支持
如有问题，请参考：
1. [pdfplumber文档](https://github.com/jsvine/pdfplumber)
2. [pandas文档](https://pandas.pydata.org/)
3. [OpenClaw技能开发指南](https://docs.openclaw.ai/skills)