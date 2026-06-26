"""
PC Controller API - 电脑控制统一接口
提供 FastAPI 接口用于远程控制电脑的各种功能
"""
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import Optional, List, Any
import uvicorn

from modules import screenshot, clipboard, keyboard, mouse, process, window, system, file, browser, shell
from modules.security import config as security_config, log_operation, SecurityMode

app = FastAPI(title="PC Controller API", description="电脑控制统一接口")


@app.middleware("http")
async def auth_middleware(request, call_next):
    """全局认证中间件"""
    if not security_config.enabled or not security_config.api_key:
        return await call_next(request)

    public_paths = ["/", "/docs", "/openapi.json", "/health"]
    if request.url.path in public_paths:
        return await call_next(request)

    auth_header = request.headers.get("authorization")
    if not auth_header:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=401,
            content={"detail": "缺少认证信息"}
        )

    if not auth_header.startswith("Bearer "):
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=401,
            content={"detail": "认证格式错误"}
        )

    token = auth_header[7:]
    if not security_config.verify_api_key(token):
        log_operation("auth_failed", {"token": token[:8] + "...", "path": request.url.path}, False, "API Key 验证失败")
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=403,
            content={"detail": "认证失败"}
        )

    log_operation("auth_success", {"path": request.url.path}, True)
    return await call_next(request)


def verify_api_key(authorization: Optional[str] = Header(None)):
    """验证 API Key"""
    if not security_config.enabled or not security_config.api_key:
        return True

    if not authorization:
        raise HTTPException(status_code=401, detail="缺少认证信息")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="认证格式错误")

    token = authorization[7:]
    if not security_config.verify_api_key(token):
        log_operation("auth_failed", {"token": token[:8] + "..."}, False, "API Key 验证失败")
        raise HTTPException(status_code=403, detail="认证失败")

    log_operation("auth_success", {"endpoint": "api"}, True)
    return True


def require_auth():
    """认证依赖"""
    return Depends(verify_api_key)


class ClipboardWriteRequest(BaseModel):
    text: str


class KeyPressRequest(BaseModel):
    key: str


class KeyTypeRequest(BaseModel):
    text: str
    interval: float = 0.05


class KeyHotkeyRequest(BaseModel):
    keys: List[str]


class KeyDownRequest(BaseModel):
    key: str


class KeyUpRequest(BaseModel):
    key: str


class MouseMoveRequest(BaseModel):
    x: int
    y: int
    duration: float = 0


class MouseClickRequest(BaseModel):
    x: Optional[int] = None
    y: Optional[int] = None
    clicks: int = 1


class MouseDragRequest(BaseModel):
    x: int
    y: int
    duration: float = 0.5


class MouseScrollRequest(BaseModel):
    clicks: int
    x: int = -1
    y: int = -1


class ProcessKillRequest(BaseModel):
    name: str


class WindowActionRequest(BaseModel):
    title: str


class FileReadRequest(BaseModel):
    path: str


class FileWriteRequest(BaseModel):
    path: str
    content: str


class FileListRequest(BaseModel):
    path: str


@app.get("/")
def root():
    return {"message": "PC Controller API", "version": "1.0.0"}


@app.get("/screenshot")
def api_screenshot(path: str = "screenshot.png"):
    return screenshot.take_screenshot(path)


@app.get("/screen-info")
def api_screen_info():
    return screenshot.get_screen_info()


@app.get("/clipboard/read")
def api_clipboard_read():
    return clipboard.clipboard_read()


@app.post("/clipboard/write")
def api_clipboard_write(req: ClipboardWriteRequest):
    return clipboard.clipboard_write(req.text)


@app.post("/key/press")
def api_key_press(req: KeyPressRequest):
    return keyboard.key_press(req.key)


@app.post("/key/type")
def api_key_type(req: KeyTypeRequest):
    return keyboard.key_type(req.text, req.interval)


@app.post("/key/hotkey")
def api_key_hotkey(req: KeyHotkeyRequest):
    return keyboard.key_hotkey(req.keys)


@app.post("/key/down")
def api_key_down(req: KeyDownRequest):
    return keyboard.key_down(req.key)


@app.post("/key/up")
def api_key_up(req: KeyUpRequest):
    return keyboard.key_up(req.key)


@app.post("/mouse/move")
def api_mouse_move(req: MouseMoveRequest):
    return mouse.mouse_move(req.x, req.y, req.duration)


@app.post("/mouse/click")
def api_mouse_click(req: MouseClickRequest):
    return mouse.mouse_click(req.x, req.y, req.clicks)


@app.post("/mouse/double")
def api_mouse_double(req: MouseClickRequest):
    return mouse.mouse_double_click(req.x, req.y)


