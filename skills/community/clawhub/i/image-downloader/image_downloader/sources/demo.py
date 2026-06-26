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
