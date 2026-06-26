# 解码base64图片
echo "🖼️  解码测试图片..."
base64 -d test_images/sample.jpg.base64 > test_images/sample.jpg
rm test_images/sample.jpg.base64

# 创建配置文件
echo "⚙️  创建配置文件..."
cat > config/styles.json << 'EOF'
{
  "styles": {
    "title": "标题",
    "heading1": "标题 1",
    "heading2": "标题 2",
    "heading3": "标题 3",
    "paragraph": "正文",
    "code": "代码",
    "quote": "引用",
    "table": "表格",
    "image": "图片标题"
  },
  "font": {
    "title": {
      "name": "微软雅黑",
      "size": 24,
      "bold": true,
      "color": "2E74B5"
    },
    "heading1": {
      "name": "微软雅黑",
      "size": 18,
      "bold": true,
      "color": "2E74B5"
    },
    "heading2": {
      "name": "微软雅黑",
      "size": 16,
      "bold": true,
      "color": "4F81BD"
    },
    "paragraph": {
      "name": "宋体",
      "size": 12
    },
    "code": {
      "name": "Consolas",
      "size": 11,
      "color": "000000"
    }
  },
  "colors": {
    "title": "2E74B5",
    "heading1": "2E74B5",
    "heading2": "4F81BD",
    "code_background": "F2F2F2",
    "quote_border": "CCCCCC"
  }
}
EOF

# 创建模板文件
echo "📄 创建模板文件..."
cat > templates/academic.docx.info << 'EOF'
学术论文模板
包含：标题页、摘要、关键词、章节编号、参考文献
EOF

cat > templates/business.docx.info << 'EOF'
商业报告模板
包含：公司Logo、页眉页脚、商业图表样式、专业配色
EOF

cat > templates/technical.docx.info << 'EOF'
技术文档模板
包含：代码样式、技术图表、API文档格式、版本历史
EOF

# 设置脚本权限
echo "🔧 设置脚本权限..."
chmod +x scripts/*.py
chmod +x install.sh

# 创建快速开始脚本
cat > quick_start.sh << 'EOF'
#!/bin/bash
# 快速开始脚本

echo "========================================="
echo "  Markdown转Word技能快速开始"
echo "========================================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行 ./install.sh"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 运行示例转换
echo "🚀 运行示例转换..."
python scripts/md2docx.py \
  --input examples/sample.md \
  --output examples/sample_output.docx \
  --debug

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 示例转换成功！"
    echo ""
    echo "📁 输出文件: examples/sample_output.docx"
    echo ""
    echo "🎯 使用示例:"
    echo "  1. 转换单个文件:"
    echo "     python scripts/md2docx.py --input your_file.md --output your_file.docx"
    echo ""
    echo "  2. 批量转换:"
    echo "     python scripts/md2docx_batch.py --input-dir ./docs --output-dir ./word_docs"
    echo ""
    echo "  3. 带图片转换:"
    echo "     python scripts/md2docx_with_images.py --input article.md --output article.docx --image-dir ./images"
    echo ""
    echo "📚 更多信息请查看 README.md"
else
    echo "❌ 示例转换失败"
    exit 1
fi
EOF

chmod +x quick_start.sh

echo ""
echo "========================================="
echo "✅ 安装完成！"
echo "========================================="
echo ""
echo "🎯 下一步:"
echo "  1. 激活虚拟环境: source venv/bin/activate"
echo "  2. 运行快速开始: ./quick_start.sh"
echo "  3. 查看文档: cat README.md"
echo ""
echo "📚 技能目录结构:"
echo "  📁 markdown-to-word-skill/"
echo "  ├── 📄 SKILL.md          # 技能定义"
echo "  ├── 📄 README.md         # 详细文档"
echo "  ├── 📁 scripts/          # Python脚本"
echo "  │   ├── md2docx.py       # 主转换脚本"
echo "  │   ├── md2docx_batch.py # 批量转换"
echo "  │   └── md2docx_with_images.py # 带图片转换"
echo "  ├── 📁 templates/        # Word模板"
echo "  ├── 📁 examples/         # 示例文件"
echo "  ├── 📁 test_images/      # 测试图片"
echo "  └── 📁 config/           # 配置文件"
echo ""
echo "🚀 开始使用: ./quick_start.sh"