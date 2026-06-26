#!/bin/bash

# ==============================================================================
# md2pdf-local.sh
# 描述: 离线版 Markdown 转 PDF (完整版 Emoji + 本地缓存)
# 版本: 2.0 (Twemoji 完整版)
# 核心: Pandoc + WeasyPrint + Local Emoji Cache (Twemoji 完整版)
# ==============================================================================

set -e

# --- 配置项 ---
CACHE_DIR="$HOME/.cache/md2pdf"
EMOJI_DIR="$CACHE_DIR/emojis"
EMOJI_MAPPING="$CACHE_DIR/emoji_mapping.json"
# 使用 Twemoji 14.0.0 完整版 (彩色 PNG, 3660个文件)
TWEMOJI_VERSION="14.0.0"
TWEMOJI_URL="https://github.com/twitter/twemoji/archive/refs/tags/v${TWEMOJI_VERSION}.tar.gz"

# --- 检查参数 ---
if [ "$#" -ne 2 ]; then
    echo "用法: $0 <input.md> <output.pdf>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"
TEMP_DIR=$(mktemp -d)
HTML_TEMP="$TEMP_DIR/temp.html"
LUA_FILTER="$TEMP_DIR/emoji_twemoji.lua"
CSS_STYLE="$TEMP_DIR/style.css"
EMOJI_JS="$TEMP_DIR/emoji_data.js"

# --- 清理函数 ---
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# --- 1. 检查并下载 Twemoji 完整版 (只需执行一次) ---
ensure_twemoji() {
    if [ -f "$EMOJI_MAPPING" ]; then
        echo "✅ Twemoji 资源已缓存: $EMOJI_DIR"
        echo "   映射表: $EMOJI_MAPPING"
        return 0
    fi

    echo "🚧 正在设置 Twemoji ${TWEMOJI_VERSION}..."
    mkdir -p "$CACHE_DIR"

    # 下载 GitHub 的 tar.gz 包
    echo "   下载 Twemoji..."
    wget -q --show-progress -O "$CACHE_DIR/twemoji.tar.gz" "$TWEMOJI_URL"

    # 解压 Twemoji
    echo "   解压 Twemoji..."
    tar -xzf "$CACHE_DIR/twemoji.tar.gz" -C "$CACHE_DIR"

    # Twemoji 目录结构: twemoji-14.0.0/assets/72x72/
    # 移动到最终目录
    mv "$CACHE_DIR/twemoji-${TWEMOJI_VERSION}/assets/72x72" "$EMOJI_DIR"

    # 清理
    rm -rf "$CACHE_DIR/twemoji-${TWEMOJI_VERSION}" "$CACHE_DIR/twemoji.tar.gz"

    echo "   Twemoji 已缓存至: $EMOJI_DIR"

    # 生成 emoji 映射表
    echo "   生成 emoji 映射表..."
    python3 /home/ltx/.openclaw/workspace/skills/md2pdf-converter/scripts/generate_emoji_mapping.py

    echo "✅ Twemoji 完整版已准备就绪"
}

ensure_twemoji

# --- 2. 生成 Lua Filter (使用 emoji 映射表) ---
cat << 'EOF' > "$LUA_FILTER"
-- 使用 emoji 映射表的 Lua Filter

-- 读取 emoji 映射表
local emoji_mapping = {}
local mapping_file = io.open("EMOJI_MAPPING_PLACEHOLDER", "r")

if mapping_file then
    local json_str = mapping_file:read("*all")
    mapping_file:close()

    -- 解析 JSON (使用简单的正则表达式提取)
    for k, v in json_str:gmatch('"([^"]*)"%s*:%s*"([^"]*)"') do
        emoji_mapping[k] = v
    end
end

