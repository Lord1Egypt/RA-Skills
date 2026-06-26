# 部署指南 - Multi-User Privacy

## 本地测试（当前实例）

技能已安装在：`~/.openclaw/skills/multi-user-privacy/`

配置文件已创建：`~/.openclaw/workspace/.user-context.json`

### 测试隐私检查

```bash
# 测试：检测账号 ID 泄露（应该失败）
node ~/.openclaw/skills/multi-user-privacy/privacy-guard.js check \
  "老刘的账号是 ou_b96f5424607baf3a0455b55e0f4a2213" \
  "ou_f5618661cbdcc6f3abb79571db7ec604"

# 测试：正常消息（应该通过）
node ~/.openclaw/skills/multi-user-privacy/privacy-guard.js check \
  "你好，有什么可以帮你的？" \
  "ou_f5618661cbdcc6f3abb79571db7ec604"

# 测试：清理消息
node ~/.openclaw/skills/multi-user-privacy/privacy-guard.js sanitize \
  "老刘的账号是 ou_b96f5424607baf3a0455b55e0f4a2213" \
  "ou_f5618661cbdcc6f3abb79571db7ec604"
```

## 部署到新 OpenClaw 实例

### 方法 1: 通过 ClawHub（推荐，发布后）

```bash
# 1. 安装技能
npx clawhub install multi-user-privacy

# 2. 运行初始化
bash ~/.openclaw/skills/multi-user-privacy/scripts/init-user-context.sh

# 3. 重启
openclaw gateway restart
```

### 方法 2: 手动复制（立即使用）

```bash
# 在目标机器上执行：

# 1. 复制技能文件
scp -r ~/.openclaw/skills/multi-user-privacy user@target:~/.openclaw/skills/

# 2. 复制配置（修改账号 ID 后）
scp ~/.openclaw/workspace/.user-context.json user@target:~/.openclaw/workspace/

# 3. 复制用户记忆（可选）
scp -r ~/.openclaw/workspace/memory/users user@target:~/.openclaw/workspace/memory/

# 4. 重启
openclaw gateway restart
```

### 方法 3: Git 同步（持续更新）

```bash
# 1. 在技能目录初始化 Git
cd ~/.openclaw/skills/multi-user-privacy
git init
git add .
git commit -m "Initial commit"

# 2. 推送到私有仓库
git remote add origin git@github.com:yourname/openclaw-multi-user-privacy.git
git push -u origin main

# 3. 在目标机器克隆
git clone git@github.com:yourname/openclaw-multi-user-privacy.git \
  ~/.openclaw/skills/multi-user-privacy

# 4. 配置并重启
bash ~/.openclaw/skills/multi-user-privacy/scripts/init-user-context.sh
openclaw gateway restart
```

## 配置多个实例

### 场景：家庭 + 公司两台机器

```bash
# 家庭机器 (.user-context.json)
{
  "primaryUser": {
    "id": "ou_home_xxx",
    "name": "老刘",
    "role": "admin"
  },
  "knownUsers": [
    {"id": "ou_family_yyy", "name": "家人", "role": "user"}
  ],
  "privacyMode": "strict"
}

# 公司机器 (.user-context.json)
{
  "primaryUser": {
    "id": "ou_work_xxx",
    "name": "刘总",
    "role": "admin"
  },
  "knownUsers": [
    {"id": "ou_colleague_yyy", "name": "同事", "role": "user"}
  ],
  "privacyMode": "strict"
}
```

**注意**: 不同实例可以有不同的用户配置，互不影响。

## 发布到 ClawHub

```bash
# 1. 登录 ClawHub
npx clawhub login

# 2. 发布技能
cd ~/.openclaw/skills/multi-user-privacy
npx clawhub publish

# 3. 验证发布
npx clawhub search multi-user-privacy
```

## 故障排除

### 问题：脚本无法执行

```bash
# 添加执行权限
chmod +x ~/.openclaw/skills/multi-user-privacy/scripts/*.sh
chmod +x ~/.openclaw/skills/multi-user-privacy/*.js
```

### 问题：配置文件格式错误

```bash
# 验证 JSON 格式
node -e "console.log(JSON.parse(require('fs').readFileSync('.user-context.json')))"
```

### 问题：隐私检查不生效

确保：
1. `.user-context.json` 存在且格式正确
2. `privacy-guard.js` 有执行权限
3. 在发送消息前调用检查函数

## 下一步

- [ ] 集成到 OpenClaw 消息发送流程
- [ ] 添加 Web UI 配置界面
- [ ] 支持更多隐私模式
- [ ] 添加审计日志功能
