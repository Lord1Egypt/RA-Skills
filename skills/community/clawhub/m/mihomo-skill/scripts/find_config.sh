#!/usr/bin/env bash
# mihomo 环境勘察：不管内核跑在本机 / 远程 Linux / Docker / 软路由 / NAS / 桌面客户端，
# 都先用它查清「形态、配置路径、控制接口、密钥」四件事，再决定怎么改。
#
# 用法:
#   bash find_config.sh                                # 本机（裸机 / systemd / 桌面客户端）
#   bash find_config.sh --ssh root@192.168.1.1         # 远程主机、软路由、VPS
#   bash find_config.sh --docker mihomo                # 配置在容器里（可叠加 --ssh）
#   bash find_config.sh --unc                          # 绿联 NAS（unc CLI 已登录）
#   bash find_config.sh --api http://host:9090         # 只探控制接口
#
# 常见可选项: --host <IP>  指定内核所在主机（NAS/容器模式自动推断）
# 输出末尾给出可直接复制的 diagnose.sh / apply_config.sh 命令行。
# 依赖: bash + curl；本机/SSH 模式额外用到 ps/ss/lsof 中任意一个

set -uo pipefail
CURL=/usr/bin/curl
[ -x "$CURL" ] || CURL=curl

MODE=local; SSH=""; CONTAINER=""; HOST=""; APIGIVEN=""
while [ $# -gt 0 ]; do
  case "$1" in
    --ssh) MODE=docker_or_local; SSH="$2"; shift 2;;
    --docker) MODE=docker; CONTAINER="$2"; shift 2;;
    --unc) MODE=unc; shift;;
    --container) CONTAINER="$2"; shift 2;;
    --host) HOST="$2"; shift 2;;
    --api) APIGIVEN="$2"; shift 2;;
    -h|--help) sed -n '2,16p' "$0"; exit 0;;
    *) echo "未知参数: $1" >&2; exit 2;;
  esac
done
# --ssh 与 --docker 的组合：有 CONTAINER 才是 docker 模式
if [ "$MODE" = docker_or_local ]; then
  [ -n "$CONTAINER" ] && MODE=docker || MODE=ssh
fi

q()  { printf "'%s'" "$(printf '%s' "$1" | sed "s/'/'\\\\''/g")"; }
rrun() {  # 在目标主机的 shell 里执行一段命令（local / ssh）
  if [ "$MODE" = ssh ]; then
    ssh -o BatchMode=yes -o ConnectTimeout=8 "$SSH" "bash -lc $(q "$1")" 2>/dev/null
  else
    bash -c "$1" 2>/dev/null
  fi
}
doc() {  # 调 docker（local 或 ssh 远端）
  if [ "$MODE" = ssh ]; then
    local s="docker" a
    for a in "$@"; do s="$s $(q "$a")"; done
    ssh -o BatchMode=yes -o ConnectTimeout=8 "$SSH" "$s" 2>/dev/null
  else
    docker "$@" 2>/dev/null
  fi
}
has_unc() { command -v unc >/dev/null 2>&1; }
hr() { printf '%s\n' "------------------------------------------------------------"; }
sec() { hr; echo "[$1] $2"; }

echo "============================================================"
echo " mihomo 环境勘察   $(date '+%Y-%m-%d %H:%M:%S')"
case "$MODE" in
  local)  echo " 模式: 本机" ;;
  ssh)    echo " 模式: ssh://$SSH" ;;
  docker) echo " 模式: docker 容器 $CONTAINER ${SSH:+(via ssh://$SSH)}" ;;
  unc)    echo " 模式: 绿联 NAS (unc)" ;;
esac
echo "============================================================"

