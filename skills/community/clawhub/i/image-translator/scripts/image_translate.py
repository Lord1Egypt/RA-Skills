#!/usr/bin/env python3
"""
象寄图片翻译脚本

使用方法:
    # 本地文件翻译
    python image_translate.py --img-key IMG_KEY --user-key USER_KEY --file /path/to/image.png --source-language JPN --target-language ENG
    
    # URL 翻译（批量）
    python image_translate.py --img-key IMG_KEY --user-key USER_KEY --urls "https://example.com/image.jpg" --source-language CHS --target-language ENG
"""
import argparse
import hashlib
import json
import sys
import time
import os
import subprocess

# URL 翻译使用 api.tosoiot.com，文件上传使用 api2.tosoiot.com
API_URL = "https://api.tosoiot.com"
API_URL_FILE = "https://api2.tosoiot.com"


def calculate_sign(commit_time: str, user_key: str, img_key: str) -> str:
    sign_str = f"{commit_time}_{user_key}_{img_key}"
    return hashlib.md5(sign_str.encode("utf-8")).hexdigest().lower()


def translate_image_file(img_key, user_key, file_path, source_language, target_language, qos=None, need_watermark=None, need_rm_url=None, engine_type=None):
    """
    翻译本地图片文件（使用 api2.tosoiot.com）
    使用 curl 发送 multipart/form-data 请求
    """
    if not os.path.exists(file_path):
        return {"Code": -1, "Message": f"文件不存在: {file_path}"}
    
    commit_time = str(int(time.time()))
    sign = calculate_sign(commit_time, user_key, img_key)
    
    # 构建 curl 命令
    cmd = [
        "curl", "-s", "-X", "POST", API_URL_FILE,
        "-F", f"Action=GetImageTranslate",
        "-F", f"Url=local",
        "-F", f"SourceLanguage={source_language}",
        "-F", f"TargetLanguage={target_language}",
        "-F", f"ImgTransKey={img_key}",
        "-F", f"CommitTime={commit_time}",
        "-F", f"Sign={sign}",
        "-F", f"file-stream=@{file_path}"
    ]
    
    if qos:
        cmd.extend(["-F", f"Qos={qos}"])
    if need_watermark is not None:
        cmd.extend(["-F", f"NeedWatermark={need_watermark}"])
    if need_rm_url is not None:
        cmd.extend(["-F", f"NeedRmUrl={need_rm_url}"])
    if engine_type is not None:
        cmd.extend(["-F", f"EngineType={engine_type}"])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"Code": -1, "Message": f"curl error: {result.stderr}"}
    except subprocess.TimeoutExpired:
        return {"Code": -1, "Message": "Request timeout"}
    except json.JSONDecodeError as e:
        return {"Code": -1, "Message": f"JSON decode error: {e}", "raw": result.stdout}
    except Exception as e:
        return {"Code": -1, "Message": f"Error: {str(e)}"}


def translate_image_url(img_key, user_key, urls, source_language, target_language, sync=1, qos=None, need_watermark=None, need_rm_url=None):
    """
    翻译图片 URL（批量，使用 api.tosoiot.com）
    """
    import urllib.parse
    import urllib.request
    import urllib.error
    
    commit_time = str(int(time.time()))
    sign = calculate_sign(commit_time, user_key, img_key)
    
    encoded_urls = ",".join(urllib.parse.quote(url, safe="") for url in urls)
    
    form_data = {
        "Action": "GetImageTranslateBatch",
        "SourceLanguage": source_language,
        "TargetLanguage": target_language,
        "Urls": encoded_urls,
        "ImgTransKey": img_key,
        "CommitTime": commit_time,
        "Sign": sign,
        "Sync": sync
    }
    
    if qos:
        form_data["Qos"] = qos
    if need_watermark is not None:
        form_data["NeedWatermark"] = need_watermark
    if need_rm_url is not None:
        form_data["NeedRmUrl"] = need_rm_url
    
    encoded_data = urllib.parse.urlencode(form_data).encode("utf-8")
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    req = urllib.request.Request(API_URL + "/", data=encoded_data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"Code": e.code, "Message": f"HTTP Error: {e.code} {e.reason}"}
    except urllib.error.URLError as e:
        return {"Code": -1, "Message": f"URL Error: {e.reason}"}


def main():
    parser = argparse.ArgumentParser(description="象寄图片翻译")
    parser.add_argument("--img-key", required=True, help="ImgTransKey")
    parser.add_argument("--user-key", required=True, help="UserKey")
    parser.add_argument("--file", help="本地图片文件路径")
    parser.add_argument("--urls", nargs="+", help="图片URL列表")
    parser.add_argument("--source-language", required=True, help="源语言")
    parser.add_argument("--target-language", required=True, help="目标语言")
    parser.add_argument("--qos", choices=["LowLatency", "BestQuality"])
    parser.add_argument("--need-watermark", type=int, choices=[0, 1])
    parser.add_argument("--need-rm-url", type=int, choices=[0, 1])
    parser.add_argument("--engine-type", type=int)
    parser.add_argument("--sync", type=int, choices=[1, 2], default=1, help="URL翻译时：1=同步(默认), 2=异步")
    
    args = parser.parse_args()
    
    if args.file:
        print(f"正在翻译本地文件: {args.file}...", file=sys.stderr)
        result = translate_image_file(
            img_key=args.img_key, user_key=args.user_key, file_path=args.file,
            source_language=args.source_language, target_language=args.target_language,
            qos=args.qos, need_watermark=args.need_watermark,
            need_rm_url=args.need_rm_url, engine_type=args.engine_type
        )
    elif args.urls:
        result = translate_image_url(
            img_key=args.img_key, user_key=args.user_key, urls=args.urls,
            source_language=args.source_language, target_language=args.target_language,
            sync=args.sync, qos=args.qos, need_watermark=args.need_watermark, need_rm_url=args.need_rm_url
        )
    else:
        print(json.dumps({"Code": -1, "Message": "请提供 --file 或 --urls 参数"}))
        sys.exit(1)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result.get("Code") == 200:
        if args.file:
            url = result.get("Data", {}).get("Url", "") or result.get("Data", {}).get("SslUrl", "")
            if url:
                print(f"\n翻译后图片URL: {url}", file=sys.stderr)
        elif args.urls:
            contents = result.get("Data", {}).get("Content", [])
            if contents:
                print("\n翻译结果:", file=sys.stderr)
                for i, item in enumerate(contents, 1):
                    print(f"  {i}. 原图: {item.get('OriginUrl', '')}", file=sys.stderr)
                    print(f"     译文: {item.get('Url', '') or item.get('SslUrl', '')}", file=sys.stderr)
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
