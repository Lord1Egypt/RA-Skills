#!/usr/bin/env bash
# mihomo 配置落盘器：把新配置写到目标机，自动备份 + SHA 校验 + 重载/重启 + 给出回滚命令。
# 同一套流程适配 本机 / SSH 远程 / Docker 容器 / 绿联 NAS(unc)，不依赖特定平台。
#
# 用法:
#   bash apply_config.sh --new ./new.yaml --path /etc/mihomo/config.yaml
#   bash apply_config.sh --new ./new.yaml --path /opt/mihomo/config.yaml --ssh root@10.0.0.2 \
#        --restart 'systemctl restart mihomo'
#   bash apply_config.sh --new ./new.yaml --path /root/.config/mihomo/config.yaml \
#        --mode docker --container mihomo --restart api --api http://127.0.0.1:9090 --secret 'xxx'
#   bash apply_config.sh --new ./new.yaml --path /volume3/docker/compose/mihomo/config/config.yaml \
#        --mode unc --container mihomo-clash-meta
#   bash apply_config.sh --rollback config.yaml.bak-20261111-2100 --path ... --mode ...
#
# 关键选项:
#   --mode local|ssh|docker|unc   local 默认；ssh 用 --ssh；docker/unc 用 --container
#   --restart auto|none|api|docker|unc|'<shell cmd>'
#                api = PUT /configs 热重载（不重启进程，但 external-controller/port/tun 改动不会生效）
#   --core-path PATH   内核进程看到的配置路径（默认同 --path；docker 模式一般就是容器内路径）
#   --skip-validate    跳过 YAML 语法校验（不建议）
#   --dry-run          只打印将要执行的命令，不做任何写操作
#
# 退出码: 0 成功 / 2 参数错误 / 3 校验失败 / 4 写入或校验不通过

set -uo pipefail
CURL=/usr/bin/curl; [ -x "$CURL" ] || CURL=curl
TS=$(date '+%Y%m%d-%H%M%S')

NEW=""; PATH_=""; MODE="local"; SSH=""; CONTAINER=""; COREPATH=""
RESTART="auto"; API=""; SECRET=""; ROLLBACK=""; DRYRUN=0; SKIPVAL=0

while [ $# -gt 0 ]; do
  case "$1" in
    --new) NEW="$2"; shift 2;;
    --path) PATH_="$2"; shift 2;;
    --mode) MODE="$2"; shift 2;;
    --ssh) MODE="ssh"; SSH="$2"; shift 2;;
    --container) CONTAINER="$2"; shift 2;;
    --docker) MODE="docker"; CONTAINER="$2"; shift 2;;
    --unc) MODE="unc"; shift;;
    --core-path) COREPATH="$2"; shift 2;;
    --restart) RESTART="$2"; shift 2;;
    --api) API="$2"; shift 2;;
    --secret) SECRET="$2"; shift 2;;
    --rollback) ROLLBACK="$2"; shift 2;;
    --dry-run) DRYRUN=1; shift;;
    --skip-validate) SKIPVAL=1; shift;;
    -h|--help) sed -n '2,26p' "$0"; exit 0;;
    *) echo "未知参数: $1" >&2; exit 2;;
  esac
done

die() { echo "✗ $*" >&2; exit "${2:-2}"; }
q() { printf "'%s'" "$(printf '%s' "$1" | sed "s/'/'\\\\''/g")"; }
sha() { if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1; else shasum -a 256 "$1" | cut -d' ' -f1; fi; }
hr() { printf '%s\n' "------------------------------------------------------------"; }
say() { echo "  $*"; }
run_or_show() { if [ "$DRYRUN" = 1 ]; then echo "  [dry-run] $*"; else eval "$@"; fi; }

# ---- 参数体检 ----
[ -n "$PATH_" ] || die "--path 必填（配置文件的绝对路径）"
[ -z "$ROLLBACK" ] && { [ -n "$NEW" ] || die "--new 必填（或用 --rollback 回滚）"; [ -f "$NEW" ] || die "找不到文件 $NEW"; }
[ -n "$COREPATH" ] || COREPATH="$PATH_"
case "$MODE" in
  local|ssh|docker|unc) ;;
  *) die "--mode 只能是 local|ssh|docker|unc";;
