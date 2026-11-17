#!/bin/bash
# Baseline 批量截图脚本 v2 - 使用 channel: 'chrome'

BASE_DIR="$HOME/.openclaw/workspace/skills/html2screenshot"
TRAIN_DIR="$BASE_DIR/test-data/training"
VAL_DIR="$BASE_DIR/test-data/validation"
OUTPUT_DIR="$BASE_DIR/test-data/output"
NODE_PATH="$HOME/.local/lib/node_modules"

mkdir -p "$OUTPUT_DIR"

echo "=========================================="
echo "📸 html2screenshot Baseline 测试开始"
echo "=========================================="
echo ""

run_screenshot() {
  local html_file="$1"
  local output_file="$2"
  
  $NODE_PATH/node - "$html_file" "$output_file" <<'EOF'
const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  try {
    const htmlFile = process.argv[2];
    const output = process.argv[3];
    const html = fs.readFileSync(htmlFile, 'utf8');

    const browser = await puppeteer.launch({
      headless: 'new',
      channel: 'chrome',
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800, deviceScaleFactor: 2 });
    await page.setContent(html, { waitUntil: 'load', timeout: 30000 });

    const dims = await page.evaluate(() => ({
      width: Math.ceil(document.body.scrollWidth),
      height: Math.ceil(document.body.scrollHeight),
    }));

    await page.setViewport({ width: dims.width, height: dims.height, deviceScaleFactor: 2 });
    await page.evaluate(() => window.stop());

    const screenshot = await page.screenshot({ type: 'png', fullPage: true });
    fs.writeFileSync(output, screenshot);
    
    console.log(JSON.stringify({
      success: true,
      width: dims.width,
      height: dims.height,
      fileSizeKB: Math.round(screenshot.length / 1024)
    }));

    await browser.close();
  } catch (e) {
    console.log(JSON.stringify({ success: false, error: e.message }));
    process.exit(1);
  }
})();
EOF
}

# 训练集
echo "📚 训练集 (T1-T15)"
echo "-------------------"

for task in T1 T2 T3 T4 T5 T6 T7 T8 T9 T10 T11 T12 T13 T14 T15; do
  html_file="$TRAIN_DIR/${task}.html"
  output_file="$OUTPUT_DIR/${task}.png"
  echo -n "  ⏳ $task ... "
  
  result=$(run_screenshot "$html_file" "$output_file" 2>/dev/null)
  
  if echo "$result" | grep -q '"success":true'; then
    width=$(echo "$result" | sed 's/.*"width":\([0-9]*\).*/\1/')
    height=$(echo "$result" | sed 's/.*"height":\([0-9]*\).*/\1/')
    size=$(echo "$result" | sed 's/.*"fileSizeKB":\([0-9]*\).*/\1/')
    echo "✅ ${width}x${height} (${size}KB)"
  else
    error=$(echo "$result" | sed 's/.*"error":"\([^"]*\)".*/\1/' | head -1)
    echo "❌ 失败: $error"
  fi
done

echo ""
echo "📋 验证集 (V1-V10)"
echo "-------------------"

for task in V1 V2 V3 V4 V5 V6 V7 V8 V9 V10; do
  html_file="$VAL_DIR/${task}.html"
  output_file="$OUTPUT_DIR/${task}.png"
  echo -n "  ⏳ $task ... "
  
  result=$(run_screenshot "$html_file" "$output_file" 2>/dev/null)
  
  if echo "$result" | grep -q '"success":true'; then
    width=$(echo "$result" | sed 's/.*"width":\([0-9]*\).*/\1/')
    height=$(echo "$result" | sed 's/.*"height":\([0-9]*\).*/\1/')
    size=$(echo "$result" | sed 's/.*"fileSizeKB":\([0-9]*\).*/\1/')
    echo "✅ ${width}x${height} (${size}KB)"
  else
    error=$(echo "$result" | sed 's/.*"error":"\([^"]*\)".*/\1/' | head -1)
    echo "❌ 失败: $error"
  fi
done

echo ""
echo "=========================================="
echo "✅ Baseline 截图完成"
echo "=========================================="
echo ""
echo "输出目录: $OUTPUT_DIR"
echo "文件列表:"
ls -lh "$OUTPUT_DIR"/*.png 2>/dev/null | awk '{print "  " $NF ": " $5}'
echo ""
echo "总文件数: $(ls "$OUTPUT_DIR"/*.png 2>/dev/null | wc -l) / 25"