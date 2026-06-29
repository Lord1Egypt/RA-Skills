"""Tests for jd_link_converter."""

import sys
import os
import pytest

# 将 scripts 目录加入路径以导入模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from jd_link_converter import extract_product_id, convert_jd_link


class TestExtractProductId:
    """测试从各类URL中提取商品ID。"""

    def test_mobile_url_with_product(self):
        url = "https://item.m.jd.com/product/100198170140.html?utm_source=iosapp"
        assert extract_product_id(url) == "100198170140"

    def test_mobile_url_without_product(self):
        url = "https://item.m.jd.com/100120810291.html?utm_medium=appshare"
        assert extract_product_id(url) == "100120810291"

    def test_pc_url(self):
        url = "https://item.jd.com/100198170140.html"
        assert extract_product_id(url) == "100198170140"

    def test_pc_url_with_params(self):
        url = "https://item.jd.com/100120810291.html?cu=true&utm_source=share"
        assert extract_product_id(url) == "100120810291"

    def test_pc_url_without_html(self):
        url = "https://item.jd.com/100355076774"
        assert extract_product_id(url) == "100355076774"

    def test_pure_product_id(self):
        assert extract_product_id("100198170140") == "100198170140"

    def test_short_product_id(self):
        assert extract_product_id("1000400") == "1000400"

    def test_non_jd_url_returns_none(self):
        url = "https://www.example.com/some-page"
        assert extract_product_id(url) is None

    def test_too_short_id_returns_none(self):
        # 5位数字太短，不符合商品ID规则
        assert extract_product_id("12345") is None


class TestConvertJdLink:
    """测试链接转换功能（不依赖网络的测试）。"""

    def test_mobile_url_to_pc(self):
        result = convert_jd_link(
            "https://item.m.jd.com/product/100198170140.html?utm_source=iosapp"
        )
        assert result["product_id"] == "100198170140"
        assert result["pc_url"] == "https://item.jd.com/100198170140.html"
        assert result["error"] is None

    def test_pc_url_with_params_stripped(self):
        result = convert_jd_link(
            "https://item.jd.com/100120810291.html?cu=true&utm_source=share"
        )
        assert result["product_id"] == "100120810291"
        assert result["pc_url"] == "https://item.jd.com/100120810291.html"
        assert result["error"] is None

    def test_pure_id_to_pc_url(self):
        result = convert_jd_link("100198170140")
        assert result["product_id"] == "100198170140"
        assert result["pc_url"] == "https://item.jd.com/100198170140.html"

    def test_invalid_url_returns_error(self):
        result = convert_jd_link("https://www.example.com/not-jd")
        assert result["pc_url"] is None
        assert result["error"] is not None

    def test_original_preserved(self):
        url = "https://item.m.jd.com/product/100198170140.html?utm_source=test"
        result = convert_jd_link(url)
        assert result["original"] == url
