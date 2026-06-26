from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


# ========== Graph Input/Output ==========
class GraphInput(BaseModel):
    """Workflow input parameters"""
    token_name: str = Field(..., description="Token name, e.g., PEPE or Dogecoin")


class GraphOutput(BaseModel):
    """Workflow output results"""
    analysis_report: str = Field(..., description="Meme token analysis report")
    generated_image_url: Optional[str] = Field(default=None, description="Generated prediction image URL, None if image generation failed")


# ========== Global State ==========
class GlobalState(BaseModel):
    """Global state definition"""
    token_name: str = Field(default="", description="Token name")
    search_results: List[Dict[str, Any]] = Field(default=[], description="Search results list")
    search_summary: str = Field(default="", description="Search results summary")
    cleaned_text: str = Field(default="", description="Cleaned text")
    generated_image_url: str = Field(default="", description="Generated image URL, empty string if generation failed")
    analysis_report: str = Field(default="", description="Analysis report")


# ========== Node Input/Output Definitions ==========

# Search Node
class SearchNodeInput(BaseModel):
    """Search node input"""
    token_name: str = Field(..., description="Token name")


class SearchNodeOutput(BaseModel):
    """Search node output"""
    search_results: List[Dict[str, Any]] = Field(default=[], description="Search results list")
    search_summary: str = Field(default="", description="AI-generated search summary")


# Image Generation Node
class ImageGenNodeInput(BaseModel):
    """Image generation node input"""
    token_name: str = Field(..., description="Token name")


class ImageGenNodeOutput(BaseModel):
    """Image generation node output"""
    generated_image_url: str = Field(default="", description="Generated image URL, empty string if generation failed")


# Clean Data Node
class CleanDataNodeInput(BaseModel):
    """Data cleaning node input"""
    search_results: List[Dict[str, Any]] = Field(default=[], description="Search results list")
    search_summary: str = Field(default="", description="Search results summary")


class CleanDataNodeOutput(BaseModel):
    """Data cleaning node output"""
    cleaned_text: str = Field(..., description="Cleaned text summary")


# Analysis Node
class AnalysisNodeInput(BaseModel):
    """Analysis node input"""
    token_name: str = Field(..., description="Token name")
    cleaned_text: str = Field(..., description="Cleaned sentiment data")
    generated_image_url: str = Field(default="", description="Generated meme prediction image URL, empty if unavailable")


class AnalysisNodeOutput(BaseModel):
    """Analysis node output"""
    analysis_report: str = Field(..., description="Meme token analysis report")
