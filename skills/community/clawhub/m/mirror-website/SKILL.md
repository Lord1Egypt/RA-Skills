---
name: mirror-website
description: "镜像网站到本地的完整工作流。当用户说镜像网站、下载网站、抓取网站、本地化网站，或者提供一个网址和保存路径时，必须使用此 skill。输入格式为：镜像网站 www.example.com 保存地址 /a/b/c。自动处理代理、递归下载、文件名清理等全流程。即使用户只是提到想把某个网站保存到本地、离线浏览、克隆站点，也应触发此 skill。"
---

# 镜像网站 Skill

## 触发格式

用户输入类似：
```
镜像网站: www.example.com，保存地址: /a/b/c
```

如果用户未提供保存路径，默认使用 `/home/claude/mirror/<DOMAIN>` 作为保存路径，并在最终输出时告知用户实际路径。

## 执行步骤

### 第一步：解析输入

从用户输入中提取：
- `TARGET_URL`：目标网址（自动补全 `https://`）
- `SAVE_PATH`：保存路径（绝对路径）
- `DOMAIN`：域名部分（用于 `--domains` 参数）

**域名处理规则：**
1. 先用 `curl -sI` 测试原始域名，观察是否有 301/302 跳转
2. 如果 `www.example.com` 跳转到 `example.com`（或反之），使用跳转后的域名作为 `DOMAIN` 和 `TARGET_URL`
3. 如果无跳转，保持用户输入的域名不变
4. `--domains` 参数同时包含 `www` 和非 `www` 版本，确保不遗漏资源：`--domains example.com,www.example.com`

### 第二步：创建保存目录

```bash
mkdir -p <SAVE_PATH>
```

### 第三步：检测网络连通性与代理

在执行 wget 前，先检测是否能直接连通目标站点：

```bash
# 先尝试直连
curl -sI --connect-timeout 5 https://<DOMAIN>/ > /dev/null 2>&1
DIRECT=$?

# 如果直连失败，尝试常见代理
if [ $DIRECT -ne 0 ]; then
  curl -sI --connect-timeout 5 -x http://127.0.0.1:7890 https://<DOMAIN>/ > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    export https_proxy=http://127.0.0.1:7890
    export http_proxy=http://127.0.0.1:7890
    echo "使用代理: http://127.0.0.1:7890"
  else
    echo "警告: 直连和代理均无法访问目标站点，请检查网络"
  fi
else
  echo "直连可用，无需代理"
fi
```

如果均不可用，告知用户网络问题并终止。

### 第四步：执行 wget 镜像下载

```bash
wget --recursive \
     --level=5 \
     --page-requisites \
     --convert-links \
     --domains <DOMAIN>,www.<DOMAIN> \
     --wait=2 \
     --random-wait \
     --no-check-certificate \
     --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36" \
     --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
     --header="Accept-Language: zh-CN,zh;q=0.9,en;q=0.8" \
     -e robots=off \
     -P <SAVE_PATH> \
     https://<DOMAIN>/
```

**参数说明：**
| 参数 | 说明 |
|------|------|
| `--level=5` | 递归深度5层 |
| `--page-requisites` | 下载页面所需的CSS/JS/图片 |
| `--convert-links` | 转换链接为本地路径 |
| `--domains` | 同时包含 www 和非 www，避免遗漏 |
| `--wait=2 --random-wait` | 随机等待，避免被封 |
| `--no-check-certificate` | 跳过SSL证书验证 |
| `-e robots=off` | 忽略 robots.txt |

> **注意：不使用 `--html-extension` / `--adjust-extension`。** 该参数会根据 Content-Type 自动追加扩展名，导致 `fontawesome.min.css` 被保存为 `fontawesome.min.css.css`。

### 第五步：补充下载带参数的资源（?v=xxx 类）

wget 的 `--page-requisites` 经常无法正确下载 URL 末尾带查询参数的资源（如 `player.js?v=2`、`style.css?v=20251204`）。
需要从已下载的 HTML 中提取这些资源链接，逐个单独下载到**去除查询参数后的正确文件名**。

