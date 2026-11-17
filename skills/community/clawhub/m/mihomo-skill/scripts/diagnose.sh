#!/usr/bin/env bash
# mihomo 一体体检：结构 → 节点 → 分流 → 连通性，一次跑完并给出结论。
# 与部署形态无关：本机、远程主机、Docker、软路由、NAS 都能用，只要能访问控制接口。
#
# 用法:
#   bash diagnose.sh --api http://192.168.1.2:9090 --secret 'xxx'
#   bash diagnose.sh --api http://127.0.0.1:9090            # secret 可留空
#   bash diagnose.sh --api http://host:9090 --proxy http://host:7890   # 手动指定代理端口
#   bash diagnose.sh --api http://host:9090 --skip-external # 只查结构，不做外网实测
#
# 代理端口无需指定：脚本会读 /configs 的 mixed-port / port / socks-port 并逐个试通。
# 所有探测都带 --noproxy '*'，避免被本机 HTTP_PROXY 环境变量误导。
# 依赖: curl、python3

set -uo pipefail
CURL=/usr/bin/curl; [ -x "$CURL" ] || CURL=curl
PY=/usr/bin/python3; [ -x "$PY" ] || PY=python3

API="http://127.0.0.1:9090"; SECRET=""; PROXY=""; SKIPEXT=0
while [ $# -gt 0 ]; do
  case "$1" in
    --api) API="$2"; shift 2;;
    --secret) SECRET="$2"; shift 2;;
    --proxy) PROXY="$2"; shift 2;;
    --skip-external) SKIPEXT=1; shift;;
    -h|--help) sed -n '2,14p' "$0"; exit 0;;
    *) echo "未知参数: $1" >&2; exit 2;;
  esac
done
API="${API%/}"

HP="${API#http://}"; HP="${HP#https://}"; HP="${HP%%/*}"
case "$HP" in *:*) : ;; *) HP="$HP:9090";; esac
AHOST="${HP%:*}"

AUTH=()
[ -n "$SECRET" ] && AUTH=(-H "Authorization: Bearer $SECRET")
api()   { $CURL -s -m 8 --noproxy '*' ${AUTH[@]+"${AUTH[@]}"} "$API$1"; }
hr()    { printf '%s\n' "------------------------------------------------------------"; }
ok()    { printf '  \033[32m✓\033[0m %s\n' "$1"; }
bad()   { printf '  \033[31m✗\033[0m %s\n' "$1"; }
warn()  { printf '  \033[33m!\033[0m %s\n' "$1"; }
try()   { $CURL -s -o /dev/null -m "${3:-10}" -w '%{http_code} %{time_total}' -x "$PROXY" "$2" 2>/dev/null; }
conn()  { $CURL -s -o /dev/null -m "${3:-10}" --noproxy '*' -w '%{http_code} %{time_total}' "$2" 2>/dev/null; }

# 是否内网/本机地址（决定"局域网直连"这一项是否有意义）
case "$AHOST" in
  localhost|127.*|10.*|192.168.*|172.1[6-9].*|172.2[0-9].*|172.3[01].*|::1) PRIVATE=1;;
  *) PRIVATE=0;;
esac

echo "============================================================"
echo " mihomo 体检报告   $(date '+%Y-%m-%d %H:%M:%S')"
echo " API : $API"
[ "$PRIVATE" = 1 ] && echo " 类型: 内网/本机" || echo " 类型: 公网/远端"
echo "============================================================"

# ---------- 1. 内核与端口 ----------
hr; echo "[1] 内核与端口"
VER=$(api /version)
if [ -z "$VER" ] || ! printf '%s' "$VER" | grep -q version; then
  bad "控制接口无响应（${API}）"
  echo "    依次排查："
  echo "      1) 容器/进程在跑吗        docker ps | grep mihomo   /   systemctl status mihomo"
  echo "      2) external-controller 是否 0.0.0.0:9090（只写 127.0.0.1 时外部连不上）"
  echo "      3) secret 是否正确（错误 secret 返回 401）"
  echo "      4) 端口是否被防火墙/安全组挡"
  echo "      5) 全 000 → 先 bash find_config.sh 确认地址"
  exit 1
fi
ok "内核: $(printf '%s' "$VER" | tr -d '\n')"

