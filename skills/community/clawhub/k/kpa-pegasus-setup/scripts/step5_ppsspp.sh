#!/bin/bash
# step5: PPSSPP 优化：拷贝 PSP ROM 到应用可读目录 + ppsspp.ini（拉伸满屏/关虚拟键）+ PSP metadata launch 行（幂等）
source "$(dirname "$0")/kpa_env.sh"
require_device

GOLD="$KPA_SKILL_DIR/assets/golden"
PPS_FILES="$INT/Android/data/$PPS_PKG/files"

# 5.1 ppsspp.ini（含 DisplayStretch 满屏、ShowTouchControls=False）
if sh "test -f $PPS_FILES/PSP/SYSTEM/ppsspp.ini && grep -q 'DisplayStretch' $PPS_FILES/PSP/SYSTEM/ppsspp.ini"; then
  echo "SKIP  ppsspp.ini 已是优化配置"
else
  sh "mkdir -p $PPS_FILES/PSP/SYSTEM"
  bak "$PPS_FILES/PSP/SYSTEM/ppsspp.ini" .bakKPA3
  "$ADB" push "$GOLD/ppsspp.ini.txt" "$PPS_FILES/PSP/SYSTEM/ppsspp.ini" || die "ppsspp.ini 推送失败"
  echo "OK    ppsspp.ini 已部署（满屏拉伸 + 关闭虚拟键）"
fi

# 5.2 PSP ROM 拷贝（TF 卡 ROM 与 PPSSPP 目录不互通，是 Android 分区存储限制）
# 注意：内置 files/ 那份才是游戏本体；TF 卡副本只供天马 file: 索引，
#       去重时可用 .app 占位替代（见 HARD_RULES 38/40、PLAYBOOK §12.8 / §13）
if sh "test -f $TF/Roms/PSP/metadata.pegasus.txt" | grep -q ""; then :; fi
sh "ls $TF/Roms/PSP/ 2>/dev/null | grep -iE '\.(iso|cso|pbp)$'" > /tmp/kpa_psp_roms.txt
n=$(wc -l < /tmp/kpa_psp_roms.txt | tr -d ' ')
if [ "$n" = "0" ]; then
  echo "SKIP  TF 卡没有 PSP ROM（可能已用 .app 占位去重）"
else
  copied=0
  while IFS= read -r rom; do
    [ -z "$rom" ] && continue
    if ! sh "test -f '$PPS_FILES/$rom'"; then
      echo "COPY  $rom（大文件，请耐心）"
      "$ADB" pull "$TF/Roms/PSP/$rom" "/tmp/kpa_psp_tmp" >/dev/null 2>&1 && \
      "$ADB" push "/tmp/kpa_psp_tmp" "$PPS_FILES/$rom" >/dev/null && \
      sh "chmod 666 '$PPS_FILES/$rom'"
      rm -f /tmp/kpa_psp_tmp
      copied=$((copied+1))
    fi
  done < /tmp/kpa_psp_roms.txt
  echo "OK    PSP ROM 已从 TF 卡拷入内置 files/（本次新拷 $copied 个）"
fi
rm -f /tmp/kpa_psp_roms.txt

# 5.3 PSP metadata launch：⛔ 禁止 -d "file://..."（天马构造 Intent 会触发 FileUriExposedException）
# 只就地改 launch 行，不整份覆盖（保留用户自定义简介 / 封面）；幂等，可重复运行修复旧配置。
META=/tmp/kpa_psp_meta.txt
"$ADB" pull "$TF/Roms/PSP/metadata.pegasus.txt" "$META" >/dev/null 2>&1 || { echo "SKIP  PSP metadata 不存在"; echo "step5 done"; exit 0; }
cp "$META" "$META.bak"
python3 - "$META" <<'PY'
import re, sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
files = '/storage/emulated/0/Android/data/org.ppsspp.ppsspp/files'
pat = re.compile(r'launch: am start --user 0 -a android\.intent\.action\.VIEW -d "file://([^"]+)" -n org\.ppsspp\.ppsspp/\.PpssppActivity')
def conv(m):
    path = m.group(1)
    if '/Roms/PSP/' in path:            # 旧版曾把 launch 指向 TF 卡，PPSSPP 读不到
        path = files + '/' + path.rsplit('/', 1)[-1]
    return ('launch: am start --user 0 -n org.ppsspp.ppsspp/.PpssppActivity '
            '--es "org.ppsspp.ppsspp.Shortcuts" "' + path + '"')
s, n = pat.subn(conv, s)
# collection 级兜底：去掉 file:// URI，避免 {file.path} 再触发异常
s = s.replace('launch: am start --user 0 -a android.intent.action.VIEW -d "file://{file.path}" -n org.ppsspp.ppsspp/.PpssppActivity',
              'launch: am start --user 0 -n org.ppsspp.ppsspp/.PpssppActivity')
# 新装机器：没有 per-game launch 时按真实 ROM 的 file: 生成 extra 版（.app 占位不生成）
if n == 0 and '--es "org.ppsspp.ppsspp.Shortcuts"' not in s:
    out = []
    for line in s.splitlines(True):
        out.append(line)
        if line.startswith('file: '):
            fname = line[6:].strip()
            if fname.lower().endswith(('.iso', '.cso', '.pbp')):
                out.append('launch: am start --user 0 -n org.ppsspp.ppsspp/.PpssppActivity '
                           '--es "org.ppsspp.ppsspp.Shortcuts" "' + files + '/' + fname + '"\n')
    s = ''.join(out)
    n = 1
open(p, 'w', encoding='utf-8').write(s)
print('RESULT psp_launch_fixed=%d file_uri_left=%d' % (n, s.count('file://')))
PY
"$ADB" push "$META" "$TF/Roms/PSP/metadata.pegasus.txt" >/dev/null
rm -f "$META" "$META.bak"
sh "rm -f /sdcard/pegasus-frontend/dataCache.json"
echo "OK    PSP launch 已统一为 shortcut extra；请重启天马并从前端逐条点击验证（PLAYBOOK §13）"
echo "step5 done"
