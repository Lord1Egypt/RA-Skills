"""
Core image processing pipeline for image-works.
Orchestrates the application of multiple operations in sequence.
"""
import os
import io
import logging
from typing import Dict, List, Optional, Callable

logger = logging.getLogger(__name__)


def process_single_image(filepath: str, operations: List[Dict],
                         output_dir: str, suffix: str = "",
                         overwrite: bool = False,
                         keep_structure: bool = True,
                         base_input_dir: str = "") -> Dict:
    """
    Process a single image through a pipeline of operations.
    
    Args:
        filepath: Path to the input image.
        operations: List of operation dicts.
        output_dir: Base output directory.
        suffix: Filename suffix (e.g., '_compressed').
        overwrite: Whether to overwrite existing files.
        keep_structure: Whether to preserve relative directory structure.
        base_input_dir: Base input directory for relative path preservation.
        
    Returns:
        Dict with processing result and metadata.
    """
    from PIL import Image
    
    try:
        # Open image
        image = Image.open(filepath)
        original_format = image.format or "JPEG"
        
        # Get original info
        orig_size = os.path.getsize(filepath)
        orig_dimensions = image.size
        
        # Track current format
        current_format = original_format
        
        # Apply operations in sequence
        for op in operations:
            op_type = op.get("type", "")
            
            if op_type == "compress":
                from operations.compress import compress_image
                quality = op.get("quality")
                target_size_kb = op.get("target_size_kb")
                lossless = op.get("lossless", False)
                result = compress_image(
                    image, quality=quality, target_size_kb=target_size_kb,
                    lossless=lossless, format=current_format
                )
                # Reload from bytes
                buf = io.BytesIO(result["bytes"])
                image = Image.open(buf)
                image.load()
            
            elif op_type == "resize":
                from operations.resize import resize_image
                result = resize_image(
                    image,
                    width=op.get("width"),
                    height=op.get("height"),
                    scale=op.get("scale"),
                    max_edge=op.get("max_edge"),
                    fit=op.get("fit", "inside"),
                )
                image = result["image"]
            
            elif op_type == "convert":
                from operations.convert import convert_image
                target_format = op.get("format", "jpeg")
                quality = op.get("quality")
                result = convert_image(
                    image, target_format, quality=quality,
                    original_format=current_format
                )
                buf = io.BytesIO(result["bytes"])
                image = Image.open(buf)
                image.load()
                current_format = result["format"].upper()
            
            elif op_type == "watermark":
                from operations.watermark import add_text_watermark, add_image_watermark
                if op.get("text"):
                    result = add_text_watermark(
                        image, text=op["text"],
                        position=op.get("position", "bottom-right"),
                        opacity=op.get("opacity", 0.5),
                        font_size=op.get("font_size", 48),
                        color=op.get("color", "#ffffff"),
                    )
                elif op.get("image_path"):
                    result = add_image_watermark(
                        image, watermark_path=op["image_path"],
                        position=op.get("position", "bottom-right"),
                        opacity=op.get("opacity", 0.5),
                    )
                else:
                    continue
                image = result["image"]
            
            elif op_type == "exif":
                from operations.exif import remove_exif, remove_gps_only
                action = op.get("action", "remove")
                if action == "remove":
                    result = remove_exif(image)
                    image = result["image"]
                elif action == "remove-gps-only":
                    result = remove_gps_only(image)
                    image = result["image"]
            
            elif op_type == "crop":
                from operations.crop import crop_region, crop_aspect_ratio
                if op.get("aspect_ratio"):
                    result = crop_aspect_ratio(
                        image, aspect_ratio=op["aspect_ratio"],
                        position=op.get("position", "center"),
                    )
                else:
                    result = crop_region(
                        image, x=op.get("x", 0), y=op.get("y", 0),
                        width=op.get("width", image.width),
                        height=op.get("height", image.height),
                    )
                image = result["image"]
        
        # Determine output path
        rel_path = ""
        if keep_structure and base_input_dir:
            rel_dir = os.path.dirname(os.path.relpath(filepath, base_input_dir))
            if rel_dir != ".":
                rel_path = rel_dir
        
        output_subdir = os.path.join(output_dir, rel_path)
        os.makedirs(output_subdir, exist_ok=True)
        
        # Determine output filename
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        out_ext = os.path.splitext(filepath)[1].lower()
        
        # Change extension if format was converted
        if current_format != original_format:
            from operations.convert import get_target_extension
            out_ext = get_target_extension(current_format.lower())
        
        new_filename = f"{base_name}{suffix}{out_ext}"
        out_path = os.path.join(output_subdir, new_filename)
        
        if os.path.exists(out_path) and not overwrite:
            # Generate unique name
            counter = 1
            while os.path.exists(out_path):
                new_filename = f"{base_name}{suffix}_{counter}{out_ext}"
                out_path = os.path.join(output_subdir, new_filename)
                counter += 1
        
        # Save final image
        save_kwargs = {"format": current_format}
        if current_format in ("JPEG",):
            save_kwargs["quality"] = 90
            save_kwargs["optimize"] = True
        elif current_format == "PNG":
            save_kwargs["optimize"] = True
        elif current_format == "WEBP":
            save_kwargs["quality"] = 90
        
        image.save(out_path, **save_kwargs)
        
        out_size = os.path.getsize(out_path)
        
        return {
            "input_path": filepath,
            "output_path": out_path,
            "input_size": orig_size,
            "output_size": out_size,
            "input_dimensions": f"{orig_dimensions[0]}×{orig_dimensions[1]}",
            "output_dimensions": f"{image.width}×{image.height}",
            "format": current_format.lower(),
            "status": "success",
            "compression_ratio": round(1 - (out_size / orig_size), 4) if orig_size > 0 else 0,
        }
    
    except Exception as e:
        logger.error("Failed to process %s: %s", filepath, e)
        return {
            "input_path": filepath,
            "status": "failed",
            "error": str(e),
        }


def process_batch(files: list, operations: List[Dict], output_dir: str,
                  suffix: str = "", overwrite: bool = False,
                  keep_structure: bool = True,
                  base_input_dir: str = "",
                  progress_callback: Optional[Callable] = None) -> list:
    """
    Process a batch of images.
    
    Args:
        files: List of file paths.
        operations: List of operation dicts.
        output_dir: Base output directory.
        suffix: Filename suffix.
        overwrite: Overwrite existing.
        keep_structure: Preserve directory structure.
        base_input_dir: Base input directory.
        progress_callback: Optional callback for progress updates.
        
    Returns:
        List of per-file result dicts.
    """
    results = []
    total = len(files)
    
    for i, filepath in enumerate(files):
        result = process_single_image(
            filepath, operations, output_dir, suffix=suffix,
            overwrite=overwrite, keep_structure=keep_structure,
            base_input_dir=base_input_dir or os.path.commonpath(files) if files else "",
        )
        results.append(result)
        
        if progress_callback:
            progress_callback(i + 1, total, filepath)
    
    return results
