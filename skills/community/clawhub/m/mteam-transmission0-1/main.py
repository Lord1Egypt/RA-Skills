import os
import requests
from transmission_rpc import Client

# ================= 1. 认证、服务与网络配置 =================
MTEAM_API_KEY = "在这里填入你真实的 M-Team API Key"
MTEAM_API_BASE = "https://api.m-team.cc/api"

# Transmission 配置
TRANS_HOST = '10.1.1.10'
TRANS_PORT = 9091
TRANS_USER = 'admin'     
TRANS_PASS = 'password'

# 代理配置：解决服务运行时无法继承系统代理导致的 502/超时 问题
# 请将 7890 替换为你实际使用的代理软件端口（如 Clash 是 7890，v2ray 是 10809）
# 如果你在软路由端已经做了全局/透明代理，可以将这里改为 PROXIES = None
PROXIES = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

# 全局通用请求头，伪装成正常浏览器，防止被 Cloudflare 拦截
COMMON_HEADERS = {
    "x-api-key": MTEAM_API_KEY,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
# ==========================================================

# ================= 2. 目录映射配置 ========================
CATEGORY_PATH_MAPPING = {
    # === 电影类 ===
    "401": "/volume3/影视/电影",  # SD电影
    "419": "/volume3/影视/电影",  # HD电影
    "420": "/volume3/影视/电影",  # 原盘/UHD
    "404": "/volume3/影视/电影",  # 纪录片
    
    # === 电视剧与动漫类 ===
    "402": "/volume3/影视/剧",    # 剧集
    "438": "/volume3/影视/剧",    # 剧集包
    "405": "/volume3/影视/剧"     # 动漫
}
# ==========================================================

def format_size(bytes_size):
    """字节转换格式化"""
    try:
        bytes_size = float(bytes_size)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
    except:
        return "未知"

def get_seeders(item):
    """安全获取做种人数"""
    if 'status' in item and isinstance(item['status'], dict):
        return int(item['status'].get('seeders') or 0)
    return int(item.get('seeders') or 0)

def has_chinese_subtitle(title):
    """判断标题中是否包含中文字幕相关的关键词"""
    keywords = ['中字', '简', '繁', '中英', 'chs', 'cht', 'chi', '国配', '国语']
    title_lower = title.lower()
    return any(kw in title_lower for kw in keywords)

def search_mteam_torrents(keyword: str) -> str:
    """工具1：搜索种子（优先中字 + 代理防封版）"""
    payload = {"keyword": keyword, "visible": 1}
    
    try:
        # 加入 headers 伪装和 proxies 代理
        response = requests.post(
            f"{MTEAM_API_BASE}/torrent/search", 
            headers=COMMON_HEADERS, 
            json=payload, 
            proxies=PROXIES, 
            timeout=15
        )
        response.raise_for_status()
        
        data = response.json().get('data', {}).get('data', [])
        if not data:
            return "在 M-Team 中没有找到相关资源。"

        # 优先判断是否有中文字幕，然后再按做种人数降序
        sorted_data = sorted(data, key=lambda x: (has_chinese_subtitle(x.get('name', '')), get_seeders(x)), reverse=True)
        top_5 = sorted_data[:5]

        result_str = "找到以下资源：\n"
        for idx, item in enumerate(top_5, 1):
            title = item.get('name', '未知标题')
            size = format_size(item.get('size', 0))
            seeders = get_seeders(item)
            torrent_id = item.get('id', '')
            category = str(item.get('category', ''))
            
            # 给带中文字幕的种子加标记
            subtitle_mark = "💖[含中字/国配] " if has_chinese_subtitle(title) else ""
            
            result_str += f"[{idx}] ID: {torrent_id} | 标题: {subtitle_mark}{title} | 大小: {size} | 做种: {seeders} | 分类: {category}\n"
            
        return result_str

    except Exception as e:
        return f"搜索失败，错误信息: {str(e)}"

def download_torrent(torrent_id: str, category: str) -> str:
    """工具2：下载种子并推送到 Transmission（两步走 + 代理防封版）"""
    temp_filepath = f"/tmp/mteam_dl_{torrent_id}.torrent" 
    
    try:
        # 1. 获取专属下载链接 (走代理)
        token_url = f"{MTEAM_API_BASE}/torrent/genDlToken"
        token_resp = requests.post(
            token_url, 
            headers=COMMON_HEADERS, 
            data={"id": torrent_id}, 
            proxies=PROXIES, 
            timeout=10
        )
        token_data = token_resp.json()
        
        if str(token_data.get('code')) != '0':
            return f"❌ 获取下载链接失败，服务器返回: {token_data}"
            
        download_url = token_data.get('data')

        # 2. 真实下载种子文件并写入临时文件 (走代理)
        dl_resp = requests.get(
            download_url, 
            headers=COMMON_HEADERS, 
            proxies=PROXIES, 
            timeout=15
        )
        dl_resp.raise_for_status()
        
        if not dl_resp.content.startswith(b'd'):
            return "❌ 下载失败：获取到的不是合法的种子文件（可能被防火墙拦截）。"
            
        with open(temp_filepath, "wb") as f:
            f.write(dl_resp.content)

        # 3. 确定保存目录
        download_dir = CATEGORY_PATH_MAPPING.get(category, "/volume3/影视/其他")

        # 4. 添加到 Transmission
        c = Client(host=TRANS_HOST, port=TRANS_PORT, username=TRANS_USER, password=TRANS_PASS)
        with open(temp_filepath, "rb") as f:
            c.add_torrent(f, download_dir=download_dir)

        # 5. 清理临时文件
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

        return f"✅ 成功！种子已添加到 Transmission。\n📁 保存路径: {download_dir}"

    except Exception as e:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        return f"❌ 下载或推送到 Transmission 失败: {str(e)}"