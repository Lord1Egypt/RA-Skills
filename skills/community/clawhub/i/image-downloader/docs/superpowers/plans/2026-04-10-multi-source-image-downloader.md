# Multi-Source Image Downloader Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将当前 Bing 专用图片下载脚本重构为一个支持统一来源接口、标准去重、历史索引和基础多来源调度的关键词图片下载器。

**Architecture:** 保留单一 CLI 入口，但将实现拆分为统一数据模型、来源模块、下载存储和报告模块。第一阶段只落地 BingSource 与 DemoSource，通过标准去重和历史索引解决重复下载问题，并为后续接入更多真实来源保留清晰边界。

**Tech Stack:** Python 3、requests、argparse、pathlib、hashlib、json、unittest、unittest.mock、uv

**当前状态（2026-04-10）:** 当前根目录实现已经完成多来源 MVP：支持多来源候选收集、历史去重、续写编号与运行摘要。`demo` 来源当前主要用于统一接口与失败容错验证，不作为稳定真实来源承诺；后续重点转向文档、skill、评测与来源扩展，而不是继续补齐基础 MVP 能力。

---

## 文件结构映射

### 计划新增文件

- `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/__init__.py`
  - 包入口，标记新的模块化实现目录。
- `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/models.py`
  - 定义统一数据模型，例如 `ImageCandidate`、`DownloadRecord`、`RunStats`。
- `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/sources/__init__.py`
  - 来源模块包入口。
- `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/sources/base.py`
  - 定义统一来源接口，例如 `BaseSource`。
- `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/sources/bing.py`
  - 承载 Bing 抓取逻辑，从旧脚本迁移提取与分页采集能力。
- `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/sources/demo.py`
  - 提供无网络依赖的示例来源，便于测试统一接口与容错行为。
- `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/storage.py`
  - 承载文件保存、内容 hash、索引读写、元数据记录能力。
- `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/reporting.py`
  - 负责生成运行结果摘要与统计信息。
- `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_models_and_sources.py`
  - 覆盖统一模型与来源接口的基础测试。
- `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_storage.py`
  - 覆盖文件 hash、索引写入、历史去重和元数据保存。
- `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_integration_multisource.py`
  - 覆盖多来源整合流程的集成测试。

### 计划修改文件

- `D:/0/7/scrape/bing-keyword-image-downloader/scripts/bing_image_downloader.py`
  - 从单体脚本改为新的 CLI 入口，负责参数解析、来源调度、调用 pipeline / storage / reporting。
- `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_bing_image_downloader.py`
  - 调整为更轻量的 CLI / 兼容性测试，避免继续把全部逻辑塞在单文件测试中。
- `D:/0/7/scrape/bing-keyword-image-downloader/README.md`
  - 更新为多来源下载器说明。
- `D:/0/7/scrape/bing-keyword-image-downloader/SKILL.md`
  - 更新为多来源 skill 说明。
- `D:/0/7/scrape/bing-keyword-image-downloader/evals/evals.json`
  - 增加多来源与去重相关评测场景。

### 关键拆分原则

1. `sources/` 只负责发现候选，不负责最终保留决策。
2. 候选合并、URL 规范化、基础去重和目标截断已由当前 CLI 与现有模块吸收，不再要求单独落地 `pipeline.py`。
3. `storage.py` 只负责落盘、计算 hash、索引和元数据，不解析来源页面。
4. `reporting.py` 只负责统计和输出文本，不修改业务数据。
5. CLI 入口只负责调度，不在入口内堆叠具体策略。

---

### Task 1: 建立统一模型与来源接口

**Files:**
- Create: `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/__init__.py`
- Create: `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/models.py`
- Create: `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/sources/__init__.py`
- Create: `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/sources/base.py`
- Test: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_models_and_sources.py`

- [ ] **Step 1: 写失败测试，锁定统一候选模型和来源接口行为**

```python
import unittest
from image_downloader.models import ImageCandidate
from image_downloader.sources.base import BaseSource


class DummySource(BaseSource):
    name = "dummy"

    def collect(self, keyword, limit, pages):
        return [
            ImageCandidate(
                source="dummy",
                keyword=keyword,
                image_url="https://img.example.com/a.jpg",
                page_url="https://example.com/a",
                thumbnail_url=None,
                title="A",
                width=None,
                height=None,
                content_type=None,
                source_rank=1,
                metadata={},
            )
        ]


class TestModelsAndSources(unittest.TestCase):
    def test_image_candidate_keeps_required_fields(self):
        candidate = ImageCandidate(
            source="bing",
            keyword="cat",
            image_url="https://img.example.com/cat.jpg",
            page_url="https://example.com/cat",
            thumbnail_url="https://img.example.com/cat-thumb.jpg",
            title="cat image",
            width=800,
            height=600,
            content_type="image/jpeg",
            source_rank=3,
            metadata={"license": "unknown"},
        )

        self.assertEqual(candidate.source, "bing")
        self.assertEqual(candidate.keyword, "cat")
        self.assertEqual(candidate.image_url, "https://img.example.com/cat.jpg")
        self.assertEqual(candidate.width, 800)
        self.assertEqual(candidate.metadata["license"], "unknown")

    def test_base_source_collect_returns_candidates(self):
        source = DummySource()
        results = source.collect("dog", limit=5, pages=2)

        self.assertEqual(source.name, "dummy")
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], ImageCandidate)
        self.assertEqual(results[0].keyword, "dog")
```

- [ ] **Step 2: 运行测试，确认当前实现下失败**

Run:
```bash
uv run python -m unittest tests/test_models_and_sources.py -v
```

Expected:
- FAIL
- 报错包含 `ModuleNotFoundError: No module named 'image_downloader'` 或 `cannot import name 'ImageCandidate'`

- [ ] **Step 3: 写最小实现，建立模型与基础来源接口**

`D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/models.py`
```python
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ImageCandidate:
    source: str
    keyword: str
    image_url: str
    page_url: str | None
    thumbnail_url: str | None
    title: str | None
    width: int | None
    height: int | None
    content_type: str | None
    source_rank: int
    metadata: dict[str, Any] = field(default_factory=dict)
