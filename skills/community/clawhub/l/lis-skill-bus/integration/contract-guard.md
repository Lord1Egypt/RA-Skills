# contract_guard 接入说明（给 s2 / s5 用）

> 版本：v1.0.0（2026-11-09）
> canonical：`${CODEX_HOME:-$HOME/.codex}/skills/lis-skill-bus/lib/contract_guard.py`
> 同步工具：`${CODEX_HOME:-$HOME/.codex}/skills/lis-skill-bus/scripts/sync_contract_guard.py`
> 自测：`python3 lib/contract_guard.py --self-test`（6/6）

## 1. 它解决什么问题

过去「只允许 cad-file-reader 识图、只允许 lis-skill-bus 传契约」只写在 `SKILL.md`，代码不校验来源，手工 JSON 与 reader 产物同门进入。`contract_guard` 把来源判断变成代码：

| 输入 | 结果 |
|---|---|
| `provenance=reader/bus` + 非空 `contract_id` + 哈希一致 | `mode=formal`，`formal_ledger_eligible=True` |
| `provenance=manual`（或缺失）且 `allow_manual=True` | `mode=manual`，`final_quantity=False`、`formal_ledger_eligible=False` |
| 手工契约但调用方没给 `allow_manual=True` | `GuardError(3)` |
| `contract_sha256` 存在但与契约文件实算 SHA-256 不同 | `GuardError(2)` |
| `schema` / `contract_version` 不是 `cad-contract/v1` | `GuardError(4)` |
| 坐标单位不是 `mm` 且没有 `unit_scale` | `GuardError(4)` |
| 顶层缺 `required_keys` | `GuardError(2)` |
| 文件不存在 / JSON 解析失败 | `GuardError(2)` |

错误码：`1 缺依赖 / 2 输入不合法 / 3 来源未授权 / 4 版本或单位不一致 / 5 数据不足`。
每条 `GuardError` 都有 `message`（给人看）和 `hint`（可复制命令），入口脚本不要吞掉 `hint`。

## 2. 安装/同步到算量技能

s1 只建 canonical，**尚未接入任何业务技能**。s2/s5 接入时先同步副本：

```bash
cd ${CODEX_HOME:-$HOME/.codex}/skills/lis-skill-bus

# 先看 5 个技能里有没有副本、是否一致（缺副本不算失败）
python3 scripts/sync_contract_guard.py --check

# 复制 canonical 并写 vendored 头（覆盖前自动备份）
python3 scripts/sync_contract_guard.py --apply --skills gangjiegou-suanliang

# 接入完再全量校验
python3 scripts/sync_contract_guard.py --check
```

副本首行固定为：

```text
# VENDORED from lis-skill-bus/lib/contract_guard.py sha256:<canonical 哈希>
```

规则：

- `--check` 遇到 `missing` 只打印、不失败；`stale` / `hand-edited` 会 `exit 1`。
- `--apply` 对无 vendored 头且内容不一致的文件默认 `REFUSE`（疑似手改），必须人工核对后加 `--force`，且 `--force` 也会先备份成 `contract_guard.py.bak.<时间戳>`。
- 沙箱验证用 `--dest-root <目录>`：把该目录下每个一级子目录当作一个技能，不会碰真实技能。

## 3. 最小接入代码（算量技能主入口）

副本在 `<skill>/scripts/contract_guard.py`，同目录脚本可直接导入：

```python
from contract_guard import GuardError, guard_contract, stamp_result

def load_contract_or_exit(path: str, allow_manual: bool) -> dict:
    try:
        guard = guard_contract(
            path,
            allow_manual=allow_manual,          # 只由命令行 --allow-manual 传 True
            required_keys=("schema", "contract"),  # 按技能实际需要补
        )
    except GuardError as exc:
        print(f"[contract] {exc.message}", file=sys.stderr)
        if exc.hint:
            print(f"[contract] 修复: {exc.hint}", file=sys.stderr)
        raise SystemExit(exc.code)
    for warning in guard["warnings"]:
        print(f"[contract] WARN: {warning}", file=sys.stderr)
    return guard

guard = load_contract_or_exit(args.steel, args.allow_manual)
result = build_result(...)                 # 原有算量逻辑
result = stamp_result(result, guard)       # 必须放在写文件之前
```

`stamp_result` 会补：

