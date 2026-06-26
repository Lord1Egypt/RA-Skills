#!/bin/bash
# 测试批量提取Kettle SQL脚本功能

set -e

echo "🧪 测试批量提取Kettle SQL脚本功能"
echo "======================================"

# 创建测试目录
TEST_DIR="test_kettle_files"
OUTPUT_DIR="test_batch_output"

# 清理旧的测试文件
rm -rf "$TEST_DIR" "$OUTPUT_DIR"

# 创建测试目录
mkdir -p "$TEST_DIR"

echo "📁 创建测试Kettle文件..."

# 创建几个示例Kettle文件
cat > "$TEST_DIR/job1.kjb" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<job>
  <name>测试作业1</name>
  <entries>
    <entry>
      <name>建表SQL</name>
      <type>SQL</type>
      <sql><![CDATA[CREATE TABLE test_table1 (
  id BIGINT,
  name VARCHAR(100),
  amount DECIMAL(18,2),
  create_time TIMESTAMP
);]]></sql>
    </entry>
    <entry>
      <name>插入SQL</name>
      <type>SQL</type>
      <sql><![CDATA[INSERT INTO test_table1 
SELECT 
  user_id,
  user_name,
  order_amount,
  CURRENT_TIMESTAMP
FROM source_table
WHERE create_date = '2024-01-01';]]></sql>
    </entry>
  </entries>
</job>
EOF

cat > "$TEST_DIR/job2.ktr" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<transformation>
  <name>测试转换2</name>
  <entries>
    <entry>
      <name>复杂查询SQL</name>
      <type>SQL</type>
      <sql><![CDATA[WITH user_stats AS (
  SELECT 
    user_id,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount
  FROM orders
  WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31'
  GROUP BY user_id
)
SELECT 
  u.user_id,
  u.user_name,
  s.order_count,
  s.total_amount,
  COALESCE(s.avg_amount, 0) AS avg_amount
FROM users u
LEFT JOIN user_stats s ON u.user_id = s.user_id
ORDER BY s.total_amount DESC;]]></sql>
    </entry>
    <entry>
      <name>更新SQL</name>
      <type>SQL</type>
      <sql><![CDATA[UPDATE customer_stats 
SET last_order_date = (
  SELECT MAX(order_date) 
  FROM orders 
  WHERE customer_id = customer_stats.customer_id
),
total_orders = (
  SELECT COUNT(*) 
  FROM orders 
  WHERE customer_id = customer_stats.customer_id
)
WHERE customer_id IN (SELECT customer_id FROM active_customers);]]></sql>
    </entry>
  </entries>
</transformation>
EOF

cat > "$TEST_DIR/job3.kjb" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<job>
  <name>测试作业3 - 包含XML转义字符</name>
  <entries>
    <entry>
      <name>条件查询SQL</name>
      <type>SQL</type>
      <sql><![CDATA[SELECT 
  product_id,
  product_name,
  CASE 
    WHEN price &lt; 100 THEN '低价'
    WHEN price BETWEEN 100 AND 500 THEN '中价'
    WHEN price &gt; 500 THEN '高价'
    ELSE '未知'
  END AS price_category,
  NVL(stock_quantity, 0) AS stock
FROM products
WHERE category_id = 1
  AND status = 'ACTIVE'
ORDER BY price DESC;]]></sql>
    </entry>
  </entries>
</job>
EOF

echo "✅ 创建了3个测试Kettle文件:"
echo "  - $TEST_DIR/job1.kjb (简单建表和插入)"
echo "  - $TEST_DIR/job2.ktr (复杂CTE查询和更新)"
echo "  - $TEST_DIR/job3.kjb (包含XML转义字符)"

echo ""
echo "🔧 运行批量提取工具..."
echo "--------------------------------------"

# 运行批量提取
python3 batch_extract_kettle_sql.py --dir "$TEST_DIR" --output "$OUTPUT_DIR" --consolidate

echo ""
echo "📊 检查输出结果..."
echo "--------------------------------------"

