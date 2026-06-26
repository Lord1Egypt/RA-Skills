#!/bin/bash
# Lobster Distill - Download and Decrypt / 龙虾蒸馏 - 下载与解密
# Usage / 用法: bash receive.sh <url> <password> <output_name> [tar|file]

set -e

URL="$1"
PASSWORD="$2"
NAME="$3"
TYPE="${4:-tar}"

if [ -z "$URL" ] || [ -z "$PASSWORD" ] || [ -z "$NAME" ]; then
    echo "Usage / 用法: bash receive.sh <url> <password> <output_name> [tar|file]"
    echo "  <url>:         Download link from Notes / Notes 中的下载链接"
    echo "  <password>:    Decryption password from Notes / Notes 中的解密密码"
    echo "  <output_name>: Name for the skill directory / 技能目录名称"
    echo "  [tar|file]:    tar = extract as directory (default) / 解压为目录（默认）"
    echo "                 file = save as single file / 保存为单个文件"
    exit 1
fi

echo "[+] Downloading / 正在下载..."
curl -s -o "/tmp/${NAME}.enc" "$URL"

if [ ! -f "/tmp/${NAME}.enc" ]; then
    echo "[-] Download failed! / 下载失败！"
    exit 1
fi

echo "[+] Decrypting / 正在解密..."
if [ "$TYPE" = "tar" ]; then
    openssl enc -aes-256-cbc -d -pbkdf2 -in "/tmp/${NAME}.enc" -out "/tmp/${NAME}.tar.gz" -k "$PASSWORD"
    echo "[+] Extracting to skills/ / 正在解压到 skills/..."
    mkdir -p "skills/${NAME}"
    tar xzf "/tmp/${NAME}.tar.gz" -C "skills/${NAME}/"
    echo "[+] Done! Skill installed at / 完成！技能已安装到: skills/${NAME}/"
    echo "[+] Read the docs / 阅读文档:"
    echo "    cat skills/${NAME}/SKILL.md"
    rm -f "/tmp/${NAME}.enc" "/tmp/${NAME}.tar.gz"
else
    openssl enc -aes-256-cbc -d -pbkdf2 -in "/tmp/${NAME}.enc" -out "/tmp/${NAME}" -k "$PASSWORD"
    echo "[+] Decrypted to / 已解密到: /tmp/${NAME}"
    echo "[+] Read it / 阅读内容:"
    echo "    cat /tmp/${NAME}"
    rm -f "/tmp/${NAME}.enc"
fi
