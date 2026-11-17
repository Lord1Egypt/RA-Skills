#!/usr/bin/env python3
"""gen-reference.py — 从 lib/registry.json 生成 references/actions.md。

改了注册表就重跑一次，手册和 `sc catalog` 永远同源：
    python3 scripts/gen-reference.py
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "lib" / "registry.json"
OUT = ROOT / "references" / "actions.md"

HEAD = """# 动作参数手册

本文件由 `scripts/gen-reference.py` 从 `lib/registry.json` 生成，不要手改。

参数键必须**逐字照抄**——写错会在生成阶段被拦，但改起来总比导进手机发现动作是空的省事。
`ident` 是 iOS 内部动作标识；要扩展新动作时才会用到。
"""

VAR_TABLE = """## 变量

| 变量 | 值 | 是否插入取动作 |
|---|---|---|
| `{clipboard}` | 剪贴板文本 | 是，`getclipboard` |
| `{battery}` | 电量百分比 | 是，`getbatterylevel` |
| `{location}` | 当前位置 | 是，`getcurrentlocation` |
| `{now}` | 当前时间 | 否，内置附件 |
| `{input}` | 快捷指令输入 | 否，内置附件 |
| `{repeat_item}` | 当前循环项 | 否，内置附件 |
| `{prev}` | 上一步输出 | 否，指向前一个动作 |

同一个变量在配方里出现多次，只会取一次。

`{prev}` 有个例外：上一步如果是 `shortcut.run` / `script.run`，它只是打开一个 URL，
拿不到输出，生成时会直接报错而不是让你在手机上发现条件永远不成立。
"""

EXTEND = """## 扩展：注册表里没有的动作

26 个是常用集合，`shortcutkit` 里还注册了 1700 多个。查一个动作长什么样：

```bash
python3 -c "import shortcutkit as sk, json; \\
print(json.dumps(sk.ACTIONS['is.workflow.actions.weather.forecast'], ensure_ascii=False, indent=2))"
```

查某类动作有哪些：

```bash
python3 -c "import shortcutkit as sk; print([k for k in sk.ACTIONS if 'weather' in k.lower()])"
```

然后在 `lib/registry.json` 的 `actions` 数组里加一条：

```json
{
  "alias": "weather.forecast",
  "ident": "is.workflow.actions.weather.forecast",
  "zh": "查天气预报",
  "doc": "取某个地点的天气预报，输出天气数据",
  "group": "媒体",
  "params": { "WFWeatherForecastType": { "desc": "daily / hourly / current", "type": "text" } },
  "notes": "未真机验证"
}
```

三条硬要求：

1. `ident` 必须在 `sk.ACTIONS` 里存在，否则生成时 `KeyError`
2. `params` 的键必须和 `sk.ACTIONS[ident]["params"]` 完全一致
3. 加完跑 `bash tests/selftest.sh`；没在手机上试过就在 `notes` 里写明，
   别让用户以为这是测过的

改完重跑 `python3 scripts/gen-reference.py` 更新本文件。

### 两段式动作：先取数据，再取字段

天气就是典型。`weather.forecast` 输出的是「天气数据」对象，不能直接用，
要再接一个 `properties.weather.conditions` 取具体字段：

```json
{ "do": "weather.forecast", "WFWeatherForecastType": "daily" },
{ "do": "weather.detail", "WFContentItemPropertyName": "降水概率" }
```

（这两条 alias 是示例，得先按上面的格式注册进 `lib/registry.json` 才能用。）

`properties.weather.conditions` 的 `WFContentItemPropertyName` 是**字段显示名**，
随 iOS 语言变化（中文系统上写「降水概率」，英文系统上写 `Precipitation Chance`）。
这类字段名没法离线枚举，接入前必须在目标手机上试一遍。

AppIntent 类动作（`com.apple.*`）参数通常是嵌套字典，比经典动作难写，
拿不准就先在手机上做一遍，再用 `sc` 反推结构。
"""


def main() -> int:
    reg = json.loads(REG.read_text(encoding="utf-8"))
    acts = reg["actions"]
    out = [HEAD]
    for g in reg["groups"]:
        rows = [a for a in acts if a["group"] == g]
        if not rows:
            continue
        out.append(f"## {g}\n")
        for a in rows:
            out.append(f"### `{a['alias']}` — {a['zh']}\n")
            out.append(f"{a['doc']}\n")
            out.append(f"- ident: `{a['ident']}`")
            if a.get("params"):
                ps = "、".join(
                    f"`{p}`" + (f"（{v.get('desc')}）" if isinstance(v, dict) and v.get("desc") else "")
                    for p, v in a["params"].items())
                out.append(f"- 参数: {ps}")
            else:
                out.append("- 参数: 无")
            if a.get("notes"):
                out.append(f"- 注意: {a['notes']}")
            if a.get("impl"):
                out.append("- 说明: 生成器特殊处理，会展开成多个 iOS 动作，"
                           "所以实际动作数比配方里看到的多")
            out.append("")
    out.append("---\n")
    out.append(VAR_TABLE)
    out.append("---\n")
    out.append(EXTEND)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"已生成 {OUT}（{len(acts)} 个动作，{OUT.stat().st_size} 字节）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
