# recipe-manager - OpenClaw 原料配方库

商用原料配方管理工具，支持录入糖水、小料配方，自动计算成本，一键导出表格。

## 功能特性

- ✅ 录入配方（名称、原料克数、做法步骤）
- ✅ 多版本支持（芋圆 v1、芋圆 v2 等）
- ✅ 自动计算单份成本
- ✅ 调取标准配比
- ✅ 导出 CSV / Excel 表格

## 支持的配方类型

- 芋圆
- 珍珠
- 四果汤
- 福鼎肉片
- 自定义任意配方

## 安装方法

```bash
mkdir -p ~/.openclaw/skills/recipe-manager
cp -r * ~/.openclaw/skills/recipe-manager/
openclaw gateway restart
pip3 install pandas openpyxl  # 可选，用于导出 Excel
MIT
# openclaw-recipe-manager
