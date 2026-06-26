# Changelog

## [0.9.0] - 2026-04-11

### Added
- 文生音乐：支持有歌词和纯音乐（instrumental）两种模式
- 翻唱模式：支持 URL 和本地 base64 参考音频，模型自动切换为 music-cover
- 自动歌词生成：非纯音乐且未提供歌词时，自动调用 lyrics_generation API
- 免费模型降级：初始化时未提供 API Key 则使用 music-2.6-free / music-cover-free
- 默认输出配置：44100Hz / 256kbps / WAV / HEX / 非流式
- 支持从文件读取歌词（--lyrics-file）
- 完整参数支持：stream、output_format、audio_setting、aigc_watermark、lyrics_optimizer
