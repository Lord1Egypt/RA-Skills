#!/usr/bin/env python3
"""
Photo Organizer - 照片批量整理工具
"""

import os
import re
import json
import argparse
from datetime import datetime
from pathlib import Path
from shutil import copy2

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class PhotoOrganizer:
    def __init__(self, input_dir, output_dir=None):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir) if output_dir else self.input_dir / "organized"
        self.backup_file = self.output_dir / ".photo-organizer-backup.json"
        self.backup_data = {}

    def load_backup(self):
        if self.backup_file.exists():
            with open(self.backup_file, 'r', encoding='utf-8') as f:
                self.backup_data = json.load(f)
        return self.backup_data

    def save_backup(self, mappings):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(self.backup_file, 'w', encoding='utf-8') as f:
            json.dump(mappings, f, indent=2, ensure_ascii=False)

    def get_photos(self):
        photos = []
        extensions = {'.jpg', '.jpeg', '.png', '.gif', '.heic', '.webp'}
        for item in self.input_dir.iterdir():
            if item.is_file() and item.suffix.lower() in extensions:
                photos.append(item)
        return sorted(photos)

    def get_exif_data(self, photo_path):
        if not HAS_PIL:
            return None
        try:
            image = Image.open(photo_path)
            exif_data = image._getexif()
            if exif_data:
                exif = {}
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'GPSInfo':
                        gps_data = {}
                        for gps_tag_id, gps_value in value.items():
                            gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            gps_data[gps_tag] = gps_value
                        exif[tag] = gps_data
                    else:
                        exif[tag] = value
                return exif
        except Exception:
            pass
        return None

    def get_capture_time(self, photo_path, exif_data=None):
        if exif_data:
            date_time = exif_data.get('DateTime')
            date_time_original = exif_data.get('DateTimeOriginal')
            if date_time_original:
                return date_time_original
            if date_time:
                return date_time
        mtime = datetime.fromtimestamp(photo_path.stat().st_mtime)
        return mtime.strftime('%Y:%m:%d %H:%M:%S')

    def get_date_components(self, date_str):
        try:
            if ' ' in date_str:
                date_part = date_str.split(' ')[0]
                year, month, day = date_part.split(':')
                return year, month, day
        except Exception:
            pass
        return 'unknown', 'unknown', 'unknown'

    def get_folder_path(self, photo_path, organize_by='date'):
        exif_data = self.get_exif_data(photo_path)
        date_str = self.get_capture_time(photo_path, exif_data)
        year, month, day = self.get_date_components(date_str)

        if organize_by == 'date':
            return self.output_dir / year / month
        elif organize_by == 'location':
            return self.output_dir / 'by-location' / year
        else:
            return self.output_dir / year

    def organize(self, organize_by='date', preview=False):
        photos = self.get_photos()
        mappings = {}

        for photo_path in photos:
            target_folder = self.get_folder_path(photo_path, organize_by)
            target_path = target_folder / photo_path.name

            mappings[str(photo_path)] = str(target_path)

            if preview:
                print(f"预览: {photo_path.name} -> {target_folder.name}/{photo_path.name}")

        if preview:
            return mappings

        confirm = input(f"即将整理 {len(mappings)} 个照片，确认吗？(y/N): ")
        if confirm.lower() != 'y':
            print("操作已取消")
            return {}

        # 保存备份
        self.save_backup(mappings)

        # 执行整理
        for old_str, new_str in mappings.items():
            old_path = Path(old_str)
            new_path = Path(new_str)
            new_path.parent.mkdir(parents=True, exist_ok=True)
            if old_path.exists() and not new_path.exists():
                copy2(old_path, new_path)
                print(f"整理: {old_path.name} -> {new_path.parent.name}/{new_path.name}")

        return mappings

    def undo(self):
        backup = self.load_backup()
        if not backup:
            print("没有找到备份文件，无法撤销")
            return False

        reverse_mappings = {v: k for k, v in backup.items()}
        count = 0

        for new_str, old_str in reverse_mappings.items():
            new_path = Path(new_str)
            old_path = Path(old_str)
            if new_path.exists() and not old_path.exists():
                copy2(new_path, old_path)
                new_path.unlink()
                print(f"撤销: {new_path.name} -> {old_path.name}")
                count += 1

        if count > 0:
            self.backup_file.unlink(missing_ok=True)
            print(f"已撤销 {count} 个照片的整理")
            return True
        else:
            print("没有需要撤销的照片")
            return False


def main():
    parser = argparse.ArgumentParser(description="照片批量整理工具")
    subparsers = parser.add_subparsers(title="命令", dest="command")

    # organize 命令
    organize_parser = subparsers.add_parser("organize", help="整理照片")
    organize_parser.add_argument("directory", help="照片目录")
    organize_parser.add_argument("--by", choices=["date", "location"], default="date", help="整理方式（默认按时间）")
    organize_parser.add_argument("--output", help="输出目录")
    organize_parser.add_argument("--preview", action="store_true", help="预览模式")

    # undo 命令
    undo_parser = subparsers.add_parser("undo", help="撤销整理")
    undo_parser.add_argument("directory", help="输出目录")

    args = parser.parse_args()

    if args.command == "organize":
        organizer = PhotoOrganizer(args.directory, args.output)
        organizer.organize(organize_by=args.by, preview=args.preview)
    elif args.command == "undo":
        organizer = PhotoOrganizer(args.directory, args.directory)
        organizer.undo()


if __name__ == "__main__":
    main()
