#!/usr/bin/env python3
"""
客如云(Keruyun)开放平台 API 抓取器
基于 scraper-template，适配 Tailwind CSS 菜单结构
"""
import sys, os, time, json, re
from pathlib import Path
from playwright.sync_api import sync_playwright

# 添加模板路径
TEMPLATE_DIR = Path(__file__).parent.parent.parent / "scraper-template" / "scripts"
sys.path.insert(0, str(TEMPLATE_DIR))
from scrape_base import OpenPlatformScraper

OUTPUT_DIR = Path(__file__).parent.parent / "references"

class KeruyunScraper(OpenPlatformScraper):
    
    def __init__(self):
        super().__init__(
            base_url="https://open.keruyun.com/official/developer.html",
            output_dir=str(OUTPUT_DIR),
            name="客如云(keruyun)",
        )
    
    def expand_menu(self, page) -> dict:
        """展开客如云菜单，发现所有API模块"""
        # 1. 点击 API文档 tab
        api_tab = page.query_selector('text="API文档"')
        if api_tab:
            self.safe_click(api_tab)
            time.sleep(4)
        
        # 2. 展开所有可展开的菜单项
        # 顶级分类: pl-32 且有 cursor-pointer
        # 子分类: pl-48
        # API: pl-64 (叶子节点)
        
        # 先展开所有顶级分类
        top_items = page.query_selector_all('[style*="padding-left: 32px"][class*="cursor-pointer"]')
        for item in top_items:
            self.safe_click(item, force=True)
            time.sleep(0.3)
        
        time.sleep(1)
        
        # 再展开所有子分类
        sub_items = page.query_selector_all('[style*="padding-left: 48px"][class*="cursor-pointer"]')
        for item in sub_items:
            self.safe_click(item, force=True)
            time.sleep(0.3)
        
        time.sleep(2)
        
        # 3. 收集所有API项
        modules = {}
        api_items = page.query_selector_all('[style*="padding-left: 64px"]')
        
        for item in api_items:
            # 提取 data-autolog 属性获取 API ID 和名称
            autolog = item.get_attribute("data-autolog") or ""
            name = item.inner_text().strip()
            
            # 解析 c2=api_id, c3=url_encoded_name
            c2_match = re.search(r'c2=([^&]+)', autolog)
            c3_match = re.search(r'c3=([^&]+)', autolog)
            
            api_id = c2_match.group(1) if c2_match else ""
            # URL decode c3
            from urllib.parse import unquote
            api_name_full = unquote(c3_match.group(1)) if c3_match else name
            
            if not name:
                continue
            
            # 根据上下文推断模块归属（通过前面的非API兄弟节点）
            # 简化：使用名称前缀作为模块ID
            modules[name] = {
                "name": name,
                "api_id_raw": api_id,
                "api_name_full": api_name_full,
                "style": item.get_attribute("style") or "",
            }
        
        # 重组为 module_id → sub_module → api 结构
        # 从文本内容推断层级关系
        all_text = page.inner_text("body")
        
        # 提取模块结构
        result = {}
        top_cats = page.query_selector_all('[style*="padding-left: 32px"]')
        for i, cat in enumerate(top_cats):
            cat_name = cat.inner_text().strip()
            text = cat.query_selector("span")
            if text:
                cat_name = text.inner_text().strip()
            
            if not cat_name or cat_name in ["解决方案", "平台规则", "平台入驻", "研发必读"]:
                continue
            
            # 找到此分类下的所有子模块
            # 简化：用 all_apis_index 来组织
            result[str(i)] = {
                "name": cat_name,
                "sub_modules": {},
                "direct_apis": [],
            }
        
        return result
    
    def navigate_to_api(self, page, api_name, api_info) -> bool:
        """点击API名称导航到详情页"""
        try:
            # Find by text
            item = page.query_selector(f'[style*="padding-left: 64px"]:has-text("{api_name}")')
            if item:
                self.safe_click(item, force=True)
                time.sleep(2)
                return True
        except:
            pass
        return False
    
    def extract_api_detail(self, page) -> dict:
        """从当前页面提取API详情"""
        detail = {
            "title": "", "method": "POST", "path": "",
            "auth": "", "qps": "",
            "request_params": [], "response_params": [],
            "response_example": None,
        }
        
        # API 标题
        h2 = page.query_selector("h2")
        if h2:
            full_title = h2.inner_text().strip()
            # 格式: "名称 - 描述"
            if " - " in full_title:
                parts = full_title.split(" - ", 1)
                detail["title"] = parts[0]
                detail["description"] = parts[1]
            else:
                detail["title"] = full_title
        
        # HTTP 方法和 URI
        text = page.inner_text("body")
        
        method_match = re.search(r'HTTP请求方式[：:]\s*(GET|POST|PUT|DELETE|PATCH)', text)
        if method_match:
            detail["method"] = method_match.group(1)
        
        uri_match = re.search(r'URI[：:]\s*(/\S+)', text)
        if uri_match:
            detail["path"] = uri_match.group(1)
        
        # 授权方式
        auth_match = re.search(r'授权方式[：:]\s*(.+)', text)
        if auth_match:
            detail["auth"] = auth_match.group(1).strip()
        
        # QPS
        qps_match = re.search(r'最大QPS[：:]\s*(\S+)', text)
        if qps_match:
            detail["qps"] = qps_match.group(1)
        
        # 解析表格
        tables = page.query_selector_all("table")
        for table in tables:
            rows = table.query_selector_all("tr")
            if not rows:
                continue
            
            headers = []
            for cell in rows[0].query_selector_all("th"):
                headers.append(cell.inner_text().strip())
            if not headers:
                for cell in rows[0].query_selector_all("td"):
                    headers.append(cell.inner_text().strip())
            
            # 请求参数表
            if "参数名" in headers and "类型" in headers:
                for row in rows[1:]:
                    cells = row.query_selector_all("td")
                    if len(cells) >= 3:
                        param = {
                            "name": cells[0].inner_text().strip(),
                            "type": cells[1].inner_text().strip(),
                            "required": cells[2].inner_text().strip() if len(cells) > 2 else "",
                            "description": cells[3].inner_text().strip() if len(cells) > 3 else "",
                        }
                        if param["name"] and param["name"] not in ["参数名", "code", "message", "messageUuid"]:
                            detail["response_params"].append(param)
            
            # 请求参数（如果表头不同）
            if "参数名" in headers and "是否必填" in headers:
                for row in rows[1:]:
                    cells = row.query_selector_all("td")
                    if len(cells) >= 3:
                        param = {
                            "name": cells[0].inner_text().strip(),
                            "type": cells[1].inner_text().strip(),
                            "required": cells[2].inner_text().strip() == "是",
                            "description": cells[3].inner_text().strip() if len(cells) > 3 else "",
                        }
                        if param["name"]:
                            detail["request_params"].append(param)
        
        # 响应示例 JSON
        code_blocks = page.query_selector_all("pre")
        for block in code_blocks:
            text = block.inner_text().strip()
            try:
                obj = json.loads(text)
                if isinstance(obj, dict) and "result" in obj:
                    detail["response_example"] = obj
                    break
            except:
                pass
        
        return detail


