"""Deterministic text extraction from one authenticated local PDF snapshot."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from io import BytesIO
from pathlib import Path
import re
import unicodedata
from typing import Any

from . import StructuredAdapterError, read_stable_local_file


class PdfAdapterError(StructuredAdapterError):
    """Base class for controlled PDF adapter failures."""


class PdfDependencyError(PdfAdapterError):
    """Raised when the declared PDF dependency is unavailable."""


class PdfParseError(PdfAdapterError):
    """Raised when a PDF snapshot cannot be parsed safely."""


_PAGE_METHODS = {"pdfplumber-text", "pypdf-text", "none"}
_PAGE_WARNINGS = {"image-only", "empty-page"}
_DOCUMENT_WARNINGS = {"image-only-pages-present", "empty-pages-present"}
_DOCUMENT_ID = re.compile(r"^sha256:[0-9a-f]{64}$")


def _warnings(value: object, *, allowed: set[str]) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise TypeError("warnings must be an ordered collection")
    try:
        result = tuple(value)  # type: ignore[arg-type]
    except TypeError:
        raise TypeError("warnings must be an ordered collection") from None
    if any(not isinstance(item, str) or item not in allowed for item in result):
        raise ValueError("warnings contain an unknown value")
    if len(result) != len(set(result)):
        raise ValueError("warnings must not repeat")
    return result


def _normalize_text(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("page text must be a string")
    lines = []
    for line in unicodedata.normalize("NFC", value).replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        normalized = " ".join(line.split())
        if normalized:
            lines.append(normalized)
    return "\n".join(lines)


@dataclass(frozen=True)
class PdfTextPage:
    page_number: int
    text: str
    extraction_method: str
    warnings: tuple[str, ...] = ()
    image_only: bool = False

    def __post_init__(self) -> None:
        if isinstance(self.page_number, bool) or not isinstance(self.page_number, int):
            raise TypeError("page_number must be an integer")
        if self.page_number < 1:
            raise ValueError("page_number must be positive")
        text = _normalize_text(self.text)
        if self.extraction_method not in _PAGE_METHODS:
            raise ValueError("unknown PDF extraction method")
        if not isinstance(self.image_only, bool):
            raise TypeError("image_only must be boolean")
        warnings = _warnings(self.warnings, allowed=_PAGE_WARNINGS)
        if text and (self.extraction_method not in _PAGE_METHODS - {"none"} or self.image_only):
            raise ValueError("text page extraction state is contradictory")
        if not text and self.extraction_method != "none":
            raise ValueError("empty text requires the none extraction method")
        expected_warnings = () if text else (("image-only",) if self.image_only else ("empty-page",))
        if warnings != expected_warnings:
            raise ValueError("page warnings must exactly match page state")
        object.__setattr__(self, "text", text)
        object.__setattr__(self, "warnings", warnings)

    def to_dict(self) -> dict[str, Any]:
        return {
            "page_number": self.page_number,
            "text": self.text,
            "extraction_method": self.extraction_method,
            "warnings": list(self.warnings),
            "image_only": self.image_only,
        }


@dataclass(frozen=True)
class PdfTextDocument:
    document_id: str
    page_count: int
    pages: tuple[PdfTextPage, ...]
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.document_id, str) or not _DOCUMENT_ID.fullmatch(self.document_id):
            raise ValueError("document_id must be a safe content identifier")
        if isinstance(self.page_count, bool) or not isinstance(self.page_count, int):
            raise TypeError("page_count must be an integer")
        if self.page_count < 1:
            raise ValueError("page_count must be positive")
        if isinstance(self.pages, (str, bytes, bytearray)):
            raise TypeError("pages must be an ordered collection")
        try:
            pages = tuple(self.pages)
        except TypeError:
            raise TypeError("pages must be an ordered collection") from None
        if not all(isinstance(page, PdfTextPage) for page in pages):
            raise TypeError("pages must contain PdfTextPage values")
        if len(pages) != self.page_count:
            raise ValueError("page_count contradicts pages")
        if tuple(page.page_number for page in pages) != tuple(range(1, self.page_count + 1)):
            raise ValueError("page numbers must be unique and contiguous")
        warnings = _warnings(self.warnings, allowed=_DOCUMENT_WARNINGS)
        expected_warnings: list[str] = []
        if any(page.image_only for page in pages):
            expected_warnings.append("image-only-pages-present")
        if any(not page.text and not page.image_only for page in pages):
            expected_warnings.append("empty-pages-present")
        if warnings != tuple(expected_warnings):
            raise ValueError("document warnings must exactly match page states")
        object.__setattr__(self, "pages", pages)
        object.__setattr__(self, "warnings", warnings)

    def to_dict(self) -> dict[str, Any]:
        return {
            "document_id": self.document_id,
            "page_count": self.page_count,
            "pages": [page.to_dict() for page in self.pages],
            "warnings": list(self.warnings),
        }


def _load_pdfplumber() -> Any:
    try:
        import pdfplumber
    except (ImportError, ModuleNotFoundError):
        raise PdfDependencyError("PDF extraction requires pdfplumber>=0.11,<1") from None
    version = getattr(pdfplumber, "__version__", "")
    match = re.match(r"^(\d+)\.(\d+)", version)
    if match is None or not (int(match.group(1)) == 0 and int(match.group(2)) >= 11):
        raise PdfDependencyError("PDF extraction requires pdfplumber>=0.11,<1") from None
    return pdfplumber


def _load_pypdf() -> Any:
    try:
        import pypdf
    except (ImportError, ModuleNotFoundError):
        raise PdfDependencyError(
            "PDF extraction requires pdfplumber>=0.11,<1 or pypdf>=4,<7"
        ) from None
    version = getattr(pypdf, "__version__", "")
    match = re.match(r"^(\d+)\.(\d+)", version)
    if match is None or not 4 <= int(match.group(1)) < 7:
        raise PdfDependencyError("PDF fallback requires pypdf>=4,<7") from None
    return pypdf


def extract_pdf_text(path: str | Path) -> PdfTextDocument:
    source = read_stable_local_file(path, suffixes=(".pdf",))
    try:
        parser = _load_pdfplumber()
        method = "pdfplumber-text"
    except PdfDependencyError:
        parser = _load_pypdf()
        method = "pypdf-text"
    pages: list[PdfTextPage] = []
    try:
        if method == "pdfplumber-text":
            with parser.open(BytesIO(source)) as document:
                for page_number, page in enumerate(document.pages, start=1):
                    text = _normalize_text(page.extract_text() or "")
                    pages.append(_page(page_number, text, method, bool(page.images or page.objects)))
        else:
            document = parser.PdfReader(BytesIO(source))
            if document.is_encrypted:
                raise PdfParseError("Encrypted PDF requires an authorized readable source")
            for page_number, page in enumerate(document.pages, start=1):
                text = _normalize_text(page.extract_text() or "")
                # Inspect drawing content without decoding images or requiring Pillow/OCR.
                content = page.get_contents()
                visual_content = content is not None and bool(content.get_data())
                pages.append(_page(page_number, text, method, visual_content))
        if not pages:
            raise PdfParseError("PDF must contain at least one page")
    except PdfParseError:
        raise
    except Exception:
        raise PdfParseError("PDF could not be parsed") from None
    warnings: list[str] = []
    if any(page.image_only for page in pages):
        warnings.append("image-only-pages-present")
    if any(not page.text and not page.image_only for page in pages):
        warnings.append("empty-pages-present")
    return PdfTextDocument(
        "sha256:" + hashlib.sha256(source).hexdigest(),
        len(pages),
        pages,
        warnings,
    )


def _page(number: int, text: str, method: str, visual_content: bool) -> PdfTextPage:
    if text:
        return PdfTextPage(number, text, method)
    warning = "image-only" if visual_content else "empty-page"
    return PdfTextPage(number, "", "none", (warning,), visual_content)


__all__ = [
    "PdfAdapterError",
    "PdfDependencyError",
    "PdfParseError",
    "PdfTextDocument",
    "PdfTextPage",
    "extract_pdf_text",
]
