# -*- coding: utf-8 -*-
"""模型卡生成器：给团队内任何 AI 系统生成一页『模型卡』。零依赖。

输出 Markdown（+JSON 可选）：身份/用途/数据/限制/风险/联系人。
三律映射：LGD-I 有籍 —— 每个 AI 系统都有一页可查的身份卡。

用法：
  python model_card_generator.py --name 客服摘要bot --org 运营部 --purpose "客服工单摘要" \
      --data "工单文本(内部)" --limits "只支持中文" --risks "摘要漏关键投诉" \
      --contact ops@example.com --out cards/kefu-bot.md
"""
import argparse, datetime, json, pathlib, sys


def main():
    ap = argparse.ArgumentParser(description="模型卡生成器 · 一页身份卡")
    ap.add_argument("--name", required=True, help="系统/智能体名称")
    ap.add_argument("--org", default="", help="所属团队")
    ap.add_argument("--purpose", required=True, help="用途（一句话）")
    ap.add_argument("--data", default="未填写", help="训练/处理数据说明")
    ap.add_argument("--limits", nargs="*", default=[], help="已知限制")
    ap.add_argument("--risks", nargs="*", default=[], help="主要风险与缓解")
    ap.add_argument("--contact", default="未填写", help="负责人/联系方式")
    ap.add_argument("--out", help="输出 Markdown 路径")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    card = {
        "name": a.name, "org": a.org or "未填写", "purpose": a.purpose,
        "data": a.data,
        "limits": a.limits or ["未填写"],
        "risks": a.risks or ["未填写"],
        "contact": a.contact,
        "generated_at": datetime.date.today().isoformat(),
    }
    md = ["# 模型卡 · " + a.name, "",
          f"- **所属**：{card['org']}",
          f"- **用途**：{card['purpose']}",
          f"- **数据**：{card['data']}",
          "- **已知限制**："] + [f"  - {x}" for x in card["limits"]] + \
         ["- **主要风险**："] + [f"  - {x}" for x in card["risks"]] + \
         [f"- **负责人**：{card['contact']}",
          f"- **生成日期**：{card['generated_at']}", "",
          "> 本卡为 LGD『有籍』身份件：系统变更时应更新此卡。口径以各法域官方要求为准。"]
    text = "\n".join(md)
    if a.out:
        outp = pathlib.Path(a.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(text, encoding="utf-8")
    if a.json:
        print(json.dumps({"card": card, "markdown": text, "out": a.out},
                         ensure_ascii=False, indent=2))
    else:
        print(text)
        if a.out:
            print("\n已写出：", a.out)
    sys.exit(0)


if __name__ == "__main__":
    main()
