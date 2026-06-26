# 无浏览器环境登录 ClawHub 解决方案

## 🎯 问题
在无浏览器环境的Linux服务器上无法使用 `clawhub login` 的默认浏览器流程。

## ✅ 解决方案

### 方案1: 使用 API Token 登录 (推荐)

#### 步骤1: 在浏览器环境获取 Token
在有浏览器的环境中（本地电脑、其他服务器）:

1. 访问 https://clawhub.com
2. 登录你的账号
3. 进入 **Settings** → **API Tokens**
4. 点击 **Generate New Token**
5. 复制生成的 token (格式: `ch_xxxxxxxxxxxx`)

#### 步骤2: 在无浏览器环境使用 Token 登录
```bash
clawhub login --token YOUR_API_TOKEN --no-browser
```

**示例**:
```bash
clawhub login --token ch_abc123def456 --no-browser
```

#### 步骤3: 验证登录
```bash
clawhub whoami
```

### 方案2: 使用环境变量

设置环境变量:
```bash
export CLAWHUB_TOKEN="ch_abc123def456"
```

然后使用:
```bash
clawhub login --token $CLAWHUB_TOKEN --no-browser
```

### 方案3: 配置文件方式

创建配置文件:
```bash
mkdir -p ~/.config/clawhub
echo "ch_abc123def456" > ~/.config/clawhub/token
chmod 600 ~/.config/clawhub/token
```

## 📋 完整发布流程（无浏览器环境）

### 1. 获取 Token
在有浏览器的环境中完成:
- 访问 https://clawhub.com/settings/tokens
- 生成 Token: `ch_xxxxxxxxxxxx`

### 2. 登录
```bash
clawhub login --token ch_your_token_here --no-browser
```

### 3. 验证
```bash
clawhub whoami
# 输出: Logged in as: your-username
```

### 4. 发布 Skill
```bash
cd /home/lutao/projects/pharma-ai-skill
clawhub publish . \
  --slug pharma-ai \
  --name "PharmaAI" \
  --version 1.0.0 \
  --changelog "Initial release"
```

## 🔧 常见问题

### Q: 如何获取 Token?
**A**: 必须在有浏览器的环境中访问 https://clawhub.com/settings/tokens 生成。

### Q: Token 有效期多久?
**A**: 默认长期有效，可在设置中撤销。

### Q: Token 泄露怎么办?
**A**: 立即在 https://clawhub.com/settings/tokens 撤销并重新生成。

### Q: 没有浏览器环境可用?
**A**: 可以使用手机浏览器、本地电脑浏览器，或临时使用SSH隧道。

## 🌐 临时浏览器访问方案

如果完全无法访问浏览器，可以使用 SSH 隧道:

```bash
# 在本地电脑（有浏览器）执行
ssh -L 8080:localhost:8080 your-server-ip

# 然后在服务器上启动临时 Web 服务
# 使用 Python 简单 HTTP 服务器或其他工具
```

或者使用文本浏览器（部分OAuth支持）:
```bash
# 安装 lynx 或 w3m
sudo apt-get install lynx

# 尝试使用文本浏览器
lynx https://clawhub.com
```

## 📞 获取帮助

如果以上方法都不可行:
1. 联系 ClawHub 支持: support@clawhub.com
2. 查看文档: https://docs.clawhub.com
3. 社区求助: https://discord.gg/clawd

---

**推荐做法**: 在本地电脑获取 Token，然后在服务器上使用 `--token` 参数登录。