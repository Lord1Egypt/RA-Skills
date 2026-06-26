#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Processor Module
Handles image resizing and compression using Pillow instead of OpenCV.
"""

import os
import io
import logging
from typing import Tuple, Optional
from PIL import Image

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Handles image processing operations (resize, compress)"""
    
    @staticmethod
    def process_for_upload(
        image_path: str, 
        max_side: int = 1024, 
        quality: int = 80
    ) -> bytes:
        """
        Resize and compress image for upload.
        
        Args:
            image_path: Path to the source image
            max_side: Maximum dimension for width or height
            quality: JPEG compression quality (1-100)
            
        Returns:
            bytes: Processed image data in JPEG format
            
        Raises:
            FileNotFoundError: If image file does not exist
            IOError: If image cannot be opened or processed
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
            
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (e.g. for PNG with transparency)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Calculate new dimensions
                width, height = img.size
                scale = 1.0
                
                if width > height:
                    if width > max_side:
                        scale = max_side / width
                else:
                    if height > max_side:
                        scale = max_side / height
                
                if scale < 1.0:
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    logger.info(f"Resized image from {width}x{height} to {new_width}x{new_height}")
                
                # Compress to JPEG
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=quality)
                return output.getvalue()
                
        except Exception as e:
            logger.error(f"Failed to process image {image_path}: {e}")
            raise IOError(f"Image processing failed: {e}")

    @staticmethod
    def get_image_ratio(image_path: str) -> float:
        """
        Get image aspect ratio (width / height).
        
        Args:
            image_path: Path to the image file
            
        Returns:
            float: Aspect ratio
        """
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                return float(width) / float(height)
        except Exception as e:
            logger.error(f"Failed to get image ratio: {e}")
            return 1.0
