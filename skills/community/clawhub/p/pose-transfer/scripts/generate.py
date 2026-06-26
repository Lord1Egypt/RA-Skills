#!/usr/bin/env python3
"""
Pose Transfer - Multi-pose generation for fashion models

Generate multiple pose variations of a model/product image using reference pose images.
Uses Nano Banana Pro Edit API (fal-ai/nano-banana-pro/edit).

Usage:
    # With detailed vision description (recommended)
    python3 generate.py \
        --original model.jpg \
        --poses pose1.jpg pose2.jpg \
        --desc "MODEL: Asian woman, black hair. CLOTHING: Red floral dress, short sleeves. ACCESSORIES: Gold necklace. VIEW: Full body." \
        --output ./output
    
    # Without description (basic mode)
    python3 generate.py \
        --original model.jpg \
        --poses pose1.jpg \
        --output ./output
"""

import os
import sys
import argparse
import json
import base64
import mimetypes
from pathlib import Path
from typing import List, Dict, Optional

# Check FAL_KEY
if not os.environ.get("FAL_KEY"):
    print("❌ Error: FAL_KEY environment variable not set")
    print("Run: export FAL_KEY='your-fal-api-key'")
    sys.exit(1)

try:
    import fal_client
except ImportError:
    print("❌ Error: fal-client not installed")
    print("Run: pip install fal-client")
    sys.exit(1)


def image_to_data_url(image_path: str) -> str:
    """Convert image file to data URL"""
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/jpeg"
    
    with open(image_path, "rb") as f:
        data = f.read()
    
    b64_data = base64.b64encode(data).decode()
    return f"data:{mime_type};base64,{b64_data}"


def download_image(url: str, output_path: str) -> bool:
    """Download image from URL to local path"""
    try:
        import urllib.request
        import ssl
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"❌ Download error: {e}")
        return False


def generate_single_pose(
    original_data_url: str,
    pose_data_url: str,
    pose_num: int,
    vision_desc: str = "",
    expression: str = "smiling",
    resolution: str = "2K",
    keep_background: bool = False
) -> Optional[Dict]:
    """Generate a single pose variation"""
    
    # Determine background instruction
    bg_instruction = "KEEP the ORIGINAL background from SOURCE image exactly" if keep_background else "Background: Pure white studio"
    bg_suffix = "+ original background" if keep_background else "+ white background"
    
    # Build prompt based on whether we have vision description
    if vision_desc:
        # Detailed mode with vision analysis
        prompt = f"""IMAGE TRANSFORMATION TASK

SOURCE IMAGE CONTENT (COPY THIS EXACTLY):
{vision_desc}

REFERENCE IMAGE (COPY ONLY POSE AND FRAMING):
- Body position, stance, limb placement
- Camera angle and perspective  
- Cropping/framing (what body parts are visible)

TRANSFORMATION RULES:
1. Use the EXACT clothing, accessories, and appearance from SOURCE
2. Use the EXACT pose and framing from REFERENCE
3. {bg_instruction}
4. Expression: {expression}

STRICT PROHIBITIONS:
- DO NOT alter the clothing design from SOURCE
- DO NOT change colors or patterns from SOURCE
- DO NOT add elements not present in SOURCE
- DO NOT remove elements present in SOURCE
- DO NOT show body parts that REFERENCE doesn't show
- DO NOT adopt clothing or accessories from REFERENCE

Generate: SOURCE content + REFERENCE pose/framing {bg_suffix}."""
    else:
        # Basic mode without vision description
        prompt = f"""POSE TRANSFER

Take the model and clothing from the first image and place into the pose shown in the second image.

RULES:
- Keep all clothing and accessories from first image unchanged
- Copy only the body pose and framing from second image
- {bg_instruction}
- Expression: {expression}
- Do not add or remove any items
- Match the cropping of the second image (if cropped, output cropped)

Generate the transformed image."""
    
    try:
        result = fal_client.subscribe(
            "fal-ai/nano-banana-pro/edit",
            arguments={
                "prompt": prompt,
                "image_urls": [original_data_url, pose_data_url],
                "resolution": resolution,
                "aspect_ratio": "3:4",
                "num_images": 1,
                "output_format": "jpeg"
            },
            with_logs=False
        )
        
        if result and "images" in result:
            return {
                "pose": pose_num,
                "url": result["images"][0]["url"],
                "success": True
            }
    except Exception as e:
        print(f"❌ Generation error: {e}")
    
    return None


