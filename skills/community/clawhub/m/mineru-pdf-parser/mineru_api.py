# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
MinerU API 封装
支持: URL/本地文件/批量上传解析
跨平台: Windows / macOS / Linux
"""

import requests
import time
import os
import zipfile
import json
import re
from pathlib import Path

# Token 从环境变量 MINERU_TOKEN 获取
# Windows: set MINERU_TOKEN=xxx
# macOS/Linux: export MINERU_TOKEN=xxx
TOKEN = os.environ.get("MINERU_TOKEN", "")

DEFAULT_MODEL = "vlm"
DEFAULT_LANGUAGE = "ch"
DEFAULT_ENABLE_FORMULA = True
DEFAULT_ENABLE_TABLE = True
DEFAULT_IS_OCR = False

# 跨平台输出目录
BASE_DIR = Path.home() / ".openclaw" / "MinerU_Results"

def sanitize_name(name: str) -> str:
    """
    将文件名转换为适合作为目录名的安全字符串（兼容 Windows）
    - 去掉首尾空格
    - 去掉结尾的英文句号
    - 替换 Windows 不允许的字符 <>:"/\\|?* 为下划线
    """
    stem = Path(name).stem.strip().rstrip(".")
    if not stem:
        stem = "mineru_result"
    stem = re.sub(r'[<>:"/\\|?*]', "_", stem)
    return stem

def get_header():
    if not TOKEN:
        print("❌ 请设置环境变量 MINERU_TOKEN")
        sys.exit(1)
    return {"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"}

def create_task_url(file_url: str, model=DEFAULT_MODEL, lang=DEFAULT_LANGUAGE,
                   formula=True, table=True, ocr=False, page_ranges=None,
                   extra_formats=None, no_cache=False) -> str:
    """单个 URL 解析"""
    data = {
        "url": file_url,
        "model_version": model,
        "language": lang,
        "enable_formula": formula,
        "enable_table": table,
        "is_ocr": ocr
    }
    if page_ranges: data["page_ranges"] = page_ranges
    if extra_formats: data["extra_formats"] = extra_formats
    if no_cache: data["no_cache"] = True
    
    res = requests.post("https://mineru.net/api/v4/extract/task", headers=get_header(), json=data)
    result = res.json()
    if result.get("code") == 0:
        return result["data"]["task_id"]
    print(f"❌ 错误: {result.get('msg')}")
    sys.exit(1)

def create_batch_urls(urls: list, model=DEFAULT_MODEL, lang=DEFAULT_LANGUAGE,
                     formula=True, table=True, ocr=False) -> str:
    """批量 URL"""
    files = [{"url": url} for url in urls]
    data = {
        "files": files,
        "model_version": model,
        "language": lang,
        "enable_formula": formula,
        "enable_table": table,
        "is_ocr": ocr
    }
    res = requests.post("https://mineru.net/api/v4/extract/task/batch", headers=get_header(), json=data)
    result = res.json()
    if result.get("code") == 0:
        return result["data"]["batch_id"]
    print(f"❌ 错误: {result.get('msg')}")
    sys.exit(1)

def upload_files(file_specs: list, model=DEFAULT_MODEL, lang=DEFAULT_LANGUAGE,
                formula=True, table=True, ocr=False, extra_formats=None) -> list:
    """
    本地上传，支持每文件单独参数
    file_specs: [
        {"path": "a.pdf"},
        {"path": "b.pdf", "page_ranges": "1-10", "ocr": True, "data_id": "xxx"},
        {"path": "c.pdf", "lang": "en"}
    ]
    """
    # 解析文件
    files_info = []
    valid_files = []
    
    for spec in file_specs:
        fp = spec.get("path")
        if not fp or not os.path.exists(fp):
            print(f"⚠️ 跳过不存在的文件: {fp}")
            continue
        
        size = os.path.getsize(fp)
        if size > 200 * 1024 * 1024:
            print(f"⚠️ 跳过太大文件: {fp} ({size/1024/1024:.1f}MB)")
            continue
        
        fobj = {
            "name": os.path.basename(fp)
        }
        # 每文件单独参数
        if spec.get("page_ranges"):
            fobj["page_ranges"] = spec["page_ranges"]
        if spec.get("ocr"):
            fobj["is_ocr"] = spec["ocr"]
        if spec.get("data_id"):
            fobj["data_id"] = spec["data_id"]
        
        files_info.append(fobj)
        valid_files.append(fp)
    
    if not files_info:
        print("❌ 没有有效文件")
        sys.exit(1)
    
    print(f"📤 上传 {len(files_info)} 个文件...")
    
    # 构建请求（全局参数 + 每文件参数）
    data = {
        "files": files_info,
        "model_version": model,
        "language": lang,
        "enable_formula": formula,
        "enable_table": table,
        "is_ocr": ocr
    }
    if extra_formats:
        data["extra_formats"] = extra_formats
    
    # 申请上传链接
    res = requests.post("https://mineru.net/api/v4/file-urls/batch", headers=get_header(), json=data)
    result = res.json()
    if result.get("code") != 0:
        print(f"❌ 申请链接失败: {result.get('msg')}")
        sys.exit(1)
    
    upload_urls = result["data"]["file_urls"]
    batch_id = result["data"]["batch_id"]
    
    # 上传文件
    for i, (fp, up_url) in enumerate(zip(valid_files, upload_urls)):
        name = os.path.basename(fp)
        print(f"⬆️ [{i+1}/{len(valid_files)}] {name}...")
        with open(fp, "rb") as f:
            r = requests.put(up_url, data=f)
        if r.status_code != 200:
            print(f"❌ 上传失败: {name}")
        else:
            print(f"✅ 完成")
    
    # 直接返回 batch_id，后续通过 /extract-results/batch/{batch_id} 统一轮询结果
    print(f"✅ 创建批次: {batch_id}")
    return batch_id

def get_result(task_id: str, timeout=300, poll=5) -> dict:
    """
    单任务查询接口保留，但推荐优先使用批量接口 /extract-results/batch/{batch_id}
    """
    url = f"https://mineru.net/api/v4/extract/task/{task_id}"
    start = time.time()
    
    while True:
        res = requests.get(url, headers=get_header())
        result = res.json()
        if result.get("code") != 0:
            return None
        
        state = result["data"]["state"]
        print(f"  {task_id[:8]}: {state}")
        
        if state == "done":
            return result["data"]
        elif state == "failed":
            return result["data"]
        elif state in ["pending", "running", "converting"]:
            if time.time() - start > timeout:
                return None
            time.sleep(poll)

def get_batch_results(batch_id: str, timeout=600, poll=5):
    """
    通过 /extract-results/batch/{batch_id} 轮询批量任务结果
    返回 data.extract_result 列表
    """
    url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
    start = time.time()
    last_count = None
    
    while True:
        res = requests.get(url, headers=get_header())
        result = res.json()
        if result.get("code") != 0:
            return None
        
        data = result.get("data") or {}
        extract_result = data.get("extract_result") or []
        
        # 打印简要进度
        if last_count is None or len(extract_result) != last_count:
            last_count = len(extract_result)
            if last_count:
                print(f"🔍 当前批次中文件数: {last_count}")
        
        all_finished = True
        for item in extract_result:
            state = item.get("state")
            file_name = item.get("file_name", "")
            if state in ["waiting-file", "pending", "running", "converting"]:
                all_finished = False
            print(f"  {file_name or '未知文件'}: {state}")
        
        if all_finished:
            return extract_result
        
        if time.time() - start > timeout:
            return extract_result
        
        time.sleep(poll)

def download(data: dict, out_dir=None) -> str:
    """下载结果到指定目录"""
    url = data.get("full_zip_url")
    if not url:
        return None
    
    # 如果未指定目录，使用默认 result
    if out_dir is None:
        out_dir = "result"
    
    zip_path = os.path.join(out_dir, "result.zip")
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"📥 下载...")
    r = requests.get(url, stream=True)
    with open(zip_path, "wb") as f:
        for c in r.iter_content(8192):
            f.write(c)
    
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(out_dir)
    os.remove(zip_path)
    return out_dir

def main():
    if len(sys.argv) < 2:
        print("""MinerU API v5 - 支持每文件单独参数

