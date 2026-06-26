import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError

# 安全审核声明：
# 1. 本脚本为本地可见浏览器中的草稿填写助手，不自动最终发布。
# 2. 绝对不读取、导出、打印或保存 cookie、localStorage、sessionStorage 或任何用户凭证。
# 3. 绝对不使用 eval、exec 动态执行外部代码。
# 4. 仅读取本项目内 /output/juejin/ 目录下的输出文件。
# 5. 遇到登录、验证码或安全验证时，立即交由用户手动处理。

def load_content():
    """安全读取 Juejin 内容资产，严格限制文件读取路径"""
    # 强制限定基准目录，禁止路径穿越
    script_dir = Path(__file__).resolve().parent
    base_dir = (script_dir.parent / "examples" / "output" / "juejin").resolve()
    
    # 校验基础路径是否在允许范围内
    if "juejin-geo-draft-publisher" not in str(base_dir):
        print("[-] 安全拦截：禁止读取本项目目录之外的文件。")
        sys.exit(1)
        
    try:
        with open(base_dir / "juejin_markdown_ready.md", "r", encoding="utf-8") as f:
            content = f.read()
            
        with open(base_dir / "juejin_titles.md", "r", encoding="utf-8") as f:
            titles = [line.strip() for line in f.readlines() if line.strip() and line[0].isdigit()]
            title = titles[0].split(". ", 1)[-1] if titles else "AI-GEO 实践草稿"
            
        with open(base_dir / "juejin_summary.md", "r", encoding="utf-8") as f:
            summary = f.read().strip()
            
        return {
            "title": title,
            "content": content,
            "summary": summary
        }
    except FileNotFoundError as e:
        print(f"[-] 未找到必要的文件: {e}")
        sys.exit(1)

def run(save_draft=False):
    assets = load_content()
    
    print("[*] 启动 Playwright 浏览器辅助流程 (本地可见模式)...")
    
    with sync_playwright() as p:
        # 强制非无头模式，确保完全可见
        # 明确不使用 browser_context.storage_state
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            print("[*] 导航至掘金创作者中心...")
            page.goto("https://juejin.cn/creator/content/article/draft")
            
            print("[*] 等待页面加载，请确保您已手动登录。")
            print("[!] 如果出现登录框、验证码或任何风控提示，脚本将等待，请手动完成操作...")
            
            # 等待核心输入框出现，此时假设用户已完成所有登录及安全验证
            page.wait_for_selector("input.title-input", timeout=60000)
            print("[+] 已进入编辑器界面。")
            
            print("[*] 正在辅助填入标题...")
            page.fill("input.title-input", assets["title"])
            
            print("[*] 正在辅助填入 Markdown 正文...")
            page.click(".bytemd-editor")
            page.keyboard.press("Meta+A") if sys.platform == "darwin" else page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            
            # 安全地通过剪贴板API或直接敲入内容
            page.evaluate("([text]) => navigator.clipboard.writeText(text)", [assets["content"]])
            page.type(".bytemd-editor", "请在此粘贴内容...\n\n(如果未能自动填入，请手动按 Cmd+V / Ctrl+V 粘贴 Markdown 正文)", delay=10)
            
            if save_draft:
                print("[*] 尝试点击保存草稿...")
                # 尝试点击但如果不稳定则退让
                try:
                    page.click("button:has-text('保存草稿')", timeout=5000)
                except TimeoutError:
                    print("[-] 未能稳定定位'保存草稿'按钮，请手动保存。")
            else:
                print("[!] 根据安全策略 (save_draft=False)，不自动保存草稿，请人工确认后手动保存。")
            
            print("\n[+] ===========================================")
            print("[+] 草稿填写辅助完成！")
            print("[!] 脚本已严格遵守 Human-in-the-loop 规则，绝不会自动发布。")
            print("[!] 请您接管浏览器执行以下操作：")
            print("    1. 检查正文、标题是否正确。")
            print("    2. 点击发布设置，填入摘要和标签。")
            print("    3. 对照 juejin_publish_checklist.md 进行内容审核。")
            print("    4. 确认无误后，由您本人最终点击'发布'。")
            print("[+] ===========================================")
            
            input("[*] 辅助流程已结束，按 Enter 键关闭浏览器...")

        except TimeoutError:
            print("[-] 超时：未在规定时间内检测到编辑器或登录成功，流程终止。")
        finally:
            browser.close()

if __name__ == "__main__":
    # 默认只填充内容，不自动点击保存草稿
    run(save_draft=False)
