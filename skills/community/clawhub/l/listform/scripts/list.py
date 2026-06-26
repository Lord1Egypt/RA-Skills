#!/usr/bin/env python3
"""智能表单 list - 数据操作脚本"""
import json, os, sys, uuid, argparse
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__),"..","..","memory","list-data")

def _path(t):
    return os.path.join(DATA_DIR,f"{t}.json")

def _load(t):
    p=_path(t)
    if not os.path.exists(p):
        return {"config":{"fields":{}},"records":[]}
    with open(p) as f: return json.load(f)

def _save(t,data):
    os.makedirs(DATA_DIR,exist_ok=True)
    with open(_path(t),"w") as f: json.dump(data,f,ensure_ascii=False,indent=2)

def cmd_types():
    os.makedirs(DATA_DIR,exist_ok=True)
    types=[f.replace(".json","") for f in os.listdir(DATA_DIR) if f.endswith(".json")]
    if not types:
        print(json.dumps({"types":[],"note":"暂无记录类型"},ensure_ascii=False))
        return
    res=[]
    for t in types:
        d=_load(t)
        fields=d["config"].get("fields",{})
        count=len(d["records"])
        res.append({"type":t,"fields":fields,"count":count})
    print(json.dumps({"types":res},ensure_ascii=False))

def cmd_new_type(t,fields):
    if os.path.exists(_path(t)):
        print(json.dumps({"error":f"类型 '{t}' 已存在"},ensure_ascii=False))
        sys.exit(1)
    _save(t,{"config":{"fields":fields},"records":[]})
    print(json.dumps({"ok":True,"type":t,"fields":fields},ensure_ascii=False))

def cmd_add(t,data,image=None):
    d=_load(t)
    rec={
        "id":uuid.uuid4().hex[:12],
        "timestamp":datetime.now().astimezone().isoformat(),
        "data":data,
        "tags":data.pop("tags",[]),
        "attachments":[]
    }
    if image:
        os.makedirs(os.path.join(DATA_DIR,"attachments"),exist_ok=True)
        ext=os.path.splitext(image)[1] or ".file"
        fname=f"{rec['id']}{ext}"
        dst=os.path.join(DATA_DIR,"attachments",fname)
        import shutil
        shutil.copy2(image,dst)
        rec["attachments"].append(fname)
    d["records"].append(rec)
    _save(t,d)
    print(json.dumps({"ok":True,"id":rec["id"],"timestamp":rec["timestamp"]},ensure_ascii=False))

def cmd_query(t,from_date,to_date,filter_json):
    d=_load(t)
    if from_date:
        d["records"]=[r for r in d["records"] if r["timestamp"][:10]>=from_date]
    if to_date:
        d["records"]=[r for r in d["records"] if r["timestamp"][:10]<=to_date]
    if filter_json:
        f=json.loads(filter_json)
        def match(r):
            for k,v in f.items():
                rv=r["data"].get(k)
                if isinstance(v,str) and isinstance(rv,str):
                    if v.lower() not in rv.lower(): return False
                elif rv!=v: return False
            return True
        d["records"]=[r for r in d["records"] if match(r)]
    d["count"]=len(d["records"])
    print(json.dumps(d,ensure_ascii=False))

def cmd_summary(t,from_date,to_date,group_by):
    d=_load(t)
    orig=len(d["records"])
    if from_date:
        d["records"]=[r for r in d["records"] if r["timestamp"][:10]>=from_date]
    if to_date:
        d["records"]=[r for r in d["records"] if r["timestamp"][:10]<=to_date]
    total=len(d["records"])
    gb=group_by or "category"
    groups={}
    for r in d["records"]:
        val=r["data"].get(gb,"未分类")
        amt=r["data"].get("amount",0)
        try: amt=float(amt)
        except: amt=0
        if val not in groups: groups[val]={"count":0,"total":0.0}
        groups[val]["count"]+=1
        groups[val]["total"]+=amt
    out={
        "type":t,"group_by":gb,"total_records":total,
        "total_records_before_filter":orig,
        "groups":{k:{"count":v["count"],"total":round(v["total"],2)} for k,v in sorted(groups.items(),key=lambda x:-x[1]["total"])}
    }
    if "amount" in d["config"].get("fields",{}):
        out["grand_total"]=round(sum(v["total"] for v in groups.values()),2)
    print(json.dumps(out,ensure_ascii=False))

def cmd_delete(t,rid):
    d=_load(t)
    before=len(d["records"])
    d["records"]=[r for r in d["records"] if r["id"]!=rid]
    if len(d["records"])==before:
        print(json.dumps({"error":f"未找到id: {rid}"},ensure_ascii=False))
        sys.exit(1)
    _save(t,d)
    print(json.dumps({"ok":True,"deleted":rid},ensure_ascii=False))

def main():
    p=argparse.ArgumentParser(prog="list.py")
    sp=p.add_subparsers(dest="cmd",required=True)

    p_types=sp.add_parser("types")
    p_new=sp.add_parser("new-type")
    p_new.add_argument("type")
    p_new.add_argument("--fields",required=True)

    p_add=sp.add_parser("add")
    p_add.add_argument("type")
    p_add.add_argument("--data",required=True)
    p_add.add_argument("--image")

    p_q=sp.add_parser("query")
    p_q.add_argument("type")
    p_q.add_argument("--from",dest="from_date")
    p_q.add_argument("--to",dest="to_date")
    p_q.add_argument("--filter")

    p_s=sp.add_parser("summary")
    p_s.add_argument("type")
    p_s.add_argument("--from",dest="from_date")
    p_s.add_argument("--to",dest="to_date")
    p_s.add_argument("--by",dest="group_by",default="category")

    p_del=sp.add_parser("delete")
    p_del.add_argument("type")
    p_del.add_argument("id")

    a=p.parse_args()
    if a.cmd=="types": cmd_types()
    elif a.cmd=="new-type": cmd_new_type(a.type,json.loads(a.fields))
    elif a.cmd=="add": cmd_add(a.type,json.loads(a.data),a.image)
    elif a.cmd=="query": cmd_query(a.type,a.from_date,a.to_date,a.filter)
    elif a.cmd=="summary": cmd_summary(a.type,a.from_date,a.to_date,a.group_by)
    elif a.cmd=="delete": cmd_delete(a.type,a.id)

if __name__=="__main__":
    main()
