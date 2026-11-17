#!/usr/bin/env bash
# gen_license.sh — Step 5: 生成 LICENSE 文件
# Usage: ./gen_license.sh <fork-path> <MIT|Apache-2.0|GPL-3.0> ["<real name>"] [year]
# Author 字段优先级: 命令行参数 > OSG_AUTHOR_NAME > profile.env > git config
set -euo pipefail

. "$(dirname "$0")/_lib_profile.sh"
osg_resolve_identity

FORK="${1:-}"
LICENSE_TYPE="${2:-}"
AUTHOR="${3:-${OSG_AUTHOR_NAME:-}}"
YEAR="${4:-$(date +%Y)}"

if [[ -z "$FORK" || -z "$LICENSE_TYPE" ]]; then
  cat <<EOF >&2
Usage: $0 <fork-path> <license-type> ["<real name>"] [year]
  license-type: MIT | Apache-2.0 | GPL-3.0
  real name:    可选；不传则从 OSG_AUTHOR_NAME / profile.env / git config 取
                未配置 profile 请先跑: bash $(dirname "$0")/setup_profile.sh
  year:         默认当年

⚠️  Apache-2.0 / GPL-3.0 生成的是缩略版引用文本；如果你的项目对法律严谨性
   有要求（商用、有专利防护需求等），请从官方 URL 替换为完整许可证文本：
     Apache-2.0: https://www.apache.org/licenses/LICENSE-2.0.txt
     GPL-3.0:    https://www.gnu.org/licenses/gpl-3.0.txt
EOF
  exit 1
fi

if [[ -z "$AUTHOR" ]]; then
  cat <<EOF >&2
❌ 未指定作者，且 OSG_AUTHOR_NAME / profile.env / git config 都没有可用值
   请任选一种方式：
     ① 一次性配置（推荐，跨 agent 跨 skill 重装持久化）:
          bash $(dirname "$0")/setup_profile.sh
     ② 命令行显式传:
          $0 $FORK $LICENSE_TYPE "Jane Doe"
     ③ 临时环境变量:
          export OSG_AUTHOR_NAME="Jane Doe"
EOF
  exit 1
fi

[[ -d "$FORK" ]] || { echo "❌ fork-path not a directory: $FORK" >&2; exit 2; }

# 清洗作者名：移除换行/回车/反引号/分号等会破坏文件格式或被 shell 误解的字符
# 注意:作者名进入 heredoc 不会被 eval,但仍可能破坏 LICENSE 的行格式
ORIG_AUTHOR="$AUTHOR"
AUTHOR="$(printf '%s' "$AUTHOR" | tr -d '\r\n`' | tr -d ';' | sed 's/[[:space:]]\+/ /g' | sed 's/^ *//;s/ *$//')"
if [[ "$AUTHOR" != "$ORIG_AUTHOR" ]]; then
  echo "ℹ️  作者名已清洗（移除换行/反引号/分号）: '$ORIG_AUTHOR' → '$AUTHOR'"
fi
if [[ -z "$AUTHOR" ]]; then
  echo "❌ 作者名清洗后为空，请提供有效作者名" >&2
  exit 4
fi

LICENSE_FILE="$FORK/LICENSE"

case "$LICENSE_TYPE" in
  MIT)
    cat > "$LICENSE_FILE" <<EOF
MIT License

Copyright (c) $YEAR $AUTHOR

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
    ;;

  Apache-2.0)
    cat > "$LICENSE_FILE" <<EOF
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Copyright $YEAR $AUTHOR

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

(Full text: see https://www.apache.org/licenses/LICENSE-2.0.txt)
EOF
    echo "ℹ️  Apache-2.0 短版已生成。如需完整法律文本，请从 https://www.apache.org/licenses/LICENSE-2.0.txt 替换。"
    ;;

  GPL-3.0)
    cat > "$LICENSE_FILE" <<EOF
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) $YEAR $AUTHOR

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

(Full text: see https://www.gnu.org/licenses/gpl-3.0.txt)
EOF
    echo "ℹ️  GPL-3.0 短版已生成。如需完整法律文本，请从 https://www.gnu.org/licenses/gpl-3.0.txt 替换。"
    ;;

  *)
    echo "❌ Unsupported license type: $LICENSE_TYPE" >&2
    echo "   Supported: MIT | Apache-2.0 | GPL-3.0" >&2
    exit 3
    ;;
esac

echo "✅ Generated $LICENSE_FILE ($LICENSE_TYPE, © $YEAR $AUTHOR)"
