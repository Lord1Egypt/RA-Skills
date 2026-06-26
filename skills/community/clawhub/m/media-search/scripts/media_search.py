#!/usr/bin/env python3
"""
媒体库搜索接口 - /api/media
基于媒体大数据平台的搜索功能实现
"""

import os
import sys
import time
import json
import argparse
import logging
import urllib.parse
import urllib3
import re
import warnings
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict, PrivateAttr
import requests

# 禁用 urllib3 的不安全请求警告
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

from token_manager import TokenManager


class SearchParameters(BaseModel):
    """搜索参数模型"""
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    keywords: str = Field(..., description="搜索关键词")
    keyword_position: Optional[str] = Field(
        default="标题或正文",
        description="关键词匹配位置: 标题、正文、标题或正文"
    )
    publish_time_start: Optional[str] = Field(
        default=None,
        description="发布开始时间，格式yyyy-MM-dd HH:mm:ss"
    )
    publish_time_end: Optional[str] = Field(
        default=None,
        description="发布结束时间，格式yyyy-MM-dd HH:mm:ss"
    )
    data_type: Optional[str] = Field(
        default=None,
        description="数据类型，直接映射到API的dataType参数"
    )
    source_name: Optional[str] = Field(
        default=None,
        description="具体信源名称，支持模糊匹配"
    )
    limit: Optional[int] = Field(
        default=10,
        ge=1, le=50,
        description="返回结果数量，1-50之间"
    )


class SearchResultItem(BaseModel):
    """搜索结果项模型"""
    title: str = Field(default="", description="文章标题")
    summary: str = Field(default="", description="文章摘要")
    publish_time: str = Field(default="", description="发布时间")
    source_name: str = Field(default="", description="信源名称")
    url: str = Field(default="", description="原文链接")
    content: Optional[str] = Field(default="", description="正文内容")
    relevance_score: Optional[float] = Field(default=0.0, description="相关性分数")


class MediaSearchResult(BaseModel):
    """媒体搜索返回结果模型"""
    success: bool = Field(..., description="是否成功")
    total: int = Field(default=0, description="总结果数")
    from_cache: bool = Field(default=False, description="是否来自缓存")
    fallback_to_web: bool = Field(default=False, description="是否降级到网页搜索")
    items: List[SearchResultItem] = Field(default_factory=list, description="搜索结果列表")
    query: str = Field(default="", description="原始查询")
    timestamp: str = Field(default="", description="查询时间")
    backend: str = Field(default="media_search", description="后端类型")
    error: Optional[str] = Field(default=None, description="错误信息")


