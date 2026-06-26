# li_nvvideocodec - NVIDIA AV1 ビデオ圧縮ツール

**バージョン**: 1.0.1  
**言語**: 日本語 (ja)

## 📋 概要

NVIDIA GPUハードウェアアクセラレーションAV1エンコーディングを使用したバッチビデオ圧縮ツール。インテリジェントな検証と複数の圧縮プロファイルで効率的にビデオを圧縮します。

## ✨ 特徴

- 🎯 **スマート検証** - 圧縮効果の自動テスト
- 📊 **3つのプロファイル** - 保守的/バランス/積極的
- 🖥️ **クロスプラットフォーム** - Windows & Ubuntu Linux
- 📈 **リアルタイム進行** - ライブ進行表示
- 🔒 **安全** - 元のファイルを保護

## 🚀 クイックスタート

```bash
# インタラクティブモード
python scripts/compress_videos.py

# コマンドラインモード
python scripts/compress_videos.py -i "/path/to/videos" -p B --no-confirm

# テストモード
python scripts/compress_videos.py -i "/path/to/videos" -p B --test
```

## 📊 圧縮プロファイル

| プロファイル | 解像度 | CRF | FPS | オーディオ | 節約 |
|------------|--------|-----|-----|----------|------|
| **A** | 維持 | 23 | 維持 | 128k | 40-60% |
| **B** ⭐ | 1280x720 | 24 | 24 | 96k | 65-75% |
| **C** | 1280x720 | 28 | 15 | 64k | 78-85% |

## ⚙️ 必要条件

- **FFmpeg** (av1_nvenc対応)
- **NVIDIA GPU** (GTX 1650以上)
- **Python 3.7+**

## 🤖 エージェント使用法

```bash
# 環境チェック
python agent_interface.py --action check

# ビデオ分析
python agent_interface.py --action analyze -i "/path/to/videos"

# 圧縮
python agent_interface.py --action compress -i "/path/to/videos" -p B
```
