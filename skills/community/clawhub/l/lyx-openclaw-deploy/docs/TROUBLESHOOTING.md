# OpenClaw Deploy 故障排查指南

> 版本：V1.2 | 更新日期：2026-03-22

---

## 目录

- [打包失败](#打包失败)
- [部署失败](#部署失败)
- [SSH 连接问题](#ssh-连接问题)
- [Docker 问题](#docker-问题)
- [批量部署问题](#批量部署问题)
- [常见错误码](#常见错误码)

---

## 打包失败

### 错误：`tar: Cannot stat: No such file or directory`

**原因**：`~/.openclaw` 目录不存在或路径错误。

**解决**：
```bash
# 确认 OpenClaw 目录存在
ls -la ~/.openclaw

# 如果目录不存在，先安装 OpenClaw
npm i -g openclaw
openclaw init
```

---

### 错误：`sha256sum: command not found`

**原因**：系统未安装 `sha256sum`（macOS 默认没有）。

**解决**：
```bash
# macOS 安装 coreutils
brew install coreutils

# 或使用 shasum（系统自带）
# 打包脚本会自动降级到 shasum -a 256
```

---

### 错误：`Permission denied` 打包的文件权限不足

**原因**：没有读取 `~/.openclaw` 目录的权限。

**解决**：
```bash
# 检查目录权限
ls -la ~ | grep .openclaw

# 修复权限
chmod 755 ~/.openclaw
chmod -R 755 ~/.openclaw/
```

---

## 部署失败

### 错误：`部署包不存在`

**原因**：传入的 tar.gz 文件路径错误。

**解决**：
```bash
# 确认文件存在
ls -lh openclaw-*.tar.gz

# 使用绝对路径
./build/full/full_builder.sh --output /tmp/openclaw-full.tar.gz
./deploy/batch/batch_deploy.sh --package /tmp/openclaw-full.tar.gz ...
```

---

### 错误：`SHA256 校验失败`

**原因**：传输过程中文件损坏，或 SHA256 文件与包不匹配。

**解决**：
```bash
# 重新生成校验文件
sha256sum openclaw-full.tar.gz > openclaw-full.tar.gz.sha256

# 或跳过校验（不推荐，仅测试用）
# 编辑 deploy/common.sh 注释掉 verify_sha 调用
```

---

### 错误：`/opt/openclaw: directory not empty`

**原因**：目标目录已有 OpenClaw 安装，冲突处理未生效。

**解决**：
```bash
# 确认目录内容
ls -la /opt/openclaw

# 使用 backup 模式（先备份再覆盖）
./scripts/deploy.sh --conflict backup

# 或使用 update 模式（仅更新，不覆盖核心文件）
./scripts/deploy.sh --conflict update

# 或手动删除后重新部署
sudo rm -rf /opt/openclaw
./scripts/deploy.sh
```

---

## SSH 连接问题

### 错误：`Connection refused`

**原因**：SSH 端口未开放或 SSH 服务未启动。

**解决**：
```bash
# 确认目标主机 SSH 服务运行中
ssh user@host 'systemctl status sshd'

# 端口不对？检查配置文件
ssh user@host 'grep Port /etc/ssh/sshd_config'
```

---

### 错误：`Host key verification failed`

**原因**：首次连接未知主机，SSH 默认拒绝。

**解决**：
```bash
# 自动接受新主机密钥（推荐，已内置）
# 脚本已使用 -o StrictHostKeyChecking=accept-new

# 手动预接受
ssh-keyscan -H hostname >> ~/.ssh/known_hosts
```

---

### 错误：`Permission denied (publickey)`

**原因**：SSH 公钥未添加到目标主机，或密钥文件路径错误。

**解决**：
```bash
# 方法1：确认密钥文件存在
ls -la ~/.ssh/id_rsa

# 方法2：使用 ssh-copy-id 预授权
ssh-copy-id user@host

# 方法3：使用密码登录（需安装 sshpass）
./build/remote/remote_deploy.sh --host ... --password "your_password"
```

---

### 错误：`sshpass: command not found`

**原因**：使用密码登录但未安装 `sshpass`。

**解决**：
```bash
# macOS
brew install sshpass

# Ubuntu/Debian
sudo apt install sshpass

# CentOS
sudo yum install sshpass
```

---

## Docker 问题

### 错误：`docker: command not found`

**原因**：目标主机未安装 Docker。

**解决**：
```bash
# 在目标主机上安装 Docker（Ubuntu 示例）
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

---

### 错误：`docker: permission denied`

**原因**：当前用户没有 Docker 执行权限。

**解决**：
```bash
# 将用户加入 docker 组
sudo usermod -aG docker $USER
# 重新登录 shell 使配置生效
newgrp docker

# 或使用 sudo 运行
sudo docker compose up -d
```

---

### 错误：`docker: connection refused`

**原因**：Docker 守护进程未启动。

**解决**：
```bash
# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker

# 确认运行状态
sudo systemctl status docker
```

---

### 错误：`Conflict. The container name "openclaw" is already in use`

**原因**：同名容器已存在。

**解决**：
```bash
# 查看现有容器
docker ps -a | grep openclaw

# 停止并删除旧容器
docker stop openclaw
docker rm openclaw

# 或使用 docker-compose down
cd /opt/openclaw/docker
docker compose down
```

---

## 批量部署问题

### 错误：`未从清单文件中解析到任何主机`

**原因**：`inventory.ini` 格式错误。

**解决**：
```bash
# 确认文件格式正确，参考：
# config/inventory.example.ini

# 常见错误：
# 1. 注释行使用了 ; 而不是 #
# 2. ansible_host= 前有空格
# 3. 主机别名中有特殊字符
```

---

### 错误：部分主机部署失败，但无法确认是哪台

**解决**：
```bash
# 查看各主机的部署日志
ls -la logs/batch-*.log

# 查看特定主机的详细输出
cat logs/batch-web01.log

# 使用 --dry-run 预检查
./deploy/batch/batch_deploy.sh \
  --inventory ./config/inventory.ini \
  --package ./openclaw.tar.gz \
  --dry-run
```

---

## 常见错误码

| 错误码 | 含义 | 处理方式 |
|--------|------|---------|
| `E001` | SSH 连接超时 | 检查网络、防火墙、目标主机 SSH 服务 |
| `E002` | 部署包 SHA256 校验失败 | 重新打包，确保传输完整 |
| `E003` | 目标目录无权限 | 使用 sudo 或确认目录权限 |
| `E004` | Docker 未安装 | 在目标主机安装 Docker |
| `E005` | 冲突处理脚本未找到 | 确认部署包完整性 |
| `E006` | Inventory 解析失败 | 检查 INI 格式是否正确 |

---

## 诊断命令速查

```bash
# 1. 快速连通性检测
ssh -o ConnectTimeout=5 user@host 'echo pong'

# 2. 查看 OpenClaw 版本
ssh user@host 'openclaw --version'

# 3. 检查 Docker 状态
ssh user@host 'docker ps -a | grep openclaw'

# 4. 查看容器日志
ssh user@host 'docker logs openclaw'

# 5. 强制重新部署
ssh user@host 'bash' < <(curl -fsSL https://your-deploy-script-url)
```

---

## 获取帮助

- **GitHub Issues**: https://github.com/lyx058019/openclaw-deploy/issues
- **ClawHub**: https://clawhub.com/s/lyx-openclaw-deploy
- **博客**: https://blog.micrabbit.com
