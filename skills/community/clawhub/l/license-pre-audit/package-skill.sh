#!/bin/bash
# 打包技能文件夹，确保所有必需文件都被包含

SKILL_NAME="license-pre-audit"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
OUTPUT_DIR="/Users/xiajinchun/Desktop/${SKILL_NAME}-package"
OUTPUT_ZIP="/Users/xiajinchun/Desktop/${SKILL_NAME}-${TIMESTAMP}.zip"

echo "📦 开始打包 ${SKILL_NAME} 技能..."

# 创建临时目录
TEMP_DIR=$(mktemp -d)
PACKAGE_DIR="${TEMP_DIR}/${SKILL_NAME}"

# 复制技能文件夹
cp -r ~/.openclaw/workspace/skills/${SKILL_NAME} ${PACKAGE_DIR}

# 验证关键文件是否存在
echo "🔍 验证关键文件..."
KEY_FILES=(
  "src/index.js"
  "src/utils/check-deps.js"
  "src/utils/pdf-ocr.js"
  "src/utils/stamp-detect.js"
  "src/utils/field-normalize.js"
  "src/utils/extract-archive.js"
  "src/utils/generate-table.js"
  "src/utils/llm-client.js"
  "src/rules/index.js"
  "references/audit-rules.json"
  "references/doc-types.json"
  "references/settings.json"
  "SKILL.md"
)

MISSING_FILES=()
for file in "${KEY_FILES[@]}"; do
  if [ ! -f "${PACKAGE_DIR}/${file}" ]; then
    MISSING_FILES+=("$file")
    echo "❌ 缺失：${file}"
  else
    echo "✅ 存在：${file}"
  fi
done

if [ ${#MISSING_FILES[@]} -ne 0 ]; then
  echo ""
  echo "❌ 发现缺失文件，打包失败！"
  echo "缺失文件列表："
  printf '  - %s\n' "${MISSING_FILES[@]}"
  rm -rf ${TEMP_DIR}
  exit 1
fi

echo ""
echo "✅ 所有关键文件已验证"

# 创建压缩包
echo ""
echo "📦 创建压缩包..."
cd ${TEMP_DIR}
zip -r ${OUTPUT_ZIP} ${SKILL_NAME} -x "*.git*" -x "*node_modules*" -x "*bak*" -x "*__pycache__*"

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ 打包成功！"
  echo "📍 压缩包位置：${OUTPUT_ZIP}"
  echo "📦 压缩包大小：$(du -h ${OUTPUT_ZIP} | cut -f1)"
  echo ""
  echo "📋 发送同事时请附带以下说明："
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "【license-pre-audit 技能使用说明】"
  echo ""
  echo "1. 解压压缩包到任意目录"
  echo "   unzip license-pre-audit-*.zip"
  echo ""
  echo "2. 进入技能目录"
  echo "   cd license-pre-audit"
  echo ""
  echo "3. 直接运行（会自动安装依赖）"
  echo "   node src/index.js <文件夹路径或压缩包路径>"
  echo ""
  echo "4. Windows 系统会自动："
  echo "   - 检测并安装 Chocolatey（如果缺失）"
  echo "   - 使用 Chocolatey 安装所有依赖"
  echo "   - 全程无需手动操作"
  echo ""
  echo "⏱️ 首次运行约需 7-14 分钟（自动安装依赖）"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
  echo ""
  echo "❌ 打包失败！"
  rm -rf ${TEMP_DIR}
  exit 1
fi

# 清理临时目录
rm -rf ${TEMP_DIR}