**⚠️ 重要：此步骤必须使用文件写入工具创建脚本，然后执行，不要在终端逐条运行。**

使用 `create_file` 在 `<SAVE_PATH>/fetch-query-assets.sh` 创建以下脚本：

```bash
#!/bin/bash
# 补充下载带 ?query 参数的资源文件
# 用法：bash fetch-query-assets.sh <下载目录> <域名>

DIR="$1"
DOMAIN="$2"

if [ -z "$DIR" ] || [ -z "$DOMAIN" ]; then
  echo "用法: bash fetch-query-assets.sh <下载目录> <域名>"
  exit 1
fi

cd "$DIR" || exit 1

echo "=== 扫描带查询参数的资源引用 ==="

# 从 HTML 文件中提取所有带 ? 的 src/href 引用
{
  grep -roh --include="*.html" -E '(src|href)="[^"]*\?[^"]*"' .
  grep -roh --include="*.html" -E "(src|href)='[^']*\?[^']*'" .
} | sed -E "s/^(src|href)=['\"]([^'\"]*)['\"]$/\2/" | sort -u | while IFS= read -r url; do

  # 跳过完整 URL（外部资源）
  echo "$url" | grep -qE '^(https?://|//)' && continue

  # 去掉查询参数得到本地文件路径
  clean_path=$(echo "$url" | sed 's/\?.*//')

  # 构建完整下载 URL
  if echo "$url" | grep -q '^/'; then
    full_url="https://${DOMAIN}${url}"
    local_file="${DIR}/${DOMAIN}${clean_path}"
  else
    full_url="https://${DOMAIN}/${url}"
    local_file="${DIR}/${DOMAIN}/${clean_path}"
  fi

  # 如果文件已存在则跳过
  if [ -f "$local_file" ]; then
    continue
  fi

  echo "下载: $full_url → $local_file"
  mkdir -p "$(dirname "$local_file")"
  wget -q --no-check-certificate \
    --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0" \
    -O "$local_file" \
    "$full_url" || echo "  失败: $full_url"
done

echo "=== 补充下载完成 ==="
```

写入后执行：
```bash
bash <SAVE_PATH>/fetch-query-assets.sh <SAVE_PATH> <DOMAIN>
```

### 第六步：创建 fix-filenames.sh 修复脚本并执行

所有文件下载完成后，使用 `create_file` 工具在 `<SAVE_PATH>/fix-filenames.sh` 创建以下脚本，然后用 `bash` 执行。

**⚠️ 重要：必须使用文件写入工具一次性写入完整脚本，不要用 `echo` 逐行拼接，也不要把清理命令零散地逐条运行在终端中。**

以下是 `fix-filenames.sh` 的完整内容：

