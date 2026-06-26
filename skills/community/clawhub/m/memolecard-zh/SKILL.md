#!/bin/bash
set -e
# ========== 配置参数 ==========
SESSION_NAME="moccard-auto"
MEMOLE_URL="https://www.moccard.com/"
CARD_TITLE="{{title}}"       # 用户输入标题，标题不少于30字
CARD_CONTENT="{{content}}"   # 用户输入正文，正文的内容不少于600字，正文为富文本内容
STYLE_CATEGORY="{{style_cat}}" # 样式分类（如简约风）
STYLE_INDEX="{{style_idx}}"  # 样式序号
DOWNLOAD_PATH="$HOME/Downloads" # 浏览器默认下载路径
ZIP_PATTERN="images-*.zip"  # 压缩包命名规则
# 兜底下载配置（根据实际服务器地址调整）
BACKUP_SERVER_URL="{{ip}}" # 兜底下载接口
TIMEOUT_SECONDS=15 # 整体超时时间

# ========== 前置校验 ==========
# 校验标题/正文长度
if [ ${#CARD_TITLE} -lt 30 ]; then
  echo "❌ 标题长度不足30字，请检查输入"
  exit 1
fi
if [ ${#CARD_CONTENT} -lt 600 ]; then
  echo "❌ 正文长度不足600字，请检查输入"
  exit 1
fi

# ========== 步骤1：初始化 + 打开官网 ==========
# 清理旧会话
agent-browser --session $SESSION_NAME close 2>/dev/null || true
# 打开官网（无头模式，调试加 --headed）
agent-browser --session $SESSION_NAME open $MEMOLE_URL \
  --set download.path "$DOWNLOAD_PATH" \ # 指定下载路径（关键！）
  --timeout ${TIMEOUT_SECONDS}000
agent-browser --session $SESSION_NAME wait --load networkidle

# ========== 步骤2：进入文章转卡片功能 ==========
agent-browser --session $SESSION_NAME scroll down 800
# 增强元素定位（兼容多语言/文本变体）
agent-browser --session $SESSION_NAME find --multiple \
  text "开始免费使用【文章转卡片】" \
  text "文章转卡片" \
  click
agent-browser --session $SESSION_NAME wait --load networkidle

# ========== 步骤3：输入标题/正文 ==========
agent-browser --session $SESSION_NAME find \
  label "标题" \
  input[name="title"] \
  fill "$CARD_TITLE"
agent-browser --session $SESSION_NAME find \
  label "正文" \
  textarea[name="content"] \
  div[class*="rich-text"] \
  fill "$CARD_CONTENT"
agent-browser --session $SESSION_NAME wait 1000

# ========== 步骤4：选择卡片样式 ==========
agent-browser --session $SESSION_NAME find text "卡片样式" click
agent-browser --session $SESSION_NAME wait 2000
agent-browser --session $SESSION_NAME find text "$STYLE_CATEGORY" click
agent-browser --session $SESSION_NAME find nth $STYLE_INDEX ".style-item" click
agent-browser --session $SESSION_NAME find text "确定" click
agent-browser --session $SESSION_NAME wait --load networkidle

# ========== 步骤5：全自动拆分 ==========
agent-browser --session $SESSION_NAME find \
  text "全自动拆分" \
  button[class*="split-btn"] \
  click
agent-browser --session $SESSION_NAME wait --text "拆分完成" --timeout 10000
agent-browser --session $SESSION_NAME wait 3000

# ========== 步骤6：打包下载（适配原生API） ==========
DOWNLOAD_URL=""

## 方式1：捕获下载链接（优先）
echo "🔍 捕获原生下载链接..."
DOWNLOAD_URL=$(agent-browser --session $SESSION_NAME eval "
  // 重写浏览器原生下载API，捕获链接
  window.originalDownload = window.download || window.URL.createObjectURL;
  let downloadUrl = '';
  window.download = function(url) {
    downloadUrl = url;
    return window.originalDownload(url);
  };
  // 点击下载按钮并监听
  const downloadBtn = document.querySelector('*:contains(\"打包下载\")') || document.querySelector('.download-btn');
  if (downloadBtn) {
    downloadBtn.click();
    setTimeout(() => { downloadUrl = downloadUrl || window.downloadUrl; }, 1500);
  }
  downloadUrl;
" --json | jq -r '.result')

## 方式2：监控本地下载文件（备用，本地路径）
if [ -z "$DOWNLOAD_URL" ]; then
  echo "🔍 监控本地下载文件..."
  # 清空旧文件
  rm -f "$DOWNLOAD_PATH/$ZIP_PATTERN" 2>/dev/null
  # 点击打包下载
  agent-browser --session $SESSION_NAME find \
    text "打包下载" \
    button[class*="download"] \
    click
  # 等待文件下载完成（最多等10秒）
  for ((i=0; i<10; i++)); do
    ZIP_FILE=$(ls "$DOWNLOAD_PATH/$ZIP_PATTERN" 2>/dev/null | head -1)
    if [ -n "$ZIP_FILE" ]; then
      DOWNLOAD_URL="file://$ZIP_FILE"
      break
    fi
    sleep 1
  done
fi

## 方式3：兜底下载（从服务器拉取图片压缩包）
if [ -z "$DOWNLOAD_URL" ]; then
  echo "🔍 执行兜底策略：从服务器下载图片压缩包..."
  # 步骤1：获取当前卡片ID（从页面/接口提取）
  CARD_ID=$(agent-browser --session $SESSION_NAME eval "
    // 从页面DOM/全局变量提取卡片ID（根据实际页面结构调整）
    const cardId = window.cardId || document.querySelector('[data-card-id]')?.dataset.cardId || '';
    cardId;
  " --json | jq -r '.result')

  if [ -n "$CARD_ID" ] && [ "$CARD_ID" != "null" ]; then
    # 步骤2：调用服务器接口下载压缩包
    BACKUP_ZIP="$DOWNLOAD_PATH/memolecard-backup-$CARD_ID.zip"
    # 发送请求下载（适配常见鉴权方式，如Cookie/Token）
    COOKIES=$(agent-browser --session $SESSION_NAME eval "document.cookie" --json | jq -r '.result')
    curl -s -o "$BACKUP_ZIP" \
      -H "Cookie: $COOKIES" \
      -H "User-Agent: $(agent-browser --session $SESSION_NAME eval 'navigator.userAgent' --json | jq -r '.result')" \
      "${BACKUP_SERVER_URL}?cardId=$CARD_ID&style=$STYLE_INDEX"
    
    # 校验兜底文件是否存在
    if [ -f "$BACKUP_ZIP" ] && [ -s "$BACKUP_ZIP" ]; then
      DOWNLOAD_URL="file://$BACKUP_ZIP"
      echo "✅ 兜底下载成功：$DOWNLOAD_URL"
    else
      echo "❌ 兜底下载失败：服务器返回空文件"
      rm -f "$BACKUP_ZIP" 2>/dev/null
    fi
  else
    echo "❌ 兜底下载失败：无法获取卡片ID"
  fi
fi

# ========== 步骤7：返回结果 ==========
if [ -n "$DOWNLOAD_URL" ] && [ "$DOWNLOAD_URL" != "null" ]; then
  echo "✅ 下载成功！压缩包地址：$DOWNLOAD_URL"
  echo "MEMOLE_DOWNLOAD_URL=$DOWNLOAD_URL" # 供ClawHub返回给用户
else
  echo "❌ 所有下载方式均失败，请检查："
  echo "  1. 页面元素是否匹配（如按钮文本、样式类名）"
  echo "  2. 兜底服务器地址是否正确"
  echo "  3. 卡片ID提取逻辑是否适配当前页面"
  exit 1
fi

# ========== 清理工作 ==========
# 关闭浏览器会话
agent-browser --session $SESSION_NAME close 2>/dev/null || true
# 清理临时变量
unset CARD_ID BACKUP_ZIP COOKIES

exit 0