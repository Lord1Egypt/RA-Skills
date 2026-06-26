# 辅助脚本说明

## `strip_ansi.py`

从 stdin 或文件读取文本，移除常见 ANSI 转义序列，便于将终端录屏转为纯文本。

**依赖**：Python 3.9+，无第三方包。

```bash
python scripts/strip_ansi.py < session.log > session.clean.txt
python scripts/strip_ansi.py path/to/file.tty > out.txt
```

## `transcode_mp3.ps1`（Windows）

在项目根或 skill 目录下调用 ffmpeg，将音视频转为 MP3。

```powershell
powershell -File scripts/transcode_mp3.ps1 -InputPath "path/to/video.mp4" -OutputPath "path/to/out.mp3"
```

需已安装 ffmpeg 且可在 PATH 中调用。

## `transcode_mp3.sh`（Unix）

```bash
sh scripts/transcode_mp3.sh path/to/video.mp4 path/to/out.mp3
```