@app.post("/mouse/right")
def api_mouse_right(req: MouseClickRequest):
    return mouse.mouse_right_click(req.x, req.y)


@app.post("/mouse/drag")
def api_mouse_drag(req: MouseDragRequest):
    return mouse.mouse_drag(req.x, req.y, req.duration)


@app.post("/mouse/scroll")
def api_mouse_scroll(req: MouseScrollRequest):
    return mouse.mouse_scroll(req.clicks, req.x, req.y)


@app.get("/mouse/position")
def api_mouse_position():
    return mouse.get_mouse_position()


@app.get("/process/list")
def api_process_list():
    return process.process_list()


@app.post("/process/kill")
def api_process_kill(req: ProcessKillRequest):
    return process.process_kill(req.name)


@app.post("/process/get")
def api_process_get(req: ProcessKillRequest):
    return process.process_get(req.name)


@app.get("/window/list")
def api_window_list():
    return window.window_list()


@app.post("/window/minimize")
def api_window_minimize(req: WindowActionRequest):
    return window.window_minimize(req.title)


@app.post("/window/maximize")
def api_window_maximize(req: WindowActionRequest):
    return window.window_maximize(req.title)


@app.post("/window/close")
def api_window_close(req: WindowActionRequest):
    return window.window_close(req.title)


@app.post("/window/focus")
def api_window_focus(req: WindowActionRequest):
    return window.window_focus(req.title)


@app.get("/system/info")
def api_system_info():
    return system.get_system_info()


@app.get("/system/displays")
def api_system_displays():
    return system.get_displays()


@app.post("/file/read")
def api_file_read(req: FileReadRequest):
    return file.file_read(req.path)


@app.post("/file/write")
def api_file_write(req: FileWriteRequest):
    return file.file_write(req.path, req.content)


@app.post("/file/list")
def api_file_list(req: FileListRequest):
    return file.file_list(req.path)


@app.post("/file/exists")
def api_file_exists(req: FileReadRequest):
    return file.file_exists(req.path)


class BrowserStartRequest(BaseModel):
    browser: str = "chromium"
    headless: bool = True


class BrowserNavigateRequest(BaseModel):
    url: str


class BrowserClickRequest(BaseModel):
    element: Optional[str] = None
    text: Optional[str] = None
    index: Optional[int] = None
    method: str = "auto"


class BrowserInputRequest(BaseModel):
    element: Optional[str] = None
    text: Optional[str] = None
    text_to_input: str = ""
    index: Optional[int] = None


class BrowserJsRequest(BaseModel):
    script: str


class BrowserWaitRequest(BaseModel):
    element: Optional[str] = None
    text: Optional[str] = None
    timeout: int = 5000


class BrowserScrollRequest(BaseModel):
    direction: str = "down"
    amount: int = 500


class BrowserExecuteScriptRequest(BaseModel):
    script: str


@app.post("/browser/start")
def api_browser_start(req: BrowserStartRequest):
    return browser.browser_start(req.browser, req.headless)


@app.post("/browser/close")
def api_browser_close():
    return browser.browser_close()


@app.post("/browser/navigate")
def api_browser_navigate(req: BrowserNavigateRequest):
    return browser.browser_navigate(req.url)


@app.get("/browser/info")
def api_browser_info():
    return browser.browser_info()


@app.get("/browser/elements")
def api_browser_elements():
    return browser.browser_elements()


@app.post("/browser/click")
def api_browser_click(req: BrowserClickRequest):
    return browser.browser_click(
        element=req.element,
        text=req.text,
        index=req.index,
        method=req.method
    )


@app.post("/browser/input")
def api_browser_input(req: BrowserInputRequest):
    return browser.browser_input(
        element=req.element,
        text=req.text,
        text_to_input=req.text_to_input,
        index=req.index
    )


@app.post("/browser/js")
def api_browser_js(req: BrowserJsRequest):
    return browser.browser_js(req.script)


@app.get("/browser/screenshot")
def api_browser_screenshot():
    return browser.browser_screenshot()


@app.post("/browser/wait")
def api_browser_wait(req: BrowserWaitRequest):
    return browser.browser_wait(
        element=req.element,
        text=req.text,
        timeout=req.timeout
    )


@app.post("/browser/back")
def api_browser_back():
    return browser.browser_back()


@app.post("/browser/forward")
def api_browser_forward():
    return browser.browser_forward()


@app.post("/browser/refresh")
def api_browser_refresh():
    return browser.browser_refresh()


@app.post("/browser/scroll")
def api_browser_scroll(req: BrowserScrollRequest):
    return browser.browser_scroll(req.direction, req.amount)


@app.post("/browser/execute_script")
def api_browser_execute_script(req: BrowserExecuteScriptRequest):
    return browser.browser_execute_script(req.script)


