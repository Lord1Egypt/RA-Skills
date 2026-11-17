# 验收清单

## 功能验收

| # | 检查项 | 判定标准 | 验证命令 |
|---|--------|----------|----------|
| A1 | 默认输出简洁列表 | 三列 别名 / 密钥ID / 状态 + 汇总行 `共 N 个密钥`；rc=0 | `python3 scripts/list_kms_keys.py --region cn-north-4` |
| A2 | `--table` 8 列 | 密钥ID / 别名 / 状态 / 密钥用途 / 密钥类型 / 轮转周期 / 创建时间 / region | 同上加 `--table` |
| A3 | `--json` 原始响应 | 可 `json.tool` 解析，含 `keys` / `key_details` / `total` / `truncated` | 加 `--json` |
| A4 | `--alias` 精确过滤 | 仅返回别名完全相同的密钥 | `--alias <alias>` |
| A5 | `--fuzzy` 模糊过滤 | 子串命中即返回 | `--alias <part> --fuzzy` |
| A6 | `--key-id` 过滤 | 子串命中即返回 | `--key-id <id-part>` |
| A7 | `--state` 过滤 | 支持 `1`-`5` 与 `enabled`/`disabled`/`pending-deletion`/`pending-import`/`pending-activation` | `--state enabled` |
| A8 | `--region` | 所有调用带该 region，表格 region 列一致 | `--region cn-north-1` |
| A9 | 分页 | `--limit` 1~200；`truncated=true` 时按 `next_marker` 续取，`total` 汇总 | `--limit 1`（多页密钥时） |
| A10 | SDK 回退 | hcloud 缺失或失败时仍能输出（`--backend sdk` 验证） | `--backend sdk` |

## 只读与安全验收

| # | 检查项 | 判定标准 | 验证命令 |
|---|--------|----------|----------|
| S1 | `--action` 写意图拦截 | rc=1，且无任何 API 调用 | `--action rotate` |
| S2 | `--alias` 写意图拦截 | rc=1，且无任何 API 调用 | `--alias create-me` |
| S3 | `--key-id` 写意图拦截 | rc=1，且无任何 API 调用 | `--key-id delete-xxx` |
| S4 | 仅构造只读操作 | 源码中只出现 `ListKeys` / `ShowKeyRotationStatus` | `grep -n "KMS\\\\|ListKeys" scripts/list_kms_keys.py` |
| S5 | 不落盘 | 运行后无新增文件（除缓存） | `git status --porcelain` |
| S6 | 不回显凭据 | 输出/日志无 AK/SK 片段 | 人工检查输出与 stderr |

## 错误路径验收

| # | 场景 | 判定标准 |
|---|------|----------|
| E1 | 空列表 | `当前区域无 KMS 密钥（区域: …）。` + 更换 region 提示，rc=0 |
| E2 | 过滤无命中 | `未找到匹配的 KMS 密钥（区域: …）。`，rc=0 |
| E3 | 403 权限不足 | 提示 `kms:cmk:list` / `kms:cmk:getRotation`，rc=1 |
| E4 | 缺凭据 | 提示配置 profile 或 `HUAWEICLOUD_SDK_AK/SK`，rc=1 |
| E5 | 无 hcloud（`--backend cli`） | 安装指引 + 安装页链接，rc=1 |
| E6 | KooCLI `[USE_ERROR]` | 参数/用法提示，rc=1 |
| E7 | `--limit` 越界 / `--state` 非法 | 参数校验提示，rc=1 |

## 交付物验收

| # | 文件 | 要求 |
|---|------|------|
| D1 | `SKILL.md` | name 与目录一致、无 version 字段、必含 Overview / Prerequisites / Workflow / Core Commands / Parameter Confirmation / References |
| D2 | `scripts/list_kms_keys.py` | 单文件、标准库为主、`py_compile` 通过 |
| D3 | `scripts/ensure_cli.sh` / `scripts/install_cli.sh` | `bash -n` 通过 |
| D4 | `tests/test_list_kms_keys.py` | 离线可跑，全部通过（mock hcloud + fake SDK） |
| D5 | `templates/test-vars.json` | `json.tool` 通过 |
| D6 | `references/` 五件套 | iam-policies / cli-installation-guide / verification-method / dataflow-diagram / acceptance-criteria |
| D7 | 结构校验 | `validate-skill.sh` FAIL=0 |

## 回归验收

| # | 检查项 | 判定标准 |
|---|--------|----------|
| R1 | 不改动现有模块 | 变更集仅新增 `skills/security/kms/huawei-cloud-kms-key-list/` |
| R2 | 现有测试不受影响 | 仓库既有测试仍通过 |
| R3 | 单 PR 单 skill | 变更仅涉及一个 skill 目录 |

## 遗留项（如有）

- 若账号无 `kms:cmk:getRotation`：表格轮转列退化为「开启 / 关闭」，需用
  `--no-rotation-detail` 显式声明，不作为缺陷。
- `--table` 对轮转开启的密钥最多发起 50 次只读轮转查询；密钥数很大时建议
  `--no-rotation-detail`。