```

`D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/sources/base.py`
```python
class BaseSource:
    name = "base"

    def collect(self, keyword, limit, pages):
        raise NotImplementedError("Sources must implement collect()")
```

`D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/__init__.py`
```python
from .models import ImageCandidate
```

`D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/sources/__init__.py`
```python
from .base import BaseSource
```

- [ ] **Step 4: 再次运行测试，确认模型与来源接口通过**

Run:
```bash
uv run python -m unittest tests/test_models_and_sources.py -v
```

Expected:
- PASS
- 输出包含 `Ran 2 tests`

- [ ] **Step 5: 提交这一小步**

```bash
git -C "D:/0/7/scrape/bing-keyword-image-downloader" add image_downloader/__init__.py image_downloader/models.py image_downloader/sources/__init__.py image_downloader/sources/base.py tests/test_models_and_sources.py
git -C "D:/0/7/scrape/bing-keyword-image-downloader" commit -m "feat: 建立统一模型与来源接口"
```

### Task 2: 重构 BingSource 并迁移抓取逻辑

**Files:**
- Create: `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/sources/bing.py`
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/scripts/bing_image_downloader.py`
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_models_and_sources.py`
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_bing_image_downloader.py`
- Test: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_models_and_sources.py`
- Test: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_bing_image_downloader.py`

- [x] **Step 1: 先补一个失败测试，锁定 BingSource.collect 会返回统一 ImageCandidate 列表**

在 `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_models_and_sources.py` 中：
- 保留现有 `import unittest`、`from unittest import mock`
- 增加 `from image_downloader.sources.bing import BingSource`
- 在 `TestModelsAndSources` 类内追加如下测试方法：

```python
    def test_bing_source_collect_returns_image_candidates(self):
        response = mock.Mock()
        response.raise_for_status.return_value = None
        response.text = '''
        <a class="iusc" m='{"murl":"https://img.example.com/1.jpg","purl":"https://example.com/1","turl":"https://img.example.com/1-thumb.jpg","t":"cat 1","w":800,"h":600}'></a>
        <a class="iusc" m='{"murl":"https://img.example.com/2.png","purl":"https://example.com/2","turl":"https://img.example.com/2-thumb.png","t":"cat 2","w":640,"h":480}'></a>
        '''

        with mock.patch("image_downloader.sources.bing.requests.get", return_value=response):
            results = BingSource().collect("cat", limit=5, pages=1)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].source, "bing")
        self.assertEqual(results[0].keyword, "cat")
        self.assertEqual(results[0].image_url, "https://img.example.com/1.jpg")
        self.assertEqual(results[0].page_url, "https://example.com/1")
        self.assertEqual(results[0].thumbnail_url, "https://img.example.com/1-thumb.jpg")
        self.assertEqual(results[0].title, "cat 1")
        self.assertEqual(results[0].width, 800)
        self.assertEqual(results[0].height, 600)
        self.assertEqual(results[0].content_type, None)
        self.assertEqual(results[0].source_rank, 1)
        self.assertEqual(results[0].metadata["bing_page"], 1)
```

- [x] **Step 2: 再补一个失败测试，锁定脚本层 extract_image_urls 兼容入口继续返回纯 URL 列表**

在 `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_bing_image_downloader.py` 中的 `TestBingImageDownloader` 类内追加：

```python
    def test_extract_image_urls_uses_bing_source_compatible_parser(self):
        html = '''
        <a class="iusc" m='{"murl":"https://img.example.com/a.jpg"}'></a>
        <a class="iusc" m='{"murl":"https://img.example.com/b.png"}'></a>
        <a class="iusc" m='{"murl":"https://img.example.com/a.jpg"}'></a>
        '''

        urls = extract_image_urls(html)

        self.assertEqual(urls, [
            "https://img.example.com/a.jpg",
            "https://img.example.com/b.png",
        ])
```

- [x] **Step 3: 再补一个失败测试，锁定 collect_image_urls 会通过 BingSource 保持旧兼容行为**

在 `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_bing_image_downloader.py` 中：
- 在现有导入区新增 `from image_downloader.models import ImageCandidate`
- 在 `TestBingImageDownloader` 类内追加如下测试方法：

```python
    @mock.patch("bing_image_downloader.BingSource")
    def test_collect_image_urls_uses_bing_source_and_returns_plain_urls(self, mock_bing_source):
        mock_bing_source.return_value.collect.return_value = [
            ImageCandidate(
                source="bing",
                keyword="cat",
                image_url="https://img.example.com/1.jpg",
                page_url=None,
                thumbnail_url=None,
                title=None,
                width=None,
                height=None,
                content_type=None,
                source_rank=1,
                metadata={},
            ),
            ImageCandidate(
                source="bing",
                keyword="cat",
                image_url="https://img.example.com/2.jpg",
                page_url=None,
                thumbnail_url=None,
                title=None,
                width=None,
                height=None,
                content_type=None,
                source_rank=2,
                metadata={},
            ),
        ]

        urls = collect_image_urls("cat", pages=2, target_count=2)

        self.assertEqual(urls, [
            "https://img.example.com/1.jpg",
            "https://img.example.com/2.jpg",
        ])
        mock_bing_source.return_value.collect.assert_called_once_with("cat", limit=2, pages=2)
```

- [x] **Step 4: 运行测试，确认在 BingSource 尚未迁移前失败**

Run:
```bash
uv run python -m unittest tests/test_models_and_sources.py tests/test_bing_image_downloader.py -v
```