```bash
#!/bin/bash
# 修复 wget 镜像下载后的文件名和引用路径问题
# 用法：bash fix-filenames.sh /path/to/download/dir

DIR="$1"
if [ -z "$DIR" ]; then
  echo "用法: bash fix-filenames.sh <下载目录路径>"
  exit 1
fi
if [ ! -d "$DIR" ]; then
  echo "错误: 目录不存在: $DIR"
  exit 1
fi

cd "$DIR" || exit 1
echo "=== 开始修复: $(pwd) ==="
echo "修复前文件总数: $(find . -type f | wc -l)"

# ========================================
# 1. 去除文件名中查询参数
#    同时处理两种情况：
#    a) 文件名含真实 ?：  DPlayer.min.js?v=5 → DPlayer.min.js
#    b) 文件名含编码 %3F：DPlayer.min.js%3Fv=5 → DPlayer.min.js
#    c) 参数后还带扩展名：mirages.min.css?v=20251215.css → mirages.min.css
# ========================================
echo ""
echo "--- 阶段1: 去除文件名中的查询参数 ---"

rename_query_file() {
  local f="$1"
  local newname="$2"
  if [ "$f" != "$newname" ] && [ ! -f "$newname" ]; then
    mkdir -p "$(dirname "$newname")"
    mv -f -- "$f" "$newname"
    echo "  重命名: $f → $newname"
  elif [ "$f" != "$newname" ] && [ -f "$newname" ]; then
    rm -f -- "$f"
    echo "  删除重复: $f（$newname 已存在）"
  fi
}

# 1a) 处理真实 ? 字符
find . -type f -name '*\?*' | while IFS= read -r f; do
  newname=$(echo "$f" | sed 's/\?.*//')
  rename_query_file "$f" "$newname"
done

# 1b) 处理 URL 编码的 %3F（wget 在某些系统下会这样保存）
find . -type f -name '*%3F*' | while IFS= read -r f; do
  newname=$(echo "$f" | sed 's/%3[Ff].*//')
  rename_query_file "$f" "$newname"
done

# 1c) 处理 @ 替代 ? 的形式（某些 wget 版本将 ? 转为 @）
#    匹配模式：文件名中 .ext@ 后跟参数，如 foo.js@v=5、foo.css@t=20231032
find . -type f | grep -E '\.[a-zA-Z0-9]{1,5}@' | while IFS= read -r f; do
  newname=$(echo "$f" | sed -E 's/(\.[a-zA-Z0-9]{1,5})@.*/\1/')
  rename_query_file "$f" "$newname"
done

# ========================================
# 2. 去除重复扩展名
#    audio.css.css → audio.css
# ========================================
echo ""
echo "--- 阶段2: 去除重复扩展名 ---"
find . -type f | while IFS= read -r f; do
  newname=$(echo "$f" | sed -E 's/(\.[a-zA-Z0-9]{1,5})\1$/\1/')
  if [ "$f" != "$newname" ]; then
    mv -f -- "$f" "$newname"
    echo "  重命名: $f → $newname"
  fi
done

# ========================================
# 3. 修复 HTML/CSS/JS 中的资源引用路径
#    将所有 ?xxx 查询参数从引用中去除
# ========================================
echo ""
echo "--- 阶段3: 修复资源引用路径 ---"

# 修复 HTML 中双引号的 src/href
find . -name "*.html" -type f -exec sed -i -E \
  's/(src|href)="([^"]*)\?[^"]*"/\1="\2"/g' {} +

# 修复 HTML 中单引号的 src/href
find . -name "*.html" -type f -exec sed -i -E \
  "s/(src|href)='([^']*)\?[^']*'/\1='\2'/g" {} +

# 修复 CSS/HTML 中的 url() 引用
find . \( -name "*.css" -o -name "*.html" \) -type f -exec sed -i -E \
  's/url\(([^)]*)\?[^)]*\)/url(\1)/g' {} +

# 修复 JS 中的资源引用（常见静态资源扩展名）
find . -name "*.js" -type f -exec sed -i -E \
  's/(["'"'"'][^"'"'"']*\.(js|css|png|jpg|jpeg|gif|svg|ico|woff2?|ttf|eot|mp3|mp4|webp|avif))\?[^"'"'"']*(["'"'"'])/\1\3/g' {} +

echo "  HTML/CSS/JS 引用路径已修复"

# ========================================
# 4. 清理 wget 生成的 convert-links 备份文件
# ========================================
echo ""
echo "--- 阶段4: 清理备份文件 ---"
ORIG_COUNT=$(find . -name "*.orig" -type f | wc -l)
if [ "$ORIG_COUNT" -gt 0 ]; then
  find . -name "*.orig" -type f -delete
  echo "  已删除 $ORIG_COUNT 个 .orig 备份文件"
else
  echo "  无备份文件需要清理"
fi

echo ""
echo "=== 修复完成 ==="
echo "修复后文件总数: $(find . -type f | wc -l)"
```

写入完成后执行：
```bash
bash <SAVE_PATH>/fix-filenames.sh <SAVE_PATH>
```

### 第七步：验证结果

执行简单验证确保镜像可用：

