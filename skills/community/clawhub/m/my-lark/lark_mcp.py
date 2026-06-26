#!/usr/bin/env python3
"""
lark-mcp + Feishu Open API 调用包装器
路径: /workspace/tools/lark_mcp.py
支持: lark-mcp (App Token) + Feishu REST API (User Token)
"""
import subprocess, json, sys, os, pathlib, urllib.request, urllib.parse

# ============ 凭证配置 ============
APP_ID = "cli_a9c97317ef78dbc6"
APP_SECRET = "bHTIdpglmPdAOu8gyFltadE4whZb3VTZ"
BASE_URL = "https://open.feishu.cn/open-apis"
TOKEN_FILE = "/workspace/.lark_tokens.json"

# 加载持久化的 User Token
def load_tokens():
    p = pathlib.Path(TOKEN_FILE)
    if p.exists():
        return json.loads(p.read_text())
    return {}

def save_tokens(tokens):
    pathlib.Path(TOKEN_FILE).write_text(json.dumps(tokens, indent=2))

# ============ lark-mcp 调用（App Token） ============
def lark_call(tool_name, arguments=None):
    """通过 lark-mcp CLI 调飞书官方 MCP 工具（App Token）"""
    if arguments is None:
        arguments = {}
    env = os.environ.copy()
    env.pop("npm_config_prefix", None)
    cmd = ["lark-mcp", "mcp",
           "--app-id", APP_ID, "--app-secret", APP_SECRET,
           "--language", "zh", "--mode", "stdio"]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, env=env)
    init = {"jsonrpc":"2.0","id":1,"method":"initialize",
            "params":{"protocolVersion":"2024-11-05","capabilities":{},
                      "clientInfo":{"name":"lark-mcp","version":"1"}}}
    call = {"jsonrpc":"2.0","id":2,"method":"tools/call",
            "params":{"name":tool_name,"arguments":arguments}}
    inp = (json.dumps(init)+"\n"+json.dumps(call)+"\n").encode()
    try:
        out, _ = proc.communicate(input=inp, timeout=30)
        for line in out.decode().split("\n"):
            if line.strip():
                r = json.loads(line)
                if r.get("id") == 2:
                    return r.get("result", {})
    except subprocess.TimeoutExpired:
        proc.kill()
    return {"error": "timeout"}

# ============ Feishu Open API 调用（User Token） ============
def feishu_api(method, path, token=None, json_data=None, params=None):
    """
    直接调用飞书 Open API
    :param method: GET/POST/PUT/DELETE
    :param path: API 路径，如 /im/v1/messages
    :param token: User Access Token（留空则用文件中的）
    :param json_data: POST body dict
    :param params: URL query params dict
    """
    if token is None:
        tokens = load_tokens()
        token = tokens.get("user_access_token", "")

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = BASE_URL + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(json_data).encode() if json_data else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        return json.loads(resp.read())
    except urllib.request.HTTPError as e:
        body = e.read().decode()
        try:
            return json.loads(body)
        except:
            return {"error": f"HTTP {e.code}: {body[:200]}"}
    except Exception as e:
        return {"error": str(e)}

# ============ 便捷方法 ============
def send_message(chat_id, text):
    """发送文本消息到群聊"""
    return feishu_api("POST", "/im/v1/messages", json_data={
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }, params={"receive_id_type": "chat_id"})

def search_docs(keyword, count=10):
    """搜索云文档（需 User Token）"""
    return feishu_api("GET", "/suite/docs-api/search/object", params={
        "search_key": keyword, "count": count
    })

def get_doc_content(doc_token):
    """读取云文档内容（需 User Token）"""
    return feishu_api("GET", f"/docx/v1/documents/{doc_token}/raw_content")

def list_chats(page_size=50):
    """获取群聊列表（App Token）"""
    r = lark_call("im_v1_chat_list", {"user_id_type": "open_id", "page_size": page_size})
    content = r.get("content", [])
    for item in content:
        if item.get("type") == "text":
            return json.loads(item["text"])
    return r

def get_user_info(open_id):
    """查询用户信息"""
    r = lark_call("contact_v3_user_batchGetId",
                  {"user_id_type": "open_id", "open_ids": [open_id]})
    content = r.get("content", [])
    for item in content:
        if item.get("type") == "text":
            return json.loads(item["text"])
    return r

# ============ CLI 入口 ============
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "help":
        print("用法:")
        print("  python3 lark_mcp.py send <chat_id> <text>    # 发送消息")
        print("  python3 lark_mcp.py search <关键词>           # 搜索云文档")
        print("  python3 lark_mcp.py chats                    # 列出群聊")
        print("  python3 lark_mcp.py user <open_id>           # 查询用户")
        print("  python3 lark_mcp.py doc <doc_token>          # 读文档内容")
        print()
        print("  # 直接调任意 MCP 工具:")
        print('  python3 lark_mcp.py call im_v1_chat_list \'{"user_id_type":"open_id","page_size":5}\'')

    elif cmd == "send" and len(sys.argv) >= 4:
        result = send_message(sys.argv[2], sys.argv[3])
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "search" and len(sys.argv) >= 3:
        result = search_docs(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "chats":
        result = list_chats()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "user" and len(sys.argv) >= 3:
        result = get_user_info(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "doc" and len(sys.argv) >= 3:
        result = get_doc_content(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "call" and len(sys.argv) >= 3:
        tool_name = sys.argv[2]
        args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        result = lark_call(tool_name, args)
        content = result.get("content", [])
        for item in content:
            if item.get("type") == "text":
                print(item["text"])
        if result.get("isError"):
            print("Error:", result)
