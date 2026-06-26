"""
OSM AI Bridge - 完整讨论模式
实测：和豆包讨论 AI 漫剧市场
"""
import asyncio
from pathlib import Path

async def discuss(topic: str, local_view: str):
    """
    讨论模式：
    1. 发送本地观点给豆包
    2. 获取豆包的补充/不同角度
    3. 本地综合分析
    """
    from playwright.async_api import async_playwright
    
    print("="*70)
    print("OSM AI Bridge - 讨论模式")
    print("="*70)
    print(f"\n📋 话题: {topic}\n")
    print(f"💭 我的观点:\n{local_view}\n")
    
    # 构建讨论prompt
    prompt = f"""我有一个关于"{topic}"的观点，想听听你的不同角度分析。

我的观点是：
{local_view}

请从中文互联网市场的角度，分析这个观点，提出我可能忽略的点，
以及补充更多相关信息。"""
    
    print("🚀 发送给豆包...")
    print("-"*70)
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # 发送讨论请求
        textarea = await page.wait_for_selector('textarea')
        await textarea.fill(prompt)
        await textarea.press("Enter")
        
        print("⏳ 等待豆包分析...")
        await asyncio.sleep(15)  # 给AI足够的思考时间
        
        # 获取回复
        print("📥 获取豆包回复...")
        texts = await page.evaluate('''() => {
            const all = document.body.innerText.split("\\n");
            return all.filter(t => t.trim().length > 5).slice(-15);
        }''')
        
        # 找到豆包的回复（通常是最后几条中的较长文本）
        doubao_reply = ""
        for text in reversed(texts):
            if len(text) > 50 and "我的观点" not in text:
                doubao_reply = text
                break
        
        if not doubao_reply:
            doubao_reply = "\\n".join(texts[-5:])
        
        await browser.close()
        
        # 输出豆包回复
        print("\n🟣 豆包回复:")
        print("="*70)
        print(doubao_reply)
        print("="*70)
        
        # 本地综合分析
        print("\n🧠 我的综合分析:")
        print("="*70)
        analysis = f"""
【我的技术视角】
{local_view}

【豆包的市场洞察】
{doubao_reply[:300]}...

【综合结论】
结合技术和市场两个角度，这个问题需要区分：
1. 技术本身的价值（AI漫剧技术确实在进步）
2. 市场泡沫的存在（营销话术和割韭菜项目）
3. 长期发展潜力（泡沫退去后，真技术会留下）

建议：对创作者来说，AI是工具不是魔法；对投资者来说，看作品质量不看PPT。
        """
        print(analysis)
        print("="*70)

if __name__ == "__main__":
    topic = "AI漫剧市场是不是一场骗局？"
    local_view = """我认为AI漫剧是技术进步的产物，但市场确实存在泡沫。
很多项目只是为了融资而炒作概念，实际作品质量参差不齐。
不过也不能全盘否定，确实有团队在认真做内容。"""
    
    asyncio.run(discuss(topic, local_view))