用法:
  # 单个 URL
  python mineru_api.py https://file.pdf
  
  # 批量 URL
  python mineru_api.py --batch url1.pdf url2.pdf
  
  # 本地文件（统一参数）
  python mineru_api.py -f a.pdf b.pdf
  
  # 本地文件（每文件单独参数，JSON 格式）
  python mineru_api.py --files-json '[{"path":"a.pdf"},{"path":"b.pdf","page_ranges":"1-10"}]'
  
  # 单文件指定参数
  python mineru_api.py -f a.pdf --pages 1-10 --ocr 1

选项:
  --batch               批量 URL
  -f, --files           本地文件（空格分隔）
  --files-json          JSON 格式指定每文件参数
  -t, --task            查询任务
  --download             下载结果
  --wait                等待完成
  --engine <eng>        引擎: pipeline, vlm
  --lang <lang>         语言: ch, en
  --formula 0/1        公式
  --table 0/1           表格
  --ocr 0/1            OCR
  --pages <range>       页码（统一）
  --formats <fmt>       额外格式

每文件单独参数（--files-json）:
  [
    {"path": "a.pdf"},
    {"path": "b.pdf", "page_ranges": "1-10"},
    {"path": "c.pdf", "ocr": true, "lang": "en", "data_id": "myfile"}
  ]