esac
[ "$MODE" = ssh ] && [ -z "$SSH" ] && die "ssh 模式需要 --ssh user@host"
{ [ "$MODE" = docker ] || [ "$MODE" = unc ]; } && [ -z "$CONTAINER" ] && die "$MODE 模式需要 --container <名字>"

# ---- 传输层 ----
rsh() {  # 在目标主机执行命令字符串
  if [ "$MODE" = ssh ]; then ssh -o BatchMode=yes -o ConnectTimeout=8 "$SSH" "bash -lc $(q "$1")"
  else bash -c "$1"; fi
}
doc() {
  if [ "$MODE" = ssh ]; then
    local s="docker" a; for a in "$@"; do s="$s $(q "$a")"; done
    ssh -o BatchMode=yes -o ConnectTimeout=8 "$SSH" "$s"
  else docker "$@"; fi
}
read_target() {
  case "$MODE" in
    unc)    unc file cat "$1" -f raw 2>/dev/null ;;
    docker) doc exec "$CONTAINER" cat "$1" ;;
    *)      rsh "cat $(q "$1")" ;;
  esac
}
restart_target() {
  case "$MODE" in
    unc)    unc docker restart "$CONTAINER" --yes ;;
    docker) doc restart "$CONTAINER" ;;
    *)      rsh "systemctl restart ${CONTAINER:-mihomo} 2>/dev/null || true" ;;
  esac
}

echo "============================================================"
echo " mihomo 配置落盘   $(date '+%Y-%m-%d %H:%M:%S')"
echo " 模式: $MODE ${SSH:+(ssh://$SSH)} ${CONTAINER:+(容器 $CONTAINER)}"
echo " 目标: $PATH_"
[ "$DRYRUN" = 1 ] && echo " ***** DRY-RUN：只打印，不写盘 *****"
echo "============================================================"

