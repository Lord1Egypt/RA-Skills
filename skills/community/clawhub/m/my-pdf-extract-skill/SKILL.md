# PDF数据提取技能

## 描述
从PDF文件中智能提取商品标签数据（商品编码、商品名称、商品批次、商品数量），并输出到Excel文件。

## 使用场景
- 从PDF文件中提取结构化数据
- 处理包含跨行文本的商品名称
- 将提取的数据保存为Excel格式
- 需要精确匹配商品编码和名称的场景

## 核心功能
1. **智能提取**：自动识别PDF中的数据块
2. **跨行处理**：正确处理跨越多行的商品名称
3. **精确匹配**：基于预定义的名称列表进行精确匹配
4. **数据验证**：验证提取结果的准确性

## 使用方法

### 基本用法
```bash
# 激活虚拟环境
source ../venv/bin/activate

# 运行提取脚本
python extract_exact.py
```

### 脚本说明
- `extract_exact.py`：主提取脚本
- 输入：`Lisa-3.pdf`
- 输出：`Lisa-3_精确提取.xlsx`

## 文件结构
```
my-pdf-extract-skill/
├── SKILL.md              # 本文件
├── references/
│   └── 完整标签数据.png  # 参考图片
├── scripts/
│   └── extract_exact.py  # 提取脚本
└── README.md             # 使用说明
```

## 依赖
- Python 3.8+
- pdfplumber
- pandas
- openpyxl

## 安装依赖
```bash
pip install pdfplumber pandas openpyxl
```

## 配置
在脚本中修改以下变量：
```python
pdf_path = "./Lisa-3.pdf"          # PDF文件路径
output_path = "./Lisa-3_精确提取.xlsx"  # 输出文件路径
```

## 示例
```python
# 提取数据
labels = extract_exact_data(pdf_path)

# 保存到Excel
df = pd.DataFrame(labels)
df.to_excel(output_path, index=False)
```

## 注意事项
1. PDF文件必须是文本可提取的（非扫描件）
2. 商品名称列表需要根据实际情况调整
3. 跨行名称需要手动合并处理
4. 建议先测试小批量数据

## 故障排除
- **问题**：提取的商品数量不正确
  **解决**：检查PDF中的CODIGO行格式
- **问题**：商品名称不完整
  **解决**：调整名称分割逻辑
- **问题**：Excel文件无法打开
  **解决**：检查openpyxl安装和文件权限

## 扩展
要适配其他PDF格式，可以：
1. 修改`extract_exact_data`函数中的正则表达式
2. 更新`get_exact_names`函数中的名称列表
3. 调整数据块识别逻辑

## 作者
[你的名字]

## 版本
v1.0.0