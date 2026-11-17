# 阵型图 JSON 结构与渲染契约

> 本文件是 `scripts/formation_diagram.py` 的输入/输出契约。SKILL.md 的 Step 7 渲染前必读。

## 目录

- [JSON 结构](#json-结构)
- [字段说明](#字段说明)
- [位置代码](#位置代码)
- [渲染行为契约（v1.4 起：绝不静默）](#渲染行为契约v14-起绝不静默)
- [命令、退出码与 --strict](#命令退出码与---strict)

## JSON 结构

```json
{
  "topic": "主题名（string，必填）",
  "formation": "4-3-3（string，必填，可选：4-3-3/4-2-3-1/4-3-2-1/4-4-2/4-5-1/4-1-4-1/3-5-2/3-4-3）",
  "coach": {
    "name": "主教练名（string，必填，= 一句话核心思想）",
    "desc": "一句话说明（string，可选）"
  },
  "players": [
    {
      "pos": "CB（string，必填，位置代码）",
      "name": "知识点名（string，必填）",
      "desc": "一句话说明（string，可选，不画进 SVG）"
    }
  ],
  "bench": [
    {
      "name": "替补知识点名（string，必填）",
      "desc": "一句话说明（string，可选）"
    }
  ],
  "flow": ["GK", "CB", "CDM", "AMD", "CF"],
  "b_team": {
    "formation": "3-4-3（string，可选）",
    "topic": "B 队主题（string，可选，默认“主题·进阶”）",
    "coach": {"name": "B队教练", "desc": "次级核心思想"},
    "players": [{"pos": "CM", "name": "扩展知识点", "desc": "一句话"}],
    "bench": [],
    "flow": ["GK", "CB", "CM", "CF"]
  }
}
```

## 字段说明

| 字段 | 必填 | 说明 |
|---|---|---|
| `topic` | 是 | 主题名，画在阵型图标题第一行 |
| `formation` | 是 | 阵型代码，决定槽位数量与坐标 |
| `coach` | 是 | 主教练（HC），`name` 必须是一句话核心思想 |
| `players` | 是 | 首发球员列表，按 `pos` 归位；同名位置按出现顺序填槽 |
| `bench` | 否 | 替补席（进阶/边角知识点） |
| `flow` | 否 | 学习路径（球路），按位置代码顺序画虚线箭头 |
| `b_team` | 否 | 第二阵容（>20 知识点时启用），结构与主队相同，画面水平翻转成对攻态势 |

## 位置代码

`GK RB CB LB CDM CM CAM AMD LAM RAM RM LM LW RW CF SS`

- `CAM` 与 `AMD` 互为别名（都归到前腰槽）。
- 位置职能映射见 `references/positions.md`，阵型槽位数见 `references/formations.md`。

## 渲染行为契约（v1.4 起：绝不静默）

脚本对任何“内容可能丢失/被改写”的情况都会在 **stderr 明确告警**，不会静默处理：

1. **同名位置超额（T1/N2）**：某位置人数超过阵型槽位（如 4-3-3 只有 2 个 CB 槽却给了 3 个 CB），多出的球员**转入替补席**并告警，列出位置、槽位数、多出人数与球员名——一个都不会消失。
2. **位置不在阵型中**：该球员转入替补席并告警。
3. **CAM/AMD 别名归一**：两者争同一组前腰槽，超额同样按第 1 条处理。
4. **flow 含阵型外代码（T6）**：跳过该点并逐条告警（报告用户写的原始代码，去重保序）；有效节点不足 2 个时不画箭头并再次告警。
5. **flow 同名多槽语义（N3）**：flow 中同名多槽位置（如两个 CB）默认连接**第一个**槽；需要区分 CB#1/CB#2 的消歧能力排 v2.0。
6. **长名字不截断（T2）**：球员名/替补名按单词（英文）或字符（中文）完整折行，超长时动态缩小字号，绝不硬截断或加省略号。
7. **替补席不溢出画布（T8）**：画布高度随替补行数自适应。
8. **非法输入（T5）**：阵型不支持、JSON 解析失败、文件不存在 → 打印中文错误并以退出码 2 结束，不抛裸 Traceback。

## 命令、退出码与 --strict

命令（按本机环境选择可用的 Python，回退链 `python3` → `python` → `py -3`）：

```bash
python3 scripts/formation_diagram.py team.json output.svg
python3 scripts/formation_diagram.py team.json output.svg --strict
```

| 退出码 | 含义 |
|---|---|
| 0 | 成功，SVG 已生成（stderr 可能仍有警告，交付前必须逐条处理） |
| 2 | 参数错误 / 输入文件不存在 / JSON 解析失败 / 阵型不支持 |
| 3 | `--strict` 模式下存在任何警告（SVG 仍会生成，便于排查） |

**交付前自检**：正式交付前用 `--strict` 再跑一次；退出码非 0 不得交付。出现告警时优先修 JSON（换阵型、把多余球员挪进 `bench`、修正 `flow`），而不是忽略告警。
