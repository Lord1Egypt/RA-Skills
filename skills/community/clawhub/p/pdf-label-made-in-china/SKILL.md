---
name: pdf-label-made-in-china
description: 在亚马逊FBA产品标签PDF中批量添加"Made In China"文字。适用于：用户上传标签PDF文件，需要在指定文字（如产品名称）下方的下一栏添加"Made In China"，并与条形码编号居中对齐，应用到所有页面。支持单类型标签和多类型混合标签（同一PDF中含有多种不同条形码的标签）。
---

# PDF Label - Made In China

## 核心工作流

### 第一步：查看PDF结构

使用 `file` 工具的 `view` 动作查看PDF第一页，确认：
- 指定文字（如 "Wooden"、"Relief"）的位置
- 条形码编号（如 `X004W8FC1T`）的位置
- 页面布局，判断 y_position 参数

### 第二步：确定 y_position 参数

y_position 是 "Made In China" 文字的 Y 坐标（从页面底部计算，单位：点）。

**参考值（适用于标准亚马逊标签，页面高度约 113pt）：**

| 目标位置 | y_position |
|---------|----------|
| 产品描述下方（常规） | 27 |
| 稍高一点 | 30~35 |

若用户要求"先生成一页检查"，先用 `--test-page` 生成测试页，确认后再全量处理。

### 第三步：运行脚本

**单类型标签（所有页面条形码相同）：**

```bash
sudo pip3 install PyPDF2 -q
python3.11 /home/ubuntu/skills/pdf-label-made-in-china/scripts/add_made_in_china.py \
  <input.pdf> <output.pdf> \
  --barcode <条形码> \
  --y-position <Y坐标>
```

**多类型标签（同一PDF含多种条形码）：**

```bash
python3.11 /home/ubuntu/skills/pdf-label-made-in-china/scripts/add_made_in_china.py \
  <input.pdf> <output.pdf> \
  --multi '[{"barcode":"X004W8IKFT","y_position":27},{"barcode":"X004W8V9YX","y_position":27}]'
```

**仅生成第一页测试：**

在命令末尾加 `--test-page`

### 第四步：验证并交付

查看输出PDF的第一页和最后一页，确认文字位置正确后，将文件发送给用户。

---

## 常见场景

### 场景1：单类型标签，直接全量处理

用户说"全部应用"时，直接运行全量脚本，无需测试页。

### 场景2：用户要求先检查

加 `--test-page` 生成单页预览，用户确认后去掉该参数重新运行。

### 场景3：位置需要调整

用户说"太靠下"→ 增大 y_position；用户说"太靠上"→ 减小 y_position。每次调整约 3~5pt。

### 场景4：FBA仓储标签（Mixed SKUs）

FBA标签（如 `FBA195G77SD2-xxx.pdf`）格式不同，"Made In China" 需放在：
- FBA编号（如 `FBA195G77SD2U000001`）下方黑色线下面，与FBA编号居中对齐
- 或与 "Mixed SKUs" 文字同一行的左侧

这类标签页面尺寸通常更大（约 612×792pt），y_position 约为 165。

---

## 注意事项

- 始终先用 `sudo pip3 install PyPDF2 -q` 确保依赖已安装
- 输出文件命名建议：`原文件名_modified.pdf`
- 多类型PDF：脚本自动通过条形码识别每页类型，无需手动分页
- 字体默认 Helvetica 8号，FBA标签可用 11号（`--font-size 11`）
