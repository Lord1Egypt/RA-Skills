# KooCLI 安装指南

> **用户手册（非 Agent 执行）**  
> 以下安装、`sudo`、下载脚本仅供用户在本机终端人工执行。Agent **仅**可执行 `hcloud version` 与 `hcloud configure list`；不得代为下载、安装或改凭证。

## 概述

华为云 KooCLI（`hcloud`）是华为云统一 CLI；**本技能仅使用其中 BSS 只读查询**。

安装后执行 `hcloud version` 确认版本；下载包以官方
[快速安装](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
页面 `latest` 链接为准。

官方下载域名（2026-04 起）：

```text
https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/
```

旧域名 `hcloudcli.obs.cn-north-4.myhuaweicloud.com` 及旧包名
`hcloud_cli_*` 已失效，勿再使用。

## 一键安装（Linux / macOS）

以下命令需要用户在本机终端确认后手动执行。Agent 只负责检查 `hcloud version`
和 `hcloud configure list`；不要在未确认时下载或执行安装脚本。

```bash
BASE=https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest
curl -sSL "$BASE/hcloud_install.sh" -o ./hcloud_install.sh
# 执行前先审阅脚本来源和内容：less ./hcloud_install.sh
bash ./hcloud_install.sh
```

默认安装到 `/usr/local/hcloud/`，并链接到 `/usr/local/bin/`。非交互模式：

```bash
BASE=https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest
curl -sSL "$BASE/hcloud_install.sh" -o ./hcloud_install.sh
# 执行前先审阅脚本来源和内容：less ./hcloud_install.sh
bash ./hcloud_install.sh -y
```

## 分步安装

### Linux (AMD 64)

```bash
curl -LO "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-linux-amd64.tar.gz"
tar -zxvf huaweicloud-cli-linux-amd64.tar.gz
sudo mv hcloud /usr/local/bin/
hcloud version
```

### Linux (ARM 64)

```bash
curl -LO "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-linux-arm64.tar.gz"
tar -zxvf huaweicloud-cli-linux-arm64.tar.gz
sudo mv hcloud /usr/local/bin/
hcloud version
```

### macOS (AMD 64)

```bash
curl -LO "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-mac-amd64.tar.gz"
tar -zxvf huaweicloud-cli-mac-amd64.tar.gz
sudo mv hcloud /usr/local/bin/
hcloud version
```

### macOS (ARM 64)

```bash
curl -LO "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-mac-arm64.tar.gz"
tar -zxvf huaweicloud-cli-mac-arm64.tar.gz
sudo mv hcloud /usr/local/bin/
hcloud version
```

### Windows (64 位)

```powershell
$url = "https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-windows-amd64.zip"
Invoke-WebRequest -Uri $url -OutFile "huaweicloud-cli-windows-amd64.zip"
Expand-Archive -Path huaweicloud-cli-windows-amd64.zip -DestinationPath C:\hcloud
# 将 C:\hcloud 加入系统 Path 后：
hcloud version
```

## 认证配置

### 推荐方式

```bash
hcloud configure list
```

优先使用本机已配置的 profile。不要让用户在对话里粘贴 AK/SK。

### 临时环境变量

```bash
export HUAWEICLOUD_SDK_AK=<your-ak>
export HUAWEICLOUD_SDK_SK=<your-sk>
export HUAWEICLOUD_SDK_REGION=cn-north-1
```

仅在用户明确授权真实验证时使用。验证完成后清理当前 shell 环境变量。

### 交互式配置

如本机未配置 KooCLI，可由用户在本机终端交互执行：

```bash
hcloud configure set
```

不要通过聊天记录、脚本参数、日志输出传递明文 AK/SK。

### 验证配置

```bash
hcloud configure list
# 期望输出:
# {
#   "current": "default",
#   "profiles": [{
#     "name": "default",
#     "mode": "AKSK",
#     "accessKeyId": "HPU****QBN",
#     "region": "cn-north-1"
#   }]
# }
```

## 获取AK/SK

1. 登录 [华为云控制台](https://console.huaweicloud.com)
2. 右上角点击用户名 → "我的凭证"
3. 选择 "访问密钥" 标签
4. 点击 "新增访问密钥"
5. 下载并妥善保存AK/SK文件

⚠️ **安全提醒**:

- AK/SK是账号的长期凭证，等同于账号密码
- 绝不在代码、配置文件、对话中明文存储
- 建议使用IAM用户AK/SK而非主账号
- 定期轮换AK/SK
- 为IAM用户配置最小权限策略
- 真实验证只使用只读 BSS/API，禁止执行支付、续费、删除、修改类命令

## 常见安装问题

| 问题 | 原因 | 解决方案 |
| --- | --- | --- |
| `hcloud: command not found` | 未加入PATH | `sudo mv hcloud /usr/local/bin/` |
| `Permission denied` | 无执行权限 | `chmod +x /usr/local/bin/hcloud` |
| 下载 404 | 使用了旧域名/旧包名 | 改用 `cn-north-4-hdn-koocli` 域名与 `huaweicloud-cli-*` 包名 |
| SSL证书错误 | 系统CA证书过旧 | 更新ca-certificates包 |
| 连接超时 | 网络限制 | 检查代理/防火墙设置 |

## 参考链接

- [KooCLI 快速安装（概述与下载表）](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Linux 安装](https://support.huaweicloud.com/qs-hcli/hcli_02_003_02.html)
- [macOS 安装](https://support.huaweicloud.com/qs-hcli/hcli_02_003_03.html)
- [Windows 安装](https://support.huaweicloud.com/qs-hcli/hcli_02_003_01.html)
- [KooCLI 产品描述](https://support.huaweicloud.com/productdesc-hcli/hcli_01.html)
- [API Explorer](https://console.huaweicloud.com/apiexplorer/#/openapi/overview)
- [IAM 权限最佳实践](https://support.huaweicloud.com/bestpractice-iam/iam_0426.html)