CFG_JSON=$(api /configs)
echo "$CFG_JSON" > /tmp/_mh_configs.json
MODEV=$($PY -c "import json;d=json.load(open('/tmp/_mh_configs.json'));print(d.get('mode','?'))" 2>/dev/null)
$PY - <<'PY' 2>/dev/null
import json
try: d=json.load(open('/tmp/_mh_configs.json'))
except Exception: raise SystemExit
ks=[('mixed-port','混合'),('port','HTTP'),('socks-port','SOCKS'),('redir-port','REDIR'),('tproxy-port','TPROXY')]
print("  配置端口: " + "  ".join(f"{lb}={d.get(k) or '-'}" for k,lb in ks))
print("  allow-lan=%s  log-level=%s  tun=%s" % (d.get('allow-lan'), d.get('log-level'), (d.get('tun') or {}).get('enable')))
PY
[ "$MODEV" = "global" ] && warn "mode=global：所有流量都走同一条，分流规则不生效（要用规则改成 rule）"

# 自动挑一个能用的代理端口
if [ -z "$PROXY" ]; then
  CANDS=$($PY -c "
import json
d=json.load(open('/tmp/_mh_configs.json'))
for k in ('mixed-port','port','socks-port'):
    v=d.get(k) or 0
    if v: print(v)
" 2>/dev/null)
  [ -z "$CANDS" ] && CANDS="7890 7891 7893"
  for p in $CANDS; do
    r=$(try "$p" https://www.baidu.com 6); c="${r%% *}"
    if [ "$c" = "200" ]; then PROXY="http://$AHOST:$p"; ok "可用代理端口: ${p}（实测国内 200）"; break; fi
  done
  [ -z "$PROXY" ] && { PROXY="http://$AHOST:$(printf '%s' "$CANDS" | awk '{print $1}')"; warn "自动测端口都失败，暂用 $PROXY"; }
else
  ok "代理端口（指定）: $PROXY"
fi

# ---------- 2. 策略组 ----------
hr; echo "[2] 策略组结构"
api /proxies > /tmp/_mh_proxies.json
$PY - /tmp/_mh_proxies.json <<'PY'
import json,sys
try: d=json.load(open(sys.argv[1]))['proxies']
except Exception: print("  读取失败"); raise SystemExit
G=('Selector','URLTest','Fallback','LoadBalance')
for k,v in d.items():
    if v.get('type') in G:
        print("  [%-9s] %-14s now=%-18s 候选=%d" % (v['type'],k,str(v.get('now'))[:18],len(v.get('all') or [])))
print()
flag=0
for k,v in d.items():
    if v.get('type')=='Fallback':
        kids=v.get('all') or []
        sub=[c for c in kids if d.get(c,{}).get('type') in G]
        if sub:
            flag=1
            print("  ! '%s' 是 fallback 但子项含策略组 %s" % (k,sub))
            print("    mihomo 会判它不可用，启动瞬间锁死后备项且不自愈 →")
            print("    改成 select + 顶部 url-test(use: 多 provider) 混池，fallback 只接真实节点")
import re as _re
SKIP=_re.compile(r'GLOBAL|直连|DIRECT|国内|本地|LAN|Private|局域网', _re.I)
for k,v in d.items():
    if v.get('type') in ('Selector','Fallback','URLTest') and str(v.get('now'))=='DIRECT' and not SKIP.search(k):
        print("  ! '%s' 当前指向 DIRECT：需要走代理的流量实际没出去（节点全挂，或手动切过）" % k)
if not flag: print("  ✓ 未发现 fallback 嵌套策略组的错误用法")
PY

# ---------- 3. providers ----------
hr; echo "[3] 订阅 provider"
api /providers/proxies > /tmp/_mh_prov.json
$PY - /tmp/_mh_prov.json <<'PY'
import json,sys,datetime
try: d=json.load(open(sys.argv[1])).get('providers',{})
except Exception: print("  读取失败"); raise SystemExit
bad=0
for k,v in d.items():
    if v.get('type') not in ('Proxy',): continue
    if v.get('vehicleType')=='Compatible': continue
    ps=v.get('proxies') or []
    alive=[p for p in ps if p.get('alive')]
    upd=v.get('updatedAt') or ''
    age=""
    try:
        t=datetime.datetime.fromisoformat(upd.replace('Z','+00:00'))
        n=datetime.datetime.now(t.tzinfo)
        h=(n-t).total_seconds()/3600
        age="  (%.1f 小时前)" % h if h<48 else "  (%.1f 天前)" % (h/24)
    except Exception: pass
    flag=""
    if ps and not alive: flag="   <<< 全部失效"; bad+=1
    elif not ps: flag="   <<< 未加载"; bad+=1
    print("  %-16s 节点=%-3d 存活=%-3d 更新=%s%s%s" % (k,len(ps),len(alive),upd[:19] or '-',age,flag))
print()
if bad: print("  → 用 scripts/probe_sub.py <订阅URL> 判断是 DNS污染/TCP阻断/SNI阻断/服务端拒绝 哪一类")
PY

# ---------- 4. 直连基线 vs 经代理 ----------
hr; echo "[4] 直连基线 vs 经代理（同一目标对照）"
printf '  %-26s %-20s %-20s\n' "目标" "直连" "经代理"
cmp1() {
  local label="$1" url="$2" d p dc pc mark=""
  d=$(conn 0 "$url" 10); dc="${d%% *}"
  p=$(try 0 "$url" 12);  pc="${p%% *}"
  [ "$dc" = "200" ] && [ "$pc" != "200" ] && mark="  ← 直连能通、代理不通"
  [ "$dc" != "200" ] && [ "$pc" = "200" ] && mark="  ← 只有代理能通"
  printf '  %-26s %-20s %-20s%s\n' "$label" "${dc} ${d##* }s" "${pc} ${p##* }s" "$mark"
}
cmp1 "国内 baidu"    "https://www.baidu.com"
cmp1 "国内 163"       "https://www.163.com"
[ "$PRIVATE" = 1 ] && cmp1 "局域网(控制接口)" "$API/version"
if [ "$SKIPEXT" = 0 ]; then
  cmp1 "境外 gstatic" "https://www.gstatic.com/generate_204"
  cmp1 "境外 google"  "https://www.google.com"
  cmp1 "境外 github"  "https://github.com"
  cmp1 "境外 youtube" "https://www.youtube.com"
fi

# ---------- 5. 出口 ----------
hr; echo "[5] 出口 IP"
# 只用"通常会被判走代理"的查询站；命中 GEOIP,CN 直连规则是正常的，
# 所以不能拿"出口 == 直连"当代理失效的证据。
eip() { local u r; for u in https://ipinfo.io/ip https://ipv4.icanhazip.com https://api.ipify.org https://ifconfig.me/ip; do
    r=$($CURL -s -m 8 --noproxy '*' ${1:+-x "$1"} "$u" 2>/dev/null | tr -d '\r' | head -1)
    printf '%s' "$r" | grep -qE '^([0-9]{1,3}\.){3}[0-9]{1,3}$|:' && { printf '%s' "$r"; return; }
  done; }
DIP=$(eip "")
EIP=$(eip "$PROXY")
[ -n "$DIP" ] && echo "  直连出口: $DIP"
if [ -z "$EIP" ]; then
  warn "经代理拿不到出口 IP（查询站可能被判直连、或被节点拒绝），以 [4] 里境外结果为准"
elif [ "$EIP" = "$DIP" ]; then
  warn "经代理出口 $EIP 与直连相同 → 该域名命中了直连规则（GEOIP,CN 常见），不代表代理失效"
  echo "    判断代理是否可用请看 [4]：google / youtube 走代理是否 200"
else
  ok "经代理出口: $EIP（与直连不同，确认流量走了节点）"
fi

# ---------- 6. 结论 ----------
hr; echo "结论自查（按顺序对号入座）："
echo "  1) 国内/局域网 200 且几十毫秒，境外 200 → 分流与节点都正常"
echo "  2) 国内正常、境外全 000/超时 → 节点这一段的问题：看 [3] 存活数，全 0 就跑 probe_sub.py"
echo "  3) 直连也失败（两边都 000）→ 不是 mihomo 的问题，先查本机网络/DNS"
echo "  4) 有存活节点但境外不通 → 看 [2] 里哪个组 now=DIRECT 或指向死节点"
echo "  5) 出口 IP 与直连相同 → 该域名被判直连（GEOIP,CN 先于 MATCH），不是故障"
echo "  6) provider 节点存活却显示未加载 → 订阅拉取失败，多半是 proxy/DNS/SNI"
echo "  7) fallback 子项含策略组、DNS 抢 53 → 按提示改结构，别在症状上打补丁"
hr
