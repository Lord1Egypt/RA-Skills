#!/usr/bin/env python3
import sys,re,os,json,hashlib,base64,html,urllib.parse,datetime,unicodedata

if len(sys.argv) != 11:
    print(json.dumps({"ok":False,"error":"usage: psl-core.py <type> <mode> <rules_dir> <log_path> <input> <actor_id> <rl_state_path> <rl_max_req> <rl_window_sec> <rl_action>"}, ensure_ascii=False))
    sys.exit(2)

type_,mode,rules_dir,log_path,text,actor_id,rl_state_path,rl_max_req,rl_window_sec,rl_action=sys.argv[1:11]
rl_max_req=int(rl_max_req)
rl_window_sec=int(rl_window_sec)


def normalize(s:str):
    s=unicodedata.normalize("NFKC",s)
    for ch in ["\u200b","\u200c","\u200d","\ufeff","\u2060","\u202a","\u202b","\u202e"]:
        s=s.replace(ch,"")
    m={"а":"a","е":"e","о":"o","р":"p","с":"c","у":"y","х":"x","і":"i","Ａ":"A"}
    s="".join(m.get(c,c) for c in s)
    s=re.sub(r'(?i)\b([a-z])(?:[+._-]([a-z])){2,}\b', lambda m: re.sub(r'[^a-zA-Z]','',m.group(0)), s)
    s=re.sub(r'(?i)\b(?:[a-z]\s+){3,}[a-z]\b', lambda m: m.group(0).replace(' ',''), s)
    return s


def decode_variants(s:str):
    out=[("original",s)]
    candidates=[]
    u=urllib.parse.unquote(s)
    if u!=s: candidates.append(("decoded_url",u))
    h=html.unescape(s)
    if h!=s: candidates.append(("decoded_html",h))
    try:
        ue=s.encode('utf-8').decode('unicode_escape')
        if ue!=s and "\\u" in s: candidates.append(("decoded_unicode",ue))
    except Exception:
        pass
    b64=re.sub(r'\s+','',s)
    if re.fullmatch(r'[A-Za-z0-9+/=]{16,}',b64):
        try:
            dec=base64.b64decode(b64,validate=True).decode('utf-8','ignore')
            if dec and sum(c.isprintable() for c in dec)/max(1,len(dec))>0.85:
                candidates.append(("decoded_base64",dec))
        except Exception:
            pass
    seen={s}
    for n,v in candidates:
        if v not in seen:
            out.append((n,v)); seen.add(v)
    return out


def load_patterns(name, level):
    p=os.path.join(rules_dir,name)
    arr=[]
    if not os.path.exists(p):
        return arr
    i=0
    for raw in open(p,encoding='utf-8'):
        line=raw.strip()
        if not line or line.startswith('#'):
            continue
        i+=1
        if '::' in line:
            rid,pat=line.split('::',1)
            rid=rid.strip() or f"{level}:L{i}"
        else:
            rid=f"{level}:L{i}"
            pat=line
        arr.append((rid,pat))
    return arr


def rate_limit_check(path:str, actor:str, now_ts:int, max_req:int, window_sec:int):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data={"actors":{}}
    if os.path.exists(path):
        try:
            with open(path,encoding='utf-8') as f:
                data=json.load(f)
        except Exception:
            data={"actors":{}}
    actors=data.setdefault("actors",{})
    arr=actors.get(actor,[])
    arr=[t for t in arr if isinstance(t,(int,float)) and (now_ts-int(t)) < window_sec]
    arr.append(now_ts)
    actors[actor]=arr

    for k in list(actors.keys()):
        if k==actor:
            continue
        old=[t for t in actors.get(k,[]) if isinstance(t,(int,float)) and (now_ts-int(t)) < window_sec]
        if old:
            actors[k]=old
        else:
            del actors[k]

    with open(path,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False)
    return len(arr), len(arr) > max_req


critical=load_patterns('critical.regex','critical')
high=load_patterns('high.regex','high')
medium=load_patterns('medium.regex','medium')
allowlist=load_patterns('allowlist.regex','allow')

orig=text
norm=normalize(text)
variants=decode_variants(norm)
reasons=[]
sev=0
hit_count=0
matched_rules=[]

for vname,vtext in variants:
    vlow=vtext.lower()
    if vname!="original":
        reasons.append(vname)
    for rid,pat in critical:
        if re.search(pat,vlow,re.I):
            sev=max(sev,4); hit_count+=1; reasons.append("critical"); matched_rules.append(rid)
    for rid,pat in high:
        if re.search(pat,vlow,re.I):
            sev=max(sev,3); hit_count+=1; reasons.append("high"); matched_rules.append(rid)
    for rid,pat in medium:
        if re.search(pat,vlow,re.I):
            sev=max(sev,2); hit_count+=1; reasons.append("medium"); matched_rules.append(rid)

if type_ == "action":
    alow=norm.lower()
    gates=[
        (r'\b(rm|mv|cp|sed|truncate)\b.*\b(/etc/|/usr/|~/.ssh|authorized_keys|memory/|SOUL\.md|AGENTS\.md|MEMORY\.md)', 'ACT_FILE_DESTRUCT_OR_CORE_TOUCH', 4),
        (r'\b(chmod\s+777|chown\s+-R)\b', 'ACT_PERM_WIDEN', 2),
        (r'\b(curl|wget)\b.*\b(webhook\.site|ngrok|pastebin|transfer\.sh)\b', 'ACT_EXFIL_ENDPOINT', 4),
        (r'\b(openclaw\s+gateway\s+(stop|restart))\b', 'ACT_SERVICE_CONTROL', 3),
        (r'\b(ssh|scp)\b.*\b(id_rsa|known_hosts|authorized_keys)\b', 'ACT_SSH_SENSITIVE', 3),
    ]
    for pat,rid,level in gates:
        if re.search(pat, alow, re.I):
            sev=max(sev,level); reasons.append('action_gate'); matched_rules.append(rid); hit_count+=1

