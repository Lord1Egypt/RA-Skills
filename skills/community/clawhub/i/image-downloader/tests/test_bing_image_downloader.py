import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from image_downloader.models import ImageCandidate

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from bing_image_downloader import (
    extract_image_urls,
    guess_extension,
    download_images,
    collect_image_urls,
    main,
    download_new_images,
    get_next_image_index,
)


class TestBingImageDownloader(unittest.TestCase):
    def test_extract_image_urls_from_bing_html(self):
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

    def test_extract_image_urls_from_html_entities(self):
        html = '''
        <a class="iusc" m="{&quot;murl&quot;:&quot;https://img.example.com/c.jpg&quot;,&quot;turl&quot;:&quot;x&quot;}"></a>
        <a class="iusc" m="{&quot;murl&quot;:&quot;https://img.example.com/d.png&quot;,&quot;turl&quot;:&quot;y&quot;}"></a>
        '''
        urls = extract_image_urls(html)
        self.assertEqual(urls, [
            "https://img.example.com/c.jpg",
            "https://img.example.com/d.png",
        ])

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

    @mock.patch("bing_image_downloader.requests.get")
    def test_collect_image_urls_across_multiple_pages(self, mock_get):
        search_page_1 = mock.Mock()
        search_page_1.raise_for_status.return_value = None
        search_page_1.text = '''
        <a class="iusc" m='{"murl":"https://img.example.com/1.jpg"}'></a>
        <a class="iusc" m='{"murl":"https://img.example.com/2.jpg"}'></a>
        '''

        search_page_2 = mock.Mock()
        search_page_2.raise_for_status.return_value = None
        search_page_2.text = '''
        <a class="iusc" m='{"murl":"https://img.example.com/2.jpg"}'></a>
        <a class="iusc" m='{"murl":"https://img.example.com/3.jpg"}'></a>
        '''

        mock_get.side_effect = [search_page_1, search_page_2]

        urls = collect_image_urls("cat", pages=2)

        self.assertEqual(urls, [
            "https://img.example.com/1.jpg",
            "https://img.example.com/2.jpg",
            "https://img.example.com/3.jpg",
        ])
        self.assertEqual(mock_get.call_count, 2)

    @mock.patch("bing_image_downloader.requests.get")
    def test_collect_image_urls_stops_when_target_pool_reached(self, mock_get):
        search_page_1 = mock.Mock()
        search_page_1.raise_for_status.return_value = None
        search_page_1.text = '''
        <a class="iusc" m='{"murl":"https://img.example.com/1.jpg"}'></a>
        <a class="iusc" m='{"murl":"https://img.example.com/2.jpg"}'></a>
        '''

        search_page_2 = mock.Mock()
        search_page_2.raise_for_status.return_value = None
        search_page_2.text = '''
        <a class="iusc" m='{"murl":"https://img.example.com/3.jpg"}'></a>
        <a class="iusc" m='{"murl":"https://img.example.com/4.jpg"}'></a>
        '''

        search_page_3 = mock.Mock()
        search_page_3.raise_for_status.return_value = None
        search_page_3.text = '''
        <a class="iusc" m='{"murl":"https://img.example.com/5.jpg"}'></a>
        '''

        mock_get.side_effect = [search_page_1, search_page_2, search_page_3]

        urls = collect_image_urls("cat", pages=3, target_count=3)

        self.assertEqual(urls, [
            "https://img.example.com/1.jpg",
            "https://img.example.com/2.jpg",
            "https://img.example.com/3.jpg",
        ])
        self.assertEqual(mock_get.call_count, 2)

    @mock.patch("bing_image_downloader.requests.get")
    def test_download_images_stops_after_requested_count(self, mock_get):
        image_response = mock.Mock()
        image_response.raise_for_status.return_value = None
        image_response.headers = {"Content-Type": "image/jpeg"}
        image_response.iter_content.return_value = [b"abc", b"def"]
        mock_get.return_value = image_response

        urls = [
            "https://img.example.com/1.jpg",
            "https://img.example.com/2.jpg",
            "https://img.example.com/3.jpg",
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            saved = download_images(urls, tmpdir, limit=2)
            self.assertEqual(len(saved), 2)
            self.assertTrue(os.path.exists(saved[0]))
            self.assertTrue(os.path.exists(saved[1]))
            self.assertTrue(saved[0].endswith("001.jpg"))
            self.assertTrue(saved[1].endswith("002.jpg"))

    @mock.patch("bing_image_downloader.requests.get")
    def test_download_images_respects_start_index(self, mock_get):
        image_response = mock.Mock()
        image_response.raise_for_status.return_value = None
        image_response.headers = {"Content-Type": "image/jpeg"}
        image_response.iter_content.return_value = [b"abc"]
        mock_get.return_value = image_response

        with tempfile.TemporaryDirectory() as tmpdir:
            saved = download_images([
                "https://img.example.com/3.jpg",
            ], tmpdir, limit=1, start_index=3)
            self.assertEqual(len(saved), 1)
            self.assertTrue(saved[0].endswith("003.jpg"))

    def test_get_next_image_index_returns_next_available_number(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            (output_dir / "001.jpg").write_bytes(b"a")
            (output_dir / "002.png").write_bytes(b"b")
            (output_dir / "010.webp").write_bytes(b"c")

            self.assertEqual(get_next_image_index(output_dir), 11)

    @mock.patch("bing_image_downloader.download_candidate")
    def test_download_new_images_skips_duplicates_and_continues_until_limit(self, mock_download_candidate):
        candidates = [
            ImageCandidate(source="bing", keyword="cat", image_url="https://img.example.com/1.jpg"),
            ImageCandidate(source="bing", keyword="cat", image_url="https://img.example.com/2.jpg"),
            ImageCandidate(source="demo", keyword="cat", image_url="https://img.example.com/3.jpg"),
        ]
        mock_download_candidate.side_effect = [None, "downloads/cat/011.jpg", "downloads/cat/012.jpg"]

        downloaded_count, skipped_count = download_new_images(
            candidates=candidates,
            output_dir=os.path.join("downloads", "cat"),
            limit=2,
            start_index=11,
        )

        self.assertEqual(downloaded_count, 2)
        self.assertEqual(skipped_count, 1)
        mock_download_candidate.assert_has_calls([
            mock.call(candidates[0], os.path.join("downloads", "cat"), 11),
            mock.call(candidates[1], os.path.join("downloads", "cat"), 11),
            mock.call(candidates[2], os.path.join("downloads", "cat"), 12),
        ])

    def test_cli_runs_from_repo_root(self):
        repo_root = Path(__file__).resolve().parents[1]
        command = [
            sys.executable,
            "scripts/bing_image_downloader.py",
            "cat",
            "--limit",
            "1",
            "--pages",
            "1",
        ]

        with mock.patch.dict(os.environ, {"PYTHONPATH": ""}, clear=False):
            result = subprocess.run(
                command,
                cwd=repo_root,
                capture_output=True,
                text=True,
            )

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}",
        )

    @mock.patch("bing_image_downloader.print")
    @mock.patch("bing_image_downloader.build_run_report")
    @mock.patch("bing_image_downloader.download_candidate")
    @mock.patch("bing_image_downloader.collect_candidates_from_sources")
    @mock.patch("bing_image_downloader.build_sources")
    @mock.patch("bing_image_downloader.argparse.ArgumentParser.parse_args")
    def test_main_runs_multisource_pipeline_and_prints_report(
        self,
        mock_parse_args,
        mock_build_sources,
        mock_collect_candidates,
        mock_download_candidate,
        mock_build_run_report,
        mock_print,
    ):
        mock_parse_args.return_value = mock.Mock(keyword="cat", limit=2, pages=3)
        sources = [mock.Mock(name="bing-source"), mock.Mock(name="demo-source")]
        mock_build_sources.return_value = sources

        collected = [
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
                source="demo",
                keyword="cat",
                image_url="https://demo.example.com/2.jpg",
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
                source="demo",
                keyword="cat",
                image_url="https://demo.example.com/3.jpg",
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
        mock_collect_candidates.return_value = collected
        mock_download_candidate.side_effect = ["downloads/cat/011.jpg", None, "downloads/cat/012.jpg"]
        mock_build_run_report.return_value = "运行完成摘要"

        with mock.patch("bing_image_downloader.get_next_image_index", return_value=11):
            main()

        mock_build_sources.assert_called_once_with(["bing", "demo"])
        mock_collect_candidates.assert_called_once_with(
            keyword="cat",
            limit=2,
            pages=3,
            sources=sources,
        )
        mock_download_candidate.assert_has_calls([
            mock.call(collected[0], os.path.join("downloads", "cat"), 11),
            mock.call(collected[1], os.path.join("downloads", "cat"), 12),
        ])
        mock_build_run_report.assert_called_once_with(
            keyword="cat",
            requested_limit=2,
            collected_count=3,
            deduped_count=3,
            downloaded_count=2,
            skipped_count=1,
            output_dir=os.path.join("downloads", "cat"),
            source_counts={"bing": 1, "demo": 2},
        )
        mock_print.assert_called_once_with("运行完成摘要")


if __name__ == "__main__":
    unittest.main()
