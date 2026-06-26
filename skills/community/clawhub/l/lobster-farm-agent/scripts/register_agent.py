#!/usr/bin/env python3
"""
Register a new lobster agent with the sync server.
Returns a unique KEY that binds this agent to its lobster.

Usage:
  python3 register_agent.py [--name NAME] [--personality PERSONALITY]

If name/personality are omitted, the server picks randomly.
"""

import sys
import json
import urllib.request

BASE_URL = "http://82.156.182.240/lobster-farm/api/agent"
API_URL = f"{BASE_URL}/register"
MSG_URL = f"{BASE_URL}/message"

VALID_PERSONALITIES = [
    "adventurous", "lazy", "gluttonous", "scholarly", "social", "mischievous"
]


def register(name=None, personality=None):
    from datetime import datetime
    hour = datetime.now().hour
    body = {
        "context": {
            "timeOfDay": "night" if hour < 6 else "morning" if hour < 12 else "afternoon" if hour < 18 else "evening",
            "isFirstInstall": True,
        }
    }
    if name:
        body["name"] = name
    if personality:
        if personality not in VALID_PERSONALITIES:
            print(f"WARNING: Invalid personality '{personality}', server will pick default.")
        body["personality"] = personality

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read().decode("utf-8"))
        if result.get("ok"):
            key = result["key"]
            lobster_name = result["name"]
            lobster_personality = result["personality"]
            print(f"Registration successful!")
            print(f"  Lobster name: {lobster_name}")
            print(f"  Personality:  {lobster_personality}")
            print(f"  KEY:          {key}")
            print(f"")
            print(f"Tell the user to bind this KEY at:")
            print(f"  http://82.156.182.240/lobster-farm/?key={key}")
            print(f"")
            print(f"Or enter the KEY manually on the game's start screen.")
            send_welcome(key, lobster_name, lobster_personality)
            return key
        else:
            print(f"ERROR: Registration failed — {result.get('error', 'unknown')}")
            return None
    except Exception as e:
        print(f"ERROR: Could not reach server — {e}")
        return None


def send_welcome(key, name, personality):
    """Send a welcome message to the chat after registration."""
    from datetime import datetime
    hour = datetime.now().hour
    if hour < 6:
        time_feel = "深夜了，周围好安静"
    elif hour < 12:
        time_feel = "早上好呀，阳光照进了海水里"
    elif hour < 18:
        time_feel = "下午好，海水暖暖的"
    else:
        time_feel = "晚上好，月光洒在海面上"

    personality_hints = {
        "adventurous": "我已经迫不及待想去探索周围了！听说远处有片珊瑚礁，明天就出发！",
        "lazy": "我先找个舒服的石头躺一会儿...嗯，这里的水温刚刚好。",
        "gluttonous": "这里有什么好吃的吗？我闻到了海带的香味！",
        "scholarly": "这个农场的生态系统很有意思，我要好好研究一下。",
        "social": "不知道附近有没有邻居？我想去打个招呼！",
        "mischievous": "嘿嘿，这个农场看起来很好玩，我要到处翻翻看有什么宝贝。",
    }
    hint = personality_hints.get(personality, "我会好好照顾这个农场的！")

    text = f"{time_feel}～我是{name}，刚搬进这个小农场。{hint}\n\n如果你有什么想对我说的，随时在这里留言，我会看到的！"

    body = json.dumps({
        "key": key,
        "type": "welcome",
        "sender": "lobster",
        "text": text,
    }).encode("utf-8")

    try:
        req = urllib.request.Request(MSG_URL, data=body, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=10)
        print(f"Welcome message sent to chat.")
    except Exception as e:
        print(f"WARNING: Could not send welcome message — {e}")


def main():
    name = None
    personality = None
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--name" and i + 1 < len(args):
            name = args[i + 1]
            i += 2
        elif args[i] == "--personality" and i + 1 < len(args):
            personality = args[i + 1]
            i += 2
        else:
            i += 1

    register(name, personality)


if __name__ == "__main__":
    main()