# 检查输出目录
if [ -d "$OUTPUT_DIR" ]; then
  echo "✅ 输出目录已创建: $OUTPUT_DIR"
  
  # 查找最新的批处理目录
  LATEST_BATCH=$(ls -td "$OUTPUT_DIR"/batch_* 2>/dev/null | head -1)
  
  if [ -n "$LATEST_BATCH" ] && [ -d "$LATEST_BATCH" ]; then
    echo "✅ 批处理目录: $LATEST_BATCH"
    
    # 检查关键文件
    echo "📋 输出文件检查:"
    
    if [ -f "$LATEST_BATCH/batch_summary.txt" ]; then
      echo "  ✅ batch_summary.txt 存在"
      echo "  └── 内容预览:"
      head -20 "$LATEST_BATCH/batch_summary.txt" | sed 's/^/    /'
    else
      echo "  ❌ batch_summary.txt 不存在"
    fi
    
    if [ -f "$LATEST_BATCH/batch_report.html" ]; then
      echo "  ✅ batch_report.html 存在"
    else
      echo "  ❌ batch_report.html 不存在"
    fi
    
    if [ -f "$LATEST_BATCH/all_extracted_sql.txt" ]; then
      echo "  ✅ all_extracted_sql.txt 存在"
      SQL_COUNT=$(grep -c "^【文件】" "$LATEST_BATCH/all_extracted_sql.txt" 2>/dev/null || echo "0")
      echo "  └── 提取了 $SQL_COUNT 个文件的SQL"
    else
      echo "  ❌ all_extracted_sql.txt 不存在"
    fi
    
    # 检查单个文件输出
    if [ -d "$LATEST_BATCH/kettle_files" ]; then
      FILE_COUNT=$(find "$LATEST_BATCH/kettle_files" -maxdepth 1 -type d | wc -l)
      echo "  ✅ kettle_files/ 目录存在，包含 $((FILE_COUNT-1)) 个文件结果"
      
      # 检查一个具体的文件结果
      FIRST_JOB=$(find "$LATEST_BATCH/kettle_files" -maxdepth 1 -type d -name "*job1*" | head -1)
      if [ -n "$FIRST_JOB" ] && [ -d "$FIRST_JOB" ]; then
        echo "  └── job1.kjb 的结果目录: $FIRST_JOB"
        if [ -f "$FIRST_JOB/extracted_sql.txt" ]; then
          echo "      ✅ extracted_sql.txt 存在"
          SQL_COMPONENTS=$(grep -c "^SQL组件" "$FIRST_JOB/extracted_sql.txt" 2>/dev/null || echo "0")
          echo "      └── 包含 $SQL_COMPONENTS 个SQL组件"
        fi
      fi
    fi
    
  else
    echo "❌ 未找到批处理目录"
  fi
  
else
  echo "❌ 输出目录未创建"
fi

echo ""
echo "🧪 测试批量处理指定文件列表..."
echo "--------------------------------------"

# 创建文件列表
FILE_LIST="test_file_list.txt"
echo "$TEST_DIR/job1.kjb" > "$FILE_LIST"
echo "$TEST_DIR/job3.kjb" >> "$FILE_LIST"

SPECIFIED_OUTPUT="test_specified_output"

python3 batch_extract_kettle_sql.py --list "$FILE_LIST" --output "$SPECIFIED_OUTPUT"

if [ -d "$SPECIFIED_OUTPUT" ]; then
  SPECIFIED_BATCH=$(ls -td "$SPECIFIED_OUTPUT"/batch_* 2>/dev/null | head -1)
  if [ -n "$SPECIFIED_BATCH" ] && [ -d "$SPECIFIED_BATCH" ]; then
    echo "✅ 指定文件列表处理完成: $SPECIFIED_BATCH"
    if [ -f "$SPECIFIED_BATCH/batch_summary.txt" ]; then
      TOTAL_FILES=$(grep "总文件数:" "$SPECIFIED_BATCH/batch_summary.txt" | grep -o '[0-9]\+' || echo "0")
      echo "  └── 处理了 $TOTAL_FILES 个文件"
    fi
  fi
fi

echo ""
echo "======================================"
echo "🧪 测试总结"
echo "--------------------------------------"

# 检查提取的SQL内容
if [ -f "$LATEST_BATCH/all_extracted_sql.txt" ]; then
  echo "✅ SQL提取测试通过"
  
  # 检查是否处理了XML转义字符
  if grep -q "price &lt; 100" "$LATEST_BATCH/all_extracted_sql.txt"; then
    echo "⚠️  警告: 发现未处理的XML转义字符 '&lt;'"
  else
    echo "✅ XML转义字符处理正常"
  fi
  
  # 检查SQL组件数量
  TOTAL_SQL=$(grep -c "^组件 [0-9]:" "$LATEST_BATCH/all_extracted_sql.txt" 2>/dev/null || echo "0")
  echo "✅ 总共提取了 $TOTAL_SQL 个SQL组件"
  
  # 检查不同类型的SQL
  if grep -qi "CREATE TABLE" "$LATEST_BATCH/all_extracted_sql.txt"; then
    echo "✅ 包含建表语句"
  fi
  
  if grep -qi "INSERT INTO" "$LATEST_BATCH/all_extracted_sql.txt"; then
    echo "✅ 包含插入语句"
  fi
  
  if grep -qi "WITH.*AS" "$LATEST_BATCH/all_extracted_sql.txt"; then
    echo "✅ 包含CTE查询"
  fi
  
  if grep -qi "COALESCE" "$LATEST_BATCH/all_extracted_sql.txt"; then
    echo "✅ 包含COALESCE函数"
  fi
  
else
  echo "❌ SQL提取测试失败"
fi

echo ""
echo "🧹 清理测试文件..."
echo "--------------------------------------"

# 询问是否清理
read -p "是否清理测试文件? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  rm -rf "$TEST_DIR" "$OUTPUT_DIR" "$SPECIFIED_OUTPUT" "$FILE_LIST"
  echo "✅ 测试文件已清理"
else
  echo "📁 测试文件保留在:"
  echo "  - $TEST_DIR (测试Kettle文件)"
  echo "  - $OUTPUT_DIR (目录批量处理结果)"
  echo "  - $SPECIFIED_OUTPUT (文件列表处理结果)"
  echo "  - $FILE_LIST (文件列表)"
fi

echo ""
echo "======================================"
echo "✅ 批量提取功能测试完成"
echo "现在你可以使用批量提取工具处理你的Kettle作业了!"