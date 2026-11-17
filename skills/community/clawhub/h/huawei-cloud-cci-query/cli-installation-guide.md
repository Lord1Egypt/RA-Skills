# hcloud CLI 安装与认证指南

## 1. 安装 KooCLI

### Linux / macOS

```bash
# 下载并安装
curl -sL https://hwcloudcli.obs.cn-north-1.myhuaweicloud.com/cli/latest/hcloud_install.sh && bash hcloud_install.sh

# 验证安装
hcloud --version
```

### 验证

```bash
hcloud --version  # 应输出 KooCLI Version 7.x
```

> 本 Skill 已验证 KooCLI Version **7.2.12** 可用。

参考文档：https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

## 2. 配置认证（AK/SK）

### 方式一：命令行交互配置（推荐脚本使用）

脚本 `scripts/cci_query.py` 会自动调用以下命令配置 default profile：

```bash
hcloud configure set \
  --cli-profile=default \
  --cli-access-key=<AK> \
  --cli-secret-key=<SK>
```

### 方式二：手动配置

```bash
hcloud configure set --cli-profile=default --cli-access-key=AKXXX --cli-secret-key=SKXXX
```

### 验证配置

```bash
hcloud configure list
# 应输出包含 agreePrivacy=true 等配置项的 JSON
```

## 3. AK/SK 获取

AK/SK 来自华为云 IAM 用户：

1. 登录华为云控制台 → 右上角用户头像 → 「我的凭证」
2. 「访问密钥」→ 「新增访问密钥」→ 下载 CSV（含 AK/SK）
3. 将 AK/SK 设置为环境变量（推荐）：

```bash
export HUAWEICLOUD_SDK_AK="你的AK"
export HUAWEICLOUD_SDK_SK="你的SK"
```

脚本会动态扫描 `HUAWEI`/`HW`/`HWC` 前缀且含 `ACCESS_KEY`/`_AK`/`SECRET_KEY`/`_SK` 的环境变量，无需固定变量名。

## 4. 区域说明

CCI 是区域级服务，查询时必须指定 `--cli-region`。常用区域：

| 区域 ID | 名称 |
|---------|------|
| `cn-north-4` | 华北-北京四 |
| `cn-north-1` | 华北-北京一 |
| `cn-east-3` | 华东-上海一 |
| `cn-south-1` | 华南-广州 |
| `ap-southeast-1` | 中国-香港 |

完整区域列表见：https://developer.huaweicloud.com/intl/en-us/endpoints

## 5. 首次使用提示

首次运行 `hcloud` 会提示隐私协议确认。脚本通过管道输入 `y` 自动同意：

```bash
echo "y" | hcloud CCI listNamespaces --cli-region=cn-north-4 --cli-profile=default
```

或在 `hcloud configure list` 中确认 `agreePrivacy=true` 后无需重复确认。

## 6. 常见错误

| 错误 | 原因 | 处理 |
|------|------|------|
| `The configuration file does not contain profile` | 未配置 AK/SK | 运行 `hcloud configure set` 或让脚本自动配置 |
| `403 CCI.01.403122 user has no agency to cci` | 区域未授权 CCI 服务委托 | CCI 控制台对应区域点击「服务授权」 |
| `[USE_ERROR]Operation XXX is not supported` | 操作名错误 | `hcloud CCI --help` 核对真实操作名 |