# ---------- 1. 运行形态 ----------
sec 1 "运行形态"
case "$MODE" in
  unc)
    has_unc || echo "  ✗ 找不到 unc 命令，先安装并登录绿联连接器"
    unc docker ps -f table 2>/dev/null | head -1
    unc docker ps -f table 2>/dev/null | grep -i -E 'mihomo|clash' | cut -c1-110 | sed 's/^/  /'
    [ -z "$CONTAINER" ] && CONTAINER=$(unc docker ps -f table 2>/dev/null | awk 'NR>1 && tolower($0) ~ /mihomo|clash/ {print $1; exit}')
    [ -z "$HOST" ] && HOST=$(unc network iface ls -f table 2>/dev/null | awk 'NR>1{for(i=1;i<=NF;i++) if($i ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\//){split($i,a,"/");print a[1];exit}}')
    echo "  → 容器: ${CONTAINER:-未识别}   NAS IP: ${HOST:-未识别}"
    ;;
  docker)
    [ -z "$CONTAINER" ] && CONTAINER=$(doc ps --format '{{.Names}}|{{.Image}}' | grep -i -E 'mihomo|clash' | head -1 | cut -d'|' -f1)
    doc inspect --format '  容器 {{.Name}} | 镜像 {{.Config.Image}} | 网络 {{.HostConfig.NetworkMode}} | 重启 {{.HostConfig.RestartPolicy.Name}}' "$CONTAINER"
    echo "  启动参数: $(doc inspect --format '{{json .Config.Cmd}} {{json .Config.Entrypoint}}' "$CONTAINER")"
    doc inspect --format '{{range .Mounts}}  挂载 {{.Source}} -> {{.Destination}}{{println}}{{end}}' "$CONTAINER"
    echo "  → 容器: $CONTAINER"
    ;;
  *)
    echo "  系统: $(rrun 'uname -s')"
    CT=$(rrun "docker ps --format '{{.Names}}|{{.Image}}|{{.Status}}' | grep -iE 'mihomo|clash|meta'" | head -3)
    if [ -n "$CT" ]; then
      echo "  检测到 docker 容器（配置可能在里面，可改用 --docker <名字>）:"
      printf '%s\n' "$CT" | awk -F'|' '{printf "    %-22s %-38s %s\n",$1,$2,$3}'
    fi
    SVC=$(rrun "systemctl list-units --type=service --no-legend 2>/dev/null | grep -iE 'mihomo|clash' | head -3")
    [ -n "$SVC" ] && { echo "  systemd 服务:"; printf '%s\n' "$SVC" | cut -c1-110 | sed 's/^/    /'; }
    APP=$(rrun "ps -Ao pid,command 2>/dev/null | grep -iE '[C]lash Verge|[C]lashX|[M]ihomo Party|[C]lash Nyanpasu' | head -2")
    [ -n "$APP" ] && { echo "  桌面客户端:"; printf '%s\n' "$APP" | cut -c1-110 | sed 's/^/    /'; }
    ;;
esac

# ---------- 2. 内核进程 / 启动参数 ----------
if [ "$MODE" = local ] || [ "$MODE" = ssh ]; then
  sec 2 "内核进程与启动参数（-d 配置目录 / -f 配置文件）"
  PSLINE=$(rrun "ps -eo pid,args 2>/dev/null | grep -iE '[m]ihomo|[c]lash' | head -3")
  [ -z "$PSLINE" ] && PSLINE=$(rrun "ps -Axo pid,command 2>/dev/null | grep -iE '[m]ihomo|[c]lash' | head -3")
  DDIR=""; DFILE=""
  if [ -n "$PSLINE" ]; then
    printf '%s\n' "$PSLINE" | cut -c1-150 | sed 's/^/  /'
    DDIR=$(printf '%s\n' "$PSLINE" | sed -n 's/.*[[:space:]]-d[[:space:]]\{1,\}\([^[:space:]]*\).*/\1/p' | head -1)
    DFILE=$(printf '%s\n' "$PSLINE" | sed -n 's/.*[[:space:]]-f[[:space:]]\{1,\}\([^[:space:]]*\).*/\1/p' | head -1)
    [ -n "$DDIR" ] && echo "  -d 目录: $DDIR"
    [ -n "$DFILE" ] && echo "  -f 文件: $DFILE"
  else
    echo "  未见内核进程（可能在容器内 / 未启动 / 无权限查看）"
    DDIR=""; DFILE=""
  fi
else
  sec 2 "内核进程"
  echo "  ${MODE} 模式下无 shell 权限（unc 无 exec），跳过进程检查，改由容器信息与 REST API 判断"
  DDIR=""; DFILE=""
fi

