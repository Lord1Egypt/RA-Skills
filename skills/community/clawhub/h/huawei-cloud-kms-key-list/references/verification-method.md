# 验证方法

本 skill 的验证分三层：离线单测 → 真实只读冒烟 → 只读守卫与错误路径。

## 1. 语法与结构检查

```bash
# Python 语法
python3 -m py_compile scripts/list_kms_keys.py tests/test_list_kms_keys.py

# Shell 语法
bash -n scripts/ensure_cli.sh
bash -n scripts/install_cli.sh

# JSON 语法
python3 -m json.tool templates/test-vars.json > /dev/null

# 结构/规范校验（creator 提供的校验脚本，FAIL 必须为 0）
bash validate-skill.sh -s "$(pwd)"
```

## 2. 离线单测（无凭据、无网络）

```bash
python3 -m unittest discover -s tests -v
```

覆盖范围：

| 用例 | 验证点 |
|------|--------|
| 默认输出 | 别名 / 密钥ID / 状态 三列 + 汇总行 |
| `--table` | 8 列齐全（密钥ID / 别名 / 状态 / 密钥用途 / 密钥类型 / 轮转周期 / 创建时间 / region） |
| `--json` | 原始响应体（keys / key_details / total / truncated） |
| 分页 | `truncated=true` + `next_marker` 时继续取页并合并去重 |
| 过滤 | `--alias` 精确、`--fuzzy` 模糊、`--key-id` 子串、`--state` 数值与名称 |
| 空列表 | 输出「当前区域无 KMS 密钥」且 rc=0 |
| 403 / 凭据 / `[USE_ERROR]` | 分类提示且 rc=1 |
| 只读守卫 | `--alias create-me`、`--action rotate` 在执行前被拒，rc=1 |
| SDK 回退 | hcloud 缺失/失败时走 fake SDK，输出一致 |

## 3. 真实只读冒烟（需要有效 AK/SK，会产生真实只读 API 调用）

```bash
# 主路径（CLI）
skill-quality-cli run --skill-name huawei-cloud-kms-key-list -- \
  python3 scripts/list_kms_keys.py --region cn-north-4; echo "rc=$?"

# 完整表格
skill-quality-cli run --skill-name huawei-cloud-kms-key-list -- \
  python3 scripts/list_kms_keys.py --table --region cn-north-4; echo "rc=$?"

# 原始 JSON
skill-quality-cli run --skill-name huawei-cloud-kms-key-list -- \
  python3 scripts/list_kms_keys.py --json --region cn-north-4

# SDK 回退
python3 scripts/list_kms_keys.py --backend sdk --region cn-north-4; echo "rc=$?"
```

判定标准：

- rc=0；输出为密钥列表（表格 + `共 N 个密钥` 汇总行）或空列表提示；
- `--json` 输出可被 `python3 -m json.tool` 解析；
- 表格里 region 列等于传入的 `--region`。

> 该账号在 `cn-north-4` 当前无自定义密钥时，冒烟应返回
> `当前区域无 KMS 密钥（区域: cn-north-4）。` 且 rc=0 —— 这是**通过**，不是失败。

## 4. 只读守卫验证（不需要凭据，不产生任何调用）

```bash
python3 scripts/list_kms_keys.py --alias create-me;            echo "rc=$?"   # 期望 rc=1
python3 scripts/list_kms_keys.py --action rotate;              echo "rc=$?"   # 期望 rc=1
python3 scripts/list_kms_keys.py --key-id delete-0d0466b0;     echo "rc=$?"   # 期望 rc=1
```

三个命令都不应出现任何 hcloud / SDK 调用痕迹（守卫在调用之前返回）。

## 5. 参数边界验证

```bash
python3 scripts/list_kms_keys.py --limit 0;     echo "rc=$?"   # rc=1，提示 1~200
python3 scripts/list_kms_keys.py --limit 201;   echo "rc=$?"   # rc=1，提示 1~200
python3 scripts/list_kms_keys.py --state foo;   echo "rc=$?"   # rc=1，提示可选值
```

## 6. 验收记录模板

| 检查项 | 结果 | 备注 |
|--------|------|------|
| `py_compile` / `bash -n` / `json.tool` | PASS / FAIL | |
| 离线单测 | N passed, 0 failed | |
| 真实只读冒烟（默认 / `--table` / `--json` / SDK） | rc + 输出摘要 | |
| 写意图拦截 | rc=1 | |
| references 五件套 | 齐全 | |