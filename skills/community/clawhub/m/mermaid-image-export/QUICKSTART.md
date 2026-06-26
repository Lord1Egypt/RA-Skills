# Mermaid Image Export 快速开始

## 📍 安装位置
```
/root/.openclaw/skills/mermaid-image-export
```

## 🚀 快速测试

### 1. 检查安装
```bash
cd /root/.openclaw/skills/mermaid-image-export
python scripts/install_mermaid_cli.py --check
```

### 2. 创建测试图表
```bash
cat > test.mmd << 'EOF'
graph TD
    A[开始] --> B{安装检查}
    B -->|通过| C[测试导出]
    B -->|失败| D[安装依赖]
    C --> E[成功]
    D --> E
    
    style A fill:#c8e6c9
    style E fill:#c8e6c9
EOF
```

### 3. 导出图表
```bash
# PNG格式
python scripts/export_mermaid_image.py test.mmd -o test.png

# SVG格式
python scripts/export_mermaid_image.py test.mmd -f svg -o test.svg

# PDF格式  
python scripts/export_mermaid_image.py test.mmd -f pdf -o test.pdf
```

### 4. 批量导出
```bash
# 导出目录中所有.mmd文件
python scripts/export_mermaid_image.py *.mmd -d exports/

# 使用shell脚本
./scripts/batch_export.sh -f svg -t dark -d svg_exports *.mmd
```

## 📂 技能结构

```
mermaid-image-export/
├── SKILL.md                    # 技能主文档
├── package.json               # 元数据
├── README.md                  # 详细说明
├── scripts/                   # 核心脚本
│   ├── export_mermaid_image.py  # 主导出脚本
│   ├── install_mermaid_cli.py   # 安装检查
│   └── batch_export.sh          # 批量导出
├── references/                # 完整文档
│   ├── overview.md           # 概述
│   ├── installation.md       # 安装指南
│   ├── usage.md             # 使用指南
│   ├── formats.md           # 格式说明
│   └── troubleshooting.md   # 问题排查
└── assets/examples/         # 示例文件
    ├── export_example.mmd   # Mermaid示例
    └── config_example.json  # 配置示例
```

## 🔧 核心脚本说明

### `export_mermaid_image.py`
主要导出脚本，支持：
- 单个文件导出
- 批量导出
- PNG/SVG/PDF格式
- 主题选择 (-t)
- 分辨率控制 (-s)
- 背景颜色 (-b)

### `install_mermaid_cli.py`
安装检查脚本：
- 检查Node.js/npm
- 检查mermaid-cli
- 检查Chrome/Chromium
- 提供安装指导

### `batch_export.sh`
批量导出包装器：
- 支持通配符
- 进度显示
- 错误处理
- 并行处理控制

## 📚 完整文档

查看 `references/` 目录获取详细信息：
1. `overview.md` - 技能架构和用例
2. `installation.md` - 各平台安装指南
3. `usage.md` - 完整命令参考
4. `formats.md` - PNG/SVG/PDF详细规格
5. `troubleshooting.md` - 问题排查指南

## 🎨 示例用法

### 高质量导出
```bash
python scripts/export_mermaid_image.py diagram.mmd -s 2.0 -t forest -o highres.png
```

### 暗色主题导出
```bash
python scripts/export_mermaid_image.py diagram.mmd -t dark -b "#1a1a1a" -o dark.png
```

### 文档生成流水线
```bash
# 导出所有文档图表
find docs/ -name "*.mmd" -exec python scripts/export_mermaid_image.py {} -d docs/images/ \;
```

## ⚡ 与Termaid配合使用

**开发工作流**:
1. 使用 `termaid` 快速预览和调试
2. 使用 `mermaid-image-export` 生成最终图片

```bash
# 1. 使用termaid预览
python /path/to/termaid/scripts/render_mermaid.py diagram.mmd

# 2. 使用mermaid-cli导出
python scripts/export_mermaid_image.py diagram.mmd -o diagram.png
```

## 📞 支持

- **安装问题**: 查看 `references/installation.md`
- **使用问题**: 查看 `references/usage.md`
- **故障排除**: 查看 `references/troubleshooting.md`
- **格式问题**: 查看 `references/formats.md`

---

**安装完成！现在可以开始导出高质量的Mermaid图表了！** 🎉