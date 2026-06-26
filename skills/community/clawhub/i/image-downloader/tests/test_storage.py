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
                "6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090",
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