Expected:
- FAIL
- 失败原因应指向 `image_downloader.sources.bing` 尚未实现、`BingSource` 尚未可导入，或脚本层尚未接入 `BingSource`
- 不应是断言值错误；如果出现导入缺失，请先补齐本任务步骤里明确要求的 import 再重跑

- [x] **Step 5: 写最小实现，把 Bing 提取与分页采集逻辑迁移到来源模块**

新建 `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/sources/bing.py`：

```python
import html
import json
import re
from urllib.parse import quote

import requests

from image_downloader.models import ImageCandidate
from image_downloader.sources.base import BaseSource


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def _extract_image_metadata(html_text):
    patterns = [
        r"m='(\{.*?\})'",
        r'm="(\{.*?\})"',
    ]

    seen = set()
    items = []

    for pattern in patterns:
        matches = re.findall(pattern, html_text)
        for raw in matches:
            try:
                data = json.loads(html.unescape(raw))
            except json.JSONDecodeError:
                continue

            image_url = data.get("murl")
            if image_url and image_url not in seen:
                seen.add(image_url)
                items.append(data)

    return items


def extract_image_urls(html_text):
    return [item["murl"] for item in _extract_image_metadata(html_text) if item.get("murl")]


class BingSource(BaseSource):
    name = "bing"

    def collect(self, keyword, limit, pages):
        candidates = []
        seen = set()

        for page in range(max(1, pages)):
            if limit is not None and len(candidates) >= limit:
                break

            first = page * 35 + 1
            url = f"https://www.bing.com/images/search?q={quote(keyword)}&form=HDRSC3&first={first}"
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()

            for data in _extract_image_metadata(response.text):
                image_url = data.get("murl")
                if not image_url or image_url in seen:
                    continue

                seen.add(image_url)
                candidates.append(
                    ImageCandidate(
                        source="bing",
                        keyword=keyword,
                        image_url=image_url,
                        page_url=data.get("purl"),
                        thumbnail_url=data.get("turl"),
                        title=data.get("t"),
                        width=data.get("w"),
                        height=data.get("h"),
                        content_type=None,
                        source_rank=len(candidates) + 1,
                        metadata={"bing_page": page + 1},
                    )
                )

                if limit is not None and len(candidates) >= limit:
                    break

        return candidates
```

- [x] **Step 6: 在 CLI 脚本中接入 BingSource，同时保留旧接口兼容**

将 `D:/0/7/scrape/bing-keyword-image-downloader/scripts/bing_image_downloader.py` 中的 Bing 解析与采集入口改写为如下关键结构：

```python
import argparse
import mimetypes
import os
from pathlib import Path
from urllib.parse import urlparse

import requests

from image_downloader.sources.bing import BingSource, HEADERS, extract_image_urls


def guess_extension(url, content_type=None):
    if content_type:
        extension = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if extension == ".jpe":
            return ".jpg"
        if extension:
            return extension

    path = urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"):
        if path.endswith(ext):
            return ".jpg" if ext == ".jpeg" else ext
    return ".jpg"


def download_images(urls, output_dir, limit=10, start_index=1):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    saved_files = []

    for offset, url in enumerate(urls[:limit]):
        response = requests.get(url, headers=HEADERS, stream=True, timeout=15)
        response.raise_for_status()
        extension = guess_extension(url, response.headers.get("Content-Type"))
        filename = f"{start_index + offset:03d}{extension}"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "wb") as file_obj:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file_obj.write(chunk)

        saved_files.append(file_path)

    return saved_files


def collect_image_urls(keyword, pages=1, target_count=None):
    source = BingSource()
    limit = target_count if target_count is not None else pages * 35
    candidates = source.collect(keyword, limit=limit, pages=pages)
    return [candidate.image_url for candidate in candidates]
```

保持这一任务的边界：
- 删除脚本内原有的 Bing HTML 解析实现，统一改为从 `image_downloader.sources.bing` 导入 `extract_image_urls`
- `extract_image_urls()` 继续可从脚本导入
- `collect_image_urls()` 继续只走 Bing
- 保持 `guess_extension()`、`download_images()`、`search_bing_images()`、`main()` 的既有职责
- 不在这一任务中加入多来源调度、去重、历史索引或报告逻辑
- 不在这一任务中修改 CLI 参数定义

- [x] **Step 7: 运行测试，确认 BingSource 迁移后通过且旧兼容测试仍通过**

Run:
```bash
uv run python -m unittest tests/test_models_and_sources.py tests/test_bing_image_downloader.py -v
```

Expected:
- PASS
- `test_bing_source_collect_returns_image_candidates` 通过
- `test_extract_image_urls_uses_bing_source_compatible_parser` 通过
- `test_collect_image_urls_uses_bing_source_and_returns_plain_urls` 通过
- 旧的 Bing 相关兼容性测试继续通过

- [x] **Step 8: 提交这一小步（使用中文 Conventional Commit + 详细正文）**

```bash
git -C "D:/0/7/scrape/bing-keyword-image-downloader" add image_downloader/sources/bing.py scripts/bing_image_downloader.py tests/test_models_and_sources.py tests/test_bing_image_downloader.py
git -C "D:/0/7/scrape/bing-keyword-image-downloader" commit -m "$(cat <<'EOF'
feat: 抽离 BingSource 抓取逻辑

将原本散落在单体脚本中的 Bing 图片解析与分页抓取逻辑迁移到独立来源模块，
建立可复用的 BingSource，实现统一的 ImageCandidate 输出。

同时保留脚本层 extract_image_urls() 与 collect_image_urls() 的兼容入口，
确保现有 Bing 相关测试与既有下载流程在不引入多来源调度的前提下继续工作。

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

### Task 3: 加入 DemoSource 与基础多来源调度

**Files:**
- Create: `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/sources/demo.py`
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/scripts/bing_image_downloader.py`
- Test: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_models_and_sources.py`
- Test: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_integration_multisource.py`

