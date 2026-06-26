
#!/bin/bash

# 压缩图片并发送到 Telegram
# 作者：Honcy Ye

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 输入参数
IMAGE_PATH="$1"
TARGET_ID="$2"

# 检查输入参数
if [ -z "$IMAGE_PATH" ] || [ -z "$TARGET_ID" ]; then
    echo "Usage: $0 <image_path> <telegram_chat_id>"
    exit 1
fi

# 压缩图片
COMPRESSED_IMAGE=$("$SCRIPT_DIR/compress_image.sh" "$IMAGE_PATH")

# 检查压缩是否成功
if [ $? -ne 0 ]; then
    echo "Error: Failed to compress image"
    exit 1
fi

# 发送压缩后的图片
openclaw message send --channel telegram --target "$TARGET_ID" --media "$COMPRESSED_IMAGE"
