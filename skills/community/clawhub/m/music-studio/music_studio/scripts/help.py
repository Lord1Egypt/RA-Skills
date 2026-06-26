"""help 命令：显示完整使用说明"""

TEXT = """=== Music Studio 帮助 ===

📝 作词
   python -m music_studio lyrics "<主题>" [--title "标题"] [--edit "歌词"]

🎵 文本生成音乐
   python -m music_studio music "<描述>" [歌词] [选项]

🎙️ 翻唱（基于参考音频）
   python -m music_studio cover "<翻唱描述>" --audio <音频URL> [--lyrics <歌词>]

🔑 Key 管理
   python -m music_studio set-key       # 显式保存 API Key 到 config.json
   python -m music_studio clear-key     # 删除本地保存的 API Key

🔄 重置
   python -m music_studio reset

🔧 music 参数

   参数说明：
     <描述>            - 音乐风格/情绪/场景描述（必填）
     歌词               - 可选，歌词内容（\\n分隔）
     --instrumental   - 生成纯音乐（无人声）
     --optimizer      - 自动根据描述生成歌词
     --format <fmt>   - 输出格式：url（默认，临时有效）或 hex
     --sr <rate>      - 采样率：16000/24000/32000/44100（默认44100）
     --bitrate <rate> - 比特率：32000/64000/128000/256000（默认256000）

🔧 cover 参数

   参数说明：
     <翻唱描述>       - 目标翻唱风格描述（必填，10~300字符）
     --audio <url>    - 参考音频URL（必填，6秒~6分钟，≤50MB）
     --lyrics <歌词>  - 可选歌词（不传则自动从参考音频提取）

🔢 歌词结构标签（14种）
   [Intro] [Verse] [Pre-Chorus] [Chorus] [Hook] [Drop]
   [Bridge] [Solo] [Build-up] [Instrumental] [Breakdown]
   [Break] [Interlude] [Outro]

📋 常用示例

   # 作词
   python -m music_studio lyrics "一首关于夏日海边的轻快情歌"

   # 作词：指定标题
   python -m music_studio lyrics "欢快的节日歌曲" --title "新年乐章"

   # 文本生成音乐（自动生成歌词）
   python -m music_studio music "欢快的节日歌曲" --optimizer

   # 纯音乐（无人声）
   python -m music_studio music "轻快的钢琴曲" --instrumental

   # 翻唱
   python -m music_studio cover "温柔女声翻唱" --audio "https://example.com/ref.mp3"

📚 音乐库管理
   python -m music_studio library list                 # 查看所有记录
   python -m music_studio library list lyrics          # 仅歌词
   python -m music_studio library list music           # 仅音乐
   python -m music_studio library get <id>             # 查看详情
   python -m music_studio library lyrics <id>          # 读取歌词
   python -m music_studio library url <id>             # 获取音频链接
   python -m music_studio library download <id>        # 下载音频
   python -m music_studio library export lyrics <id>   # 导出歌词
   python -m music_studio library export all           # 导出全部
   python -m music_studio library clean                # 清理过期记录
   python -m music_studio library purge                # 彻底清理所有文件

📂 初始化
   python -m music_studio init

🧹 清理过期文件
   python -m music_studio clean

❓ 常见建议
   - 只有在明确需要时，才用 set-key 保存到本地配置
"""


def main(_=None):
    print(TEXT)
