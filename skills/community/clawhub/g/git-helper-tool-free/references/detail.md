# 详细参考 - git-helper-tool-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (bash)

```bash
setup_git_config() {
    echo "=== Git配置向导 ==="

    read -p "姓名: " name
    read -p "邮箱: " email
    git config --global user.name "$name"
    git config --global user.email "$email"

    git config --global init.defaultBranch main

    git config --global pull.rebase true
    git config --global push.default current
    git config --global push.autoSetupRemote true

    git config --global alias.st "status -sb"
    git config --global alias.co checkout
    git config --global alias.sw switch
    git config --global alias.br branch
    git config --global alias.ci commit
    git config --global alias.lg "log --graph --oneline --all -20"

    echo "Git配置完成"
    git config --list --global
}

generate_gitignore() {
    local type="${1:-node}"
    echo "=== 生成 .gitignore ($type) ==="

    case "$type" in
        node)
            cat > .gitignore << 'EOF'
node_modules/
dist/
.env
.env.local
*.log
.vscode/
.DS_Store
coverage/
.nyc_output/
EOF
            ;;
        python)
            cat > .gitignore << 'EOF'
__pycache__/
*.pyc
venv/
.venv/
*.egg-info/
dist/
build/
.env
.pytest_cache/
.mypy_cache/
EOF
            ;;
        java)
            cat > .gitignore << 'EOF'
target/
*.class
*.jar
*.war
.idea/
*.iml
.gradle/
build/
EOF
            ;;
        *)
            cat > .gitignore << 'EOF'
*.log
*.tmp
*.bak
.DS_Store
Thumbs.db
.vscode/
.idea/
EOF
            ;;
    esac
    echo ".gitignore 已生成"
}
```

## 代码示例 (bash)

```bash
#!/bin/bash
echo "=== Git误操作恢复 ==="

echo "选择恢复场景:"
echo "1. 撤销最近的提交(保留变更)"
echo "2. 撤销最近的提交(丢弃变更)"
echo "3. 恢复误删除的分支"
echo "4. 恢复误reset的提交"
echo "5. 撤销已推送的提交"
read -p "选择(1-5): " choice

case $choice in
    1)
        echo "撤销提交,保留变更..."
        git reset --soft HEAD~1
        echo "变更已保留在工作区"
        ;;
    2)
        echo "撤销提交,丢弃变更..."
        read -p "确认丢弃所有变更? (y/N) " confirm
        [ "$confirm" = "y" ] && git reset --hard HEAD~1
        ;;
    3)
        echo "查找误删除的分支..."
        git reflog | grep "checkout\|branch"
        echo "找到SHA后: git checkout -b branch-name <sha>"
        ;;
    4)
        echo "查找误reset的提交..."
        git reflog | grep "reset"
        echo "找到SHA后: git reset --hard <sha>"
        ;;
    5)
        echo "撤销已推送的提交(安全方式)..."
        echo "1. git revert <commit-sha>"
        echo "2. git push origin <branch>"
        ;;
esac
```