- [x] **Step 1: 先写 DemoSource 的失败测试，锁定示例来源输出与 limit 截断行为**

在 `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_models_and_sources.py` 追加：

```python
from image_downloader.sources.demo import DemoSource

    def test_demo_source_collect_respects_limit(self):
        source = DemoSource()
        results = source.collect("cat", limit=2, pages=3)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].source, "demo")
        self.assertEqual(results[0].keyword, "cat")
        self.assertEqual(results[0].image_url, "https://demo.example.com/cat/1.jpg")
        self.assertEqual(results[1].source_rank, 2)
```

- [x] **Step 2: 再写一个集成失败测试，锁定多来源合并入口先按来源顺序串联结果**

新建 `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_integration_multisource.py`：

```python
import unittest
from unittest import mock

from image_downloader.models import ImageCandidate
from bing_image_downloader import collect_candidates_from_sources


class TestMultiSourceIntegration(unittest.TestCase):
    def test_collect_candidates_from_sources_merges_results_in_source_order(self):
        bing_source = mock.Mock()
        bing_source.name = "bing"
        bing_source.collect.return_value = [
            ImageCandidate(
                source="bing",
                keyword="cat",
                image_url="https://img.example.com/bing-1.jpg",
                page_url=None,
                thumbnail_url=None,
                title=None,
                width=None,
                height=None,
                content_type=None,
                source_rank=1,
                metadata={},
            )
        ]

        demo_source = mock.Mock()
        demo_source.name = "demo"
        demo_source.collect.return_value = [
            ImageCandidate(
                source="demo",
                keyword="cat",
                image_url="https://demo.example.com/cat/1.jpg",
                page_url=None,
                thumbnail_url=None,
                title="demo cat 1",
                width=640,
                height=480,
                content_type="image/jpeg",
                source_rank=1,
                metadata={"demo": True},
            )
        ]

        results = collect_candidates_from_sources(
            keyword="cat",
            limit=5,
            pages=2,
            sources=[bing_source, demo_source],
        )

        self.assertEqual([item.source for item in results], ["bing", "demo"])
        self.assertEqual(results[0].image_url, "https://img.example.com/bing-1.jpg")
        self.assertEqual(results[1].image_url, "https://demo.example.com/cat/1.jpg")
        bing_source.collect.assert_called_once_with("cat", limit=5, pages=2)
        demo_source.collect.assert_called_once_with("cat", limit=5, pages=2)


if __name__ == "__main__":
    unittest.main()
```

- [x] **Step 3: 运行测试，确认 DemoSource 和多来源调度入口尚未实现时失败**

Run:
```bash
uv run python -m unittest tests/test_models_and_sources.py tests/test_integration_multisource.py -v
```

Expected:
- FAIL
- 报错包含 `ModuleNotFoundError: No module named 'image_downloader.sources.demo'` 或 `cannot import name 'collect_candidates_from_sources'`

- [x] **Step 4: 写最小 DemoSource 实现，提供稳定的无网络候选输出**

新建 `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/sources/demo.py`：

```python
from image_downloader.models import ImageCandidate
from image_downloader.sources.base import BaseSource


class DemoSource(BaseSource):
    name = "demo"

    def collect(self, keyword, limit, pages):
        candidates = []
        max_items = min(limit, max(1, pages) * 3)

        for index in range(1, max_items + 1):
            candidates.append(
                ImageCandidate(
                    source="demo",
                    keyword=keyword,
                    image_url=f"https://demo.example.com/{keyword}/{index}.jpg",
                    page_url=f"https://demo.example.com/{keyword}/{index}",
                    thumbnail_url=f"https://demo.example.com/{keyword}/{index}-thumb.jpg",
                    title=f"demo {keyword} {index}",
                    width=640,
                    height=480,
                    content_type="image/jpeg",
                    source_rank=index,
                    metadata={"demo": True, "page": (index - 1) // 3 + 1},
                )
            )

        return candidates
```

- [x] **Step 5: 在 CLI 脚本中加入来源注册表与多来源候选收集入口**

在 `D:/0/7/scrape/bing-keyword-image-downloader/scripts/bing_image_downloader.py` 中追加或改写为如下关键结构：

```python
from image_downloader.sources.bing import BingSource, extract_image_urls
from image_downloader.sources.demo import DemoSource


SOURCE_REGISTRY = {
    "bing": BingSource,
    "demo": DemoSource,
}


def build_sources(source_names):
    return [SOURCE_REGISTRY[name]() for name in source_names]


def collect_candidates_from_sources(keyword, limit, pages, sources):
    candidates = []
    for source in sources:
        candidates.extend(source.collect(keyword, limit=limit, pages=pages))
    return candidates


def collect_image_urls(keyword, pages=1, target_count=None):
    source = BingSource()
    limit = target_count if target_count is not None else pages * 35
    candidates = source.collect(keyword, limit=limit, pages=pages)
    return [candidate.image_url for candidate in candidates]
```

保持当前旧接口兼容：
- `extract_image_urls()` 继续可从脚本导入
- `collect_image_urls()` 继续只走 Bing，避免一次性破坏旧测试
- 新增的 `collect_candidates_from_sources()` 只负责收集并串联候选，不在这一任务中做去重

- [x] **Step 6: 运行测试，确认 DemoSource 与多来源调度入口通过**

Run:
```bash
uv run python -m unittest tests/test_models_and_sources.py tests/test_integration_multisource.py tests/test_bing_image_downloader.py -v
```

Expected:
- PASS
- `test_demo_source_collect_respects_limit` 通过
- `test_collect_candidates_from_sources_merges_results_in_source_order` 通过
- 旧的 Bing 兼容性测试继续通过

- [ ] **Step 7: 提交这一小步**

