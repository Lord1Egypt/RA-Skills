# PCS数据自动转储录入脚本

import time
from playwright.sync_api import sync_playwright

# 配置
PCS_URL = "http://10.68.160.117:5173"
PCS_PAGE = "/#/vmodelDemo"
EBP_PAGE = "/#/home"

def extract_table_data(page):
    """从PCS页面抓取表格数据"""
    # 等待表格加载
    page.wait_for_selector("table", timeout=10000)
    
    # 获取所有行
    rows = page.query_selector_all("table tr")
    
    data = []
    for row in rows:
        cols = row.query_selector_all("td")
        if cols:
            row_data = [col.inner_text().strip() for col in cols]
            data.append(row_data)
    
    return data

def export_to_excel(data, filename="pcs_data.xlsx"):
    """导出数据到Excel"""
    import openpyxl
    
    wb = openpyxl.Workbook()
    ws = wb.active
    
    for row in data:
        ws.append(row)
    
    wb.save(filename)
    return filename

def import_to_epbp(page, filename):
    """导入Excel到EBP系统"""
    # 导航到EBP页面
    page.goto(f"{PCS_URL}{EBP_PAGE}")
    time.sleep(3)
    
    # 点击选择Excel文件按钮
    page.click('button:has-text("选择Excel文件")')
    time.sleep(1)
    
    # 找到文件上传输入框
    file_input = page.query_selector('input[type="file"]')
    if file_input:
        file_input.set_input_files(filename)
        time.sleep(2)
        print(f"已选择文件: {filename}")

    page.click('button:has-text("上传")')
    return True

def main():
    """主函数"""
    with sync_playwright() as p:
        # 启动浏览器 (无头模式)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 1. 访问PCS页面抓取数据
        print("访问PCS页面...")
        page.goto(f"{PCS_URL}{PCS_PAGE}")
        time.sleep(3)
        
        print("抓取表格数据...")
        data = extract_table_data(page)
        
        if not data:
            print("未获取到数据，请检查页面是否正确加载")
            return
        
        print(f"获取到 {len(data)} 行数据")
        
        # 2. 导出到Excel
        print("导出到Excel...")
        filename = export_to_excel(data)
        
        # 3. 导入到EBP
        print("导入到EBP系统...")
        import_to_epbp(page, filename)
        
        print("完成!")
        
        browser.close()

if __name__ == "__main__":
    main()