# ============ 简化版：直接点击+提取 ============

def scrape_simple():
    """简化抓取流程"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1200})
        page.set_default_timeout(15000)
        
        # 加载页面
        print("📂 加载客如云开放平台...")
        page.goto("https://open.keruyun.com/official/developer.html", timeout=30000)
        time.sleep(5)
        
        # 点击 API文档
        page.click('text="API文档"')
        time.sleep(5)
        
        # 展开所有菜单层级
        # Level 1: padding-left: 32px - 顶级分类
        # Level 2: padding-left: 48px - 子分类
        # Level 3: padding-left: 64px - API 项
        
        print("🔍 展开菜单...")
        l1_items = page.query_selector_all('[style*="padding-left: 32px"][class*="cursor-pointer"]')
        for item in l1_items:
            try:
                item.click(force=True)
                time.sleep(0.2)
            except:
                pass
        time.sleep(1)
        
        l2_items = page.query_selector_all('[style*="padding-left: 48px"][class*="cursor-pointer"]')
        for item in l2_items:
            try:
                item.click(force=True)
                time.sleep(0.2)
            except:
                pass
        time.sleep(2)
        
        # 收集所有 API 项
        api_items = page.query_selector_all('[style*="padding-left: 64px"]')
        print(f"📊 发现 {len(api_items)} 个 API 文档项\n")
        
        apis = []
        for i, item in enumerate(api_items):
            name = item.inner_text().strip()
            if name and name not in [a["name"] for a in apis]:
                apis.append({"index": i, "name": name})
        
        print(f"唯一 API: {len(apis)} 个")
        
        # 抓取每个 API 详情
        results = []
        for i, api in enumerate(apis):
            print(f"  [{i+1}/{len(apis)}] {api['name'][:50]}...", end=" ", flush=True)
            
            try:
                # 重新定位（页面可能已刷新）
                api_item = page.query_selector_all('[style*="padding-left: 64px"]')
                target = None
                for item in api_item:
                    if item.inner_text().strip() == api["name"]:
                        target = item
                        break
                
                if not target:
                    print("❌ not found")
                    continue
                
                target.click(force=True)
                time.sleep(2)
                
                # 提取详情
                text = page.inner_text("body")
                
                # Method
                method = "POST"
                mm = re.search(r'HTTP请求方式[：:]\s*(GET|POST|PUT|DELETE)', text)
                if mm:
                    method = mm.group(1)
                
                # URI
                path = ""
                um = re.search(r'URI[：:]\s*(/\S+)', text)
                if um:
                    path = um.group(1)
                
                # Title
                title = api["name"]
                h2 = page.query_selector("h2")
                if h2:
                    title = h2.inner_text().strip()
                    if " - " in title:
                        title = title.split(" - ")[0]
                
                results.append({
                    "name": api["name"],
                    "title": title,
                    "method": method,
                    "path": path,
                })
                
                print(f"✅ {method} {path[:40]}")
                
            except Exception as e:
                print(f"❌ {e}")
        
        # 保存结果
        with open(os.path.join(str(OUTPUT_DIR), "_keruyun_apis.json"), "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 完成: {len(results)} API 基本信息")
        print(f"📄 保存到: {OUTPUT_DIR}/_keruyun_apis.json")
        
        browser.close()
        return results


if __name__ == "__main__":
    scrape_simple()