def generate_poses(
    original_path: str,
    pose_paths: List[str],
    output_dir: str = "./output",
    vision_desc: str = "",
    expression: str = "smiling",
    resolution: str = "2K",
    keep_background: bool = False
) -> Dict:
    """
    Generate multiple pose variations
    
    Args:
        original_path: Path to original model/product image
        pose_paths: List of paths to pose reference images (1-4)
        output_dir: Directory to save generated images
        vision_desc: Detailed description of original image (optional but recommended)
        expression: Desired expression (default: "smiling")
        resolution: Image resolution (default: "2K")
    
    Returns:
        Dictionary with generation results
    """
    
    # Validate inputs
    if not os.path.exists(original_path):
        raise FileNotFoundError(f"Original image not found: {original_path}")
    
    for pose_path in pose_paths:
        if not os.path.exists(pose_path):
            raise FileNotFoundError(f"Pose image not found: {pose_path}")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("🚀 Pose Transfer - Multi-pose Generation")
    print("=" * 60)
    print(f"\nOriginal: {original_path}")
    print(f"Poses: {len(pose_paths)}")
    print(f"Output: {output_dir}")
    if keep_background:
        print("📷 Background: KEEP original")
    else:
        print("📷 Background: White studio")
    if vision_desc:
        print("\n📋 Using detailed vision description")
    
    # Convert original to data URL
    print("\n📤 Converting images...")
    original_data_url = image_to_data_url(original_path)
    print("✅ Original converted")
    
    results = {
        "original": original_path,
        "output_dir": str(output_path),
        "poses": []
    }
    
    # Generate each pose
    for i, pose_path in enumerate(pose_paths, 1):
        print(f"\n{'='*60}")
        print(f"Generating pose {i}/{len(pose_paths)}...")
        print(f"{'='*60}")
        
        # Convert pose to data URL
        print(f"📤 Converting {Path(pose_path).name}...")
        pose_data_url = image_to_data_url(pose_path)
        print("✅ Reference converted")
        
        print("🎨 Generating...")
        result = generate_single_pose(
            original_data_url,
            pose_data_url,
            i,
            vision_desc,
            expression,
            resolution,
            keep_background
        )
        
        if result:
            # Download
            filename = f"pose_{i}.jpg"
            output_file = output_path / filename
            
            print("📥 Downloading...")
            if download_image(result["url"], str(output_file)):
                results["poses"].append({
                    "pose": i,
                    "url": result["url"],
                    "file": str(output_file),
                    "reference": pose_path,
                    "success": True
                })
                print(f"✅ Saved: {output_file}")
            else:
                results["poses"].append({
                    "pose": i,
                    "url": result["url"],
                    "reference": pose_path,
                    "success": False,
                    "error": "Download failed"
                })
        else:
            results["poses"].append({
                "pose": i,
                "reference": pose_path,
                "success": False,
                "error": "Generation failed"
            })
    
    # Save results JSON
    results_file = output_path / "generation_results.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved: {results_file}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Generation Summary")
    print("=" * 60)
    successful = sum(1 for p in results["poses"] if p.get("success"))
    print(f"Total: {len(pose_paths)} | Success: {successful} | Failed: {len(pose_paths) - successful}")
    
    for p in results["poses"]:
        status = "✅" if p.get("success") else "❌"
        print(f"{status} Pose {p['pose']}: {Path(p['reference']).name}")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Generate multiple pose variations for fashion models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # With detailed description (recommended for accuracy)
  python3 generate.py --original model.jpg --poses pose1.jpg pose2.jpg \\
      --desc "MODEL: Woman with long black hair. CLOTHING: Red dress with floral pattern, short sleeves, v-neck. ACCESSORIES: Gold earrings. VIEW: Full body."
  
  # Basic mode (without description)
  python3 generate.py --original model.jpg --poses pose1.jpg --output ./output
        """
    )
    parser.add_argument(
        "--original", "-o",
        required=True,
        help="Path to original model/product image"
    )
    parser.add_argument(
        "--poses", "-p",
        nargs="+",
        required=True,
        help="Paths to pose reference images (1-4)"
    )
    parser.add_argument(
        "--output", "-out",
        default="./output",
        help="Output directory (default: ./output)"
    )
    parser.add_argument(
        "--desc", "-d",
        default="",
        help="Detailed description of original image content (model, clothing, accessories, view). Recommended for best results."
    )
    parser.add_argument(
        "--expression", "-e",
        default="smiling",
        help="Desired expression (default: smiling)"
    )
    parser.add_argument(
        "--resolution", "-r",
        default="2K",
        choices=["1K", "2K", "4K"],
        help="Image resolution (default: 2K)"
    )
    parser.add_argument(
        "--keep-background", "-kb",
        action="store_true",
        help="Keep original background instead of replacing with white studio"
    )

    args = parser.parse_args()
    
    try:
        results = generate_poses(
            original_path=args.original,
            pose_paths=args.poses,
            output_dir=args.output,
            vision_desc=args.desc,
            expression=args.expression,
            resolution=args.resolution,
            keep_background=args.keep_background
        )
        
        # Return success if all generated
        successful = sum(1 for p in results["poses"] if p.get("success"))
        sys.exit(0 if successful == len(args.poses) else 1)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
