#!/usr/bin/env bash
# selftest.sh — 技能自测：生成链路 + 签名链路 + 错误拦截
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"
PY="${PYTHON:-python3}"
SC="$PY bin/sc"
CERT_DIR="${SC_CERT_DIR:-$DIR/certs}"
export SC_CERT_DIR="$CERT_DIR"   # 所有子调用认同一个证书目录
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
pass=0; fail=0
ok()   { printf '  ✓ %s\n' "$1"; pass=$((pass+1)); }
bad()  { printf '  ✗ %s\n' "$1"; fail=$((fail+1)); }
chk()  { if eval "$2"; then ok "$1"; else bad "$1"; fi }

echo "== 1. 环境与证书"
if $SC doctor >/dev/null 2>&1; then ok "doctor 通过"; else bad "doctor 未通过（没跑 sc init？）"; fi
chk "doctor 报出实际证书目录" '$SC doctor 2>&1 | grep -qF "$CERT_DIR"'
chk "key.bin 是 97 字节" '[ "$(stat -c%s "$CERT_DIR/key.bin" 2>/dev/null || echo 0)" = "97" ]'
chk "签名证书带 Apple OID" 'openssl x509 -in "$CERT_DIR/sign.crt" -noout -text 2>/dev/null | grep -q 1.2.840.113635.100.18.1'
chk "证书链是 2 张" '[ "$($PY -c "import plistlib;print(len(plistlib.load(open(\""$CERT_DIR/auth.plist"\",\"rb\"))[\"SigningCertificateChain\"]))" 2>/dev/null)" = "2" ]'

echo "== 2. 动作目录"
n=$($SC catalog --json | $PY -c 'import json,sys;print(len(json.load(sys.stdin)))')
chk "目录共 26 个动作（实际 $n）" '[ "$n" = "26" ]'
chk "按关键词可检索" '$SC catalog --grep 通知 | grep -q notify'