```bash
git -C "D:/0/7/scrape/bing-keyword-image-downloader" add image_downloader/sources/demo.py scripts/bing_image_downloader.py tests/test_models_and_sources.py tests/test_integration_multisource.py tests/test_bing_image_downloader.py
git -C "D:/0/7/scrape/bing-keyword-image-downloader" commit -m "feat: 增加 DemoSource 与多来源调度入口"
```

### Task 5: 实现下载存储、历史索引与元数据

**Files:**
- Create: `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/storage.py`
- Create: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_storage.py`
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/scripts/bing_image_downloader.py`
- Test: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_integration_multisource.py`

- [ ] **Step 1: 先写 storage 的失败测试，锁定 URL 规范化索引、文件 hash 与元数据保存行为**

新建 `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_storage.py`：

```python
import json
import tempfile
import unittest
from pathlib import Path

from image_downloader.models import ImageCandidate
from image_downloader.storage import (
    compute_file_hash,
    load_index,
    normalize_url_for_index,
    record_download,
)


class TestStorage(unittest.TestCase):
    def test_normalize_url_for_index_removes_query_and_fragment(self):
        normalized = normalize_url_for_index("https://img.example.com/cat.jpg?x=1#top")
        self.assertEqual(normalized, "https://img.example.com/cat.jpg")

    def test_compute_file_hash_returns_sha256(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "sample.jpg"
            file_path.write_bytes(b"abc123")

            digest = compute_file_hash(file_path)
            self.assertEqual(
                digest,
                "6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d23925b4c1b8b4d99b5d",
            )

    def test_record_download_updates_index_and_metadata_file(self):
        candidate = ImageCandidate(
            source="demo",
            keyword="cat",
            image_url="https://demo.example.com/cat/1.jpg?token=1",
            page_url="https://demo.example.com/cat/1",
            thumbnail_url=None,
            title="demo cat 1",
            width=640,
            height=480,
            content_type="image/jpeg",
            source_rank=1,
            metadata={"demo": True},
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            image_path = output_dir / "001.jpg"
            image_path.write_bytes(b"demo-image")

            record = record_download(candidate, image_path, output_dir)
            index = load_index(output_dir)
            metadata_path = output_dir / "metadata.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

            self.assertEqual(record["file_name"], "001.jpg")
            self.assertIn("https://demo.example.com/cat/1.jpg", index["by_normalized_url"])
            self.assertIn(record["sha256"], index["by_sha256"])
            self.assertEqual(metadata[0]["source"], "demo")
            self.assertEqual(metadata[0]["keyword"], "cat")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 再写一个集成失败测试，锁定历史索引会跳过已下载候选**

在 `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_integration_multisource.py` 追加：

```python
import tempfile
from pathlib import Path

from image_downloader.storage import record_download, should_skip_candidate

    def test_history_index_skips_previously_downloaded_candidate(self):
        candidate = ImageCandidate(
            source="demo",
            keyword="cat",
            image_url="https://demo.example.com/cat/1.jpg?cache=1",
            page_url="https://demo.example.com/cat/1",
            thumbnail_url=None,
            title="demo cat 1",
            width=640,
            height=480,
            content_type="image/jpeg",
            source_rank=1,
            metadata={},
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            saved_path = output_dir / "001.jpg"
            saved_path.write_bytes(b"demo-image")
            record_download(candidate, saved_path, output_dir)

            duplicate = ImageCandidate(
                source="bing",
                keyword="cat",
                image_url="https://demo.example.com/cat/1.jpg?cache=2",
                page_url=None,
                thumbnail_url=None,
                title=None,
                width=None,
                height=None,
                content_type=None,
                source_rank=2,
                metadata={},
            )

            self.assertTrue(should_skip_candidate(duplicate, output_dir))
```

- [x] **Step 3: 运行测试，确认 storage 尚未实现时失败**

Run:
```bash
uv run python -m unittest tests/test_storage.py tests/test_integration_multisource.py -v
```

Expected:
- FAIL
- 报错包含 `ModuleNotFoundError: No module named 'image_downloader.storage'`

- [x] **Step 4: 写最小 storage 实现，完成 hash、索引、历史去重与元数据写入**

新建 `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/storage.py`：

```python
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


INDEX_FILE = "download_index.json"
METADATA_FILE = "metadata.json"


def normalize_url_for_index(url):
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def compute_file_hash(file_path):
    digest = hashlib.sha256()
    with Path(file_path).open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(8192), b""):
            if chunk:
                digest.update(chunk)
    return digest.hexdigest()


def load_index(output_dir):
    output_path = Path(output_dir)
    index_path = output_path / INDEX_FILE
    if not index_path.exists():
        return {"by_normalized_url": {}, "by_sha256": {}}
    return json.loads(index_path.read_text(encoding="utf-8"))


def save_index(output_dir, index_data):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    index_path = output_path / INDEX_FILE
    index_path.write_text(json.dumps(index_data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_metadata(output_dir):
    metadata_path = Path(output_dir) / METADATA_FILE
    if not metadata_path.exists():
        return []
    return json.loads(metadata_path.read_text(encoding="utf-8"))


def save_metadata(output_dir, records):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    metadata_path = output_path / METADATA_FILE
    metadata_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")


def record_download(candidate, image_path, output_dir):
    output_path = Path(output_dir)
    sha256 = compute_file_hash(image_path)
    normalized_url = normalize_url_for_index(candidate.image_url)
    record = {
        "source": candidate.source,
        "keyword": candidate.keyword,
        "image_url": candidate.image_url,
        "normalized_url": normalized_url,
        "page_url": candidate.page_url,
        "file_name": Path(image_path).name,
        "file_path": str(Path(image_path)),
        "sha256": sha256,
        "source_rank": candidate.source_rank,
    }

    index_data = load_index(output_path)
    index_data["by_normalized_url"][normalized_url] = record["file_name"]
    index_data["by_sha256"][sha256] = record["file_name"]
    save_index(output_path, index_data)

    metadata = load_metadata(output_path)
    metadata.append(record)
    save_metadata(output_path, metadata)
    return record


def should_skip_candidate(candidate, output_dir):
    index_data = load_index(output_dir)
    normalized_url = normalize_url_for_index(candidate.image_url)
    return normalized_url in index_data["by_normalized_url"]
```

- [x] **Step 5: 在 CLI 脚本中补一个最小存储入口，供后续主流程复用**

把 `D:/0/7/scrape/bing-keyword-image-downloader/scripts/bing_image_downloader.py` 中的下载流程旁边补一个包装函数：

```python
from image_downloader.storage import record_download, should_skip_candidate


def download_candidate(candidate, output_dir, index):
    if should_skip_candidate(candidate, output_dir):
        return None

    saved_files = download_images([candidate.image_url], output_dir, limit=1, start_index=index)
    if not saved_files:
        return None

    record_download(candidate, saved_files[0], output_dir)
    return saved_files[0]
```

此时先不要全面重写 `main()`，只把这个包装入口准备好，供下一任务接入总流程。

- [x] **Step 6: 再次运行测试，确认 storage 与历史索引通过**

Run:
```bash
uv run python -m unittest tests/test_storage.py tests/test_integration_multisource.py tests/test_bing_image_downloader.py -v
```

Expected:
- PASS
- `test_record_download_updates_index_and_metadata_file` 通过
- `test_history_index_skips_previously_downloaded_candidate` 通过
- 旧下载测试继续通过

- [x] **Step 7: 提交这一小步**

```bash
git -C "D:/0/7/scrape/bing-keyword-image-downloader" add image_downloader/storage.py scripts/bing_image_downloader.py tests/test_storage.py tests/test_integration_multisource.py tests/test_bing_image_downloader.py
git -C "D:/0/7/scrape/bing-keyword-image-downloader" commit -m "feat: 增加下载存储与历史索引"
```

**进度补记（2026-04-10）**
- 已在 `scripts/bing_image_downloader.py` 中补充 `get_next_image_index()`，连续运行时会从现有最大编号后续写，避免再次从 `001` 开始覆盖旧文件。
- 已将主流程调整为遍历本轮全部唯一候选；当历史索引命中或单个候选下载失败时，会继续向后补位，直到下载满 `--limit` 或候选耗尽。
- 已补充对应回归测试：
  - `tests/test_bing_image_downloader.py` 中的 `test_cli_runs_from_repo_root`
  - `tests/test_bing_image_downloader.py` 中的 `test_get_next_image_index_returns_next_available_number`
  - `tests/test_bing_image_downloader.py` 中的 `test_download_new_images_skips_duplicates_and_continues_until_limit`
- 已完成多轮真实 CLI 验证，确认历史去重与续写编号在实际下载目录中生效：
  - `"西野七濑" --limit 20 --pages 5` 在已有首轮下载结果基础上未覆盖旧文件，仍能补充下载新的不重复图片。
  - `"西野七濑" --limit 50 --pages 9` 在已有约 50 张图片时，后续运行仍可继续跳过重复候选，并实际补进新的不重复图片。
  - 更大规模的 `wallpaper-verify-20260410` 验证显示：首次运行可成功下载 12 张，第二次运行会跳过 24 个已记录候选，且不会覆盖 `001` 到 `012` 既有文件。
- 当前已确认的现实边界：脚本主流程、历史去重和补位逻辑已工作正常，但最终能新增多少图片仍受 Bing 返回候选质量与第三方源站可访问性影响；`demo` 来源目前主要用于补足候选与验证失败容错，不提供稳定可下载内容。

### Task 6: 接入报告输出并更新文档与评测

**Files:**
- Create: `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/reporting.py`
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/scripts/bing_image_downloader.py`
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/README.md`
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/SKILL.md`
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/evals/evals.json`
- Test: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_integration_multisource.py`
- Test: `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_bing_image_downloader.py`

- [x] **Step 1: 先写失败测试，锁定报告文本必须包含来源贡献、去重数量和保存目录**

在 `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_integration_multisource.py` 追加：

```python
from image_downloader.reporting import build_run_report

    def test_build_run_report_includes_source_counts_and_output_dir(self):
        report = build_run_report(
            keyword="cat",
            requested_limit=5,
            collected_count=8,
            deduped_count=5,
            downloaded_count=3,
            skipped_count=2,
            output_dir="downloads/cat",
            source_counts={"bing": 4, "demo": 4},
        )

        self.assertIn("关键词: cat", report)
        self.assertIn("候选总数: 8", report)
        self.assertIn("去重后数量: 5", report)
        self.assertIn("实际成功下载: 3", report)
        self.assertIn("跳过重复: 2", report)
        self.assertIn("- bing: 4", report)
        self.assertIn("- demo: 4", report)
        self.assertIn("保存目录: downloads/cat", report)
```

- [x] **Step 2: 再写一个 CLI 失败测试，锁定新主流程会调用多来源收集、去重和报告输出**

在 `D:/0/7/scrape/bing-keyword-image-downloader/tests/test_bing_image_downloader.py` 追加：

```python
    @mock.patch("bing_image_downloader.print")
    @mock.patch("bing_image_downloader.build_run_report")
    @mock.patch("bing_image_downloader.download_candidate")
    @mock.patch("bing_image_downloader.dedupe_candidates")
    @mock.patch("bing_image_downloader.collect_candidates_from_sources")
    @mock.patch("bing_image_downloader.build_sources")
    @mock.patch("bing_image_downloader.argparse.ArgumentParser.parse_args")
    def test_main_runs_multisource_pipeline_and_prints_report(
        self,
        mock_parse_args,
        mock_build_sources,
        mock_collect,
        mock_dedupe,
        mock_download_candidate,
        mock_build_report,
        mock_print,
    ):
        mock_parse_args.return_value = mock.Mock(
            keyword="cat",
            limit=2,
            pages=2,
            sources="bing,demo",
        )
        mock_build_sources.return_value = [mock.Mock(name="bing"), mock.Mock(name="demo")]
        candidate = mock.Mock(image_url="https://img.example.com/1.jpg")
        mock_collect.return_value = [candidate]
        mock_dedupe.return_value = [candidate]
        mock_download_candidate.return_value = "downloads/cat/001.jpg"
        mock_build_report.return_value = "mock report"

        from bing_image_downloader import main
        main()

        mock_build_sources.assert_called_once_with(["bing", "demo"])
        mock_collect.assert_called_once()
        mock_dedupe.assert_called_once_with([candidate], limit=2)
        mock_build_report.assert_called_once()
        mock_print.assert_any_call("mock report")
```

- [x] **Step 3: 运行测试，确认 reporting 和新 CLI 流程尚未实现时失败**

Run:
```bash
uv run python -m unittest tests/test_integration_multisource.py tests/test_bing_image_downloader.py -v
```

Expected:
- FAIL
- 报错包含 `ModuleNotFoundError: No module named 'image_downloader.reporting'` 或 `AttributeError: module 'bing_image_downloader' has no attribute 'build_run_report'`

- [x] **Step 4: 写最小 reporting 实现，输出可解释的结果摘要**

新建 `D:/0/7/scrape/bing-keyword-image-downloader/image_downloader/reporting.py`：

```python
def build_run_report(
    keyword,
    requested_limit,
    collected_count,
    deduped_count,
    downloaded_count,
    skipped_count,
    output_dir,
    source_counts,
):
    lines = [
        f"关键词: {keyword}",
        f"目标数量: {requested_limit}",
        f"候选总数: {collected_count}",
        f"去重后数量: {deduped_count}",
        f"实际成功下载: {downloaded_count}",
        f"跳过重复: {skipped_count}",
        "来源贡献:",
    ]

    for source_name, count in source_counts.items():
        lines.append(f"- {source_name}: {count}")

    lines.append(f"保存目录: {output_dir}")
    return "\n".join(lines)
```

- [x] **Step 5: 改写 CLI 主流程，让它接入多来源、去重、历史索引与报告输出**

把 `D:/0/7/scrape/bing-keyword-image-downloader/scripts/bing_image_downloader.py` 的 `main()` 收缩到如下结构：

```python
from image_downloader.pipeline import dedupe_candidates
from image_downloader.reporting import build_run_report


def main():
    parser = argparse.ArgumentParser(description="按关键词从多个来源下载图片")
    parser.add_argument("keyword", help="搜索关键词，例如 cat")
    parser.add_argument("--limit", type=int, default=10, help="下载数量，默认 10")
    parser.add_argument("--pages", type=int, default=5, help="每个来源最多抓取页数，默认 5")
    parser.add_argument("--sources", default="bing", help="逗号分隔的来源列表，例如 bing,demo")
    args = parser.parse_args()

    source_names = [item.strip() for item in args.sources.split(",") if item.strip()]
    sources = build_sources(source_names)
    output_dir = os.path.join("downloads", args.keyword)

    candidates = collect_candidates_from_sources(
        keyword=args.keyword,
        limit=args.limit * 3,
        pages=args.pages,
        sources=sources,
    )
    deduped = dedupe_candidates(candidates, limit=args.limit)

    success = 0
    for candidate in deduped:
        saved = download_candidate(candidate, output_dir, index=success + 1)
        if saved:
            success += 1

    source_counts = {}
    for candidate in candidates:
        source_counts[candidate.source] = source_counts.get(candidate.source, 0) + 1

    report = build_run_report(
        keyword=args.keyword,
        requested_limit=args.limit,
        collected_count=len(candidates),
        deduped_count=len(deduped),
        downloaded_count=success,
        skipped_count=max(0, len(deduped) - success),
        output_dir=output_dir,
        source_counts=source_counts,
    )
    print(report)
```

同时保留旧的兼容函数：
- `extract_image_urls()`
- `collect_image_urls()`
- `guess_extension()`
- `download_images()`

这样旧测试和新流程可以同时存在。

- [ ] **Step 6: 更新 README，让说明从 Bing 专用升级为多来源下载器**

把 `D:/0/7/scrape/bing-keyword-image-downloader/README.md` 关键段落改成如下内容：

```markdown
# bing-keyword-image-downloader

一个基于 Python 的多来源关键词图片下载项目，当前第一阶段支持 `bing` 与 `demo` 两类来源，同时保留了旧的 Bing 兼容接口，并整理成了一个可供其他 agent 复用的 Claude skill。

它的核心能力是：
- 按关键词从一个或多个来源收集图片候选
- 通过统一数据模型组织来源输出
- 在下载前执行原始 URL 与规范化 URL 去重
- 保存下载索引与元数据，减少跨次运行重复下载
- 输出包含来源贡献和去重结果的任务摘要
```

把参数说明补成：

```markdown
- `keyword`：搜索关键词，例如 `cat`、`dog`、`landscape`
- `--limit`：目标下载数量
- `--pages`：每个来源抓取的页数
- `--sources`：来源列表，例如 `bing` 或 `bing,demo`
```

把测试命令补成：

```bash
uv run --with requests python -m unittest tests.test_bing_image_downloader tests.test_models_and_sources tests.test_storage tests.test_integration_multisource -v
```

- [ ] **Step 7: 更新 SKILL.md，让 skill 说明与多来源能力一致**

把 `D:/0/7/scrape/bing-keyword-image-downloader/SKILL.md` 的头部与适用场景改成如下内容：

```markdown
---
name: bing-keyword-image-downloader
description: 当用户需要按关键词从一个或多个公开图片来源批量下载图片时使用。遇到类似“帮我按关键词下载 10 张图片”“批量抓取图片并避免重复”“从 Bing 和 demo 来源一起收集图片”这类请求时，应主动使用这个 skill。它专门处理基于关键词的多来源候选收集、标准去重、历史索引和本地保存工作流。
---

# 多来源关键词图片批量下载

这个 skill 用于复用当前目录中的 `scripts/bing_image_downloader.py` 脚本，让其他 agent 能稳定完成“按关键词从一个或多个来源收集图片并下载到本地”的任务。
```

把“何时使用”改成：

```markdown
- 按关键词从一个或多个来源下载若干图片
- 想减少重复图片并保留历史索引
- 想指定 `bing` 或 `bing,demo` 这类来源组合
- 想复用现成脚本完成多来源图片批量下载任务
```

把推荐命令模板补成：

```bash
uv run --with requests python "scripts/bing_image_downloader.py" "cat" --limit 10 --pages 3 --sources bing
uv run --with requests python "scripts/bing_image_downloader.py" "cat" --limit 10 --pages 2 --sources bing,demo
```

- [ ] **Step 8: 更新 evals，增加多来源与去重场景**

把 `D:/0/7/scrape/bing-keyword-image-downloader/evals/evals.json` 改成如下内容：

```json
{
  "skill_name": "bing-keyword-image-downloader",
  "evals": [
    {
      "id": 1,
      "prompt": "帮我从 Bing 按关键词下载 10 张猫咪图片到本地，我用 uv 管理 Python。",
      "expected_output": "调用当前目录中的 bing_image_downloader.py，设置合适的 pages 参数，使用 bing 来源，下载图片到 downloads/cat/ 或等价目录，并汇报成功数量。",
      "files": []
    },
    {
      "id": 2,
      "prompt": "我想批量抓取关于风景的 10 张图片，同时减少重复，来源用 Bing 和 demo。",
      "expected_output": "识别这是多来源图片下载任务，使用 --sources bing,demo，执行标准去重，并汇报候选数量、去重后数量和实际成功下载数量。",
      "files": []
    },
    {
      "id": 3,
      "prompt": "请按关键词下载 5 张 dog 图片，如果之前下载过重复 URL 就跳过，并告诉我保存目录。",
      "expected_output": "执行下载任务，启用历史索引去重，结束后说明保存目录、成功数量以及跳过重复的情况。",
      "files": []
    }
  ]
}
```

- [ ] **Step 9: 运行测试，确认报告与主流程通过，并检查文档示例一致**

Run:
```bash
uv run python -m unittest tests/test_bing_image_downloader.py tests/test_integration_multisource.py -v
```

Expected:
- PASS
- `test_main_runs_multisource_pipeline_and_prints_report` 通过
- `test_build_run_report_includes_source_counts_and_output_dir` 通过
- README、SKILL、evals 中的命令与参数名均为 `--sources`

- [ ] **Step 10: 提交这一小步**

```bash
git -C "D:/0/7/scrape/bing-keyword-image-downloader" add image_downloader/reporting.py scripts/bing_image_downloader.py README.md SKILL.md evals/evals.json tests/test_integration_multisource.py tests/test_bing_image_downloader.py
git -C "D:/0/7/scrape/bing-keyword-image-downloader" commit -m "feat: 接入多来源报告并更新说明文档"
```

### Task 7: 自检计划完整性并准备执行交接

**Files:**
- Modify: `D:/0/7/scrape/bing-keyword-image-downloader/docs/superpowers/plans/2026-04-10-multi-source-image-downloader.md`

- [ ] **Step 1: 对照 spec 检查覆盖范围，确认每项一阶段需求都有任务落点**

手动检查以下设计点是否都在本计划中出现：
- 统一 source 接口 → Task 1
- BingSource 重构 → Task 2
- DemoSource / 本地测试来源 → Task 3
- 多来源调度能力 → Task 3、Task 6
- 标准去重能力 → Task 4、Task 5
- 历史索引 → Task 5
- 元数据保存 → Task 5
- 任务报告 → Task 6
- README / SKILL / evals 更新 → Task 6

Expected:
- 无缺项
- 如发现缺项，直接把缺失任务补写到本文件中

- [ ] **Step 2: 扫描计划文本，删除占位表达与未定义引用**

手动搜索并确认本文件中没有以下内容：
- `TODO`
- `TBD`
- “类似 Task N”
- “写测试”但没有代码块
- 使用了未定义函数名或与前文不一致的类型名

Expected:
- 无占位符
- `ImageCandidate`、`BingSource`、`DemoSource`、`dedupe_candidates`、`record_download`、`build_run_report` 等命名保持一致

- [ ] **Step 3: 检查类型与主流程名称一致性，必要时直接在计划中修正**

重点检查：
- `collect_candidates_from_sources(keyword, limit, pages, sources)` 在 Task 3 与 Task 6 中签名一致
- `download_candidate(candidate, output_dir, index)` 在 Task 5 与 Task 6 中调用一致
- `build_sources(source_names)`、`dedupe_candidates(candidates, limit)`、`build_run_report(...)` 的参数名在所有任务中一致
- README / SKILL / evals 中统一使用 `--sources`

Expected:
- 所有函数签名一致
- 所有文档命令一致

- [ ] **Step 4: 在计划末尾追加执行交接说明**

在本文件末尾追加：

```markdown
---

Plan complete and saved to `docs/superpowers/plans/2026-04-10-multi-source-image-downloader.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
```

- [ ] **Step 5: 提交计划文档最终版本**

```bash
git -C "D:/0/7/scrape/bing-keyword-image-downloader" add docs/superpowers/plans/2026-04-10-multi-source-image-downloader.md
git -C "D:/0/7/scrape/bing-keyword-image-downloader" commit -m "docs: 完成多来源图片下载器实现计划"
```
