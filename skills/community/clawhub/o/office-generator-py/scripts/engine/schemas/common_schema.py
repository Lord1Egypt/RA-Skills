from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

DocumentType = Literal['docx', 'xlsx', 'pptx']
SlideLayout = Literal['title', 'content', 'table', 'image']


class OutputSpec(BaseModel):
    filename: Optional[str] = None
    directory: Optional[str] = None


class ImageSpec(BaseModel):
    path: str
    widthInches: Optional[float] = None


class Section(BaseModel):
    heading: Optional[str] = None
    paragraphs: List[str] = Field(default_factory=list)
    bullets: List[str] = Field(default_factory=list)
    table: List[List[Any]] = Field(default_factory=list)
    images: List[ImageSpec] = Field(default_factory=list)


class SheetSpec(BaseModel):
    name: str
    columns: List[str] = Field(default_factory=list)
    rows: List[List[Any]] = Field(default_factory=list)


class SlideImageSpec(BaseModel):
    path: str


class SlideSpec(BaseModel):
    title: Optional[str] = None
    layout: SlideLayout = 'content'
    bullets: List[str] = Field(default_factory=list)
    table: List[List[Any]] = Field(default_factory=list)
    image: Optional[SlideImageSpec] = None


class DocxContentSpec(BaseModel):
    sections: List[Section] = Field(default_factory=list)


class XlsxContentSpec(BaseModel):
    sheets: List[SheetSpec] = Field(default_factory=list)


class PptxContentSpec(BaseModel):
    slides: List[SlideSpec] = Field(default_factory=list)


class OfficeRequest(BaseModel):
    documentType: DocumentType
    templateId: Optional[str] = None
    title: Optional[str] = None
    audience: Optional[str] = None
    purpose: Optional[str] = None
    style: Dict[str, Any] = Field(default_factory=dict)
    sourceMaterials: List[str] = Field(default_factory=list)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    output: OutputSpec = Field(default_factory=OutputSpec)
    contentSpec: Dict[str, Any] = Field(default_factory=dict)


def validate_request(data: Dict[str, Any]) -> OfficeRequest:
    return OfficeRequest.model_validate(data)