- `provenance`（reader / bus / manual）
- `contract_id`
- `source_sha256`（原图哈希）
- `contract_sha256`（契约文件哈希）
- `contract_mode`（formal / manual）
- `formal_ledger_eligible`（只有 formal 为 True）
- `contract_warnings`（如有）

`mode=manual` 时**强制** `final_quantity=False`，即使算量结果里原本写了 `True`。

## 4. 入口参数约定（s2/s5 统一）

```text
--allow-manual     显式允许手工契约；不加时手工契约直接 exit 3
--contract PATH    契约路径（已有 --steel 等参数保持不变）
```

建议：

- 默认**不加** `--allow-manual`；只有用户明确说“我手工给数据”时才加。
- 用 `--allow-manual` 时在输出开头打印一行：`手工契约模式：final_quantity=false，不可进正式台账`。
- 技能内部不要读 `CAD_ALLOW_DIRECT` 之类的环境变量来绕过闸门；`allow_manual` 只能来自显式参数。
- 原来的 `CAD_ALLOW_DIRECT=1` 逃生口只用于开发/回归，且必须在输出里标记 `debug_direct=true`，不得静默。

## 5. 错误处理模板

```python
try:
    guard = guard_contract(path, allow_manual=args.allow_manual, required_keys=(...))
except GuardError as exc:
    # 不要改写成“继续算”；缺来源就算量，正是这次要堵的洞
    print(f"契约不可用（code={exc.code}）：{exc.message}", file=sys.stderr)
    if exc.hint:
        print(f"修复：{exc.hint}", file=sys.stderr)
    return exc.code
```

| code | 入口应怎么处理 |
|---|---|
| 1 | 提示安装 cad-file-reader / lis-skill-bus，给安装命令，停止算量 |
| 2 | 原样打印 message + hint（路径/JSON/哈希/缺键），停止 |
| 3 | 提示“手工契约需 --allow-manual”，或让用户重跑 reader；停止 |
| 4 | 打印版本/单位修复命令，停止；不要自动改用户契约 |
| 5 | 数据不足，列缺哪些字段；停止 |

## 6. CLI 直接排错

```bash
# 只看结论
python3 lib/contract_guard.py /path/to/contract.json

# 手工契约（输出会标 manual）
python3 lib/contract_guard.py /path/to/contract.json --allow-manual

# 完整 JSON（含 contract 原文）
python3 lib/contract_guard.py /path/to/contract.json --json

# 自定义必需键
python3 lib/contract_guard.py /path/to/contract.json --require-key project_key --require-key contract
```

退出码等于 `GuardError.code`，可直接被 shell / 回归脚本判断。

## 7. 契约最小字段

```json
{
  "schema": "cad-contract/v1",
  "contract_id": "cad-20261109-0001",
  "provenance": "reader",
  "coordinate_unit": "mm",
  "source": {"file": "plan.dwg", "sha256": "<原图 64 位哈希>"},
  "contract": {}
}
```

- `source.sha256` = **原图**哈希，写入结果字段 `source_sha256`。
- `contract_sha256`（可选）= **契约文件自身**哈希，用于发现契约被替换；guard 返回的 `contract_sha256` 永远是实算值。
- `provenance` 缺失按 `manual` 处理，不按 `reader`。
- 坐标单位不是 `mm` 时必须给 `unit_scale`（换算到 mm 的系数），否则 `GuardError(4)`。
- 契约版本也可用 `contract_version` 声明，但推荐顶层同时写 `schema`。

## 8. 验证清单（接入后每条都要跑）

```bash
cd ${CODEX_HOME:-$HOME/.codex}/skills/lis-skill-bus
python3 lib/contract_guard.py --self-test
python3 tests/test_contract_guard.py
python3 scripts/sync_contract_guard.py --check
python3 -m py_compile lib/contract_guard.py scripts/sync_contract_guard.py
```

业务技能侧至少加 3 条入口测试：

1. reader 契约 → 正常算量，结果 `formal_ledger_eligible=true`；
2. 手工契约不加 `--allow-manual` → `exit 3`，不写结果文件；
3. 手工契约加 `--allow-manual` → `final_quantity=false`，输出标记 manual。

## 9. 边界

- 本模块不联网、不读环境变量决定放行、不解析图纸。
- 它只判断“这份契约能不能进算量”，不替代 cad-file-reader 的识图质量复核。
- `formal` 只代表来源与完整性通过，不代表工程量已复核；算量技能自己的置信度/复核字段照旧输出。
