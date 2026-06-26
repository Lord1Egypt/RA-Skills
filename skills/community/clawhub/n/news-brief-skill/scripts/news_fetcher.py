#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
News Fetcher Module
新闻获取模块：管理工具、渠道、执行新闻抓取
"""

import os
import json
import time
import random
import requests
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Any, Optional

from bs4 import BeautifulSoup
import feedparser

class NewsFetcher:
    """新闻获取器"""
    
    def __init__(self, user_id: str, user_config: Dict[str, Any]):
        self.user_id = user_id
        self.user_config = user_config
        self.project_root = Path(__file__).parent.parent
        
        # 加载配置文件
        self.tools_config = self._load_json_config("config/tools.json")
        self.sources_config = self._load_json_config("config/sources.json")
        
        # 初始化日志
        self.logger = self._setup_logger()
        
    def _load_json_config(self, config_path: str) -> Dict:
        """加载JSON配置文件"""
        config_file = self.project_root / config_path
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _setup_logger(self):
        """设置日志"""
        import logging
        log_dir = self.project_root / "data" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logger = logging.getLogger(f"NewsFetcher_{self.user_id}")
        if not logger.handlers:
            handler = logging.FileHandler(
                log_dir / f"news_fetch_{datetime.now().strftime('%Y%m%d')}.log"
            )
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def fetch_news(self) -> List[Dict[str, Any]]:
        """
        获取新闻主函数
        
        Returns:
            新闻列表
        """
        try:
            self.logger.info("开始获取新闻")
            
            # 1. 检测工具和渠道可用性
            self._check_tools_availability()
            self._check_sources_availability()
            
            # 2. 获取用户兴趣关键词
            interest_keywords = self.user_config.get('interest_keywords', [])
            domains = self.user_config.get('domains', ['tech'])
            
            # 3. 根据优先级获取新闻
            all_news = []
            
            # 尝试API接口
            if self.tools_config.get('api_interfaces'):
                api_news = self._fetch_from_apis(domains, interest_keywords)
                all_news.extend(api_news)
            
            # 尝试RSS订阅
            if self.tools_config.get('rss_feeds'):
                rss_news = self._fetch_from_rss(domains, interest_keywords)
                all_news.extend(rss_news)
            
            # 尝试网页爬虫
            if self.tools_config.get('web_crawlers'):
                crawler_news = self._fetch_from_crawlers(domains, interest_keywords)
                all_news.extend(crawler_news)
            
            # 4. 去重处理
            unique_news = self._remove_duplicates(all_news)
            
            # 5. 筛选和排序
            filtered_news = self._filter_and_sort_news(unique_news, interest_keywords)
            
            # 6. 限制条数
            max_items = self.user_config.get('max_items', 5)
            final_news = filtered_news[:max_items]
            
            self.logger.info(f"获取到 {len(final_news)} 条新闻")
            return final_news
            
        except Exception as e:
            self.logger.error(f"获取新闻时出错: {e}")
            # 应急方案：调用通用新闻聚合API
            return self._emergency_fetch(interest_keywords)
    
    def _check_tools_availability(self):
        """检测工具可用性并调整优先级"""
        # 更新工具成功率统计
        tools_updated = False
        
        for tool_type in ['api_interfaces', 'web_crawlers', 'rss_feeds']:
            tools = self.tools_config.get(tool_type, [])
            for tool in tools:
                # 基于最近3次成功率调整优先级
                success_rate = tool.get('success_rate', 0.5)
                if success_rate < 0.3:
                    tool['priority'] += 1  # 降低优先级
                    tools_updated = True
                elif success_rate > 0.8:
                    tool['priority'] = max(1, tool['priority'] - 1)  # 提升优先级
                    tools_updated = True
        
        if tools_updated:
            self._save_tools_config()
    
    def _check_sources_availability(self):
        """检测新闻源可用性"""
        sources_updated = False
        
        for domain_category, sources in self.sources_config.items():
            for source_name, source_info in sources.items():
                primary_domain = source_info.get('primary_domain')
                backup_domains = source_info.get('backup_domains', [])
                
                # 检测主域名
                if not self._is_domain_available(primary_domain):
                    source_info['failure_count'] = source_info.get('failure_count', 0) + 1
                    sources_updated = True
                    
                    # 切换到备用域名
                    if backup_domains:
                        for backup_domain in backup_domains:
                            if self._is_domain_available(backup_domain):
                                source_info['primary_domain'] = backup_domain
                                source_info['failure_count'] = 0
                                self.logger.info(f"切换 {source_name} 到备用域名: {backup_domain}")
                                break
                
                # 淘汰连续7天失效的渠道
                if source_info.get('failure_count', 0) >= 7:
                    source_info['status'] = 'inactive'
                    self.logger.warning(f"淘汰失效渠道: {source_name}")
                    sources_updated = True
        
        if sources_updated:
            self._save_sources_config()
    
    def _is_domain_available(self, domain: str) -> bool:
        """检测域名是否可用"""
        try:
            response = requests.get(f"https://{domain}", timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def _fetch_from_apis(self, domains: List[str], keywords: List[str]) -> List[Dict]:
        """从API接口获取新闻"""
        news_list = []
        apis = sorted(
            self.tools_config.get('api_interfaces', []),
            key=lambda x: x.get('priority', 999)
        )
        
        for api in apis:
            if api.get('success_rate', 0) < 0.1:  # 失效率太高跳过
                continue
                
            try:
                # 这里需要根据具体API实现，示例使用通用结构
                api_news = self._call_api(api, domains, keywords)
                news_list.extend(api_news)
                # 更新成功率
                self._update_tool_success_rate(api, True)
            except Exception as e:
                self.logger.error(f"API {api.get('name')} 调用失败: {e}")
                self._update_tool_success_rate(api, False)
        
        return news_list
    
    def _fetch_from_rss(self, domains: List[str], keywords: List[str]) -> List[Dict]:
        """从RSS订阅获取新闻"""
        news_list = []
        rss_feeds = sorted(
            self.tools_config.get('rss_feeds', []),
            key=lambda x: x.get('priority', 999)
        )
        
        for feed in rss_feeds:
            try:
                feed_url = feed.get('url')
                if not feed_url:
                    continue
                    
                feed_data = feedparser.parse(feed_url)
                for entry in feed_data.entries[:10]:  # 限制每源10条
                    title = entry.get('title', '')
                    link = entry.get('link', '')
                    published = entry.get('published', '')
                    
                    # 关键词过滤
                    if self._match_keywords(title, keywords):
                        news_item = {
                            'title': title,
                            'url': link,
                            'published': published,
                            'source': feed.get('name', 'RSS'),
                            'content': entry.get('summary', ''),
                            'domain': self._get_domain_from_url(link)
                        }
                        news_list.append(news_item)
                
                self._update_tool_success_rate(feed, True)
            except Exception as e:
                self.logger.error(f"RSS {feed.get('name')} 获取失败: {e}")
                self._update_tool_success_rate(feed, False)
        
        return news_list
    
    def _fetch_from_crawlers(self, domains: List[str], keywords: List[str]) -> List[Dict]:
        """从网页爬虫获取新闻"""
        news_list = []
        crawlers = sorted(
            self.tools_config.get('web_crawlers', []),
            key=lambda x: x.get('priority', 999)
        )
        
        for crawler in crawlers:
            try:
                domain_name = crawler.get('name')
                domains_list = crawler.get('domains', [])
                
                # 匹配用户感兴趣的领域
                if not any(d in domains for d in domains_list):
                    continue
                
                # 执行爬虫逻辑（这里简化为示例）
                crawler_news = self._execute_crawler(crawler, keywords)
                news_list.extend(crawler_news)
                self._update_tool_success_rate(crawler, True)
                
            except Exception as e:
                self.logger.error(f"爬虫 {crawler.get('name')} 执行失败: {e}")
                self._update_tool_success_rate(crawler, False)
        
        return news_list
    
    def _execute_crawler(self, crawler_config: Dict, keywords: List[str]) -> List[Dict]:
        """执行具体爬虫逻辑（示例实现）"""
        news_list = []
        base_url = f"https://{crawler_config.get('domains', [''])[0]}"
        
        try:
            response = requests.get(base_url, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 根据不同网站结构解析（这里简化）
            articles = soup.find_all(['article', 'div'], class_=lambda x: x and 'article' in x.lower())
            
            for article in articles[:5]:  # 限制每页5条
                title_elem = article.find(['h1', 'h2', 'h3', 'a'])
                if not title_elem:
                    continue
                    
                title = title_elem.get_text().strip()
                if not self._match_keywords(title, keywords):
                    continue
                
                link = title_elem.get('href', '')
                if link and not link.startswith('http'):
                    link = urljoin(base_url, link)
                
                news_item = {
                    'title': title,
                    'url': link,
                    'published': datetime.now().strftime('%Y-%m-%d'),
                    'source': crawler_config.get('name', 'Web Crawler'),
                    'content': '',
                    'domain': crawler_config.get('domains', [''])[0]
                }
                news_list.append(news_item)
                
        except Exception as e:
            self.logger.error(f"爬虫执行错误: {e}")
        
        return news_list
    
    def _match_keywords(self, text: str, keywords: List[str]) -> bool:
        """关键词匹配"""
        if not keywords:
            return True
        text_lower = text.lower()
        return any(kw.lower() in text_lower for kw in keywords)
    
    def _get_domain_from_url(self, url: str) -> str:
        """从URL提取域名"""
        try:
            return urlparse(url).netloc
        except:
            return ''
    
    def _remove_duplicates(self, news_list: List[Dict]) -> List[Dict]:
        """去重处理"""
        seen_titles = set()
        unique_news = []
        
        for news in news_list:
            title = news.get('title', '').lower()
            if title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(news)
        
        return unique_news
    
    def _filter_and_sort_news(self, news_list: List[Dict], keywords: List[str]) -> List[Dict]:
        """筛选和排序新闻"""
        # 按发布时间排序（最新在前）
        def get_publish_date(news):
            pub_date = news.get('published', '')
            try:
                return datetime.strptime(pub_date, '%Y-%m-%d')
            except:
                return datetime.now()
        
        sorted_news = sorted(news_list, key=get_publish_date, reverse=True)
        return sorted_news
    
    def _emergency_fetch(self, keywords: List[str]) -> List[Dict]:
        """应急获取方案"""
        self.logger.warning("启动应急获取方案")
        # 返回空列表或预设内容
        return []
    
    def _call_api(self, api_config: Dict, domains: List[str], keywords: List[str]) -> List[Dict]:
        """调用API接口（示例）"""
        # 实际实现需要根据具体API
        return []
    
    def _update_tool_success_rate(self, tool: Dict, success: bool):
        """更新工具成功率"""
        current_rate = tool.get('success_rate', 0.5)
        if success:
            tool['success_rate'] = min(1.0, current_rate + 0.1)
        else:
            tool['success_rate'] = max(0.0, current_rate - 0.2)
    
    def _save_tools_config(self):
        """保存工具配置"""
        tools_file = self.project_root / "config" / "tools.json"
        with open(tools_file, 'w', encoding='utf-8') as f:
            json.dump(self.tools_config, f, ensure_ascii=False, indent=2)
    
    def _save_sources_config(self):
        """保存新闻源配置"""
        sources_file = self.project_root / "config" / "sources.json"
        with open(sources_file, 'w', encoding='utf-8') as f:
            json.dump(self.sources_config, f, ensure_ascii=False, indent=2)