
#!/bin/bash

# 压缩图片并发送到微信文件传输助手
# 作者：Honcy Ye

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 输入参数
IMAGE_PATH="$1"
CONTACT_NAME="${2:-文件传输助手}"

# 检查输入参数
if [ -z "$IMAGE_PATH" ]; then
    echo "Usage: $0 <image_path> [contact_name]"
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
bash "/Users/honcy/.openclaw/skills/WeChat-Send/scripts/wechat_send_image.sh" "$CONTACT_NAME" "$COMPRESSED_IMAGE"
