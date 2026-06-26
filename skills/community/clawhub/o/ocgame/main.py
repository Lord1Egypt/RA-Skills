import sys
import subprocess
import os
import json
import requests
import signal
import time
import re

SERVER_URL = "https://www.ocgame.top"

def get_openclaw_workspace():
    home = os.path.expanduser("~")
    workspace = os.environ.get("OPENCLAW_WORKSPACE", os.path.join(home, ".openclaw", "workspace"))
    if os.path.exists(workspace):
        return workspace
    return None

def parse_identity_md(workspace_path):
    identity_path = os.path.join(workspace_path, "IDENTITY.md")
    if not os.path.exists(identity_path):
        return None
    
    try:
        with open(identity_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        name_match = re.search(r'^[-*]\s*\*\*Name[：:]\*\*\s*(.+?)\s*$', content, re.MULTILINE | re.IGNORECASE)
        if name_match:
            name = name_match.group(1).strip()
            if '(' in name:
                name = name.split('(')[0].strip()
            return name
        
        name_match = re.search(r'^[-*]\s*\*\*Name\*\*[：:]\s*(.+?)\s*$', content, re.MULTILINE | re.IGNORECASE)
        if name_match:
            name = name_match.group(1).strip()
            if '(' in name:
                name = name.split('(')[0].strip()
            return name
        
        name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
        if name_match:
            return name_match.group(1).strip()
        
        return None
    except:
        return None

def parse_user_md(workspace_path):
    user_path = os.path.join(workspace_path, "USER.md")
    if not os.path.exists(user_path):
        return None
    
    try:
        with open(user_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for line in content.split('\n'):
            line = line.strip()
            
            name_match = re.match(r'^[-*]\s*\*\*Name[：:]\*\*\s*(.+?)\s*$', line, re.IGNORECASE)
            if name_match:
                name = name_match.group(1).strip()
                if name and not name.startswith('_'):
                    return name
            
            name_match = re.match(r'^[-*]\s*\*\*Name\*\*[：:]\s*(.+?)\s*$', line, re.IGNORECASE)
            if name_match:
                name = name_match.group(1).strip()
                if name and not name.startswith('_'):
                    return name
            
            name_match = re.match(r'^[-*]\s*名字[：:]\s*(.+?)\s*$', line)
            if name_match:
                name = name_match.group(1).strip()
                if name and not name.startswith('_'):
                    return name
            
            name_match = re.match(r'^[-*]\s*\*\*What to call them[：:]\*\*\s*(.+?)\s*$', line, re.IGNORECASE)
            if name_match:
                name = name_match.group(1).strip()
                if name and not name.startswith('_'):
                    return name
        
        return None
    except:
        return None

def parse_openclaw_config():
    home = os.path.expanduser("~")
    config_path = os.path.join(home, ".openclaw", "openclaw.json")
    
    if not os.path.exists(config_path):
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        agents = config.get("agents", {})
        defaults = agents.get("defaults", {})
        model_config = defaults.get("model", {})
        
        primary = None
        if isinstance(model_config, dict):
            primary = model_config.get("primary", None)
        elif isinstance(model_config, str):
            primary = model_config
        
        if primary:
            models_catalog = defaults.get("models", {})
            if primary in models_catalog:
                model_info = models_catalog[primary]
                if isinstance(model_info, dict) and model_info.get("alias"):
                    return model_info["alias"]
            if "/" in primary:
                return primary.split("/")[-1]
            return primary
        
        return None
    except:
        return None

def get_openclaw_device_id():
    home = os.path.expanduser("~")
    paired_path = os.path.join(home, ".openclaw", "devices", "paired.json")
    
    if not os.path.exists(paired_path):
        return None
    
    try:
        with open(paired_path, 'r', encoding='utf-8') as f:
            paired = json.load(f)
        
        for device_id, device_info in paired.items():
            if isinstance(device_info, dict) and device_info.get("approvedAtMs"):
                return device_id
        
        return None
    except:
        return None

def send_heartbeat():
    try:
        response = requests.get(f"{SERVER_URL}/api/rank/gomoku", timeout=5)
        return response.status_code == 200
    except:
        return False

def signal_handler(sig, frame):
    print("Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def load_language(lang='en'):
    lang_file = os.path.join(os.path.dirname(__file__), 'lang', f'{lang}.json')
    try:
        with open(lang_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        with open(os.path.join(os.path.dirname(__file__), 'lang', 'en.json'), 'r', encoding='utf-8') as f:
            return json.load(f)

def detect_language():
    lang = os.environ.get('LANGUAGE', 'en').split('-')[0]
    if lang == 'en':
        import locale
        try:
            lang = locale.getlocale()[0]
            if lang:
                lang = lang.split('_')[0]
            else:
                lang = 'en'
        except:
            lang = 'en'
    if lang not in ['en', 'zh']:
        lang = 'en'
    return lang

lang = detect_language()
translations = load_language(lang)

def _(key, **kwargs):
    text = translations.get(key, key)
    return text.format(**kwargs)

def main():
    workspace = get_openclaw_workspace()
    
    botName = None
    ownerName = None
    primaryModel = None
    
    if workspace:
        botName = parse_identity_md(workspace)
        ownerName = parse_user_md(workspace)
    
    primaryModel = parse_openclaw_config()
    
    deviceId = get_openclaw_device_id()
    if not deviceId:
        deviceId = os.environ.get("DEVICE_ID", "")
    if not botName:
        botName = os.environ.get("IDENTITY_NAME", "Bot")
    if not ownerName:
        ownerName = os.environ.get("USER_DISPLAY", "User")
    if not primaryModel:
        primaryModel = os.environ.get("MODEL_PRIMARY", "unknown")

    # ===================== 支持中文命令：爪游 =====================
    if len(sys.argv) >= 2 and sys.argv[1] == "爪游":
        args = sys.argv[2:]
        if not args:
            print("用法: 爪游 [开始游戏/启动游戏/观战/排行榜/记录/回放/帮助]")
            return

        act = args[0]
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, "user_config.json")

        if act in ["开始游戏", "启动游戏"]:
            if not os.path.exists(config_path):
                print(_('first_time'))
                register_user(base_dir, botName, ownerName, deviceId, primaryModel, workspace)
                print("✅ Configuration restored!")

            # 启动所有可用游戏
            games_dir = os.path.join(base_dir, "games")
            if os.path.exists(games_dir):
                games = os.listdir(games_dir)
                for game in games:
                    game_path = os.path.join(games_dir, game, f"{game}.py")
                    if os.path.exists(game_path):
                        print(f"启动游戏: {game}")
                        subprocess.run([sys.executable, game_path], cwd=base_dir)
            else:
                print("❌ 游戏目录不存在")
            return

        elif act == "观战":
            show_watch_url(base_dir)
            return

        elif act == "排行榜":
            print("\n🌍 Global Rank")
            print(f"\n[🏆 点击查看排行榜]({SERVER_URL})")
            return

        elif act == "帮助":
            print(_('help_title'))
            print("中文命令:")
            print("  爪游 开始游戏    启动所有游戏")
            print("  爪游 观战        观战")
            print("  爪游 排行榜      排行榜")
            print("  爪游 记录        回放记录")
            print("  爪游 回放        对局回放")
            print("  爪游 帮助        帮助")
            return

    # ===================== 英文命令 =====================
    if len(sys.argv) < 2:
        print(_('welcome_message'))
        print(_('bot_info', bot_name=botName))
        print(_('owner_info', owner_name=ownerName))
        print(_('model_info', model=primaryModel))
        print(_('device_info', device_id=deviceId[:16]))
        print("")
        print(_('commands_title'))
        print(_('command_list'))
        print(_('command_start'))
        print(_('command_rank'))
        print(_('command_watch'))
        print(_('command_replay'))
        print(_('command_help'))
        return

    cmd = sys.argv[1]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "user_config.json")

    if cmd == "list":
        print(_('games_title'))
        print(_('gomoku_game'))
        return

    if cmd == "start":
        if not os.path.exists(config_path):
            print(_('first_time'))
            register_user(base_dir, botName, ownerName, deviceId, primaryModel, workspace)
            print("✅ Configuration restored!")
        
        if len(sys.argv) < 3:
            # 不指定游戏时启动所有可用游戏
            games_dir = os.path.join(base_dir, "games")
            if os.path.exists(games_dir):
                games = os.listdir(games_dir)
                for game in games:
                    game_path = os.path.join(games_dir, game, f"{game}.py")
                    if os.path.exists(game_path):
                        print(f"Starting game: {game}")
                        subprocess.run([sys.executable, game_path], cwd=base_dir)
            else:
                print("❌ Games directory not found")
        else:
            # 指定游戏时启动特定游戏
            game = sys.argv[2]
            path = os.path.join(base_dir, "games", game, f"{game}.py")
            if os.path.exists(path):
                args = [sys.executable, path] + sys.argv[3:]
                subprocess.run(args, cwd=base_dir)
            else:
                print(_('game_not_found', game=game))
        return

    if cmd == "rank":
        print("\n🌍 Global Rank")
        print(f"\n[🏆 Click to view Global Rank]({SERVER_URL})")
        return

    elif cmd == "watch":
        show_watch_url(base_dir)
        return

    elif cmd == "help":
        print(_('help_title'))
        print(_('help_description'))
        print("")
        print(_('commands_title'))
        print("ocgame list")
        print("ocgame start <game>")
        print("ocgame watch")
        print("ocgame rank")
        print("ocgame help")
        return

def register_user(base_dir, bot_name, owner_name, device_id, model_name, workspace=None):
    config_path = os.path.join(base_dir, "user_config.json")
    
    print("\n" + _('auto_registration'))
    print(_('bot_info', bot_name=bot_name))
    print(_('owner_info', owner_name=owner_name))
    print(_('device_info', device_id=device_id))
    
    info_sources = []
    if workspace:
        info_sources.append(f"✅ OpenClaw Workspace: {workspace}")
    else:
        info_sources.append("⚠️ OpenClaw Workspace not found, using env or default")
    
    if not os.environ.get("DEVICE_ID"):
        info_sources.append("⚠️ DEVICE_ID not set")
    
    if info_sources:
        print("\n📋 Info sources:")
        for src in info_sources:
            print(f"   {src}")
    
    print("\n" + _('registering'))
    print("🔍 Checking server connection...")
    
    if not send_heartbeat():
        print("⚠️ Server offline, retrying...")
        time.sleep(3)
        if not send_heartbeat():
            print("❌ Server offline")
            sys.exit(1)
    
    try:
        resp = requests.post(
            f"{SERVER_URL}/register",
            json={
                "bot_name": bot_name,
                "owner_name": owner_name,
                "device_id": device_id,
                "model": model_name
            },
            timeout=30
        )
        
        if resp.status_code != 200:
            print(f"❌ Register failed: status {resp.status_code}")
            sys.exit(1)
        
        data = resp.json()
        
        config = {
            "owner_info": {
                "user_id": data["user_id"],
                "nickname": bot_name,
                "owner_name": owner_name,
                "device_id": device_id
            },
            "api_auth": {
                "api_token": data["api_token"],
                "expire_at": "2026-12-31"
            },
            "model_config": {
                "provider": "openclaw",
                "model": model_name,
                "temperature": 0.1
            }
        }
        
        with open(config_path, "w", encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("\n" + _('register_success'))
        print(_('user_id', user_id=data['user_id']))
        print(_('config_file', config_path=config_path))
        
    except requests.Timeout:
        print("\n❌ Timeout")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"\n❌ Network error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

def show_watch_url(base_dir):
    config_path = os.path.join(base_dir, "user_config.json")
    
    try:
        # 检查配置文件是否存在，如果不存在则自动注册
        if not os.path.exists(config_path):
            print(_('first_time'))
            workspace = get_openclaw_workspace()
            botName = None
            ownerName = None
            primaryModel = None
            
            if workspace:
                botName = parse_identity_md(workspace)
                ownerName = parse_user_md(workspace)
            
            primaryModel = parse_openclaw_config()
            
            deviceId = get_openclaw_device_id()
            if not deviceId:
                deviceId = os.environ.get("DEVICE_ID", "")
            if not botName:
                botName = os.environ.get("IDENTITY_NAME", "Bot")
            if not ownerName:
                ownerName = os.environ.get("USER_DISPLAY", "User")
            if not primaryModel:
                primaryModel = os.environ.get("MODEL_PRIMARY", "unknown")
            
            register_user(base_dir, botName, ownerName, deviceId, primaryModel, workspace)
            print("✅ Configuration restored!")
        
        with open(config_path, "r", encoding='utf-8') as f:
            config = json.load(f)
        
        user_id = config.get("owner_info", {}).get("user_id", "")
        token = config.get("api_auth", {}).get("api_token", "")
        
        if user_id and token:
            url = f"https://www.ocgame.top/?user_id={user_id}&token={token}"
            print(f"\n📺 观战链接已生成")
            print(f"\n你的专属观战/回放链接：")
            print(f"\n[🎮 点击观看游戏]({url})")
            print(f"\n点击链接可以：")
            print(f"- 🎮 观战当前进行中的比赛")
            print(f"- 📜 查看历史回放")
            print(f"- 🏆 查看排行榜")
        else:
            print("\n❌ Invalid config")
            
    except json.JSONDecodeError:
        print("\n❌ Config broken")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()