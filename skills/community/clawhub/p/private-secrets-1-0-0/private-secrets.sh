#!/bin/bash

# Private Secrets Skill - Manage private information

SECRETS_FILE="/workspace/skills/private-secrets-1.0.0/secrets.json"

# Initialize file if not exists
if [ ! -f "$SECRETS_FILE" ]; then
    echo '{}' > "$SECRETS_FILE"
fi

# Parse command
COMMAND="$1"
NAME="$2"
VALUE="$3"

case "$COMMAND" in
    "add")
        if [ -z "$NAME" ] || [ -z "$VALUE" ]; then
            echo "用法: private-secrets add <名称> <内容>"
            exit 1
        fi
        # Use node to update JSON
        node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('$SECRETS_FILE', 'utf8'));
data['$NAME'] = '$VALUE';
fs.writeFileSync('$SECRETS_FILE', JSON.stringify(data, null, 2));
console.log('已添加: $NAME');
"
        ;;
    "list")
        node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('$SECRETS_FILE', 'utf8'));
const keys = Object.keys(data);
if (keys.length === 0) {
    console.log('暂无存储的私密信息');
} else {
    console.log('已存储的信息:');
    keys.forEach(k => console.log('  - ' + k));
}
"
        ;;
    "get")
        if [ -z "$NAME" ]; then
            echo "用法: private-secrets get <名称>"
            exit 1
        fi
        node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('$SECRETS_FILE', 'utf8'));
if (data['$NAME']) {
    console.log(data['$NAME']);
} else {
    console.log('未找到: $NAME');
    process.exit(1);
}
"
        ;;
    *)
        echo "Private Secrets Skill"
        echo ""
        echo "用法:"
        echo "  private-secrets add <名称> <内容>  - 添加私密信息"
        echo "  private-secrets list               - 列出所有名称"
        echo "  private-secrets get <名称>         - 查看具体内容"
        ;;
esac
