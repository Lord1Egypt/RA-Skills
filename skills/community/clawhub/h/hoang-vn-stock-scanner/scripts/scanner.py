import argparse
import requests
import json
import xml.etree.ElementTree as ET
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_news(keywords=""):
    """Lấy tin tức mới nhất từ RSS của CafeF."""
    url = "https://cafef.vn/tin-tuc-su-kien.rss"
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10, verify=False)
        root = ET.fromstring(resp.content)
        
        results = []
        for item in root.findall('./channel/item')[:20]:
            title = item.find('title').text
            link = item.find('link').text
            
            # Lọc theo từ khóa (nếu có)
            if keywords:
                if any(kw.lower() in title.lower() for kw in keywords.split(",")):
                    results.append(f"📰 {title} ({link})")
            else:
                results.append(f"📰 {title} ({link})")
                
        if not results:
            print(json.dumps({"status": "success", "message": f"Không có tin tức nào chứa từ khóa: {keywords}"}, ensure_ascii=False))
        else:
            print(json.dumps({"status": "success", "news": results[:10]}, ensure_ascii=False))
            
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Lỗi cào tin CafeF: {str(e)}"}, ensure_ascii=False))

def get_ticker_info(ticker):
    """Lấy thông tin cơ bản của mã chứng khoán VN qua API public của TCBS."""
    url = f"https://apipubaws.tcbs.com.vn/tcanalysis/v1/ticker/{ticker.upper()}/overview"
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=5, verify=False)
        if resp.status_code == 200:
            data = resp.json()
            
            info = (
                f"📊 Mã: {data.get('ticker')}\\n"
                f"- Sàn: {data.get('exchange')}\\n"
                f"- Ngành: {data.get('industryEn')}\\n"
                f"- Vốn hóa: {data.get('marketCap', 0):,.0f} tỷ VND\\n"
                f"- P/E: {data.get('pe', 'N/A')}\\n"
                f"- P/B: {data.get('pb', 'N/A')}\\n"
                f"- Tỷ suất cổ tức (Dividend Yield): {data.get('dividendYield', 0)}%\\n"
                f"- EPS: {data.get('eps', 'N/A')}"
            )
            print(json.dumps({"status": "success", "info": info}, ensure_ascii=False))
        else:
            print(json.dumps({"status": "error", "message": f"Không tìm thấy mã {ticker}"}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Lỗi gọi API TCBS: {str(e)}"}, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(description="VN Stock Scanner - Quét tin tức và dữ liệu CKVN")
    parser.add_argument("action", choices=["news", "ticker"], help="Hành động: news (lấy tin) hoặc ticker (xem mã)")
    parser.add_argument("--ticker", type=str, default="", help="Mã cổ phiếu (VD: VCB, FPT)")
    parser.add_argument("--keywords", type=str, default="", help="Từ khóa lọc tin tức (VD: mua,bán,chủ tịch,lãi)")
    
    args = parser.parse_args()

    if args.action == "news":
        get_news(args.keywords)
    elif args.action == "ticker":
        if not args.ticker:
            print(json.dumps({"status": "error", "message": "Thiếu tham số --ticker"}, ensure_ascii=False))
        else:
            get_ticker_info(args.ticker)

if __name__ == "__main__":
    main()