# ---- 回滚分支 ----
if [ -n "$ROLLBACK" ]; then
  RDIR=$(dirname "$PATH_"); RB="$ROLLBACK"
  case "$RB" in /*) ;; *) RB="$RDIR/$RB";; esac      # 裸文件名补成绝对路径，否则 unc 解析不到共享目录
  BRK="$(basename "$PATH_").broken-$TS"
  hr; echo "[回滚] $RB  →  $PATH_"
  okrb=1
  case "$MODE" in
    unc)
      if [ "$DRYRUN" = 1 ]; then
        echo "  [dry-run] unc file mv '$PATH_' '$BRK' --yes"
        echo "  [dry-run] unc file mv '$RB' '$(basename "$PATH_")' --yes"
      else
        unc file mv "$PATH_" "$BRK" --yes >/tmp/_mh_rb.log 2>&1 || say "（当前配置不存在或改不动，继续直接覆盖）"
        unc file mv "$RB" "$(basename "$PATH_")" --yes >/tmp/_mh_rb2.log 2>&1 || { cat /tmp/_mh_rb2.log; okrb=0; }
      fi ;;
    docker)
      if [ "$DRYRUN" = 1 ]; then
        echo "  [dry-run] doc exec $CONTAINER cp '$PATH_' '$RDIR/$BRK'"
        echo "  [dry-run] doc exec $CONTAINER cp '$RB' '$PATH_'"
      else
        doc exec "$CONTAINER" cp "$PATH_" "$RDIR/$BRK" >/dev/null 2>&1 || say "（当前配置不存在，继续）"
        doc exec "$CONTAINER" cp "$RB" "$PATH_" >/dev/null 2>&1 || okrb=0
      fi ;;
    *)
      if [ "$DRYRUN" = 1 ]; then
        echo "  [dry-run] rsh cp -p '$PATH_' '$RDIR/$BRK'"
        echo "  [dry-run] rsh cp -p '$RB' '$PATH_'"
      else
        rsh "cp -p $(q "$PATH_") $(q "$RDIR/$BRK")" 2>/dev/null || say "（当前配置不存在，继续）"
        rsh "cp -p $(q "$RB") $(q "$PATH_")" 2>/dev/null || okrb=0
      fi ;;
  esac
  [ "$okrb" = 1 ] || die "回滚失败 —— 配置可能仍缺失，手工把 $RB 改名回 $PATH_" 4
  say "✓ 已恢复"
  hr; echo "[重启] $RESTART"
  case "$RESTART" in
    none) say "跳过" ;;
    api)  run_or_show "$CURL -s -X PUT -H 'Content-Type: application/json' ${SECRET:+-H 'Authorization: Bearer $SECRET'} -d '{\"path\": \"$COREPATH\"}' '$API/configs'" ;;
    unc|docker|auto) run_or_show restart_target ;;
    *) run_or_show "$RESTART" ;;
  esac
  hr; echo "✓ 回滚完成"
  exit 0
fi

# ---- 1. 校验 YAML ----
hr; echo "[1] 校验新配置"
if [ "$SKIPVAL" = 1 ]; then say "已跳过（--skip-validate）"
else
  okv=0
  if command -v python3 >/dev/null 2>&1 && python3 -c 'import yaml' >/dev/null 2>&1; then
    if python3 - "$NEW" >/tmp/_mh_valout 2>/tmp/_mh_valerr <<'PYV'
import sys, yaml
try:
    d = yaml.safe_load(open(sys.argv[1], encoding='utf-8'))
    assert isinstance(d, dict), "顶层不是键值映射"
    print("  YAML OK：顶层键 %d 个" % len(d))
except Exception as e:
    print(type(e).__name__ + ": " + str(e).replace(chr(10), " ")[:180], file=sys.stderr)
    sys.exit(1)
PYV
    then cat /tmp/_mh_valout; okv=1; else cat /tmp/_mh_valerr; fi
  elif command -v ruby >/dev/null 2>&1; then
    if ruby -ryaml -e 'begin; d=YAML.load_file(ARGV[0]); puts "  YAML OK：顶层键 #{d.size} 个"; rescue => e; warn e.message; exit 1; end' "$NEW" >/tmp/_mh_valout 2>/tmp/_mh_valerr
    then cat /tmp/_mh_valout; okv=1; else cat /tmp/_mh_valerr; fi
  else
    say "! 没有 PyYAML 也没有 ruby，无法校验语法，继续（风险自负）"
    okv=1
  fi
  [ "$okv" = 0 ] && die "语法错误就别往线上写 —— 会让容器反复重启" 3
fi
NEWSHA=$(sha "$NEW"); NEWSZ=$(wc -c < "$NEW" | tr -d ' ')
say "本地: $NEWSZ 字节  SHA=$(printf '%s' "$NEWSHA" | cut -c1-16)…"

# ---- 2. 备份 ----
hr; echo "[2] 备份原配置"
BAKNAME="$(basename "$PATH_").bak-$TS"
if [ "$MODE" = unc ]; then
  # unc 的上传不覆盖同名文件，所以"备份=改名"，腾出目标位置
  if [ "$DRYRUN" = 1 ]; then
    echo "  [dry-run] unc file mv '$PATH_' '$BAKNAME' --yes"
  else
    if ! unc file mv "$PATH_" "$BAKNAME" --yes >/tmp/_mh_mv.log 2>&1; then
      # 同名备份已存在（同一秒重复执行）→ 换后缀重试一次
      BAKNAME="$(basename "$PATH_").bak-$TS-$(printf '%02d' $((RANDOM%100)))"
      unc file mv "$PATH_" "$BAKNAME" --yes >/tmp/_mh_mv.log 2>&1 || { cat /tmp/_mh_mv.log; die "备份失败（目标文件可能不存在或同名冲突）" 4; }
    fi
  fi
  say "已改名备份: $BAKNAME"
else
  case "$MODE" in
    docker) run_or_show "doc exec $CONTAINER cp $(q "$PATH_") $(q "$(dirname "$PATH_")/$BAKNAME")" ;;
    *)      run_or_show "rsh \"cp -p $(q "$PATH_") $(q "$(dirname "$PATH_")/$BAKNAME")\"" ;;
  esac
  say "已备份到: $(dirname "$PATH_")/$BAKNAME"
fi

# ---- 3. 写入 ----
hr; echo "[3] 写入新配置"
case "$MODE" in
  unc)
    if [ "$DRYRUN" = 1 ]; then echo "  [dry-run] unc file upload $NEW $PATH_ --verify"
    else unc file upload "$NEW" "$PATH_" --verify >/tmp/_mh_up.log 2>&1 || { cat /tmp/_mh_up.log; die "上传失败" 4; }; fi
    ;;
  docker)
    if [ "$DRYRUN" = 1 ]; then echo "  [dry-run] cat $NEW | doc exec -i $CONTAINER sh -c 'cat > $PATH_'"
    else doc exec -i "$CONTAINER" sh -c "cat > $PATH_" < "$NEW" || die "写入失败" 4; fi
    ;;
  ssh)
    echo "  [ssh] 写入 $SSH:$PATH_"
    [ "$DRYRUN" = 1 ] || { ssh -o BatchMode=yes "$SSH" "cat > $(q "$PATH_")" < "$NEW" || die "写入失败" 4; }
    ;;
  local)
    if [ "$DRYRUN" = 1 ]; then echo "  [dry-run] cat $NEW > $PATH_"
    else cat "$NEW" > "$PATH_" || die "写入失败（权限？试试 sudo）" 4; fi
    ;;
esac
say "已写入"

# ---- 4. 校验落地 ----
hr; echo "[4] 回读校验"
if [ "$DRYRUN" = 1 ]; then echo "  [dry-run] 回读比对 SHA"; else
  read_target "$PATH_" > /tmp/_mh_back.yaml 2>/dev/null
  RSHA=$(sha /tmp/_mh_back.yaml); RSZ=$(wc -c < /tmp/_mh_back.yaml | tr -d ' ')
  say "远端: $RSZ 字节  SHA=$(printf '%s' "$RSHA" | cut -c1-16)…"
  if [ "$RSHA" != "$NEWSHA" ]; then
    echo "  ✗ SHA 不一致，文件没真正落地！先别重启，排查后再动。"
    echo "    回滚: bash $0 --rollback '$BAKNAME' --path '$PATH_' --mode $MODE ${SSH:+--ssh $SSH} ${CONTAINER:+--container $CONTAINER} --restart auto"
    exit 4
  fi
  say "✓ SHA 一致，确认落地"
fi

# ---- 5. 重载 / 重启 ----
hr; echo "[5] 让配置生效（${RESTART}）"
DO="$RESTART"
if [ "$DO" = auto ]; then
  case "$MODE" in
    unc|docker) DO=$MODE ;;
    *) if [ -n "$API" ]; then DO=api; else DO=systemd; fi ;;
  esac
  say "auto → $DO"
fi
case "$DO" in
  none) say "跳过（--restart none）。记得自己重启内核" ;;
  api)
    [ -n "$API" ] || die "--restart api 需要 --api http://host:9090" 2
    if [ "$DRYRUN" = 1 ]; then echo "  [dry-run] PUT $API/configs {\"path\":\"$COREPATH\"}"
    else
      code=$($CURL -s -o /tmp/_mh_reload.txt -w '%{http_code}' -m 20 -X PUT \
        -H 'Content-Type: application/json' ${SECRET:+-H "Authorization: Bearer $SECRET"} \
        -d "{\"path\": \"$COREPATH\"}" "$API/configs")
      say "热重载 HTTP=$code $(head -c 120 /tmp/_mh_reload.txt)"
      [ "$code" = "204" ] || [ "$code" = "200" ] || say "! 非 2xx：内核可能没权限读该路径，改用重启模式"
    fi
    say "注意: 热重载不改变 external-controller / port / tun 这类启动参数，改过这些必须重启"
    ;;
  unc) if [ "$DRYRUN" = 1 ]; then echo "  [dry-run] unc docker restart '$CONTAINER' --yes"
       else unc docker restart "$CONTAINER" --yes >/tmp/_mh_rs.log 2>&1 && say "已重启" || { cat /tmp/_mh_rs.log; say "! 重启失败"; }; fi ;;
  docker) run_or_show "doc restart $(q "$CONTAINER")" ;;
  systemd) run_or_show "rsh \"systemctl restart mihomo\"" ;;
  *) run_or_show "$DO" ;;
esac

# ---- 6. 收尾 ----
hr; echo "✓ 完成"
echo "  回滚: bash $0 --rollback '$BAKNAME' --path '$PATH_' --mode $MODE ${SSH:+--ssh $SSH} ${CONTAINER:+--container $CONTAINER} --restart $DO"
case "$MODE" in
  unc)    echo "  日志: unc docker logs $CONTAINER --format raw | tail -40" ;;
  docker) echo "  日志: docker logs --tail 40 $CONTAINER" ;;
  *)      echo "  日志: journalctl -u mihomo -n 40 --no-pager   或   docker logs --tail 40 <容器>" ;;
esac
echo "  复检: bash scripts/diagnose.sh --api ${API:-http://127.0.0.1:9090} ${SECRET:+--secret '$SECRET'}"
hr
