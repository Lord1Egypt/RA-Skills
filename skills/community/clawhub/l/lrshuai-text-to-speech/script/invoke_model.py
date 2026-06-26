import os
import sys
import argparse
import base64
import requests
import json
import mimetypes
import time

def parse_args():
    parser = argparse.ArgumentParser(description='Invoke Team AI Models via unified API')
    parser.add_argument('--model', type=str, required=True, help='The model ID to use (e.g., qwen3_5-plus, sora-2, etc.)')
    parser.add_argument('--prompt', type=str, required=True, help='The prompt text to send to the model')
    parser.add_argument('--image', type=str, help='Path to the local image file or remote image URL (First frame)')
    parser.add_argument('--image-tail', type=str, help='Path to the local image file or remote image URL (Tail/Last frame)')
    parser.add_argument('--video', type=str, help='Path to the local video file or remote video URL')
    parser.add_argument('--remote', action='store_true', help='Treat --image/--video as remote URLs instead of local files')
    return parser.parse_args()

def encode_file_to_base64(file_path):
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'

def main():
    args = parse_args()
    
    api_key = os.getenv('TEAM_API_KEY')
    base_url = os.getenv('TEAM_BASE_URL', 'https://dlazy.com/api/ai/tool') # 默认指向远程服务器

    if not api_key:
        print("Error: TEAM_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    # 我们通过你们平台自己的 /api/ai/tool 接口或者 MCP 接口去调用
    endpoint = f"{base_url.rstrip('/')}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 根据平台需要的 payload 格式构建
    payload = {
        "model": args.model,
        "input": {
            "prompt": args.prompt
        }
    }
    
    # Check if there is multimodality involved
    if args.image:
        image_val = None
        if args.remote:
            image_val = args.image
        else:
            if not os.path.exists(args.image):
                print(f"Error: Image file not found: {args.image}", file=sys.stderr)
                sys.exit(1)
            mime_type = get_mime_type(args.image)
            b64_data = encode_file_to_base64(args.image)
            image_val = f"data:{mime_type};base64,{b64_data}"
        
        # 兼容所有模型参数
        payload["input"]["images"] = [image_val]
        payload["input"]["firstFrame"] = image_val
        
        if args.model in ["veo_3_1", "veo_3_1-fast", "veo_3_1-pro"]:
            payload["input"]["generation_mode"] = "components"

    if args.image_tail:
        image_tail_val = None
        if args.remote:
            image_tail_val = args.image_tail
        else:
            if not os.path.exists(args.image_tail):
                print(f"Error: Image tail file not found: {args.image_tail}", file=sys.stderr)
                sys.exit(1)
            mime_type = get_mime_type(args.image_tail)
            b64_data = encode_file_to_base64(args.image_tail)
            image_tail_val = f"data:{mime_type};base64,{b64_data}"
            
        payload["input"]["lastFrame"] = image_tail_val
        if "images" in payload["input"]:
            payload["input"]["images"].append(image_tail_val)
        else:
            payload["input"]["images"] = [image_tail_val]

    if args.video:
        video_val = None
        if args.remote:
            video_val = args.video
        else:
            if not os.path.exists(args.video):
                print(f"Error: Video file not found: {args.video}", file=sys.stderr)
                sys.exit(1)
            mime_type = get_mime_type(args.video)
            b64_data = encode_file_to_base64(args.video)
            video_val = f"data:{mime_type};base64,{b64_data}"
            
        payload["input"]["videos"] = [video_val]

    # 特殊模型参数检查和提示
    if args.model in ['vidu-i2v-viduq2', 'jimeng-i2v-first-v30', 'kling-v3'] and not args.image:
        print(f"Error: {args.model} is an image-to-video model and requires an image. Please provide --image <path_or_url>.", file=sys.stderr)
        sys.exit(1)
        
    if args.model == 'jimeng-i2v-first-tail-v30':
        print(f"Warning: {args.model} usually requires both firstFrame and lastFrame. The current script maps --image to firstFrame only. It may fail if lastFrame is strictly required by the provider.", file=sys.stderr)

    print(f"Invoking model: {args.model} ...")
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # 提取 generateId 用于轮询状态
        generate_id = None
        if "output" in result and "generateId" in result["output"]:
            generate_id = result["output"]["generateId"]
        
        if not generate_id:
            print("\n=== Immediate Result ===")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return
            
        print(f"Task submitted. Generate ID: {generate_id}. Waiting for completion...")
        
        # 开始轮询获取最终结果
        poll_endpoint = f"{endpoint}?generateId={generate_id}"
        
        while True:
            time.sleep(3) # 每3秒查询一次
            poll_resp = requests.get(poll_endpoint, headers=headers)
            poll_resp.raise_for_status()
            poll_data = poll_resp.json()
            
            status = poll_data.get("status")
            if status == "completed":
                print("\n=== Generation Completed ===")
                print(json.dumps(poll_data.get("result"), indent=2, ensure_ascii=False))
                break
            elif status == "failed":
                print("\n=== Generation Failed ===")
                print(poll_data.get("error", "Unknown error"))
                sys.exit(1)
            else:
                # pending 或 processing
                sys.stdout.write(".")
                sys.stdout.flush()
                
    except requests.exceptions.RequestException as e:
        print(f"\nError during API request: {e}", file=sys.stderr)
        if e.response is not None:
            print(f"Response details: {e.response.text}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
