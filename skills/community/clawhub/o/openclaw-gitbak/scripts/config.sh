#!/bin/bash
# OpenClaw GitBak 配置文件
# 格式: 键名="本地路径:仓库名:描述"
# 添加新仓库只需在这里加一行

# ========== Git 远程仓库配置 ==========
# 可切换到 GitHub: github.com, GitLab, 或其他 Git 托管服务
GIT_HOST="gitee.com"
GIT_ORG="burnlife"
GIT_BRANCH="master"  # 分支名: master 或 main

# 构建完整远程仓库 URL
get_remote_url() {
    local repo="$1"
    echo "git@${GIT_HOST}:${GIT_ORG}/${repo}.git"
}
# ======================================

declare -A BACKUP_ITEMS
BACKUP_ITEMS["cfg"]="~/.openclaw:openclaw_bak1_cfg:配置文件"
BACKUP_ITEMS["workspace"]="~/.openclaw/workspace:openclaw_bak1_workspace:工作空间"
BACKUP_ITEMS["workspace-coder"]="~/.openclaw/workspace-coder:openclaw_bak1_workspace_coder:代码工作空间"

# 获取所有可用备份项的键列表
get_backup_keys() {
    echo "${!BACKUP_ITEMS[@]}" | tr ' ' '\n' | sort
}

# 通过键获取配置信息 (返回: 路径:仓库名:描述)
get_backup_item() {
    local key="$1"
    echo "${BACKUP_ITEMS[$key]}"
}