class MediaSearchEngine:
    """
    媒体库搜索引擎
    提供基于媒体大数据平台的搜索功能
    """

    def __init__(self, token_manager: Optional[TokenManager] = None):
        """
        初始化搜索引擎

        Args:
            token_manager: Token管理器，如果为None则创建新的实例
        """
        self.token_manager = token_manager or TokenManager()
        self.base_url = "https://mbdapi.fzdzyun.com"
        self.api_endpoint = "/api/query/media"

        # 配置日志
        logging.basicConfig(
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.INFO,
        )
        self.logger = logging.getLogger(__name__)

    def _parse_time_range(self, params: SearchParameters) -> tuple[str, str]:
        """
        解析时间范围参数，直接使用传入的值不做额外处理

        Args:
            params: 搜索参数

        Returns:
            (开始时间, 结束时间) 元组，格式为 yyyy-MM-dd HH:mm:ss
        """
        # 直接使用传入的时间值，不做任何转换或默认值处理
        start_time = params.publish_time_start or ""
        end_time = params.publish_time_end or ""

        return start_time, end_time

    def _map_keyword_position(self, position: str) -> str:
        """
        映射关键词位置到API参数

        Args:
            position: 关键词位置描述

        Returns:
            API参数值
        """
        mapping = {
            "标题": "title",
            "正文": "content",
            "标题或正文": "title_content"
        }
        return mapping.get(position, "title_content")


    def _build_api_request(self, params: SearchParameters) -> Dict[str, Any]:
        """
        构建API请求参数

        Args:
            params: 搜索参数

        Returns:
            API请求参数字典
        """
        # 解析时间范围
        start_time, end_time = self._parse_time_range(params)

        # 构建请求参数
        request_params = {
            "keyWords": f"({params.keywords})",  # 添加括号提高搜索准确性
            "page": 1,
            "pagesize": params.limit,
            "queryField": self._map_keyword_position(params.keyword_position),
            "dataType": params.data_type if params.data_type else "news,app,wechat,wemedia,epaper,weibo",
            "beginTime": start_time,
            "endTime": end_time,
            "sortField": "score",
            "sortType": "desc",
            "showContent": 0,  # 不返回正文内容
            "duplicate": 1,
            "sourceRank": "1,2,3"  # 使用所有信源等级
        }

        # 添加可选参数
        if params.source_name:
            request_params["source"] = params.source_name

        # 移除空值参数
        return {k: v for k, v in request_params.items() if v}

    def _call_media_api(self, request_params: Dict[str, Any], timeout: int = 60) -> Optional[Dict[str, Any]]:
        """
        调用媒体库API

        Args:
            request_params: 请求参数
            timeout: 超时时间（秒）

        Returns:
            API响应数据，如果调用失败则返回None
        """
        # 获取访问Token
        access_token = self.token_manager.get_token()
        if not access_token:
            self.logger.error("无法获取访问Token")
            return None

        # 构建请求
        url = f"{self.base_url}{self.api_endpoint}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "token": access_token,
        }

        try:
            # 记录详细的API调用参数
            encoded_data = urllib.parse.urlencode(request_params)
            self.logger.info(f"调用媒体库API: {url}")
            self.logger.info(f"API请求参数: {request_params}")
            self.logger.info(f"请求头: {headers}")

            response = requests.post(
                url=url,
                data=encoded_data,
                headers=headers,
                timeout=timeout,
                verify=False,
            )
            response.raise_for_status()

            if response.status_code == 200:
                response.encoding = "utf-8"
                json_response = response.json()
                self.logger.info(f"API调用成功，状态码: {response.status_code}")
                return json_response
            else:
                self.logger.error(f"API调用失败: {response.status_code}")
                self.logger.error(f"错误响应: {response.text}")
                return None

        except requests.RequestException as e:
            self.logger.error(f"API请求异常: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"API响应解析失败: {e}")
            return None

    def _parse_api_response(self, api_response: Dict[str, Any], query: str) -> MediaSearchResult:
        """
        解析API响应数据

        Args:
            api_response: API响应数据
            query: 原始查询

        Returns:
            解析后的搜索结果
        """
        if not api_response:
            return MediaSearchResult(
                success=False,
                error="API响应为空",
                query=query,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

        # 检查API响应状态
        status = api_response.get("status")
        if status != 0:
            error_msg = api_response.get("message", "未知错误")
            return MediaSearchResult(
                success=False,
                error=f"API错误: {error_msg}",
                query=query,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

        # 解析数据
        data = api_response.get("data", {})
        rows = data.get("rows", [])

        # 转换结果项
        items = []
        for item in rows:
            # 清理HTML标签
            title = self._clean_html_tags(item.get("title", ""))
            summary = self._clean_html_tags(item.get("summary", ""))
            content = self._clean_html_tags(item.get("content", ""))

            search_item = SearchResultItem(
                title=title,
                summary=summary,
                publish_time=item.get("pubdate", ""),
                source_name=item.get("source", ""),
                url=item.get("location", ""),
                content=content if content else "",  # 处理showContent=0的情况
                relevance_score=item.get("score", 0.0)
            )
            items.append(search_item)

        # 记录解析结果摘要
        self.logger.info(f"API数据解析完成，找到 {len(items)} 条结果 (总计: {data.get('total', 0)})")

        return MediaSearchResult(
            success=True,
            total=data.get("total", len(items)),
            items=items,
            query=query,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    def _clean_html_tags(self, text: str) -> str:
        """
        清理HTML标签

        Args:
            text: 包含HTML标签的文本

        Returns:
            清理后的文本
        """
        if not text:
            return ""

        # 移除强调标签
        text = re.sub(r"</?em>", "", text)
        # 移除图片标签
        text = re.sub(r"<img[^>]*>", "", text, flags=re.IGNORECASE)
        # 移除其他HTML标签
        text = re.sub(r"<[^>]+>", "", text)

        return text.strip()

    def search(self, params: SearchParameters, timeout: int = 60) -> MediaSearchResult:
        """
        执行媒体库搜索

        Args:
            params: 搜索参数
            timeout: 超时时间（秒）

        Returns:
            搜索结果
        """
        try:
            # 记录搜索参数
            self.logger.info(f"开始执行搜索: 关键词='{params.keywords}', 时间范围='{params.publish_time_start}' 到 '{params.publish_time_end}'")
            self.logger.info(f"搜索参数详情: keyword_position='{params.keyword_position}', source_name='{params.source_name}', limit={params.limit}")

            # 验证参数
            if not params.keywords:
                return MediaSearchResult(
                    success=False,
                    error="搜索关键词不能为空",
                    query="",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

            # 构建API请求参数
            request_params = self._build_api_request(params)

            # 调用API
            api_response = self._call_media_api(request_params, timeout)

            # 解析响应
            result = self._parse_api_response(api_response, params.keywords)

            return result

        except Exception as e:
            self.logger.error(f"搜索执行异常: {e}")
            return MediaSearchResult(
                success=False,
                error=f"搜索执行异常: {str(e)}",
                query=params.keywords,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        description="媒体库搜索工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python media_search.py --keywords "人工智能 政策" --limit 20
  python media_search.py --keywords "乡村振兴" --limit 10
  python media_search.py --keywords "人民日报 一带一路" --source_name "人民日报"
        """,
    )

    parser.add_argument("--keywords", required=True, help="搜索关键词")
    parser.add_argument("--keyword_position", default="标题或正文",
                        choices=["标题", "正文", "标题或正文"],
                        help="关键词匹配位置")
    parser.add_argument("--publish_time_start", help="开始时间 (yyyy-MM-dd HH:mm:ss)")
    parser.add_argument("--publish_time_end", help="结束时间 (yyyy-MM-dd HH:mm:ss)")
    parser.add_argument("--source_name", help="具体信源名称")
    parser.add_argument("--limit", type=int, default=10,
                        help="返回结果数量 (1-50)")
    parser.add_argument("--timeout", type=int, default=60, help="超时时间（秒）")

    args = parser.parse_args()

    # 验证limit范围
    if args.limit < 1 or args.limit > 50:
        print("错误: limit必须在1-50之间")
        return 1

    # 创建搜索参数
    search_params = SearchParameters(
        keywords=args.keywords,
        keyword_position=args.keyword_position,
        publish_time_start=args.publish_time_start,
        publish_time_end=args.publish_time_end,
        source_name=args.source_name,
        limit=args.limit
    )

    # 执行搜索
    engine = MediaSearchEngine()
    result = engine.search(search_params, timeout=args.timeout)

    # 输出结果
    if result.success:
        print(f"搜索成功！找到 {result.total} 条结果")
        for i, item in enumerate(result.items, 1):
            print(f"\n{i}. {item.title}")
            if item.publish_time:
                print(f"   发布时间: {item.publish_time}")
            if item.source_name:
                print(f"   信源: {item.source_name}")
            if item.summary:
                print(f"   摘要: {item.summary}")
            if item.url:
                print(f"   链接: {item.url}")
    else:
        print(f"搜索失败: {result.error}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())