#!/usr/bin/env python3
"""Image Manager - Save image with indexing, thumbnails, and categorization."""
import sys
import os
import json
import shutil
import hashlib
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', '/home/admin/.openclaw/workspace'))
MEDIA_DIR = WORKSPACE / 'media'
IMAGES_DIR = MEDIA_DIR / 'images'
THUMBS_DIR = MEDIA_DIR / 'thumbnails'
INDEX_FILE = MEDIA_DIR / 'index.json'

VALID_CATEGORIES = ['pets', 'people', 'food', 'scenery', 'receipts', 'other']


def load_index():
    """Load or create the image index."""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"images": [], "version": 1}


def save_index(index):
    """Save the image index."""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def generate_id(category, source_path):
    """Generate a unique image ID."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    short_hash = hashlib.md5(source_path.encode()).hexdigest()[:6]
    return f"{category}-{date_str}-{short_hash}"


def create_thumbnail(source_path, thumb_path, size=300):
    """Create a thumbnail image."""
    try:
        from PIL import Image
        img = Image.open(source_path)
        img.thumbnail((size, size), Image.Resampling.LANCZOS)
        thumb_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(thumb_path), 'JPEG', quality=85)
        return True
    except ImportError:
        # PIL not available, just copy as thumbnail
        thumb_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(source_path), str(thumb_path))
        return False
    except Exception as e:
        print(f"Warning: Thumbnail creation failed: {e}", file=sys.stderr)
        return False


def get_image_info(source_path):
    """Get image dimensions and file size."""
    info = {"size_bytes": os.path.getsize(source_path), "width": 0, "height": 0}
    try:
        from PIL import Image
        img = Image.open(source_path)
        info["width"], info["height"] = img.size
    except:
        pass
    return info


def save_image(source_path, category='other', tags=None, description='', source='manual'):
    """Save an image with indexing."""
    if not os.path.exists(source_path):
        print(f"Error: File not found: {source_path}", file=sys.stderr)
        return None

    if category not in VALID_CATEGORIES:
        print(f"Warning: Unknown category '{category}', using 'other'", file=sys.stderr)
        category = 'other'

    # Generate ID and paths
    img_id = generate_id(category, source_path)
    ext = Path(source_path).suffix or '.jpg'
    if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        ext = '.jpg'

    cat_dir = IMAGES_DIR / category
    thumb_cat_dir = THUMBS_DIR / category
    cat_dir.mkdir(parents=True, exist_ok=True)
    thumb_cat_dir.mkdir(parents=True, exist_ok=True)

    dest_path = cat_dir / f"{img_id}{ext}"
    thumb_path = thumb_cat_dir / f"{img_id}.jpg"

    # Copy original (no compression)
    shutil.copy2(str(source_path), str(dest_path))

    # Create thumbnail
    create_thumbnail(source_path, thumb_path)

    # Get image info
    info = get_image_info(source_path)

    # Parse tags
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',') if t.strip()]

    # Create index entry
    entry = {
        "id": img_id,
        "path": str(dest_path.relative_to(WORKSPACE)),
        "thumbnail": str(thumb_path.relative_to(WORKSPACE)),
        "category": category,
        "tags": tags or [],
        "description": description,
        "saved_at": datetime.now().isoformat(),
        "source": source,
        "size_bytes": info["size_bytes"],
        "width": info["width"],
        "height": info["height"]
    }

    # Update index
    index = load_index()
    index["images"].append(entry)
    save_index(index)

    # Output result
    print(json.dumps(entry, ensure_ascii=False))
    return entry


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Save image to indexed storage')
    parser.add_argument('image_path', help='Path to source image')
    parser.add_argument('--category', '-c', default='other', choices=VALID_CATEGORIES)
    parser.add_argument('--tags', '-t', default='', help='Comma-separated tags')
    parser.add_argument('--description', '-d', default='', help='Image description')
    parser.add_argument('--source', '-s', default='manual', help='Source (feishu/manual/clipboard)')
    args = parser.parse_args()

    save_image(args.image_path, args.category, args.tags, args.description, args.source)
