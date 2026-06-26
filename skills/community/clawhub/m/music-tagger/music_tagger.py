#!/usr/bin/env python3
"""
Music Tagger - 音乐文件批量标签工具
"""

import os
import json
import argparse
from pathlib import Path
from shutil import copy2


class MusicTagger:
    def __init__(self, input_dir, output_dir=None):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir) if output_dir else self.input_dir / "organized"
        self.backup_file = self.output_dir / ".music-tagger-backup.json"
        self.backup_data = {}

        self.music_extensions = {
            ".mp3", ".flac", ".wav", ".aac", ".m4a", ".ogg",
            ".wma", ".ape", ".alac", ".opus", ".mpc", ".tta"
        }

    def load_backup(self):
        if self.backup_file.exists():
            with open(self.backup_file, 'r', encoding='utf-8') as f:
                self.backup_data = json.load(f)
        return self.backup_data

    def save_backup(self, mappings):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(self.backup_file, 'w', encoding='utf-8') as f:
            json.dump(mappings, f, indent=2, ensure_ascii=False)

    def get_music_files(self):
        music_files = []
        for item in self.input_dir.iterdir():
            if item.is_file() and item.suffix.lower() in self.music_extensions:
                music_files.append(item)
        return sorted(music_files)

    def read_tags(self, file_path):
        """读取音乐文件标签（简化版）"""
        print(f"[模拟] 读取标签: {file_path.name}")
        return {
            "title": file_path.stem,
            "artist": "Unknown Artist",
            "album": "Unknown Album",
            "genre": "Unknown Genre",
            "year": "",
            "track": ""
        }

    def write_tags(self, file_path, tags):
        """写入音乐文件标签（简化版）"""
        print(f"[模拟] 写入标签: {file_path.name}")
        print(f"[模拟] 标签: {tags}")
        return True

    def get_folder_path(self, file_path, organize_by='artist-album'):
        tags = self.read_tags(file_path)
        if organize_by == 'artist-album':
            artist = tags.get('artist', 'Unknown Artist')
            album = tags.get('album', 'Unknown Album')
            return self.output_dir / artist / album
        elif organize_by == 'genre':
            genre = tags.get('genre', 'Unknown Genre')
            return self.output_dir / genre
        elif organize_by == 'year':
            year = tags.get('year', 'Unknown Year')
            return self.output_dir / year
        else:
            return self.output_dir

    def batch_set_tag(self, tag_name, tag_value, preview=False):
        music_files = self.get_music_files()
        mappings = {}

        for music_path in music_files:
            tags = self.read_tags(music_path)
            tags[tag_name] = tag_value
            mappings[str(music_path)] = {
                "tags": tags,
                "action": f"set {tag_name} to {tag_value}"
            }

            if preview:
                print(f"预览: {music_path.name} → {tag_name} = {tag_value}")

        if preview:
            return mappings

        confirm = input(f"即将批量设置 {len(mappings)} 个文件的标签，确认吗？(y/N): ")
        if confirm.lower() != 'y':
            print("操作已取消")
            return {}

        for music_str, data in mappings.items():
            music_path = Path(music_str)
            self.write_tags(music_path, data['tags'])

        return mappings

    def organize(self, organize_by='artist-album', preview=False):
        music_files = self.get_music_files()
        mappings = {}

        for music_path in music_files:
            target_folder = self.get_folder_path(music_path, organize_by)
            target_path = target_folder / music_path.name

            mappings[str(music_path)] = str(target_path)

            if preview:
                if organize_by == 'artist-album':
                    tags = self.read_tags(music_path)
                    artist = tags.get('artist', 'Unknown Artist')
                    album = tags.get('album', 'Unknown Album')
                    print(f"预览: {music_path.name} -> {artist}/{album}/{music_path.name}")
                elif organize_by == 'genre':
                    tags = self.read_tags(music_path)
                    genre = tags.get('genre', 'Unknown Genre')
                    print(f"预览: {music_path.name} -> {genre}/{music_path.name}")
                else:
                    print(f"预览: {music_path.name} -> {music_path.name}")

        if preview:
            return mappings

        confirm = input(f"即将整理 {len(mappings)} 个音乐文件，确认吗？(y/N): ")
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
            print(f"已撤销 {count} 个音乐文件的操作")
            return True
        else:
            print("没有需要撤销的音乐文件")
            return False


def main():
    parser = argparse.ArgumentParser(description="音乐文件批量标签工具")
    subparsers = parser.add_subparsers(title="命令", dest="command")

    # read 命令
    read_parser = subparsers.add_parser("read", help="读取标签")
    read_parser.add_argument("file", help="音乐文件")

    # edit 命令
    edit_parser = subparsers.add_parser("edit", help="编辑标签")
    edit_parser.add_argument("file", help="音乐文件")
    edit_parser.add_argument("--title", help="歌名")
    edit_parser.add_argument("--artist", help="艺术家")
    edit_parser.add_argument("--album", help="专辑")
    edit_parser.add_argument("--genre", help="流派")
    edit_parser.add_argument("--year", help="年份")
    edit_parser.add_argument("--track", help="曲目号")

    # batch 命令
    batch_parser = subparsers.add_parser("batch", help="批量设置标签")
    batch_parser.add_argument("directory", help="音乐目录")
    batch_parser.add_argument("--title", help="批量设置歌名")
    batch_parser.add_argument("--artist", help="批量设置艺术家")
    batch_parser.add_argument("--album", help="批量设置专辑")
    batch_parser.add_argument("--genre", help="批量设置流派")
    batch_parser.add_argument("--year", help="批量设置年份")
    batch_parser.add_argument("--preview", action="store_true", help="预览模式")

    # organize 命令
    organize_parser = subparsers.add_parser("organize", help="整理音乐")
    organize_parser.add_argument("directory", help="音乐目录")
    organize_parser.add_argument("--by", choices=["artist-album", "genre", "year"], default="artist-album", help="整理方式（默认按艺术家/专辑）")
    organize_parser.add_argument("--output", help="输出目录")
    organize_parser.add_argument("--preview", action="store_true", help="预览模式")

    # undo 命令
    undo_parser = subparsers.add_parser("undo", help="撤销操作")
    undo_parser.add_argument("directory", help="输出目录")

    args = parser.parse_args()

    tagger = MusicTagger(args.directory if hasattr(args, 'directory') else '.', 
                          args.output if hasattr(args, 'output') else None)

    if args.command == "read":
        tags = tagger.read_tags(args.file)
        print(f"标签: {tags}")
    elif args.command == "edit":
        tags = tagger.read_tags(args.file)
        if args.title:
            tags['title'] = args.title
        if args.artist:
            tags['artist'] = args.artist
        if args.album:
            tags['album'] = args.album
        if args.genre:
            tags['genre'] = args.genre
        if args.year:
            tags['year'] = args.year
        if args.track:
            tags['track'] = args.track
        tagger.write_tags(args.file, tags)
    elif args.command == "batch":
        if args.artist:
            tagger.batch_set_tag('artist', args.artist, preview=args.preview)
        elif args.album:
            tagger.batch_set_tag('album', args.album, preview=args.preview)
        elif args.genre:
            tagger.batch_set_tag('genre', args.genre, preview=args.preview)
        elif args.year:
            tagger.batch_set_tag('year', args.year, preview=args.preview)
        elif args.title:
            tagger.batch_set_tag('title', args.title, preview=args.preview)
    elif args.command == "organize":
        tagger.organize(organize_by=args.by, preview=args.preview)
    elif args.command == "undo":
        tagger.undo()


if __name__ == "__main__":
    main()
