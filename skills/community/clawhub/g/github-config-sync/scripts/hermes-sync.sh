#!/bin/bash
# Hermes GitHub 同步工具
# 用法: hermes-sync [push|pull]

HERMES_DIR="$HOME/.hermes"
SYNC_DIR="$HOME/hermes-sync"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 检查依赖
check_deps() {
    if ! command -v git &> /dev/null; then
        echo -e "${RED}错误: 请先安装Git${NC}"
        exit 1
    fi
    
    if [ ! -d "$SYNC_DIR/.git" ]; then
        echo -e "${RED}错误: 请先克隆仓库${NC}"
        echo "运行: git clone https://github.com/zhangwenhao66/hermes-config.git ~/hermes-sync"
        exit 1
    fi
}

# 模式A：上传（Mac → GitHub）
push_to_github() {
    echo -e "${GREEN}=== 上传配置到GitHub ===${NC}"
    
    cd "$SYNC_DIR"
    git pull
    
    echo "复制配置到同步目录..."
    cp "$HERMES_DIR/config.yaml" .
    cp -r "$HERMES_DIR/memories" .
    cp -r "$HERMES_DIR/skills" .
    
    # 可选文件
    [ -f "$HERMES_DIR/.env" ] && cp "$HERMES_DIR/.env" .
    [ -f "$HERMES_DIR/auth.json" ] && cp "$HERMES_DIR/auth.json" .
    [ -d "$HERMES_DIR/sessions" ] && cp -r "$HERMES_DIR/sessions" .
    
    echo "提交变更..."
    git add .
    
    if git diff --staged --quiet; then
        echo "没有需要上传的变更"
        return
    fi
    
    git commit -m "更新配置 $(date '+%Y-%m-%d %H:%M')"
    git push
    
    echo -e "${GREEN}✅ 上传完成！${NC}"
}

# 模式B：下载（GitHub → Windows）
pull_from_github() {
    echo -e "${GREEN}=== 从GitHub下载配置 ===${NC}"
    
    cd "$SYNC_DIR"
    git pull
    
    echo "复制到Hermes目录..."
    cp config.yaml "$HERMES_DIR/config.yaml"
    cp -r memories/* "$HERMES_DIR/memories/" 2>/dev/null || true
    cp -r skills/* "$HERMES_DIR/skills/" 2>/dev/null || true
    
    # 可选文件
    [ -f ".env" ] && cp .env "$HERMES_DIR/.env"
    [ -f "auth.json" ] && cp auth.json "$HERMES_DIR/auth.json"
    [ -d "sessions" ] && cp -r sessions/* "$HERMES_DIR/sessions/" 2>/dev/null || true
    
    echo -e "${GREEN}✅ 下载完成！${NC}"
    echo ""
    echo "运行 'hermes restart' 重启Hermes"
}

# 主命令
case "$1" in
    push)
        check_deps
        push_to_github
        ;;
    pull)
        check_deps
        pull_from_github
        ;;
    *)
        echo "Hermes GitHub 同步工具"
        echo ""
        echo "用法:"
        echo "  hermes-sync push   # 上传到GitHub（Mac上用）"
        echo "  hermes-sync pull   # 从GitHub下载（Windows上用）"
        echo ""
        echo "第一次使用:"
        echo "  git clone https://github.com/zhangwenhao66/hermes-config.git ~/hermes-sync"
        ;;
esac