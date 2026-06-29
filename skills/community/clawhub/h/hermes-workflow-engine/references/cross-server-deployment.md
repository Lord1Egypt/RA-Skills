# 跨服务器部署workflow-engine

## 部署到OpenClaw (龙虾)

### 步骤1：传输SKILL.md
```bash
ssh root@REMOTE_IP "mkdir -p /root/.openclaw/workspace/skills/workflow-engine"
scp /path/to/workflow-engine/SKILL.md root@REMOTE_IP:/root/.openclaw/workspace/skills/workflow-engine/SKILL.md
```

### 步骤2：适配路径
```bash
# 修改author
ssh root@REMOTE_IP "sed -i 's/author: 小狗/author: 老狗/' /root/.openclaw/workspace/skills/workflow-engine/SKILL.md"

# 修改路径（OpenClaw用.openclaw/workspace/）
ssh root@REMOTE_IP "sed -i 's|~/.hermes/workflow-engine/|~/.openclaw/workspace/workflow-engine/|g' /root/.openclaw/workspace/skills/workflow-engine/SKILL.md"
```

### 步骤3：传输代码
```bash
# 打包
cd ~/.hermes/workflow-engine
tar czf /tmp/workflow-engine-code.tar.gz --exclude='runs/*' --exclude='_community/*' --exclude='workflows/*' *.py *.md examples/

# 传输
scp /tmp/workflow-engine-code.tar.gz root@REMOTE_IP:/tmp/
ssh root@REMOTE_IP "cd /root/.openclaw/workspace/workflow-engine && tar xzf /tmp/workflow-engine-code.tar.gz"
```

### 步骤4：修改run.py路径
```bash
# run.py中hardcoded了~/.hermes路径，需要改为~/.openclaw/workspace
ssh root@REMOTE_IP "sed -i \"s|Path.home() / '.hermes' / 'workflow-engine'|Path.home() / '.openclaw' / 'workspace' / 'workflow-engine'|g\" /root/.openclaw/workspace/workflow-engine/run.py"
```

### 步骤5：验证
```bash
ssh root@REMOTE_IP "cd /root/.openclaw/workspace/workflow-engine && python3 run.py list"
ssh root@REMOTE_IP "cd /root/.openclaw/workspace/workflow-engine && python3 run.py validate examples/ai-news-daily.yaml"
```

## 注意事项

1. **路径适配**：run.py中hardcoded了`~/.hermes/workflow-engine`路径，必须改为目标系统的路径
2. **author字段**：SKILL.md中的author需要改为对应agent的名字
3. **排除运行时文件**：runs/、_community/、workflows/是运行时生成的，不需要传输
4. **Python版本**：确认目标服务器有python3

## ClawHub发布

```bash
# 从另一台服务器导入token
scp root@SOURCE_IP:~/.config/clawhub/config.json ~/.config/clawhub/config.json

# 验证
clawhub whoami

# 发布（slug必须唯一）
clawhub publish . --slug hermes-workflow-engine --name "Hermes Workflow Engine" --version 3.0.0
```

## GitHub SSH Key复制

```bash
# 从另一台服务器复制私钥
scp root@SOURCE_IP:~/.ssh/id_ed25519 ~/.ssh/id_ed25519_backup

# 配置SSH使用该私钥
cat >> ~/.ssh/config << 'EOF'
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_backup
    IdentitiesOnly yes
EOF

# 测试
ssh -T git@github.com
```
