#!/bin/bash

# 提取APK中的AndroidManifest.xml到当前目录

APK_PATH="$1"

if [ -z "$APK_PATH" ]; then
    echo "用法: $0 <apk文件>"
    echo "示例: $0 base.apk"
    exit 1
fi

if [ ! -f "$APK_PATH" ]; then
    echo "错误: APK文件不存在: $APK_PATH"
    exit 1
fi

echo "开始提取 AndroidManifest.xml..."

# 1. apktool反编译（不反编译资源）
apktool d "$APK_PATH" -s -o decompile_for_extract

if [ $? -ne 0 ]; then
    echo "错误: apktool反编译失败"
    exit 1
fi

# 2. 复制AndroidManifest.xml到当前目录
cp decompile_for_extract/AndroidManifest.xml ./

if [ $? -ne 0 ]; then
    echo "错误: 复制AndroidManifest.xml失败"
    rm -rf decompile_for_extract
    exit 1
fi

# 3. 删除临时目录
rm -rf decompile_for_extract

echo "完成: AndroidManifest.xml已提取到当前目录"