echo "== 3. 示例配方全部可编译"
for f in examples/*.json; do
  base=$(basename "$f" .json)
  if $SC build "$f" --no-sign -o "$TMP/$base.shortcut" >/dev/null 2>&1; then
    ok "$base 编译通过"
  else
    bad "$base 编译失败"
  fi
done

echo "== 4. 产物结构"
if $PY - "$TMP" <<'EOF'
import plistlib, sys, pathlib
tmp = pathlib.Path(sys.argv[1])
exp = {"pill-reminder": 2, "low-battery-guard": 8, "clip-to-note": 3, "quick-scene": 8, "arrived-home": 6}
ctrl = {"is.workflow.actions.conditional", "is.workflow.actions.repeat.count",
        "is.workflow.actions.repeat.each", "is.workflow.actions.choosefrommenu"}
bad = 0
for name, want in exp.items():
    p = tmp / f"{name}.shortcut"
    if not p.is_file():
        print(f"  ✗ {name} 没产物"); bad += 1; continue
    d = plistlib.load(open(p, "rb"))
    acts = d["WFWorkflowActions"]
    opens = sum(1 for a in acts if a["WFWorkflowActionIdentifier"] in ctrl
                and a.get("WFWorkflowActionParameters", {}).get("WFControlFlowMode") == 0)
    closes = sum(1 for a in acts if a["WFWorkflowActionIdentifier"] in ctrl
                 and a.get("WFWorkflowActionParameters", {}).get("WFControlFlowMode") == 2)
    top = [a for a in acts if "UUID" in a or "GroupingIdentifier" in a]
    if len(acts) != want:
        print(f"  ✗ {name} 动作数 {len(acts)}，应为 {want}"); bad += 1
    elif opens != closes:
        print(f"  ✗ {name} 控制流不配对 {opens}/{closes}"); bad += 1
    elif top:
        print(f"  ✗ {name} UUID 落在顶层，会被导入器裁切"); bad += 1
    else:
        print(f"  ✓ {name} {len(acts)} 动作，控制流 {opens}/{closes}，canonical OK")
sys.exit(1 if bad else 0)
EOF
then pass=$((pass+5)); else fail=$((fail+1)); fi

echo "== 5. 签名链路"
if $SC build examples/pill-reminder.json -o "$TMP/SignTest.shortcut" >"$TMP/sign.log" 2>&1; then
  ok "生成+签名一次通过"
else
  bad "生成或签名失败"; sed -n '1,10p' "$TMP/sign.log"
fi
chk "签名件存在" '[ -f "$TMP/SignTest-signed.shortcut" ]'
chk "签名前后动作数一致" 'grep -q "一致" "$TMP/sign.log"'
chk "签名件能被签名器读取" './bin/shortcut-sign info -i "$TMP/SignTest-signed.shortcut" 2>&1 | grep -qi "Certificate"'

echo "== 6. adopt：认证书 / 沿用名字 / 起名"
same=$("$PY" bin/sc adopt "$TMP/SignTest-signed.shortcut" --dry-run 2>&1)
chk "认得出样本与本机是同一张证书" 'grep -q "同一张证书" <<< "$same"'
chk "同一张时明确说不用重装" 'grep -q "不用再装" <<< "$same"'

COPY="$TMP/skill"
cp -a "$DIR" "$COPY"; rm -rf "$COPY/certs" "$COPY/out"
NOKEYS="$TMP/nokeys"   # 副本用空目录，模拟「本机还没有证书」
aout=$(SC_CERT_DIR="$NOKEYS" "$PY" "$COPY/bin/sc" adopt "$TMP/SignTest-signed.shortcut" --dry-run 2>&1)
chk "无证书时沿用样本里的 CA 名" 'grep -q "沿用它的 CA 名" <<< "$aout"'
ca_cn=$(openssl x509 -in "$CERT_DIR/ca.crt" -noout -subject -nameopt utf8 2>/dev/null | sed 's/.*CN *= *//')
chk "沿用的名字与本机 CA 一致（$ca_cn）" 'grep -qF "$ca_cn" <<< "$aout"'
chk "讲明私钥不跟着文件走" 'grep -q "私钥不会跟着" <<< "$aout"'

uout=$(SC_CERT_DIR="$NOKEYS" "$PY" "$COPY/bin/sc" adopt "$TMP/pill-reminder.shortcut" --dry-run 2>&1)
chk "未签名件按快捷指令名起名" 'grep -q "PillReminder CA" <<< "$uout"'
chk "起名时说明为什么（不含证书）" 'grep -q "不含证书" <<< "$uout"'

bout=$(SC_CERT_DIR="$NOKEYS" "$PY" "$COPY/bin/sc" adopt "https://www.icloud.com/shortcuts/zzz" 2>&1)
chk "坏链接给出可操作提示" 'grep -q "正确形态" <<< "$bout"'

SC_CERT_DIR="$NOKEYS" "$PY" "$COPY/bin/sc" init --cn "另一套CA" >/dev/null 2>&1
SC_CERT_DIR="$NOKEYS" "$PY" "$COPY/bin/sc" build "$COPY/examples/pill-reminder.json" -o "$TMP/Other.shortcut" >/dev/null 2>&1
if [ -f "$TMP/Other-signed.shortcut" ]; then
  cout=$("$PY" bin/sc adopt "$TMP/Other-signed.shortcut" --dry-run 2>&1)
  chk "外来证书时指出不是同一张" 'grep -q "不是同一张" <<< "$cout"'
  chk "外来证书时给出二选一" 'grep -q "加 --force" <<< "$cout"'
else
  bad "第二套证书没造出来，跳过冲突用例"
fi

