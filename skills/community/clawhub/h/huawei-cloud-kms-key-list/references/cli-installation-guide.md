# KooCLI（hcloud）安装与凭据配置

本 skill 的主路径依赖 KooCLI 7.x。缺失 hcloud 时脚本会自动回退到
`huaweicloudsdk` KMS SDK，但推荐安装 CLI 以获得与手工操作一致的行为。

## 1. 安装 KooCLI

### Linux / macOS（推荐，一键脚本）

```bash
curl -sSL https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/hcloud_install.sh -o ./hcloud_install.sh
bash ./hcloud_install.sh -y
```

### 官方镜像 / 离线安装

1. 打开 KooCLI 下载页：<https://support.huaweicloud.com/qs-hcli/hcli_02_003.html>
2. 按操作系统下载对应压缩包（Linux x86_64 / ARM64、Windows、macOS）。
3. 解压后把 `hcloud` 放到 `PATH` 目录（如 `/usr/local/bin`），执行 `hcloud version` 验证。

### 验证

```bash
hcloud version
# 期望输出：KooCLI Version 7.x.x ...
```

## 2. 配置凭据（离线，严禁在对话/命令行里粘贴 AK/SK）

```bash
hcloud configure init
# 交互式输入 AK / SK / region / project_id；输入内容不会回显
```

已有 profile 时查看状态（只读、不回显密钥）：

```bash
hcloud configure list
```

也可以使用环境变量（仅当前 shell 有效）：

```bash
export HUAWEICLOUD_SDK_AK="<your-ak>"
export HUAWEICLOUD_SDK_SK="<your-sk>"
export HUAWEICLOUD_SDK_REGION="cn-north-4"
```

> 安全红线：不要把 AK/SK 写进脚本、仓库、Issue 评论或聊天；也不要用
> `hcloud configure set` 把密钥作为命令行参数传入。
> 本 skill 的脚本从不读取、打印或落盘任何密钥。

## 3. 确认 KMS 服务可用

```bash
hcloud KMS ListKeys --cli-region=cn-north-4 --help
```

输出应包含 `Method: POST`、`Params: --cli-region / --project_id / --key_spec /
--key_state / --limit / --marker`。若提示 `[USE_ERROR]`，说明参数写错；
若提示服务不存在，说明 CLI 版本过旧，升级后重试。

## 4. 常见问题

| 现象 | 原因 | 处置 |
|------|------|------|
| `hcloud: command not found` | 未安装或不在 PATH | 按上文安装；或使用 `--backend sdk` 回退 |
| `[USE_ERROR]cli-region` | 区域参数缺失/拼错 | 用 `--region` 指定合法 region |
| `[USE_ERROR]` 其它参数 | 参数名不存在 | 只使用 `--help` 中列出的参数 |
| 403 / not authorized | IAM 权限不足 | 见 `iam-policies.md` |
| 凭据相关报错 | 未配置 profile 或环境变量 | `hcloud configure init` 或导出 AK/SK |

## 5. SDK 回退（不安装 CLI 时）

```bash
pip install huaweicloudsdkcore huaweicloudsdkkms
export HUAWEICLOUD_SDK_AK="<your-ak>"
export HUAWEICLOUD_SDK_SK="<your-sk>"
python3 scripts/list_kms_keys.py --backend sdk --region=cn-north-4
```

SDK 路径只从环境变量取凭据；未设置时脚本会直接给出「缺少华为云凭据」提示并退出 1。