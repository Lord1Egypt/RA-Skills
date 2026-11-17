#!/usr/bin/env python3
import argparse, json, re, sys
from pathlib import Path

def convert(text):
    body=" ".join(x.strip() for x in text.splitlines() if x.strip() and not x.startswith("#"))
    if len(body)<35 or not re.search(r"[。！？]",body): raise ValueError("needs_more_source: 请提供包含人物和冲突的故事")
    return {"status":"scaffold","title":"未命名短剧","episode":1,"gaps":["本文件是占位示例，需由当前 AI 根据原文完成场次、动作与对白。"],"scenes":[{"scene_id":"E01-S01","slugline":"待确认","goal":"待改写","characters":[],"actions":[body[:36]],"dialogue":[],"conflict":{"obstacle":"待从原文确认","escalation":"待确认","result":"待确认"},"turn":"待确认","props":[],"ending_hook":"待编写"}]}

def write(data,out):
    if any((out/name).exists() for name in ("drama-script.json","drama-script.md")): raise ValueError("输出文件已存在，请选择新目录")
    out.mkdir(parents=True,exist_ok=True); (out/"drama-script.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    s=data["scenes"][0]; lines=[f"# {data['title']}","","> 占位示例，非完整剧本；请由 AI 根据原文完成改写。","",f"## {s['scene_id']} {s['slugline']}","",f"场次目标：{s['goal']}","", "### 动作"]+[f"- {a}" for a in s["actions"]]+["", "### 冲突", f"- 阻力：{s['conflict']['obstacle']}", f"- 升级：{s['conflict']['escalation']}", "", f"### 结尾钩子\n{s['ending_hook']}"]
    (out/"drama-script.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True); sub.add_parser("self-test"); c=sub.add_parser("convert"); c.add_argument("--input",required=True); c.add_argument("--output",required=True); a=p.parse_args()
    if a.cmd=="self-test":
        root=Path(__file__).parents[1]; sample=convert((root/"examples/success-input.md").read_text(encoding="utf-8")); assert sample["status"]=="scaffold" and sample["gaps"]
        try: convert((root/"examples/failure-input.md").read_text(encoding="utf-8"))
        except ValueError as e: assert str(e).startswith("needs_more_source")
        else: raise AssertionError("failure sample was accepted")
        print("self-test: PASS (labelled scaffold + failure sample)"); return
    try: write(convert(Path(a.input).read_text(encoding="utf-8")),Path(a.output))
    except (OSError,ValueError) as e: print(e,file=sys.stderr); return 1
    print("已生成占位示例，不是完整剧本；请由 AI 改编并用 render_script.py 输出成品。",file=sys.stderr)
    print("wrote drama-script.md and drama-script.json (scaffold)")
if __name__=="__main__": sys.exit(main() or 0)
