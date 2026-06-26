"""
Web Scraper 单元测试
测试网页抓取功能（需要外部URL，请填写到下方列表）
"""

import pytest
import sys
sys.path.insert(0, 'd:/vscode/AI-podcast/ai-podcast-dual-host')

from src.web_scraper import WebScraper, WebScraperError


class TestWebScraper:
    """测试 WebScraper 类"""

    @pytest.fixture
    def scraper(self):
        return WebScraper(timeout=10)

    # ============ 测试URL配置 ============
    # 来源: tests/url/url-test.txt
    TEST_URLS = {
        "csdn_ai_article": "https://blog.csdn.net/csdnnews/article/details/159555175",
        "gitcode_glm5": "https://gitcode.com/atomgit-ascend/GLM-5-w4a8",
        "csdn_tech": "https://blog.csdn.net/csdnnews/article/details/159517430",
        "36kr_article": "https://36kr.com/p/3744568577064967",
        "huxiu_article": "https://www.huxiu.com/article/4846439.html",
        "sina_news": "https://news.sina.com.cn/w/2026-03-30/doc-inhstpih6551105.shtml",
        "qq_news": "https://news.qq.com/rain/a/20260330A044XD00",
    }
    # =============================================

    @pytest.mark.skipif(len(TEST_URLS) == 0, reason="未配置测试URL")
    def test_fetch_valid_url(self, scraper):
        """测试抓取有效URL"""
        for name, url in self.TEST_URLS.items():
            content = scraper.fetch(url)
            assert isinstance(content, str)
            assert len(content) > 500, f"{name}: 提取内容过短"
            print(f"\n{name}: 提取 {len(content)} 字符")

    def test_fetch_invalid_url(self, scraper):
        """测试无效URL应抛出异常"""
        with pytest.raises(WebScraperError):
            scraper.fetch("https://this-domain-does-not-exist-12345.com")

    def test_fetch_404(self, scraper):
        """测试404页面"""
        with pytest.raises(WebScraperError):
            scraper.fetch("https://httpbin.org/status/404")

    def test_fetch_empty_url(self, scraper):
        """测试空URL"""
        with pytest.raises(WebScraperError):
            scraper.fetch("")

    def test_fetch_malformed_url(self, scraper):
        """测试格式错误的URL"""
        with pytest.raises(WebScraperError):
            scraper.fetch("not-a-valid-url")


class TestWebScraperContentQuality:
    """测试内容提取质量"""

    @pytest.fixture
    def scraper(self):
        return WebScraper()

    # ============ 请在此处填写内容质量测试URL ============
    QUALITY_TEST_URLS = {
        # 格式: "测试名称": {
        #     "url": "...",
        #     "expected_keywords": ["关键词1", "关键词2"],
        #     "min_length": 1000,
        # }
    }
    # ====================================================

    @pytest.mark.skipif(len(QUALITY_TEST_URLS) == 0, reason="未配置质量测试URL")
    def test_content_quality(self, scraper):
        """测试内容质量"""
        for name, config in self.QUALITY_TEST_URLS.items():
            content = scraper.fetch(config["url"])

            # 检查长度
            assert len(content) >= config.get("min_length", 500), \
                f"{name}: 内容长度不足"

            # 检查关键词
            for keyword in config.get("expected_keywords", []):
                assert keyword in content, \
                    f"{name}: 未找到关键词 '{keyword}'"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
