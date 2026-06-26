import unittest
from unittest import mock

from image_downloader.models import ImageCandidate
from image_downloader.sources.base import BaseSource
from image_downloader.sources.bing import BingSource
from image_downloader.sources.demo import DemoSource


class DummySource(BaseSource):
    def collect(self, keyword, limit=None):
        return [
            ImageCandidate(
                source="dummy",
                keyword=keyword,
                image_url="https://img.example.com/cat.jpg",
                page_url="https://example.com/cat",
                thumbnail_url="https://img.example.com/cat-thumb.jpg",
                title="cat",
                width=800,
                height=600,
                content_type="image/jpeg",
                source_rank=1,
                metadata={"origin": "dummy"},
            )
        ]


class TestModelsAndSources(unittest.TestCase):
    def test_image_candidate_preserves_plan_fields(self):
        candidate = ImageCandidate(
            source="bing",
            keyword="cat",
            image_url="https://img.example.com/cat.jpg",
            page_url="https://www.bing.com/images/search?q=cat",
            thumbnail_url="https://img.example.com/thumb.jpg",
            title="cat title",
            width=800,
            height=600,
            content_type="image/jpeg",
            source_rank=3,
            metadata={"id": "abc"},
        )

        self.assertEqual(candidate.source, "bing")
        self.assertEqual(candidate.keyword, "cat")
        self.assertEqual(candidate.image_url, "https://img.example.com/cat.jpg")
        self.assertEqual(candidate.page_url, "https://www.bing.com/images/search?q=cat")
        self.assertEqual(candidate.thumbnail_url, "https://img.example.com/thumb.jpg")
        self.assertEqual(candidate.title, "cat title")
        self.assertEqual(candidate.width, 800)
        self.assertEqual(candidate.height, 600)
        self.assertEqual(candidate.content_type, "image/jpeg")
        self.assertEqual(candidate.source_rank, 3)
        self.assertEqual(candidate.metadata, {"id": "abc"})

    def test_dummy_source_collect_returns_image_candidate(self):
        candidates = DummySource().collect("cat", limit=1)

        self.assertEqual(len(candidates), 1)
        self.assertIsInstance(candidates[0], ImageCandidate)
        self.assertEqual(candidates[0].keyword, "cat")
        self.assertEqual(candidates[0].source, "dummy")

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

    def test_extract_image_urls_still_returns_plain_url_list(self):
        from image_downloader.sources.bing import extract_image_urls

        html = '''
        <a class="iusc" m='{"murl":"https://img.example.com/a.jpg","purl":"https://example.com/a"}'></a>
        <a class="iusc" m='{"murl":"https://img.example.com/b.png","purl":"https://example.com/b"}'></a>
        <a class="iusc" m='{"murl":"https://img.example.com/a.jpg","purl":"https://example.com/a-dup"}'></a>
        '''

        self.assertEqual(
            extract_image_urls(html),
            [
                "https://img.example.com/a.jpg",
                "https://img.example.com/b.png",
            ],
        )

    def test_demo_source_collect_respects_limit(self):
        source = DemoSource()
        results = source.collect("cat", limit=2, pages=3)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].source, "demo")
        self.assertEqual(results[0].keyword, "cat")
        self.assertEqual(results[0].image_url, "https://demo.example.com/cat/1.jpg")
        self.assertEqual(results[1].source_rank, 2)


if __name__ == "__main__":
    unittest.main()
