#!/bin/bash
# master-agent-workflow-global 发布到ClawdHub脚本
# 版本: 2.0.0

set -e

echo "========================================"
echo "  发布 master-agent-workflow-global 到 ClawdHub"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 技能信息
SKILL_NAME="master-agent-workflow-global"
VERSION="2.0.0"
DESCRIPTION="全局可迁移的主控代理工作流技能"
AUTHOR="小龙"
LICENSE="MIT"

# 目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$SCRIPT_DIR"
BUILD_DIR="$SCRIPT_DIR/build"
DIST_DIR="$SCRIPT_DIR/dist"

# 清理构建目录
clean_build() {
    echo -e "${BLUE}[1/6] 清理构建目录...${NC}"
    rm -rf "$BUILD_DIR" "$DIST_DIR"
    mkdir -p "$BUILD_DIR" "$DIST_DIR"
    echo -e "  ${GREEN}✓${NC} 构建目录已清理"
}

# 验证技能结构
validate_skill() {
    echo -e "${BLUE}[2/6] 验证技能结构...${NC}"
    
    local required_files=(
        "skill.json"
        "SKILL.md"
        ".clawhub/origin.json"
        "install.sh"
    )
    
    local missing_files=()
    for file in "${required_files[@]}"; do
        if [ ! -f "$SKILL_ROOT/$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        echo -e "  ${RED}✗ 缺少必要文件:${NC}"
        for file in "${missing_files[@]}"; do
            echo -e "    - $file"
        done
        return 1
    fi
    
    echo -e "  ${GREEN}✓${NC} 技能结构验证通过"
    
    # 验证skill.json
    if ! jq empty "$SKILL_ROOT/skill.json" 2>/dev/null; then
        echo -e "  ${RED}✗ skill.json 格式错误${NC}"
        return 1
    fi
    
    # 验证版本号
    local skill_version=$(jq -r '.version' "$SKILL_ROOT/skill.json")
    if [ "$skill_version" != "$VERSION" ]; then
        echo -e "  ${YELLOW}⚠ 版本不匹配: skill.json=$skill_version, 脚本=$VERSION${NC}"
    fi
    
    echo -e "  ${GREEN}✓${NC} 配置文件验证通过"
}

# 创建发布包
create_package() {
    echo -e "${BLUE}[3/6] 创建发布包...${NC}"
    
    local package_name="$SKILL_NAME-v$VERSION"
    local tar_file="$DIST_DIR/$package_name.tar.gz"
    
    # 复制文件到构建目录
    echo -e "  复制文件到构建目录..."
    cp -r "$SKILL_ROOT"/* "$BUILD_DIR/" 2>/dev/null || true
    
    # 移除不需要的文件
    echo -e "  清理不需要的文件..."
    rm -f "$BUILD_DIR"/*.bat 2>/dev/null || true
    rm -f "$BUILD_DIR"/*.tmp 2>/dev/null || true
    rm -f "$BUILD_DIR"/*.log 2>/dev/null || true
    
    # 创建包
    echo -e "  创建压缩包..."
    tar -czf "$tar_file" \
        --exclude=".git" \
        --exclude="node_modules" \
        --exclude="*.tmp" \
        --exclude="*.log" \
        --exclude="test-*" \
        -C "$BUILD_DIR" .
    
    # 计算大小和校验和
    local size=$(du -h "$tar_file" | cut -f1)
    local checksum=$(sha256sum "$tar_file" | cut -d' ' -f1)
    
    echo -e "  ${GREEN}✓${NC} 发布包创建完成"
    echo -e "    文件: $(basename "$tar_file")"
    echo -e "    大小: $size"
    echo -e "    SHA256: $checksum"
    
    # 保存校验和
    echo "$checksum  $(basename "$tar_file")" > "$DIST_DIR/SHA256SUMS"
    
    # 创建发布信息
    cat > "$DIST_DIR/release-info.json" << EOF
{
  "name": "$SKILL_NAME",
  "version": "$VERSION",
  "description": "$DESCRIPTION",
  "author": "$AUTHOR",
  "license": "$LICENSE",
  "package": "$(basename "$tar_file")",
  "size": "$size",
  "checksum": "$checksum",
  "build_time": "$(date -Iseconds)",
  "files": [
    "$(basename "$tar_file")",
    "SHA256SUMS",
    "release-info.json"
  ]
}
EOF
}

# 更新元数据
update_metadata() {
    echo -e "${BLUE}[4/6] 更新元数据...${NC}"
    
    local tar_file="$DIST_DIR/$SKILL_NAME-v$VERSION.tar.gz"
    local checksum=$(sha256sum "$tar_file" | cut -d' ' -f1)
    
    # 更新origin.json中的校验和
    if [ -f "$SKILL_ROOT/.clawhub/origin.json" ]; then
        jq --arg checksum "sha256:$checksum" \
           '.installation.checksum = $checksum' \
           "$SKILL_ROOT/.clawhub/origin.json" > "$SKILL_ROOT/.clawhub/origin.json.tmp"
        mv "$SKILL_ROOT/.clawhub/origin.json.tmp" "$SKILL_ROOT/.clawhub/origin.json"
        echo -e "  ${GREEN}✓${NC} 更新origin.json校验和"
    fi
    
    # 创建版本文件
    cat > "$DIST_DIR/VERSION" << EOF
$SKILL_NAME v$VERSION
Build: $(date)
Checksum: $checksum
EOF
    
    echo -e "  ${GREEN}✓${NC} 元数据更新完成"
}

# 生成发布说明
generate_release_notes() {
    echo -e "${BLUE}[5/6] 生成发布说明...${NC}"
    
    cat > "$DIST_DIR/CHANGELOG.md" << EOF
# master-agent-workflow-global 变更日志

## v2.0.0 (2026-03-27)

### 🎉 新特性
- **全局可迁移**: 支持一键安装和配置迁移
- **模板系统**: 预定义文件处理、API调用、数据处理模板
- **配置管理**: 外部JSON配置，支持环境变量覆盖
- **跨平台兼容**: Windows/Linux/macOS全支持
- **版本管理**: 语义化版本，支持升级和回滚
- **钩子集成**: 与OpenClaw深度集成，自动触发

### 🔄 迁移功能
- 导出/导入配置和模板
- 完整备份和恢复功能
- 兼容v1.0.0配置格式

### 📦 安装方式
1. 使用安装脚本: \`./install.sh\`
2. 通过ClawdHub: \`clawdhub install master-agent-workflow-global\`
3. 手动安装: 复制到全局技能目录

### 🚀 使用示例
\`\`\`bash
# 快捷命令
maw "处理任务"

# 使用模板
maw "批量处理" --template file_processing

# 配置管理
maw configure save my-config --max-workers 10
\`\`\`

### 📋 系统要求
- OpenClaw >= 1.0.0
- Node.js >= 18.0.0
- jq (用于迁移工具)

### 🔧 维护信息
- **作者**: 小龙
- **许可证**: MIT
- **仓库**: https://github.com/xiaolong-ai/master-agent-workflow
- **问题反馈**: GitHub Issues 或 ClawdHub反馈

---

## v1.0.0 (2026-03-25)
- 初始版本，基本的主控代理工作流功能
- 并行任务调度和错误处理
- 本地使用版本
EOF
    
    echo -e "  ${GREEN}✓${NC} 发布说明生成完成"
}

# 显示发布信息
show_release_info() {
    echo -e "${BLUE}[6/6] 发布信息汇总...${NC}"
    echo ""
    echo -e "${GREEN}✅ 发布准备完成！${NC}"
    echo ""
    echo -e "${YELLOW}📦 发布包信息:${NC}"
    echo -e "  名称: $SKILL_NAME-v$VERSION.tar.gz"
    echo -e "  位置: $DIST_DIR/"
    echo -e "  大小: $(du -h "$DIST_DIR/$SKILL_NAME-v$VERSION.tar.gz" | cut -f1)"
    echo ""
    echo -e "${YELLOW}📋 包含文件:${NC}"
    ls -la "$DIST_DIR/" | tail -n +2 | awk '{print "  " $9 " (" $5 " bytes)"}'
    echo ""
    echo -e "${YELLOW}🚀 发布到ClawdHub:${NC}"
    cat << EOF
  使用以下命令发布到ClawdHub:

  clawdhub publish \\
    --name "$SKILL_NAME" \\
    --version "$VERSION" \\
    --description "$DESCRIPTION" \\
    --category "workflow" \\
    --tags "agent,parallel,scheduling,migration" \\
    --author "$AUTHOR" \\
    --license "$LICENSE" \\
    "$DIST_DIR/$SKILL_NAME-v$VERSION.tar.gz"

  或者使用Web界面上传:
  1. 访问 https://clawhub.com
  2. 登录您的账户
  3. 点击"发布技能"
  4. 上传 $DIST_DIR/$SKILL_NAME-v$VERSION.tar.gz
  5. 填写技能信息
  6. 点击发布
EOF
    echo ""
    echo -e "${YELLOW}📄 发布检查清单:${NC}"
    echo -e "  [ ] 测试安装脚本"
    echo -e "  [ ] 验证技能功能"
    echo -e "  [ ] 更新文档链接"
    echo -e "  [ ] 创建GitHub Release"
    echo -e "  [ ] 发布到ClawdHub"
    echo ""
    echo -e "${GREEN}🎉 技能已准备好分享给其他人！${NC}"
}

# 主函数
main() {
    echo ""
    echo -e "${BLUE}开始发布流程...${NC}"
    echo ""
    
    # 检查依赖
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}错误: 需要 jq 命令${NC}"
        echo "请安装: brew install jq 或 apt-get install jq"
        exit 1
    fi
    
    if ! command -v tar &> /dev/null; then
        echo -e "${RED}错误: 需要 tar 命令${NC}"
        exit 1
    fi
    
    # 执行发布步骤
    clean_build
    validate_skill || exit 1
    create_package
    update_metadata
    generate_release_notes
    show_release_info
}

# 运行主函数
main "$@"