allow_hit=False
for rid,pat in allowlist:
    if re.search(pat,norm,re.I):
        allow_hit=True
        matched_rules.append(rid)

if allow_hit:
    sev=max(0,sev-1)
    reasons.append("allowlist_context")

sanitized=None
if type_=="send":
    sanitized=orig
    redactions=[
        (r"sk-proj-[A-Za-z0-9_\-]{20,}","[REDACTED:openai_project_key]"),
        (r"sk-[A-Za-z0-9]{20,}","[REDACTED:openai_api_key]"),
        (r"github_pat_[A-Za-z0-9_]{20,}","[REDACTED:github_fine_grained_token]"),
        (r"ghp_[A-Za-z0-9]{20,}","[REDACTED:github_token]"),
        (r"AKIA[0-9A-Z]{16}","[REDACTED:aws_key]"),
        (r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----","[REDACTED:private_key_block]"),
        (r"-----BEGIN [A-Z ]*PRIVATE KEY-----","[REDACTED:private_key]"),
        (r"eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+","[REDACTED:jwt]"),
        (r"Bearer\s+[a-zA-Z0-9\-._~+/]+=*","[REDACTED:bearer_token]"),
        (r"xox[baprs]-[a-zA-Z0-9\-]{10,}","[REDACTED:slack_token]"),
        (r"hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[a-zA-Z0-9]+","[REDACTED:slack_webhook]"),
        (r"AIza[0-9A-Za-z\-_]{35}","[REDACTED:google_api_key]"),
        (r"bot[0-9]{8,10}:[A-Za-z0-9_-]{20,}","[REDACTED:telegram_token]"),
        (r"([A-Za-z]:)?/(Users|home)/[^\s]+","[REDACTED:local_path]"),
    ]
    changed=False
    for pat,rep in redactions:
        new=re.sub(pat,rep,sanitized)
        if new!=sanitized:
            changed=True
            sanitized=new
    if changed and sev<3:
        sev=max(sev,2)
        reasons.append("redacted_output")

now_ts=int(datetime.datetime.now(datetime.timezone.utc).timestamp())
req_count,rl_exceeded=rate_limit_check(rl_state_path, actor_id, now_ts, rl_max_req, rl_window_sec)
if rl_exceeded:
    reasons.append('rate_limit_exceeded')
    matched_rules.append('RL_PER_ACTOR')
    if rl_action == 'warn':
        sev=max(sev,2)
    else:
        sev=max(sev,4)

if mode not in {"strict","balanced","lowfp"}:
    mode="balanced"

if mode=="strict":
    action="block" if sev>=2 else ("warn" if sev==1 else "allow")
elif mode=="lowfp":
    action="block" if sev>=3 else ("warn" if sev==2 else "allow")
else:
    action="block" if sev>=3 else ("warn" if sev==2 else "allow")

sev_name={0:"SAFE",1:"LOW",2:"MEDIUM",3:"HIGH",4:"CRITICAL"}.get(sev,"SAFE")
reasons_sorted=sorted(set(reasons))
matched_sorted=sorted(set(matched_rules))

confidence=min(0.99, round(0.20 + (sev*0.18) + (min(hit_count,5)*0.08) + (0.07 if any(r.startswith('decoded_') for r in reasons_sorted) else 0), 2))

fp=hashlib.sha256((norm+"|"+"|".join(reasons_sorted)+"|"+"|".join(matched_sorted)).encode()).hexdigest()[:16]
result={
    "ok": action!="block",
    "severity": sev_name,
    "confidence": confidence,
    "action": action,
    "reasons": reasons_sorted,
    "matched_rules": matched_sorted,
    "mode": mode,
    "fingerprint": fp,
    "sanitized_text": sanitized,
    "type": type_,
    "actor_id": actor_id,
    "rate_limit": {"count_in_window": req_count, "max": rl_max_req, "window_sec": rl_window_sec},
}
print(json.dumps(result,ensure_ascii=False))

os.makedirs(os.path.dirname(log_path),exist_ok=True)
prev_hash=""
if os.path.exists(log_path):
    try:
        with open(log_path,'rb') as f:
            f.seek(0,2)
            size=f.tell()
            block=min(size, 8192)
            f.seek(max(0,size-block))
            tail=f.read().decode('utf-8','ignore').strip().splitlines()
            if tail:
                last=json.loads(tail[-1])
                prev_hash=last.get('entry_hash','')
    except Exception:
        prev_hash=""

log={
    "ts":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "type":type_,
    "actor_id":actor_id,
    "severity":sev_name,
    "confidence":confidence,
    "action":action,
    "reasons":reasons_sorted,
    "matched_rules":matched_sorted,
    "fingerprint":fp,
    "mode":mode,
    "hits":hit_count,
    "rate_limit_count": req_count,
    "prev_hash": prev_hash,
}
entry_hash=hashlib.sha256(json.dumps(log,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
log["entry_hash"]=entry_hash

with open(log_path,'a',encoding='utf-8') as f:
    f.write(json.dumps(log,ensure_ascii=False)+"\n")

if action=="block":
    sys.exit(20)
if action=="warn":
    sys.exit(10)
sys.exit(0)