echo "== 7. 错误配方必须被拦住"
t() { # name, json
  printf '%s' "$2" > "$TMP/bad.json"
  if $SC build "$TMP/bad.json" --no-sign -o "$TMP/bad.shortcut" >/dev/null 2>&1; then
    bad "$1（本该报错却通过了）"
  else
    ok "$1 被拦住"
  fi
}
t "未知动作" '{"name":"A","steps":[{"do":"teleport"}]}'
t "未知参数键" '{"name":"A","steps":[{"do":"notify","WFWrongKey":"x"}]}'
t "未知变量" '{"name":"A","steps":[{"do":"notify","WFNotificationActionBody":"{foo}"}]}'
t "中文 name" '{"name":"每日提醒","steps":[{"do":"vibrate"}]}'
t "非法条件" '{"name":"A","steps":[{"do":"if","subject":"x","op":"差不多","value":"1","then":[]}]}'
t "空配方" '{"name":"A","steps":[]}'

echo "== 8. 特殊实现的动作（这几个曾经整段崩过）"
sp() { # name, json
  printf '%s' "$2" > "$TMP/sp.json"
  if $SC build "$TMP/sp.json" --no-sign -o "$TMP/sp.shortcut" >/dev/null 2>&1; then
    ok "$1 能生成"
  else
    bad "$1 生成失败"
  fi
}
sp "clipboard.set 写文本" '{"name":"A","steps":[{"do":"clipboard.set","WFInput":"你好"}]}'
sp "clipboard.set 写引用" '{"name":"A","steps":[{"do":"clipboard.set","WFInput":{"ref":"clipboard"}}]}'
sp "reminder.add" '{"name":"A","steps":[{"do":"reminder.add","WFCalendarItemTitle":"买牛奶"}]}'
sp "shortcut.run" '{"name":"A","steps":[{"do":"shortcut.run","name":"每日打卡"}]}'
sp "script.run" '{"name":"A","steps":[{"do":"script.run","name":"天气"}]}'

echo "== 9. 验签命令（曾经假通过，必须守住）"
chk "已签名件验签返回 0" './bin/sc verify "$TMP/SignTest-signed.shortcut" >/dev/null 2>&1'
if ./bin/sc verify "$TMP/pill-reminder.shortcut" >"$TMP/v.log" 2>&1; then
  bad "未签名件本该验签失败（假通过回归）"
else
  ok "未签名件验签失败，不再假通过"
fi
chk "未签名件说清原因" 'grep -q "不是签名件" "$TMP/v.log"'
if ./bin/sc verify "$TMP/nothing.shortcut" >/dev/null 2>&1; then
  bad "不存在的文件本该报错"
else
  ok "不存在的文件被拒绝"
fi

echo "== 10. 短信收件人校验（填联系人名会静默失败）"
printf '%s' '{"name":"A","steps":[{"do":"sms.send","WFSendMessageActionRecipients":"老婆","WFSendMessageContent":"到家了"}]}' > "$TMP/sms1.json"
if $SC build "$TMP/sms1.json" --no-sign -o "$TMP/sms1.shortcut" >"$TMP/sms1.log" 2>&1; then
  ok "填联系人名不阻断生成"
else
  bad "填联系人名不该直接失败"
fi
chk "但会警告发不出去" 'grep -q "不像号码" "$TMP/sms1.log"'
printf '%s' '{"name":"A","steps":[{"do":"sms.send","WFSendMessageActionRecipients":"13800138000","WFSendMessageContent":"到家了"}]}' > "$TMP/sms2.json"
$SC build "$TMP/sms2.json" --no-sign -o "$TMP/sms2.shortcut" >"$TMP/sms2.log" 2>&1
chk "正常号码不误报" '! grep -q "不像号码" "$TMP/sms2.log"'

echo "== 11. 发布元数据"
chk "frontmatter 有 examples_zh" 'grep -q "^examples_zh:" SKILL.md'
chk "frontmatter 有 display_name" 'grep -q "^display_name:" SKILL.md'
chk "动作手册存在" '[ -f references/actions.md ]'
chk "手册与注册表动作数一致" '[ "$(grep -c "^### \`" references/actions.md)" = "26" ]'
# 个人信息残留由 package.sh 在打包时把关（它扫全包，且不会扫到自己）

echo
echo "结果：$pass 通过 / $fail 失败"
[ "$fail" -eq 0 ]
