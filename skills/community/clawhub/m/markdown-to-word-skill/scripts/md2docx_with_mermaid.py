    parser = argparse.ArgumentParser(description='支持Mermaid的Markdown转Word转换器')
    parser.add_argument('--input', '-i', required=True, help='输入Markdown文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出Word文件路径')
    parser.add_argument('--template', '-t', help='Word模板文件路径')
    parser.add_argument('--image-dir', '-d', help='图片目录路径')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # 执行转换
    success = convert_markdown_with_mermaid(
        input_file=args.input,
        output_file=args.output,
        template=args.template,
        image_dir=args.image_dir,
        debug=args.debug
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()