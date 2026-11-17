# hcloud CLI 安装指南

## 简介

本 skill 依赖华为云 KooCLI（hcloud）调用 CES API。KooCLI 是华为云命令行工具，支持 AK/SK 认证。

## 安装方法

### Linux

```bash
# 下载安装脚本
curl -sSL https://hcloudcli.obs.cn-north-1.myhuaweicloud.com/cli/latest/hcloud_install.sh -o hcloud_install.sh

# 执行安装
bash hcloud_install.sh

# 验证
hcloud --version
```

### macOS

```bash
# 使用 Homebrew
brew install hcloudcli

# 或下载安装脚本
curl -sSL https://hcloudcli.obs.cn-north-1.myhuaweicloud.com/cli/latest/hcloud_install.sh -o hcloud_install.sh
bash hcloud_install.sh
```

### Windows

下载安装包：https://hcloudcli.obs.cn-north-1.myhuaweicloud.com/cli/latest/hcloud_install.exe

## 认证配置

### 方式一：环境变量（推荐，本 skill 使用）

设置 AK/SK 环境变量，脚本动态扫描读取：

```bash
export HUAWEICLOUD_SDK_AK="您的AccessKey"
export HUAWEICLOUD_SDK_SK="您的SecretKey"
```

脚本支持任意 `HUAWEI*`/`HW*`/`HWC*` 前缀的环境变量名（含 `ACCESS_KEY`/`SECRET_KEY` 或以 `_AK`/`_SK` 结尾）。

### 方式二：配置 hcloud profile

```bash
hcloud configure set --cli-mode=AKSK \
  --cli-region=cn-north-4 \
  --cli-access-key=您的AK \
  --cli-secret-key=您的SK
```

> 本 skill 脚本优先从环境变量读取 AK/SK 并通过 `--cli-access-key`/`--cli-secret-key` 运行时注入，无需预配置 profile。

## 获取 AK/SK

1. 登录华为云控制台 → 右上角头像 → 「我的凭证」
2. 选择「访问密钥」→ 「新增访问密钥」
3. 下载 CSV 文件获取 AK/SK

## 验证安装

```bash
hcloud CES ListMetrics --cli-region=cn-north-4 --help
```

能正常显示参数说明即安装成功。

## 参考文档

- KooCLI 快速入门：https://support.huaweicloud.com/qs-hcli/hcli_02_003.html
- CES API 参考：https://support.huaweicloud.com/api-ces/ces_03_0057.html
