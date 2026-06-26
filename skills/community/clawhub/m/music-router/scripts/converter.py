import re
import json
import sys
import urllib.parse
import requests
import logging
import os
import time

class MusicLinkConverter:
    def __init__(self, enable_logging=False):
        self.platforms = {
            "netease": {
                "name": "网易云音乐",
                "patterns": [r"music\.163\.com", r"y\.music\.163\.com"],
                "search_url": "https://music.163.com/#/search/m/?s={query}",
                "link_template": "https://music.163.com/#/song?id={id}"
            },
            "qq": {
                "name": "QQ音乐",
                "patterns": [r"y\.qq\.com", r"c6\.y\.qq\.com", r"c\.y\.qq\.com"],
                "search_url": "https://y.qq.com/n/ryqq/search?w={query}",
                "link_template": "https://y.qq.com/n/ryqq/songDetail/{songmid}"
            },
            "spotify": {"name": "Spotify", "patterns": [r"open\.spotify\.com", r"spotify\.link"]},
            "youtube": {"name": "YouTube Music", "patterns": [r"music\.youtube\.com"]},
            "apple": {"name": "Apple Music", "patterns": [r"music\.apple\.com"]},
            "amazon": {"name": "Amazon Music", "patterns": [r"music\.amazon\.com"]},
            "tidal": {"name": "Tidal", "patterns": [r"tidal\.com"]}
        }
        self.enable_logging = enable_logging
        self.logger = self._setup_logging()

    def _setup_logging(self):
        logger = logging.getLogger("MusicLinkConverter")
        if logger.hasHandlers():
            logger.handlers.clear()
            
        if not self.enable_logging:
            logger.addHandler(logging.NullHandler())
            return logger

        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "converter.log")

        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        
        return logger

    def identify_platform(self, url):
        self.logger.debug(f"Identifying platform for URL: {url}")
        for platform_id, info in self.platforms.items():
            for pattern in info["patterns"]:
                if re.search(pattern, url):
                    self.logger.info(f"Identified platform: {platform_id}")
                    return platform_id
        self.logger.warning("Platform not identified")
        return None

    def get_song_info(self, url, platform_id):
        """从链接中提取歌曲信息"""
        self.logger.debug(f"Extracting song info from {platform_id} URL: {url}")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
            }
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            html = response.text
            
            title_match = re.search(r'<title>(.*?)</title>', html)
            if title_match:
                title = title_match.group(1).strip()
                
                if platform_id == "netease":
                    title = title.replace(" - 网易云音乐", "").replace(" - 单曲", "").strip()
                elif platform_id == "qq":
                    title = title.replace(" - QQ音乐", "").strip()
                elif platform_id == "spotify":
                    title = title.replace(" | Spotify", "")
                    if " - song and lyrics by " in title:
                        title = title.replace(" - song and lyrics by ", " ")
                    elif " - song by " in title:
                        title = title.replace(" - song by ", " ")
                elif platform_id == "apple":
                    title = title.replace(" on Apple Music", "").strip()
                
                self.logger.info(f"Cleaned song info: {title}")
                return title
        except Exception as e:
            self.logger.error(f"Error extracting song info: {e}")
        return None

    def get_songlink_data(self, url):
        """使用 Odesli (song.link) API 获取并解析所有平台链接及封面图"""
        self.logger.debug(f"Fetching song.link data for URL: {url}")
        api_url = f"https://api.song.link/v1-alpha.1/links?url={urllib.parse.quote(url)}"
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                links_by_platform = data.get("linksByPlatform", {})
                
                results = {"links": {}, "thumbnail": None}
                
                entities = data.get("entitiesByUniqueId", {})
                if entities:
                    first_entity = next(iter(entities.values()))
                    results["thumbnail"] = first_entity.get("thumbnailUrl")
                
                platform_map = {
                    "spotify": "Spotify",
                    "appleMusic": "Apple Music",
                    "youtube": "YouTube",
                    "youtubeMusic": "YouTube Music",
                    "amazonMusic": "Amazon Music",
                    "tidal": "Tidal",
                    "deezer": "Deezer",
                    "soundcloud": "SoundCloud"
                }
                
                for api_pid, info in links_by_platform.items():
                    if api_pid in platform_map:
                        results["links"][platform_map[api_pid]] = info.get("url")
                
                results["song.link (Aggregation)"] = data.get("pageUrl")
                return results
        except Exception as e:
            self.logger.error(f"Error fetching song.link data: {e}")
        return None

    def search_netease_api(self, query):
        self.logger.debug(f"Searching Netease for: {query}")
        search_url = f"https://music.163.com/api/search/get/web?s={urllib.parse.quote(query)}&type=1&limit=1"
        try:
            response = requests.get(search_url, timeout=10)
            data = response.json()
            songs = data.get("result", {}).get("songs", [])
            if songs:
                song_id = songs[0].get("id")
                link = self.platforms["netease"]["link_template"].format(id=song_id)
                self.logger.info(f"Netease link found: {link}")
                return link
        except Exception as e:
            self.logger.error(f"Error searching Netease: {e}")
        return None

    def search_qq_api(self, query, retries=2):
        self.logger.debug(f"Searching QQ Music for: {query}")
        search_url = f"https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=1&w={urllib.parse.quote(query)}&format=json"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://y.qq.com/'
        }
        
        for i in range(retries + 1):
            try:
                response = requests.get(search_url, headers=headers, timeout=10)
                if response.status_code == 500:
                    if i < retries:
                        time.sleep(1)
                        continue
                    return None
                
                text = response.text
                if text.startswith("callback(") or text.startswith("jsonp("):
                    text = text[text.find("(")+1 : text.rfind(")")]
                
                data = json.loads(text)
                songs = data.get("data", {}).get("song", {}).get("list", [])
                if songs:
                    song_mid = songs[0].get("songmid")
                    link = self.platforms["qq"]["link_template"].format(songmid=song_mid)
                    self.logger.info(f"QQ Music link found: {link}")
                    return link
            except Exception as e:
                self.logger.error(f"Error searching QQ Music: {e}")
                if i < retries:
                    time.sleep(1)
                    continue
        return None

    def convert(self, url, song_info=None):
        platform_id = self.identify_platform(url)
        if not platform_id:
            return {"error": "无法识别的平台链接"}

        if not song_info:
            song_info = self.get_song_info(url, platform_id)
            if not song_info:
                song_info = "未知歌曲"

        results = {}
        thumbnail = None
        
        if platform_id != "netease":
            netease_link = self.search_netease_api(song_info)
            results["网易云音乐"] = netease_link if netease_link else self.platforms["netease"]["search_url"].format(query=urllib.parse.quote(song_info))

        if platform_id != "qq":
            qq_link = self.search_qq_api(song_info)
            results["QQ音乐"] = qq_link if qq_link else self.platforms["qq"]["search_url"].format(query=urllib.parse.quote(song_info))

        songlink_data = self.get_songlink_data(url)
        if songlink_data:
            thumbnail = songlink_data.get("thumbnail")
            for platform_name, link in songlink_data["links"].items():
                if platform_id == "spotify" and platform_name == "Spotify": continue
                if platform_id == "apple" and platform_name == "Apple Music": continue
                if platform_id == "youtube" and platform_name == "YouTube Music": continue
                results[platform_name] = link
        else:
            results["song.link (Aggregation)"] = f"https://song.link/{url}"

        output = {
            "original_platform": self.platforms[platform_id]["name"],
            "detected_song": song_info,
            "thumbnail": thumbnail,
            "conversions": results
        }
        
        if self.enable_logging:
            output["log_file"] = os.path.join("music-router", "data", "converter.log")
            
        return output

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Music Link Converter')
    parser.add_argument('url', help='Music sharing link')
    parser.add_argument('song_info', nargs='?', default=None, help='Song name and artist')
    parser.add_argument('--log', action='store_true', help='Enable logging to file')
    
    args = parser.parse_args()
    
    converter = MusicLinkConverter(enable_logging=args.log)
    result = converter.convert(args.url, args.song_info)
    print(json.dumps(result, ensure_ascii=False, indent=2))
