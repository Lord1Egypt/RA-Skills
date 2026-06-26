#!/bin/bash
# GitHub 发布脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 配置
REPO_NAME="multi-user-privacy"
VERSION="0.8.0"
GITHUB_USERNAME=""

echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}🚀 GitHub 发布脚本${NC}"
echo -e "${BLUE}==================================${NC}"
echo ""

# 步骤 1：检查 Git 配置
echo -e "${YELLOW}[1/6] 检查 Git 配置...${NC}"
if ! git --version &> /dev/null; then
    echo -e "${RED}❌ Git 未安装，请先安装 Git${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Git 已安装${NC}"
echo ""

# 步骤 2：初始化 Git 仓库
echo -e "${YELLOW}[2/6] 初始化 Git 仓库...${NC}"
if [ ! -d ".git" ]; then
    git init
    echo -e "${GREEN}✅ Git 仓库已初始化${NC}"
else
    echo -e "${GREEN}✅ Git 仓库已存在${NC}"
fi
echo ""

# 步骤 3：添加文件
echo -e "${YELLOW}[3/6] 添加文件...${NC}"
git add .
echo -e "${GREEN}✅ 文件已添加${NC}"
echo ""

# 步骤 4：首次提交
echo -e "${YELLOW}[4/6] 提交代码...${NC}"
if git rev-parse HEAD &> /dev/null; then
    echo -e "${YELLOW}⚠️  已有提交，跳过首次提交${NC}"
else
    git commit -m "Initial commit: Multi-User Privacy v${VERSION}"
    echo -e "${GREEN}✅ 首次提交完成${NC}"
fi
echo ""

# 步骤 5：关联远程仓库
echo -e "${YELLOW}[5/6] 关联远程仓库...${NC}"
echo -e "请输入你的 GitHub 用户名："
read -p "> " GITHUB_USERNAME

if git remote | grep -q "^origin$"; then
    echo -e "${YELLOW}⚠️  远程仓库已关联${NC}"
    git remote -v
else
    git remote add origin https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git
    echo -e "${GREEN}✅ 远程仓库已关联${NC}"
fi
echo ""

# 步骤 6：推送到 GitHub
echo -e "${YELLOW}[6/6] 推送到 GitHub...${NC}"
git branch -M main

if git push -u origin main; then
    echo -e "${GREEN}✅ 推送成功${NC}"
    echo ""
    echo -e "${BLUE}==================================${NC}"
    echo -e "${GREEN}🎉 发布成功！${NC}"
    echo -e "${BLUE}==================================${NC}"
    echo ""
    echo -e "仓库地址：${GREEN}https://github.com/${GITHUB_USERNAME}/${REPO_NAME}${NC}"
    echo ""
    echo -e "${YELLOW}下一步:${NC}"
    echo "1. 在 GitHub 创建 Release"
    echo "2. 添加发布说明"
    echo "3. 推广项目"
    echo ""
else
    echo -e "${RED}❌ 推送失败${NC}"
    echo -e "${YELLOW}可能原因:${NC}"
    echo "1. 仓库已存在（需要删除后重试）"
    echo "2. 认证失败（需要配置 SSH 或 Token）"
    echo "3. 网络问题"
    exit 1
fi
