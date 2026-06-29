"""
EXIF operations for image-works.
View, clean, and selectively remove EXIF metadata.
"""
import io
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def read_exif(image) -> Dict:
    """
    Read all EXIF data from an image.
    
    Args:
        image: PIL Image object.
        
    Returns:
        Dict with EXIF fields and their values.
    """
    exif_data = image.info.get("exif", b"")
    if not exif_data:
        return {"status": "no_exif_data", "fields": {}}
    
    try:
        from PIL import ExifTags
        
        exif = image.getexif()
        fields = {}
        
        for tag_id, value in exif.items():
            tag_name = ExifTags.TAGS.get(tag_id, f"Tag_{tag_id}")
            
            # Handle bytes values
            if isinstance(value, bytes):
                try:
                    value = value.decode("utf-8", errors="replace")
                except Exception:
                    value = f"[{len(value)} bytes]"
            
            # Handle tuples
            if isinstance(value, tuple):
                value = list(value)
            
            # Handle GPS info
            if tag_id == 34853:  # GPSInfo
                gps_fields = {}
                if hasattr(value, "items"):
                    for gps_tag_id, gps_value in value.items():
                        gps_name = ExifTags.GPSTAGS.get(gps_tag_id, f"GPS_{gps_tag_id}")
                        gps_fields[gps_name] = str(gps_value)
                    value = gps_fields
                else:
                    value = str(value)
            
            fields[tag_name] = str(value)
        
        return {"status": "ok", "fields": fields}
    
    except Exception as e:
        logger.warning("Error reading EXIF: %s", e)
        return {"status": "error", "error": str(e), "fields": {}}


def remove_exif(image) -> Dict:
    """
    Remove all EXIF metadata from an image.
    
    Args:
        image: PIL Image object.
        
    Returns:
        Dict with 'image' (cleaned PIL Image).
    """
    from PIL import Image
    
    # Create a new image without EXIF
    # Preserve the pixel data but strip metadata
    if image.mode == "RGBA":
        new_image = Image.new("RGBA", image.size)
    else:
        new_image = Image.new("RGB", image.size)
    
    new_image.putdata(list(image.getdata()))
    
    return {"image": new_image, "removed": True}


def remove_gps_only(image) -> Dict:
    """
    Remove only GPS-related EXIF tags, keeping other metadata.
    
    Args:
        image: PIL Image object.
        
    Returns:
        Dict with 'image'.
    """
    from PIL import Image
    
    exif_data = image.info.get("exif", b"")
    if not exif_data:
        return {"image": image, "message": "No EXIF to clean"}
    
    try:
        exif = image.getexif()
        
        # Remove GPSInfo tag (tag_id 34853)
        if 34853 in exif:
            del exif[34853]
        
        # Remove GeoLocation tags
        geo_tags = {0, 1, 2, 3, 4}  # GPSLatitudeRef, GPSLatitude, etc.
        # These are inside the GPSInfo IFD, handled above
        
        # Save back to a new buffer
        buf = io.BytesIO()
        save_format = image.format or "JPEG"
        
        save_kwargs = {"format": save_format, "exif": exif.tobytes()}
        if save_format in ("JPEG",):
            save_kwargs["quality"] = "keep"
        
        image.save(buf, **save_kwargs)
        buf.seek(0)
        
        cleaned = Image.open(buf)
        cleaned.load()
        
        return {"image": cleaned, "removed_gps": True}
    
    except Exception as e:
        logger.warning("Error removing GPS EXIF: %s", e)
        return {"image": image, "warning": str(e)}


def has_gps_data(image) -> bool:
    """Check if an image contains GPS location data."""
    exif = image.getexif()
    return 34853 in exif  # GPSInfo tag