class ShellRunRequest(BaseModel):
    command: str
    shell: str = "powershell"
    timeout: int = 30


class ShellRunFileRequest(BaseModel):
    script_path: str
    shell: str = "powershell"
    timeout: int = 60


@app.post("/shell/run")
def api_shell_run(req: ShellRunRequest):
    return shell.shell_run(req.command, req.shell, req.timeout)


@app.post("/shell/run-file")
def api_shell_run_file(req: ShellRunFileRequest):
    return shell.shell_run_file(req.script_path, req.shell, req.timeout)


@app.get("/shell/info")
def api_shell_info():
    return shell.get_shell_info()


class SecurityModeRequest(BaseModel):
    mode: str
    api_key: Optional[str] = None


@app.get("/security/info")
def api_security_info():
    return security_config.get_mode_info()


@app.post("/security/mode")
def api_security_set_mode(req: SecurityModeRequest):
    """设置安全模式和 API Key"""
    if req.mode not in [SecurityMode.DISABLED, SecurityMode.RELAXED, SecurityMode.STANDARD, SecurityMode.STRICT]:
        return {"success": False, "data": None, "error": f"无效的安全模式: {req.mode}"}

    if req.api_key:
        security_config.set_api_key(req.api_key)

    security_config.apply_preset(req.mode)
    security_config.save_to_file()

    log_operation("security_mode_changed", {"mode": req.mode}, True)
    return {
        "success": True,
        "data": security_config.get_mode_info(),
        "error": None
    }


@app.get("/security/modes")
def api_security_modes():
    """获取所有可用的安全模式"""
    return {
        "success": True,
        "data": {
            mode: {
                "description": SecurityConfig.PRESETS[mode]["description"]
            }
            for mode in [SecurityMode.RELAXED, SecurityMode.STANDARD, SecurityMode.STRICT]
        },
        "error": None
    }


if __name__ == "__main__":
    import argparse
    from modules.security import config, SecurityMode, SecurityConfig

    def print_banner():
        print("=" * 50)
        print("   PC Controller API Server")
        print("=" * 50)
        print()

    def print_mode_menu():
        print("请选择安全模式:")
        print(f"  0. 禁用模式 (disabled)  - 不启用任何安全限制")
        print(f"  1. 宽松模式 (relaxed)    - 仅 API 认证，基本不限制功能")
        print(f"  2. 标准模式 (standard)   - 认证 + 基本沙箱保护 [推荐]")
        print(f"  3. 严格模式 (strict)    - 完整安全限制")
        print()

    def get_api_key_input():
        print("请输入 API Key (直接回车使用当前配置):")
        api_key = input("> ").strip()
        return api_key

    def start_server(port: int, mode: str, api_key: str = None):
        if api_key:
            config.set_api_key(api_key)

        config.apply_preset(mode)
        config.save_to_file()

        print()
        print(f"✓ 安全模式: {mode}")
        print(f"✓ API Key: {'已设置' if config.api_key else '未设置'}")
        print(f"✓ 服务器地址: http://localhost:{port}")
        print(f"✓ API 文档: http://localhost:{port}/docs")
        print()
        print("按 Ctrl+C 停止服务")
        print("-" * 50)

        uvicorn.run(app, host="0.0.0.0", port=port)

    def main():
        parser = argparse.ArgumentParser(description="PC Controller API Server")
        parser.add_argument("--port", "-p", type=int, default=8080, help="服务端口 (默认 8080)")
        parser.add_argument("--mode", "-m", type=str, choices=["disabled", "relaxed", "standard", "strict"],
                          help="安全模式")
        parser.add_argument("--api-key", "-k", type=str, help="API Key")
        parser.add_argument("--no-menu", action="store_true", help="不显示菜单，直接启动")

        args = parser.parse_args()

        print_banner()

        if args.mode:
            start_server(args.port, args.mode, args.api_key)
            return

        print_mode_menu()

        while True:
            choice = input("请选择 (0-3) 或直接回车选择标准模式: ").strip()

            if choice == "":
                choice = "2"

            if choice not in ["0", "1", "2", "3"]:
                print("无效选择，请重新输入")
                continue

            mode_map = {
                "0": SecurityMode.DISABLED,
                "1": SecurityMode.RELAXED,
                "2": SecurityMode.STANDARD,
                "3": SecurityMode.STRICT
            }

            selected_mode = mode_map[choice]

            if selected_mode != SecurityMode.DISABLED:
                api_key = get_api_key_input()
                if not api_key and not config.api_key:
                    print("警告: 未设置 API Key，安全模式将使用默认空密钥")
            else:
                api_key = None

            start_server(args.port, selected_mode, api_key if api_key else None)
            break

    main()
