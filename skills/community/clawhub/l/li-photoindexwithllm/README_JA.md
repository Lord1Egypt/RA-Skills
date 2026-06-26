# 📸 PhotoIndexWithLLM — 日本語

## 概要

PhotoIndexWithLLM は、ビジョンランゲージ（VL）大規模モデルを活用し、写真のスマート索引付け、分析、検索を提供するシステムです。

## クイックスタート

```bash
# 依存関係をインストール
pip install requests

# 写真をスキャン
python skill.py scan --dir /home/user/Photos

# 写真を検索
python skill.py search "ビーチ 夕日"

# JSON 出力
python skill.py search "ビーチ" --format json
```

## サポートされているプラットフォーム

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

## サポートされている画像形式（17種類）

| タイプ | フォーマット |
|--------|-------------|
| 一般的な形式 | `.jpg` `.jpeg` `.png` `.webp` `.bmp` `.tiff` `.gif` |
| iPhone/Apple | `.heic` `.heif` |
| Canon デジタル一眼 | `.cr2` |
| Nikon デジタル一眼 | `.nef` |
| Sony デジタル一眼 | `.arw` |
| その他 RAW | `.orf` `.raf` `.dng` `.rw2` `.pef` `.sr2` |

## プライバシー保護

- デフォルトでローカルモードのみ使用
- 写真はマシンから外部へ送信されません
- リモートモデルへの送信にはユーザーの確認が必要です

## 完全なコマンド一覧

```bash
# 写真をスキャン
python skill.py scan --dir /home/user/Photos

# 写真を検索
python skill.py search "ビーチ 夕日"

# スキャン＆検索
python skill.py scan_and_search --dir /home/user/Photos --query "ビーチ"

# アノテーション
python skill.py annotate --photo /photos/img001.jpg --type person --name 田中

# モデル訓練
python skill.py train

# 統計情報の表示
python skill.py stats

# 接続テスト
python skill.py test
```

## 連絡先

**著者**: 北京老李（beijingLL）
**ClawHub ID**: 43622283
