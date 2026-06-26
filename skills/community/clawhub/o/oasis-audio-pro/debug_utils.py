import json

DEBUG = False


def set_debug(enabled: bool):
    global DEBUG
    DEBUG = enabled


def debug_print(message: str):
    if DEBUG:
        print(f"[DEBUG] {message}")


def log_request(method: str, url: str, **kwargs):
    if not DEBUG:
        return
    
    print(f"[DEBUG] >>> Request")
    print(f"[DEBUG]   Method: {method}")
    print(f"[DEBUG]   URL: {url}")
    
    if "json" in kwargs:
        print(f"[DEBUG]   Body: {json.dumps(kwargs['json'], ensure_ascii=False)}")
    elif "params" in kwargs:
        print(f"[DEBUG]   Params: {json.dumps(kwargs['params'], ensure_ascii=False)}")
    
    print(f"[DEBUG] >>> End Request")


def log_response(response, body=None):
    if not DEBUG:
        return
    
    print(f"[DEBUG] <<< Response")
    
    if hasattr(response, "status_code"):
        print(f"[DEBUG]   Status Code: {response.status_code}")
        try:
            print(f"[DEBUG]   Body: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        except Exception:
            print(f"[DEBUG]   Body: {response.text}")
    elif hasattr(response, "status"):
        print(f"[DEBUG]   Status Code: {response.status}")
        if body:
            try:
                print(f"[DEBUG]   Body: {json.dumps(json.loads(body), ensure_ascii=False, indent=2)}")
            except Exception:
                print(f"[DEBUG]   Body: {body}")
    
    print(f"[DEBUG] <<< End Response")
