# KooCLI（hcloud）安装、凭据配置与质量 CLI

本 skill 的主路径依赖 KooCLI 7.x。缺失 hcloud 时脚本会自动回退到
`huaweicloudsdkas` v1 SDK，但推荐安装 CLI 以获得与手工操作一致的行为。

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

## 3. 确认 AS 服务可用

```bash
hcloud AS ListScalingGroups --cli-region=cn-north-4 --help
hcloud AS ListScalingInstances --cli-region=cn-north-4 --help
```

输出应分别包含：

- `ListScalingGroups`：`Method: GET`，`Params: --cli-region / --project_id /
  --scaling_group_name / --scaling_group_status / --start_number / --limit /
  --enterprise_project_id`。
- `ListScalingInstances`：`Method: GET`，`Params: --cli-region / --project_id /
  --scaling_group_id / --life_cycle_state / --health_status /
  --protect_from_scaling_down / --start_number / --limit`。

若提示 `[USE_ERROR]`，说明参数写错；若提示服务不存在，说明 CLI 版本过旧，
升级后重试。

## 4. 常见问题

| 现象 | 原因 | 处置 |
|------|------|------|
| `hcloud: command not found` | 未安装或不在 PATH | 按上文安装；或使用 `--backend sdk` 回退 |
| `[USE_ERROR]cli-region` | 区域参数缺失/拼错 | 用 `--region` 指定合法 region |
| `[USE_ERROR]` 其它参数 | 参数名不存在 | 只使用 `--help` 中列出的参数 |
| 403 / not authorized | IAM 权限不足 | 见 `iam-policies.md` |
| 凭据相关报错 | 未配置 profile 或环境变量 | `hcloud configure init` 或导出 AK/SK |
| `伸缩组不存在` | group-id 错误或不在当前 region | 先不带 `--group-id` 列出全部伸缩组，再选择有效 ID |

## 5. SDK 回退（不安装 CLI 时）

```bash
pip install huaweicloudsdkcore huaweicloudsdkas
export HUAWEICLOUD_SDK_AK="<your-ak>"
export HUAWEICLOUD_SDK_SK="<your-sk>"
python3 scripts/list_as_groups.py --backend sdk --region=cn-north-4
```

SDK 路径只从环境变量取凭据；未设置时脚本会直接给出「缺少华为云凭据」提示并
退出 1。SDK 使用 `huaweicloudsdkas` 的 `v1` 包与 `AsRegion`。

## 6. skill-quality-cli（质量遥测）

生成的 skill 与创建器保持一致，携带可选的 skill-quality-cli 遥测能力
（设置 `SKILL_QUALITY_REPORT=0` 可关闭）：

```bash
# 幂等就绪：已安装可用则静默退出，缺失时自动安装
bash scripts/ensure_cli.sh

# 手动安装（ensure_cli.sh 安装失败时的兜底）
bash scripts/install_cli.sh

# 手动升级（不自动升级）
skill-quality-cli upgrade

# 关闭遥测上报
export SKILL_QUALITY_REPORT=0
```

本 skill 的 `hcloud` 命令统一以
`skill-quality-cli run --skill-name huawei-cloud-as-group-list -- hcloud ...`
包装执行；裸 `hcloud` 调用不允许。

## 7. 脚本自带的 hcloud 路径覆盖（测试/离线）

离线测试可以通过环境变量指定 hcloud 二进制：

```bash
export HUAWEI_CLOUD_AS_GROUP_LIST_HCLOUD_BIN=/path/to/mock-hcloud
# 或
export AS_HCLOUD_BIN=/path/to/mock-hcloud
```

该覆盖只用于测试与离线验证，生产环境请直接把 `hcloud` 放入 `PATH`。