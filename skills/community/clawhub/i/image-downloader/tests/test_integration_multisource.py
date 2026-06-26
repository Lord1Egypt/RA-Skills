import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from image_downloader.models import ImageCandidate
from image_downloader.reporting import build_run_report
from image_downloader.storage import record_download, should_skip_candidate

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

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


if __name__ == "__main__":
    unittest.main()
