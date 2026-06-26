#!/usr/bin/env bash

# 输入可以是包名或应用名
input="$1"

if [ -z "$input" ]; then
  echo "Usage: $0 <包名或应用名>"
  # exit 1
fi

echo "搜索: $input"
echo "---"

# 使用 frida-ps 列出所有应用并查找匹配项
result=$(frida-ps -Uai | grep -i "$input")

if [ $? -ne 0 ] || [ -z "$result" ]; then
  echo "未找到匹配的包"
  exit 1
fi

echo "$result"
echo "---"

# 获取匹配的包名（最后一个字段）
package=$(echo "$result" | head -1 | awk '{print $NF}')
echo "选中包: $package"
echo "---"

# 使用 adb 获取 APK 路径
path=$(adb shell pm path "$package" 2>/dev/null | sed 's/package://')

if [ -z "$path" ]; then
  echo "无法获取 APK 路径"
  exit 1
fi

echo "路径: $path"
echo "---"

# 获取APK文件名
filename=$(basename "$path")

# 拉取到本地
adb pull "$path" ./"$filename"
echo "已拉取到: $filename"