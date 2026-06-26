"""
OSM AI Bridge - 完整实现版
兑现 SKILL.md 承诺的所有功能
"""
import os
import sys
import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime

# 配置目录
CONFIG_DIR = Path.home() / ".openclaw" / "ai_bridge"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# 生产级日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(CONFIG_DIR / 'ai_bridge.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('osm_ai_bridge')

class AIBridge:
    """
    OSM AI Bridge - 完整实现
    - CDP连接浏览器
    - 反检测脚本注入
    - Cookie/LocalStorage访问
    - 自动启动浏览器
    - 生产级错误处理
    """
    
    CDP_URL = "http://localhost:9222"
    
    def __init__(self, ai_name: str):
        self.ai_name = ai_name
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        
    async def _check_cdp_available(self) -> bool:
        """检查CDP是否可用"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.CDP_URL}/json/version", timeout=3) as resp:
                    return resp.status == 200
        except:
            return False
    
    async def _start_browser_with_debugging(self):
        """自动启动带调试端口的浏览器"""
        import subprocess
        
        # 查找浏览器
        edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
        if not Path(edge_path).exists():
            edge_path = r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
        
        if not Path(edge_path).exists():
            raise RuntimeError("未找到Edge浏览器")
        
        logger.info("启动带调试端口的Edge...")
        
        # 启动Edge（独立user data，不干扰用户主浏览器）
        debug_profile = CONFIG_DIR / "edge_debug_profile"
        debug_profile.mkdir(exist_ok=True)
        
        subprocess.Popen([
            edge_path,
            f"--remote-debugging-port=9222",
            f"--user-data-dir={debug_profile}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-blink-features=AutomationControlled",
            "https://www.doubao.com" if self.ai_name == "doubao" else "https://gemini.google.com"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 等待启动
        logger.info("等待浏览器启动...")
        await asyncio.sleep(5)
        
        # 等待CDP可用
        for i in range(10):
            if await self._check_cdp_available():
                logger.info("浏览器已就绪")
                return True
            await asyncio.sleep(1)
        
        raise RuntimeError("浏览器启动超时")
    
    async def _inject_anti_detection(self):
        """注入反检测脚本"""
        if not self.context:
            return
            
        logger.info("注入反检测脚本...")
        
        await self.context.add_init_script("""
            // 隐藏 webdriver
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // 模拟真实插件
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
                    {name: 'Native Client', filename: 'internal-nacl-plugin'},
                    {name: 'Widevine Content Decryption Module', filename: 'widevinecdmadapter.dll'}
                ]
            });
            
            // 隐藏 automation 标记
            delete navigator.__proto__.webdriver;
            
            // 模拟 Chrome
            window.chrome = {
                runtime: {
                    OnInstalledReason: {CHROME_UPDATE: "chrome_update"},
                    PlatformOs: {WIN: "win"},
                    PlatformArch: {X86_64: "x86-64"}
                }
            };
            
            // 覆盖 Permissions API
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => {
                if (parameters.name === 'notifications') {
                    return Promise.resolve({ state: 'prompt' });
                }
                return originalQuery(parameters);
            };
            
            // 模拟 WebGL
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Inc.';
                if (parameter === 37446) return 'Intel Iris OpenGL Engine';
                return getParameter(parameter);
            };
        """)
        
        logger.info("反检测脚本已注入")
    
    async def _access_storage(self):
        """访问Cookie和LocalStorage"""
        if not self.page:
            return {}
        
        try:
            # 获取Cookies
            cookies = await self.context.cookies()
            
            # 获取LocalStorage
            local_storage = await self.page.evaluate('() => {
                const items = {};
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    items[key] = localStorage.getItem(key);
                }
                return items;
            }')
            
            logger.info(f"访问到 {len(cookies)} 个cookies, {len(local_storage)} 个localStorage项")
            
            return {
                'cookies': cookies,
                'localStorage': local_storage
            }
        except Exception as e:
            logger.warning(f"访问storage失败: {e}")
            return {}
    
    async def start(self):
        """启动连接"""
        from playwright.async_api import async_playwright
        
        self.playwright = await async_playwright().start()
        
        # 检查CDP是否可用，如不可用则自动启动浏览器
        if not await self._check_cdp_available():
            await self._start_browser_with_debugging()
        else:
            logger.info("连接到现有浏览器...")
        
        # 连接浏览器
        self.browser = await self.playwright.chromium.connect_over_cdp(self.CDP_URL)
        
        # 获取或创建上下文
        contexts = self.browser.contexts
        if contexts:
            self.context = contexts[0]
            logger.info(f"使用现有上下文，{len(self.context.pages)} 个页面")
        else:
            self.context = await self.browser.new_context()
        
        # 注入反检测脚本
        await self._inject_anti_detection()
        
        # 获取或创建页面
        pages = self.context.pages
        if pages:
            self.page = pages[0]
        else:
            self.page = await self.context.new_page()
        
        # 访问Cookie/LocalStorage
        await self._access_storage()
        
        return True
    
    async def ask(self, question: str) -> str:
        """问AI"""
        logger.info(f"开始Ask流程 - AI: {self.ai_name}, 问题: {question[:50]}...")
        
        try:
            # 启动连接
            await self.start()
            
            # 确保在正确页面
            url = "https://www.doubao.com" if self.ai_name == "doubao" else "https://gemini.google.com"
            
            if url not in self.page.url:
                logger.info(f"导航到 {self.ai_name}...")
                await self.page.goto(url, timeout=60000)
                await asyncio.sleep(3)
            
            # 检查登录
            logger.info("检查登录状态...")
            if self.ai_name == "gemini":
                login_needed = await self.page.query_selector('text=Sign in')
            else:
                login_needed = await self.page.query_selector('text=登录')
            
            if login_needed:
                logger.warning("需要登录，请在浏览器中完成")
                print("\n⚠️  请完成登录后按 Enter 继续...")
                input()
                # 重新检查
                login_still = await self.page.query_selector('text=登录') if self.ai_name != "gemini" else await self.page.query_selector('text=Sign in')
                if login_still:
                    return "登录未完成"
            else:
                logger.info("已登录")
            
            # 发送问题
            logger.info("发送问题...")
            input_box = await self.page.wait_for_selector('textarea', timeout=10000)
            await input_box.fill(question)
            await input_box.press("Enter")
            
            # 等待回复
            logger.info("等待回复生成...")
            await asyncio.sleep(12)
            
            # 提取回复
            logger.info("提取回复...")
            texts = await self.page.evaluate('''() => {
                const all = document.body.innerText.split("\\n");
                return all.filter(t => t.trim().length > 5).slice(-10);
            }''')
            
            # 找到AI回复（通常是较长的文本）
            reply = ""
            for text in reversed(texts):
                if len(text) > 20 and question not in text:
                    reply = text
                    break
            
            if not reply:
                reply = "\\n".join(texts[-3:])
            
            logger.info("Ask流程完成")
            return reply
            
        except Exception as e:
            logger.error(f"Ask流程出错: {e}", exc_info=True)
            return f"错误: {str(e)}"
        finally:
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()

async def main():
    """主函数"""
    question = sys.argv[1] if len(sys.argv) > 1 else "你好"
    
    print("="*60)
    print("OSM AI Bridge")
    print("="*60)
    
    bridge = AIBridge("doubao")
    result = await bridge.ask(question)
    
    print(f"\n回复:\n{result}")
    print("="*60)
    print(f"\n日志文件: {CONFIG_DIR / 'ai_bridge.log'}")

if __name__ == "__main__":
    asyncio.run(main())