function Str(el)
    local text = el.text
    if #text == 0 then
        return nil
    end

    -- 检查文本是否包含 emoji
    local contains_emoji = false
    for p, c in utf8.codes(text) do
        -- Emoji 范围检测 (更全面)
        if (c >= 0x1F600 and c <= 0x1F64F) or -- Emoticons
           (c >= 0x1F300 and c <= 0x1F5FF) or -- Misc Symbols and Pictographs
           (c >= 0x1F680 and c <= 0x1F6FF) or -- Transport and Map
           (c >= 0x1F900 and c <= 0x1F9FF) or -- Supplemental Symbols and Pictographs
           (c >= 0x2600 and c <= 0x26FF) or   -- Misc Symbols
           (c >= 0x2700 and c <= 0x27BF) or   -- Dingbats
           (c >= 0x1F1E0 and c <= 0x1F1FF) or -- Regional Indicator Symbols
           (c >= 0x1F200 and c <= 0x1F2FF) or -- Enclosed Alphanumerics
           (c >= 0x2B50 and c <= 0x2BFF) or   -- Glagolitic Supplement
           (c >= 0x1F004 and c <= 0x1F0FF) or   -- Mahjong Tiles
           (c >= 0x1F0C0 and c <= 0x1F0FF) or   -- Domino Tiles
           (c >= 0x0FE0 and c <= 0x0FE0) or   -- Variation Selectors
           (c >= 0x1F300 and c <= 0x1F5FF) or -- Misc Symbols
           (c >= 0x1F680 and c <= 0x1F6FF) then -- Transport and Map
            contains_emoji = true
            break
        end
    end

    -- 如果不包含 emoji，直接返回 nil
    if not contains_emoji then
        return nil
    end

    -- 如果包含 emoji，逐字符处理
    local new_inlines = {}
    local emoji_dir = "EMOJI_DIR_PLACEHOLDER"

    for p, c in utf8.codes(text) do
        local emoji_char = utf8.char(c)
        local is_emoji = false

        -- 检测 emoji
        if (c >= 0x1F600 and c <= 0x1F64F) or -- Emoticons
           (c >= 0x1F300 and c <= 0x1F5FF) or -- Misc Symbols and Pictographs
           (c >= 0x1F680 and c <= 0x1F6FF) or -- Transport and Map
           (c >= 0x1F900 and c <= 0x1F9FF) or -- Supplemental Symbols and Pictographs
           (c >= 0x2600 and c <= 0x26FF) or   -- Misc Symbols
           (c >= 0x2700 and c <= 0x27BF) or   -- Dingbats
           (c >= 0x1F1E0 and c <= 0x1F1FF) or -- Regional Indicator Symbols
           (c >= 0x1F200 and c <= 0x1F2FF) or -- Enclosed Alphanumerics
           (c >= 0x2B50 and c <= 0x2BFF) or   -- Glagolitic Supplement
           (c >= 0x1F004 and c <= 0x1F0FF) or   -- Mahjong Tiles
           (c >= 0x1F0C0 and c <= 0x1F0FF) or   -- Domino Tiles
           (c >= 0x0FE0 and c <= 0x0FE0) or   -- Variation Selectors
           (c >= 0x1F300 and c <= 0x1F5FF) or -- Misc Symbols
           (c >= 0x1F680 and c <= 0x1F6FF) then -- Transport and Map
            is_emoji = true
        end

        if is_emoji then
            -- 查找对应的文件名
            local filename = emoji_mapping[emoji_char]

            if filename then
                -- 构建本地 file:// 路径
                local url = "file://" .. emoji_dir .. "/" .. filename

                -- 生成 HTML img 标签
                local img_html = string.format(
                    '<img src="%s" class="emoji" alt="%s" style="height:1.1em;width:1.1em;vertical-align:-0.2em;display:inline-block;margin:0 0.05em;">',
                    url,
                    emoji_char
                )

                table.insert(new_inlines, pandoc.RawInline('html', img_html))
            else
                -- 如果找不到对应的文件，保持原字符
                table.insert(new_inlines, pandoc.Str(emoji_char))
            end
        else
            table.insert(new_inlines, pandoc.Str(emoji_char))
        end
    end

    if #new_inlines > 0 then
        return new_inlines
    else
        return nil
    end
end
EOF

# 替换 Lua 模板中的路径占位符
sed -e "s|EMOJI_DIR_PLACEHOLDER|$EMOJI_DIR|g; s|EMOJI_MAPPING_PLACEHOLDER|$EMOJI_MAPPING|g" "$LUA_FILTER" > "${LUA_FILTER}.tmp"
mv "${LUA_FILTER}.tmp" "$LUA_FILTER"

# --- 3. 生成 CSS 样式 ---
cat << 'EOF' > "$CSS_STYLE"
@page {
    size: A4;
    margin: 2.5cm;
    @bottom-center {
        content: "Page " counter(page);
        font-family: "AR PL UMing CN", "Noto Sans SC", sans-serif;
        font-size: 9pt;
        color: #888;
    }
}

body {
    font-family: "AR PL UMing CN", "AR PL SungtiL GB", "AR PL KaitiM GB", "Noto Sans SC", "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
    line-height: 1.6;
    font-size: 11pt;
    color: #333;
}

/* Emoji 样式：确保彩色 PNG 正确显示 */
img.emoji {
    height: 1.1em;
    width: 1.1em;
    vertical-align: -0.2em;
    display: inline-block;
    margin: 0 0.05em;
    /* 强制彩色显示 */
    image-rendering: auto;
}

h1, h2, h3 {
    font-family: "AR PL UMing CN", "AR PL SungtiL GB", "AR PL KaitiM GB", "Noto Sans SC", sans-serif;
    font-weight: bold;
    color: #2c3e50;
}

h1 {
    border-bottom: 2px solid #eee;
    padding-bottom: 0.3em;
}

code {
    background-color: #f5f5f5;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: "Menlo", "Monaco", monospace;
}

pre {
    background-color: #f5f5f5;
    padding: 1em;
    border-radius: 5px;
    overflow-x: auto;
}

blockquote {
    border-left: 4px solid #ddd;
    padding-left: 1em;
    color: #777;
    font-style: italic;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #f8f9fa;
}
EOF

# --- 4. 执行转换 ---

echo "📝 正在处理 Markdown (使用 Twemoji 完整版 ${TWEMOJI_VERSION})..."
pandoc "$INPUT_FILE" \
    --lua-filter="$LUA_FILTER" \
    --css="$CSS_STYLE" \
    --metadata title=" " \
    --standalone \
    -o "$HTML_TEMP"

echo "🖨️  正在生成 PDF..."
weasyprint "$HTML_TEMP" "$OUTPUT_FILE"

echo "✨ 转换成功: $OUTPUT_FILE"
echo ""
echo "📊 Emoji 信息:"
echo "   - 版本: Twemoji ${TWEMOJI_VERSION}"
echo "   - 数量: 3660 个彩色 PNG (包含变体)"
echo "   - 大小: 72x72px"
echo "   - 位置: $EMOJI_DIR"
