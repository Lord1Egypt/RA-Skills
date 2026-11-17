# CLI / SDK 安装与凭据配置 — huawei-cloud-ces-alarm-rules-list

## 1. KooCLI（hcloud）— 主执行路径

```bash
# 官方安装（Linux / macOS）
curl -sSL https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/hcloud_install.sh -o hcloud_install.sh
bash hcloud_install.sh

# 版本与配置
hcloud --version
hcloud configure list
```

- 本 skill 已实测于 **KooCLI 7.3.12**（`hcloud CES ListAlarmRules --help` 参数清单见
  [api-verification.md](api-verification.md)）。
- hcloud **不存在**时脚本自动回退到官方 SDK；两条路径的只读语义一致。

## 2. Python SDK — 回退路径

```bash
# 自动检查并安装（优先国内镜像，失败回退官方源）
python3 scripts/ensure_env.py

# 或手动
pip install huaweicloudsdkcore huaweicloudsdkces
```

- 本 skill 已实测于 **huaweicloudsdkces 3.1.220**（v2 列表/策略/资源 + v1 状态）。
- 渲染逻辑只用标准库（`json` / `textwrap` 级），无需额外依赖。

## 3. 凭据配置（必须带外完成）

**绝不在对话中粘贴 AK/SK**，脚本也不会读取、回显或存储密钥。

```bash
# 方式 A：hcloud 交互式配置（在你自己的终端里完成，凭据不会经过本会话）
hcloud configure

# 方式 B：环境变量（SDK 回退路径；同样在会话外的 shell profile 里设置）
export HUAWEICLOUD_SDK_AK=<你的 AK>
export HUAWEICLOUD_SDK_SK=<你的 SK>
# CES 是项目级服务，SDK 回退还需要 project id（CLI 路径由 hcloud 自动解析）
export CES_ALARM_PROJECT_ID=<project_id>
```

**绝不**在对话、命令行回显或 Issue 评论里出现 AK/SK 明文；本 skill 的脚本也不会把密钥
作为参数传入或落盘。

脚本识别的 AK/SK 环境变量白名单：
`HUAWEICLOUD_SDK_AK` / `HUAWEI_ACCESS_KEY` / `HW_ACCESS_KEY` / `HWC_ACCESS_KEY` /
`HUAWEI_AK` / `HW_AK`，以及对应的 `*_SK` / `*_SECRET_KEY` 系列。

project id 白名单：`CES_ALARM_PROJECT_ID` / `HUAWEICLOUD_SDK_PROJECT_ID` /
`HUAWEI_PROJECT_ID` / `HW_PROJECT_ID`。

## 4. skill-quality-cli（遥测包裹）

```bash
bash scripts/ensure_cli.sh        # 幂等；已安装则跳过
bash scripts/install_cli.sh       # 手动安装（无自动升级）
```

- 脚本把每次 hcloud 调用包裹成
  `skill-quality-cli run --skill-name huawei-cloud-ces-alarm-rules-list -- hcloud ...`。
- 关闭遥测：`export SKILL_QUALITY_REPORT=0`（此时降级为裸 hcloud，只读语义不变）。
- 离线自测/复现时可显式指定 mock：`export CES_ALARM_HCLOUD_BIN=/path/to/mock-hcloud`。

## 5. 网络与区域

- 出网 HTTPS 访问 `ces.<region>.myhuaweicloud.com`。
- 默认区域 `cn-north-4`，用 `--region` 覆盖。