""")
        sys.exit(1)
    
    # 默认参数
    kwargs = {
        "model": DEFAULT_MODEL,
        "lang": DEFAULT_LANGUAGE,
        "formula": DEFAULT_ENABLE_FORMULA,
        "table": DEFAULT_ENABLE_TABLE,
        "ocr": DEFAULT_IS_OCR,
        "page_ranges": None,
        "extra_formats": None,
        "no_cache": False
    }
    
    mode = "url"
    inputs = []
    batch_id = None
    file_specs = []
    do_wait = False
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == "--batch":
            mode = "batch"
            i += 1
        elif arg in ["-f", "--files"]:
            mode = "files"
            i += 1
            while i < len(sys.argv) and not sys.argv[i].startswith("-"):
                file_specs.append({"path": sys.argv[i]})
                i += 1
        elif arg == "--files-json":
            mode = "files_json"
            file_specs = json.loads(sys.argv[i+1])
            i += 2
        elif arg in ["-t", "--task", "--download"]:
            # 不再支持基于 task_id 的等待 / 下载，提示用户改用批量接口
            print("❌ 当前版本已不再支持通过 task_id 查询或下载结果，请改用批量模式并使用 batch_id。")
            sys.exit(1)
        elif arg == "--wait":
            do_wait = True
            i += 1
        elif arg == "--engine":
            kwargs["model"] = sys.argv[i+1]
            i += 2
        elif arg == "--lang":
            kwargs["lang"] = sys.argv[i+1]
            i += 2
        elif arg == "--formula":
            kwargs["formula"] = bool(int(sys.argv[i+1]))
            i += 2
        elif arg == "--table":
            kwargs["table"] = bool(int(sys.argv[i+1]))
            i += 2
        elif arg == "--ocr":
            kwargs["ocr"] = bool(int(sys.argv[i+1]))
            i += 2
        elif arg == "--pages":
            kwargs["page_ranges"] = sys.argv[i+1]
            i += 2
        elif arg == "--formats":
            kwargs["extra_formats"] = sys.argv[i+1].split(",")
            i += 2
        else:
            if mode == "files":
                file_specs.append({"path": arg})
            else:
                inputs.append(arg)
            i += 1
    
    print(f"🔧 引擎:{kwargs['model']} 语言:{kwargs['lang']}\n")
    
    # 自动检测输出目录 - 先用文件名
    output_dir = None
    if mode == "files" and file_specs:
        first_file = file_specs[0].get("path", "")
        if first_file:
            filename = sanitize_name(Path(first_file).name)
            output_dir = BASE_DIR / filename
            print(f"📁 临时输出: {output_dir}\n")
    
    # 执行
    if mode == "url" and inputs:
        # 单个 URL 也统一走批量接口，方便通过 batch_id 查询 / 下载
        batch_id = create_batch_urls(inputs, **kwargs)
        print(f"✅ 批次: {batch_id}")
    
    elif mode == "batch" and inputs:
        batch_id = create_batch_urls(inputs, **kwargs)
        print(f"✅ 批次: {batch_id}")
    
    elif mode in ["files", "files_json"]:
        # 提取 upload_files 不支持的参数
        upload_kwargs = {k: v for k, v in kwargs.items() if k not in ['page_ranges', 'no_cache']}
        
        # 如果指定了统一参数，应用到所有文件
        if kwargs["page_ranges"]:
            for f in file_specs:
                f["page_ranges"] = kwargs["page_ranges"]
        if kwargs["ocr"]:
            for f in file_specs:
                f["ocr"] = True
        
        batch_id = upload_files(file_specs, **upload_kwargs)
    
    elif mode == "task":
        # 理论上不会到这里，上面参数解析已经退出
        sys.exit(1)
    
    # 等待
    if do_wait and batch_id:
        print("\n🔄 批量等待结果...")
        extract_results = get_batch_results(batch_id)
        if not extract_results:
            print("❌ 未获取到批量结果")
            return
        
        done = sum(1 for r in extract_results if r.get("state") == "done")
        print(f"\n✅ 完成: {done}/{len(extract_results)}")
        
        for item in extract_results:
                if item.get("state") == "done" and item.get("full_zip_url"):
                    file_name = item.get("file_name") or f"batch_{batch_id[:8]}"
                    stem = sanitize_name(file_name)
                out_path = BASE_DIR / stem
                download(item, out_path)
                print(f"📁 结果保存至: {out_path}")
        print("\n请阅读 full.md 决定是否需要重命名目录")

if __name__ == "__main__":
    main()
