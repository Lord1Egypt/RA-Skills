#!/bin/bash
# fix_kettle_extract.sh
# Kettle作业SQL提取问题快速修复脚本

set -e

echo "🔧 Kettle作业SQL提取问题快速修复工具"
echo "=========================================="

# 参数检查
if [ $# -lt 1 ]; then
    echo "用法: $0 <kettle文件路径> [输出目录]"
    echo ""
    echo "示例:"
    echo "  $0 /path/to/job_DWD_HEL_INV_BALANCE_DAY.kjb"
    echo "  $0 job.kjb output_analysis"
    exit 1
fi

KETTLE_FILE="$1"
OUTPUT_DIR="${2:-kettle_analysis_$(date +%Y%m%d_%H%M%S)}"

# 检查文件是否存在
if [ ! -f "$KETTLE_FILE" ]; then
    echo "❌ 错误: 文件不存在: $KETTLE_FILE"
    exit 1
fi

echo "📄 处理文件: $KETTLE_FILE"
echo "📁 输出目录: $OUTPUT_DIR"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo ""
echo "📊 步骤1: 基本信息分析"
echo "----------------------"

# 文件大小
FILE_SIZE=$(ls -lh "$KETTLE_FILE" | awk '{print $5}')
echo "文件大小: $FILE_SIZE"

# SQL组件数量
SQL_COUNT=$(grep -c "<sql>" "$KETTLE_FILE")
echo "SQL组件数量: $SQL_COUNT"

# 保存基本信息
echo "文件: $(basename "$KETTLE_FILE")" > "$OUTPUT_DIR/basic_info.txt"
echo "大小: $FILE_SIZE" >> "$OUTPUT_DIR/basic_info.txt"
echo "SQL组件: $SQL_COUNT" >> "$OUTPUT_DIR/basic_info.txt"
echo "分析时间: $(date)" >> "$OUTPUT_DIR/basic_info.txt"

echo ""
echo "🔍 步骤2: 查看SQL组件名称"
echo "------------------------"

# 提取组件名称
echo "SQL组件列表:" > "$OUTPUT_DIR/components.txt"
grep -B5 "<sql>" "$KETTLE_FILE" | grep "<name>" | sed 's/.*<name>//g;s/<\/name>.*//g' | cat -n >> "$OUTPUT_DIR/components.txt"
cat "$OUTPUT_DIR/components.txt"

echo ""
echo "💾 步骤3: 完整提取SQL内容"
echo "------------------------"

# 创建Python提取脚本
cat > "$OUTPUT_DIR/extract_kettle_complete.py" << 'EOF'
#!/usr/bin/env python3
"""
Kettle SQL完整提取脚本
解决XML转义字符和截断问题
"""
import re
import sys
import os

def extract_complete_sql(file_path):
    """完整提取Kettle SQL"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复1: 替换XML特殊字符
    content = content.replace('&lt;', '<').replace('&gt;', '>')
    content = content.replace('&amp;', '&')
    
    # 修复2: 使用[\s\S]匹配任何字符
    entries = re.findall(r'<entry>[\s\S]*?</entry>', content)
    
    sql_components = []
    
    for i, entry in enumerate(entries, 1):
        name_match = re.search(r'<name>([^<]+)</name>', entry)
        step_name = name_match.group(1).strip() if name_match else f"步骤_{i}"
        
        sql_match = re.search(r'<sql>([\s\S]*?)</sql>', entry)
        if sql_match:
            sql_content = sql_match.group(1).strip()
            sql_content = re.sub(r'<!\[CDATA\[|\]\]>', '', sql_content)
            
            if sql_content:
                sql_components.append({
                    'step': step_name,
                    'sql': sql_content,
                    'length': len(sql_content)
                })
    
    return sql_components

def main():
    if len(sys.argv) < 2:
        print("用法: python extract_kettle_complete.py <kettle文件>")
        sys.exit(1)
    
    kettle_file = sys.argv[1]
    print(f"处理文件: {kettle_file}")
    
    components = extract_complete_sql(kettle_file)
    
    print(f"找到 {len(components)} 个SQL组件")
    
    # 保存结果
    output_file = os.path.splitext(kettle_file)[0] + "_complete_sql.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Kettle文件: {os.path.basename(kettle_file)}\n")
        f.write(f"SQL组件数量: {len(components)}\n")
        f.write("=" * 80 + "\n\n")
        
        total_length = 0
        for i, comp in enumerate(components, 1):
            f.write(f"SQL组件 {i}: {comp['step']}\n")
            f.write(f"长度: {comp['length']} 字符\n")
            f.write("-" * 40 + "\n")
            f.write(comp['sql'])
            f.write("\n\n" + "=" * 80 + "\n\n")
            total_length += comp['length']
        
        f.write(f"\n总计: {total_length} 字符\n")
    
    print(f"结果已保存到: {output_file}")
    
    # 验证提取完整性
    file_size = os.path.getsize(kettle_file)
    completeness_ratio = total_length / file_size
    
    print(f"\n📊 提取完整性验证:")
    print(f"  原始文件大小: {file_size} 字节")
    print(f"  提取SQL长度: {total_length} 字符")
    print(f"  提取比例: {completeness_ratio:.2%}")
    
    if completeness_ratio < 0.2:
        print("  ⚠️  警告: 提取比例较低，可能有不完整内容")
    else:
        print("  ✅ 提取比例正常")

if __name__ == "__main__":
    main()
EOF

# 执行提取
echo "执行SQL提取..."
python3 "$OUTPUT_DIR/extract_kettle_complete.py" "$KETTLE_FILE" > "$OUTPUT_DIR/extract.log" 2>&1

EXTRACTED_FILE="$(basename "$KETTLE_FILE" .kjb)_complete_sql.txt"
if [ -f "$EXTRACTED_FILE" ]; then
    mv "$EXTRACTED_FILE" "$OUTPUT_DIR/"
    echo "✅ SQL提取完成，结果保存在: $OUTPUT_DIR/$EXTRACTED_FILE"
else
    echo "❌ SQL提取失败，查看日志: $OUTPUT_DIR/extract.log"
fi

echo ""
echo "✅ 步骤4: 创建验证报告"
echo "----------------------"

# 创建验证脚本
cat > "$OUTPUT_DIR/validate_extraction.py" << 'EOF'
#!/usr/bin/env python3
"""
验证提取的SQL完整性
"""
import re
import os

def validate_sql_file(sql_file):
    """验证SQL文件完整性"""
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"验证文件: {os.path.basename(sql_file)}")
    print("=" * 60)
    
    # 1. 检查CREATE TABLE语句
    create_tables = re.findall(r'create table[^;]+;', content, re.IGNORECASE)
    print(f"1. 找到 {len(create_tables)} 个建表语句")
    
    # 2. 统计字段数量
    total_fields = 0
    for i, table_sql in enumerate(create_tables, 1):
        fields = re.findall(r'(\w+)\s+(?:bigint|varchar|numeric|timestamp|BIGINT|VARCHAR|DECIMAL|DATETIME)', 
                          table_sql, re.IGNORECASE)
        print(f"   表{i}: {len(fields)} 个字段")
        if len(fields) > 0:
            sample = ', '.join(fields[:3]) + ('...' if len(fields) > 3 else '')
            print(f"     示例字段: {sample}")
        total_fields += len(fields)
    
    # 3. 检查关键SQL模式
    patterns = [
        (r'CASE.*?END', 'CASE WHEN语句'),
        (r'SUM\(.*?\)', '聚合函数'),
        (r'JOIN.*?ON', '表关联'),
        (r'GROUP BY', '分组语句'),
        (r'WHERE.*=', '过滤条件')
    ]
    
    print(f"2. 关键SQL模式检查:")
    for pattern, description in patterns:
        count = len(re.findall(pattern, content, re.IGNORECASE | re.DOTALL))
        if count > 0:
            print(f"   ✅ {description}: {count} 个")
    
    # 4. 生成验证总结
    print("\n📋 验证总结:")
    print(f"   建表语句: {len(create_tables)} 个")
    print(f"   总字段数: {total_fields} 个")
    print(f"   平均每表: {total_fields/len(create_tables):.1f} 个字段" if create_tables else "   平均每表: N/A")
    
    # 5. 常见问题检查
    print("\n🔍 常见问题检查:")
    
    # 检查XML字符
    if '&lt;' in content or '&gt;' in content:
        print("   ⚠️  发现未处理的XML特殊字符")
    else:
        print("   ✅ XML特殊字符已正确处理")
    
    # 检查截断标记
    if '[...]' in content or '...' in content.lower():
        print("   ⚠️  可能存在内容截断")
    else:
        print("   ✅ 未发现明显截断标记")
    
    print("\n✅ 验证完成")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python validate_extraction.py <SQL文件>")
        sys.exit(1)
    
    validate_sql_file(sys.argv[1])
EOF

# 执行验证
if [ -f "$OUTPUT_DIR/$EXTRACTED_FILE" ]; then
    echo "执行SQL验证..."
    python3 "$OUTPUT_DIR/validate_extraction.py" "$OUTPUT_DIR/$EXTRACTED_FILE" > "$OUTPUT_DIR/validation_report.txt"
    echo "验证报告: $OUTPUT_DIR/validation_report.txt"
    cat "$OUTPUT_DIR/validation_report.txt"
else
    echo "跳过验证（SQL文件不存在）"
fi

echo ""
echo "📁 步骤5: 生成修复建议"
echo "----------------------"

cat > "$OUTPUT_DIR/fix_suggestions.md" << EOF
# Kettle作业SQL提取问题修复建议

## 问题诊断
- **文件**: $(basename "$KETTLE_FILE")
- **大小**: $FILE_SIZE
- **SQL组件**: $SQL_COUNT 个

## 发现的问题
根据分析，可能遇到以下问题：

### 1. SQL提取不完整
如果提取的SQL显示[...]或内容截断，可能是因为：
- XML特殊字符未处理（&lt;, &gt;, &amp;）
- 正则表达式匹配模式不正确
- SQL内容跨越多行

### 2. 字段缺失
如果字段数量不对，可能是因为：
- 多表创建语句未完整提取
- 字段注释被误处理
- 提取提前终止

## 解决方案

### 立即修复
已使用改进的提取脚本重新提取SQL，结果保存在：
\`\`\`
$OUTPUT_DIR/$EXTRACTED_FILE
\`\`\`

### 预防措施
1. **总是先处理XML特殊字符**：
   \`\`\`python
   content = content.replace('&lt;', '<').replace('&gt;', '>')
   \`\`\`

2. **使用正确的匹配模式**：
   \`\`\`python
   # 使用[\s\S]而不是.
   re.findall(r'<sql>([\s\S]*?)</sql>', content)
   \`\`\`

3. **验证提取结果**：
   - 检查提取长度（应大于文件大小20%）
   - 验证字段数量
   - 检查关键SQL模式

## 后续步骤

### 如果问题已解决
1. 使用提取的SQL进行转换
2. 验证处理后的SQL字段完整性
3. 检查业务逻辑一致性

### 如果问题未解决
1. 查看提取日志: \`$OUTPUT_DIR/extract.log\`
2. 检查原始Kettle文件结构
3. 手动查看XML内容定位问题

## 联系支持
如有问题，请提供：
1. \`$OUTPUT_DIR/basic_info.txt\`
2. \`$OUTPUT_DIR/extract.log\`
3. 具体的错误描述

---

**分析完成时间**: $(date)
EOF

echo "修复建议已保存到: $OUTPUT_DIR/fix_suggestions.md"

echo ""
echo "🎉 修复工具执行完成!"
echo "====================="
echo ""
echo "📋 生成的文件:"
echo "  $OUTPUT_DIR/basic_info.txt      # 基本信息"
echo "  $OUTPUT_DIR/components.txt       # SQL组件列表"
echo "  $OUTPUT_DIR/$EXTRACTED_FILE      # 提取的完整SQL"
echo "  $OUTPUT_DIR/validation_report.txt # 验证报告"
echo "  $OUTPUT_DIR/fix_suggestions.md   # 修复建议"
echo "  $OUTPUT_DIR/extract.log          # 提取日志"
echo ""
echo "🚀 下一步:"
echo "  1. 查看 $OUTPUT_DIR/validation_report.txt 验证结果"
echo "  2. 阅读 $OUTPUT_DIR/fix_suggestions.md 获取建议"
echo "  3. 使用提取的SQL进行进一步处理"
echo ""
echo "💡 提示: 如需重新分析，删除目录后重新运行:"
echo "  rm -rf $OUTPUT_DIR && $0 \"$KETTLE_FILE\""
echo ""