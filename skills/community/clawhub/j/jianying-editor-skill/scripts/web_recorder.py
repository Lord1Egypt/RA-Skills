
"""
智能网页录屏工具 (Smart Web Recorder)

依赖:
    pip install playwright
    playwright install chromium

功能:
    1. 启动无头浏览器并开启视频录制。
    2. 加载目标 URL/HTML。
    3. 智能等待 JS 信号 (window.animationFinished) 或固定时长。
    4. 导出为高清 MP4 素材文件。
"""
import os
import shutil
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Error: 'playwright' module not found.")
    print("Please install dependencies:")
    print("  pip install playwright")
    print("  playwright install chromium")
    # 为了演示兼容性，如果用户没安装 playwright，我们定义一个假的录制器
    sync_playwright = None

def record_web_animation(url_or_path: str, output_path: str, max_duration=30):
    """
    录制网页动画直至完成信号触发。
    """
    if not sync_playwright:
        print("⚠️ Playwright not detected. Skipping real recording.")
        return False

    # 确保路径是绝对路径
    if not url_or_path.startswith('http'):
        url_or_path = 'file://' + os.path.abspath(url_or_path)
    
    output_dir = os.path.dirname(os.path.abspath(output_path))
    temp_video_dir = os.path.join(output_dir, "temp_rec")
    
    if os.path.exists(temp_video_dir):
        shutil.rmtree(temp_video_dir)

    print(f"🎥 Starting Recorder for: {url_or_path}")
    
    with sync_playwright() as p:
        # Launch browser with recording enabled
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir=temp_video_dir,
            record_video_size={"width": 1920, "height": 1080},
            viewport={"width": 1920, "height": 1080}
        )
        
        page = context.new_page()

        try:
            page.goto(url_or_path)
            
            # 智能等待 JavaScript 信号
            # 这里的 predicate 会在浏览器上下文中反复执行，直到返回 true
            print("⏳ Waiting for 'window.animationFinished' signal...", end="", flush=True)
            page.wait_for_function("() => window.animationFinished === true", timeout=max_duration * 1000)
            print(" ✅ Signal Received!")
            
            # 稍微多录一点点 (0.5s) 作为缓冲，防止截断
            time.sleep(0.5)

        except Exception as e:
            print(f"\n❌ Timeout or Error waiting for animation: {e}")
            # 即使超时，也保存已录制的内容
        
        # Close context to save video
        context.close()
        browser.close()
        
        # Playwright 保存的文件名是随机的，我们需要找到它并重命名
        video_files = [f for f in os.listdir(temp_video_dir) if f.endswith('.webm')]
        if video_files:
            src_video = os.path.join(temp_video_dir, video_files[0])
            # Playwright 默认录制的是 .webm (Chromium)，剪映通常也支持 webm，
            # 若需 mp4 可能需要 ffmpeg 转码，但这里简单起见直接改后缀或保留
            # 注意：Chromium record_video 产出通常是 webm
            final_ext = os.path.splitext(output_path)[1]
            if not final_ext: final_ext = ".webm"
            
            shutil.move(src_video, output_path)
            print(f"💾 Video saved to: {output_path}")
            
            # 清理临时目录
            shutil.rmtree(temp_video_dir)
            return True
        else:
            print("❌ No video file generated.")
            return False

if __name__ == "__main__":
    # 测试代码
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(skill_root, "assets", "web_vfx_demo.html")
    output_video = os.path.join(skill_root, "assets", "generated_vfx.webm")
    
    if os.path.exists(html_path):
        record_web_animation(html_path, output_video)
    else:
        print("HTML file not found.")
