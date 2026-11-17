#!/usr/bin/env python3
"""LINK42 Agent transport: stdlib-only SDK, no command-line secrets or paid retries."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import sys
import unicodedata
import uuid
import time
from urllib.request import Request, build_opener, HTTPRedirectHandler

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"lib"))
from link42 import Link42, Link42Error, PollTimeoutError, TaskFailedError

OPERATIONS=("discover","doctor","plan","workflow-plan","model-get","estimate","chat","responses","messages","count-tokens","gemini","embeddings","image","image-edit","image-create","image-get","image-wait","video-create","video-get","video-list","video-wait","video-cancel","asset-begin","asset-upload","asset-list","asset-get","asset-delete","asset-complete","usage-report","usage-logs","usage-csv","score")
MUTATIONS={"chat","responses","messages","gemini","embeddings","image","image-edit","image-create","video-create","video-cancel","asset-begin","asset-upload","asset-delete","asset-complete","score"}
QUOTE_ENDPOINTS={"chat":"chat/completions","image":"images/generations","image-create":"images/generations","video-create":"videos"}

def redact(value):
    text=str(value)
    text=re.sub(r"\b(?:ark|sk|ak)-[A-Za-z0-9_-]{4,}","[REDACTED]",text)
    text=re.sub(r"(?i)bearer\s+\S+","Bearer [REDACTED]",text)
    return text[:800]

def normalized(value):
    return "".join(ch for ch in unicodedata.normalize("NFKC",value).casefold() if ch.isalnum())

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None

def discover(client,options=None):
    allowed=client.models.list(**(options or {})).get("data",[])
    metadata={}
    try:
        request=Request(client.base_url+"/api/control/models?page=1&page_size=200",headers={"Accept":"application/json"})
        with build_opener(NoRedirect()).open(request,timeout=min(client.timeout,15)) as response:
            public=json.load(response)
        for model in (public.get("data") or public).get("list",[]): metadata[model["name"]]=model
    except Exception: pass  # Basic authenticated discovery still works; never fabricate capabilities.
    return [{**model,"details":metadata.get(model["id"]),"capabilities_known":model["id"] in metadata} for model in allowed]

def choose(models,name=None,modality=None):
    eligible=[m for m in models if not modality or m.get("modality")==modality]
    if name:
        wanted=normalized(name)
        eligible=[m for m in eligible if wanted in {normalized(str(v)) for v in [m["id"],m.get("display_name",""),*(m.get("details") or {}).get("aliases",[])]}]
    if len(eligible)!=1: raise ValueError("Model selection is missing or ambiguous; use an exact authorized API id from discover")
    return eligible[0]["id"]

def estimate(client,endpoint,payload,options=None):
    return client.estimates.create(endpoint=endpoint,payload=payload,request_options={**(options or {}),"retries":0})

def validate_options(model,operation,payload):
    detail=model.get("details") or {}
    if operation in {"image","image-create"}:
        opts=detail.get("image_options") or {}
        size=payload.get("size")
        if size and opts.get("sizes") and size not in opts["sizes"]:
            match=re.fullmatch(r"(\d+)x(\d+)",str(size))
            if not match or not opts.get("allow_custom_size"):raise ValueError("Unsupported image size")
            area=int(match[1])*int(match[2])
            if not opts.get("min_pixels",1)<=area<=opts.get("max_pixels",2**63):raise ValueError("Image dimensions exceed the model pixel range")
        count=payload.get("n",1)
        if not isinstance(count,int) or count<1 or count>opts.get("max_images",9):raise ValueError("Unsupported image count")
    if operation=="video-create":
        opts=detail.get("video_options") or {}
        for key,allowed in [("resolution",opts.get("resolutions")),("ratio",opts.get("ratios")),("output_format",opts.get("output_formats"))]:
            if key in payload and allowed and payload[key] not in allowed:raise ValueError("Unsupported video "+key)
        duration=payload.get("duration")
        if duration is not None:
            if duration==-1 and not opts.get("smart_duration"):raise ValueError("Automatic duration is unsupported")
            if duration!=-1 and not opts.get("duration_min",1)<=duration<=opts.get("duration_max",120):raise ValueError("Unsupported video duration")
        if "n" in payload:raise ValueError("Videos are separate tasks; do not invent a provider n parameter")

def plan(client,payload,options=None):
    operation=payload.get("operation")
    if operation not in QUOTE_ENDPOINTS:raise ValueError("Planning supports chat, image/image-create and video-create")
    body=dict(payload.get("request") or {})
    models=discover(client,options)
    modality={"chat":"text","image":"image","image-create":"image","video-create":"video"}[operation]
    model_id=choose(models,payload.get("model") or body.get("model"),modality)
    model=next(m for m in models if m["id"]==model_id)
    body["model"]=model_id;validate_options(model,operation,body)
    quote=estimate(client,QUOTE_ENDPOINTS[operation],body,options)
    return {"operation":operation,"request":body,"quote":quote,"capabilities_known":model.get("capabilities_known",False),"submitted":False,"upstream_execution_checked":False}

def workflow_plan(client,payload,options=None):
    stages=payload.get("stages")
    if not isinstance(stages,list) or not 1<=len(stages)<=8:raise ValueError("Plan 1–8 explicit stages")
    plans=[plan(client,stage,options) for stage in stages]
    total=sum(stage["quote"]["estimated_micro_usd"] for stage in plans)
    budget=payload.get("budget_usd")
    if budget is not None and (not isinstance(budget,(int,float)) or not __import__('math').isfinite(budget) or budget<0 or total>budget*1_000_000):raise ValueError("Workflow exceeds the estimate budget; nothing submitted")
    return {"stages":plans,"estimated_total_micro_usd":total,"submitted":False,"note":"Refresh each quote before execution; key budgets enforce settlement limits. Future assets are not fabricated."}

def wait_with_options(resource,task_id,timeout,options):
    deadline=time.monotonic()+timeout;last=None
    while time.monotonic()<deadline:
        remaining=deadline-time.monotonic()
        try:
            last=resource.get(task_id,**{**options,"timeout":min(options.get("timeout",60),remaining),"retries":0})
            if last.get("status") in {"succeeded","failed","cancelled","timeout","expired"}:
                if last["status"]!="succeeded":raise TaskFailedError(last)
                return last
        except Link42Error as error:
            if isinstance(error,TaskFailedError) or (error.status not in {429,500,502,503,504}):raise
        time.sleep(min(3,max(0,deadline-time.monotonic())))
    raise PollTimeoutError(task_id,last)

def run(client,operation,payload,*,resource_id=None,file=None,stream=False,execute=False,idempotency_key=None,max_estimate_usd=None,wait_timeout=600,request_options=None):
    if not __import__('math').isfinite(wait_timeout) or wait_timeout<=0: raise ValueError("Invalid wait timeout")
    if operation in MUTATIONS and not execute: raise ValueError("Mutation refused: confirm the user's scope/cost, then pass --execute")
    if stream and operation not in {"chat","responses","messages","gemini"}:raise ValueError("Streaming is unsupported for this operation")
    options={**(request_options or {}),"retries":0}
    if idempotency_key: options["idempotency_key"]=idempotency_key
    if max_estimate_usd is not None and operation in {"responses","messages","gemini","embeddings","image-edit"}:
        raise ValueError("This operation has no supported estimate; use a quote-supported operation or an authoritative key budget")
    if operation in {"model-get","image-get","image-wait","video-get","video-wait","video-cancel","asset-get","asset-delete","asset-complete"} and not resource_id:
        raise ValueError("--id is required")
    if operation in {"chat","image","image-create","video-create"}:
        endpoint={"chat":"chat/completions","image":"images/generations","image-create":"images/generations","video-create":"videos"}[operation]
        quote=estimate(client,endpoint,payload,options)
        if max_estimate_usd==0 and not quote.get("is_free",False): raise ValueError("A zero budget requires an explicitly free model")
        if max_estimate_usd is not None and quote["estimated_micro_usd"]>max_estimate_usd*1_000_000: raise ValueError("Estimated cost exceeds the user's limit; no generation submitted")
    if operation=="discover":return discover(client,options)
    if operation=="doctor":return {"authorized_models":discover(client,options),"base_url":client.base_url,"authorization_checked":True,"upstream_execution_checked":False,"payment_submitted":False}
    if operation=="plan":return plan(client,payload,options)
    if operation=="workflow-plan":return workflow_plan(client,payload,options)
    if operation=="model-get":return client.models.get(resource_id,**options)
    if operation=="estimate":return estimate(client,payload["endpoint"],payload["payload"],options)
    if operation=="chat":return client.chat.completions.create(**{**payload,"stream":stream},request_options=options)
    if operation=="responses":return client.responses.create(**{**payload,"stream":stream},request_options=options)
    if operation=="messages":return client.messages.create(**{**payload,"stream":stream},request_options=options)
    if operation=="count-tokens":return client.messages.count_tokens(**payload,request_options=options)
    if operation=="gemini":
        model=payload["model"];body={k:v for k,v in payload.items() if k!="model"}
        return (client.gemini.stream_generate_content if stream else client.gemini.generate_content)(model,request_options=options,**body)
    if operation=="embeddings":return client.embeddings.create(**payload,request_options=options)
    if operation=="image":return client.images.generate(**payload,request_options=options)
    if operation=="image-edit":return client.images.edit(**payload,request_options=options)
    if operation=="image-create":return client.image_tasks.create(**payload,request_options=options)
    if operation=="image-get":return client.image_tasks.get(resource_id,**options)
    if operation=="image-wait":return wait_with_options(client.image_tasks,resource_id,wait_timeout,options) if request_options else client.image_tasks.wait(resource_id,timeout=wait_timeout)
    if operation=="video-create":return client.videos.create(**payload,request_options=options)
    if operation=="video-get":return client.videos.get(resource_id,**options)
    if operation=="video-list":return client.videos.list(**payload,request_options=options)
    if operation=="video-wait":return wait_with_options(client.videos,resource_id,wait_timeout,options) if request_options else client.videos.wait(resource_id,timeout=wait_timeout)
    if operation=="video-cancel":return client.videos.cancel(resource_id,**options)
    if operation=="asset-begin":return client.assets.begin(**payload,request_options=options)
    if operation=="asset-upload":return client.assets.upload_file(file,**payload,request_options=options)
    if operation=="asset-list":return client.assets.list(**payload,request_options=options)
    if operation=="asset-get":return client.assets.get(resource_id,**options)
    if operation=="asset-delete":return client.assets.delete(resource_id,**options)
    if operation=="asset-complete":return client.assets.complete(resource_id,**options)
    if operation=="usage-report":return client.usage.report(**payload,request_options=options)
    if operation=="usage-logs":return client.usage.logs(**payload,request_options=options)
    if operation=="usage-csv":return client.usage.report_csv(**payload,request_options=options)
    if operation=="score":return client.scores.create(**payload,request_options=options)
    raise ValueError("Unsupported operation")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation",choices=OPERATIONS)
    parser.add_argument("--json",help="JSON request file; - reads stdin")
    parser.add_argument("--id",dest="resource_id")
    parser.add_argument("--file")
    parser.add_argument("--base-url",default=os.environ.get("LINK42_BASE_URL","https://www.link42.ai"))
    parser.add_argument("--key-file",help="Explicit user-provided private key file; never bundled")
    parser.add_argument("--stream",action="store_true")
    parser.add_argument("--execute",action="store_true")
    parser.add_argument("--idempotency-key")
    parser.add_argument("--max-estimate-usd",type=float)
    parser.add_argument("--wait-timeout",type=float,default=600)
    parser.add_argument("--request-options",help="Private JSON file with SDK timeout/headers/request_id; no authorization overrides")
    args=parser.parse_args()
    try:
        key=Path(args.key_file).read_text().strip() if args.key_file else os.environ.get("LINK42_API_KEY","")
        if key.startswith("ark-"):raise ValueError("Use a LINK42 customer key, not an upstream Ark key")
        client=Link42(api_key=key,base_url=args.base_url)
        payload=json.loads(sys.stdin.read() if args.json=="-" else Path(args.json).read_text()) if args.json else {}
        if not isinstance(payload,dict):raise ValueError("Input must be a JSON object")
        request_options=json.loads(Path(args.request_options).read_text()) if args.request_options else {}
        if not isinstance(request_options,dict) or set(request_options)-{"headers","timeout","request_id"}:raise ValueError("Unsupported transport options")
        if args.max_estimate_usd is not None and (args.max_estimate_usd<0 or not __import__('math').isfinite(args.max_estimate_usd)):raise ValueError("Invalid budget")
        if args.operation in {"image-create","video-create"} and not args.idempotency_key:
            args.idempotency_key="link42-agent-"+uuid.uuid4().hex
            print(json.dumps({"event":"idempotency_key","idempotency_key":args.idempotency_key}),file=sys.stderr)
        result=run(client,args.operation,payload,resource_id=args.resource_id,file=args.file,stream=args.stream,execute=args.execute,idempotency_key=args.idempotency_key,max_estimate_usd=args.max_estimate_usd,wait_timeout=args.wait_timeout,request_options=request_options)
        if args.stream:
            for event in result: print(json.dumps(event,ensure_ascii=False),flush=True)
        elif isinstance(result,str):print(result)
        else:print(json.dumps(result,ensure_ascii=False))
    except Exception as error:
        value={"error":redact(error),"status":getattr(error,"status",0),"code":getattr(error,"code","invalid_operation"),"request_id":getattr(error,"request_id",None),"task_id":getattr(error,"task_id",None),"idempotency_key":getattr(error,"idempotency_key",None)}
        print(json.dumps(value,ensure_ascii=False),file=sys.stderr);return 1
    return 0

if __name__=="__main__":sys.exit(main())
