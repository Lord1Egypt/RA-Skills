# insurance-product-deconstruction

保险产品标准化拆解技能，按照明亚保险经纪人的标准流程，将保险产品原始文件拆解为结构化 Markdown 文档，直接存入 Obsidian 保险产品库。

## 功能特性

- **本地证据提取**：从 PDF/Excel 自动提取产品数据
- **产品类型识别**：自动识别增额终身寿、养老年金、杠杆寿、快返年金、重疾险、医疗险
- **结构化输出**：8个标准化模块，包含产品基础信息、保障责任、现金价值分析等
- **质量检查**：多级检查机制，确保数据准确性
- **Obsidian 集成**：直接输出到 Obsidian 知识库

## 目录结构

```
insurance-product-deconstruction/
├── SKILL.md                    # 技能定义文件
├── config.json                 # 配置文件
├── requirements.txt            # Python 依赖
├── HANDOFF.md                  # 交接文档
├── scripts/
│   ├── product_evidence.py     # 主入口脚本
│   ├── generate_report.py      # 报告生成
│   ├── generate_report_input.py # 报告输入生成
│   ├── checks.py               # 检查脚本
│   ├── config.py               # 配置管理
│   └── evidence_pipeline/      # 证据提取管线
│       ├── cache.py            # 缓存管理
│       ├── calculations.py     # 计算逻辑
│       ├── inventory.py        # 文件分类
│       ├── pdf_extract.py      # PDF 提取
│       ├── search.py           # 证据检索
│       ├── validator.py        # 验证器
│       └── workbook_extract.py # Excel 提取
└── tests/                      # 测试文件
```

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/Lzquinn/insurance-product-deconstruction.git
cd insurance-product-deconstruction
```

### 2. 创建 Python 虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 可选：安装 OCR 支持

```bash
pip install rapidocr-onnxruntime
```

### 5. 配置

编辑 `config.json`，设置 Obsidian 输出路径：

```json
{
  "obsidian_output": "/path/to/your/obsidian/vault/02-长期知识库/保险/产品研究",
  "python_venv": "/path/to/your/venv",
  "ocr_tools_dir": ""
}
```

## 使用方法

### 基本用法

```bash
# 激活虚拟环境
source .venv/bin/activate

# 构建证据包
python scripts/product_evidence.py build "/path/to/product/files"

# 生成报告输入
python scripts/product_evidence.py report "/path/to/product/files"

# 生成 Markdown 报告
python scripts/generate_report.py "/path/to/product/files"

# 校验报告
python scripts/product_evidence.py validate "/path/to/product/files" --report "/path/to/report.md"
```

### 完整流程

```bash
PYTHON=scripts/product_evidence.py
PRODUCT_DIR="/path/to/product/files"

# Step 1: 构建证据包
python $PYTHON build "$PRODUCT_DIR"

# Step 2: 生成报告输入
python $PYTHON report "$PRODUCT_DIR"

# Step 3: 生成报告
python scripts/generate_report.py "$PRODUCT_DIR"

# Step 4: 校验
python $PYTHON validate "$PRODUCT_DIR" --report "$PRODUCT_DIR/report-draft.md"

# Step 5: 监工检查
python $PYTHON check "$PRODUCT_DIR" all
```

## 产品类型

支持以下产品类型的自动识别和拆解：

| 产品类型 | 核心关注点 |
|---------|-----------|
| 增额终身寿 | 现金价值增长率、回本年限、分红方式 |
| 养老年金 | 领取金额、领取方式、保证期限 |
| 杠杆寿 | 杠杆倍数、保障期限、健康告知 |
| 快返年金 | 回本速度、前期领取、灵活性 |
| 重疾险 | 病种数量、赔付比例、豁免责任 |
| 医疗险 | 保额、免赔额、报销比例、续保条件 |

## 输出结构

生成的 Markdown 文档包含 8 个标准化模块：

1. **产品基础信息** - 承保公司、投保年龄、缴费期间等
2. **核心保障责任拆解** - 按产品类型拆解的责任详情
3. **现金价值与收益分析** - IRR 计算、分红演示
4. **免责条款与重要提示** - 责任免除、健康告知
5. **投保规则与权益** - 减保、保单贷款等权益
6. **增值服务清单** - 重疾绿通、就医陪诊等
7. **优缺点与适合人群** - 产品分析
8. **对比模板预留字段** - YAML frontmatter

## 铁律

本技能遵循以下铁律（违反即出错）：

1. **禁止联网搜索** - 只使用用户提供的本地文件
2. **唯一信息源** - 只使用目录内的原始文件
3. **禁止外部知识** - 不使用模型记忆或行业惯例
4. **禁止非本地工具** - 只使用本地 Python 脚本
5. **资料包按完整处理** - 穷尽所有检索方式
6. **不得保留缺失占位词** - 不出现"未提供""未载明"等词
7. **违规检测** - 发现违规立即停止

## 依赖

- Python 3.8+
- pdfplumber (PDF 提取)
- pandas + openpyxl + xlrd (Excel 处理)
- Pillow (图像处理)
- RapidOCR (可选，OCR 支持)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request。

## 联系方式

- GitHub: [Lzquinn](https://github.com/Lzquinn)
