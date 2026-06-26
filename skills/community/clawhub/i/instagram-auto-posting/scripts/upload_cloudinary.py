"""
Upload image to Cloudinary and return public URL.

Required env vars:
  CLOUDINARY_CLOUD_NAME    - Your Cloudinary cloud name (required)
  CLOUDINARY_UPLOAD_PRESET - Your upload preset (required — use signed/unsigned based on your account)
  CLOUDINARY_FOLDER       - Optional folder name (default: none)

Usage:
  python upload_cloudinary.py <image_path> [folder]

NOTE: Using public unsigned presets may expose uploaded images. Configure restricted or signed uploads for production use.
"""

import urllib.request, urllib.parse, base64, json, os, sys

def upload_to_cloudinary(image_path, folder=None):
    """
    Upload an image to Cloudinary.

    Args:
        image_path: local path to the image file
        folder:     Cloudinary folder name (default: from CLOUDINARY_FOLDER env var, or none)

    Returns:
        Secure URL on success, None on failure.
    """
    if not os.path.exists(image_path):
        print(f"[ERROR] File not found: {image_path}")
        return None

    # Required — no defaults to prevent accidental public uploads
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    upload_preset = os.environ.get("CLOUDINARY_UPLOAD_PRESET")

    if not cloud_name:
        print("[ERROR] CLOUDINARY_CLOUD_NAME environment variable is not set.")
        print("        Create a free Cloudinary account at https://cloudinary.com")
        print("        and set CLOUDINARY_CLOUD_NAME to your cloud name.")
        return None

    if not upload_preset:
        print("[ERROR] CLOUDINARY_UPLOAD_PRESET environment variable is not set.")
        print("        Create an upload preset in your Cloudinary dashboard.")
        print("        Use a signed preset for private uploads.")
        return None

    folder = folder or os.environ.get("CLOUDINARY_FOLDER", "")

    with open(image_path, "rb") as f:
        img_data = f.read()

    b64 = base64.b64encode(img_data).decode("ascii")

    url = f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload"
    data = urllib.parse.urlencode({
        "file": f"data:image/png;base64,{b64}",
        "folder": folder,
        "upload_preset": upload_preset,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read().decode())
            secure_url = result.get("secure_url")
            if secure_url:
                print(f"[OK] Uploaded: {secure_url}")
            else:
                print(f"[ERROR] No secure_url in response: {result}")
            return secure_url
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode())
        print(f"[ERROR] HTTP {e.code}: {body.get('error', {}).get('message', e.reason)}")
        return None
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_cloudinary.py <image_path> [folder]")
        print("")
        print("Required env vars:")
        print("  CLOUDINARY_CLOUD_NAME     - your cloud name")
        print("  CLOUDINARY_UPLOAD_PRESET  - your upload preset (signed recommended)")
        print("  CLOUDINARY_FOLDER         - optional folder name")
        sys.exit(1)

    path = sys.argv[1]
    folder = sys.argv[2] if len(sys.argv) > 2 else None
    url = upload_to_cloudinary(path, folder)
    if url:
        print(url)
    else:
        sys.exit(1)
