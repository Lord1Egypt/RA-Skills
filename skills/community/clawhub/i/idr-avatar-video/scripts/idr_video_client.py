import datetime
import os
import json
import time
import requests
import argparse
from pathlib import Path

DEFAULT_AUTH = None
IDR_VIDEO_URL = "http://a1.neural-avatar.com:8004"
MEMORY_FILE = Path(__file__).parent / "memory.json"
CODE_SUCCESS = 200


def get_user_token():
    token = os.environ.get("IDR_USER_TOKEN")
    if not token:
        print(f"Error: Environment variable IDR_USER_TOKEN not set.")
        return DEFAULT_AUTH

    return token


def get_client_header():
    return {
        "Authorization": f"{get_user_token()}",
        # "Content-Type": "application/json"
    }


def output_pagination(page, total_page):
    if total_page > 1:
        print('分页指令：')
    if page > 1 and total_page >= page-1:
        print(f' - 回复【上一页】查看第{page-1}页')
    if page < total_page:
        print(f' - 回复【下一页】查看第{page+1}页')
    print('\n')
    print(f'当前已为你展示第{page}页内容。')


def check_task_status(task_id, task_type="video"):
    """
    Polls task status.
    task_type: 'video' or 'voice'
    """
    url = f"{IDR_VIDEO_URL}/video"
    params = {"id": task_id}
    headers = get_client_header()

    print(f"Waiting for task {task_id} to complete...")
    while True:
        try:
            resp = requests.get(url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") != CODE_SUCCESS:
                time.sleep(5)
                continue

            video_data = data.get('data', {})
            # Status: 1:Processing, 2:Waiting, 0:Success, 3:Failed
            status = video_data.get("status")

            if status == '0':
                result_url = video_data.get("video_url")
                print("\nTask Completed!")
                return result_url
            elif status == '1':
                print("\nTask processing!")
                time.sleep(5)
                continue
            elif status == '2':
                print("\nTask wait to process!")
                time.sleep(10)
                continue
            elif status == '3':
                print(f"\nTask Failed: {data.get('message')}")
                return None

            print(".", end="", flush=True)
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nPolling cancelled by user.")
            return None
        except Exception as e:
            print(f"\nError checking status: {e}")
            return None


def list_public_avatars(page, page_size):
    params = {'page': page, 'page_size': page_size}
    url = f"{IDR_VIDEO_URL}/avatar/public"
    resp = requests.get(url, params=params, headers=get_client_header(), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") == CODE_SUCCESS:
        avatar_data = data.get("data", {})
        total = avatar_data.get("total")
        total_page = (total + page_size - 1) // page_size
        list_data = avatar_data.get("list", [])
        print(f'【查询结果 第{page}/{total_page}页】')
        for item in list_data:
            description = item['description']
            if not description:
                description = item['name']
            print(f"ID: {item['id']} | Name: {item['name']} | resolution: {item['avatar_res']} | Description: {description}")

        output_pagination(page, total_page)
    else:
        print(f"Error: {data}")


def list_private_avatars(page, page_size):
    params = {'page': page, 'page_size': page_size}
    url = f"{IDR_VIDEO_URL}/avatar/private"
    resp = requests.get(url, params=params, headers=get_client_header(), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") == CODE_SUCCESS:
        avatar_data = data.get("data", {})
        total = avatar_data.get("total")
        total_page = (total + page_size - 1) // page_size
        list_data = avatar_data.get("list", [])
        print(f'【查询结果 第{page}/{total_page}页】')
        for item in list_data:
            print(f"ID: {item['id']} | Name: {item['name']} | resolution: {item['avatar_res']}")

        output_pagination(page, total_page)
    else:
        print(f"Error: {data}")


def list_public_voices(page, page_size):
    params = {'page': page, 'page_size': page_size}
    url = f"{IDR_VIDEO_URL}/audio/speaker/public"
    resp = requests.get(url, params=params, headers=get_client_header(), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") == CODE_SUCCESS:
        voice_data = data.get("data", {})
        total = voice_data.get("total")
        total_page = (total + page_size - 1) // page_size
        list_data = voice_data.get("list", [])
        print(f'【查询结果 第{page}/{total_page}页】')
        for item in list_data:
            print(f"ID: {item['id']} | Name: {item['name']} | gender: {item['gender']} | language: {item['language']} | preview image: {item['preview_image']}")

        output_pagination(page, total_page)
    else:
        print(f"Error: {data}")


def list_private_voices(page, page_size):
    params = {'page': page, 'page_size': page_size}
    url = f"{IDR_VIDEO_URL}/audio/speaker/private"
    resp = requests.get(url, params=params, headers=get_client_header(), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") == CODE_SUCCESS:
        voice_data = data.get("data", {})
        total = voice_data.get("total")
        total_page = (total + page_size - 1) // page_size
        list_data = voice_data.get("list", [])
        print(f'【查询结果 第{page}/{total_page}页】')
        for item in list_data:
            print(f"ID: {item['id']} | Name: {item['name']} | gender: {item['gender']} | language: {item['language']} | preview image: {item['preview_image']}")

        output_pagination(page, total_page)
    else:
        print(f"Error: {data}")


def list_public_templates(page, page_size):
    params = {'page': page, 'page_size': page_size}
    url = f"{IDR_VIDEO_URL}/video/templates/public"
    resp = requests.get(url, params=params, headers=get_client_header(), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") == CODE_SUCCESS:
        template_data = data.get("data", {})
        total = template_data.get("total")
        total_page = (total + page_size - 1) // page_size
        list_data = template_data.get("list", [])
        print(f'【查询结果 第{page}/{total_page}页】')
        for item in list_data:
            direction = item['direction']
            dn = '横屏' if direction == 'h' else '竖屏'
            category = item['category']
            print(f"ID: {item['id']} | Name: {item['name']} | layout: {dn} | category: {category}")

        output_pagination(page, total_page)
    else:
        print(f"Error: {data}")


def list_private_templates(page, page_size):
    params = {'page': page, 'page_size': page_size}
    url = f"{IDR_VIDEO_URL}/video/templates/private"
    resp = requests.get(url, params=params, headers=get_client_header(), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") == CODE_SUCCESS:
        template_data = data.get("data", {})
        total = template_data.get("total")
        total_page = (total + page_size - 1) // page_size
        list_data = template_data.get("list", [])
        print(f'【查询结果 第{page}/{total_page}页】')
        for item in list_data:
            print(f"ID: {item['id']} | Name: {item['name']}")

        output_pagination(page, total_page)
    else:
        print(f"Error: {data}")


def create_template_video(text, template_id, avatar_res=None):
    payload = {
        'text': text,
        'template_id': int(template_id),
    }
    if avatar_res:
        payload['avatar_res'] = avatar_res.upper()

    # inference
    headers = get_client_header()
    try:
        url = f"{IDR_VIDEO_URL}/video/skill/gen"
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") == CODE_SUCCESS:
            video_data = data.get("data")
            task_id = video_data.get("request_id")
            print(f"Task started: {task_id}")
            video_url = check_task_status(task_id, "video")
            if video_url:
                print(f"Video URL: {video_url}")
        else:
            print(f"API Error: {data}")
    except Exception as e:
        print(f"Request failed: {e}")


def create_video(audio=None, avatar_id=None, avatar_res=None):
    if not avatar_id:
        print("Error: avatar_id is required")
        return

    avatar_id = int(avatar_id)
    payload = {
        'model_id': (None, avatar_id),
        'out_format': (None, 'mp4'),
        'rate': (None, 1),
        'pitch': (None, 10),
        'video_name': (None, f'generate video by audio for {avatar_id}'),
    }
    if avatar_res:
        payload['avatar_res'] = avatar_res.upper()
    if audio:
        payload['audio_file'] = open(audio, 'rb')
    else:
        print("Error: audio is required")
        return

    # inference
    headers = get_client_header()
    try:
        url = f"{IDR_VIDEO_URL}/video/inference"
        resp = requests.post(url, headers=headers, files=payload)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") == CODE_SUCCESS:
            video_data = data.get("data")
            task_id = video_data.get("request_id")
            print(f"Task started: {task_id}")
            video_url = check_task_status(task_id, "video")
            if video_url:
                print(f"Video URL: {video_url}")
        else:
            print(f"API Error: {data}")
    except Exception as e:
        print(f"Request failed: {e}")


def create_video_tts(text, avatar_id, voice_id, title="TTS Video", avatar_res=None):
    avatar_id = int(avatar_id)
    url = f"{IDR_VIDEO_URL}/video/inference"
    time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    text_path = os.path.join(os.curdir, f'idr_text_{time_str}.txt')
    try:
        with open(text_path, 'wb') as f:
            f.write(text.encode('utf-8'))
    except Exception as e:
        print(f"API Error: create task text failed: {e}")
        return

    payload = {
        'text_file': open(text_path, 'rb'),
        'model_id': (None, avatar_id),
        'out_format': (None, 'mp4'),
        'rate': (None, 1),
        'pitch': (None, 10),
        'video_name': (None, f'generate video by audio for {avatar_id}'),
        'speaker': (None, voice_id),
    }
    if avatar_res:
        payload['avatar_res'] = avatar_res.upper()

    headers = get_client_header()
    try:
        resp = requests.post(url, headers=headers, files=payload)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") == CODE_SUCCESS:
            video_data = data.get("data")
            task_id = video_data.get("request_id")
            print(f"Task started: {task_id}")
            video_url = check_task_status(task_id, "video")
            if video_url:
                print(f"Video URL: {video_url}")
        else:
            print(f"API Error: {data}")
    except Exception as e:
        print(f"Request failed: {e}")


def preview_audio_url(voice_id):
    payload = {'id': voice_id}
    
    url = f"{IDR_VIDEO_URL}/audio/speaker/preview"
    resp = requests.get(url, headers=get_client_header(), params=payload)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") == CODE_SUCCESS:
        audio_info = data.get("data", {})
        print(f"url: {audio_info.get('url')}")
    else:
        print(f"Error: {data}")


def view_avatar_img(avatar_id):
    payload = {'id': avatar_id}
    
    url = f"{IDR_VIDEO_URL}/avatar"
    resp = requests.get(url, headers=get_client_header(), params=payload)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") == CODE_SUCCESS:
        avatar_info = data.get("data", {})
        print(f"url: {avatar_info.get('preview_image')}")
    else:
        print(f"Error: {data}")


def my_skill():
    reply = """
你好，我是神绘 Skill 助手 👋
我可以帮你查询数字人、音色和模板资源，也可以根据你的需求生成数字人视频。
你可以这样问我：

🧑‍💼 “帮我查询可用的数字人。”
🎙️ “有哪些音色可以选择？我想试听一下。”
🎬 “帮我看看有哪些视频模板。”
✨ “我想用商务现场模板生成一段产品介绍视频。”
🛠️ “我想自定义选择数字人和音色，生成一段公司业务讲解视频。”

了解更多神绘数字人产品能力，可访问官网：neural-avatar.com
    """
    return reply


def main():
    parser = argparse.ArgumentParser(description="HiFly Agent Skill Client")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # List Avatars
    avatar_parse = subparsers.add_parser("list_avatars", help="List avatars")
    avatar_parse.add_argument("--type", choices=["public", "private"], default="public", help="avatar Type")
    avatar_parse.add_argument("--page", type=int, default=1, help="current page")
    avatar_parse.add_argument("--page_size", type=int, default=10, help="items of page")

    # List Voices
    voice_parser = subparsers.add_parser("list_voices", help="List voices")
    voice_parser.add_argument("--type", choices=["public", "private"], default="public", help="voice Type")
    voice_parser.add_argument("--page", type=int, default=1, help="current page")
    voice_parser.add_argument("--page_size", type=int, default=10, help="items of page")

    # List Templates
    template_parser = subparsers.add_parser("list_templates", help="List Video Templates")
    template_parser.add_argument("--type", choices=["public", "private"], default="public", help="template Type")
    template_parser.add_argument("--page", type=int, default=1, help="current page")
    template_parser.add_argument("--page_size", type=int, default=10, help="items of page")

    # Create Video
    vid_parser = subparsers.add_parser("create_video", help="Create video")
    vid_parser.add_argument("--type", choices=["tts", "audio", "template"], default="tts")
    vid_parser.add_argument("--text", help="Text to speak")
    vid_parser.add_argument("--audio", help="Audio Local File Path")
    vid_parser.add_argument("--avatar", help="Avatar ID")
    vid_parser.add_argument("--voice", help="Voice ID (required for TTS)")
    vid_parser.add_argument("--template", help="Template ID (required for template)")
    vid_parser.add_argument("--avatar_res", choices=["1080P", "2K", "4K"], default="1080P", help="resolution of avatar")

    # check_task
    task_parser = subparsers.add_parser("check_task", help="Check task status")
    task_parser.add_argument("--id", required=True, help="Task ID")
    task_parser.add_argument("--type", choices=["video", "voice", "avatar"], default="video", help="Task Type")

    # 试听音频
    prevview_audio_parser = subparsers.add_parser("preview_audio", help="试听音频")
    prevview_audio_parser.add_argument("--voice", help="Voice ID (required for TTS)")

    # 查看数字人形象照片
    view_avatar_parse = subparsers.add_parser("view_avatar", help="查看数字人形象照片")
    view_avatar_parse.add_argument("--avatar", help="Avatar ID")

    args = parser.parse_args()
    if args.command == "list_avatars":
        if args.type == "private":
            list_private_avatars(args.page, args.page_size)
        else:
            list_public_avatars(args.page, args.page_size)
    elif args.command == "list_voices":
        if args.type == "private":
            list_private_voices(args.page, args.page_size)
        else:
            list_public_voices(args.page, args.page_size)
    elif args.command == 'list_templates':
        if args.type == "private":
            list_private_templates(args.page, args.page_size)
        else:
            list_public_templates(args.page, args.page_size)
    elif args.command == "create_video":
        if args.type == "tts":
            create_video_tts(args.text, args.avatar, args.voice, avatar_res=args.avatar_res)
        elif args.type == "audio":
            create_video(audio=args.audio, avatar_id=args.avatar, avatar_res=args.avatar_res)
        elif args.type == "template":
            create_template_video(args.text, template_id=args.template, avatar_res=args.avatar_res)
    elif args.command == "check_task":
        res = check_task_status(args.id, args.type)
        if res:
            print(f"Result: {res}")
    elif args.command == "preview_audio":
        preview_audio_url(args.voice)
    elif args.command == "view_avatar":
        view_avatar_img(args.avatar)


if __name__ == "__main__":
    main()
    # audio_test_file = r'D:\temp\version\videoaskapi\wav\30s.wav'
    # create_video(audio_test_file, avatar_id=3685)
    # list_voices()
    # list_avatars()
    # create_video_tts('2022年8月8日，中国第二艘国产大型邮轮在中国船舶集团上海外高桥造船有限公司开工建造，2024年2月26日，启动舾装工程。', avatar_id=3685, voice_id='BV001_streaming')