```bash
# 检查是否有残留的带查询参数的文件名（? / %3F / .ext@param 三种形式）
R1=$(find <SAVE_PATH> -type f -name '*\?*' | wc -l)
R2=$(find <SAVE_PATH> -type f \( -name '*%3F*' -o -name '*%3f*' \) | wc -l)
R3=$(find <SAVE_PATH> -type f | grep -cE '\.[a-zA-Z0-9]{1,5}@')
echo "残留带参数文件名: ?=$R1, %3F=$R2, @param=$R3"

# 如果有残留，列出具体文件方便排查
if [ $((R1 + R2 + R3)) -gt 0 ]; then
  echo "残留文件列表:"
  find <SAVE_PATH> -type f \( -name '*\?*' -o -name '*%3F*' -o -name '*%3f*' \)
  find <SAVE_PATH> -type f | grep -E '\.[a-zA-Z0-9]{1,5}@'
fi

# 检查 HTML 中是否还有带 ?xxx= 的资源引用（覆盖 ?v= ?t= ?ver= 等）
REFS=$(grep -rl --include="*.html" -E '\?(v|t|ver|_|hash|ts)=' <SAVE_PATH> 2>/dev/null | wc -l)
echo "残留带参数引用的HTML文件: $REFS"

# 统计文件类型分布
echo "文件类型分布:"
find <SAVE_PATH> -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20
```

### 第八步：启动本地预览服务器

清理完成后，在保存目录下启动一个 Python HTTP 服务器，方便用户在浏览器中预览镜像效果。

```bash
# 先检查 9527 端口是否被占用，如果被占用则自动换一个可用端口
PORT=9527
while lsof -i :$PORT > /dev/null 2>&1; do
  PORT=$((PORT + 1))
done

# 进入网站根目录（即域名子目录），以后台方式启动服务器
cd <SAVE_PATH>/<DOMAIN>
nohup python3 -m http.server $PORT > /dev/null 2>&1 &
SERVER_PID=$!

echo "预览服务器已启动:"
echo "  地址: http://localhost:$PORT"
echo "  PID:  $SERVER_PID"
echo "  停止: kill $SERVER_PID"
```

**注意事项：**
- 服务器工作目录是 `<SAVE_PATH>/<DOMAIN>`（即网站根目录），这样访问 `http://localhost:9527` 就相当于访问网站首页
- 默认端口 9527，如果被占用会自动递增寻找可用端口
- 使用 `nohup` 后台运行，不会阻塞终端
- 告知用户 PID，方便随时 `kill` 停止服务

### 第九步：输出结果摘要

完成后告知用户：
- 保存路径
- 下载文件数量（`find <SAVE_PATH> -type f | wc -l`）
- 验证结果（是否有残留问题）
- 预览地址（`http://localhost:<PORT>`）
- 停止服务器命令（`kill <SERVER_PID>`）
- 如果后续需要重新修复文件名，可以再次运行：`bash <SAVE_PATH>/fix-filenames.sh <SAVE_PATH>`

## 常见问题处理

### 连接被拒绝 / SSL 失败
第三步已自动检测代理。如果仍然失败，告知用户需要开启代理工具（如 Clash）。

### 只下载了首页
通常是域名重定向问题（www → 非www），已在第一步通过 curl 跳转检测处理。如果仍有问题，检查目标站是否为 SPA（单页应用），wget 无法抓取 JS 渲染的内容。

### 下载速度过慢
可调整 `--wait=1` 或去掉 `--random-wait`，但注意可能被服务器限速。

### 动态内容（JS 渲染的页面）无法抓取
wget 不支持 JavaScript 渲染，这类网站建议用 Puppeteer 或 Playwright。告知用户此 skill 适用于传统服务端渲染（SSR）网站。

### 下载完成后文件名仍有问题
重新执行修复脚本即可：
```bash
bash <SAVE_PATH>/fix-filenames.sh <SAVE_PATH>
```

### 部分资源 404
某些带查询参数的资源可能在服务器端依赖查询参数来返回不同内容（如版本化 CDN）。这种情况下去掉参数后可能 404，属于正常现象，不影响大多数静态站点的镜像。
