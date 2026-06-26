        if not os.path.exists(input_file):
            print(f"❌ 输入文件不存在: {input_file}")
            return False
        
        # 读取Markdown文件
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        
        if debug:
            print(f"📄 读取Markdown文件: {input_file} ({len(markdown_text)} 字符)")
        
        # 创建转换器
        converter = MarkdownToDocxConverter(template, debug)
        
        # 转换
        converter.convert(markdown_text, image_dir)
        
        # 保存
        converter.save(output_file)
        
        print(f"✅ 转换成功: {input_file} → {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        return False


def list_available_styles(template_path: Optional[str] = None):
    """列出可用样式"""
    try:
        if template_path and os.path.exists(template_path):
            doc = Document(template_path)
            print(f"📋 模板中的样式: {template_path}")
        else:
            doc = Document()
            print("📋 默认样式:")
        
        for style in doc.styles:
            print(f"  - {style.name} ({style.type})")
    
    except Exception as e:
        print(f"❌ 列出样式失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Markdown转Word文档转换器')
    parser.add_argument('--input', '-i', required=True, help='输入Markdown文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出Word文件路径')
    parser.add_argument('--template', '-t', help='Word模板文件路径')
    parser.add_argument('--image-dir', '-d', help='图片目录路径')
    parser.add_argument('--list-styles', action='store_true', help='列出可用样式')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    parser.add_argument('--encoding', default='utf-8', help='文件编码（默认: utf-8）')
    
    args = parser.parse_args()
    
    if args.list_styles:
        list_available_styles(args.template)
        return
    
    # 确保输出目录存在
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # 执行转换
    success = convert_markdown_to_docx(
        input_file=args.input,
        output_file=args.output,
        template=args.template,
        image_dir=args.image_dir,
        debug=args.debug
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()