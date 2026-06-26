# OBS 配置指南
# OBS Configuration Guide

## 当前状态 | Current Status

- ✅ 技能已安装 | Skill installed: `/root/.openclaw/workspace-obs/skills/obs`
- ❌ 未配置凭证 | Credentials not configured
- ❌ osc 工具未安装 | osc tool not installed

---

## 配置方法 | Configuration Methods

### 方法 1: 使用 oscrc 配置文件（推荐）| Method 1: Using oscrc Config File (Recommended)

编辑配置文件 | Edit config file: `~/.config/osc/oscrc`

```ini
[general]
apiurl = https://api.opensuse.org

[https://api.opensuse.org]
user = YOUR_USERNAME
pass = YOUR_API_TOKEN
```

**获取 API Token 步骤 | Get API Token Steps:**

1. 登录 OBS | Login to OBS: https://build.opensuse.org
2. 点击右上角用户名 | Click your username (top right)
3. 选择 "Settings" | Select "Settings"
4. 点击 "API Tokens" 标签 | Click "API Tokens" tab
5. 点击 "Create new token" | Click "Create new token"
6. 输入描述（如 "OBS CLI"）| Enter description (e.g., "OBS CLI")
7. 点击 "Create" | Click "Create"
8. **复制 Token（只显示一次！）** | **Copy token (shown only once!)**

---

### 方法 2: 使用环境变量 | Method 2: Using Environment Variables

添加到 `~/.bashrc` 或 `~/.zshrc`:

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export OBS_APIURL=https://api.opensuse.org
export OBS_USERNAME=your_username
export OBS_TOKEN=your_api_token
```

然后执行 | Then run:
```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

---

## 快速配置脚本 | Quick Setup Script

运行以下命令快速配置 | Run these commands to quickly configure:

```bash
# 创建配置目录
mkdir -p ~/.config/osc

# 创建配置文件（替换 YOUR_USERNAME 和 YOUR_API_TOKEN）
cat > ~/.config/osc/oscrc << 'EOF'
[general]
apiurl = https://api.opensuse.org

[https://api.opensuse.org]
user = YOUR_USERNAME
pass = YOUR_API_TOKEN
EOF

# 设置文件权限（仅自己可读）
chmod 600 ~/.config/osc/oscrc
```

---

## 测试配置 | Test Configuration

配置完成后，运行以下命令测试 | After configuration, run this to test:

```bash
# 使用 obs 测试
obs auth test

# 或使用 API 库测试
source /root/.openclaw/workspace-obs/skills/obs/references/obs-lib.sh
obs_auth_test
```

预期输出 | Expected output:
```
✓ Authentication successful | 认证成功
```

---

## 验证安装 | Verify Installation

```bash
# 查看帮助
obs --help

# 查看项目帮助
obs project --help

# 查看包帮助
obs package --help

# 查看构建帮助
obs build --help

# 查看请求帮助
obs request --help
```

---

## 常用命令速查 | Quick Command Reference

### 项目操作 | Project Operations
```bash
# 创建项目
obs project create --name "home:username:project" --title "My Project" --description "Description"

# 获取项目信息
obs project get --name "home:username:project"

# 列出项目下的包
obs project list --name "home:username:project"
```

### 包操作 | Package Operations
```bash
# 创建包
obs package create --project "home:username:project" --package "mypackage"

# 下载包源码
obs package checkout --project "home:username:project" --package "mypackage" --output "./mypackage"

# 列出包文件
obs package list --project "home:username:project" --package "mypackage"
```

### 文件操作 | File Operations
```bash
# 上传文件
obs file upload --project "home:username:project" --package "mypackage" --file "./mypackage.spec" --message "Initial commit"

# 读取文件
obs file get --project "home:username:project" --package "mypackage" --file "mypackage.spec"

# 列出文件
obs file list --project "home:username:project" --package "mypackage"
```

### 构建操作 | Build Operations
```bash
# 查看构建状态
obs build status --project "home:username:project" --package "mypackage"

# 触发重建
obs build rebuild --project "home:username:project" --package "mypackage" --repository "openSUSE_Tumbleweed" --arch "x86_64"

# 获取构建日志
obs build log --project "home:username:project" --package "mypackage" --repository "openSUSE_Tumbleweed" --arch "x86_64"
```

### 提交请求 | Submit Requests
```bash
# 创建提交请求
obs request create --source-project "home:username:project" --source-package "mypackage" --target-project "openSUSE:Factory" --target-package "mypackage" --description "Update"

# 查看请求
obs request get --id 123456

# 列出请求
obs request list --states "new,review"

# 接受/拒绝请求
obs request accept --id 123456 --message "Looks good"
obs request reject --id 123456 --message "Needs work"
```

---

## 故障排除 | Troubleshooting

### 问题：认证失败 | Issue: Authentication Failed

**检查凭证 | Check Credentials:**
```bash
obs auth status
```

**重新配置 | Reconfigure:**
```bash
# 检查 oscrc 文件
cat ~/.config/osc/oscrc

# 检查环境变量
env | grep OBS_
```

### 问题：命令未找到 | Issue: Command Not Found

**添加脚本到 PATH | Add script to PATH:**
```bash
export PATH="$PATH:/root/.openclaw/workspace-obs/skills/obs/scripts"
```

或创建符号链接 | Or create symlink:
```bash
ln -s /root/.openclaw/workspace-obs/skills/obs/scripts/obs /usr/local/bin/obs
```

### 问题：权限错误 | Issue: Permission Error

**确保配置文件权限正确 | Ensure config file permissions:**
```bash
chmod 600 ~/.config/osc/oscrc
```

---

## 下一步 | Next Steps

1. **配置凭证** - 按照上述方法配置 OBS 凭证
   **Configure Credentials** - Follow the methods above to configure OBS credentials

2. **测试连接** - 运行 `obs auth test` 测试
   **Test Connection** - Run `obs auth test`

3. **开始使用** - 参考上面的常用命令速查
   **Start Using** - Refer to the quick command reference above

---

## 相关资源 | Resources

- **OBS Web UI**: https://build.opensuse.org
- **OBS API Docs**: https://api.opensuse.org/apidocs/index
- **openSUSE Packaging Guide**: https://en.opensuse.org/openSUSE:Packaging_guidelines
- **osc Documentation**: https://openbuildservice.org/help/manuals/obs-user-guide/cha.obs.osc.html

---

**配置完成时间 | Configured:** 等待用户配置 | Waiting for user configuration  
**技能版本 | Skill Version:** 1.0.0