# ---------- 3. 配置路径 ----------
sec 3 "配置路径"
FOUND=""
read_cfg() {
  case "$MODE" in
    unc)   unc file cat "$1" -f raw 2>/dev/null ;;
    docker) doc exec "$CONTAINER" cat "$1" ;;
    *)     rrun "cat $(q "$1")" ;;
  esac
}
exists_cfg() {
  case "$MODE" in
    unc)   [ -n "$(unc file cat "$1" -f raw 2>/dev/null | head -c 1)" ] ;;
    docker) doc exec "$CONTAINER" test -f "$1" ;;
    *)     rrun "[ -f $(q "$1") ] && echo y" | grep -q y ;;
  esac
}

CANDS=""
case "$MODE" in
  unc)
    PRJ=$(unc docker compose ls -f table 2>/dev/null | grep -i -E 'mihomo|clash' | awk '{print $NF; exit}')
    [ -z "$PRJ" ] && PRJ=$(unc docker compose ls -f json 2>/dev/null | grep -oE '"/[^"]+"' | tr -d '"' | grep -i -E 'mihomo|clash' | head -1)
    # 返回的可能是 docker-compose.yaml 本体，取目录
    case "$PRJ" in *.yaml|*.yml) PRJ=$(dirname "$PRJ");; esac
    echo "  compose 项目目录: ${PRJ:-未识别}"
    [ -n "$PRJ" ] && CANDS="$PRJ/config/config.yaml $PRJ/config.yaml $PRJ/mihomo/config.yaml $PRJ/conf/config.yaml"
    ;;
  docker)
    M=$(doc inspect --format '{{range .Mounts}}{{.Destination}}{{"\n"}}{{end}}' "$CONTAINER" | grep -iE 'mihomo|clash|config' | head -6)
    for d in $M; do CANDS="$CANDS $d/config.yaml $d"; done
    CMDL=$(doc inspect --format '{{json .Config.Cmd}}' "$CONTAINER")
    for f in $(printf '%s' "$CMDL" | tr -d '[]",' | tr ' ' '\n'); do
      case "$f" in *.yaml|*.yml|*/) CANDS="$CANDS $f";; esac
    done
    ;;
  *)
    [ -n "$DFILE" ] && CANDS="$CANDS $DFILE"
    [ -n "$DDIR" ] && CANDS="$CANDS $DDIR/config.yaml $DDIR/config.yml"
    CANDS="$CANDS /etc/mihomo/config.yaml /etc/mihomo/config.yml \
/etc/clash/config.yaml /opt/clash/config.yaml \
/root/.config/mihomo/config.yaml /root/.config/clash/config.yaml \
$HOME/.config/mihomo/config.yaml $HOME/.config/clash/config.yaml \
/etc/openclash/config.yaml"
    ;;
esac

for c in $CANDS; do
  [ -z "$c" ] && continue
  if exists_cfg "$c"; then
    SZ=$(read_cfg "$c" | wc -c | tr -d ' ')
    printf "  ✓ %-56s %s 字节\n" "$c" "$SZ"
    [ -z "$FOUND" ] && FOUND="$c"
  fi
done
[ -z "$FOUND" ] && echo "  （没找到 → 用 --docker/--unc 指定形态，或手动确认挂载路径后传 --path）"

# ---------- 4. 控制接口 ----------
sec 4 "控制接口探测（对 /version 逐个试）"
CFG=""; [ -n "$FOUND" ] && CFG=$(read_cfg "$FOUND")
yval() { printf '%s\n' "$CFG" | sed -n "s/^$1:[[:space:]]*//p" | head -1 | sed 's/[[:space:]]*#.*$//' | tr -d "\"' " ; }
CTRL=$(yval external-controller)
CPORT=9090
[ -n "$CTRL" ] && CPORT="${CTRL##*:}"

BASE_CANDS=""
[ -n "$APIGIVEN" ] && BASE_CANDS="$APIGIVEN"
[ -n "$HOST" ] && for p in "$CPORT" 9090 9091 9097; do BASE_CANDS="$BASE_CANDS http://$HOST:$p"; done
for p in "$CPORT" 9090 9091 9092 9093 9097 6170; do BASE_CANDS="$BASE_CANDS http://127.0.0.1:$p"; done

