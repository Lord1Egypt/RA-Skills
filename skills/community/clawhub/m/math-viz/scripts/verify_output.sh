#!/bin/bash
# ============================================================
# math-viz 输出验证脚本 v1.0
# 嵌入在 math-viz skill 中，发布后任何人安装 skill 即可使用
# 用法: bash scripts/verify_output.sh <html-file>
# ============================================================
set -e

HTML="$1"
NAME=$(basename "$HTML" .html)
PASS=0
FAIL=0

# 确保能找到 Node.js（优先用系统node，其次找managed node）
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
for d in "$HOME/.workbuddy/binaries/node/versions/"*/bin; do
  [ -d "$d" ] && PATH="$d:$PATH"
done 2>/dev/null
NODE=$(command -v node 2>/dev/null || echo "")
if [ -z "$NODE" ]; then
  for p in /usr/local/bin/node /opt/homebrew/bin/node; do
    if [ -x "$p" ]; then NODE="$p"; break; fi
  done
fi

check() {
  local msg="$1" result="$2"
  if echo "$result" | grep -q '^pass'; then
    echo "  ✅ $msg"
    PASS=$((PASS + 1))
  else
    echo "  ❌ $msg"
    FAIL=$((FAIL + 1))
  fi
}

echo ""
echo "🔍 math-viz 输出验证: $NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ===== Step 1: 文件完整性 =====
echo "📋 Step 1: HTML 结构完整性"

if [ ! -f "$HTML" ]; then
  echo "  ❌ 文件不存在: $HTML"
  exit 1
fi

HAS_JSXGRAPH=$(grep -c 'jsxgraph\|jxgbox' "$HTML" 2>/dev/null || true)
HAS_THREEJS=$(grep -c 'Three\.js\|THREE\.\|OrbitControls' "$HTML" 2>/dev/null || true)

if [ "$HAS_JSXGRAPH" -gt 0 ] || [ "$HAS_THREEJS" -gt 0 ]; then
  check "画板容器存在 (JSXGraph/Three.js)" "pass"
else
  check "画板容器存在 (JSXGraph/Three.js)" "fail"
fi

if grep -q 'initBoard\|THREE\.Scene\|new THREE\.' "$HTML" 2>/dev/null; then
  check "图形初始化代码存在" "pass"
else
  check "图形初始化代码存在" "fail"
fi

SCRIPT_OPEN=$(grep -o '<script[^>]*>' "$HTML" | wc -l | tr -d ' ')
SCRIPT_CLOSE=$(grep -o '</script>' "$HTML" | wc -l | tr -d ' ')
check "<script> 标签闭合" "$([ "$SCRIPT_OPEN" = "$SCRIPT_CLOSE" ] && [ "$SCRIPT_OPEN" -gt 0 ] && echo pass || echo fail)"

HEAD_OPEN=$(grep -o '<head>' "$HTML" | wc -l | tr -d ' ')
HEAD_CLOSE=$(grep -o '</head>' "$HTML" | wc -l | tr -d ' ')
check "<head> 标签闭合" "$([ "$HEAD_OPEN" = "$HEAD_CLOSE" ] && echo pass || echo fail)"

BODY_OPEN=$(grep -o '<body>' "$HTML" | wc -l | tr -d ' ')
BODY_CLOSE=$(grep -o '</body>' "$HTML" | wc -l | tr -d ' ')
check "<body> 标签闭合" "$([ "$BODY_OPEN" = "$BODY_CLOSE" ] && echo pass || echo fail)"

# ===== Step 2: JS 语法检查 =====
echo ""
echo "📝 Step 2: JavaScript 语法检查"

if [ -n "$NODE" ]; then
  python3 -c "
import re, sys
html = open('$HTML', 'r', encoding='utf-8').read()
scripts = list(re.finditer(r'<script([^>]*)>(.*?)</script>', html, re.DOTALL))
found = False
for m in reversed(scripts):
    attrs = m.group(1).strip()
    if 'src=' not in attrs:
        code = m.group(2).strip()
        if len(code) > 50:
            with open('/tmp/_mathviz_verify.js', 'w') as f:
                f.write(code)
            found = True
            break
if not found:
    print('NOT_FOUND')
" 2>/dev/null > /tmp/_mathviz_extract_result

  if grep -q 'NOT_FOUND' /tmp/_mathviz_extract_result 2>/dev/null; then
    check "JS 语法检查" "fail  (未找到内联脚本)"
  else
    if "$NODE" --check /tmp/_mathviz_verify.js 2>/dev/null; then
      check "JS 语法检查" "pass"
    else
      echo "  --- 语法错误详情 ---"
      "$NODE" --check /tmp/_mathviz_verify.js 2>&1
      echo "  ---------------------"
      check "JS 语法检查" "fail"
    fi
  fi
