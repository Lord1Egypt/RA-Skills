#!/usr/bin/env python3
"""
Image Cropper
Crop images based on bounding box annotations
"""

import argparse
import json
import os
import sys
from pathlib import Path
from PIL import Image
from typing import Dict, List, Tuple


def parse_yolo_annotation(txt_path: str, img_width: int, img_height: int) -> List[Tuple]:
    """Parse YOLO format annotation"""
    annotations = []
    try:
        with open(txt_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                
                class_id = int(parts[0])
                x_center = float(parts[1]) * img_width
                y_center = float(parts[2]) * img_height
                width = float(parts[3]) * img_width
                height = float(parts[4]) * img_height
                
                # Convert to corner coordinates
                x1 = int(x_center - width / 2)
                y1 = int(y_center - height / 2)
                x2 = int(x_center + width / 2)
                y2 = int(y_center + height / 2)
                
                annotations.append((class_id, x1, y1, x2, y2))
    except:
        pass
    return annotations


def parse_coco_annotation(coco_data: Dict, img_id: int) -> List[Tuple]:
    """Parse COCO format annotation"""
    annotations = []
    
    for ann in coco_data.get('annotations', []):
        if ann.get('image_id') != img_id:
            continue
        
        class_id = ann.get('category_id', 1) - 1
        bbox = ann.get('bbox', [0, 0, 0, 0])
        
        x1 = int(bbox[0])
        y1 = int(bbox[1])
        x2 = int(bbox[0] + bbox[2])
        y2 = int(bbox[1] + bbox[3])
        
        annotations.append((class_id, x1, y1, x2, y2))
    
    return annotations


def parse_voc_annotation(xml_path: str) -> List[Tuple]:
    """Parse VOC XML annotation"""
    annotations = []
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        for obj in root.findall('object'):
            bbox = obj.find('bndbox')
            if bbox is not None:
                xmin = int(float(bbox.findtext('xmin', 0)))
                ymin = int(float(bbox.findtext('ymin', 0)))
                xmax = int(float(bbox.findtext('xmax', 0)))
                ymax = int(float(bbox.findtext('ymax', 0)))
                
                annotations.append((0, xmin, ymin, xmax, ymax))
    except:
        pass
    
    return annotations


def crop_image(image_path: str, bbox: Tuple, padding: int = 0, 
              img_width: int = 0, img_height: int = 0) -> Image.Image:
    """Crop image based on bounding box"""
    img = Image.open(image_path)
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    width, height = img.size
    
    class_id, x1, y1, x2, y2 = bbox
    
    # Apply padding
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(width, x2 + padding)
    y2 = min(height, y2 + padding)
    
    # Crop
    cropped = img.crop((x1, y1, x2, y2))
    
    return cropped


def cmd_yolo(args):
    """Crop YOLO format"""
    images_dir = Path(args.images)
    labels_dir = Path(args.labels)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all images
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(images_dir.glob(f"*{ext}"))
        image_files.extend(images_dir.glob(f"*{ext.upper()}"))
    
    print(f"Processing {len(image_files)} images...")
    
    total_cropped = 0
    object_idx = 0
    
    for img_path in image_files:
        base_name = img_path.stem
        label_path = labels_dir / f"{base_name}.txt"
        
        if not label_path.exists():
            continue
        
        # Get image size
        with Image.open(img_path) as img:
            width, height = img.size
        
        # Parse annotations
        annotations = parse_yolo_annotation(str(label_path), width, height)
        
        if not annotations:
            continue
        
        if args.objects:
            # Save each object as separate file
            for i, bbox in enumerate(annotations):
                class_id, x1, y1, x2, y2 = bbox
                
                # Check minimum size
                if args.min_size:
                    if (x2 - x1) < args.min_size or (y2 - y1) < args.min_size:
                        continue
                
                cropped = crop_image(str(img_path), bbox, args.padding, width, height)
                output_name = f"{base_name}_{i}.{args.format}"
                output_path = output_dir / output_name
                cropped.save(output_path, quality=args.quality)
                total_cropped += 1
                object_idx += 1
        else:
            # Save cropped images (one per input image)
            cropped = crop_image(str(img_path), annotations[0], args.padding, width, height)
            output_path = output_dir / f"{base_name}_crop.{args.format}"
            cropped.save(output_path, quality=args.quality)
            total_cropped += 1
    
    print(f"✓ Total: {total_cropped} cropped images")


def cmd_coco(args):
    """Crop COCO format"""
    # Load COCO JSON
    with open(args.annotation, 'r') as f:
        coco_data = json.load(f)
    
    images_dir = Path(args.images)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build image index
    images = {img['id']: img for img in coco_data.get('images', [])}
    
    print(f"Processing {len(images)} images...")
    
    total_cropped = 0
    object_idx = 0
    
    for img_id, img_info in images.items():
        img_name = img_info.get('file_name', f'{img_id}.jpg')
        img_path = images_dir / img_name
        
        if not img_path.exists():
            continue
        
        width = img_info.get('width', 0)
        height = img_info.get('height', 0)
        
        if width == 0 or height == 0:
            with Image.open(img_path) as img:
                width, height = img.size
        
        # Parse annotations
        annotations = parse_coco_annotation(coco_data, img_id)
        
        if not annotations:
            continue
        
        if args.objects:
            for i, bbox in enumerate(annotations):
                class_id, x1, y1, x2, y2 = bbox
                
                if args.min_size:
                    if (x2 - x1) < args.min_size or (y2 - y1) < args.min_size:
                        continue
                
                cropped = crop_image(str(img_path), bbox, args.padding, width, height)
                base_name = Path(img_name).stem
                output_name = f"{base_name}_{i}.{args.format}"
                output_path = output_dir / output_name
                cropped.save(output_path, quality=args.quality)
                total_cropped += 1
        else:
            cropped = crop_image(str(img_path), annotations[0], args.padding, width, height)
            base_name = Path(img_name).stem
            output_path = output_dir / f"{base_name}_crop.{args.format}"
            cropped.save(output_path, quality=args.quality)
            total_cropped += 1
    
    print(f"✓ Total: {total_cropped} cropped images")


def cmd_voc(args):
    """Crop VOC format"""
    import xml.etree.ElementTree as ET
    
    xml_dir = Path(args.annotations)
    images_dir = Path(args.images)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all XML files
    xml_files = list(xml_dir.glob("*.xml"))
    
    print(f"Processing {len(xml_files)} images...")
    
    total_cropped = 0
    
    for xml_path in xml_files:
        base_name = xml_path.stem
        
        # Find image
        img_path = None
        for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            potential = images_dir / (base_name + ext)
            if potential.exists():
                img_path = potential
                break
        
        if not img_path:
            continue
        
        # Parse annotations
        annotations = parse_voc_annotation(str(xml_path))
        
        if not annotations:
            continue
        
        if args.objects:
            for i, bbox in enumerate(annotations):
                class_id, x1, y1, x2, y2 = bbox
                
                if args.min_size:
                    if (x2 - x1) < args.min_size or (y2 - y1) < args.min_size:
                        continue
                
                cropped = crop_image(str(img_path), bbox, args.padding)
                output_name = f"{base_name}_{i}.{args.format}"
                output_path = output_dir / output_name
                cropped.save(output_path, quality=args.quality)
                total_cropped += 1
        else:
            cropped = crop_image(str(img_path), annotations[0], args.padding)
            output_path = output_dir / f"{base_name}_crop.{args.format}"
            cropped.save(output_path, quality=args.quality)
            total_cropped += 1
    
    print(f"✓ Total: {total_cropped} cropped images")


def main():
    parser = argparse.ArgumentParser(
        description="Image Cropper - Crop images based on bounding boxes"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # yolo command
    parser_yolo = subparsers.add_parser("yolo", help="Crop YOLO format")
    parser_yolo.add_argument("images", help="Images directory")
    parser_yolo.add_argument("labels", help="YOLO labels directory")
    parser_yolo.add_argument("output", help="Output directory")
    parser_yolo.add_argument("--padding", "-p", type=int, default=0, help="Padding around box")
    parser_yolo.add_argument("--objects", "-o", action="store_true", help="Save each object separately")
    parser_yolo.add_argument("--min-size", type=int, help="Minimum box size")
    parser_yolo.add_argument("--format", "-f", default="jpg", help="Output format")
    parser_yolo.add_argument("--quality", "-q", type=int, default=95, help="JPEG quality")
    parser_yolo.set_defaults(func=cmd_yolo)
    
    # coco command
    parser_coco = subparsers.add_parser("coco", help="Crop COCO format")
    parser_coco.add_argument("annotation", help="COCO JSON file")
    parser_coco.add_argument("images", help="Images directory")
    parser_coco.add_argument("output", help="Output directory")
    parser_coco.add_argument("--padding", "-p", type=int, default=0, help="Padding around box")
    parser_coco.add_argument("--objects", "-o", action="store_true", help="Save each object separately")
    parser_coco.add_argument("--min-size", type=int, help="Minimum box size")
    parser_coco.add_argument("--format", "-f", default="jpg", help="Output format")
    parser_coco.add_argument("--quality", "-q", type=int, default=95, help="JPEG quality")
    parser_coco.set_defaults(func=cmd_coco)
    
    # voc command
    parser_voc = subparsers.add_parser("voc", help="Crop VOC format")
    parser_voc.add_argument("annotations", help="VOC XML directory")
    parser_voc.add_argument("images", help="Images directory")
    parser_voc.add_argument("output", help="Output directory")
    parser_voc.add_argument("--padding", "-p", type=int, default=0, help="Padding around box")
    parser_voc.add_argument("--objects", "-o", action="store_true", help="Save each object separately")
    parser_voc.add_argument("--min-size", type=int, help="Minimum box size")
    parser_voc.add_argument("--format", "-f", default="jpg", help="Output format")
    parser_voc.add_argument("--quality", "-q", type=int, default=95, help="JPEG quality")
    parser_voc.set_defaults(func=cmd_voc)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
