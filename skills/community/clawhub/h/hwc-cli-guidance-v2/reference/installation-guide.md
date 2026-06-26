# KooCLI 安装指南

## 安装前准备

### 系统要求

- **操作系统**: Windows / macOS / Linux
- **Python 版本**: 3.8 或更高版本（如使用 pip 安装）
- **网络**: 需要访问华为云服务

### 获取访问密钥

1. 登录 [华为云控制台](https://console.huaweicloud.com/)
2. 点击右上角用户名，选择"我的凭证"
3. 在"访问密钥"页面，点击"新增访问密钥"
4. 下载 `credentials.csv` 文件，保存 Access Key ID 和 Secret Access Key

---

## 安装方法

### 方法一：使用 pip 安装（推荐）

```bash
pip install huaweicloudsdkcore
pip install huaweicloudsdkkoocli
```

**验证安装**

```bash
hcloud --version
```

---

### 方法二：使用 curl 安装（Linux/macOS）

```bash
# 下载安装包
curl -LO https://dl.koo.cloud/cli/latest/huaweicloud-cli-linux-amd64.tar.gz

# 解压
tar -xzvf huaweicloud-cli-linux-amd64.tar.gz

# 移动到系统路径
sudo mv huaweicloud-cli-linux-amd64 /usr/local/bin/hcloud

# 添加执行权限
sudo chmod +x /usr/local/bin/hcloud

# 验证安装
hcloud --version
```

---

### 方法三：使用 PowerShell 安装（Windows）

```powershell
# 下载安装包
Invoke-WebRequest -Uri "https://dl.koo.cloud/cli/latest/huaweicloud-cli-windows-amd64.zip" -OutFile "huaweicloud-cli-windows-amd64.zip"

# 解压
Expand-Archive -Path "huaweicloud-cli-windows-amd64.zip" -DestinationPath .

# 添加到环境变量
$env:Path += ";$pwd\huaweicloud-cli-windows-amd64"

# 验证安装
hcloud --version
```

---

### 方法四：使用 Homebrew 安装（macOS）

```bash
# 添加华为云 tap
brew tap huaweicloud/homebrew-tap

# 安装
brew install huaweicloud-cli

# 验证安装
hcloud --version
```

---

## 配置认证信息

### 初始化配置

```bash
hcloud configure init
```

按提示输入以下信息：

```
Access Key ID [required]: <your-access-key-id>
Secret Access Key [required]: <your-secret-access-key>
Region [required]: cn-north-4
```

### 查看配置

```bash
hcloud configure list
```

输出示例：

```
CURRENT  NAME    REGION
*        default cn-north-4
```

### 切换配置

```bash
hcloud configure set --profile=prod
```

### 删除配置

```bash
hcloud configure delete --profile=test
```

---

## 验证安装

### 测试命令

```bash
# 查询云服务器列表
hcloud ecs list-servers

# 查询桶列表
hcloud obs list-buckets
```

### 查看帮助

```bash
hcloud --help
hcloud ecs --help
hcloud ecs list-servers --help
```

---

## 卸载

### pip 卸载

```bash
pip uninstall huaweicloudsdkcore
pip uninstall huaweicloudsdkkoocli
```

### 手动卸载

```bash
# Linux/macOS
sudo rm /usr/local/bin/hcloud

# Windows
Remove-Item -Path "huaweicloud-cli-windows-amd64" -Recurse -Force
```

---

## 常见问题

### Q1: pip 安装失败

**A**: 检查 Python 版本和网络连接，尝试使用国内镜像源：

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple huaweicloudsdkkoocli
```

---

### Q2: 命令未找到

**A**: 检查环境变量配置，确保 KooCLI 安装路径已添加到 PATH。

---

### Q3: 认证失败

**A**: 检查 AK/SK 是否正确，确认账户权限和区域配置。

---

## 参考文档

- [KooCLI 官方文档](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [华为云服务文档](https://support.huaweicloud.com/)

---

🎯