else
  echo "  ⏭  跳过（未安装Node.js）"
fi

# ===== Step 3: 括号平衡 =====
echo ""
echo "🔢 Step 3: 括号平衡检查"

python3 -c "
import re, sys
html = open('$HTML', 'r', encoding='utf-8').read()
scripts = list(re.finditer(r'<script([^>]*)>(.*?)</script>', html, re.DOTALL))
code = ''
for m in reversed(scripts):
    if 'src=' not in m.group(1).strip():
        code = m.group(2).strip()
        break

if not code:
    print('  ❌ 未找到内联脚本')
    sys.exit(0)

depth = {'()': 0, '[]': 0, '{}': 0}
in_str = False
str_char = ''
escaped = False

for ch in code:
    if escaped:
        escaped = False
        continue
    if in_str:
        if ch == '\\\\': escaped = True
        elif ch == str_char: in_str = False
        continue
    if ch in ('\"', \"'\", '\`'):
        in_str = True
        str_char = ch
        continue
    if ch == '(': depth['()'] += 1
    elif ch == ')': depth['()'] -= 1
    elif ch == '[': depth['[]'] += 1
    elif ch == ']': depth['[]'] -= 1
    elif ch == '{': depth['{}'] += 1
    elif ch == '}': depth['{}'] -= 1

errors = []
for k, v in depth.items():
    if v != 0:
        errors.append(f'{k}: {v:+d}')
if not errors:
    print('PASS')
else:
    print('FAIL:' + ', '.join(errors))
" 2>/dev/null > /tmp/_mathviz_bracket_result

BR=$(cat /tmp/_mathviz_bracket_result)
if echo "$BR" | grep -q '^PASS$'; then
  check "括号平衡" "pass"
else
  check "括号平衡" "fail  ($BR)"
fi

# ===== Step 4: 常见陷阱检查 =====
echo ""
echo "🔍 Step 4: 常见陷阱检查"

# 陷阱1: angle 复合元素
python3 -c "
import re
html = open('$HTML').read()
scripts = list(re.finditer(r'<script([^>]*)>(.*?)</script>', html, re.DOTALL))
code = ''
for m in reversed(scripts):
    if 'src=' not in m.group(1).strip():
        code = m.group(2).strip()
        break
count = len(re.findall(r\"create\(\s*\[\s*['\\\"\x60]angle['\\\"\x60]\", code))
print(count)
" 2>/dev/null > /tmp/_mathviz_angle_count
ANGLE_COUNT=$(cat /tmp/_mathviz_angle_count 2>/dev/null || echo "0")

if [ "$ANGLE_COUNT" -gt 0 ]; then
  check "无 angle 复合元素" "fail  ($ANGLE_COUNT处，建议改用arc+text)"
else
  check "无 angle 复合元素" "pass"
fi

# 陷阱2: suspendUpdate/unsuspendUpdate
if grep -q 'suspendUpdate\|unsuspendUpdate' "$HTML" 2>/dev/null; then
  check "无危险API调用" "fail  (suspendUpdate/unsuspendUpdate)"
else
  check "无危险API调用" "pass"
fi

# 陷阱3: CSS 传对象
if grep -q "'CSS'[[:space:]]*:" "$HTML" 2>/dev/null; then
  check "CSS属性安全" "fail  (text的CSS只接受字符串class名)"
else
  check "CSS属性安全" "pass"
fi

# 陷阱4: 括号缺失模式检查
python3 -c "
import re
html = open('$HTML').read()
scripts = list(re.finditer(r'<script([^>]*)>(.*?)</script>', html, re.DOTALL))
code = ''
for m in reversed(scripts):
    if 'src=' not in m.group(1).strip():
        code = m.group(2).strip()
        break
# 统计 create(...) 调用和对应的闭合数
creates = len(re.findall(r'create\s*\(\s*\[', code))
close_paren = len(re.findall(r'\]\s*\)\s*;', code))
# 这只是一个粗略检查
if creates > 0:
    print(f'create()调用: {creates}, 闭合: {close_paren}')
else:
    print('NO_CREATE')
" 2>/dev/null > /tmp/_mathviz_create_result
check "create()调用统计" "pass  ($(cat /tmp/_mathviz_create_result))"

# ===== 汇总 =====
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 验证结果: $PASS 通过 / $FAIL 失败"
if [ "$FAIL" -eq 0 ]; then
  echo "✅ 所有自动化检查通过"
  echo ""
  echo "⚠️  仍需手动确认:"
  echo "   1. 浏览器打开页面，确认图形正常渲染"
  echo "   2. 拖动交互元素，确认动画流畅无残留"
  echo "   3. 数据面板数值与数学推理一致"
  exit 0
else
  echo "❌ $FAIL 项检查未通过，需要在交付前修复"
  exit 1
fi
