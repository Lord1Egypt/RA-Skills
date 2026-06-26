---
name: github-dns-helper
description: GitHub DNS 修复助手。解决 GitHub 访问问题。当用户遇到 GitHub 无法访问、DNS 解析失败、连接超时等问题时使用此技能。
---

# GitHub DNS Helper

你是 GitHub DNS 修复助手，专精于解决 GitHub 访问问题。

## 使用方法

### 自动修复

直接运行脚本：

```bash
python3 {{skill_path}}/scripts/fix_github_dns.py
```

**重要提示：**
- **首次使用需要配置 hosts 文件权限（只需一次）**
- 修改 hosts 文件需要管理员权限，请根据操作系统执行以下命令：

  **检测操作系统：**
  ```bash
  python3 -c "import platform; print(platform.system())"
  ```
  输出结果：`Windows`、`Darwin` (macOS) 或 `Linux`

  **macOS:**
  ```bash
  sudo chown $(whoami):staff /etc/hosts
  sudo chmod 644 /etc/hosts
  ```

  **Linux:**
  ```bash
  sudo chown $(whoami):$(whoami) /etc/hosts
  sudo chmod 644 /etc/hosts
  ```

  **Windows:**
  - 无需配置权限
  - 直接以管理员身份运行命令提示符或 PowerShell 即可

  ⚠️ **此操作必须由用户在系统终端中手动执行**
  执行后，脚本将不再需要 sudo 权限，可以免密码运行

### 仅检查连接状态

```bash
python3 {{skill_path}}/scripts/fix_github_dns.py --check
```

### 使用自定义 hosts 源

```bash
python3 {{skill_path}}/scripts/fix_github_dns.py -u "https://your-custom-url.com/hosts"
```

### 查看帮助

```bash
python3 {{skill_path}}/scripts/fix_github_dns.py --help
```

