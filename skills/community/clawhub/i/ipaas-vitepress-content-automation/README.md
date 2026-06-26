# iPaaS 自动化发布工具包

## 核心安全要求
为通过安装校验，本工具包遵循高安全标准：
1. **主机密钥校验**：脚本不再自动接受未知主机。请在首次运行前执行：
   `ssh-keyscan -p [端口] [服务器IP] >> ~/.ssh/known_hosts`
2. **免密配置**：必须完成 `ssh-copy-id` 授权。
3. **路径限制**：禁止向系统根目录同步。

## 环境准备
确保您的 Shell 环境中已定义：
```bash
export SERVER_IP="1.2.3.4"
export REMOTE_DIR="/path/to/vpress/dist"