APIURL=""
for b in $(printf '%s\n' $BASE_CANDS | sort -u); do
  out=$($CURL -s -m 2 --noproxy '*' -w '\n%{http_code}' "$b/version" 2>/dev/null)
  code=$(printf '%s\n' "$out" | tail -1); body=$(printf '%s\n' "$out" | sed '$d')
  case "$body" in
    *'"version"'*)
      echo "  ✓ $b  →  $body"
      [ -z "$APIURL" ] && APIURL="$b" ;;
    *) [ "$code" = "401" ] && { echo "  ! $b  →  401：是控制接口但需要 secret"; [ -z "$APIURL" ] && APIURL="$b"; } ;;
  esac
done
[ -z "$APIURL" ] && echo "  （未发现控制接口 → 内核可能没开 external-controller，或端口被防火墙挡住）"

# ---------- 5. 关键配置项 ----------
sec 5 "关键配置项"
SECRETV=""
if [ -n "$FOUND" ]; then
  SECRETV=$(yval secret)
  [ -n "$CTRL" ] && echo "  external-controller: $CTRL"
  printf '%s\n' "$CFG" | grep -E '^(mixed-port|port|socks-port|mode|log-level|allow-lan|ipv6|external-ui):' | sed 's/^/  /'
  [ -n "$SECRETV" ] && echo "  secret: $SECRETV   ← 凭证，勿外传"
  echo "  proxy-providers:"
  printf '%s\n' "$CFG" | awk '/^proxy-providers:/{f=1;next} /^[a-z-]+:/{f=0} f && /^  [^ #]/{sub(/:.*/,"");printf "    %s\n",$1}' | head -10
  echo "  proxy-groups:"
  printf '%s\n' "$CFG" | awk '/^proxy-groups:/{f=1;next} /^[a-z-]+:/{f=0} f && /^  - name:/{v=substr($0,index($0,"name:")+6); sub(/[[:space:]]*#.*/,"",v); printf "    %s\n",v}' | head -10
  BAKS=""
  if [ "$MODE" = unc ]; then
    BAKS=$(unc file ls "$(dirname "$FOUND")" 2>/dev/null \
           | grep -oE '"name": *"[^"]+"' | sed -E 's/.*"name": *"([^"]+)"/\1/' \
           | grep -E 'bak' | tr '\n' ' ')
  else
    BAKS=$(rrun "ls -1 $(q "$(dirname "$FOUND")") 2>/dev/null | grep bak" | tr '\n' ' ')
  fi
  [ -n "$BAKS" ] && echo "  同目录备份: $BAKS"
else
  echo "  （没找到配置，跳过）"
fi

# ---------- 6. 下一步 ----------
hr; echo "下一步（复制即用）："
[ -z "$APIURL" ] && APIURL="http://${HOST:-127.0.0.1}:${CPORT}"
CSEC=""; [ -n "$SECRETV" ] && CSEC="--secret '$SECRETV'"
XPORT=""
[ -n "$SSH" ] && XPORT="--ssh $SSH"
[ -n "$CONTAINER" ] && XPORT="$XPORT --container $CONTAINER"
case "$MODE" in unc) XPORT="$XPORT --unc";; esac

echo "  1) 体检:   bash scripts/diagnose.sh --api $APIURL $CSEC"
echo "  2) 改配置: bash scripts/apply_config.sh --new ./new.yaml \\"
echo "                --path ${FOUND:-<配置路径>} --mode $MODE $XPORT \\"
echo "                --restart auto --api $APIURL $CSEC"
if [ "$MODE" = unc ]; then
  echo "  3) 看日志: unc docker logs $CONTAINER --format raw | tail -50"
elif [ "$MODE" = docker ]; then
  echo "  3) 看日志: docker logs --tail 50 $CONTAINER"
else
  echo "  3) 看日志: journalctl -u mihomo -n 50   或   docker logs --tail 50 <容器>"
fi
echo "  桌面客户端（Clash Verge Rev / Mihomo Party / ClashX Meta）改的是 profile 文件，"
echo "  不要直接改运行时生成的 config.yaml —— 下次切订阅就被覆盖。"
hr
