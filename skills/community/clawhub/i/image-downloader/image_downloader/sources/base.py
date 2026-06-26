from image_downloader.models import ImageCandidate


class BaseSource:
    name = "base"

    def collect(
        self,
        keyword: str,
        limit: int | None = None,
        pages: int = 1,
    ) -> list[ImageCandidate]:
        raise NotImplementedError("Sources must implement collect()")
