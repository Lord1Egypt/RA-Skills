#!/bin/bash
# check_duplicate.sh - 检查论文是否已处理（去重）
# 用法：./check_duplicate.sh <metadata.json> <papers_dir>
# 返回：
#   0 - 新论文（需要处理）
#   1 - 完全重复（停止处理）
#   2 - 补充材料（需要合并）

set -e

METADATA_JSON="$1"
PAPERS_DIR="$2"

if [[ -z "$METADATA_JSON" || -z "$PAPERS_DIR" ]]; then
    echo "❌ 用法：$0 <metadata.json> <papers_dir>"
    exit 1
fi

if [[ ! -f "$METADATA_JSON" ]]; then
    echo "❌ 元数据文件不存在：$METADATA_JSON"
    exit 1
fi

# 提取元数据
PAPER_ID=$(jq -r '.paper_id' "$METADATA_JSON")
DOI=$(jq -r '.doi // empty' "$METADATA_JSON")
PDF_HASH=$(jq -r '.pdf_hash' "$METADATA_JSON")
TITLE=$(jq -r '.title // empty' "$METADATA_JSON")

echo "🔍 正在检查去重..."
echo "📝 Paper ID: $PAPER_ID"
if [[ -n "$DOI" ]]; then
    echo "🔗 DOI: $DOI"
fi
echo "📄 PDF Hash: $PDF_HASH"

# 检查 0：全局搜索 PDF 哈希（最可靠的查重方式）
echo "🔎 全局搜索 PDF 哈希..."
for dir in "$PAPERS_DIR"/*/; do
    if [[ -d "$dir" ]]; then
        dir_name=$(basename "$dir")
        # 跳过临时目录
        if [[ "$dir_name" == "temp"* || "$dir_name" == "test"* ]]; then
            continue
        fi
        
        # 检查该目录的 metadata.json
        if [[ -f "$dir/metadata.json" ]]; then
            existing_hash=$(jq -r '.pdf_hash // empty' "$dir/metadata.json" 2>/dev/null)
            if [[ -n "$existing_hash" && "$existing_hash" == "$PDF_HASH" ]]; then
                echo "❌ 发现完全重复的论文（PDF 哈希匹配）："
                echo "   目录：$dir"
                if [[ -f "$dir/feishu_doc_token.txt" ]]; then
                    existing_token=$(cat "$dir/feishu_doc_token.txt")
                    echo "   飞书文档：https://feishu.cn/docx/$existing_token"
                fi
                echo "RESULT=duplicate"
                exit 1
            fi
        fi
    fi
done

# 检查 1：检查 paper_id 目录是否存在
PAPER_DIR="$PAPERS_DIR/$PAPER_ID"
if [[ -d "$PAPER_DIR" ]]; then
    echo "⚠️  发现已存在的论文目录：$PAPER_DIR"
    
    # 检查是否已有飞书文档
    if [[ -f "$PAPER_DIR/feishu_doc_token.txt" ]]; then
        EXISTING_TOKEN=$(cat "$PAPER_DIR/feishu_doc_token.txt")
        echo "📋 已存在飞书文档 token: $EXISTING_TOKEN"
        
        # 检查 PDF 哈希是否相同（尝试多个可能的文件名）
        FOUND_PDF=false
        for pdf_name in "paper.pdf" "paper_official.pdf"; do
            if [[ -f "$PAPER_DIR/$pdf_name" ]]; then
                EXISTING_HASH=$(md5sum "$PAPER_DIR/$pdf_name" | cut -d' ' -f1)
                echo "📄 找到 PDF 文件：$pdf_name (哈希：$EXISTING_HASH)"
                FOUND_PDF=true
                
                if [[ "$EXISTING_HASH" == "$PDF_HASH" ]]; then
                    echo "❌ 完全重复：PDF 文件哈希相同"
                    echo "RESULT=duplicate"
                    exit 1
                else
                    echo "⚠️  相同论文的不同版本（PDF 哈希不同）"
                    echo "RESULT=new_version"
                    exit 0
                fi
            fi
        done
        
        # 如果没找到 PDF 文件，但有 token，说明之前处理过
        if [[ "$FOUND_PDF" == "false" ]]; then
            echo "⚠️  未找到 PDF 文件，但已存在飞书文档"
            echo "💡 建议：手动检查是否重复"
            echo "RESULT=possible_duplicate"
            exit 0
        fi
    fi
fi

# 检查 2：通过 DOI 检查（如果没有 paper_id 目录）
if [[ -n "$DOI" ]]; then
    # DOI 转目录名
    DOI_DIR=$(echo "$DOI" | sed 's/\//_/g')
    DOI_PAPER_DIR="$PAPERS_DIR/$DOI_DIR"
    
    if [[ -d "$DOI_PAPER_DIR" && "$DOI_PAPER_DIR" != "$PAPER_DIR" ]]; then
        echo "⚠️  发现相同 DOI 的论文目录：$DOI_PAPER_DIR"
        
        if [[ -f "$DOI_PAPER_DIR/feishu_doc_token.txt" ]]; then
            EXISTING_TOKEN=$(cat "$DOI_PAPER_DIR/feishu_doc_token.txt")
            echo "📋 已存在飞书文档 token: $EXISTING_TOKEN"
            echo "❌ 完全重复：DOI 相同"
            echo "RESULT=duplicate"
            exit 1
        fi
    fi
fi

# 检查 3：判断是否为补充材料
# 补充材料特征：文件名包含 "supplement", "suppl", "additional", "extended" 等
INPUT_FILE=$(jq -r '.source_file' "$METADATA_JSON")
FILENAME=$(basename "$INPUT_FILE")

if echo "$FILENAME" | grep -qiE '(supplement|suppl|additional|extended|appendix)'; then
    echo "📎 检测到补充材料特征"
    
    # 尝试查找主论文目录（通过 DOI 前缀匹配）
    if [[ -n "$DOI" ]]; then
        # 提取 DOI 前缀（如 10.1038/s41591-025-04176-7 → 10_1038_s41591-025-04176）
        DOI_PREFIX=$(echo "$DOI" | sed 's/-[^-]*$//' | sed 's/\//_/g')
        
        # 在 papers 目录中查找匹配的主论文
        for dir in "$PAPERS_DIR"/*/; do
            dir_name=$(basename "$dir")
            if [[ "$dir_name" == "$DOI_PREFIX"* ]]; then
                echo "📄 找到主论文目录：$dir"
                echo "RESULT=supplement"
                echo "MAIN_PAPER_DIR=$dir"
                exit 2
            fi
        done
    fi
    
    echo "⚠️  补充材料但未找到主论文，作为新论文处理"
fi

# 通过：新论文
echo "✅ 新论文，可以处理"
echo "RESULT=new"
echo "PAPER_DIR=$PAPER_DIR"
exit 0
