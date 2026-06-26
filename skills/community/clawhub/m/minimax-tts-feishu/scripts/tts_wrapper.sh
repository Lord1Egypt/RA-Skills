#!/bin/bash
# TTS wrapper - 支持多个子命令
# 用法:
#   tts_wrapper.sh tts "<文本>" [voice_id] [user_open_id]
#   tts_wrapper.sh design "<音色描述>" "<试听文本>" "<要说的内容>"
#   tts_wrapper.sh list
#   tts_wrapper.sh update
#   tts_wrapper.sh save "<文本>"           # 保存最后一条消息（用于转语音）
#   tts_wrapper.sh trigger "<用户消息>" <发送者open_id> [被回复消息ID]  # 触发转语音

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

case "$1" in
    tts)
        shift
        python3 "$SCRIPT_DIR/tts.py" "$@"
        ;;
    design)
        shift
        python3 "$SCRIPT_DIR/voice_design.py" "$@"
        ;;
    list)
        python3 "$SCRIPT_DIR/list_voices.py"
        ;;
    update)
        python3 "$SCRIPT_DIR/update_voices_map.py"
        ;;
    save)
        shift
        python3 "$SCRIPT_DIR/tts_from_chat.py" save "$@"
        ;;
    trigger)
        shift
        python3 "$SCRIPT_DIR/tts_from_chat.py" trigger "$@"
        ;;
    *)
        echo "用法:"
        echo "  tts_wrapper.sh tts <文本> [voice_id] [user_open_id]"
        echo "  tts_wrapper.sh design <音色描述> <试听文本> <要说的内容>"
        echo "  tts_wrapper.sh list"
        echo "  tts_wrapper.sh update"
        echo "  tts_wrapper.sh save <文本>"
        echo "  tts_wrapper.sh trigger <用户消息> <发送者open_id> [被回复消息ID]"
        exit 1
        ;;
esac
