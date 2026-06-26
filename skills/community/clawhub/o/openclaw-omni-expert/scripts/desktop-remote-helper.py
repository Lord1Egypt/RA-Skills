#!/usr/bin/env python3
"""
OpenClaw 桌面远程协助助手
生成交互式操作指南，帮助通过远程软件协助安装 OpenClaw
支持 Windows/macOS/Linux 平台
"""

import argparse
import sys
import platform
from datetime import datetime
from pathlib import Path


class DesktopRemoteHelper:
    """桌面远程协助助手"""

    def __init__(self, target_platform: str):
        self.target_platform = target_platform.lower()
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_guide(self, output_format: str = "markdown") -> str:
        """生成安装指南"""

        if output_format == "markdown":
            return self._generate_markdown_guide()
        elif output_format == "text":
            return self._generate_text_guide()
        else:
            raise ValueError(f"不支持的格式: {output_format}")

    def _generate_markdown_guide(self) -> str:
        """生成 Markdown 格式指南"""

        platform_name = self.target_platform.capitalize()
        guide = f"""# OpenClaw 远程协助安装指南

**目标平台**: {platform_name}
**生成时间**: {self.timestamp}

---

## 操作前检查清单

### 环境检查
- [ ] 操作系统: {self._get_os_version()}
- [ ] 管理员权限: 已确认
- [ ] 网络连接: 正常
- [ ] 磁盘空间: ≥ 2GB
- [ ] 内存: ≥ 4GB (推荐 8GB+)

### 远程软件检查
- [ ] 双方已安装相同的远程软件
- [ ] 远程软件连接正常
- [ ] 已准备好操作日志记录工具

---

## 安装步骤

{self._get_install_steps()}

---

## 验证步骤

### 基础验证
1. 打开终端/命令提示符/PowerShell
2. 执行: `openclaw --version`
   - 应显示版本号，如: `openclaw v1.0.0`

3. 执行: `openclaw gateway status`
   - 应显示服务运行中

4. 打开浏览器访问: http://127.0.0.1:18789
   - 应显示 OpenClaw Web UI

### 功能验证
- [ ] 能发送测试消息
- [ ] AI 能正常响应
- [ ] 配置文件已生成
- [ ] 日志文件存在

---

## 常见问题

{self._get_troubleshooting()}

---

## 安全注意事项

- [ ] 仅在必要时获取管理员权限
- [ ] 不要分享密码
- [ ] 安装完成后关闭管理员权限
- [ ] 避免打开不相关文件
- [ ] 协助结束后断开远程连接

---

## 操作记录模板

| 时间 | 步骤 | 操作 | 结果 | 备注 |
|------|------|------|------|------|
|      |      |      |      |      |

---

## 支持资源

- 官方文档: https://docs.openclaw.com
- 故障排查: 见 SKILL.md 中的 troubleshooting-guide.md
- 技术支持: [联系方式]

---

**祝你安装顺利！**
"""
        return guide

    def _generate_text_guide(self) -> str:
        """生成纯文本格式指南（适合打印）"""

        platform_name = self.target_platform.capitalize()
        guide = f"""
OpenClaw 远程协助安装指南
{'='*60}
目标平台: {platform_name}
生成时间: {self.timestamp}

{'='*60}
操作前检查清单
{'='*60}

环境检查:
[ ] 操作系统已知
[ ] 管理员权限已确认
[ ] 网络连接正常
[ ] 磁盘空间 ≥ 2GB
[ ] 内存 ≥ 4GB

远程软件检查:
[ ] 双方已安装相同远程软件
[ ] 远程软件连接正常
[ ] 已准备好操作日志记录工具

{'='*60}
安装步骤
{'='*60}

{self._get_install_steps_text()}

{'='*60}
验证步骤
{'='*60}

1. 验证安装:
   - 打开终端/命令提示符
   - 执行: openclaw --version
   - 应显示版本号

2. 验证服务:
   - 执行: openclaw gateway status
   - 应显示服务运行中

3. 访问 Web UI:
   - 打开浏览器
   - 访问: http://127.0.0.1:18789
   - 确认页面正常显示

4. 功能测试:
   - 发送测试消息
   - 确认 AI 响应正常

{'='*60}
常见问题
{'='*60}

{self._get_troubleshooting_text()}

{'='*60}
安全注意事项
{'='*60}

- 仅在必要时获取管理员权限
- 不要分享密码给任何人
- 安装完成后关闭管理员权限
- 避免打开不相关文件
- 协助结束后断开远程连接

{'='*60}
操作记录
{'='*60}

时间 | 步骤 | 操作 | 结果 | 备注
-----|------|------|------|-----


{'='*60}
祝你安装顺利！
{'='*60}
"""
        return guide

    def _get_os_version(self) -> str:
        """获取目标平台版本信息"""
        if self.target_platform == "windows":
            return "Windows 10/11"
        elif self.target_platform == "macos":
            return "macOS 12+ (Monterey 或更高版本)"
        elif self.target_platform == "linux":
            return "Ubuntu 20.04+ / CentOS 7+ / 其他主流发行版"
        else:
            return "未知"

    def _get_install_steps(self) -> str:
        """获取安装步骤"""

        if self.target_platform == "windows":
            return self._get_windows_install_steps()
        elif self.target_platform == "macos":
            return self._get_macos_install_steps()
        elif self.target_platform == "linux":
            return self._get_linux_install_steps()
        else:
            return "不支持的平台"

    def _get_install_steps_text(self) -> str:
        """获取纯文本格式的安装步骤"""
        steps = self._get_install_steps()
        # 移除 Markdown 格式
        steps = steps.replace("`", "")
        steps = steps.replace("```", "")
        steps = steps.replace("**", "")
        steps = steps.replace("###", "")
        steps = steps.replace("-", "")
        return steps.strip()

    def _get_windows_install_steps(self) -> str:
        """Windows 安装步骤"""
        return """### 步骤 1: 安装 Node.js

1. 打开浏览器，访问 https://nodejs.org
2. 下载 **LTS** 版本（推荐 v22 或更高版本）
3. 运行安装程序
4. 点击 "Next" 接受许可协议
5. 选择默认安装路径，点击 "Next"
6. 勾选所有选项（npm package manager 等），点击 "Next"
7. 点击 "Install" 开始安装
8. 安装完成后，点击 "Finish"

**验证**:
- 打开 PowerShell（按 Win+X，选择 "Windows PowerShell"）
- 执行: `node --version`
- 应显示版本号，如: `v22.11.0`
- 执行: `npm --version`
- 应显示版本号，如: `10.9.0`

### 步骤 2: 配置 npm 镜像源（国内用户推荐）

1. 以管理员身份打开 PowerShell
2. 执行以下命令:
   ```powershell
   npm config set registry https://registry.npmmirror.com
   ```

**验证**:
```powershell
npm config get registry
```
应显示: `https://registry.npmmirror.com`

### 步骤 3: 安装 Git（如未安装）

1. 访问 https://git-scm.com/download/win
2. 下载并安装 Git
3. 安装过程中一路点击 "Next" 使用默认配置

**验证**:
```powershell
git --version
```

### 步骤 4: 安装 OpenClaw

1. 以管理员身份打开 PowerShell
2. 执行:
   ```powershell
   npm install -g openclaw@latest
   ```

3. 等待安装完成（可能需要 2-5 分钟）

**验证**:
```powershell
openclaw --version
```
应显示版本号

### 步骤 5: 初始化配置

1. 执行:
   ```powershell
   openclaw onboard
   ```

2. 按照提示完成配置:
   - 选择 AI 模型（Claude/GPT）
   - 输入 API Key
   - 选择通讯频道（微信/钉钉/Slack 等）
   - 设置其他选项

### 步骤 6: 启动服务

1. 执行:
   ```powershell
   openclaw gateway start
   ```

2. 服务启动后，打开浏览器
3. 访问: http://127.0.0.1:18789
4. 应显示 OpenClaw Web UI

### 步骤 7: 设置开机自启动（可选）

如果希望开机自动启动 OpenClaw 服务:

1. 以管理员身份打开 PowerShell
2. 执行:
   ```powershell
   openclaw gateway enable
   ```

## 常用命令

```powershell
# 启动服务
openclaw gateway start

# 停止服务
openclaw gateway stop

# 重启服务
openclaw gateway restart

# 查看状态
openclaw gateway status

# 查看日志
openclaw gateway logs

# 禁用开机自启动
openclaw gateway disable
```"""

    def _get_macos_install_steps(self) -> str:
        """macOS 安装步骤"""
        return """### 步骤 1: 安装 Homebrew（如未安装）

1. 打开终端（按 Cmd+Space，搜索 "Terminal"）
2. 访问 https://brew.sh
3. 复制安装命令（通常在页面顶部）
4. 粘贴到终端并执行
5. 按照提示安装 Xcode Command Line Tools（如提示）
6. 安装完成后，执行:
   ```bash
   brew --version
   ```
   验证安装成功

### 步骤 2: 安装 Node.js

1. 执行:
   ```bash
   brew install node@22
   ```

2. 链接到系统:
   ```bash
   brew link node@22
   ```

**验证**:
```bash
node --version
```
应显示版本号，如: `v22.11.0`

```bash
npm --version
```

### 步骤 3: 配置 npm 镜像源（国内用户推荐）

1. 执行:
   ```bash
   npm config set registry https://registry.npmmirror.com
   ```

**验证**:
```bash
npm config get registry
```

### 步骤 4: 安装 Git

1. 执行:
   ```bash
   brew install git
   ```

**验证**:
```bash
git --version
```

### 步骤 5: 安装 OpenClaw

1. 执行:
   ```bash
   npm install -g openclaw@latest
   ```

2. 等待安装完成

**验证**:
```bash
openclaw --version
```

### 步骤 6: 初始化配置

1. 执行:
   ```bash
   openclaw onboard
   ```

2. 按照提示完成配置

### 步骤 7: 启动服务

1. 执行:
   ```bash
   openclaw gateway start
   ```

2. 打开浏览器，访问: http://127.0.0.1:18789

### 步骤 8: 设置开机自启动（可选）

```bash
openclaw gateway enable
```

## 常用命令

```bash
# 启动服务
openclaw gateway start

# 停止服务
openclaw gateway stop

# 重启服务
openclaw gateway restart

# 查看状态
openclaw gateway status

# 查看日志
openclaw gateway logs
```"""

    def _get_linux_install_steps(self) -> str:
        """Linux 安装步骤"""
        return """### 步骤 1: 更新系统

**Ubuntu/Debian**:
```bash
sudo apt update && sudo apt upgrade -y
```

**CentOS/RHEL**:
```bash
sudo yum update -y
```

**Fedora**:
```bash
sudo dnf update -y
```

### 步骤 2: 安装 Node.js v22+

**Ubuntu/Debian**:
```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
```

**CentOS/RHEL**:
```bash
curl -fsSL https://rpm.nodesource.com/setup_22.x | sudo bash -
sudo yum install -y nodejs
```

**Fedora**:
```bash
sudo dnf install -y nodejs
```

**验证**:
```bash
node --version
```
应显示版本号，如: `v22.11.0`

```bash
npm --version
```

### 步骤 3: 配置 npm 镜像源（国内用户推荐）

```bash
npm config set registry https://registry.npmmirror.com
```

**验证**:
```bash
npm config get registry
```

### 步骤 4: 安装构建工具

**Ubuntu/Debian**:
```bash
sudo apt install -y build-essential git
```

**CentOS/RHEL**:
```bash
sudo yum groupinstall -y "Development Tools"
sudo yum install -y git
```

**验证**:
```bash
git --version
```

### 步骤 5: 安装 OpenClaw

```bash
sudo npm install -g openclaw@latest
```

**验证**:
```bash
openclaw --version
```

### 步骤 6: 初始化配置

```bash
openclaw onboard
```

按照提示完成配置

### 步骤 7: 启动服务

```bash
openclaw gateway start
```

打开浏览器，访问: http://127.0.0.1:18789

### 步骤 8: 设置开机自启动（可选）

```bash
openclaw gateway enable
```

## 常用命令

```bash
# 启动服务
openclaw gateway start

# 停止服务
openclaw gateway stop

# 重启服务
openclaw gateway restart

# 查看状态
openclaw gateway status

# 查看日志
openclaw gateway logs

# 禁用开机自启动
openclaw gateway disable
```

### 步骤 9: 配置防火墙（如需要）

如果需要从其他设备访问 OpenClaw:

**Ubuntu/Debian (UFW)**:
```bash
sudo ufw allow 18789/tcp
sudo ufw reload
```

**CentOS/RHEL (Firewalld)**:
```bash
sudo firewall-cmd --permanent --add-port=18789/tcp
sudo firewall-cmd --reload
```

## 系统服务配置

如果希望使用 systemd 管理服务:

```bash
# 创建服务文件
sudo nano /etc/systemd/system/openclaw-gateway.service
```

添加以下内容:
```ini
[Unit]
Description=OpenClaw Gateway Service
After=network.target

[Service]
Type=simple
User=your_username
ExecStart=/usr/local/bin/openclaw gateway start
ExecStop=/usr/local/bin/openclaw gateway stop
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

启用并启动服务:
```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw-gateway
sudo systemctl start openclaw-gateway
sudo systemctl status openclaw-gateway
```"""

    def _get_troubleshooting(self) -> str:
        """获取故障排查信息"""
        return """### 问题 1: Node.js 安装失败

**症状**: 安装程序报错

**解决方案**:
- 检查操作系统版本是否支持
- 禁用杀毒软件临时安装
- 以管理员身份运行安装程序
- 尝试下载不同版本的 Node.js

### 问题 2: npm install 失败

**症状**: 安装 OpenClaw 时报错

**常见错误**:
- `EACCES`: 权限不足
- `ETIMEDOUT`: 网络超时
- `ENOSPC`: 磁盘空间不足

**解决方案**:
```bash
# 权限不足
# Windows: 以管理员身份运行 PowerShell
# macOS/Linux: 使用 sudo

# 网络超时
npm config set registry https://registry.npmmirror.com
npm cache clean --force

# 磁盘空间不足
# 清理临时文件
```

### 问题 3: OpenClaw 启动失败

**症状**: `openclaw gateway start` 报错

**解决方案**:
```bash
# 检查 Node.js 版本
node --version  # 需要 v22+

# 检查端口占用
# Windows
netstat -ano | findstr :18789

# macOS/Linux
lsof -i :18789

# 检查配置文件
# 查看配置文件内容
cat ~/.openclaw/config.json

# 查看日志
cat ~/.openclaw/logs/gateway.err.log

# 重新安装
npm install -g openclaw@latest
```

### 问题 4: 无法访问 Web UI

**症状**: 浏览器打开 http://127.0.0.1:18789 无响应

**解决方案**:
```bash
# 确认服务已启动
openclaw gateway status

# 检查端口占用

# 尝试使用 localhost
# 在浏览器中访问: http://localhost:18789

# 检查防火墙设置

# 重启服务
openclaw gateway restart
```

### 问题 5: AI 无法响应

**症状**: 发送消息后 AI 无响应

**解决方案**:
1. 检查 AI 模型配置
2. 检查 API Key 是否有效
3. 检查网络连接
4. 查看日志文件
5. 检查账号余额（如使用付费 API）

```bash
# 查看输出日志
cat ~/.openclaw/logs/gateway.out.log
```"""

    def _get_troubleshooting_text(self) -> str:
        """获取纯文本格式的故障排查信息"""
        steps = self._get_troubleshooting()
        steps = steps.replace("`", "")
        steps = steps.replace("```", "")
        steps = steps.replace("###", "")
        steps = steps.replace("###", "")
        steps = steps.replace("**", "")
        steps = steps.replace("-", "")
        return steps.strip()

    def generate_checklist(self) -> str:
        """生成检查清单"""
        return """OpenClaw 安装检查清单

环境检查:
[ ] 操作系统版本已知
[ ] 管理员权限已确认
[ ] 网络连接正常
[ ] 磁盘空间 ≥ 2GB
[ ] 内存 ≥ 4GB

依赖安装:
[ ] Node.js v22+ 已安装
[ ] npm 已安装
[ ] Git 已安装
[ ] npm 镜像源已配置

OpenClaw 安装:
[ ] openclaw 已安装
[ ] openclaw --version 能显示版本号
[ ] 配置已完成
[ ] 服务已启动
[ ] Web UI 可访问
[ ] 功能测试通过

验证:
[ ] 能发送测试消息
[ ] AI 能正常响应
[ ] 配置文件已生成
[ ] 日志文件存在
[ ] 服务状态正常

安全:
[ ] 管理员权限已关闭
[ ] 远程连接已断开
[ ] 密码未泄露
"""

    def generate_operation_log(self) -> str:
        """生成操作日志模板"""
        return """OpenClaw 远程协助操作日志

操作者: _______________
被协助者: _______________
远程软件: _______________
目标平台: _______________
开始时间: _______________
结束时间: _______________

环境信息:
操作系统: _______________
内存大小: _______________
磁盘空间: _______________
网络环境: _______________

操作记录:
------------------------------------------------------
时间   | 步骤 | 操作 | 结果 | 备注
-------|------|------|------|-----
       |      |      |      |
       |      |      |      |
       |      |      |      |
       |      |      |      |
       |      |      |      |
       |      |      |      |
       |      |      |      |
       |      |      |      |
       |      |      |      |
       |      |      |      |
------------------------------------------------------

遇到的问题:
1.
2.
3.

解决方案:
1.
2.
3.

后续建议:
1.
2.
3.

签名:
操作者: _______________
被协助者: _______________
日期: _______________
"""


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="OpenClaw 桌面远程协助助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成 Windows 安装指南（Markdown 格式）
  python desktop-remote-helper.py --platform windows --format markdown

  # 生成 macOS 安装指南（纯文本格式，适合打印）
  python desktop-remote-helper.py --platform macos --format text

  # 生成 Linux 安装指南
  python desktop-remote-helper.py --platform linux

  # 生成检查清单
  python desktop-remote-helper.py --platform windows --checklist

  # 生成操作日志模板
  python desktop-remote-helper.py --log-template
        """
    )

    parser.add_argument(
        "--platform",
        choices=["windows", "macos", "linux"],
        help="目标平台"
    )

    parser.add_argument(
        "--format",
        choices=["markdown", "text"],
        default="markdown",
        help="输出格式（默认: markdown）"
    )

    parser.add_argument(
        "--output",
        "-o",
        help="输出文件路径（默认: 打印到标准输出）"
    )

    parser.add_argument(
        "--checklist",
        action="store_true",
        help="生成检查清单"
    )

    parser.add_argument(
        "--log-template",
        action="store_true",
        help="生成操作日志模板"
    )

    args = parser.parse_args()

    # 生成日志模板
    if args.log_template:
        helper = DesktopRemoteHelper("windows")  # 平台不重要
        log_template = helper.generate_operation_log()
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(log_template)
            print(f"操作日志模板已保存到: {args.output}")
        else:
            print(log_template)
        return

    # 生成检查清单
    if args.checklist:
        if not args.platform:
            parser.error("--checklist 需要 --platform 参数")

        helper = DesktopRemoteHelper(args.platform)
        checklist = helper.generate_checklist()
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(checklist)
            print(f"检查清单已保存到: {args.output}")
        else:
            print(checklist)
        return

    # 生成安装指南
    if not args.platform:
        parser.error("--platform 是必需的参数")

    helper = DesktopRemoteHelper(args.platform)
    guide = helper.generate_guide(args.format)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(guide)
        print(f"安装指南已保存到: {args.output}")
    else:
        print(guide)


if __name__ == "__main__":
    main()
